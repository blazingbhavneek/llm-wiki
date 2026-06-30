"""Revision matching and cascade updates for the graph package."""

from __future__ import annotations

import re
from collections import deque
from pathlib import Path

from .db import Database
from .md_ingest import MarkdownIngest
from .models import Edge, Node, NodeStatus, NodeType, Settings
from .runtime import GraphExogenous, GraphQuery, GraphRuntime
from .utils import (
    claim_keys,
    jaccard,
    make_edge_id,
    make_exogenous_node_id,
    make_node_id,
    normalize_text,
    normalize_token,
    source_hash,
    token_jaccard,
)

# region CONSTANTS
_TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")
_CASCADE_MATCH_THRESHOLD = 0.45
_UNCHANGED_CLAIM_THRESHOLD = 0.9
# endregion CONSTANTS


class GraphRevisions:
    # region LIFECYCLE
    def __init__(
        self,
        database: Database,
        settings: Settings,
        runtime: GraphRuntime,
        query: GraphQuery,
        exogenous: GraphExogenous,
        ingest: MarkdownIngest,
    ) -> None:
        self.database = database
        self.settings = settings
        self.runtime = runtime
        self.query = query
        self.exogenous = exogenous
        self.ingest = ingest

    # endregion LIFECYCLE

    # region PUBLIC API
    def recon(self, source_file: str | Path) -> dict[str, str]:
        path = Path(source_file)
        text = path.read_text(encoding="utf-8", errors="ignore")
        current = source_hash(text)
        known = self.database.get_source(path.name)

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
            self.runtime.fill_derived_fields(old)
            self.database.upsert_node(old)
            return old

        self._persist_node(replacement)
        self._supersede(old, replacement)
        return replacement

    def cascading_update(self, source_file: str | Path) -> list[str]:
        nodes, structural_edges = self.ingest.load_md_output(source_file)
        if not nodes:
            return []

        document_name = nodes[0].original_document_name or Path(source_file).name
        version = self._source_version_for_nodes(nodes)
        incoming: list[Node] = []

        # Cheap pass: stamp version + body hash only. NO LLM enrichment yet —
        # unchanged chunks must not pay for summarize/keywords/claims.
        for node in nodes:
            node.source_version = version
            if not node.source_material_hash:
                node.source_material_hash = source_hash(node.body)
            incoming.append(node)

        active_old = [
            node
            for node in self.database.get_nodes_by_document(
                document_name, active_only=True
            )
            if node.type == NodeType.endogenous
        ]
        if not active_old:
            for node in incoming:
                self._persist_node(node)
            self._replace_structural_edges(document_name, structural_edges)
            self.database.record_source(document_name, version)
            return [f"ingested-new:{node.id}" for node in incoming]

        actions: list[str] = []
        replacements: dict[str, str] = {}
        stale_sources: set[str] = set()
        matched_old: set[str] = set()
        exact_by_hash: dict[str, Node] = {}
        for old in active_old:
            exact_by_hash.setdefault(
                old.source_material_hash or source_hash(old.body), old
            )
        pending: list[Node] = []

        # PASS 1 — exact body-hash match (no enrichment on either side).
        for node in incoming:
            exact = exact_by_hash.get(node.source_material_hash)
            if exact and exact.id not in matched_old:
                matched_old.add(exact.id)
                actions.append(f"unchanged:{exact.id}")
            else:
                pending.append(node)

        # Only changed/new chunks get enriched + matched fuzzily.
        for node in pending:
            self.runtime.fill_derived_fields(node)
        unmatched_old = [
            self._ensure_revision_metadata(old)
            for old in active_old
            if old.id not in matched_old
        ]

        for node in pending:
            best = self._best_revision_match(
                node,
                [old for old in unmatched_old if old.id not in matched_old],
            )
            if best is None:
                self._persist_node(node)
                actions.append(f"new:{node.id}")
                continue

            old, score = best
            if score < _CASCADE_MATCH_THRESHOLD:
                self._persist_node(node)
                actions.append(f"new:{node.id}")
                continue

            matched_old.add(old.id)
            if self._claims_equivalent(old, node):
                actions.append(f"remapped:{old.id}")
                continue

            self._persist_node(node)
            self._supersede(old, node)
            replacements[old.id] = node.id
            actions.append(f"superseded:{old.id}->{node.id}")

        for old in active_old:
            if old.id in matched_old:
                continue
            self._mark_stale(old.id)
            stale_sources.add(old.id)
            actions.append(f"stale:{old.id}")

        self._cascade_dependents(replacements, stale_sources, actions)
        self._replace_structural_edges(document_name, structural_edges)
        self.database.record_source(document_name, version)
        return actions

    # endregion PUBLIC API

    # region VERSIONING
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

    def _ensure_revision_metadata(self, node: Node) -> Node:
        changed = False

        if not node.source_material_hash:
            node.source_material_hash = source_hash(node.body)
            changed = True
        if not node.claims:
            extracted = self.runtime.extract_claims(node.body)
            node.entity = node.entity or extracted.entity
            node.claims = extracted.claims
            changed = True
        if not node.entity and node.keywords:
            node.entity = node.keywords[0]
            changed = True

        if changed:
            self.database.upsert_node(node)
        return node

    # endregion VERSIONING

    # region MATCHING
    def _best_revision_match(
        self,
        node: Node,
        candidates: list[Node],
    ) -> tuple[Node, float] | None:
        if not candidates:
            return None

        scored = [
            (candidate, self._revision_match_score(candidate, node))
            for candidate in candidates
        ]
        return max(scored, key=lambda item: item[1])

    def _claims_equivalent(self, old: Node, new: Node) -> bool:
        old_claims = claim_keys(old, _TOKEN_RE)
        new_claims = claim_keys(new, _TOKEN_RE)

        if old_claims and new_claims:
            return jaccard(old_claims, new_claims) >= _UNCHANGED_CLAIM_THRESHOLD
        return token_jaccard(old.body, new.body, _TOKEN_RE) >= 0.95

    def _revision_match_score(self, old: Node, new: Node) -> float:
        claim_score = jaccard(claim_keys(old, _TOKEN_RE), claim_keys(new, _TOKEN_RE))
        keyword_score = jaccard(
            {normalize_token(keyword) for keyword in old.keywords},
            {normalize_token(keyword) for keyword in new.keywords},
        )
        body_score = token_jaccard(old.body, new.body, _TOKEN_RE)
        entity_bonus = 0.0

        if old.entity and new.entity:
            entity_bonus = (
                0.2
                if normalize_text(old.entity, _TOKEN_RE)
                == normalize_text(new.entity, _TOKEN_RE)
                else 0.0
            )

        return min(
            1.0,
            max(claim_score, keyword_score * 0.8, body_score * 0.65) + entity_bonus,
        )

    # endregion MATCHING

    # region MUTATION
    def _persist_node(self, node: Node) -> Node:
        self.runtime.fill_derived_fields(node)
        self.database.upsert_node(node)
        body_vec, summary_vec = self.runtime.store_vectors(node)
        self.runtime.build_semantic_edges(
            node,
            body_vec,
            summary_vec,
            self.settings.edge_candidate_k,
        )
        return node

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

    def _replace_structural_edges(
        self,
        document_name: str | None,
        edges: list[Edge],
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
                source
                and target
                and source.status == NodeStatus.active
                and target.status == NodeStatus.active
            ):
                self.database.upsert_edge(edge)

    def _mark_stale(self, node_id: str) -> None:
        self.database.set_node_status(node_id, NodeStatus.stale)

    # endregion MUTATION

    # region CASCADE
    def _cascade_dependents(
        self,
        replacements: dict[str, str],
        stale_sources: set[str],
        actions: list[str],
    ) -> None:
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
                    self._mark_stale(target.id)
                    actions.append(f"stale-exogenous:{target.id}")
                    if target_depth < max_hops:
                        frontier.append((target.id, target_depth))
                    continue

                replacement = self._regenerate_exogenous_node(target, support_nodes)
                if replacement is None:
                    self._mark_stale(target.id)
                    actions.append(f"stale-exogenous:{target.id}")
                    if target_depth < max_hops:
                        frontier.append((target.id, target_depth))
                    continue

                replacements[target.id] = replacement.id
                actions.append(f"regenerated-exogenous:{target.id}->{replacement.id}")
                if target_depth < max_hops:
                    frontier.append((target.id, target_depth))

    def _current_support_nodes(
        self,
        node: Node,
        replacements: dict[str, str],
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

        return self.runtime.collapse_same_as(list(support_nodes.values()))

    def _active_replacement_id(self, node_id: str) -> str | None:
        for edge in self.database.get_outgoing_edges(node_id, "superseded_by"):
            target = self.database.get_node(edge.target_node_id)
            if target and target.status == NodeStatus.active:
                return target.id
        return None

    def _regenerate_exogenous_node(
        self,
        old: Node,
        support_nodes: list[Node],
    ) -> Node | None:
        body = self.runtime.regenerate_exogenous_text(old, support_nodes).strip()
        if not body:
            return None

        support_ids = sorted(node.id for node in support_nodes)
        version = source_hash(
            "|".join(
                [
                    source_hash(body),
                    *support_ids,
                    *(node.source_version or "" for node in support_nodes),
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

        self._persist_node(replacement)
        self.exogenous._link_support_edges(
            replacement,
            [node.id for node in support_nodes],
        )
        self._supersede(old, replacement)
        return replacement

    # endregion CASCADE

    # region FUTURE COMPATIBILITY
    # stronger rewrite matching goes here later.
    # temporal/conflict edge logic goes here later.
    # endregion FUTURE COMPATIBILITY
