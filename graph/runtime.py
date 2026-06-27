"""Runtime collaborators for the graph package."""
from __future__ import annotations
from collections import Counter
import json
import re
from typing import Any
from db import Database
from .models import (
    ClaimExtraction,
    Edge,
    EdgeSuggestion,
    EdgeSuggestions,
    GraphStats,
    Keywords,
    Node,
    NodeStatus,
    NodeType,
    QueryResult,
    Settings,
)
from .utils import make_edge_id, make_exogenous_node_id, source_hash

# region PROMPTS
GRAPH_SYSTEM_PROMPT = "You maintain a concise, factual knowledge-graph wiki."

SUMMARY_PROMPT = (
    "Summarize this markdown node for a knowledge graph. Use ONLY facts present "
    "in the text. Keep it to 1-3 sentences. No preamble."
)

KEYWORD_PROMPT = (
    "Extract the salient technical keywords/entities from this text for graph "
    "search: function names, library names, error codes, concepts, proper nouns. "
    "Return the distinct keywords, most important first, at most 12. Lowercase "
    "unless an acronym or identifier."
)

CLAIM_PROMPT = (
    "Extract stable identity facts from this markdown node for revision matching. "
    "Return one primary entity/topic and up to 20 atomic claims. A claim must be "
    "a short factual statement supported directly by the text. Prefer facts that "
    "would remain recognizable if the source document is reordered. Do not infer "
    "or add facts not present in the text."
)

REGENERATE_EXOGENOUS_PROMPT = (
    "Regenerate a derived wiki node after its supporting source material changed. "
    "Use the previous derived node only to understand the intended topic and shape. "
    "The new node body must be supported only by the CURRENT SUPPORT MATERIAL. "
    "Drop stale claims that are no longer supported. Keep the result concise, "
    "factual, and in markdown. No preamble."
)

EDGE_PROMPT = (
    "You maintain a wiki graph. Given a NEW node and a list of CANDIDATE existing "
    "nodes (already pre-filtered by semantic similarity), decide which candidates "
    "the new node should link to and why.\n"
    "Rules:\n"
    "- Only use candidate ids that were given.\n"
    "- A label is a short verb phrase describing how the target relates to the new "
    "node (e.g. 'uses', 'defines', 'example-of', 'prerequisite-for', 'contradicts').\n"
    "- Only propose an edge when the relationship is clearly useful; skip weak ones.\n"
    "- summary: one short clause explaining the link."
)
# endregion PROMPTS

