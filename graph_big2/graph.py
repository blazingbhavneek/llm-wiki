"""One class that owns the whole knowledge graph.

`Graph` holds every operation over the graph — ingest (md.py outputs AND the
global output_wiki layout), enrich, embed, semantic edges, query,
revision/cascade, analytics, and the reasoning agent — as methods on a single
object. The only dependencies are the swappable backends (`db` / `embedder` /
`reranker` / `llm`); a `Graph` carries no per-call mutable state, so it is
reusable and the read path is safe to run from worker threads (each subagent
builds its own `Graph` on its own DB connection).
"""

from __future__ import annotations

import json
import logging
import math
import re
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from embeddings import Embedder, Reranker
from llm.agent import AgentClient

# `db` is imported lazily inside the constructor / subagent spawn: `db` imports
# `graph_big2.models`, so importing it at module top would re-enter this package
# mid-load. The lazy import means `graph_big2` never pulls `db` at import time.
if TYPE_CHECKING:
    from .db import Database

from . import core
from .core import make_edge_id, make_exogenous_node_id, make_node_id, source_hash
from .models import (
    AgentAnswer,
    ClaimExtraction,
    Edge,
    EdgeSuggestions,
    EntityMatch,
    GraphStats,
    Keywords,
    Node,
    NodeStatus,
    NodeType,
    QueryResult,
    Settings,
    now_iso,
)
from .utils import (
    LEAD_TOOLS,
    SUBAGENT_TOOLS,
    Subrun,
    clean_node_ref,
    dedupe,
    format_node_full,
    node_ref,
    repair_answer_mermaid,
)

log = logging.getLogger("graph")

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
_NUMBERED_DOC_RE = re.compile(r"^\d+-(.+\.md)$")
_MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
_SOURCE_REF_RE = re.compile(r"\[([A-Za-z0-9_.-]+):L(\d+)-L(\d+)\]")

_CASCADE_MATCH_THRESHOLD = 0.45

# Global output_wiki layout: folder -> (page kind, cluster label).
_WIKI_PAGE_FOLDERS = {
    "entities": ("entity", "Wiki Entities"),
    "concepts": ("concept", "Wiki Concepts"),
    "summaries": ("summary", "Wiki Summaries"),
    "indexes": ("index", "Wiki Indexes"),
}
_GLOBAL_WIKI_DOCUMENT = "global_wiki"


