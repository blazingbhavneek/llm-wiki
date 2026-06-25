"""DomainEngine — the main API from the canvas.

Coordinates database, embeddings, LLM, markdown ingestion, queries, updates,
deletion and health. Real ops throughout: embeddings via sqlite-vec, keywords/
summaries/edges via the LLM. No heuristic stand-ins.
"""

from __future__ import annotations

from pathlib import Path
import re

from .config import Settings
from .database import Database
from .edges import build_semantic_edges
from .embeddings import Embedder
from .health import compute_health
from .ids import make_edge_id, make_exogenous_node_id, make_node_id, source_hash
from .llm_client import LlmClient
from .md_ingest import load_md_output
from .models import Edge, GraphStats, Node, NodeStatus, NodeType, QueryResult


_TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")
_CASCADE_MATCH_THRESHOLD = 0.45
_UNCHANGED_CLAIM_THRESHOLD = 0.9


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

    def _fill_derived_fields(self, node: Node) -> Node:
        """Fill re-derivable metadata. The body itself stays source-verbatim."""

        if not node.source_material_hash:
            node.source_material_hash = source_hash(node.body)

        if not node.summary.strip():
            node.summary = self.llm.summarize(node.body)
        if not node.keywords:
            node.keywords = self.llm.extract_keywords(node.body)
        if not node.claims:
            extracted = self.llm.extract_claims(node.body)
            node.entity = node.entity or extracted.entity
            node.claims = extracted.claims
        if not node.entity and node.keywords:
            node.entity = node.keywords[0]
        return node

    def ingest(self, node: Node) -> list[Edge]:
        """Persist one node (filling derived fields) and link it semantically."""

        self._fill_derived_fields(node)

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
        version = self._source_version_for_nodes(nodes)
        for node in nodes:
            node.source_version = version
            self.ingest(node)
        if nodes:
            self._replace_structural_edges(nodes[0].original_document_name, structural_edges)
        if nodes and nodes[0].original_document_name:
            self.database.record_source(nodes[0].original_document_name, version)
        return nodes

    def _source_version_for_nodes(self, nodes: list[Node]) -> str:
        if not nodes:
            return source_hash("")
        source_path = nodes[0].source_path
        if source_path and Path(source_path).exists():
            return source_hash(
                Path(source_path).read_text(encoding="utf-8", errors="ignore")
            )
        return source_hash("\n\n".join(node.body for node in nodes))

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
                        if other and other.status == NodeStatus.active:
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
        old = self.database.get_node(node_id)
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
            self._fill_derived_fields(old)
            self.database.upsert_node(old)
            return old
        self.ingest(replacement)
        self._supersede(old, replacement)
        return replacement

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
        """Apply a revised md.py output directory with append/supersede semantics.

        The source body is immutable. Matching is claim/entity based, so a pure
        re-order mostly remaps to existing active nodes, while changed claims
        create a new node and supersede the old one.
        """

        nodes, structural_edges = self.md_to_nodes(source_file)
        if not nodes:
            return []

        document_name = nodes[0].original_document_name or Path(source_file).name
        version = self._source_version_for_nodes(nodes)
        incoming: list[Node] = []
        for node in nodes:
            node.source_version = version
            incoming.append(self._fill_derived_fields(node))

        active_old = [
            self._ensure_revision_metadata(node)
            for node in self.database.get_nodes_by_document(document_name, active_only=True)
            if node.type == NodeType.endogenous
        ]
        if not active_old:
            for node in incoming:
                self.ingest(node)
            self._replace_structural_edges(document_name, structural_edges)
            self.database.record_source(document_name, version)
            return [f"ingested-new:{node.id}" for node in incoming]

        actions: list[str] = []
        matched_old: set[str] = set()
        exact_by_hash = {
            node.source_material_hash or source_hash(node.body): node
            for node in active_old
        }
        pending: list[Node] = []

        for node in incoming:
            exact = exact_by_hash.get(node.source_material_hash or source_hash(node.body))
            if exact and exact.id not in matched_old:
                matched_old.add(exact.id)
                actions.append(f"unchanged:{exact.id}")
            else:
                pending.append(node)

        for node in pending:
            best = self._best_revision_match(
                node, [old for old in active_old if old.id not in matched_old]
            )
            if best is None:
                self.ingest(node)
                actions.append(f"new:{node.id}")
                continue

            old, score = best
            if score < _CASCADE_MATCH_THRESHOLD:
                self.ingest(node)
                actions.append(f"new:{node.id}")
                continue

            matched_old.add(old.id)
            if self._claims_equivalent(old, node):
                actions.append(f"remapped:{old.id}")
                continue

            self.ingest(node)
            self._supersede(old, node)
            self._stale_supported_exogenous(old.id, actions)
            actions.append(f"superseded:{old.id}->{node.id}")

        for old in active_old:
            if old.id in matched_old:
                continue
            self.database.set_node_status(old.id, NodeStatus.stale)
            self._stale_supported_exogenous(old.id, actions)
            actions.append(f"stale:{old.id}")

        self._replace_structural_edges(document_name, structural_edges)
        self.database.record_source(document_name, version)
        return actions

    def _ensure_revision_metadata(self, node: Node) -> Node:
        changed = False
        if not node.source_material_hash:
            node.source_material_hash = source_hash(node.body)
            changed = True
        if not node.claims:
            extracted = self.llm.extract_claims(node.body)
            node.entity = node.entity or extracted.entity
            node.claims = extracted.claims
            changed = True
        if not node.entity and node.keywords:
            node.entity = node.keywords[0]
            changed = True
        if changed:
            self.database.upsert_node(node)
        return node

    def _best_revision_match(
        self, node: Node, candidates: list[Node]
    ) -> tuple[Node, float] | None:
        if not candidates:
            return None
        scored = [(candidate, _revision_match_score(candidate, node)) for candidate in candidates]
        return max(scored, key=lambda item: item[1])

    def _claims_equivalent(self, old: Node, new: Node) -> bool:
        old_claims = _claim_keys(old)
        new_claims = _claim_keys(new)
        if old_claims and new_claims:
            return _jaccard(old_claims, new_claims) >= _UNCHANGED_CLAIM_THRESHOLD
        return _token_jaccard(old.body, new.body) >= 0.95

    def _supersede(self, old: Node, new: Node) -> None:
        self.database.upsert_edge(
            Edge(
                id=make_edge_id(old.id, new.id, "superseded_by"),
                source_node_id=old.id,
                target_node_id=new.id,
                label="superseded_by",
                summary="Newer source material replaces these facts.",
            )
        )
        self.database.upsert_edge(
            Edge(
                id=make_edge_id(new.id, old.id, "supersedes"),
                source_node_id=new.id,
                target_node_id=old.id,
                label="supersedes",
                summary="Older source material replaced by this node.",
            )
        )
        self.database.set_node_status(old.id, NodeStatus.superseded)

    def _stale_supported_exogenous(self, source_node_id: str, actions: list[str]) -> None:
        for edge in self.database.get_outgoing_edges(source_node_id, "supports"):
            target = self.database.get_node(edge.target_node_id)
            if target and target.type == NodeType.exogenous and target.status == NodeStatus.active:
                self.database.set_node_status(target.id, NodeStatus.stale)
                actions.append(f"stale-exogenous:{target.id}")

    def _replace_structural_edges(
        self, document_name: str | None, edges: list[Edge]
    ) -> None:
        if document_name:
            node_ids = {
                node.id
                for node in self.database.get_nodes_by_document(document_name)
                if node.type == NodeType.endogenous
            }
            self.database.delete_edges_by_label_for_nodes("follows", node_ids)
        for edge in edges:
            source = self.database.get_node(edge.source_node_id)
            target = self.database.get_node(edge.target_node_id)
            if (
                source and target
                and source.status == NodeStatus.active
                and target.status == NodeStatus.active
            ):
                self.database.upsert_edge(edge)

    def recluster(self, resolution: float = 1.0) -> dict[str, str]:
        """Recompute node clusters via Louvain community detection."""

        from .edges import louvain_clusters

        return louvain_clusters(self.database, resolution=resolution)


