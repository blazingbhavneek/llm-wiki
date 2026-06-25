"""DomainEngine — the main API from the canvas.

Coordinates database, embeddings, LLM, markdown ingestion, queries, updates,
deletion and health. Real ops throughout: embeddings via sqlite-vec, keywords/
summaries/edges via the LLM. No heuristic stand-ins.
"""

from __future__ import annotations

from pathlib import Path

from .config import Settings
from .database import Database
from .edges import build_semantic_edges
from .embeddings import Embedder
from .health import compute_health
from .ids import make_exogenous_node_id, source_hash
from .llm_client import LlmClient
from .md_ingest import load_md_output
from .models import Edge, GraphStats, Node, NodeStatus, NodeType, QueryResult


class DomainEngine:
    def __init__(
        self,
        settings: Settings | None = None,
        embedder: object | None = None,
        llm_client: object | None = None,
    ) -> None:
        self.settings = settings or Settings.from_env()
        self.database = Database(self.settings.database_path)
        self.embedder = embedder or Embedder(self.settings)
        self.llm = llm_client or LlmClient(self.settings)
        self._vec_ready = False

    def close(self) -> None:
        self.database.close()

    # ── embedding plumbing ──────────────────────────────────────────────

    def _ensure_vec(self) -> None:
        if not self._vec_ready:
            self.database.ensure_vec_tables(self.embedder.dim)
            self._vec_ready = True

    def _store_vectors(self, node: Node) -> tuple[list[float], list[float] | None]:
        self._ensure_vec()
        body_vec = self.embedder.embed_query(node.body)
        self.database.set_vector(node.id, "vec_body", body_vec)
        summary_vec = None
        if node.summary.strip():
            summary_vec = self.embedder.embed_query(node.summary)
            self.database.set_vector(node.id, "vec_summary", summary_vec)
        return body_vec, summary_vec

    # ── ingest ──────────────────────────────────────────────────────────

    def ingest(self, node: Node) -> list[Edge]:
        """Persist one node (filling derived fields) and link it semantically."""

        if not node.summary.strip():
            node.summary = self.llm.summarize(node.body)
        if not node.keywords:
            node.keywords = self.llm.extract_keywords(node.body)

        self.database.upsert_node(node)
        body_vec, summary_vec = self._store_vectors(node)
        return build_semantic_edges(
            self.database, self.llm, node, body_vec, summary_vec,
            self.settings.edge_candidate_k,
        )

    def md_to_nodes(self, md_output_dir: str | Path) -> tuple[list[Node], list[Edge]]:
        return load_md_output(md_output_dir)

    def ingest_md_output(self, md_output_dir: str | Path) -> list[Node]:
        """Ingest a whole md.py output dir: nodes, structural + semantic edges."""

        nodes, structural_edges = self.md_to_nodes(md_output_dir)
        for node in nodes:
            self.ingest(node)
        for edge in structural_edges:  # add after nodes exist
            if self.database.get_node(edge.source_node_id) and self.database.get_node(
                edge.target_node_id
            ):
                self.database.upsert_edge(edge)
        if nodes and nodes[0].original_document_name:
            src = nodes[0].source_path
            if src and Path(src).exists():
                self.database.record_source(
                    nodes[0].original_document_name,
                    source_hash(Path(src).read_text(encoding="utf-8", errors="ignore")),
                )
        return nodes

    # ── query ───────────────────────────────────────────────────────────

    def query(self, query_type: str, value: str) -> QueryResult:
        query_type = query_type.lower().strip()
        if query_type == "id":
            node = self.database.get_node(value)
            nodes = [node] if node else []
            edges = self.database.get_edges_for_node(value) if node else []
            return QueryResult(query_type=query_type, value=value, nodes=nodes, edges=edges)

        if query_type == "keyword":
            nodes = self.database.keyword_search(value, self.settings.vector_query_k)
            return QueryResult(
                query_type=query_type, value=value, nodes=nodes,
                edges=self._edges_for_nodes(nodes),
            )

        if query_type == "vector":
            self._ensure_vec()
            vec = self.embedder.embed_query(value)
            hits = self.database.vector_search(vec, "vec_body", self.settings.vector_query_k)
            seed_nodes = [self.database.get_node(nid) for nid, _ in hits]
            seed_nodes = [n for n in seed_nodes if n]
            nodes, edges = self._expand_neighborhood(seed_nodes, hops=2)
            return QueryResult(query_type=query_type, value=value, nodes=nodes, edges=edges)

        raise ValueError("query_type must be 'keyword', 'vector', or 'id'")

    def _expand_neighborhood(
        self, seeds: list[Node], hops: int = 2
    ) -> tuple[list[Node], list[Edge]]:
        seen_nodes = {n.id: n for n in seeds}
        seen_edges: dict[str, Edge] = {}
        frontier = list(seen_nodes)
        for _ in range(hops):
            nxt: list[str] = []
            for nid in frontier:
                for edge in self.database.get_edges_for_node(nid):
                    seen_edges[edge.id] = edge
                    other_id = (
                        edge.target_node_id if edge.source_node_id == nid
                        else edge.source_node_id
                    )
                    if other_id not in seen_nodes:
                        other = self.database.get_node(other_id)
                        if other:
                            seen_nodes[other_id] = other
                            nxt.append(other_id)
            frontier = nxt
        return list(seen_nodes.values()), list(seen_edges.values())

    def _edges_for_nodes(self, nodes: list[Node]) -> list[Edge]:
        seen: dict[str, Edge] = {}
        for node in nodes:
            for edge in self.database.get_edges_for_node(node.id):
                seen[edge.id] = edge
        return list(seen.values())

    # ── recon ───────────────────────────────────────────────────────────

    def recon(self, source_file: str | Path) -> dict:
        """Decide if a source doc is new or already ingested (by content hash)."""

        path = Path(source_file)
        text = path.read_text(encoding="utf-8", errors="ignore")
        current = source_hash(text)
        known = self.database.get_source(path.name)
        if known is None:
            return {"document": path.name, "status": "new", "action": "md_to_nodes+ingest"}
        if known[0] == current:
            return {"document": path.name, "status": "unchanged", "action": "skip"}
        return {"document": path.name, "status": "changed", "action": "cascading_update"}

    # ── update / delete / get / health ──────────────────────────────────

    def update(self, node_id: str, body: str) -> Node:
        node = self.database.get_node(node_id)
        if not node:
            raise KeyError(f"node not found: {node_id}")
        node.body = body
        node.summary = self.llm.summarize(body)
        node.keywords = self.llm.extract_keywords(body)
        self.database.upsert_node(node)
        body_vec, summary_vec = self._store_vectors(node)
        build_semantic_edges(
            self.database, self.llm, node, body_vec, summary_vec,
            self.settings.edge_candidate_k,
        )
        return node

    def delete(self, node_id: str) -> None:
        self.database.delete_node(node_id)

    def get(self) -> tuple[list[Node], list[Edge]]:
        return self.database.get_all_nodes(), self.database.get_all_edges()

    def health(self, node_id: str | None = None) -> GraphStats:
        nodes, edges = self.get()
        return compute_health(nodes, edges, node_id)

    # ── exogenous nodes (agent/user cache) ──────────────────────────────

    def create_exogenous_node(
        self, body: str, source_node_ids: list[str], origin: str | None = None
    ) -> Node:
        from .ids import make_edge_id

        node = Node(
            id=make_exogenous_node_id(origin or body),
            body=body, type=NodeType.exogenous,
            original_document_name=origin, cluster="Agent Notes",
            summary=self.llm.summarize(body),
            keywords=self.llm.extract_keywords(body),
        )
        self.database.upsert_node(node)
        self._store_vectors(node)
        for src in source_node_ids:
            if self.database.get_node(src):
                edge = Edge(
                    id=make_edge_id(src, node.id, "supports"),
                    source_node_id=src, target_node_id=node.id,
                    label="supports", summary="Source node supports this derived node.",
                )
                self.database.upsert_edge(edge)
        return node

    # ── pass 2 (explicit, not faked) ────────────────────────────────────

    def cascading_update(self, source_file: str | Path) -> list[str]:
        raise NotImplementedError("cascading fact-check update lands in pass 2")

    def recluster(self, resolution: float = 1.0) -> dict[str, str]:
        """Recompute node clusters via Louvain community detection."""

        from .edges import louvain_clusters

        return louvain_clusters(self.database, resolution=resolution)
