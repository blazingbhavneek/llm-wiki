"""The one query service every interface uses (handoff.md "Query behavior").

Normal wiki search, keyword/FTS, future vector/Elasticsearch adapters, LLM
agents, and the future UI all call QueryService. It seeds from exact-title +
FTS hits, ranks absolute pages and active synthetic nodes, expands one/two typed
weighted hops within a strict budget (preferring local document-subgraph hops),
and returns Markdown with exact source citations. Stale synthetic nodes are
excluded from trusted retrieval.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .models import Edge, Node
from .policy import Policy
from .search import Fts5Backend, SearchBackend, SearchHit
from .store import Store


@dataclass
class Citation:
    document_id: str
    source_version_id: str
    source_ranges: list[list[int]]
    title: str


@dataclass
class RetrievedNode:
    node: Node
    score: float
    hop: int
    via: str = "seed"


@dataclass
class QueryResult:
    query: str
    nodes: list[RetrievedNode] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)

    def seeds(self) -> list[RetrievedNode]:
        return [r for r in self.nodes if r.hop == 0]

    def context_markdown(self, max_chars: int = 12000) -> str:
        """Assemble LLM-ready context: selected Markdown + citations."""
        parts: list[str] = []
        used = 0
        for r in self.nodes:
            n = r.node
            header = f"## {n.title}  (id={n.id}, score={r.score:.2f}, hop={r.hop})"
            body = ""
            if n.markdown_path and Path(n.markdown_path).exists():
                body = Path(n.markdown_path).read_text(encoding="utf-8")
            else:
                body = n.summary
            block = f"{header}\n\n{body}\n"
            if used + len(block) > max_chars:
                block = block[: max(0, max_chars - used)]
            parts.append(block)
            used += len(block)
            if used >= max_chars:
                break
        if self.citations:
            cites = "\n".join(
                f"- {c.title} [{c.document_id} {c.source_version_id} "
                f"lines {c.source_ranges}]"
                for c in self.citations
            )
            parts.append(f"\n### Citations\n{cites}\n")
        return "\n".join(parts)


class QueryService:
    def __init__(
        self,
        store: Store,
        policy: Policy,
        backend: Optional[SearchBackend] = None,
    ):
        self.store = store
        self.policy = policy
        self.fts = Fts5Backend(store)
        self.backend = backend or self.fts

    def query(self, text: str, limit: Optional[int] = None) -> QueryResult:
        budget = limit or self.policy.get("max_query_nodes", 30)
        min_strength = self.policy.get("minimum_active_strength", 0.45)
        exclude_stale = self.policy.get("exclude_stale_synthetic_nodes", True)

        # 1. seeds: exact title first, then FTS
        seed_hits: dict[str, float] = {}
        for hit in self.fts.exact_title(text):
            seed_hits[hit.node_id] = max(seed_hits.get(hit.node_id, 0), hit.score)
        for hit in self.backend.search(text, limit=budget):
            seed_hits[hit.node_id] = max(seed_hits.get(hit.node_id, 0), hit.score)

        retrieved: dict[str, RetrievedNode] = {}
        for nid, score in seed_hits.items():
            node = self.store.get_node(nid)
            if node is None or node.status not in ("active",):
                continue
            if node.node_class == "synthetic" and exclude_stale and node.status != "active":
                continue
            retrieved[nid] = RetrievedNode(node=node, score=score, hop=0)

        # 2. bounded typed/weighted traversal
        max_hops = int(self.policy.get("max_semantic_hops", 2))
        decay = float(self.policy.get("second_hop_decay", 0.35))
        frontier = list(retrieved.values())
        for hop in range(1, max_hops + 1):
            next_frontier: list[RetrievedNode] = []
            for rn in sorted(frontier, key=lambda item: -item.score):
                if len(retrieved) >= budget:
                    break
                for edge in self._expand_edges(rn.node, min_strength):
                    other_id = edge.dst_id if edge.src_id == rn.node.id else edge.src_id
                    if other_id in retrieved:
                        continue
                    other = self.store.get_node(other_id)
                    if other is None or other.status != "active":
                        continue
                    score = (
                        rn.score
                        * self._traversal_strength(edge)
                        * (decay ** (hop - 1))
                    )
                    nxt = RetrievedNode(
                        node=other, score=score, hop=hop, via=edge.type
                    )
                    retrieved[other_id] = nxt
                    next_frontier.append(nxt)
                    if len(retrieved) >= budget:
                        break
            frontier = next_frontier
            if not frontier:
                break

        ordered = sorted(retrieved.values(), key=lambda r: -r.score)[:budget]
        result = QueryResult(query=text, nodes=ordered)
        result.citations = self._citations(ordered)
        return result

    def _expand_edges(self, node: Node, min_strength: float) -> list[Edge]:
        """Local document-subgraph hops first, then weaker global jumps."""
        edges = [
            e
            for e in self.store.edges_touching(node.id, status="active")
            if e.strength >= min_strength
        ]
        # Prefer structural/local edges and same-document targets, but never
        # expand an entire book merely because its document root was a seed.
        def rank(e: Edge) -> tuple[int, float]:
            local = 0
            other_id = e.dst_id if e.src_id == node.id else e.src_id
            other = self.store.get_node(other_id)
            if other and node.document_id and other.document_id == node.document_id:
                local = 1
            return (local, self._traversal_strength(e))

        edges = sorted(edges, key=rank, reverse=True)
        if node.node_subtype == "document":
            local_limit = int(self.policy.get("max_local_pages_from_document", 6))
            edges = [edge for edge in edges if edge.type == "contains"][:local_limit]
        else:
            edges = edges[: int(self.policy.get("max_edges_per_expansion", 8))]
        return edges

    def _traversal_strength(self, edge: Edge) -> float:
        if edge.type == "contains":
            return edge.strength * float(
                self.policy.get("contains_traversal_weight", 0.1)
            )
        return edge.strength

    def _citations(self, nodes: list[RetrievedNode]) -> list[Citation]:
        cites: list[Citation] = []
        seen: set[tuple] = set()
        for rn in nodes:
            n = rn.node
            ranges = n.metadata.get("source_ranges")
            if not ranges or not n.source_version_id:
                continue
            key = (n.document_id, n.source_version_id, str(ranges))
            if key in seen:
                continue
            seen.add(key)
            cites.append(
                Citation(
                    document_id=n.document_id or "",
                    source_version_id=n.source_version_id,
                    source_ranges=ranges,
                    title=n.title,
                )
            )
        return cites