# region INTERNAL CONSTANTS
_TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")
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
# endregion INTERNAL CONSTANTS
class GraphRuntime:
    # region LIFECYCLE
    def __init__(
        self,
        database: Database,
        embedder: object,
        llm: object,
        settings: Settings,
    ) -> None:
        self.database = database
        self.embedder = embedder
        self.llm = llm
        self.settings = settings
        self._vec_ready = False

    # endregion LIFECYCLE

    # region ENRICHMENT
    def fill_derived_fields(self, node: Node) -> Node:
        """Fill re-derivable metadata while preserving source-verbatim body."""

        if not node.source_material_hash:
            node.source_material_hash = source_hash(node.body)

        if not node.summary.strip():
            node.summary = self.summarize(node.body)
        if not node.keywords:
            node.keywords = self.extract_keywords(node.body)
        if not node.claims:
            extracted = self.extract_claims(node.body)
            node.entity = node.entity or extracted.entity
            node.claims = extracted.claims
        if not node.entity and node.keywords:
            node.entity = node.keywords[0]
        return node

    def summarize(self, text: str) -> str:
        if not text.strip():
            return ""
        override = getattr(self.llm, "summarize", None)
        if callable(override):
            return str(override(text) or "").strip()
        return self._run_text_query(SUMMARY_PROMPT, text)

    def extract_keywords(self, text: str) -> list[str]:
        if not text.strip():
            return []
        override = getattr(self.llm, "extract_keywords", None)
        if callable(override):
            return list(override(text))
        result = self._run_structured_query(KEYWORD_PROMPT, text[:8000], Keywords)
        parsed = result if isinstance(result, Keywords) else Keywords.model_validate(result)
        seen: list[str] = []
        seen_lower: set[str] = set()
        for keyword in parsed.keywords:
            keyword = keyword.strip()
            lowered = keyword.lower()
            if keyword and lowered not in seen_lower:
                seen.append(keyword)
                seen_lower.add(lowered)
        return seen[:12]

    def extract_claims(self, text: str) -> ClaimExtraction:
        if not text.strip():
            return ClaimExtraction()
        override = getattr(self.llm, "extract_claims", None)
        if callable(override):
            result = override(text)
            return (
                result
                if isinstance(result, ClaimExtraction)
                else ClaimExtraction.model_validate(result)
            )

        result = self._run_structured_query(CLAIM_PROMPT, text[:12000], ClaimExtraction)
        parsed = (
            result
            if isinstance(result, ClaimExtraction)
            else ClaimExtraction.model_validate(result)
        )
        claims: list[str] = []
        seen: set[str] = set()
        for claim in parsed.claims:
            claim = " ".join(claim.strip().split())
            key = claim.lower()
            if claim and key not in seen:
                seen.add(key)
                claims.append(claim)

        return ClaimExtraction(
            entity=" ".join(parsed.entity.strip().split()),
            claims=claims[:20],
        )

    # endregion ENRICHMENT

    # region EMBEDDINGS
    def ensure_vec(self) -> None:
        if not self._vec_ready:
            self.database.ensure_vec_tables(self.embedder.dim)
            self._vec_ready = True

    def store_vectors(self, node: Node) -> tuple[list[float], list[float] | None]:
        self.ensure_vec()
        body_embedding_text = self._text_for_embedding(node.body)
        body_vec = self._embed_with_context_fallback(body_embedding_text)
        self.database.set_vector(node.id, "vec_body", body_vec)
        summary_vec = None
        if node.summary.strip():
            summary_embedding_text = self._text_for_embedding(node.summary)
            summary_vec = self._embed_with_context_fallback(summary_embedding_text)
            self.database.set_vector(node.id, "vec_summary", summary_vec)
        return body_vec, summary_vec

    def _text_for_embedding(self, text: str) -> str:
        """Return embedding-safe text without changing the stored node body."""
        if not text:
            return ""

        def replace_image_unit(match: re.Match[str]) -> str:
            image_unit = match.group(0)
            desc_match = _IMAGE_DESCRIPTION_RE.search(image_unit)

            if desc_match:
                description = desc_match.group(1).strip()
                if description:
                    return "\n\n[Embedded image description]\n" f"{description}\n[/Embedded image description]\n\n"
            return "\n\n[Embedded image omitted: no description available]\n\n"
        cleaned = _IMAGE_UNIT_RE.sub(replace_image_unit, text)
        cleaned = _IMAGE_MEDIA_RE.sub("\n\n[Embedded image media omitted]\n\n", cleaned)
        cleaned = _DATA_IMAGE_URI_RE.sub("data:image;base64,[omitted]", cleaned)
        return cleaned

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
        message = str(exc).lower()
        return (
            "maximum context length" in message
            or "context length" in message
            or "input_tokens" in message
            or "too many tokens" in message
        )

    def _split_lines_into_chunks(self, lines: list[str], chunk_count: int) -> list[str]:
        chunk_count = max(1, min(chunk_count, len(lines)))
        size = max(1, (len(lines) + chunk_count - 1) // chunk_count)
        return [
            "\n".join(lines[index:index + size])
            for index in range(0, len(lines), size)
        ]

    def _mean_vectors(self, vectors: list[list[float]]) -> list[float]:
        if not vectors:
            raise ValueError("cannot average empty embedding vector list")
        dim = len(vectors[0])
        return [
            sum(vector[index] for vector in vectors) / len(vectors)
            for index in range(dim)
        ]

    # endregion EMBEDDINGS

    # region SEMANTIC EDGES
    def knn_candidates(
        self,
        node_id: str,
        body_vec: list[float],
        summary_vec: list[float] | None,
        k: int,
    ) -> list[Node]:
        ranked: list[str] = []
        probes = [("vec_body", body_vec)]
        if summary_vec:
            probes.append(("vec_summary", summary_vec))
        for table, vector in probes:
            for candidate_id, _distance in self.database.vector_search(vector, table, k + 1):
                if candidate_id != node_id and candidate_id not in ranked:
                    ranked.append(candidate_id)
        candidates: list[Node] = []
        for candidate_id in ranked:
            other = self.database.get_node(candidate_id)
            if other and other.status == NodeStatus.active:
                candidates.append(other)
        return candidates[:k]

    def build_semantic_edges(
        self,
        node: Node,
        body_vec: list[float],
        summary_vec: list[float] | None,
        k: int,
    ) -> list[Edge]:
        candidates = self.knn_candidates(node.id, body_vec, summary_vec, k)
        suggestions = self._suggest_edges(node, candidates)
        edges: list[Edge] = []
        for suggestion in suggestions:
            if suggestion.target_node_id == node.id:
                continue
            label = suggestion.label.strip() or "related"
            forward = Edge(
                id=make_edge_id(node.id, suggestion.target_node_id, label),
                source_node_id=node.id,
                target_node_id=suggestion.target_node_id,
                label=label,
                summary=suggestion.summary.strip(),
            )
            backward = Edge(
                id=make_edge_id(suggestion.target_node_id, node.id, label),
                source_node_id=suggestion.target_node_id,
                target_node_id=node.id,
                label=label,
                summary=suggestion.summary.strip(),
            )
            self.database.upsert_edge(forward)
            self.database.upsert_edge(backward)
            edges.extend([forward, backward])

        return edges

    def _suggest_edges(self, node: Node, candidates: list[Node]) -> list[EdgeSuggestion]:
        if not candidates:
            return []
        override = getattr(self.llm, "suggest_edges", None)
        if callable(override):
            return list(override(node, candidates))
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
                    "id": candidate.id,
                    "title": candidate.title,
                    "summary": candidate.summary,
                    "keywords": candidate.keywords,
                    "body": candidate.body[:1200],
                }
                for candidate in candidates
            ],
        }
        result = self._run_structured_query(
            EDGE_PROMPT,
            json.dumps(payload, ensure_ascii=False),
            EdgeSuggestions,
        )
        parsed = (
            result
            if isinstance(result, EdgeSuggestions)
            else EdgeSuggestions.model_validate(result)
        )
        allowed = {candidate.id for candidate in candidates}
        return [edge for edge in parsed.edges if edge.target_node_id in allowed]

    def _run_text_query(self, system_prompt: str, user_content: str) -> str:
        from langchain_core.messages import HumanMessage, SystemMessage
        run_messages = getattr(self.llm, "run_messages", None)
        if not callable(run_messages):
            raise TypeError("client must provide run_messages() or graph-specific overrides")
        return str(
            run_messages(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_content),
                ]
            )
            or ""
        ).strip()

    def _run_structured_query(
        self,
        system_prompt: str,
        user_content: str,
        output_model: type[Any],
    ) -> Any:
        from langchain_core.messages import HumanMessage, SystemMessage
        run_messages_structured = getattr(self.llm, "run_messages_structured", None)
        if not callable(run_messages_structured):
            raise TypeError(
                "client must provide run_messages_structured() or graph-specific overrides"
            )
        return run_messages_structured(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_content),
            ],
            output_model,
        )

    # endregion SEMANTIC EDGES

    # region EXOGENOUS REGENERATION
    def regenerate_exogenous_text(self, previous: Node, support_nodes: list[Node]) -> str:
        if not support_nodes:
            return ""
        override = getattr(self.llm, "regenerate_exogenous", None)
        if callable(override):
            return str(override(previous, support_nodes) or "").strip()
        payload = {
            "previous_node": {
                "id": previous.id,
                "title": previous.title,
                "summary": previous.summary,
                "body": previous.body[:4000],
            },
            "current_support_material": [
                {
                    "id": node.id,
                    "title": node.title,
                    "summary": node.summary,
                    "body": node.body[:2500],
                }
                for node in support_nodes[:8]
            ],
        }
        return self._run_text_query(
            REGENERATE_EXOGENOUS_PROMPT,
            json.dumps(payload, ensure_ascii=False),
        )

    # endregion EXOGENOUS REGENERATION

    # region FUTURE COMPATIBILITY
    # entity dedup logic goes here later.
    # contradiction helpers go here only if needed.
