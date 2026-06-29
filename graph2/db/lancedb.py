"""LanceDB vector backend layered on top of the SQLModel graph store.

Graph state still lives in SQLite/SQLModel. LanceDB replaces the vector index
so you can compare maintenance and search ergonomics without rewriting the graph.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from graph2.models import NodeStatus

from .sqlmodel import SQLModelDatabase

try:
    import lancedb
except ImportError as exc:  # pragma: no cover - handled at runtime
    lancedb = None
    _LANCEDB_IMPORT_ERROR = exc
else:
    _LANCEDB_IMPORT_ERROR = None


class LanceDatabase(SQLModelDatabase):
    def __init__(
        self,
        path: str | Path = ".wiki/wiki.sqlite",
        lance_path: str | Path | None = None,
    ) -> None:
        default_path = Path(path).with_suffix(".lancedb")
        self.lance_path = Path(lance_path) if lance_path is not None else default_path
        self._lance: Any | None = None
        self._vector_tables: dict[str, Any] = {}
        super().__init__(path)

    def _setup_search_storage(self) -> None:
        self._create_fts_table()
        self._connect_lancedb()

    def _connect_lancedb(self) -> None:
        if lancedb is None:
            raise RuntimeError(
                "lancedb is not installed. Install `lancedb` to use LanceDatabase."
            ) from _LANCEDB_IMPORT_ERROR

        self.lance_path.parent.mkdir(parents=True, exist_ok=True)
        self._lance = lancedb.connect(str(self.lance_path))

    def ensure_vec_tables(self, dim: int) -> None:
        if self._dim is not None:
            if self._dim != dim:
                raise ValueError(
                    f"embedding dim mismatch: db built for {self._dim}, got {dim}"
                )
            return
        self._set_meta("embed_dim", str(dim))
        self._dim = dim

    def set_vector(self, node_id: str, table: str, vector: list[float]) -> None:
        if self._dim is None:
            raise RuntimeError("ensure_vec_tables() must run before set_vector()")

        row = {"node_id": node_id, "embedding": list(vector)}
        table_ref = self._open_vector_table(table)
        if table_ref is None:
            self._vector_tables[table] = self._lance.create_table(table, data=[row])
            return

        self._delete_lance_row(table_ref, node_id)
        table_ref.add([row])

    def vector_search(
        self, vector: list[float], table: str = "vec_body", limit: int = 20
    ) -> list[tuple[str, float]]:
        if self._dim is None:
            return []

        table_ref = self._open_vector_table(table)
        if table_ref is None:
            return []

        results = table_ref.search(vector).limit(limit).to_list()
        hits: list[tuple[str, float]] = []
        for result in results:
            node_id = result.get("node_id")
            if not node_id:
                continue
            node = self.get_node(node_id)
            if node is None or node.status != NodeStatus.active:
                continue

            if "_distance" in result:
                distance = float(result["_distance"])
            elif "distance" in result:
                distance = float(result["distance"])
            else:
                distance = 0.0
            hits.append((node_id, distance))
        return hits

    def _delete_search_records(self, node_id: str) -> None:
        self._delete_fts_record(node_id)
        for table_name in ("vec_body", "vec_summary"):
            table_ref = self._open_vector_table(table_name)
            if table_ref is not None:
                self._delete_lance_row(table_ref, node_id)

    def _open_vector_table(self, table_name: str) -> Any | None:
        if table_name in self._vector_tables:
            return self._vector_tables[table_name]
        if self._lance is None:
            return None

        try:
            names = set(self._lance.table_names())
        except Exception:
            return None

        if table_name not in names:
            return None

        table_ref = self._lance.open_table(table_name)
        self._vector_tables[table_name] = table_ref
        return table_ref

    def _delete_lance_row(self, table_ref: Any, node_id: str) -> None:
        safe_node_id = node_id.replace("'", "''")
        table_ref.delete(f"node_id = '{safe_node_id}'")


Database = LanceDatabase
