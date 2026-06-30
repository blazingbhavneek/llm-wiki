"""Facade API for the graph package."""

from __future__ import annotations

from pathlib import Path

from db import Database
from embeddings import Embedder, Reranker
from llm.agent import AgentClient

from .agent import QueryAgent
from .md_ingest import MarkdownIngest
from .models import AgentAnswer, Edge, GraphStats, Node, QueryResult, Settings
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
        reranker: object | None = None,
    ) -> None:
        self.settings = settings or Settings.from_env()
        self.database = Database(self.settings.database_path)
        self.embedder = embedder or Embedder(self.settings)
        self.reranker = reranker if reranker is not None else self._build_reranker()
        self.llm = llm_client or AgentClient(
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
            reranker=self.reranker,
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
        self.agent = QueryAgent(
            self.query_api,
            self.exogenous,
            self.llm,
            self.settings,
        )

        # Eagerly reconcile stored vectors with the current embedding model at
        # startup (server start), so a model change or a half-finished re-embed
        # is fully rebuilt here — never lazily mid-query.
        self.runtime.prepare_embeddings()

    def _build_reranker(self) -> object | None:
        """Build the reranker, degrading to no-rerank if unavailable.

        Retrieval still works without it (search falls back to fused order), so a
        missing rerank server + missing local model must not abort the engine.
        """
        try:
            return Reranker(self.settings)
        except Exception as exc:  # noqa: BLE001 - rerank is an optional enhancement
            print(f"[engine] reranker unavailable, continuing without it: {exc}", flush=True)
            return None

    def close(self) -> None:
        self.database.close()

    # endregion LIFECYCLE

    # region INGEST API
    def md_to_nodes(self, md_output_dir: str | Path) -> tuple[list[Node], list[Edge]]:
        return self.ingest_parser.load_md_output(md_output_dir)

    def ingest(self, node: Node) -> list[Edge]:
        # node.id = hash(body, document) → an existing complete node is the exact
        # same chunk in the same doc (same context): skip enrich+embed+edges.
        if self.runtime.node_is_complete(node.id):
            return []
        self.runtime.fill_derived_fields(node)
        self.database.upsert_node(node)
        body_vec, summary_vec = self.runtime.store_vectors(node)
        edges = self.runtime.build_semantic_edges(
            node,
            body_vec,
            summary_vec,
            self.settings.edge_candidate_k,
        )
        if self.settings.entity_dedup:
            candidates = self.runtime.knn_candidates(
                node.id,
                body_vec,
                summary_vec,
                self.settings.edge_candidate_k,
            )
            edges += self.runtime.link_entity_duplicates(node, candidates)
        return edges

    def ingest_md_output(self, md_output_dir: str | Path) -> list[Node]:
        nodes, structural_edges = self.md_to_nodes(md_output_dir)
        version = self.revisions._source_version_for_nodes(nodes)

        total = len(nodes)
        edge_count = 0
        for index, node in enumerate(nodes, start=1):
            node.source_version = version
            edges = self.ingest(node)
            edge_count += len(edges)
            print(
                f"[ingest] {index}/{total} nodes | semantic+dedup edges so far: "
                f"{edge_count} | {node.id}",
                flush=True,
            )

        if nodes:
            self.revisions._replace_structural_edges(
                nodes[0].original_document_name,
                structural_edges,
            )
        if nodes and nodes[0].original_document_name:
            self.database.record_source(nodes[0].original_document_name, version)

        print(
            f"[ingest] done: {total} node(s), {edge_count} semantic/dedup edge(s), "
            f"{len(structural_edges)} structural edge(s)",
            flush=True,
        )
        # Assign topic clusters at ingest time (Louvain over the current graph), so
        # node.cluster holds real communities, not raw heading titles. Best-effort:
        # never let clustering failure abort an ingest.
        self._safe_recluster()
        return nodes

    def _safe_recluster(self) -> None:
        try:
            labels = self.recluster()
            print(f"[ingest] reclustered into {len(set(labels.values()))} topic(s)", flush=True)
        except Exception as exc:  # noqa: BLE001 - clustering is non-critical
            print(f"[ingest] recluster skipped: {exc}", flush=True)

    # endregion INGEST API

    # region QUERY API
    def query(self, query_type: str, value: str) -> QueryResult:
        return self.query_api.query(query_type, value)

    # endregion QUERY API

    # region AGENT API
    def ask(self, question: str, persist: bool = True, on_event=None) -> AgentAnswer:
        return self.agent.ask(question, persist, on_event=on_event)

    # endregion AGENT API

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
        return self.analytics.recluster(resolution=resolution, namer=self._llm_cluster_namer)

    def _llm_cluster_namer(
        self,
        keywords: list[str],
        titles: list[str],
        used_names: list[str] | None = None,
    ) -> str | None:
        """Name one community from its distinctive keywords + sample titles.

        Best-effort: returns ``None`` on any failure / unusable output so the
        caller falls back to the deterministic keyword label.
        """
        if not keywords and not titles:
            return None
        avoided = used_names or []
        system = (
            "あなたはナレッジグラフ内の 1 つのトピッククラスタに名前を付けます。"
            "すでに使用されている他の名前と区別できる、具体的な名前を選んでください。"
            "キーワードとサンプルセクションタイトルに現れている、最も具体的な技術的サブトピックを優先してください。"
            "より狭いトピックが存在する場合は、CUDA、SYCL、OpenMP、oneAPI のような広範なソース名は避けてください。"
            "回答は、簡潔なトピック名 1 つだけにしてください。"
            "最大 4 語以内にしてください。"
            "引用符、句読点、説明は不要です。"
            "トピック名は日本語で記述してください。"
        )
        user = (
            f"キーワード: {', '.join(keywords) or '(なし)'}\n"
            f"サンプルタイトル: {'; '.join(titles) or '(なし)'}\n"
            f"避けるべき使用済みの名前: {', '.join(avoided) or '(なし)'}\n\n"
            "トピック名:"
        )
        try:
            raw = self.llm.complete(system, user)
        except Exception:  # noqa: BLE001 - naming is non-critical
            return None
        name = " ".join(raw.strip().strip('"\'').split())
        if not name or len(name) > 60 or len(name.split()) > 6:
            return None
        if name.lower() in {used.lower() for used in avoided}:
            return None
        return name.title()

    # endregion GRAPH API

    # region SOURCE UPDATE API
    def recon(self, source_file: str | Path) -> dict[str, str]:
        return self.revisions.recon(source_file)

    def update(self, node_id: str, body: str) -> Node:
        return self.revisions.update_node(node_id, body)

    def delete(self, node_id: str) -> None:
        self.database.delete_node(node_id)

    def cascading_update(self, source_file: str | Path) -> list[str]:
        actions = self.revisions.cascading_update(source_file)
        # refresh clusters after the graph changed shape
        self._safe_recluster()
        return actions

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