# endregion FUTURE COMPATIBILITY
class GraphQuery:
    # region LIFECYCLE
    def __init__(
        self,
        database: Database,
        embedder: object,
        settings: Settings,
        runtime: GraphRuntime,
    ) -> None:
        self.database = database
        self.embedder = embedder
        self.settings = settings
        self.runtime = runtime
    # endregion LIFECYCLE

    # region PUBLIC API
    def query(self, query_type: str, value: str) -> QueryResult:
        normalized = query_type.lower().strip()
        if normalized == "id":
            return self._query_id(value)
        if normalized == "keyword":
            return self._query_keyword(value)
        if normalized == "vector":
            return self._query_vector(value)
        raise ValueError("query_type must be 'keyword', 'vector', or 'id'")

    def search(self, text: str, limit: int | None = None) -> list[Node]:
        return self.database.keyword_search(text, limit or self.settings.vector_query_k)

    def read(self, node_id: str) -> Node | None:
        return self.database.get_node(node_id)

    def follow_link(
        self,
        node_id: str,
        label: str | None = None,
        direction: str = "both",
        limit: int | None = None,
    ) -> list[tuple[Edge, Node]]:
        normalized_direction = direction.lower().strip()
        if normalized_direction not in {"incoming", "outgoing", "both"}:
            raise ValueError("direction must be 'incoming', 'outgoing', or 'both'")
        pairs: list[tuple[Edge, Node]] = []
        if normalized_direction in {"outgoing", "both"}:
            for edge in self.database.get_outgoing_edges(node_id, label):
                target = self.database.get_node(edge.target_node_id)
                if target and target.status == NodeStatus.active:
                    pairs.append((edge, target))
        if normalized_direction in {"incoming", "both"}:
            for edge in self.database.get_incoming_edges(node_id, label):
                source = self.database.get_node(edge.source_node_id)
                if source and source.status == NodeStatus.active:
                    pairs.append((edge, source))
        return pairs[:limit] if limit is not None else pairs

    # endregion PUBLIC API

    # region QUERY MODES
    def _query_id(self, value: str) -> QueryResult:
        node = self.read(value)
        nodes = [node] if node else []
        edges = self.database.get_edges_for_node(value) if node else []
        return QueryResult(query_type="id", value=value, nodes=nodes, edges=edges)

    def _query_keyword(self, value: str) -> QueryResult:
        nodes = self.search(value, limit=self.settings.vector_query_k)
        return QueryResult(
            query_type="keyword",
            value=value,
            nodes=nodes,
            edges=self._edges_for_nodes(nodes),
        )

    def _query_vector(self, value: str) -> QueryResult:
        self.runtime.ensure_vec()
        vector = self.embedder.embed_query(value)
        hits = self.database.vector_search(vector, "vec_body", self.settings.vector_query_k)
        seed_nodes = [self.database.get_node(node_id) for node_id, _score in hits]
        seeds = [node for node in seed_nodes if node]
        nodes, edges = self._expand_neighborhood(seeds, hops=2)
        return QueryResult(query_type="vector", value=value, nodes=nodes, edges=edges)

    # endregion QUERY MODES

    # region TRAVERSAL
    def _expand_neighborhood(
        self,
        seeds: list[Node],
        hops: int = 2,
    ) -> tuple[list[Node], list[Edge]]:
        seen_nodes = {node.id: node for node in seeds}
        seen_edges: dict[str, Edge] = {}
        frontier = list(seen_nodes)
        for _ in range(hops):
            next_frontier: list[str] = []
            for node_id in frontier:
                for edge in self.database.get_edges_for_node(node_id):
                    seen_edges[edge.id] = edge
                    other_id = (
                        edge.target_node_id
                        if edge.source_node_id == node_id
                        else edge.source_node_id
                    )
                    if other_id in seen_nodes:
                        continue
                    other = self.database.get_node(other_id)
                    if other and other.status == NodeStatus.active:
                        seen_nodes[other_id] = other
                        next_frontier.append(other_id)
            frontier = next_frontier
        return list(seen_nodes.values()), list(seen_edges.values())

    def _edges_for_nodes(self, nodes: list[Node]) -> list[Edge]:
        seen: dict[str, Edge] = {}
        for node in nodes:
            for edge in self.database.get_edges_for_node(node.id):
                seen[edge.id] = edge
        return list(seen.values())

    # endregion TRAVERSAL

    # region FUTURE COMPATIBILITY
    # context_markdown helper can be added here later.
    # agent-facing scoring/traversal tweaks stay here later.
