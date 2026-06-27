"""DomainEngine — the main API from the canvas.

Coordinates database, embeddings, LLM, markdown ingestion, queries, updates,
deletion and health. Real ops throughout: embeddings via sqlite-vec, keywords/
summaries/edges via the LLM. No heuristic stand-ins.
"""

from __future__ import annotations

from collections import deque
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

_IMAGE_UNIT_RE = re.compile(
    r"<image-unit\b[^>]*>.*?</image-unit>",
    re.IGNORECASE | re.DOTALL,
)

_IMAGE_DESCRIPTION_RE = re.compile(
    r"<image-description\b[^>]*>(.*?)</image-description>",
    re.IGNORECASE | re.DOTALL,
)

_IMAGE_MEDIA_RE = re.compile(
    r"<image-media\b[^>]*>.*?</image-media>",
    re.IGNORECASE | re.DOTALL,
)

_DATA_IMAGE_URI_RE = re.compile(
    r"data:image/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/=\r\n]+",
    re.IGNORECASE,
)

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

    def _embed_with_context_fallback(self, text: str) -> list[float]:
        try:
            return self.embedder.embed_query(text)
        except Exception as exc:
            if not self._is_context_length_error(exc):
                raise

        lines = text.splitlines()
        if not lines:
            raise

        chunk_count = 2

        while chunk_count <= max(2, len(lines)):
            chunks = self._split_lines_into_chunks(lines, chunk_count)

            try:
                vectors = [self.embedder.embed_query(chunk) for chunk in chunks if chunk.strip()]
                return self._mean_vectors(vectors)
            except Exception as exc:
                if not self._is_context_length_error(exc):
                    raise
                chunk_count += 1

        raise RuntimeError(
            f"embedding failed even after splitting into {chunk_count - 1} line chunks"
        )


    def _is_context_length_error(self, exc: Exception) -> bool:
        msg = str(exc).lower()
        return (
            "maximum context length" in msg
            or "context length" in msg
            or "input_tokens" in msg
            or "too many tokens" in msg
        )


    def _split_lines_into_chunks(self, lines: list[str], chunk_count: int) -> list[str]:
        chunk_count = max(1, min(chunk_count, len(lines)))
        size = max(1, (len(lines) + chunk_count - 1) // chunk_count)

        return [
            "\n".join(lines[i:i + size])
            for i in range(0, len(lines), size)
        ]


    def _mean_vectors(self, vectors: list[list[float]]) -> list[float]:
        if not vectors:
            raise ValueError("cannot average empty embedding vector list")

        dim = len(vectors[0])

        return [
            sum(vec[i] for vec in vectors) / len(vectors)
            for i in range(dim)
        ]

    def _text_for_embedding(self, text: str) -> str:
        """Return embedding-safe text.

        Source node bodies may contain image units with inline base64 data URIs.
        Base64 is not useful for text embeddings and can exceed model context limits.

        For embedding only:
        - replace each image unit with its image-description text
        - remove image-media/base64 payloads
        - leave the original node.body unchanged in the database
        """

        if not text:
            return ""

        def replace_image_unit(match: re.Match) -> str:
            image_unit = match.group(0)
            desc_match = _IMAGE_DESCRIPTION_RE.search(image_unit)

            if desc_match:
                description = desc_match.group(1).strip()
                if description:
                    return f"\n\n[Embedded image description]\n{description}\n[/Embedded image description]\n\n"

            return "\n\n[Embedded image omitted: no description available]\n\n"

        cleaned = _IMAGE_UNIT_RE.sub(replace_image_unit, text)

        # Safety pass for malformed/partial image blocks.
        cleaned = _IMAGE_MEDIA_RE.sub(
            "\n\n[Embedded image media omitted]\n\n",
            cleaned,
        )

        # Safety pass for any remaining raw base64 data image URI.
        cleaned = _DATA_IMAGE_URI_RE.sub(
            "data:image;base64,[omitted]",
            cleaned,
        )

        return cleaned


    def _store_vectors(self, node: Node) -> tuple[list[float], list[float] | None]:
        self._ensure_vec()

        body_embedding_text = self._text_for_embedding(node.body)
        body_vec = self._embed_with_context_fallback(body_embedding_text)
        self.database.set_vector(node.id, "vec_body", body_vec)

        summary_vec = None
        if node.summary.strip():
            summary_embedding_text = self._text_for_embedding(node.summary)
            summary_vec = self._embed_with_context_fallback(summary_embedding_text)
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

        parts: list[str] = []

        for node in nodes:
            if node.source_path and Path(node.source_path).exists():
                parts.append(
                    Path(node.source_path).read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                )
            else:
                parts.append(node.body)

        return source_hash("\n\n--- NODE BREAK ---\n\n".join(parts))

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
        replacements: dict[str, str] = {}
        stale_sources: set[str] = set()
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
            replacements[old.id] = node.id
            actions.append(f"superseded:{old.id}->{node.id}")

        for old in active_old:
            if old.id in matched_old:
                continue
            self.database.set_node_status(old.id, NodeStatus.stale)
            stale_sources.add(old.id)
            actions.append(f"stale:{old.id}")

        self._cascade_dependents(replacements, stale_sources, actions)
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

    def _cascade_dependents(
        self,
        replacements: dict[str, str],
        stale_sources: set[str],
        actions: list[str],
    ) -> None:
        """Regenerate downstream exogenous nodes through provenance edges.

        Only ``supports`` edges participate. Each regenerated exogenous node is
        append-only: the old derived node is superseded, and the new one receives
        support edges from the current active support nodes.
        """

        max_hops = max(0, self.settings.cascade_max_hops)
        max_nodes = max(0, self.settings.cascade_max_nodes)
        if max_hops == 0 or max_nodes == 0:
            if replacements or stale_sources:
                actions.append("cascade-skipped:disabled")
            return

        frontier: deque[tuple[str, int]] = deque(
            (node_id, 0) for node_id in sorted(set(replacements) | set(stale_sources))
        )
        visited_dependents: set[str] = set()
        processed = 0

        while frontier:
            changed_id, depth = frontier.popleft()
            target_depth = depth + 1
            if target_depth > max_hops:
                continue

            for edge in self.database.get_outgoing_edges(changed_id, "supports"):
                target = self.database.get_node(edge.target_node_id)
                if (
                    not target
                    or target.status != NodeStatus.active
                    or target.type != NodeType.exogenous
                    or target.id in visited_dependents
                ):
                    continue

                if processed >= max_nodes:
                    actions.append(
                        f"cascade-cap-hit:max_nodes={max_nodes}:at={target.id}"
                    )
                    return

                visited_dependents.add(target.id)
                processed += 1

                support_nodes = self._current_support_nodes(target, replacements)
                if not support_nodes:
                    self.database.set_node_status(target.id, NodeStatus.stale)
                    actions.append(f"stale-exogenous:{target.id}")
                    if target_depth < max_hops:
                        frontier.append((target.id, target_depth))
                    continue

                replacement = self._regenerate_exogenous_node(target, support_nodes)
                if replacement is None:
                    self.database.set_node_status(target.id, NodeStatus.stale)
                    actions.append(f"stale-exogenous:{target.id}")
                    if target_depth < max_hops:
                        frontier.append((target.id, target_depth))
                    continue

                replacements[target.id] = replacement.id
                actions.append(f"regenerated-exogenous:{target.id}->{replacement.id}")
                if target_depth < max_hops:
                    frontier.append((target.id, target_depth))

    def _current_support_nodes(
        self, node: Node, replacements: dict[str, str]
    ) -> list[Node]:
        support_nodes: dict[str, Node] = {}
        for edge in self.database.get_incoming_edges(node.id, "supports"):
            source_id = replacements.get(edge.source_node_id, edge.source_node_id)
            source = self.database.get_node(source_id)
            if source and source.status == NodeStatus.superseded:
                replacement_id = self._active_replacement_id(source.id)
                if replacement_id:
                    source = self.database.get_node(replacement_id)
            if source and source.status == NodeStatus.active:
                support_nodes[source.id] = source
        return list(support_nodes.values())

    def _active_replacement_id(self, node_id: str) -> str | None:
        for edge in self.database.get_outgoing_edges(node_id, "superseded_by"):
            target = self.database.get_node(edge.target_node_id)
            if target and target.status == NodeStatus.active:
                return target.id
        return None

    def _regenerate_exogenous_node(
        self, old: Node, support_nodes: list[Node]
    ) -> Node | None:
        body = self.llm.regenerate_exogenous(old, support_nodes).strip()
        if not body:
            return None

        support_ids = sorted(node.id for node in support_nodes)
        version = source_hash("|".join(
            [source_hash(body), *support_ids, *(n.source_version or "" for n in support_nodes)]
        ))
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

        self.ingest(replacement)
        for support in support_nodes:
            self.database.upsert_edge(
                Edge(
                    id=make_edge_id(support.id, replacement.id, "supports"),
                    source_node_id=support.id,
                    target_node_id=replacement.id,
                    label="supports",
                    summary="Current source node supports this regenerated node.",
                )
            )
        self._supersede(old, replacement)
        return replacement

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
