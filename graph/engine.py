"""Facade API for the graph package."""

from __future__ import annotations

from pathlib import Path

from db import Database
from embeddings import Embedder
from llm.llm import LlmClient

from .md_ingest import MarkdownIngest
from .models import Edge, GraphStats, Node, QueryResult, Settings
from .revisions import GraphRevisions
from .runtime import (
    GRAPH_SYSTEM_PROMPT,
    GraphAnalytics,
    GraphExogenous,
    GraphQuery,
    GraphRuntime,
)


class DomainEngine:
    # region LIFECYCLE
    def __init__(
        self,
        settings: Settings | None = None,
        embedder: object | None = None,
        llm_client: object | None = None,
    ) -> None:
        self.settings = settings or Settings.from_env()
        self.database = Database(self.settings.database_path)
        self.embedder = embedder or Embedder(self.settings)
        self.llm = llm_client or LlmClient(
            model=self.settings.chat_model,
            base_url=self.settings.chat_base_url,
            api_key=self.settings.chat_api_key,
            system_prompt=GRAPH_SYSTEM_PROMPT,
            temperature=self.settings.chat_temperature,
        )

        self.ingest_parser = MarkdownIngest()
        self.runtime = GraphRuntime(
            self.database,
            self.embedder,
            self.llm,
            self.settings,
        )
        self.query_api = GraphQuery(
            self.database,
            self.embedder,
            self.settings,
            self.runtime,
        )
        self.exogenous = GraphExogenous(
            self.database,
            self.runtime,
            self.settings,
        )
        self.analytics = GraphAnalytics(self.database)
        self.revisions = GraphRevisions(
            self.database,
            self.settings,
            self.runtime,
            self.query_api,
            self.exogenous,
            self.ingest_parser,
        )

    def close(self) -> None:
        self.database.close()

    # endregion LIFECYCLE

    # region INGEST API
    def md_to_nodes(self, md_output_dir: str | Path) -> tuple[list[Node], list[Edge]]:
        return self.ingest_parser.load_md_output(md_output_dir)

    def ingest(self, node: Node) -> list[Edge]:
        self.runtime.fill_derived_fields(node)
        self.database.upsert_node(node)
        body_vec, summary_vec = self.runtime.store_vectors(node)
        return self.runtime.build_semantic_edges(
            node,
            body_vec,
            summary_vec,
            self.settings.edge_candidate_k,
        )

    def ingest_md_output(self, md_output_dir: str | Path) -> list[Node]:
        nodes, structural_edges = self.md_to_nodes(md_output_dir)
        version = self.revisions._source_version_for_nodes(nodes)

        for node in nodes:
            node.source_version = version
            self.ingest(node)

        if nodes:
            self.revisions._replace_structural_edges(
                nodes[0].original_document_name,
                structural_edges,
            )
        if nodes and nodes[0].original_document_name:
            self.database.record_source(nodes[0].original_document_name, version)

        return nodes

    # endregion INGEST API

    # region QUERY API
    def query(self, query_type: str, value: str) -> QueryResult:
        return self.query_api.query(query_type, value)

    # endregion QUERY API

    # region TOOL COMPATIBILITY API
    def search(self, text: str, limit: int | None = None) -> list[Node]:
        return self.query_api.search(text, limit)

    def read(self, node_id: str) -> Node | None:
        return self.query_api.read(node_id)

    def follow_link(
        self,
        node_id: str,
        label: str | None = None,
        direction: str = "both",
        limit: int | None = None,
    ) -> list[tuple[Edge, Node]]:
        return self.query_api.follow_link(node_id, label, direction, limit)

    # endregion TOOL COMPATIBILITY API

    # region GRAPH API
    def get(self) -> tuple[list[Node], list[Edge]]:
        return self.database.get_all_nodes(), self.database.get_all_edges()

    def health(self, node_id: str | None = None) -> GraphStats:
        return self.analytics.health(node_id)

    def recluster(self, resolution: float = 1.0) -> dict[str, str]:
        return self.analytics.recluster(resolution=resolution)

    # endregion GRAPH API

    # region SOURCE UPDATE API
    def recon(self, source_file: str | Path) -> dict[str, str]:
        return self.revisions.recon(source_file)

    def update(self, node_id: str, body: str) -> Node:
        return self.revisions.update_node(node_id, body)

    def delete(self, node_id: str) -> None:
        self.database.delete_node(node_id)

    def cascading_update(self, source_file: str | Path) -> list[str]:
        return self.revisions.cascading_update(source_file)

    # endregion SOURCE UPDATE API

    # region EXOGENOUS API
    def create_exogenous_node(
        self,
        body: str,
        source_node_ids: list[str],
        origin: str | None = None,
    ) -> Node:
        return self.exogenous.create_exogenous_node(body, source_node_ids, origin)

    # endregion EXOGENOUS API

    # region FUTURE COMPATIBILITY
    # agent-driven query will plug in here later.
    # maintain/stale-refresh can be exposed here later.
    # endregion FUTURE COMPATIBILITY