# endregion FUTURE COMPATIBILITY
class GraphExogenous:
    # region LIFECYCLE
    def __init__(
        self,
        database: Database,
        runtime: GraphRuntime,
        settings: Settings,
    ) -> None:
        self.database = database
        self.runtime = runtime
        self.settings = settings
    # endregion LIFECYCLE

    # region PUBLIC API
    def create_exogenous_node(
        self,
        body: str,
        source_node_ids: list[str],
        origin: str | None = None,
    ) -> Node:
        node = Node(
            id=make_exogenous_node_id(origin or body),
            body=body,
            type=NodeType.exogenous,
            original_document_name=origin,
            cluster="Agent Notes",
        )
        self.runtime.fill_derived_fields(node)
        self.database.upsert_node(node)
        self.runtime.store_vectors(node)
        self._link_support_edges(node, source_node_ids)
        return node

    # endregion PUBLIC API

    # region SUPPORTS GRAPH
    def _link_support_edges(self, node: Node, source_node_ids: list[str]) -> None:
        for source_id in source_node_ids:
            if not self.database.get_node(source_id):
                continue
            edge = Edge(
                id=make_edge_id(source_id, node.id, "supports"),
                source_node_id=source_id,
                target_node_id=node.id,
                label="supports",
                summary="Source node supports this derived node.",
            )
            self.database.upsert_edge(edge)

    # endregion SUPPORTS GRAPH

    # region FUTURE COMPATIBILITY
    # query cache / synthetic reuse goes here later.
    # query-time exogenous growth goes here later.
