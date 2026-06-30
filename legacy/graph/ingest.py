"""Bootstrap and incremental ingest, extraction, and invalidation.

Each compiled source becomes a document subgraph (handoff.md "Large documents
are document subgraphs"): one document-root absolute node, one absolute node per
leaf source page, and shared global topic nodes. Cross-document linking happens
only through shared topic identity, never page-to-page cliques.

Updates are staged then activated in one transaction: a new source version is
built, prior-version local edges retire, globally supported topics survive, and
dependent synthetic nodes are marked stale (refreshed lazily).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from . import ids
from .llm import LLMClient
from .models import (
    EDGE_TYPES,
    SUBTYPE_DOCUMENT,
    SUBTYPE_SOURCE_PAGE,
    SUBTYPE_TOPIC,
    CompiledDocument,
    CompiledSourcePage,
    Edge,
    Evidence,
    Node,
)
from .policy import DEFAULT_POLICY, Policy
from .source_tree import discover_compiled_documents, read_compiled_document
from .store import Store


class Ingestor:
    def __init__(
        self,
        store: Store,
        llm: Optional[LLMClient] = None,
        policy: Optional[Policy] = None,
    ):
        self.store = store
        self.llm = llm
        self.policy = policy or Policy(dict(DEFAULT_POLICY))
        self._external_edges_remaining = 0

    # ----------------------------------------------------------------- API

    def bootstrap(self, output_parent: Path | str) -> list[str]:
        """Ingest every compiled tree under output/. Returns document ids."""
        done: list[str] = []
        for root in discover_compiled_documents(output_parent):
            doc = read_compiled_document(root)
            self.ingest_document(doc, created_by="bootstrap")
            done.append(doc.document_id)
        return done

    def ingest_document(self, doc: CompiledDocument, created_by: str = "ingest") -> str:
        """Stage + activate a document version as one catalog transaction."""
        if not doc.exact_coverage():
            raise RuntimeError(
                f"refusing to ingest {doc.document_id}: coverage not validated"
            )

        sid = ids.source_id(doc.document_id)
        vid = ids.version_id(doc.document_id, doc.source_sha256)
        prev_vid = self.store.active_version(sid)
        is_update = prev_vid is not None and prev_vid != vid
        self._external_edges_remaining = int(
            self.policy.get("max_external_edges_per_document", 25)
        )

        with self.store.transaction():
            self.store.upsert_source(
                sid, str(doc.source_path), doc.title, source_type="markdown"
            )
            self.store.add_source_version(vid, sid, doc.source_sha256)

            self._build_document_node(doc, vid, created_by)
            for page in doc.source_pages:
                self._build_page_node(doc, page, vid, created_by)

            # Activate the new version atomically.
            self.store.activate_version(sid, vid)

            if is_update:
                self._retire_previous_version(prev_vid, vid)

        return vid

    # ----------------------------------------------------- node builders

    def _build_document_node(
        self, doc: CompiledDocument, vid: str, created_by: str
    ) -> None:
        node = Node(
            id=ids.doc_node_id(doc.document_id),
            node_class="absolute",
            node_subtype=SUBTYPE_DOCUMENT,
            title=doc.title,
            markdown_path=str(doc.output_root / "index.md"),
            source_version_id=vid,
            document_id=doc.document_id,
            section_path=[],
            metadata={
                "document_topics": doc.document_topics,
                "source_line_count": doc.source_line_count,
                "source_path": str(doc.source_path),
                "summary": f"Document {doc.title} ({len(doc.source_pages)} source pages).",
            },
        )
        self.store.upsert_node(node)
        self._index_node(node, body=node.summary)

        # document has_topic -> shared topic nodes (controlled global links).
        # Evidence is the whole document range, so the edge stays evidenced.
        whole = [[1, max(1, doc.source_line_count)]]
        for topic in doc.document_topics[: self._external_edges_remaining]:
            self._link_topic(
                node, topic, doc, ranges=whole, strength=0.6, created_by=created_by
            )

    def _build_page_node(
        self,
        doc: CompiledDocument,
        page: CompiledSourcePage,
        vid: str,
        created_by: str,
    ) -> None:
        node_id = ids.page_node_id(doc.document_id, page.rel_path)
        body = ""
        if page.markdown_path.exists():
            body = page.markdown_path.read_text(encoding="utf-8")
        node = Node(
            id=node_id,
            node_class="absolute",
            node_subtype=SUBTYPE_SOURCE_PAGE,
            title=page.title,
            markdown_path=str(page.markdown_path),
            source_version_id=vid,
            document_id=doc.document_id,
            section_path=page.section_path,
            metadata={
                "summary": page.summary,
                "source_ranges": page.source_ranges,
                "local_topics": page.local_topics,
                "document_topics": doc.document_topics,
            },
        )
        self.store.upsert_node(node)
        self._index_node(node, body=body, aliases=" ".join(page.local_topics))

        # document contains -> page (structural, full strength, evidenced)
        evidence = [
            Evidence(
                source_version_id=vid,
                document_id=doc.document_id,
                source_ranges=page.source_ranges,
            )
        ]
        self._add_edge(
            ids.doc_node_id(doc.document_id),
            node_id,
            "contains",
            explanation=f"Section path: {' / '.join(page.section_path)}",
            strength=1.0,
            evidence=evidence,
            created_by=created_by,
        )

        # page has_topic -> shared topic nodes (factual, evidenced)
        page_topic_limit = int(self.policy.get("max_external_edges_per_source_page", 8))
        linked_topics = 0
        for topic in page.local_topics[:page_topic_limit]:
            if self._link_topic(
                node,
                topic,
                doc,
                ranges=page.source_ranges,
                strength=0.7,
                created_by=created_by,
            ):
                linked_topics += 1

        self._extract_absolute_facts(
            doc,
            page,
            node,
            body,
            created_by,
            edge_limit=max(0, page_topic_limit - linked_topics),
        )

    def _link_topic(
        self,
        from_node: Node,
        topic: str,
        doc: CompiledDocument,
        ranges: list[list[int]],
        strength: float,
        created_by: str,
    ) -> bool:
        if self._external_edges_remaining <= 0:
            return False
        tid = ids.topic_node_id(topic)
        existing = self.store.get_node(tid)
        if existing is None:
            tnode = Node(
                id=tid,
                node_class="absolute",
                node_subtype=SUBTYPE_TOPIC,
                title=topic,
                metadata={"summary": topic},
            )
            self.store.upsert_node(tnode)
            self._index_node(tnode, body=topic)
        elif existing.status != "active":
            # a topic referenced again revives from archived/stale
            self.store.set_node_status(tid, "active")
        evidence = [
            Evidence(
                source_version_id=from_node.source_version_id or "",
                document_id=doc.document_id,
                source_ranges=ranges,
            )
        ]
        self._add_edge(
            from_node.id,
            tid,
            "has_topic",
            explanation=f"{from_node.title} discusses {topic}",
            strength=strength,
            evidence=evidence,
            created_by=created_by,
        )
        self._external_edges_remaining -= 1
        return True

    # ------------------------------------------------------- LLM extraction

    def _extract_absolute_facts(
        self,
        doc: CompiledDocument,
        page: CompiledSourcePage,
        page_node: Node,
        body: str,
        created_by: str,
        edge_limit: int,
    ) -> None:
        """Extract evidence-backed absolute nodes/edges when an LLM is enabled.

        Structural ingest remains deterministic when no LLM is requested. With
        `--llm`, this turns document text into the planned concepts, entities,
        code symbols, and typed relationships rather than only topic nodes.
        """
        if not self.llm or not self.llm.available or not body:
            return

        source_ranges = page.source_ranges
        system = (
            "Extract only document-grounded knowledge from one Markdown source page. "
            "Return JSON with `nodes` and `edges`. Node fields: title, subtype, "
            "aliases, summary. Edge fields: from, to, type, explanation, strength, "
            "evidence_ranges. `from` or `to` may be `page` for the source page. "
            "Allowed subtypes include concept, entity, procedure, code_module, "
            "code_symbol, api, and configuration. Allowed edge types include "
            "mentions, supports, explains, applies_to, implements, depends_on, "
            "contradicts, derives_from, and has_topic. Use only facts in the input. "
            "Every edge must cite one or more global source-line ranges."
        )
        user = (
            f"Document: {doc.title}\n"
            f"Document topics: {doc.document_topics}\n"
            f"Section path: {page.section_path}\n"
            f"Allowed global source ranges for this page: {source_ranges}\n\n"
            f"Source page:\n{body}"
        )
        try:
            extracted = self.llm.complete_json(system, user)
        except Exception:
            return
        if not isinstance(extracted, dict):
            return

        name_to_id: dict[str, str] = {
            "page": page_node.id,
            page_node.title.strip().casefold(): page_node.id,
        }
        extracted_node_ids: list[str] = []
        for raw in extracted.get("nodes", []):
            if not isinstance(raw, dict):
                continue
            title = str(raw.get("title", "")).strip()
            if not title:
                continue
            subtype = str(raw.get("subtype", "concept")).strip().lower() or "concept"
            canonical_id = ids.absolute_node_id(subtype, title)
            existing = self.store.get_node(canonical_id)
            aliases = {
                str(alias).strip()
                for alias in raw.get("aliases", [])
                if str(alias).strip()
            }
            aliases.add(title)
            metadata = dict(existing.metadata) if existing else {}
            metadata["aliases"] = sorted(set(metadata.get("aliases", [])) | aliases)
            metadata["summary"] = str(raw.get("summary", "")).strip() or metadata.get(
                "summary", title
            )
            node = Node(
                id=canonical_id,
                node_class="absolute",
                node_subtype=subtype,
                title=title,
                metadata=metadata,
            )
            self.store.upsert_node(node)
            self._index_node(
                node,
                body=node.summary,
                aliases=" ".join(metadata["aliases"]),
            )
            extracted_node_ids.append(canonical_id)
            name_to_id[title.casefold()] = canonical_id
            for alias in aliases:
                name_to_id[alias.casefold()] = canonical_id

        created = 0
        linked_node_ids: set[str] = set()
        for raw in extracted.get("edges", []):
            if created >= edge_limit or self._external_edges_remaining <= 0:
                break
            if not isinstance(raw, dict):
                continue
            src = name_to_id.get(str(raw.get("from", "page")).strip().casefold())
            dst = name_to_id.get(str(raw.get("to", "")).strip().casefold())
            if not src or not dst or src == dst:
                continue
            edge_type = str(raw.get("type", "related")).strip()
            if edge_type not in EDGE_TYPES:
                edge_type = "related"
            ranges = self._valid_evidence_ranges(
                raw.get("evidence_ranges"), source_ranges
            )
            if not ranges:
                continue
            try:
                strength = float(raw.get("strength", 0.5))
            except (TypeError, ValueError):
                strength = 0.5
            self._add_edge(
                src,
                dst,
                edge_type,
                explanation=str(raw.get("explanation", "")).strip()
                or f"Extracted from {page.title}",
                strength=min(1.0, max(0.0, strength)),
                evidence=[
                    Evidence(
                        source_version_id=page_node.source_version_id or "",
                        document_id=doc.document_id,
                        source_ranges=ranges,
                    )
                ],
                created_by=created_by,
            )
            if src != page_node.id:
                linked_node_ids.add(src)
            if dst != page_node.id:
                linked_node_ids.add(dst)
            created += 1
            self._external_edges_remaining -= 1

        # An extraction may identify a node but omit a relationship. Keep that
        # absolute node source-grounded by adding an evidenced page mention,
        # subject to the same per-page/document edge budgets.
        for canonical_id in dict.fromkeys(extracted_node_ids):
            if (
                canonical_id in linked_node_ids
                or created >= edge_limit
                or self._external_edges_remaining <= 0
            ):
                continue
            self._add_edge(
                page_node.id,
                canonical_id,
                "mentions",
                explanation=f"{page.title} identifies {self.store.get_node(canonical_id).title}",
                strength=0.5,
                evidence=[
                    Evidence(
                        source_version_id=page_node.source_version_id or "",
                        document_id=doc.document_id,
                        source_ranges=source_ranges,
                    )
                ],
                created_by=created_by,
            )
            created += 1
            self._external_edges_remaining -= 1

        # Do not leave newly extracted canonical nodes floating without any
        # current source evidence when a page/document edge budget was reached.
        for canonical_id in dict.fromkeys(extracted_node_ids):
            has_support = any(
                edge.has_evidence()
                for edge in self.store.edges_touching(canonical_id, status="active")
            )
            if not has_support:
                self.store.set_node_status(canonical_id, "archived")
                self.store.fts_delete(canonical_id)

    @staticmethod
    def _valid_evidence_ranges(
        raw_ranges: Any, allowed_ranges: list[list[int]]
    ) -> list[list[int]]:
        if not isinstance(raw_ranges, list):
            return []
        valid: list[list[int]] = []
        for item in raw_ranges:
            if not isinstance(item, list) or len(item) != 2:
                continue
            try:
                start, end = int(item[0]), int(item[1])
            except (TypeError, ValueError):
                continue
            if end < start:
                continue
            if any(a <= start <= end <= b for a, b in allowed_ranges):
                valid.append([start, end])
        return valid

    # ------------------------------------------------------------- edges

    def _add_edge(
        self,
        src: str,
        dst: str,
        etype: str,
        explanation: str,
        strength: float,
        evidence: Optional[list[Evidence]] = None,
        dependencies: Optional[list[str]] = None,
        created_by: str = "ingest",
    ) -> None:
        edge = Edge(
            id=ids.edge_id(src, dst, etype),
            src_id=src,
            dst_id=dst,
            type=etype,
            explanation=explanation,
            strength=strength,
            status="active",
            evidence=evidence or [],
            dependencies=dependencies or [],
            created_by=created_by,
        )
        self.store.upsert_edge(edge)

    # ---------------------------------------------------------- indexing

    def _index_node(self, node: Node, body: str = "", aliases: str = "") -> None:
        self.store.fts_index(
            node.id,
            title=node.title,
            aliases=aliases,
            summary=node.summary,
            body=body,
        )

    # ------------------------------------------------------ invalidation

    def _retire_previous_version(self, prev_vid: str, new_vid: str) -> None:
        """Retire prior-version local pages/edges; mark dependents stale.

        A global topic node survives as long as any active source still links to
        it; it is only the prior-version *pages* and their *edges* that retire.
        Synthetic nodes whose dependency closure references the old version go
        stale and are excluded from trusted retrieval until refreshed.
        """
        # retire prior-version source pages / document nodes
        for node in self.store.nodes_by_version(prev_vid):
            if node.node_subtype in (SUBTYPE_SOURCE_PAGE, SUBTYPE_DOCUMENT):
                self.store.set_node_status(node.id, "archived")
                self.store.fts_delete(node.id)
        # retire edges with evidence pointing at the old version
        self.store.set_edge_status_for_version(prev_vid, "stale")
        # mark dependent synthetic nodes stale
        for node in self.store.nodes_by_class("synthetic"):
            deps = node.metadata.get("source_version_fingerprint", [])
            if prev_vid in deps:
                self.store.set_node_status(node.id, "stale")
        # Canonical absolute nodes survive only while current source evidence
        # supports them; document/page nodes are handled above.
        self._prune_unsupported_canonical_nodes()

    def _prune_unsupported_canonical_nodes(self) -> None:
        for node in self.store.nodes_by_class("absolute"):
            if node.node_subtype in (SUBTYPE_SOURCE_PAGE, SUBTYPE_DOCUMENT):
                continue
            active_evidence = [
                edge
                for edge in self.store.edges_touching(node.id, status="active")
                if edge.has_evidence()
            ]
            if not active_evidence:
                self.store.set_node_status(node.id, "archived")
                self.store.fts_delete(node.id)


def ingest_path(
    store: Store,
    output_root: Path | str,
    llm: Optional[LLMClient] = None,
    policy: Optional[Policy] = None,
) -> str:
    """Convenience: ingest a single compiled output/<source>/ tree."""
    doc = read_compiled_document(output_root)
    return Ingestor(store, llm, policy).ingest_document(doc)
