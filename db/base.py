"""Shared database interface for graph storage backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from graph_big.models import Edge, Node, NodeStatus


class BaseDatabase(ABC):
    """Common API used by the graph engine."""

    path: Path

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def ensure_vec_tables(self, dim: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def upsert_node(self, node: Node) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_node(self, node_id: str) -> Node | None:
        raise NotImplementedError

    @abstractmethod
    def set_node_status(self, node_id: str, status: NodeStatus) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_node(self, node_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_nodes(self, include_deleted: bool = False) -> list[Node]:
        raise NotImplementedError

    @abstractmethod
    def get_nodes_by_document(
        self, document_name: str, active_only: bool = False
    ) -> list[Node]:
        raise NotImplementedError

    @abstractmethod
    def upsert_edge(self, edge: Edge) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_edges(self) -> list[Edge]:
        raise NotImplementedError

    @abstractmethod
    def get_edges_for_node(self, node_id: str) -> list[Edge]:
        raise NotImplementedError

    @abstractmethod
    def get_outgoing_edges(self, node_id: str, label: str | None = None) -> list[Edge]:
        raise NotImplementedError

    @abstractmethod
    def get_incoming_edges(self, node_id: str, label: str | None = None) -> list[Edge]:
        raise NotImplementedError

    @abstractmethod
    def delete_edges_by_label_for_nodes(self, label: str, node_ids: set[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def record_source(self, document_name: str, source_hash: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_source(self, document_name: str) -> tuple[str, str] | None:
        raise NotImplementedError

    @abstractmethod
    def keyword_search(self, text: str, limit: int = 20) -> list[Node]:
        raise NotImplementedError

    def reset_vec_tables(self) -> None:
        """Drop vector tables + forget stored dim (used on embed-model change)."""
        raise NotImplementedError

    def get_meta(self, key: str) -> str | None:
        raise NotImplementedError

    def set_meta(self, key: str, value: str) -> None:
        raise NotImplementedError

    def count_vectors(self, table: str = "vec_body") -> int:
        """Number of stored vectors (used to detect incomplete coverage)."""
        raise NotImplementedError

    @abstractmethod
    def set_vector(self, node_id: str, table: str, vector: list[float]) -> None:
        raise NotImplementedError

    @abstractmethod
    def vector_search(
        self, vector: list[float], table: str = "vec_body", limit: int = 20
    ) -> list[tuple[str, float]]:
        raise NotImplementedError
