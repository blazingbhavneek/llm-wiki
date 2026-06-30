"""Synthetic knowledge nodes: durable, reusable agent memory.

A synthetic node is Markdown an LLM wrote after traversing several absolute
nodes -- a how-to, discovery, case, or comparison that exists in no single
source (handoff.md "Synthetic knowledge nodes"). It stores a *flattened* closure
of absolute dependencies and the source-version fingerprint, so a source update
marks it stale without recursive synthetic update chains.

Policy guards: an active synthetic node requires absolute evidence; the same
semantic query must recur `synthetic_repeat_query_threshold` times before one is
created; before creating, an equivalent existing node is refreshed instead.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from . import ids
from .llm import LLMClient
from .models import Edge, Evidence, Node, utcnow
from .policy import Policy
from .query import QueryResult, QueryService
from .store import Store

_WS = re.compile(r"\s+")


def normalize_query(text: str) -> str:
    return _WS.sub(" ", text.strip().lower())


class SyntheticManager:
    def __init__(
        self,
        store: Store,
        policy: Policy,
        wiki_dir: Path | str,
        llm: Optional[LLMClient] = None,
    ):
        self.store = store
        self.policy = policy
        self.wiki_dir = Path(wiki_dir)
        self.llm = llm

    # --------------------------------------------------------------- reuse

    def lookup(self, query: str) -> Optional[Node]:
        """Return an active cached synthetic node for this query, if any."""
        key = normalize_query(query)
        row = self.store.get_cache(key)
        if not row or not row["synthetic_node_id"]:
            return None
        node = self.store.get_node(row["synthetic_node_id"])
        if node and node.status == "active":
            with self.store.transaction():
                self.store.bump_cache_use(key)
            return node
        return None

    def record_query(self, query: str) -> int:
        """Count a query occurrence; returns the running total for this key."""
        key = normalize_query(query)
        with self.store.transaction():
            row = self.store.get_cache(key)
            if row is None:
                self.store.upsert_cache(
                    ids.short_hash(key, 16), key, intent="", synthetic_node_id=""
                )
            return self.store.bump_cache_use(key)

    def should_create(self, query: str, explicit: bool = False) -> bool:
        if explicit:
            return True
        threshold = int(self.policy.get("synthetic_repeat_query_threshold", 2))
        return self.record_query(query) >= threshold

    # -------------------------------------------------------------- create

    def create_or_refresh(
        self,
        query: str,
        result: QueryResult,
        kind: str = "discovery",
    ) -> Optional[Node]:
        """Create (or refresh an equivalent) synthetic node from a result.

        Refuses to create an evidence-free node when policy requires absolute
        evidence -- the system must not turn uncited speculation into a fact.
        """
        deps = self._absolute_dependencies(result)
        fingerprint = self._source_version_fingerprint(result, deps)
        requires_ev = self.policy.get("synthetic_requires_absolute_evidence", True)
        if requires_ev and not deps:
            return None

        key = normalize_query(query)
        node_id = ids.synthetic_node_id(key)
        existing = self.store.get_node(node_id)

        body = self._compose_markdown(query, result, kind)
        path = self.wiki_dir / "synthetic" / f"{node_id.split(':', 1)[1]}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

        meta = {
            "kind": kind,
            "creation_query": query,
            "absolute_dependencies": deps,
            "source_version_fingerprint": fingerprint,
            "times_retrieved": (
                existing.metadata.get("times_retrieved", 0) if existing else 0
            ),
            "times_confirmed": (
                existing.metadata.get("times_confirmed", 0) if existing else 0
            ),
            "times_refreshed": (
                (existing.metadata.get("times_refreshed", 0) + 1) if existing else 0
            ),
            "summary": self._summary_line(result),
        }
        node = Node(
            id=node_id,
            node_class="synthetic",
            node_subtype=kind,
            title=self._title(query),
            markdown_path=str(path),
            status="active",
            metadata=meta,
        )
        with self.store.transaction():
            self.store.upsert_node(node)
            self.store.fts_index(
                node.id,
                title=node.title,
                aliases=query,
                summary=node.summary,
                body=body,
            )
            self._link_dependencies(node, deps, result)
            self.store.upsert_cache(
                ids.short_hash(key, 16), key, intent=kind, synthetic_node_id=node_id
            )
        return node

    # --------------------------------------------------------------- helpers

    def _absolute_dependencies(self, result: QueryResult) -> list[str]:
        """Flattened closure of absolute node ids backing this result.

        If a synthetic node was used, expand to its own recorded absolute
        dependencies -- the flattening that avoids recursive update chains.
        """
        deps: set[str] = set()
        for rn in result.nodes:
            n = rn.node
            if n.node_class == "absolute":
                deps.add(n.id)
            else:
                for aid in n.metadata.get("absolute_dependencies", []):
                    deps.add(aid)
        return sorted(deps)

    def _source_version_fingerprint(
        self, result: QueryResult, absolute_dependencies: list[str]
    ) -> list[str]:
        """Resolve the complete absolute dependency closure to source versions.

        Canonical topics/concepts do not own a source version themselves. Their
        current supporting versions live on active incident-edge evidence, which
        must be included or source updates would leave a synthetic node trusted.
        """
        versions: set[str] = set()
        for node_id in absolute_dependencies:
            versions.update(self.store.source_versions_for_node(node_id))
        for retrieved in result.nodes:
            if retrieved.node.node_class == "synthetic":
                versions.update(
                    str(version)
                    for version in retrieved.node.metadata.get(
                        "source_version_fingerprint", []
                    )
                    if version
                )
        return sorted(versions)

    def _link_dependencies(
        self, node: Node, deps: list[str], result: QueryResult
    ) -> None:
        max_edges = int(self.policy.get("max_edges_per_synthetic_node", 10))
        scored = sorted(result.nodes, key=lambda r: -r.score)
        count = 0
        for rn in scored:
            if count >= max_edges:
                break
            if rn.node.id not in deps:
                continue
            edge = Edge(
                id=ids.edge_id(rn.node.id, node.id, "supports"),
                src_id=rn.node.id,
                dst_id=node.id,
                type="supports",
                explanation=f"{rn.node.title} supports synthetic {node.title}",
                strength=min(1.0, max(0.5, rn.score / 1000.0 + 0.5)),
                status="active",
                evidence=self._dependency_evidence(rn.node.id),
                dependencies=deps,
                created_by="query",
            )
            self.store.upsert_edge(edge)
            count += 1

    def _dependency_evidence(self, node_id: str) -> list[Evidence]:
        evidence: list[Evidence] = []
        node = self.store.get_node(node_id)
        if node and node.source_version_id:
            ranges = node.metadata.get("source_ranges", [])
            if ranges:
                evidence.append(
                    Evidence(
                        source_version_id=node.source_version_id,
                        document_id=node.document_id or "",
                        source_ranges=[list(item) for item in ranges],
                    )
                )
        for edge in self.store.edges_touching(node_id, status="active"):
            evidence.extend(edge.evidence)

        unique: dict[tuple[str, str, str], Evidence] = {}
        for item in evidence:
            key = (item.source_version_id, item.document_id, str(item.source_ranges))
            unique[key] = item
        return list(unique.values())

    def _compose_markdown(self, query: str, result: QueryResult, kind: str) -> str:
        if self.llm and self.llm.available:
            try:
                return self._llm_markdown(query, result, kind)
            except Exception:
                pass
        return self._template_markdown(query, result, kind)

    def _llm_markdown(self, query: str, result: QueryResult, kind: str) -> str:
        system = (
            f"You write a durable wiki {kind} page from provided sources. "
            "Use only the supplied context. Cite source line ranges. "
            "Do not invent facts beyond the context."
        )
        user = f"Query: {query}\n\nContext:\n{result.context_markdown()}"
        body = self.llm.complete(system, user)
        return self._frontmatter(query, kind) + body.strip() + "\n"

    def _template_markdown(self, query: str, result: QueryResult, kind: str) -> str:
        lines = [self._frontmatter(query, kind)]
        lines.append(f"# {self._title(query)}\n")
        lines.append(f"*Compiled {kind} for query:* **{query}**\n")
        lines.append("## Supporting sources\n")
        for rn in result.nodes[:10]:
            lines.append(f"- **{rn.node.title}** ({rn.node.id})")
            if rn.node.summary:
                lines.append(f"  - {rn.node.summary}")
        if result.citations:
            lines.append("\n## Citations\n")
            for c in result.citations:
                lines.append(
                    f"- {c.title} — {c.document_id} {c.source_version_id} "
                    f"lines {c.source_ranges}"
                )
        return "\n".join(lines) + "\n"

    def _frontmatter(self, query: str, kind: str) -> str:
        return (
            "---\n"
            f"node_class: synthetic\n"
            f"kind: {kind}\n"
            f'creation_query: "{query}"\n'
            f"generated_at: {utcnow()}\n"
            "---\n\n"
        )

    def _title(self, query: str) -> str:
        t = query.strip().rstrip("?.")
        return t[:1].upper() + t[1:] if t else "Synthetic note"

    def _summary_line(self, result: QueryResult) -> str:
        titles = ", ".join(rn.node.title for rn in result.nodes[:3])
        return f"Synthesized from: {titles}" if titles else "Synthetic knowledge node."