# endregion FUTURE COMPATIBILITY
class GraphAnalytics:
    # region LIFECYCLE
    def __init__(self, database: Database) -> None:
        self.database = database

    # endregion LIFECYCLE

    # region HEALTH
    def health(self, node_id: str | None = None) -> GraphStats:
        nodes = self.database.get_all_nodes()
        edges = self.database.get_all_edges()
        if node_id:
            nodes = [node for node in nodes if node.id == node_id]
            edges = [
                edge
                for edge in edges
                if edge.source_node_id == node_id or edge.target_node_id == node_id
            ]
        node_ids = {node.id for node in nodes}
        neighbors: dict[str, set[str]] = {node_id_value: set() for node_id_value in node_ids}
        for edge in edges:
            if edge.source_node_id in neighbors and edge.target_node_id in node_ids:
                neighbors[edge.source_node_id].add(edge.target_node_id)
            if edge.target_node_id in neighbors and edge.source_node_id in node_ids:
                neighbors[edge.target_node_id].add(edge.source_node_id)
        node_count = len(nodes)
        degrees = [len(neighbors[node_id_value]) for node_id_value in node_ids]
        total_degree = sum(degrees)
        avg_degree = (total_degree / node_count) if node_count else 0.0
        max_edges = node_count * (node_count - 1) / 2
        undirected_edges = total_degree / 2
        density = (undirected_edges / max_edges) if max_edges else 0.0
        clusters: dict[str, int] = {}
        for node in nodes:
            key = node.cluster or "Unclustered"
            clusters[key] = clusters.get(key, 0) + 1
        return GraphStats(
            total_nodes=node_count,
            active_nodes=sum(1 for node in nodes if node.status == NodeStatus.active),
            endogenous_nodes=sum(1 for node in nodes if node.type == NodeType.endogenous),
            exogenous_nodes=sum(1 for node in nodes if node.type == NodeType.exogenous),
            total_edges=len(edges),
            isolated_nodes=sum(1 for node_id_value in node_ids if not neighbors[node_id_value]),
            avg_degree=round(avg_degree, 3),
            density=round(density, 5),
            mean_neighbor_overlap=round(self._mean_neighbor_overlap(neighbors), 4),
            clusters=clusters,
            target_node_id=node_id,
        )

    def _mean_neighbor_overlap(self, neighbors: dict[str, set[str]]) -> float:
        pairs = 0
        total = 0.0
        for node_id, node_neighbors in neighbors.items():
            for other_id in node_neighbors:
                if other_id <= node_id:
                    continue
                other_neighbors = neighbors.get(other_id, set())
                union = node_neighbors | other_neighbors
                if union:
                    total += len(node_neighbors & other_neighbors) / len(union)
                    pairs += 1
        return (total / pairs) if pairs else 0.0

    # endregion HEALTH

    # region CLUSTERING
    def recluster(
        self,
        resolution: float = 1.0,
        seed: int = 42,
        persist: bool = True,
    ) -> dict[str, str]:
        import networkx as nx
        nodes = [node for node in self.database.get_all_nodes() if node.status == NodeStatus.active]
        node_by_id = {node.id: node for node in nodes}
        graph = nx.Graph()
        graph.add_nodes_from(node_by_id)
        for edge in self.database.get_all_edges():
            source_id = edge.source_node_id
            target_id = edge.target_node_id
            if source_id not in node_by_id or target_id not in node_by_id or source_id == target_id:
                continue
            if graph.has_edge(source_id, target_id):
                graph[source_id][target_id]["weight"] += 1.0
            else:
                graph.add_edge(source_id, target_id, weight=1.0)
        communities = nx.community.louvain_communities(
            graph,
            weight="weight",
            resolution=resolution,
            seed=seed,
        )
        mapping: dict[str, str] = {}
        used: Counter[str] = Counter()
        for index, members in enumerate(sorted(communities, key=len, reverse=True)):
            label = self._community_label(members, node_by_id, index, used)
            for node_id in members:
                mapping[node_id] = label
        if persist:
            for node in nodes:
                new_label = mapping.get(node.id)
                if new_label and node.cluster != new_label:
                    node.cluster = new_label
                    self.database.upsert_node(node)
        return mapping

    def _community_label(
        self,
        members: set[str],
        node_by_id: dict[str, Node],
        index: int,
        used: Counter[str],
    ) -> str:
        counts: Counter[str] = Counter()
        for node_id in members:
            node = node_by_id.get(node_id)
            if node:
                counts.update(keyword.lower() for keyword in node.keywords)
        label = counts.most_common(1)[0][0].title() if counts else f"Cluster {index + 1}"
        used[label] += 1
        return f"{label} {used[label]}" if used[label] > 1 else label

    # endregion CLUSTERING

    # region FUTURE COMPATIBILITY
    # maintain/lint logic can be added here later or split later.
    # endregion FUTURE COMPATIBILITY