class Graph:
    # region lifecycle
    def __init__(
        self,
        settings: Settings | None = None,
        db: "Database | None" = None,
        embedder: core.EmbedderPort | None = None,
        reranker: core.RerankerPort | None = None,
        llm: core.LlmClient | None = None,
        subagent: bool = False,
    ) -> None:
        """Wire backends; unless this is a subagent, reconcile stored vectors at startup."""
        from .db import Database  # lazy: see the module-level import note

        self.settings = settings or Settings.from_env()
        self.db = db or Database(self.settings.database_path)
        self.embedder = embedder or Embedder(self.settings)
        self.reranker = reranker if reranker is not None else self.build_reranker()
        self.llm = llm or AgentClient(
            model=self.settings.chat_model,
            base_url=self.settings.chat_base_url,
            api_key=self.settings.chat_api_key,
            system_prompt=core.GRAPH_SYSTEM_PROMPT,
            temperature=self.settings.chat_temperature,
        )
        # Subagent graphs are read-only and share the already-synced model; they
        # must never re-embed (it would run once per subagent).
        self.subagent = subagent
        self._vec_ready = False
        self._emit: Callable[[dict[str, Any]], None] = lambda event: None
        if not subagent:
            self.prepare_embeddings()

    def build_reranker(self) -> core.RerankerPort | None:
        """Build the cross-encoder reranker, or None if unavailable (retrieval still works)."""
        try:
            return Reranker(self.settings)
        except Exception as exc:  # noqa: BLE001 - rerank is optional
            log.info("reranker unavailable, continuing without it: %s", exc)
            return None

    def close(self) -> None:
        """Close the database connection."""
        self.db.close()

    def emit_event(self, event_type: str, **fields: Any) -> None:
        """Send one progress event to the current sink, swallowing any sink error."""
        try:
            self._emit({"type": event_type, **fields})
        except Exception:  # noqa: BLE001 - progress events must never break a run
            pass

    # endregion

    # region markdown ingest
    def ingest_md_output(self, md_output_dir: str | Path) -> list[Node]:
        """Ingest a whole md.py / output_wiki dir: build nodes, enrich each, link structure, recluster."""
        nodes, structural_edges = self.load_md_output(md_output_dir)
        version = self.source_version_for_nodes(nodes)

        edge_count = 0
        for index, node in enumerate(nodes, start=1):
            node.source_version = version
            edge_count += len(self.ingest(node))
            log.info(
                "ingest %d/%d | edges so far %d | %s",
                index,
                len(nodes),
                edge_count,
                node.id,
            )

        if nodes:
            self.replace_structural_edges(
                nodes[0].original_document_name, structural_edges
            )
            if nodes[0].original_document_name:
                self.db.record_source(nodes[0].original_document_name, version)

        log.info(
            "ingest done: %d nodes, %d semantic/dedup edges, %d structural",
            len(nodes),
            edge_count,
            len(structural_edges),
        )
        try:
            labels = self.recluster()
            log.info("reclustered into %d topics", len(set(labels.values())))
        except Exception as exc:  # noqa: BLE001 - clustering is non-critical
            log.info("recluster skipped: %s", exc)
        return nodes

    # The generated global wiki is also an md.py output as far as ingest cares;
    # this alias exists for callers/CLI that name the wiki layout explicitly.
    ingest_wiki_output = ingest_md_output

    def load_md_output(self, out_dir: str | Path) -> tuple[list[Node], list[Edge]]:
        """Read one output dir and return ``(nodes, structural_edges)``.

        Dispatches across the three supported layouts: the old manifest.json
        layout, the global output_wiki layout (raw/ + entities|concepts|... +
        _planning page json), and the new _planning + docs/ layout.
        """
        out_path = Path(out_dir)
        if not out_path.exists():
            raise FileNotFoundError(f"input directory does not exist: {out_path}")
        if not out_path.is_dir():
            raise NotADirectoryError(f"input path is not a directory: {out_path}")

        if (out_path / "manifest.json").exists():
            return self.load_old_manifest_output(out_path)
        if self.looks_like_global_wiki_output(out_path):
            return self.load_global_wiki_output(out_path)
        return self.load_new_planning_docs_output(out_path)

    def load_old_manifest_output(self, out_path: Path) -> tuple[list[Node], list[Edge]]:
        """Build nodes + section-adjacency edges from the old manifest.json layout."""
        manifest = json.loads((out_path / "manifest.json").read_text(encoding="utf-8"))
        source_path = manifest.get("source")
        document_name = Path(source_path).name if source_path else out_path.name

        by_filename = {
            r["filename"]: r for r in manifest.get("files", []) if r.get("filename")
        }
        nodes: list[Node] = []
        sections: dict[str, list[str]] = {}
        for filename, record in by_filename.items():
            leaf = out_path / filename
            if not leaf.exists():
                continue
            meta, body = self.split_frontmatter(
                leaf.read_text(encoding="utf-8", errors="ignore")
            )
            if not body:
                continue
            node = Node(
                id=make_node_id(body, document_name),
                body=body,
                type=NodeType.endogenous,
                title=record.get("title") or meta.get("title", ""),
                original_document_name=document_name,
                source_path=source_path,
                source_ranges=self.parse_ranges(record.get("source_ranges"))
                or self.parse_ranges(meta.get("source_lines")),
                summary=record.get("summary") or meta.get("summary", ""),
                cluster=self.humanize(Path(filename).parent.name),
            )
            nodes.append(node)
            sections.setdefault(str(Path(filename).parent), []).append(node.id)

        edges: list[Edge] = []
        for node_ids in sections.values():
            edges += self.chain_edges(
                node_ids, "Adjacent page in the same source section."
            )
        return nodes, edges

    def load_new_planning_docs_output(
        self, out_path: Path
    ) -> tuple[list[Node], list[Edge]]:
        """Build nodes + linear edges from the new _planning + docs/ layout."""
        planning_dir = out_path / "_planning"
        docs_dir = out_path / "docs"
        if not docs_dir.exists():
            raise FileNotFoundError(
                f"no manifest.json and no docs directory found in {out_path}"
            )

        metadata = self.read_json(planning_dir / "metadata.json", default={})
        coverage = self.read_json(planning_dir / "coverage.json", default={})
        document_name = (
            metadata.get("inferred_file_name")
            or metadata.get("original_file_name")
            or out_path.name
        )
        metadata_by_name = {
            i.get("name"): i for i in metadata.get("files", []) if i.get("name")
        }
        coverage_by_name = {
            i.get("filename"): i for i in coverage.get("files", []) if i.get("filename")
        }

        nodes: list[Node] = []
        ordered_ids: list[str] = []
        for md_file in sorted(docs_dir.glob("*.md"), key=self.doc_sort_key):
            meta, body = self.split_frontmatter(
                md_file.read_text(encoding="utf-8", errors="ignore")
            )
            body = body.strip()
            if not body:
                continue
            canonical = self.canonical_doc_name(md_file.name)
            meta_rec = metadata_by_name.get(canonical, {})
            cov_rec = coverage_by_name.get(canonical, {})

            ranges: list[tuple[int, int]] = []
            start, end = cov_rec.get("source_start"), cov_rec.get("source_end")
            if start is not None and end is not None:
                try:
                    ranges = [(int(start), int(end))]
                except (TypeError, ValueError):
                    ranges = []
            else:
                ranges = self.parse_ranges(meta.get("source_lines"))

            node = Node(
                id=make_node_id(body, document_name),
                body=body,
                type=NodeType.endogenous,
                title=(
                    cov_rec.get("title")
                    or meta.get("title")
                    or meta_rec.get("header")
                    or self.title_from_markdown(body)
                    or self.humanize(canonical.removesuffix(".md"))
                ),
                original_document_name=document_name,
                source_path=str(md_file),
                source_ranges=ranges,
                summary=cov_rec.get("summary") or meta.get("summary") or "",
                cluster=cov_rec.get("header") or meta_rec.get("header") or "General",
            )
            nodes.append(node)
            ordered_ids.append(node.id)

        edges = self.chain_edges(ordered_ids, "Next page in the source document.")
        return nodes, edges

    # --- global output_wiki layout --------------------------------------------
    def looks_like_global_wiki_output(self, out_path: Path) -> bool:
        """True for an output_wiki dir: a raw/ source store + page-type folders."""
        if not (out_path / "raw").is_dir():
            return False
        return any((out_path / folder).is_dir() for folder in _WIKI_PAGE_FOLDERS)

    def load_global_wiki_output(self, out_path: Path) -> tuple[list[Node], list[Edge]]:
        """Build source-anchor + wiki-page nodes and citation/link/follows edges."""
        planning_dir = out_path / "_planning"
        page_sources = self.read_json(planning_dir / "page_sources.json", default={})
        page_metadata = self.read_json(planning_dir / "page_metadata.json", default={})
        catalog = self.read_json(planning_dir / "global_catalog.json", default={})
        sources_by_slug = self.extract_page_sources(page_sources)
        metadata_by_slug = self.extract_page_metadata(page_metadata, catalog)

        source_nodes, source_lookup = self.build_wiki_source_nodes(out_path)
        page_nodes, page_files_by_id, page_file_lookup = self.build_wiki_page_nodes(
            out_path=out_path,
            sources_by_slug=sources_by_slug,
            metadata_by_slug=metadata_by_slug,
            source_doc_ids=set(source_lookup),
        )

        nodes = [*source_nodes, *page_nodes]
        edges: list[Edge] = []
        edges.extend(self.wiki_folder_edges(out_path, page_file_lookup))
        edges.extend(
            self.wiki_citation_edges(page_nodes, source_lookup, sources_by_slug)
        )
        edges.extend(self.wiki_markdown_link_edges(page_files_by_id, page_file_lookup))
        log.info(
            "wiki ingest: %d source node(s), %d page node(s), %d edge(s)",
            len(source_nodes),
            len(page_nodes),
            len(edges),
        )
        return nodes, edges

    @staticmethod
    def slug_key(slug: str) -> str:
        """Bare-stem key for slug matching across wiki_gen's mixed slug styles.

        wiki_gen writes planning JSON keyed by the raw page slug, which is
        sometimes bare ("assertion") and sometimes type-prefixed
        ("concept/assertion"); the on-disk file is always ``<folder>/<stem>.md``.
        Collapsing to the part after the last ``/`` makes both styles match the
        folder-derived page slug.
        """
        return slug.rsplit("/", 1)[-1]

    def extract_page_sources(self, payload: Any) -> dict[str, list[dict[str, Any]]]:
        """page_sources.json -> {bare-stem slug: [source ref dicts]}."""
        if not isinstance(payload, dict):
            return {}
        pages = payload.get("pages", {})
        if not isinstance(pages, dict):
            return {}
        out: dict[str, list[dict[str, Any]]] = {}
        for slug, refs in pages.items():
            if isinstance(slug, str) and isinstance(refs, list):
                key = self.slug_key(slug)
                out.setdefault(key, []).extend(
                    ref for ref in refs if isinstance(ref, dict)
                )
        return out

    def extract_page_metadata(
        self, metadata_payload: Any, catalog_payload: Any
    ) -> dict[str, dict[str, Any]]:
        """Merge catalog + page_metadata into {bare-stem slug: metadata dict}."""
        out: dict[str, dict[str, Any]] = {}
        for payload in (catalog_payload, metadata_payload):
            if not isinstance(payload, dict):
                continue
            pages = payload.get("pages", {})
            if isinstance(pages, dict):
                items = pages.items()
            elif isinstance(pages, list):
                items = (
                    (item.get("slug"), item) for item in pages if isinstance(item, dict)
                )
            else:
                continue
            for slug, item in items:
                if isinstance(slug, str) and isinstance(item, dict):
                    out.setdefault(self.slug_key(slug), {}).update(item)
        return out

    def build_wiki_source_nodes(
        self, out_path: Path
    ) -> tuple[list[Node], dict[str, str]]:
        """One anchor node per preserved raw source document; returns (nodes, doc_id->node_id)."""
        raw_dir = out_path / "raw"
        nodes: list[Node] = []
        lookup: dict[str, str] = {}
        if not raw_dir.exists():
            return nodes, lookup

        for doc_dir in sorted(child for child in raw_dir.iterdir() if child.is_dir()):
            doc_id = doc_dir.name
            original = doc_dir / "original.md"
            if not original.exists():
                continue
            coverage = self.read_json(doc_dir / "coverage.json", default={})
            metadata = self.read_json(doc_dir / "metadata.json", default={})
            line_count = self.wiki_source_line_count(original, coverage)
            original_name = (
                metadata.get("inferred_file_name")
                or metadata.get("original_file_name")
                or doc_id
            )
            title = f"Source Document: {original_name}"
            body = self.wiki_source_anchor_body(
                title=title,
                doc_id=doc_id,
                original_path=self.safe_relative(original, out_path),
                line_count=line_count,
                metadata=metadata,
                coverage=coverage,
            )
            node = Node(
                id=make_node_id(body, f"{_GLOBAL_WIKI_DOCUMENT}:source:{doc_id}"),
                body=body,
                type=NodeType.endogenous,
                title=title,
                original_document_name=_GLOBAL_WIKI_DOCUMENT,
                source_path=str(original),
                source_ranges=[(1, line_count)] if line_count else [],
                summary=(
                    f"Preserved original source document `{doc_id}` for global wiki "
                    "citations."
                ),
                cluster="Wiki Source Documents",
                keywords=[doc_id, str(original_name), "source", "original"],
            )
            nodes.append(node)
            lookup[doc_id] = node.id
        return nodes, lookup

    def build_wiki_page_nodes(
        self,
        *,
        out_path: Path,
        sources_by_slug: dict[str, list[dict[str, Any]]],
        metadata_by_slug: dict[str, dict[str, Any]],
        source_doc_ids: set[str],
    ) -> tuple[list[Node], dict[str, Path], dict[Path, str]]:
        """Build a node per wiki page; returns (nodes, node_id->path, path->node_id)."""
        nodes: list[Node] = []
        files_by_id: dict[str, Path] = {}
        node_id_by_path: dict[Path, str] = {}

        for folder, (page_kind, cluster) in _WIKI_PAGE_FOLDERS.items():
            base = out_path / folder
            if not base.exists():
                continue
            for md_file in sorted(base.glob("*.md")):
                slug = self.wiki_slug(folder, md_file)
                key = self.slug_key(slug)
                text = md_file.read_text(encoding="utf-8", errors="ignore")
                source_refs = self.merge_source_refs(
                    sources_by_slug.get(key, []),
                    self.source_refs_from_markdown(
                        text=text, out_path=out_path, source_doc_ids=source_doc_ids
                    ),
                )
                if source_refs:
                    sources_by_slug[key] = source_refs
                node = self.build_wiki_page_node(
                    md_file=md_file,
                    slug=slug,
                    cluster=cluster,
                    source_refs=source_refs,
                    metadata=metadata_by_slug.get(key, {}),
                )
                if node is None:
                    continue
                nodes.append(node)
                files_by_id[node.id] = md_file
                node_id_by_path[md_file.resolve()] = node.id
        return nodes, files_by_id, node_id_by_path

    def build_wiki_page_node(
        self,
        *,
        md_file: Path,
        slug: str,
        cluster: str,
        source_refs: list[dict[str, Any]],
        metadata: dict[str, Any],
    ) -> Node | None:
        """Build one wiki-page node from its markdown file + planning metadata."""
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        meta, body = self.split_frontmatter(text)
        body = body.strip()
        if not body:
            return None

        title = (
            str(metadata.get("title") or "").strip()
            or meta.get("title")
            or self.title_from_markdown(body)
            or self.humanize(md_file.stem)
        )
        summary = (
            str(metadata.get("summary") or "").strip()
            or meta.get("summary")
            or self.first_summary_from_markdown(body)
        )
        aliases = self.string_list(metadata.get("aliases"))
        doc_ids = self.doc_ids_from_refs(source_refs)
        ranges = self.source_ranges_from_refs(source_refs)
        body_for_node = self.append_wiki_reference_section(body, source_refs)
        page_kind = self.slug_kind(slug)
        return Node(
            id=make_node_id(body_for_node, f"{_GLOBAL_WIKI_DOCUMENT}:{slug}"),
            body=body_for_node,
            type=NodeType.endogenous,
            title=title,
            original_document_name=_GLOBAL_WIKI_DOCUMENT,
            source_path=str(md_file),
            source_ranges=ranges,
            summary=summary,
            cluster=cluster,
            keywords=[slug, page_kind, *aliases, *doc_ids],
        )

    def wiki_source_anchor_body(
        self,
        *,
        title: str,
        doc_id: str,
        original_path: str,
        line_count: int,
        metadata: dict[str, Any],
        coverage: dict[str, Any],
    ) -> str:
        """Markdown body for a source-anchor node (the original stays on disk)."""
        lines = [
            f"# {title}",
            "",
            f"Document id: `{doc_id}`.",
            f"Preserved original source: `{original_path}`.",
            f"Global source line range: `L1-L{line_count}`.",
        ]
        original_name = metadata.get("original_file_name")
        inferred_name = metadata.get("inferred_file_name")
        if original_name:
            lines.append(f"Original file name: `{original_name}`.")
        if inferred_name and inferred_name != original_name:
            lines.append(f"Inferred file name: `{inferred_name}`.")
        file_count = coverage.get("file_count")
        if file_count is not None:
            lines.append(f"Chunk artifact count: `{file_count}`.")
        lines.extend(
            [
                "",
                "This node is an anchor for wiki citations; the original document "
                "content remains in the preserved source file rather than being "
                "duplicated inside the graph node.",
            ]
        )
        return "\n".join(lines).strip() + "\n"

    def append_wiki_reference_section(
        self, body: str, source_refs: list[dict[str, Any]]
    ) -> str:
        """Append a Graph Source References section listing the page's citations."""
        if not source_refs:
            return body
        lines = [body.rstrip(), "", "## Graph Source References"]
        for ref in source_refs:
            doc_id = ref.get("doc_id")
            line_start = ref.get("line_start")
            line_end = ref.get("line_end")
            ref_label = ref.get("ref") or (
                f"{doc_id}:L{line_start}-L{line_end}"
                if doc_id and line_start is not None and line_end is not None
                else ""
            )
            source_path = ref.get("source_path")
            rendered = f"- [{ref_label}]" if ref_label else "- Source reference"
            if source_path:
                rendered += f" `{source_path}`"
            lines.append(rendered)
        return "\n".join(lines).strip() + "\n"

    def wiki_folder_edges(
        self, out_path: Path, node_id_by_path: dict[Path, str]
    ) -> list[Edge]:
        """`follows` edges chaining the pages within each wiki folder in name order."""
        edges: list[Edge] = []
        for folder, (_page_kind, cluster) in _WIKI_PAGE_FOLDERS.items():
            base = out_path / folder
            if not base.exists():
                continue
            ordered_ids = [
                node_id_by_path[path.resolve()]
                for path in sorted(base.glob("*.md"))
                if path.resolve() in node_id_by_path
            ]
            edges += self.chain_edges(
                ordered_ids, f"Next page in the {cluster.lower()} section."
            )
        return edges

    def wiki_citation_edges(
        self,
        page_nodes: list[Node],
        source_lookup: dict[str, str],
        sources_by_slug: dict[str, list[dict[str, Any]]],
    ) -> list[Edge]:
        """Bidirectional wiki_cites_source / source_supports_wiki edges per citation."""
        page_id_by_slug = {
            self.slug_key(keyword): node.id
            for node in page_nodes
            for keyword in node.keywords[:1]
            if "/" in keyword
        }
        edges: list[Edge] = []
        for slug, refs in sorted(sources_by_slug.items()):
            page_id = page_id_by_slug.get(slug)
            if not page_id:
                continue
            refs_by_doc: dict[str, list[str]] = {}
            for ref in refs:
                doc_id = ref.get("doc_id")
                if not isinstance(doc_id, str) or doc_id not in source_lookup:
                    continue
                line_start = ref.get("line_start")
                line_end = ref.get("line_end")
                rendered = (
                    f"L{line_start}-L{line_end}"
                    if line_start is not None and line_end is not None
                    else str(ref.get("ref") or "")
                )
                refs_by_doc.setdefault(doc_id, []).append(rendered)

            for doc_id, ranges in sorted(refs_by_doc.items()):
                source_id = source_lookup[doc_id]
                range_text = ", ".join(r for r in ranges if r)
                summary = f"Wiki page `{slug}` cites preserved source `{doc_id}`" + (
                    f" at {range_text}." if range_text else "."
                )
                edges.append(
                    Edge(
                        id=make_edge_id(page_id, source_id, "wiki_cites_source"),
                        source_node_id=page_id,
                        target_node_id=source_id,
                        label="wiki_cites_source",
                        summary=summary,
                    )
                )
                edges.append(
                    Edge(
                        id=make_edge_id(source_id, page_id, "source_supports_wiki"),
                        source_node_id=source_id,
                        target_node_id=page_id,
                        label="source_supports_wiki",
                        summary=summary,
                    )
                )
        return edges

    def wiki_markdown_link_edges(
        self, page_files_by_id: dict[str, Path], node_id_by_path: dict[Path, str]
    ) -> list[Edge]:
        """`wiki_links_to` edges from inline markdown links between generated pages."""
        edges: list[Edge] = []
        for source_id, path in page_files_by_id.items():
            text = path.read_text(encoding="utf-8", errors="ignore")
            for target in self.markdown_link_targets(path, text):
                target_id = node_id_by_path.get(target)
                if not target_id or target_id == source_id:
                    continue
                edges.append(
                    Edge(
                        id=make_edge_id(source_id, target_id, "wiki_links_to"),
                        source_node_id=source_id,
                        target_node_id=target_id,
                        label="wiki_links_to",
                        summary="Markdown link between generated wiki pages.",
                    )
                )
        return edges

    def markdown_link_targets(self, path: Path, text: str) -> list[Path]:
        """Resolve relative .md link targets in a page's markdown to absolute paths."""
        targets: list[Path] = []
        for raw_target in _MARKDOWN_LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (path.parent / target).resolve()
            if candidate.suffix.lower() == ".md":
                targets.append(candidate)
        return targets

    def wiki_slug(self, folder: str, path: Path) -> str:
        """Type-prefixed slug for a wiki page file, e.g. concept/<stem>."""
        prefix = _WIKI_PAGE_FOLDERS.get(folder, (folder, ""))[0]
        return f"{prefix}/{path.stem}"

    def slug_kind(self, slug: str) -> str:
        """Page kind ('concept'/'entity'/...) parsed from a type-prefixed slug."""
        return slug.split("/", 1)[0] if "/" in slug else "concept"

    def wiki_source_line_count(self, original: Path, coverage: dict[str, Any]) -> int:
        """Source line count from coverage.json, falling back to counting the file."""
        raw_count = (
            coverage.get("source_line_count") if isinstance(coverage, dict) else None
        )
        try:
            count = int(raw_count)
            if count > 0:
                return count
        except (TypeError, ValueError):
            pass
        return len(original.read_text(encoding="utf-8", errors="ignore").splitlines())

    def source_ranges_from_refs(
        self, refs: list[dict[str, Any]]
    ) -> list[tuple[int, int]]:
        """(line_start, line_end) pairs from source ref dicts."""
        ranges: list[tuple[int, int]] = []
        for ref in refs:
            try:
                ranges.append((int(ref["line_start"]), int(ref["line_end"])))
            except (KeyError, TypeError, ValueError):
                continue
        return ranges

    def source_refs_from_markdown(
        self, *, text: str, out_path: Path, source_doc_ids: set[str]
    ) -> list[dict[str, Any]]:
        """Inline ``[doc:Lx-Ly]`` citations in page markdown as source ref dicts."""
        refs: list[dict[str, Any]] = []
        for match in _SOURCE_REF_RE.finditer(text):
            doc_id, raw_start, raw_end = match.groups()
            if source_doc_ids and doc_id not in source_doc_ids:
                continue
            start, end = int(raw_start), int(raw_end)
            refs.append(
                {
                    "doc_id": doc_id,
                    "source_path": str(out_path / "raw" / doc_id / "original.md"),
                    "line_start": start,
                    "line_end": end,
                    "ref": f"{doc_id}:L{start}-L{end}",
                }
            )
        return refs

    def merge_source_refs(
        self, left: list[dict[str, Any]], right: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Union of two ref lists, deduped on (doc_id, line_start, line_end)."""
        merged: list[dict[str, Any]] = []
        seen: set[tuple[str, int, int]] = set()
        for ref in [*left, *right]:
            try:
                key = (str(ref["doc_id"]), int(ref["line_start"]), int(ref["line_end"]))
            except (KeyError, TypeError, ValueError):
                continue
            if key in seen:
                continue
            seen.add(key)
            merged.append(ref)
        return merged

    def doc_ids_from_refs(self, refs: list[dict[str, Any]]) -> list[str]:
        """Distinct doc_ids referenced, in first-seen order."""
        doc_ids: list[str] = []
        for ref in refs:
            doc_id = ref.get("doc_id")
            if isinstance(doc_id, str) and doc_id not in doc_ids:
                doc_ids.append(doc_id)
        return doc_ids

    def string_list(self, value: Any) -> list[str]:
        """Coerce a value into a list of non-empty strings."""
        if not isinstance(value, list):
            return []
        return [str(item) for item in value if str(item).strip()]

    def safe_relative(self, path: Path, root: Path) -> str:
        """``path`` relative to ``root`` as posix, or the absolute string if outside."""
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return str(path)

    def first_summary_from_markdown(self, body: str) -> str:
        """First non-heading line of a markdown body, capped, as a fallback summary."""
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                continue
            return stripped[:240]
        return ""

    # --- shared markdown parsing ----------------------------------------------
    def split_frontmatter(self, text: str) -> tuple[dict[str, str], str]:
        """Split frontmatter from body; returns (meta, body)."""
        match = _FRONTMATTER_RE.match(text)
        if not match:
            return {}, text
        meta: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip().strip('"')
        return meta, match.group(2).strip()

    def parse_ranges(self, value: str | list[object] | None) -> list[tuple[int, int]]:
        """Parse source line ranges from JSON/list into [(start, end), ...]."""
        if not value:
            return []
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return []
        ranges: list[tuple[int, int]] = []
        for pair in value or []:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                try:
                    ranges.append((int(pair[0]), int(pair[1])))
                except (TypeError, ValueError):
                    pass
        return ranges

    def title_from_markdown(self, body: str) -> str | None:
        """First markdown heading in the body, or None."""
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or None
        return None

    def humanize(self, dirname: str) -> str:
        """Turn a slug / directory name into a Title Cased label."""
        name = re.sub(r"^\d+-", "", dirname).replace("-", " ").strip()
        return name.title()[:80] or "General"

    def read_json(self, path: Path, default: Any) -> Any:
        """Load JSON at path, or return default if the file is missing."""
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def canonical_doc_name(self, filename: str) -> str:
        """Strip a leading number prefix from a docs filename."""
        match = _NUMBERED_DOC_RE.match(filename)
        return match.group(1) if match else filename

    def doc_sort_key(self, path: Path) -> tuple[int, str]:
        """Sort key ordering docs by their leading number, then name."""
        first = path.name.split("-", 1)[0]
        return (int(first), path.name) if first.isdigit() else (10**9, path.name)

    def chain_edges(self, node_ids: list[str], summary: str) -> list[Edge]:
        """`follows` edges linking each node to the next in order."""
        return [
            Edge(
                id=make_edge_id(prev_id, next_id, "follows"),
                source_node_id=prev_id,
                target_node_id=next_id,
                label="follows",
                summary=summary,
            )
            for prev_id, next_id in zip(node_ids, node_ids[1:])
        ]

    # endregion

    # region ingest one node + enrichment
    def ingest(self, node: Node) -> list[Edge]:
        # node.id = hash(body, doc): an existing complete node (active + body
        # vector stored) is the exact same chunk in the same context — skip it.
        """Enrich, embed, and link one node; skip if it is already fully ingested."""
        existing = self.db.get_node(node.id)
        has_vector = getattr(self.db, "has_vector", None)
        complete = (
            existing is not None
            and existing.status == NodeStatus.active
            and (not callable(has_vector) or bool(has_vector(node.id)))
        )
        if complete:
            return []

        self.fill_derived_fields(node)
        self.db.upsert_node(node)
        body_vec, summary_vec = self.store_vectors(node)
        edges = self.build_semantic_edges(
            node, body_vec, summary_vec, self.settings.edge_candidate_k
        )
        if self.settings.entity_dedup:
            candidates = self.knn_candidates(
                node.id, body_vec, summary_vec, self.settings.edge_candidate_k
            )
            edges += self.link_entity_duplicates(node, candidates)
        return edges

    def fill_derived_fields(self, node: Node) -> Node:
        """Fill re-derivable metadata while keeping the source-verbatim body."""
        if not node.source_material_hash:
            node.source_material_hash = source_hash(node.body)
        if not node.summary.strip() and node.body.strip():
            node.summary = self.llm.complete(core.SUMMARY_PROMPT, node.body).strip()
        if not node.keywords:
            node.keywords = self.extract_keywords(node.body)
        if not node.claims:
            extracted = self.extract_claims(node.body)
            node.entity = node.entity or extracted.entity
            node.claims = extracted.claims
        if not node.entity and node.keywords:
            node.entity = node.keywords[0]
        return node

    def extract_keywords(self, text: str) -> list[str]:
        """LLM keyword extraction, deduped and capped at 12."""
        if not text.strip():
            return []
        result = self.llm.complete_structured(
            core.KEYWORD_PROMPT, text[:8000], Keywords
        )
        parsed = (
            result if isinstance(result, Keywords) else Keywords.model_validate(result)
        )
        kept: list[str] = []
        seen: set[str] = set()
        for keyword in parsed.keywords:
            keyword = keyword.strip()
            if keyword and keyword.lower() not in seen:
                kept.append(keyword)
                seen.add(keyword.lower())
        return kept[:12]

    def extract_claims(self, text: str) -> ClaimExtraction:
        """LLM claim/entity extraction, deduped and capped at 20."""
        if not text.strip():
            return ClaimExtraction()
        result = self.llm.complete_structured(
            core.CLAIM_PROMPT, text[:12000], ClaimExtraction
        )
        parsed = (
            result
            if isinstance(result, ClaimExtraction)
            else ClaimExtraction.model_validate(result)
        )
        claims: list[str] = []
        seen: set[str] = set()
        for claim in parsed.claims:
            claim = " ".join(claim.strip().split())
            if claim and claim.lower() not in seen:
                seen.add(claim.lower())
                claims.append(claim)
        return ClaimExtraction(
            entity=" ".join(parsed.entity.strip().split()), claims=claims[:20]
        )

    # endregion

    # region embeddings
    def prepare_embeddings(self) -> None:
        """Startup: rebuild every node's vectors if the embedding model/dim
        changed or a previous re-embed was interrupted. Runs once, eagerly."""
        if self.subagent:
            return
        try:
            current_model = self.embedder.model_name
            current_dim = self.embedder.dim
        except Exception as exc:  # noqa: BLE001 - embedder down: cannot prepare now
            log.warning("prepare_embeddings: embedder unavailable: %s", exc)
            return

        stored_model = self.db.get_meta("embed_model")
        stored_dim_raw = self.db.get_meta("embed_dim")
        stored_dim = int(stored_dim_raw) if stored_dim_raw else None
        active_nodes = [
            n for n in self.db.get_all_nodes() if n.status == NodeStatus.active
        ]

        dim_changed = stored_dim is not None and stored_dim != current_dim
        model_changed = stored_model is not None and stored_model != current_model
        coverage_incomplete = False
        if not dim_changed:
            self.db.ensure_vec_tables(current_dim)
            coverage_incomplete = self.db.count_vectors("vec_body") < len(active_nodes)

        if dim_changed or model_changed or coverage_incomplete:
            log.info(
                "rebuilding ALL vectors (model %s->%s dim %s->%s)",
                stored_model,
                current_model,
                stored_dim,
                current_dim,
            )
            self.db.reset_vec_tables()
            self.db.ensure_vec_tables(current_dim)
            for index, node in enumerate(active_nodes, start=1):
                try:
                    self.db.set_vector(
                        node.id, "vec_body", self.embedder.embed_document(node.body)
                    )
                    if node.summary.strip():
                        self.db.set_vector(
                            node.id,
                            "vec_summary",
                            self.embedder.embed_document(node.summary),
                        )
                except (
                    Exception
                ) as exc:  # noqa: BLE001 - skip a poison node, keep going
                    log.warning("reembed node %s failed: %s", node.id, exc)
                if index % 25 == 0 or index == len(active_nodes):
                    log.info("reembed %d/%d nodes", index, len(active_nodes))
            self.db.set_meta("embed_model", current_model)
        elif stored_model != current_model:
            self.db.set_meta("embed_model", current_model)
        self._vec_ready = True

    def ensure_vec(self) -> None:
        """Make sure the vector tables exist at the embedder's dimension (once)."""
        if self._vec_ready:
            return
        self.db.ensure_vec_tables(self.embedder.dim)
        self._vec_ready = True

    def store_vectors(self, node: Node) -> tuple[list[float], list[float] | None]:
        """Embed body (and summary) and store the vectors; returns them."""
        self.ensure_vec()
        body_vec = self.embedder.embed_document(node.body)
        self.db.set_vector(node.id, "vec_body", body_vec)
        summary_vec = None
        if node.summary.strip():
            summary_vec = self.embedder.embed_document(node.summary)
            self.db.set_vector(node.id, "vec_summary", summary_vec)
        return body_vec, summary_vec

    # endregion

    # region semantic edges + dedup
    def knn_candidates(
        self,
        node_id: str,
        body_vec: list[float],
        summary_vec: list[float] | None,
        k: int,
    ) -> list[Node]:
        """KNN over body/summary vectors -> active, same-as-collapsed candidate nodes."""
        ranked: list[str] = []
        probes = [("vec_body", body_vec)] + (
            [("vec_summary", summary_vec)] if summary_vec else []
        )
        for table, vector in probes:
            for candidate_id, _distance in self.db.vector_search(vector, table, k + 1):
                if candidate_id != node_id and candidate_id not in ranked:
                    ranked.append(candidate_id)
        candidates = [
            node
            for node in (self.db.get_node(cid) for cid in ranked)
            if node and node.status == NodeStatus.active
        ]
        return self.collapse_same_as(candidates)[:k]

    def build_semantic_edges(
        self, node: Node, body_vec: list[float], summary_vec: list[float] | None, k: int
    ) -> list[Edge]:
        candidates = self.knn_candidates(node.id, body_vec, summary_vec, k)
        if not candidates:
            return []
        payload = {
            "new_node": {
                "id": node.id,
                "title": node.title,
                "summary": node.summary,
                "keywords": node.keywords,
                "body": node.body[:4000],
            },
            "candidates": [
                {
                    "id": c.id,
                    "title": c.title,
                    "summary": c.summary,
                    "keywords": c.keywords,
                    "body": c.body[:1200],
                }
                for c in candidates
            ],
        }
        result = self.llm.complete_structured(
            core.EDGE_PROMPT, json.dumps(payload, ensure_ascii=False), EdgeSuggestions
        )
        parsed = (
            result
            if isinstance(result, EdgeSuggestions)
            else EdgeSuggestions.model_validate(result)
        )
        allowed = {c.id for c in candidates}

        edges: list[Edge] = []
        for suggestion in parsed.edges:
            target_id = suggestion.target_node_id
            if target_id not in allowed or target_id == node.id:
                continue
            label = suggestion.label.strip() or "related"
            stamp = now_iso()
            if label == "contradicts":
                self.invalidate_prior_edges(node.id, target_id, stamp)
            episodes = [node.id, target_id]
            for src, dst in ((node.id, target_id), (target_id, node.id)):
                edge = Edge(
                    id=make_edge_id(src, dst, label),
                    source_node_id=src,
                    target_node_id=dst,
                    label=label,
                    summary=suggestion.summary.strip(),
                    valid_at=stamp,
                    source_episode_ids=episodes,
                )
                self.db.upsert_edge(edge)
                edges.append(edge)
        return edges

    def invalidate_prior_edges(
        self, source_id: str, target_id: str, stamp: str
    ) -> None:
        """Graphiti-style: a new `contradicts` edge marks the older fact between
        the same pair as no-longer-valid (never deleted)."""
        for edge in self.db.get_edges_for_node(target_id):
            if {edge.source_node_id, edge.target_node_id} != {source_id, target_id}:
                continue
            if edge.label == "contradicts" or edge.invalid_at:
                continue
            edge.invalid_at = stamp
            edge.expired_at = stamp
            self.db.upsert_edge(edge)

    def link_entity_duplicates(self, node: Node, candidates: list[Node]) -> list[Edge]:
        """Detect a same-real-world-entity neighbor and link it with a same-as edge."""
        if not candidates:
            return []
        payload = {
            "new_node": {
                "id": node.id,
                "title": node.title,
                "entity": node.entity,
                "summary": node.summary,
            },
            "candidates": [
                {"id": c.id, "title": c.title, "entity": c.entity, "summary": c.summary}
                for c in candidates
            ],
        }
        result = self.llm.complete_structured(
            core.ENTITY_DEDUP_PROMPT,
            json.dumps(payload, ensure_ascii=False),
            EntityMatch,
        )
        match = (
            result
            if isinstance(result, EntityMatch)
            else EntityMatch.model_validate(result)
        )
        allowed = {c.id for c in candidates}
        if (
            not match.is_same
            or match.target_node_id not in allowed
            or match.target_node_id == node.id
        ):
            return []

        stamp = now_iso()
        episodes = [node.id, match.target_node_id]
        edges: list[Edge] = []
        for src, dst in (
            (node.id, match.target_node_id),
            (match.target_node_id, node.id),
        ):
            edge = Edge(
                id=make_edge_id(src, dst, "same-as"),
                source_node_id=src,
                target_node_id=dst,
                label="same-as",
                summary="Same real-world entity.",
                valid_at=stamp,
                source_episode_ids=episodes,
            )
            self.db.upsert_edge(edge)
            edges.append(edge)
        return edges

    def collapse_same_as(self, nodes: list[Node]) -> list[Node]:
        """Keep one representative per same-as cluster, preserving input order."""
        kept: list[Node] = []
        seen: set[str] = set()
        for node in nodes:
            if node.id in seen:
                continue
            kept.append(node)
            group = {node.id}
            for edge in self.db.get_edges_for_node(node.id):
                if edge.label == "same-as":
                    other = (
                        edge.target_node_id
                        if edge.source_node_id == node.id
                        else edge.source_node_id
                    )
                    group.add(other)
            seen |= group
        return kept

    def link_supports(self, node: Node, source_node_ids: list[str]) -> None:
        """Add `supports` edges from each existing source node to this derived node."""
        for source_id in source_node_ids:
            if not self.db.get_node(source_id):
                continue
            self.db.upsert_edge(
                Edge(
                    id=make_edge_id(source_id, node.id, "supports"),
                    source_node_id=source_id,
                    target_node_id=node.id,
                    label="supports",
                    summary="Source node supports this derived node.",
                )
            )

    def create_exogenous_node(
        self, body: str, source_node_ids: list[str], origin: str | None = None
    ) -> Node:
        """Create, enrich, embed, and support-link a derived (LLM-authored) node."""
        node = Node(
            id=make_exogenous_node_id(origin or body),
            body=body,
            type=NodeType.exogenous,
            original_document_name=origin,
            cluster="Agent Notes",
        )
        self.fill_derived_fields(node)
        self.db.upsert_node(node)
        self.store_vectors(node)
        self.link_supports(node, source_node_ids)
        return node

    # endregion

    # region query / retrieval
    def query(self, query_type: str, value: str) -> QueryResult:
        """One-shot lookup by id, keyword (BM25), or vector (KNN + neighborhood)."""
        normalized = query_type.lower().strip()
        if normalized == "id":
            node = self.read(value)
            return QueryResult(
                query_type="id",
                value=value,
                nodes=[node] if node else [],
                edges=self.db.get_edges_for_node(value) if node else [],
            )
        if normalized == "keyword":
            nodes = self.db.keyword_search(value, self.settings.vector_query_k)
            edges: dict[str, Edge] = {}
            for node in nodes:
                for edge in self.db.get_edges_for_node(node.id):
                    edges[edge.id] = edge
            return QueryResult(
                query_type="keyword",
                value=value,
                nodes=nodes,
                edges=list(edges.values()),
            )
        if normalized == "vector":
            self.ensure_vec()
            vector = self.embedder.embed_query(value)
            hits = self.db.vector_search(
                vector, "vec_body", self.settings.vector_query_k
            )
            seeds = [n for n in (self.db.get_node(nid) for nid, _ in hits) if n]
            nodes, edges_list = self.expand_neighborhood(seeds, hops=2)
            return QueryResult(
                query_type="vector", value=value, nodes=nodes, edges=edges_list
            )
        raise ValueError("query_type must be 'keyword', 'vector', or 'id'")

    def search(self, text: str, limit: int | None = None) -> list[Node]:
        """Hybrid BM25 + semantic search fused with Reciprocal Rank Fusion, then
        optionally cross-encoder reranked. Degrades to BM25-only if embedding fails."""
        limit = limit or self.settings.vector_query_k
        pool = (
            max(limit, self.settings.search_candidate_pool)
            if self.reranker
            else max(limit, 10)
        )

        ranked_lists: list[list[str]] = [
            [n.id for n in self.db.keyword_search(text, pool)]
        ]
        try:
            self.ensure_vec()
            query_vec = self.embedder.embed_query(text)
            for table in ("vec_body", "vec_summary"):
                hits = self.db.vector_search(query_vec, table, pool)
                ranked_lists.append([node_id for node_id, _score in hits])
        except Exception as exc:  # noqa: BLE001 - vec unavailable: BM25-only
            log.info("vector search failed; BM25-only: %s", exc)

        # RRF: sum 1/(k + rank) of each id across lists.
        rrf_k = self.settings.search_rrf_k
        scores: dict[str, float] = {}
        for ids in ranked_lists:
            for rank, node_id in enumerate(ids):
                scores[node_id] = scores.get(node_id, 0.0) + 1.0 / (rrf_k + rank + 1)
        fused_ids = sorted(scores, key=lambda nid: scores[nid], reverse=True)

        nodes: list[Node] = []
        for node_id in fused_ids:
            node = self.db.get_node(node_id)
            if node and node.status == NodeStatus.active:
                nodes.append(node)
            if len(nodes) >= pool:
                break

        if not self.reranker or len(nodes) <= 1:
            return nodes[:limit]
        try:
            items = [(f"{n.title}\n{n.summary}\n{n.body}".strip(), n) for n in nodes]
            return [node for node, _score in self.reranker.top_k(text, items, limit)]
        except Exception as exc:  # noqa: BLE001 - reranker down: keep fused order
            log.info("rerank failed (%s); fused order", exc)
            return nodes[:limit]

    def read(self, node_id: str) -> Node | None:
        """Fetch a node by id, repairing a missing `node:` prefix, then fuzzy keyword fallback."""
        node = self.db.get_node(node_id)
        if node:
            return node
        if not node_id.startswith("node:"):
            node = self.db.get_node(f"node:{node_id}")
            if node:
                return node
        matches = self.db.keyword_search(node_id, 5)
        return matches[0] if matches else None

    def follow_link(
        self,
        node_id: str,
        label: str | None = None,
        direction: str = "both",
        limit: int | None = None,
    ) -> list[tuple[Edge, Node]]:
        """Active neighbor nodes reached by edges in the given direction."""
        normalized = direction.lower().strip()
        if normalized not in {"incoming", "outgoing", "both"}:
            raise ValueError("direction must be 'incoming', 'outgoing', or 'both'")

        pairs: list[tuple[Edge, Node]] = []
        if normalized in {"outgoing", "both"}:
            for edge in self.db.get_outgoing_edges(node_id, label):
                target = self.db.get_node(edge.target_node_id)
                if target and target.status == NodeStatus.active:
                    pairs.append((edge, target))
        if normalized in {"incoming", "both"}:
            for edge in self.db.get_incoming_edges(node_id, label):
                source = self.db.get_node(edge.source_node_id)
                if source and source.status == NodeStatus.active:
                    pairs.append((edge, source))
        return pairs[:limit] if limit is not None else pairs

    def expand_neighborhood(
        self, seeds: list[Node], hops: int = 2
    ) -> tuple[list[Node], list[Edge]]:
        """Collect all active nodes/edges within `hops` of the seeds (BFS)."""
        seen_nodes = {node.id: node for node in seeds}
        seen_edges: dict[str, Edge] = {}
        frontier = list(seen_nodes)
        for _hop in range(hops):
            next_frontier: list[str] = []
            for node_id in frontier:
                for edge in self.db.get_edges_for_node(node_id):
                    seen_edges[edge.id] = edge
                    other_id = (
                        edge.target_node_id
                        if edge.source_node_id == node_id
                        else edge.source_node_id
                    )
                    if other_id in seen_nodes:
                        continue
                    other = self.db.get_node(other_id)
                    if other and other.status == NodeStatus.active:
                        seen_nodes[other_id] = other
                        next_frontier.append(other_id)
            frontier = next_frontier
        return list(seen_nodes.values()), list(seen_edges.values())

    # endregion

    # region revision / cascade
    def recon(self, source_file: str | Path) -> dict[str, str]:
        """Report whether a source file is new, unchanged, or changed vs the stored hash."""
        path = Path(source_file)
        current = source_hash(path.read_text(encoding="utf-8", errors="ignore"))
        known = self.db.get_source(path.name)
        if known is None:
            return {
                "document": path.name,
                "status": "new",
                "action": "md_to_nodes+ingest",
            }
        if known[0] == current:
            return {"document": path.name, "status": "unchanged", "action": "skip"}
        return {
            "document": path.name,
            "status": "changed",
            "action": "cascading_update",
        }

    def update_node(self, node_id: str, body: str) -> Node:
        """Replace one node's body; supersede the old node if the body actually changed."""
        old = self.db.get_node(node_id)
        if not old:
            raise KeyError(f"node not found: {node_id}")
        replacement = Node(
            id=make_node_id(body, old.original_document_name),
            body=body,
            type=old.type,
            title=old.title,
            original_document_name=old.original_document_name,
            source_path=old.source_path,
            source_version=source_hash(body),
            cluster=old.cluster,
        )
        if replacement.id == old.id:
            old.source_version = replacement.source_version
            self.fill_derived_fields(old)
            self.db.upsert_node(old)
            return old
        self.persist_node(replacement)
        self.supersede(old, replacement)
        return replacement

    def cascading_update(self, source_file: str | Path) -> list[str]:
        """Apply a revised output: match, supersede, stale, and cascade derived nodes."""
        nodes, structural_edges = self.load_md_output(source_file)
        if not nodes:
            return []
        document_name = nodes[0].original_document_name or Path(source_file).name
        version = self.source_version_for_nodes(nodes)

        # Cheap pass: stamp version + body hash only. No LLM enrichment yet.
        for node in nodes:
            node.source_version = version
            if not node.source_material_hash:
                node.source_material_hash = source_hash(node.body)

        active_old = [
            n
            for n in self.db.get_nodes_by_document(document_name, active_only=True)
            if n.type == NodeType.endogenous
        ]
        if not active_old:
            for node in nodes:
                self.persist_node(node)
            self.replace_structural_edges(document_name, structural_edges)
            self.db.record_source(document_name, version)
            return [f"ingested-new:{n.id}" for n in nodes]

        actions: list[str] = []
        replacements: dict[str, str] = {}
        stale_sources: set[str] = set()
        matched_old: set[str] = set()
        exact_by_hash: dict[str, Node] = {}
        for old in active_old:
            exact_by_hash.setdefault(
                old.source_material_hash or source_hash(old.body), old
            )

        # PASS 1 — exact body-hash match (no enrichment on either side).
        pending: list[Node] = []
        for node in nodes:
            exact = exact_by_hash.get(node.source_material_hash)
            if exact and exact.id not in matched_old:
                matched_old.add(exact.id)
                actions.append(f"unchanged:{exact.id}")
            else:
                pending.append(node)

        # Only changed/new chunks get enriched + matched fuzzily.
        for node in pending:
            self.fill_derived_fields(node)
        unmatched_old = [
            self.backfill_revision_metadata(old)
            for old in active_old
            if old.id not in matched_old
        ]

        # PASS 2 — fuzzy match for pending.
        for node in pending:
            candidates = [old for old in unmatched_old if old.id not in matched_old]
            best = max(
                ((c, core.match_score(c, node)) for c in candidates),
                key=lambda item: item[1],
                default=None,
            )
            if best is None or best[1] < _CASCADE_MATCH_THRESHOLD:
                self.persist_node(node)
                actions.append(f"new:{node.id}")
                continue
            old = best[0]
            matched_old.add(old.id)
            if core.claims_equivalent(old, node):
                actions.append(f"remapped:{old.id}")
                continue
            self.persist_node(node)
            self.supersede(old, node)
            replacements[old.id] = node.id
            actions.append(f"superseded:{old.id}->{node.id}")

        # PASS 3 — unmatched old nodes go stale.
        for old in active_old:
            if old.id not in matched_old:
                self.db.set_node_status(old.id, NodeStatus.stale)
                stale_sources.add(old.id)
                actions.append(f"stale:{old.id}")

        self.cascade_dependents(replacements, stale_sources, actions)
        self.replace_structural_edges(document_name, structural_edges)
        self.db.record_source(document_name, version)
        # Refresh clusters after the graph changed shape (best-effort).
        try:
            self.recluster()
        except Exception as exc:  # noqa: BLE001 - clustering is non-critical
            log.info("recluster skipped: %s", exc)
        return actions

    def source_version_for_nodes(self, nodes: list[Node]) -> str:
        """Hash of all source bodies (or files) — one version id for the document."""
        if not nodes:
            return source_hash("")
        parts: list[str] = []
        for node in nodes:
            if node.source_path and Path(node.source_path).exists():
                parts.append(
                    Path(node.source_path).read_text(encoding="utf-8", errors="ignore")
                )
            else:
                parts.append(node.body)
        return source_hash("\n\n--- NODE BREAK ---\n\n".join(parts))

    def backfill_revision_metadata(self, node: Node) -> Node:
        """Backfill the claims/entity an old node needs for fuzzy matching."""
        changed = False
        if not node.source_material_hash:
            node.source_material_hash = source_hash(node.body)
            changed = True
        if not node.claims:
            extracted = self.extract_claims(node.body)
            node.entity = node.entity or extracted.entity
            node.claims = extracted.claims
            changed = True
        if not node.entity and node.keywords:
            node.entity = node.keywords[0]
            changed = True
        if changed:
            self.db.upsert_node(node)
        return node

    def persist_node(self, node: Node) -> Node:
        """Enrich, store, embed, and build semantic edges for a node."""
        self.fill_derived_fields(node)
        self.db.upsert_node(node)
        body_vec, summary_vec = self.store_vectors(node)
        self.build_semantic_edges(
            node, body_vec, summary_vec, self.settings.edge_candidate_k
        )
        return node

    def supersede(self, old: Node, new: Node) -> None:
        """Link old->new with supersedes edges and mark the old node superseded."""
        self.db.upsert_edge(
            Edge(
                id=make_edge_id(old.id, new.id, "superseded_by"),
                source_node_id=old.id,
                target_node_id=new.id,
                label="superseded_by",
                summary="Newer source material replaces these facts.",
            )
        )
        self.db.upsert_edge(
            Edge(
                id=make_edge_id(new.id, old.id, "supersedes"),
                source_node_id=new.id,
                target_node_id=old.id,
                label="supersedes",
                summary="Older source material replaced by this node.",
            )
        )
        self.db.set_node_status(old.id, NodeStatus.superseded)

    def replace_structural_edges(
        self, document_name: str | None, edges: list[Edge]
    ) -> None:
        """Drop a document's old structural edges and re-add the new ones.

        Normal documents only carry `follows` chains; the global wiki layout also
        owns citation/link labels, so those are cleared too when re-ingesting it.
        """
        labels = {edge.label for edge in edges}
        if document_name == _GLOBAL_WIKI_DOCUMENT:
            labels.update(
                {
                    "follows",
                    "wiki_cites_source",
                    "source_supports_wiki",
                    "wiki_links_to",
                }
            )
        if document_name and labels:
            node_ids = {
                n.id
                for n in self.db.get_nodes_by_document(document_name)
                if n.type == NodeType.endogenous
            }
            for label in labels:
                self.db.delete_edges_by_label_for_nodes(label, node_ids)
        for edge in edges:
            source = self.db.get_node(edge.source_node_id)
            target = self.db.get_node(edge.target_node_id)
            if (
                source
                and target
                and source.status == NodeStatus.active
                and target.status == NodeStatus.active
            ):
                self.db.upsert_edge(edge)

    def cascade_dependents(
        self, replacements: dict[str, str], stale_sources: set[str], actions: list[str]
    ) -> None:
        """BFS over `supports` edges: regenerate or stale the derived nodes whose
        source material changed. Bounded by cascade_max_hops / cascade_max_nodes."""
        max_hops = max(0, self.settings.cascade_max_hops)
        max_nodes = max(0, self.settings.cascade_max_nodes)
        if max_hops == 0 or max_nodes == 0:
            if replacements or stale_sources:
                actions.append("cascade-skipped:disabled")
            return

        frontier: deque[tuple[str, int]] = deque(
            (nid, 0) for nid in sorted(set(replacements) | set(stale_sources))
        )
        visited: set[str] = set()
        processed = 0
        while frontier:
            changed_id, depth = frontier.popleft()
            target_depth = depth + 1
            if target_depth > max_hops:
                continue
            for edge in self.db.get_outgoing_edges(changed_id, "supports"):
                target = self.db.get_node(edge.target_node_id)
                if (
                    not target
                    or target.status != NodeStatus.active
                    or target.type != NodeType.exogenous
                    or target.id in visited
                ):
                    continue
                if processed >= max_nodes:
                    actions.append(
                        f"cascade-cap-hit:max_nodes={max_nodes}:at={target.id}"
                    )
                    return
                visited.add(target.id)
                processed += 1

                support_nodes = self.current_support_nodes(target, replacements)
                replacement = (
                    self.regenerate_exogenous_node(target, support_nodes)
                    if support_nodes
                    else None
                )
                if replacement is None:
                    self.db.set_node_status(target.id, NodeStatus.stale)
                    actions.append(f"stale-exogenous:{target.id}")
                else:
                    replacements[target.id] = replacement.id
                    actions.append(
                        f"regenerated-exogenous:{target.id}->{replacement.id}"
                    )
                if target_depth < max_hops:
                    frontier.append((target.id, target_depth))

    def current_support_nodes(
        self, node: Node, replacements: dict[str, str]
    ) -> list[Node]:
        """Live active support nodes for a derived node, following swaps/supersedes."""
        support_nodes: dict[str, Node] = {}
        for edge in self.db.get_incoming_edges(node.id, "supports"):
            source_id = replacements.get(edge.source_node_id, edge.source_node_id)
            source = self.db.get_node(source_id)
            if source and source.status == NodeStatus.superseded:
                for swap in self.db.get_outgoing_edges(source.id, "superseded_by"):
                    target = self.db.get_node(swap.target_node_id)
                    if target and target.status == NodeStatus.active:
                        source = target
                        break
            if source and source.status == NodeStatus.active:
                support_nodes[source.id] = source
        return self.collapse_same_as(list(support_nodes.values()))

    def regenerate_exogenous_node(
        self, old: Node, support_nodes: list[Node]
    ) -> Node | None:
        if not support_nodes:
            return None
        payload = {
            "previous_node": {
                "id": old.id,
                "title": old.title,
                "summary": old.summary,
                "body": old.body[:4000],
            },
            "current_support_material": [
                {
                    "id": n.id,
                    "title": n.title,
                    "summary": n.summary,
                    "body": n.body[:2500],
                }
                for n in support_nodes[:8]
            ],
        }
        body = self.llm.complete(
            core.REGENERATE_EXOGENOUS_PROMPT, json.dumps(payload, ensure_ascii=False)
        ).strip()
        if not body:
            return None

        support_ids = sorted(n.id for n in support_nodes)
        version = source_hash(
            "|".join(
                [
                    source_hash(body),
                    *support_ids,
                    *(n.source_version or "" for n in support_nodes),
                ]
            )
        )
        replacement = Node(
            id=make_exogenous_node_id(f"{old.id}|{version}|{body}"),
            body=body,
            type=NodeType.exogenous,
            title=old.title,
            original_document_name=old.original_document_name,
            source_version=version,
            cluster=old.cluster,
        )
        if replacement.id == old.id:
            return old
        self.persist_node(replacement)
        self.link_supports(replacement, [n.id for n in support_nodes])
        self.supersede(old, replacement)
        return replacement

    # endregion

    # region analytics
    def get(self) -> tuple[list[Node], list[Edge]]:
        """All nodes and edges."""
        return self.db.get_all_nodes(), self.db.get_all_edges()

    def delete(self, node_id: str) -> None:
        """Hard-delete a node."""
        self.db.delete_node(node_id)

    def health(self, node_id: str | None = None) -> GraphStats:
        """Graph metrics: counts, degree, density, neighbor overlap, cluster histogram."""
        nodes = self.db.get_all_nodes()
        edges = self.db.get_all_edges()
        if node_id:
            nodes = [n for n in nodes if n.id == node_id]
            edges = [
                e for e in edges if node_id in (e.source_node_id, e.target_node_id)
            ]
        node_ids = {n.id for n in nodes}
        neighbors: dict[str, set[str]] = {nid: set() for nid in node_ids}
        for edge in edges:
            if edge.source_node_id in neighbors and edge.target_node_id in node_ids:
                neighbors[edge.source_node_id].add(edge.target_node_id)
            if edge.target_node_id in neighbors and edge.source_node_id in node_ids:
                neighbors[edge.target_node_id].add(edge.source_node_id)

        node_count = len(nodes)
        total_degree = sum(len(v) for v in neighbors.values())
        avg_degree = (total_degree / node_count) if node_count else 0.0
        max_edges = node_count * (node_count - 1) / 2
        density = ((total_degree / 2) / max_edges) if max_edges else 0.0

        overlap_total, overlap_pairs = 0.0, 0
        for nid, nid_neighbors in neighbors.items():
            for other_id in nid_neighbors:
                if other_id <= nid:
                    continue
                union = nid_neighbors | neighbors.get(other_id, set())
                if union:
                    overlap_total += len(
                        nid_neighbors & neighbors.get(other_id, set())
                    ) / len(union)
                    overlap_pairs += 1
        mean_overlap = (overlap_total / overlap_pairs) if overlap_pairs else 0.0

        clusters: dict[str, int] = {}
        for node in nodes:
            key = node.cluster or "Unclustered"
            clusters[key] = clusters.get(key, 0) + 1

        return GraphStats(
            total_nodes=node_count,
            active_nodes=sum(1 for n in nodes if n.status == NodeStatus.active),
            endogenous_nodes=sum(1 for n in nodes if n.type == NodeType.endogenous),
            exogenous_nodes=sum(1 for n in nodes if n.type == NodeType.exogenous),
            total_edges=len(edges),
            isolated_nodes=sum(1 for nid in node_ids if not neighbors[nid]),
            avg_degree=round(avg_degree, 3),
            density=round(density, 5),
            mean_neighbor_overlap=round(mean_overlap, 4),
            clusters=clusters,
            target_node_id=node_id,
        )

    def recluster(
        self, resolution: float = 1.0, seed: int = 42, persist: bool = True
    ) -> dict[str, str]:
        """Louvain communities over active nodes+edges, each named by its
        distinctive (TF-IDF) keywords, refined by the LLM when available."""
        import networkx as nx

        nodes = [n for n in self.db.get_all_nodes() if n.status == NodeStatus.active]
        node_by_id = {n.id: n for n in nodes}
        graph = nx.Graph()
        graph.add_nodes_from(node_by_id)
        for edge in self.db.get_all_edges():
            src, dst = edge.source_node_id, edge.target_node_id
            if src not in node_by_id or dst not in node_by_id or src == dst:
                continue
            if graph.has_edge(src, dst):
                graph[src][dst]["weight"] += 1.0
            else:
                graph.add_edge(src, dst, weight=1.0)

        communities = nx.community.louvain_communities(
            graph, weight="weight", resolution=resolution, seed=seed
        )
        ordered = sorted(communities, key=len, reverse=True)

        per_comm: list[Counter[str]] = []
        titles: list[list[str]] = []
        doc_freq: Counter[str] = Counter()
        for members in ordered:
            counts: Counter[str] = Counter()
            comm_titles: list[str] = []
            for nid in members:
                node = node_by_id.get(nid)
                if node:
                    counts.update(k.lower().strip() for k in node.keywords if k.strip())
                    if node.title:
                        comm_titles.append(node.title)
            per_comm.append(counts)
            titles.append(comm_titles)
            doc_freq.update(counts.keys())

        n_comms = max(len(ordered), 1)
        mapping: dict[str, str] = {}
        used: Counter[str] = Counter()
        used_labels: list[str] = []
        for index, members in enumerate(ordered):
            keywords = self.tfidf_keywords(per_comm[index], doc_freq, n_comms, k=8)
            label = self.name_cluster(keywords, titles[index][:12], used_labels)
            used[label] += 1
            if used[label] > 1:
                label = f"{label} {used[label]}"
            used_labels.append(label)
            for nid in members:
                mapping[nid] = label

        if persist:
            for node in nodes:
                new_label = mapping.get(node.id)
                if new_label and node.cluster != new_label:
                    node.cluster = new_label
                    self.db.upsert_node(node)
        return mapping

    def tfidf_keywords(
        self, counts: Counter[str], doc_freq: Counter[str], n_comms: int, k: int = 5
    ) -> list[str]:
        """Top-k keywords that DISTINGUISH this community (shared terms drop out)."""
        if not counts:
            return []
        scored = sorted(
            counts.items(),
            key=lambda kv: kv[1] * math.log(1 + n_comms / max(doc_freq[kv[0]], 1)),
            reverse=True,
        )
        return [kw for kw, _ in scored[:k]]

    def name_cluster(
        self, keywords: list[str], titles: list[str], used_names: list[str]
    ) -> str:
        """LLM name for a community; deterministic keyword fallback on any failure."""
        fallback = (
            " · ".join(kw.title() for kw in keywords[:3]) if keywords else "Cluster"
        )
        if not keywords and not titles:
            return fallback
        user = (
            f"Keywords: {', '.join(keywords) or '(none)'}\n"
            f"Sample titles: {'; '.join(titles) or '(none)'}\n"
            f"Already used names to avoid: {', '.join(used_names) or '(none)'}\n\n"
            "Topic name:"
        )
        try:
            raw = self.llm.complete(core.CLUSTER_NAMER_SYSTEM, user)
        except Exception:  # noqa: BLE001 - naming is non-critical
            return fallback
        name = " ".join(raw.strip().strip("\"'").split())
        if not name or len(name) > 60 or len(name.split()) > 6:
            return fallback
        if name.lower() in {u.lower() for u in used_names}:
            return fallback
        return name.title()

    # endregion

    # region reasoning agent
    def ask(
        self,
        question: str,
        persist: bool = True,
        on_event: Callable[[dict[str, Any]], None] | None = None,
    ) -> AgentAnswer:
        """Answer a question via the lead/subagent loop; repair mermaid; persist the answer node."""
        self._emit = on_event or (lambda event: None)
        answer = self.run_lead(question)

        if self.settings.enable_mermaid and answer.answer:
            answer.answer = repair_answer_mermaid(
                answer.answer, self.llm, self.settings, self._emit
            )

        if persist and answer.cited_node_ids:
            valid_ids = [
                nid for nid in answer.cited_node_ids if self.read(nid) is not None
            ]
            if valid_ids:
                exo = self.create_exogenous_node(
                    answer.answer, valid_ids, origin=f"agent:{question[:60]}"
                )
                answer.exogenous_node_id = exo.id
        return answer

    def run_lead(self, question: str) -> AgentAnswer:
        """Run the lead agent loop (search + explore) and compile its final answer."""
        evidence: list[str] = []  # local — appended when subagent reports return

        def dispatch(name: str, args: dict[str, Any]) -> str:
            if name == "search":
                query = str(args.get("text", ""))
                self.emit_event("search", phase="main", query=query)
                nodes = self.search(query, limit=self.settings.rerank_top_k)
                self.emit_event(
                    "candidates", count=len(nodes), nodes=[node_ref(n) for n in nodes]
                )
                if not nodes:
                    return "no nodes found"
                return "\n".join(
                    f"- node_id: `{n.id}`\n  title: {n.title}\n  summary: {n.summary}\n"
                    f"  next_action: pass this id to explore(node_ids=[...]) if promising and distinct"
                    for n in nodes
                )
            if name == "explore":
                return self.run_subagents(args.get("node_ids", []), question, evidence)
            return f"unknown tool: {name}"

        system_prompt = core.MAIN_AGENT_SYSTEM_PROMPT
        if self.settings.enable_mermaid:
            system_prompt += core.MERMAID_INSTRUCTION
        result = self.llm.run_tool_loop(
            system_prompt, question, LEAD_TOOLS, dispatch, self.settings.agent_max_steps
        )
        self.emit_event("compiling")

        if result.finished_args is not None:
            answer_text = str(result.finished_args.get("answer", "")).strip()
            cited = [
                nid for nid in result.finished_args.get("cited_node_ids", []) if nid
            ]
        else:
            answer_text, cited = result.content, []
        return AgentAnswer(
            question=question,
            answer=answer_text,
            cited_node_ids=cited or dedupe(evidence),
            steps=result.steps,
        )

    def run_subagents(
        self, raw_node_ids: list[Any], question: str, evidence: list[str]
    ) -> str:
        """Resolve distinct starts and run the exploration team, gathering evidence."""
        starts = self.resolve_distinct_starts(raw_node_ids)
        if not starts:
            return (
                "no valid starting nodes resolved from those ids. Search again and pass "
                "exact node ids from the search results to explore."
            )
        self.emit_event(
            "subagents_spawned",
            starts=[node_ref(n) for n in (self.read(s) for s in starts) if n],
        )
        assignments = [(start, [o for o in starts if o != start]) for start in starts]

        reports: list[dict[str, Any]] = []
        with ThreadPoolExecutor(
            max_workers=max(1, self.settings.subagent_concurrency)
        ) as pool:
            futures = [
                pool.submit(self.run_subagent, start, siblings, question, index)
                for index, (start, siblings) in enumerate(assignments, start=1)
            ]
            for future in futures:
                try:
                    reports.append(future.result())
                except (
                    Exception
                ) as exc:  # noqa: BLE001 - one subagent failing is non-fatal
                    reports.append(
                        {
                            "start": "?",
                            "answer": f"(subagent failed: {exc})",
                            "cited": [],
                        }
                    )

        for report in reports:
            evidence.extend(report.get("cited", []))

        blocks = ["Subagent reports (each explored a different region):"]
        for index, report in enumerate(reports, start=1):
            cited = ", ".join(report.get("cited", [])) or "(none)"
            blocks.append(
                f"\n### Subagent {index} — start node: {report.get('start')}\n"
                f"{report.get('answer', '').strip()}\nEvidence node ids: {cited}"
            )
        return "\n".join(blocks)

    def resolve_distinct_starts(self, raw_node_ids: list[Any]) -> list[str]:
        """Clean, resolve, and de-dup start ids, capped at subagent_count."""
        resolved: list[str] = []
        seen: set[str] = set()
        for raw in raw_node_ids or []:
            node = self.read(clean_node_ref(str(raw)))
            if node and node.id not in seen:
                seen.add(node.id)
                resolved.append(node.id)
            if len(resolved) >= self.settings.subagent_count:
                break
        return resolved

    def run_subagent(
        self, start_id: str, sibling_ids: list[str], question: str, index: int
    ) -> dict[str, Any]:
        """Explore one region on this subagent's OWN read-only Graph + DB
        connection (we are on a worker thread; the engine's connection is thread-bound).
        """
        from .db import Database  # lazy: see the module-level import note

        sub = Graph(
            self.settings,
            db=Database(self.settings.database_path),
            embedder=self.embedder,
            reranker=self.reranker,
            llm=self.llm,
            subagent=True,
        )
        run = Subrun(start_id=start_id, index=index)
        try:
            start_node = sub.read(start_id)
            if start_node is not None:
                self.emit_event(
                    "subagent_start", agent=index, node=node_ref(start_node)
                )

            def dispatch(name: str, args: dict[str, Any]) -> str:
                return self.dispatch_subagent(sub, name, args, run)

            def finish_guard(_args: dict[str, Any]) -> str | None:
                if len(run.read_ids) < self.settings.subagent_min_reads:
                    return (
                        f"You have read only {len(run.read_ids)} node(s); read at least "
                        f"{self.settings.subagent_min_reads} before finishing. Read another now."
                    )
                return None

            siblings = ", ".join(sibling_ids) if sibling_ids else "(none)"
            user_prompt = (
                f"Question: {question}\n\n"
                f"Your assigned starting node: {start_id}\n"
                f"Sibling agents are covering (do NOT explore these): {siblings}\n\n"
                "Read your starting node first, then follow links / search within your "
                "region. Report what this region says about the question."
            )
            result = self.llm.run_tool_loop(
                core.SUBAGENT_SYSTEM_PROMPT,
                user_prompt,
                SUBAGENT_TOOLS,
                dispatch,
                self.settings.subagent_max_steps,
                finish_guard=finish_guard,
            )

            if result.finished_args is not None:
                answer = str(result.finished_args.get("answer", "")).strip()
                cited = [
                    nid for nid in result.finished_args.get("cited_node_ids", []) if nid
                ]
            else:
                answer, cited = result.content, []
            cited = cited or dedupe(run.visited)
            self.emit_event("subagent_done", agent=index, cited=cited)
            return {
                "start": start_id,
                "answer": answer or "(no findings)",
                "cited": cited,
            }
        finally:
            sub.close()

    def dispatch_subagent(
        self, sub: "Graph", name: str, args: dict[str, Any], run: Subrun
    ) -> str:
        """Run one subagent tool call (search/read/follow_link) against its own Graph."""
        if name == "search":
            query = str(args.get("text", ""))
            self.emit_event("search", phase="sub", agent=run.index, query=query)
            nodes = sub.search(query, limit=self.settings.rerank_top_k)
            run.visited.extend(n.id for n in nodes)
            if nodes:
                run.empty_streak = 0
                return "\n".join(
                    f"- node_id: `{n.id}`\n  title: {n.title}\n  summary: {n.summary}\n"
                    f"  next_action: read this node with read(node_id='{n.id}') if relevant"
                    for n in nodes
                )
            run.empty_streak += 1
            if run.empty_streak >= self.settings.agent_patience:
                return (
                    f"no nodes found ({run.empty_streak} consecutive empty searches). Stop "
                    "searching now: call finish with the best answer supported by nodes you read."
                )
            return "no nodes found"

        if name == "read":
            requested_id = str(args.get("node_id", ""))
            cleaned_id = clean_node_ref(requested_id)
            node = sub.read(cleaned_id)
            if node:
                if node.id in run.read_ids:
                    return f"already read {node.id} ({node.title}). Pick a DIFFERENT node, follow a link, or finish."
                if len(run.read_ids) >= self.settings.subagent_max_reads:
                    return (
                        f"read budget reached ({len(run.read_ids)}/{self.settings.subagent_max_reads} "
                        "nodes). Call finish now with what you have gathered."
                    )
                run.empty_streak = 0
                run.read_ids.add(node.id)
                run.visited.append(node.id)
                self.emit_event("read", agent=run.index, node=node_ref(node))
            return format_node_full(node, requested_id, cleaned_id)

        if name == "follow_link":
            node_id = str(args.get("node_id", ""))
            pairs = sub.follow_link(
                node_id, direction=str(args.get("direction", "both"))
            )
            if pairs:
                run.empty_streak = 0
            run.visited.extend(n.id for _edge, n in pairs)
            anchor = sub.read(node_id)
            self.emit_event(
                "follow_link",
                agent=run.index,
                node=node_ref(anchor) if anchor else {"id": node_id, "title": node_id},
                neighbors=len(pairs),
            )
            if not pairs:
                return "no neighbors"
            return "\n".join(
                f"- [{e.label}] {n.id} | {n.title} | {n.summary}" for e, n in pairs
            )

        return f"unknown tool: {name}"

    # endregion
