"""Runtime collaborators for the graph package."""
from __future__ import annotations
from collections import Counter
from typing import Callable
import json
from db import Database
from .models import (
    ClaimExtraction,
    Edge,
    EdgeSuggestion,
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
from .utils import make_edge_id, make_exogenous_node_id, source_hash

import re
from difflib import SequenceMatcher

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

AGENT_SYSTEM_PROMPT = (
    "You answer questions by navigating a knowledge-graph wiki. You cannot see the "
    "graph directly; you must use tools to gather evidence.\n\n"

    "Tools:\n"
    "- search(text): find candidate nodes by keyword.\n"
    "- read(node_id): read a node's full body.\n"
    "- follow_link(node_id, direction): jump to a node's neighbors.\n"
    "- finish(answer, cited_node_ids): end with your answer and the node ids you used.\n\n"

    "Critical rules:\n"
    "1. Do NOT answer early.\n"
    "2. Search results are only summaries; they are NOT enough evidence.\n"
    "3. You must read full node bodies before answering.\n"
    "4. Before calling finish, read at least 3 relevant nodes when available.\n"
    "5. For API/function questions, specifically read nodes for each mentioned function name.\n"
    "6. If the question mentions multiple functions, search and read evidence for each one.\n"
    "7. If a read fails, retry using the exact full node_id from search results, including the 'node:' prefix.\n"
    "8. Prefer reading promising nodes over finishing early.\n"
    "9. Follow links when a read node references related concepts, examples, events, or required setup.\n"
    "10. Base the final answer ONLY on node bodies you actually read.\n\n"

    "Suggested workflow:\n"
    "1. Search the main query.\n"
    "2. Read the top relevant search results.\n"
    "3. Search individual important terms/functions from the question.\n"
    "4. Read those function-specific nodes.\n"
    "5. Follow links from important nodes if needed.\n"
    "6. Only then call finish.\n\n"

    "For this wiki, node ids often start with 'node:'. Always copy node ids exactly as shown.\n"
    "Never remove the 'node:' prefix.\n\n"

    "You should only call finish when you have enough full-body evidence to give a useful, concrete answer. "
    "If you have read fewer than 3 useful nodes and more relevant nodes are available, keep searching or reading."
)

ENTITY_DEDUP_PROMPT = (
    "You maintain a wiki graph. Given a NEW node and a list of CANDIDATE existing "
    "nodes, decide whether the new node describes the SAME real-world entity/topic "
    "as exactly one candidate.\n"
    "Rules:\n"
    "- Same entity means the same concrete thing (same API, same tool, same concept), "
    "not merely a related or similar topic.\n"
    "- Be conservative: if unsure, answer is_same=false. Never merge homonyms that "
    "refer to different things.\n"
    "- If there is a match, return is_same=true and target_node_id of that candidate; "
    "otherwise is_same=false and target_node_id=null."
)
# endregion PROMPTS

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
        return self.llm.complete(SUMMARY_PROMPT, text).strip()

    def extract_keywords(self, text: str) -> list[str]:
        if not text.strip():
            return []
        override = getattr(self.llm, "extract_keywords", None)
        if callable(override):
            return list(override(text))
        result = self.llm.complete_structured(KEYWORD_PROMPT, text[:8000], Keywords)
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

        result = self.llm.complete_structured(CLAIM_PROMPT, text[:12000], ClaimExtraction)
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

    # region DEDUP
    def node_is_complete(self, node_id: str) -> bool:
        """True if the node exists, is active, and its body vector is stored.

        Used to skip re-processing an already-ingested node (idempotent re-add,
        crash resume). Body-vector presence proves enrich+embed finished.
        """
        node = self.database.get_node(node_id)
        if not node or node.status != NodeStatus.active:
            return False
        has_vector = getattr(self.database, "has_vector", None)
        if callable(has_vector):
            return bool(has_vector(node_id))
        return True

    def same_as_group(self, node_id: str) -> set[str]:
        """Ids in this node's same-as equivalence class (including itself)."""
        group = {node_id}
        for edge in self.database.get_edges_for_node(node_id):
            if edge.label != "same-as":
                continue
            other = (
                edge.target_node_id
                if edge.source_node_id == node_id
                else edge.source_node_id
            )
            group.add(other)
        return group

    def collapse_same_as(self, nodes: list[Node]) -> list[Node]:
        """Keep one representative per same-as cluster, preserving input order.

        Use-time collapse: storage keeps every contextually-distinct node, but
        callers (edge candidates, regen supports, agent results) treat a same-as
        cluster as one unit so processing cost stays bounded as the graph grows.
        """
        kept: list[Node] = []
        seen: set[str] = set()
        for node in nodes:
            if node.id in seen:
                continue
            kept.append(node)
            seen |= self.same_as_group(node.id)
        return kept

    # endregion DEDUP

    # region EMBEDDINGS
    def ensure_vec(self) -> None:
        if not self._vec_ready:
            self.database.ensure_vec_tables(self.embedder.dim)
            self._vec_ready = True

    def store_vectors(self, node: Node) -> tuple[list[float], list[float] | None]:
        self.ensure_vec()
        body_vec = self.embedder.embed_document(node.body)
        self.database.set_vector(node.id, "vec_body", body_vec)
        summary_vec = None
        if node.summary.strip():
            summary_vec = self.embedder.embed_document(node.summary)
            self.database.set_vector(node.id, "vec_summary", summary_vec)
        return body_vec, summary_vec

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
        return self.collapse_same_as(candidates)[:k]

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
            target_id = suggestion.target_node_id
            if target_id == node.id:
                continue
            label = suggestion.label.strip() or "related"
            stamp = now_iso()
            if label == "contradicts":
                self._invalidate_prior_edges(node.id, target_id, stamp)
            episodes = [node.id, target_id]
            forward = Edge(
                id=make_edge_id(node.id, target_id, label),
                source_node_id=node.id,
                target_node_id=target_id,
                label=label,
                summary=suggestion.summary.strip(),
                valid_at=stamp,
                source_episode_ids=episodes,
            )
            backward = Edge(
                id=make_edge_id(target_id, node.id, label),
                source_node_id=target_id,
                target_node_id=node.id,
                label=label,
                summary=suggestion.summary.strip(),
                valid_at=stamp,
                source_episode_ids=episodes,
            )
            self.database.upsert_edge(forward)
            self.database.upsert_edge(backward)
            edges.extend([forward, backward])

        return edges

    def _invalidate_prior_edges(self, source_id: str, target_id: str, stamp: str) -> None:
        """Mark existing non-contradiction edges between a pair as invalid."""
        for edge in self.database.get_edges_for_node(target_id):
            endpoints = {edge.source_node_id, edge.target_node_id}
            if endpoints != {source_id, target_id}:
                continue
            if edge.label == "contradicts" or edge.invalid_at:
                continue
            edge.invalid_at = stamp
            edge.expired_at = stamp
            self.database.upsert_edge(edge)

    def link_entity_duplicates(self, node: Node, candidates: list[Node]) -> list[Edge]:
        """Detect a same-real-world-entity neighbor and link with a same-as edge."""
        if not candidates:
            return []
        match = self._check_entity_duplicate(node, candidates)
        if not match.is_same or not match.target_node_id:
            return []
        allowed = {candidate.id for candidate in candidates}
        if match.target_node_id not in allowed or match.target_node_id == node.id:
            return []
        stamp = now_iso()
        episodes = [node.id, match.target_node_id]
        edges = []
        for src, dst in ((node.id, match.target_node_id), (match.target_node_id, node.id)):
            edge = Edge(
                id=make_edge_id(src, dst, "same-as"),
                source_node_id=src,
                target_node_id=dst,
                label="same-as",
                summary="Same real-world entity.",
                valid_at=stamp,
                source_episode_ids=episodes,
            )
            self.database.upsert_edge(edge)
            edges.append(edge)
        return edges

    def _check_entity_duplicate(self, node: Node, candidates: list[Node]) -> EntityMatch:
        override = getattr(self.llm, "check_entity_duplicate", None)
        if callable(override):
            result = override(node, candidates)
            return result if isinstance(result, EntityMatch) else EntityMatch.model_validate(result)
        payload = {
            "new_node": {
                "id": node.id,
                "title": node.title,
                "entity": node.entity,
                "summary": node.summary,
            },
            "candidates": [
                {
                    "id": candidate.id,
                    "title": candidate.title,
                    "entity": candidate.entity,
                    "summary": candidate.summary,
                }
                for candidate in candidates
            ],
        }
        result = self.llm.complete_structured(
            ENTITY_DEDUP_PROMPT,
            json.dumps(payload, ensure_ascii=False),
            EntityMatch,
        )
        return result if isinstance(result, EntityMatch) else EntityMatch.model_validate(result)

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
        result = self.llm.complete_structured(
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
        return self.llm.complete(
            REGENERATE_EXOGENOUS_PROMPT,
            json.dumps(payload, ensure_ascii=False),
        ).strip()

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

        print("[GraphQuery.__init__] initialized", flush=True)
        print(f"[GraphQuery.__init__] database={database}", flush=True)
        print(f"[GraphQuery.__init__] embedder={embedder}", flush=True)
        print(f"[GraphQuery.__init__] settings={settings}", flush=True)
        print(f"[GraphQuery.__init__] runtime={runtime}", flush=True)

    # endregion LIFECYCLE

    # region PUBLIC API
    def query(self, query_type: str, value: str) -> QueryResult:
        print("\n[GraphQuery.query] called", flush=True)
        print(f"[GraphQuery.query] query_type={query_type!r}", flush=True)
        print(f"[GraphQuery.query] value={value!r}", flush=True)

        normalized = query_type.lower().strip()
        print(f"[GraphQuery.query] normalized={normalized!r}", flush=True)

        if normalized == "id":
            return self._query_id(value)
        if normalized == "keyword":
            return self._query_keyword(value)
        if normalized == "vector":
            return self._query_vector(value)

        raise ValueError("query_type must be 'keyword', 'vector', or 'id'")

    def search(self, text: str, limit: int | None = None) -> list[Node]:
        """Hybrid BM25 + semantic search, fused with Reciprocal Rank Fusion.

        Three ranked lists (FTS5/BM25 over bodies, KNN over vec_body, KNN over
        vec_summary) are combined by RRF so a node strong in any one signal
        surfaces. Falls back to BM25-only if embedding the query fails.
        """

        print("\n" + "=" * 80, flush=True)
        print("[GraphQuery.search] called", flush=True)
        print(f"[GraphQuery.search] text={text!r}", flush=True)
        print(f"[GraphQuery.search] incoming limit={limit}", flush=True)

        limit = limit or self.settings.vector_query_k
        pool = max(limit, 10)

        print(f"[GraphQuery.search] resolved limit={limit}", flush=True)
        print(f"[GraphQuery.search] pool={pool}", flush=True)

        ranked_lists: list[list[str]] = []

        print("[GraphQuery.search] running keyword_search / BM25", flush=True)
        keyword_nodes = self.database.keyword_search(text, pool)
        keyword_ids = [node.id for node in keyword_nodes]

        print(f"[GraphQuery.search] keyword_search returned {len(keyword_nodes)} node(s)", flush=True)
        for i, node in enumerate(keyword_nodes, start=1):
            print(
                f"[GraphQuery.search] BM25 {i}. id={node.id!r} | title={node.title!r}",
                flush=True,
            )
            print(
                f"[GraphQuery.search] BM25 {i}. summary={(node.summary or '')[:300]!r}",
                flush=True,
            )

        ranked_lists.append(keyword_ids)

        try:
            print("[GraphQuery.search] ensuring vector extension/table availability", flush=True)
            self.runtime.ensure_vec()

            print("[GraphQuery.search] embedding query", flush=True)
            query_vec = self.embedder.embed_query(text)

            try:
                print(f"[GraphQuery.search] query_vec length={len(query_vec)}", flush=True)
            except Exception:
                print("[GraphQuery.search] query_vec length unavailable", flush=True)

            for table in ("vec_body", "vec_summary"):
                print(f"[GraphQuery.search] running vector_search table={table!r}", flush=True)

                vector_hits = self.database.vector_search(query_vec, table, pool)
                vector_ids = [node_id for node_id, _score in vector_hits]

                print(
                    f"[GraphQuery.search] vector_search table={table!r} returned {len(vector_hits)} hit(s)",
                    flush=True,
                )

                for i, hit in enumerate(vector_hits, start=1):
                    node_id, score = hit
                    print(
                        f"[GraphQuery.search] VECTOR {table} {i}. id={node_id!r} score={score}",
                        flush=True,
                    )

                ranked_lists.append(vector_ids)

        except Exception as exc:  # noqa: BLE001 - embedding/vec unavailable: degrade to BM25
            print("[GraphQuery.search] vector search failed; falling back to BM25-only", flush=True)
            print(f"[GraphQuery.search] vector exception={repr(exc)}", flush=True)

        print("[GraphQuery.search] ranked_lists before RRF:", flush=True)
        for i, ids in enumerate(ranked_lists, start=1):
            print(f"[GraphQuery.search] ranked_list[{i}] count={len(ids)} ids={ids}", flush=True)

        fused_ids = self._rrf(ranked_lists)

        print(f"[GraphQuery.search] RRF fused ids count={len(fused_ids)}", flush=True)
        print(f"[GraphQuery.search] RRF fused ids={fused_ids}", flush=True)

        nodes: list[Node] = []

        for node_id in fused_ids:
            print(f"[GraphQuery.search] loading fused node_id={node_id!r}", flush=True)
            node = self.database.get_node(node_id)

            if node is None:
                print(f"[GraphQuery.search] node_id={node_id!r} NOT FOUND in database", flush=True)
                continue

            print(
                f"[GraphQuery.search] loaded node id={node.id!r} title={node.title!r} status={node.status}",
                flush=True,
            )

            if node.status == NodeStatus.active:
                nodes.append(node)
                print(f"[GraphQuery.search] accepted active node id={node.id!r}", flush=True)
            else:
                print(f"[GraphQuery.search] skipped inactive node id={node.id!r}", flush=True)

            if len(nodes) >= limit:
                print("[GraphQuery.search] reached limit; stopping", flush=True)
                break

        print(f"[GraphQuery.search] returning {len(nodes)} node(s)", flush=True)
        for i, node in enumerate(nodes, start=1):
            print(
                f"[GraphQuery.search] RETURN {i}. id={node.id!r} | title={node.title!r}",
                flush=True,
            )
            print(
                f"[GraphQuery.search] RETURN {i}. summary={(node.summary or '')[:500]!r}",
                flush=True,
            )

        print("=" * 80 + "\n", flush=True)
        return nodes

    def _rrf(self, ranked_lists: list[list[str]]) -> list[str]:
        """Reciprocal Rank Fusion: sum 1/(k + rank) of each id across lists."""

        print("\n[GraphQuery._rrf] called", flush=True)

        k = self.settings.search_rrf_k
        scores: dict[str, float] = {}

        print(f"[GraphQuery._rrf] k={k}", flush=True)

        for list_index, ids in enumerate(ranked_lists, start=1):
            print(
                f"[GraphQuery._rrf] processing ranked_list[{list_index}] count={len(ids)}",
                flush=True,
            )

            for rank, node_id in enumerate(ids):
                contribution = 1.0 / (k + rank + 1)
                scores[node_id] = scores.get(node_id, 0.0) + contribution

                print(
                    f"[GraphQuery._rrf] node_id={node_id!r} rank={rank} "
                    f"contribution={contribution} total_score={scores[node_id]}",
                    flush=True,
                )

        sorted_ids = sorted(scores, key=lambda node_id: scores[node_id], reverse=True)

        print("[GraphQuery._rrf] final scores:", flush=True)
        for node_id in sorted_ids:
            print(f"[GraphQuery._rrf] id={node_id!r} score={scores[node_id]}", flush=True)

        return sorted_ids

    def read(self, node_id: str) -> Node | None:
        print("\n" + "=" * 80, flush=True)
        print("[GraphQuery.read] called", flush=True)
        print(f"[GraphQuery.read] node_id={node_id!r}", flush=True)

        node = self.database.get_node(node_id)

        if node:
            print("[GraphQuery.read] exact lookup succeeded", flush=True)
            print(f"[GraphQuery.read] found id={node.id!r} title={node.title!r}", flush=True)
            print("=" * 80 + "\n", flush=True)
            return node

        print("[GraphQuery.read] exact lookup failed", flush=True)

        if not node_id.startswith("node:"):
            repaired_id = f"node:{node_id}"
            print(f"[GraphQuery.read] trying repaired_id={repaired_id!r}", flush=True)

            node = self.database.get_node(repaired_id)

            if node:
                print("[GraphQuery.read] repaired lookup succeeded", flush=True)
                print(f"[GraphQuery.read] found id={node.id!r} title={node.title!r}", flush=True)
                print("=" * 80 + "\n", flush=True)
                return node

            print("[GraphQuery.read] repaired lookup failed", flush=True)

        print("[GraphQuery.read] trying fuzzy/keyword fallback", flush=True)
        matches = self.database.keyword_search(node_id, 5)

        print(f"[GraphQuery.read] fuzzy matches={len(matches)}", flush=True)

        for i, match in enumerate(matches, start=1):
            print(
                f"[GraphQuery.read] fuzzy {i}. id={match.id!r} title={match.title!r}",
                flush=True,
            )
            print(
                f"[GraphQuery.read] fuzzy {i}. summary={(match.summary or '')[:300]!r}",
                flush=True,
            )

        if matches:
            node = matches[0]
            print("[GraphQuery.read] using best fuzzy match", flush=True)
            print(f"[GraphQuery.read] selected id={node.id!r} title={node.title!r}", flush=True)
            print("=" * 80 + "\n", flush=True)
            return node

        print("[GraphQuery.read] result=None / NODE NOT FOUND", flush=True)
        print("=" * 80 + "\n", flush=True)
        return None

    def follow_link(
        self,
        node_id: str,
        label: str | None = None,
        direction: str = "both",
        limit: int | None = None,
    ) -> list[tuple[Edge, Node]]:
        print("\n" + "=" * 80, flush=True)
        print("[GraphQuery.follow_link] called", flush=True)
        print(f"[GraphQuery.follow_link] node_id={node_id!r}", flush=True)
        print(f"[GraphQuery.follow_link] label={label!r}", flush=True)
        print(f"[GraphQuery.follow_link] direction={direction!r}", flush=True)
        print(f"[GraphQuery.follow_link] limit={limit}", flush=True)

        normalized_direction = direction.lower().strip()
        print(f"[GraphQuery.follow_link] normalized_direction={normalized_direction!r}", flush=True)

        if normalized_direction not in {"incoming", "outgoing", "both"}:
            raise ValueError("direction must be 'incoming', 'outgoing', or 'both'")

        pairs: list[tuple[Edge, Node]] = []

        if normalized_direction in {"outgoing", "both"}:
            print("[GraphQuery.follow_link] loading outgoing edges", flush=True)

            outgoing_edges = self.database.get_outgoing_edges(node_id, label)
            print(
                f"[GraphQuery.follow_link] outgoing edge count={len(outgoing_edges)}",
                flush=True,
            )

            for edge in outgoing_edges:
                print(
                    f"[GraphQuery.follow_link] outgoing edge id={edge.id!r} "
                    f"label={edge.label!r} target={edge.target_node_id!r}",
                    flush=True,
                )

                target = self.database.get_node(edge.target_node_id)

                if target is None:
                    print(
                        f"[GraphQuery.follow_link] target node NOT FOUND id={edge.target_node_id!r}",
                        flush=True,
                    )
                    continue

                print(
                    f"[GraphQuery.follow_link] target node found id={target.id!r} "
                    f"title={target.title!r} status={target.status}",
                    flush=True,
                )

                if target.status == NodeStatus.active:
                    pairs.append((edge, target))
                    print(
                        f"[GraphQuery.follow_link] accepted outgoing neighbor id={target.id!r}",
                        flush=True,
                    )
                else:
                    print(
                        f"[GraphQuery.follow_link] skipped inactive outgoing neighbor id={target.id!r}",
                        flush=True,
                    )

        if normalized_direction in {"incoming", "both"}:
            print("[GraphQuery.follow_link] loading incoming edges", flush=True)

            incoming_edges = self.database.get_incoming_edges(node_id, label)
            print(
                f"[GraphQuery.follow_link] incoming edge count={len(incoming_edges)}",
                flush=True,
            )

            for edge in incoming_edges:
                print(
                    f"[GraphQuery.follow_link] incoming edge id={edge.id!r} "
                    f"label={edge.label!r} source={edge.source_node_id!r}",
                    flush=True,
                )

                source = self.database.get_node(edge.source_node_id)

                if source is None:
                    print(
                        f"[GraphQuery.follow_link] source node NOT FOUND id={edge.source_node_id!r}",
                        flush=True,
                    )
                    continue

                print(
                    f"[GraphQuery.follow_link] source node found id={source.id!r} "
                    f"title={source.title!r} status={source.status}",
                    flush=True,
                )

                if source.status == NodeStatus.active:
                    pairs.append((edge, source))
                    print(
                        f"[GraphQuery.follow_link] accepted incoming neighbor id={source.id!r}",
                        flush=True,
                    )
                else:
                    print(
                        f"[GraphQuery.follow_link] skipped inactive incoming neighbor id={source.id!r}",
                        flush=True,
                    )

        result = pairs[:limit] if limit is not None else pairs

        print(f"[GraphQuery.follow_link] returning {len(result)} pair(s)", flush=True)
        for i, pair in enumerate(result, start=1):
            edge, node = pair
            print(
                f"[GraphQuery.follow_link] RETURN {i}. edge_label={edge.label!r} "
                f"node_id={node.id!r} title={node.title!r}",
                flush=True,
            )

        print("=" * 80 + "\n", flush=True)
        return result

    # endregion PUBLIC API

    # region QUERY MODES
    def _query_id(self, value: str) -> QueryResult:
        print("\n[GraphQuery._query_id] called", flush=True)
        print(f"[GraphQuery._query_id] value={value!r}", flush=True)

        node = self.read(value)
        nodes = [node] if node else []
        edges = self.database.get_edges_for_node(value) if node else []

        print(f"[GraphQuery._query_id] nodes={len(nodes)} edges={len(edges)}", flush=True)

        return QueryResult(query_type="id", value=value, nodes=nodes, edges=edges)

    def _query_keyword(self, value: str) -> QueryResult:
        print("\n[GraphQuery._query_keyword] called", flush=True)
        print(f"[GraphQuery._query_keyword] value={value!r}", flush=True)

        nodes = self.database.keyword_search(value, self.settings.vector_query_k)

        print(f"[GraphQuery._query_keyword] keyword_search returned {len(nodes)} node(s)", flush=True)
        for i, node in enumerate(nodes, start=1):
            print(
                f"[GraphQuery._query_keyword] {i}. id={node.id!r} title={node.title!r}",
                flush=True,
            )

        edges = self._edges_for_nodes(nodes)

        print(f"[GraphQuery._query_keyword] edges={len(edges)}", flush=True)

        return QueryResult(
            query_type="keyword",
            value=value,
            nodes=nodes,
            edges=edges,
        )

    def _query_vector(self, value: str) -> QueryResult:
        print("\n[GraphQuery._query_vector] called", flush=True)
        print(f"[GraphQuery._query_vector] value={value!r}", flush=True)

        self.runtime.ensure_vec()

        print("[GraphQuery._query_vector] embedding query", flush=True)
        vector = self.embedder.embed_query(value)

        print("[GraphQuery._query_vector] running vector_search vec_body", flush=True)
        hits = self.database.vector_search(vector, "vec_body", self.settings.vector_query_k)

        print(f"[GraphQuery._query_vector] hits={len(hits)}", flush=True)
        for i, hit in enumerate(hits, start=1):
            node_id, score = hit
            print(
                f"[GraphQuery._query_vector] hit {i}. id={node_id!r} score={score}",
                flush=True,
            )

        seed_nodes = [self.database.get_node(node_id) for node_id, _score in hits]
        seeds = [node for node in seed_nodes if node]

        print(f"[GraphQuery._query_vector] seeds={len(seeds)}", flush=True)

        nodes, edges = self._expand_neighborhood(seeds, hops=2)

        print(f"[GraphQuery._query_vector] expanded nodes={len(nodes)} edges={len(edges)}", flush=True)

        return QueryResult(query_type="vector", value=value, nodes=nodes, edges=edges)

    # endregion QUERY MODES

    # region TRAVERSAL
    def _expand_neighborhood(
        self,
        seeds: list[Node],
        hops: int = 2,
    ) -> tuple[list[Node], list[Edge]]:
        print("\n[GraphQuery._expand_neighborhood] called", flush=True)
        print(f"[GraphQuery._expand_neighborhood] seed_count={len(seeds)}", flush=True)
        print(f"[GraphQuery._expand_neighborhood] hops={hops}", flush=True)

        seen_nodes = {node.id: node for node in seeds}
        seen_edges: dict[str, Edge] = {}
        frontier = list(seen_nodes)

        print(f"[GraphQuery._expand_neighborhood] initial frontier={frontier}", flush=True)

        for hop_index in range(hops):
            print(f"[GraphQuery._expand_neighborhood] hop={hop_index + 1}", flush=True)

            next_frontier: list[str] = []

            for node_id in frontier:
                print(f"[GraphQuery._expand_neighborhood] expanding node_id={node_id!r}", flush=True)

                edges = self.database.get_edges_for_node(node_id)
                print(
                    f"[GraphQuery._expand_neighborhood] edge_count={len(edges)}",
                    flush=True,
                )

                for edge in edges:
                    seen_edges[edge.id] = edge

                    other_id = (
                        edge.target_node_id
                        if edge.source_node_id == node_id
                        else edge.source_node_id
                    )

                    print(
                        f"[GraphQuery._expand_neighborhood] edge id={edge.id!r} "
                        f"label={edge.label!r} other_id={other_id!r}",
                        flush=True,
                    )

                    if other_id in seen_nodes:
                        print(
                            f"[GraphQuery._expand_neighborhood] already seen other_id={other_id!r}",
                            flush=True,
                        )
                        continue

                    other = self.database.get_node(other_id)

                    if other and other.status == NodeStatus.active:
                        seen_nodes[other_id] = other
                        next_frontier.append(other_id)

                        print(
                            f"[GraphQuery._expand_neighborhood] added node id={other.id!r} "
                            f"title={other.title!r}",
                            flush=True,
                        )
                    else:
                        print(
                            f"[GraphQuery._expand_neighborhood] skipped missing/inactive other_id={other_id!r}",
                            flush=True,
                        )

            frontier = next_frontier
            print(
                f"[GraphQuery._expand_neighborhood] next_frontier={next_frontier}",
                flush=True,
            )

        print(
            f"[GraphQuery._expand_neighborhood] returning nodes={len(seen_nodes)} edges={len(seen_edges)}",
            flush=True,
        )

        return list(seen_nodes.values()), list(seen_edges.values())

    def _edges_for_nodes(self, nodes: list[Node]) -> list[Edge]:
        print("\n[GraphQuery._edges_for_nodes] called", flush=True)
        print(f"[GraphQuery._edges_for_nodes] node_count={len(nodes)}", flush=True)

        seen: dict[str, Edge] = {}

        for node in nodes:
            print(f"[GraphQuery._edges_for_nodes] loading edges for node_id={node.id!r}", flush=True)

            edges = self.database.get_edges_for_node(node.id)
            print(f"[GraphQuery._edges_for_nodes] edge_count={len(edges)}", flush=True)

            for edge in edges:
                seen[edge.id] = edge
                print(
                    f"[GraphQuery._edges_for_nodes] edge id={edge.id!r} label={edge.label!r}",
                    flush=True,
                )

        print(f"[GraphQuery._edges_for_nodes] returning edges={len(seen)}", flush=True)

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
        namer: Callable[..., str | None] | None = None,
    ) -> dict[str, str]:
        """Detect communities (Louvain) and label each.

        ``namer(top_keywords, sample_titles, used_names) -> name`` is an optional
        caller-supplied labeller (e.g. an LLM in the engine layer). It keeps this
        module LLM-free: the callback receives plain strings and returns a name,
        or ``None``/empty to fall back to the deterministic TF-IDF keyword label.
        """
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
        ordered = sorted(communities, key=len, reverse=True)

        # Per-community keyword counts + global document-frequency (how many
        # communities each keyword appears in), so labels are built from the
        # keywords that DISTINGUISH a community rather than the one shared by all
        # (which produced useless "Cuda / Cuda 2 / Cuda 3" names).
        per_comm: list[Counter[str]] = []
        titles: list[list[str]] = []
        doc_freq: Counter[str] = Counter()
        for members in ordered:
            counts: Counter[str] = Counter()
            comm_titles: list[str] = []
            for node_id in members:
                node = node_by_id.get(node_id)
                if node:
                    counts.update(kw.lower().strip() for kw in node.keywords if kw.strip())
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
            keywords = self._tfidf_keywords(per_comm[index], doc_freq, n_comms, k=8)
            sample_titles = titles[index][:12]
            label = ""
            if namer:
                try:
                    label = (namer(keywords, sample_titles, used_labels) or "").strip()
                except TypeError:
                    try:
                        label = (namer(keywords, sample_titles) or "").strip()
                    except Exception:  # noqa: BLE001 - LLM naming is best-effort
                        label = ""
                except Exception:  # noqa: BLE001 - LLM naming is best-effort
                    label = ""
            if not label:
                label = self._community_label(keywords, index)
            used[label] += 1
            if used[label] > 1:
                label = f"{label} {used[label]}"
            used_labels.append(label)
            for node_id in members:
                mapping[node_id] = label
        if persist:
            for node in nodes:
                new_label = mapping.get(node.id)
                if new_label and node.cluster != new_label:
                    node.cluster = new_label
                    self.database.upsert_node(node)
        return mapping

    def _tfidf_keywords(
        self,
        counts: Counter[str],
        doc_freq: Counter[str],
        n_comms: int,
        k: int = 5,
    ) -> list[str]:
        """Top-k keywords that DISTINGUISH this community.

        Weight = count * log(1 + n_comms / docfreq); keywords present in every
        community (docfreq == n_comms) contribute ~0, so shared terms drop out.
        """
        import math

        if not counts:
            return []
        scored = sorted(
            counts.items(),
            key=lambda kv: kv[1] * math.log(1 + n_comms / max(doc_freq[kv[0]], 1)),
            reverse=True,
        )
        return [kw for kw, _ in scored[:k]]

    def _community_label(self, keywords: list[str], index: int) -> str:
        """Deterministic fallback label from the distinctive keywords."""
        if not keywords:
            return f"Cluster {index + 1}"
        return " · ".join(kw.title() for kw in keywords[:3])

    # endregion CLUSTERING

    # region FUTURE COMPATIBILITY
    # maintain/lint logic can be added here later or split later.
    # endregion FUTURE COMPATIBILITY