def _revision_match_score(old: Node, new: Node) -> float:
    claim_score = _jaccard(_claim_keys(old), _claim_keys(new))
    keyword_score = _jaccard(
        {_normalize_token(k) for k in old.keywords},
        {_normalize_token(k) for k in new.keywords},
    )
    body_score = _token_jaccard(old.body, new.body)
    entity_bonus = 0.0
    if old.entity and new.entity:
        entity_bonus = 0.2 if _normalize_text(old.entity) == _normalize_text(new.entity) else 0.0
    return min(1.0, max(claim_score, keyword_score * 0.8, body_score * 0.65) + entity_bonus)


def _claim_keys(node: Node) -> set[str]:
    return {_normalize_text(claim) for claim in node.claims if _normalize_text(claim)}


def _token_jaccard(left: str, right: str) -> float:
    return _jaccard({_normalize_token(t) for t in _TOKEN_RE.findall(left.lower())},
                    {_normalize_token(t) for t in _TOKEN_RE.findall(right.lower())})


def _jaccard(left: set[str], right: set[str]) -> float:
    left = {x for x in left if x}
    right = {x for x in right if x}
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _normalize_text(text: str) -> str:
    return " ".join(_normalize_token(tok) for tok in _TOKEN_RE.findall(text.lower()))


def _normalize_token(token: str) -> str:
    return token.strip().lower()
