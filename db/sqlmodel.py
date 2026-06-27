"""SQLModel-backed graph database.

Normal tables use SQLModel for readability. FTS5 and sqlite-vec stay raw SQLite
because those are SQLite-specific features.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from graph.models import Edge, Node, NodeStatus, now_iso

from .base import BaseDatabase

try:
    from sqlmodel import Field, Session, SQLModel, create_engine, select
except ImportError as exc:  # pragma: no cover - handled at runtime
    Field = None
    Session = None
    SQLModel = None
    create_engine = None
    select = None
    _SQLMODEL_IMPORT_ERROR = exc
else:
    _SQLMODEL_IMPORT_ERROR = None

_FTS_SPECIAL = re.compile(r'["()*:^]')


def _fts_query(text: str) -> str:
    terms = [t for t in _FTS_SPECIAL.sub(" ", text).split() if t]
    return " OR ".join(f'"{t}"' for t in terms)


if SQLModel is not None:

    class MetaRow(SQLModel, table=True):
        __tablename__ = "meta"

        key: str = Field(primary_key=True)
        value: str


    class NodeRow(SQLModel, table=True):
        __tablename__ = "nodes"

        id: str = Field(primary_key=True)
        body: str
        type: str = Field(index=True)
        title: str = ""
        original_document_name: str | None = Field(default=None, index=True)
        source_path: str | None = None
        source_ranges_json: str = "[]"
        source_version: str | None = Field(default=None, index=True)
        source_material_hash: str | None = Field(default=None, index=True)
        entity: str = Field(default="", index=True)
        claims_json: str = "[]"
        keywords_json: str = "[]"
        summary: str = ""
        cluster: str | None = None
        status: str = Field(default=NodeStatus.active.value, index=True)
        created_at: str
        updated_at: str


    class EdgeRow(SQLModel, table=True):
        __tablename__ = "edges"

        id: str = Field(primary_key=True)
        source_node_id: str = Field(index=True)
        target_node_id: str = Field(index=True)
        label: str
        summary: str = ""
        created_at: str


    class SourceRow(SQLModel, table=True):
        __tablename__ = "sources"

        document_name: str = Field(primary_key=True)
        source_hash: str
        ingested_at: str


    class SourceVersionRow(SQLModel, table=True):
        __tablename__ = "source_versions"

        document_name: str = Field(primary_key=True)
        source_hash: str = Field(primary_key=True)
        ingested_at: str


class SQLModelDatabase(BaseDatabase):
    def __init__(self, path: str | Path = ".wiki/wiki.sqlite") -> None:
        if SQLModel is None or create_engine is None:
            raise RuntimeError(
                "sqlmodel is not installed. Install `sqlmodel` to use SQLModelDatabase."
            ) from _SQLMODEL_IMPORT_ERROR

        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path))
        self.connection.row_factory = sqlite3.Row
        self.engine = create_engine(
            f"sqlite:///{self.path}",
            connect_args={"check_same_thread": False},
        )
        self._dim: int | None = None
        self._create_core_tables()
        self._setup_search_storage()
        self._restore_dim()

    def _create_core_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)
        self._ensure_node_columns()
        self.connection.commit()

    def _ensure_node_columns(self) -> None:
        existing = {
            row["name"]
            for row in self.connection.execute("PRAGMA table_info(nodes)").fetchall()
        }
        additions = {
            "source_version": "TEXT",
            "source_material_hash": "TEXT",
            "entity": "TEXT",
            "claims_json": "TEXT NOT NULL DEFAULT '[]'",
        }
        for column, ddl in additions.items():
            if column not in existing:
                self.connection.execute(f"ALTER TABLE nodes ADD COLUMN {column} {ddl}")
        self.connection.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_nodes_source_version ON nodes(source_version);
            CREATE INDEX IF NOT EXISTS idx_nodes_source_material_hash ON nodes(source_material_hash);
            CREATE INDEX IF NOT EXISTS idx_nodes_entity ON nodes(entity);
            """
        )

    def _setup_search_storage(self) -> None:
        self._create_fts_table()
        self._load_vec_extension()

    def _create_fts_table(self) -> None:
        self.connection.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS nodes_fts USING fts5(
                node_id UNINDEXED, text
            )
            """
        )
        self.connection.commit()

    def _load_vec_extension(self) -> None:
        import sqlite_vec

        self.connection.enable_load_extension(True)
        sqlite_vec.load(self.connection)
        self.connection.enable_load_extension(False)

    def _restore_dim(self) -> None:
        row = self.connection.execute(
            "SELECT value FROM meta WHERE key = 'embed_dim'"
        ).fetchone()
        if row:
            self._dim = int(row["value"])

    def ensure_vec_tables(self, dim: int) -> None:
        if self._dim is not None:
            if self._dim != dim:
                raise ValueError(
                    f"embedding dim mismatch: db built for {self._dim}, got {dim}"
                )
            return
        self.connection.execute(
            f"CREATE VIRTUAL TABLE IF NOT EXISTS vec_body "
            f"USING vec0(node_id TEXT PRIMARY KEY, embedding float[{dim}])"
        )
        self.connection.execute(
            f"CREATE VIRTUAL TABLE IF NOT EXISTS vec_summary "
            f"USING vec0(node_id TEXT PRIMARY KEY, embedding float[{dim}])"
        )
        self._set_meta("embed_dim", str(dim))
        self.connection.commit()
        self._dim = dim

    def close(self) -> None:
        self.connection.close()
        self.engine.dispose()

    def upsert_node(self, node: Node) -> None:
        with Session(self.engine) as session:
            row = session.get(NodeRow, node.id)
            if row is None:
                row = NodeRow(
                    id=node.id,
                    body=node.body,
                    type=node.type.value,
                    title=node.title,
                    original_document_name=node.original_document_name,
                    source_path=node.source_path,
                    source_ranges_json="[]",
                    source_version=node.source_version,
                    source_material_hash=node.source_material_hash,
                    entity=node.entity,
                    claims_json="[]",
                    keywords_json="[]",
                    summary=node.summary,
                    cluster=node.cluster,
                    status=node.status.value,
                    created_at=node.created_at,
                    updated_at=node.updated_at,
                )
                session.add(row)
            else:
                node.created_at = row.created_at

            node.updated_at = now_iso()
            self._apply_node(row, node)
            session.add(row)
            session.commit()

        self._reindex_fts(node)
        self.connection.commit()

    def get_node(self, node_id: str) -> Node | None:
        with Session(self.engine) as session:
            row = session.get(NodeRow, node_id)
            return _node_from_record(row) if row else None

    def set_node_status(self, node_id: str, status: NodeStatus) -> None:
        with Session(self.engine) as session:
            row = session.get(NodeRow, node_id)
            if row is None:
                return
            row.status = status.value
            row.updated_at = now_iso()
            session.add(row)
            session.commit()

    def delete_node(self, node_id: str) -> None:
        with Session(self.engine) as session:
            edge_stmt = select(EdgeRow).where(
                (EdgeRow.source_node_id == node_id) | (EdgeRow.target_node_id == node_id)
            )
            for edge in session.exec(edge_stmt).all():
                session.delete(edge)

            row = session.get(NodeRow, node_id)
            if row is not None:
                session.delete(row)
            session.commit()

        self._delete_search_records(node_id)

    def get_all_nodes(self, include_deleted: bool = False) -> list[Node]:
        with Session(self.engine) as session:
            stmt = select(NodeRow)
            if not include_deleted:
                stmt = stmt.where(NodeRow.status != NodeStatus.deleted.value)
            stmt = stmt.order_by(NodeRow.updated_at.desc())
            return [_node_from_record(row) for row in session.exec(stmt).all()]

    def get_nodes_by_document(
        self, document_name: str, active_only: bool = False
    ) -> list[Node]:
        with Session(self.engine) as session:
            stmt = select(NodeRow).where(NodeRow.original_document_name == document_name)
            if active_only:
                stmt = stmt.where(NodeRow.status == NodeStatus.active.value)
            stmt = stmt.order_by(NodeRow.updated_at.desc())
            return [_node_from_record(row) for row in session.exec(stmt).all()]

    def upsert_edge(self, edge: Edge) -> None:
        with Session(self.engine) as session:
            row = session.get(EdgeRow, edge.id)
            if row is None:
                row = EdgeRow(
                    id=edge.id,
                    source_node_id=edge.source_node_id,
                    target_node_id=edge.target_node_id,
                    label=edge.label,
                    summary=edge.summary,
                    created_at=edge.created_at,
                )
            else:
                row.label = edge.label
                row.summary = edge.summary

            session.add(row)
            session.commit()

    def get_all_edges(self) -> list[Edge]:
        with Session(self.engine) as session:
            stmt = select(EdgeRow).order_by(EdgeRow.created_at.desc())
            return [_edge_from_record(row) for row in session.exec(stmt).all()]

    def get_edges_for_node(self, node_id: str) -> list[Edge]:
        with Session(self.engine) as session:
            stmt = (
                select(EdgeRow)
                .where(
                    (EdgeRow.source_node_id == node_id)
                    | (EdgeRow.target_node_id == node_id)
                )
                .order_by(EdgeRow.created_at.desc())
            )
            return [_edge_from_record(row) for row in session.exec(stmt).all()]

    def get_outgoing_edges(self, node_id: str, label: str | None = None) -> list[Edge]:
        with Session(self.engine) as session:
            stmt = select(EdgeRow).where(EdgeRow.source_node_id == node_id)
            if label is not None:
                stmt = stmt.where(EdgeRow.label == label)
            stmt = stmt.order_by(EdgeRow.created_at.desc())
            return [_edge_from_record(row) for row in session.exec(stmt).all()]

    def get_incoming_edges(self, node_id: str, label: str | None = None) -> list[Edge]:
        with Session(self.engine) as session:
            stmt = select(EdgeRow).where(EdgeRow.target_node_id == node_id)
            if label is not None:
                stmt = stmt.where(EdgeRow.label == label)
            stmt = stmt.order_by(EdgeRow.created_at.desc())
            return [_edge_from_record(row) for row in session.exec(stmt).all()]

    def delete_edges_by_label_for_nodes(self, label: str, node_ids: set[str]) -> None:
        if not node_ids:
            return

        with Session(self.engine) as session:
            stmt = select(EdgeRow).where(
                EdgeRow.label == label,
                EdgeRow.source_node_id.in_(node_ids),
                EdgeRow.target_node_id.in_(node_ids),
            )
            for row in session.exec(stmt).all():
                session.delete(row)
            session.commit()

    def record_source(self, document_name: str, source_hash: str) -> None:
        stamp = now_iso()
        with Session(self.engine) as session:
            source_row = session.get(SourceRow, document_name)
            if source_row is None:
                source_row = SourceRow(
                    document_name=document_name,
                    source_hash=source_hash,
                    ingested_at=stamp,
                )
            else:
                source_row.source_hash = source_hash
                source_row.ingested_at = stamp
            session.add(source_row)

            version_stmt = select(SourceVersionRow).where(
                SourceVersionRow.document_name == document_name,
                SourceVersionRow.source_hash == source_hash,
            )
            version_row = session.exec(version_stmt).first()
            if version_row is None:
                session.add(
                    SourceVersionRow(
                        document_name=document_name,
                        source_hash=source_hash,
                        ingested_at=stamp,
                    )
                )

            session.commit()

    def get_source(self, document_name: str) -> tuple[str, str] | None:
        with Session(self.engine) as session:
            row = session.get(SourceRow, document_name)
            if row is None:
                return None
            return row.source_hash, row.ingested_at

    def keyword_search(self, text: str, limit: int = 20) -> list[Node]:
        query = _fts_query(text)
        if not query:
            return []
        rows = self.connection.execute(
            """
            SELECT n.* FROM nodes_fts f JOIN nodes n ON n.id = f.node_id
            WHERE nodes_fts MATCH ? AND n.status = 'active'
            ORDER BY rank LIMIT ?
            """,
            (query, limit),
        ).fetchall()
        return [_node_from_sql_row(row) for row in rows]

    def set_vector(self, node_id: str, table: str, vector: list[float]) -> None:
        import sqlite_vec

        if self._dim is None:
            raise RuntimeError("ensure_vec_tables() must run before set_vector()")
        blob = sqlite_vec.serialize_float32(vector)
        self.connection.execute(f"DELETE FROM {table} WHERE node_id=?", (node_id,))
        self.connection.execute(
            f"INSERT INTO {table}(node_id, embedding) VALUES(?, ?)", (node_id, blob)
        )
        self.connection.commit()

    def vector_search(
        self, vector: list[float], table: str = "vec_body", limit: int = 20
    ) -> list[tuple[str, float]]:
        import sqlite_vec

        if self._dim is None:
            return []
        blob = sqlite_vec.serialize_float32(vector)
        rows = self.connection.execute(
            f"""
            WITH matches AS (
                SELECT node_id, distance FROM {table}
                WHERE embedding MATCH ? ORDER BY distance LIMIT ?
            )
            SELECT m.node_id AS node_id, m.distance AS distance
            FROM matches m JOIN nodes n ON n.id = m.node_id
            WHERE n.status = 'active'
            ORDER BY m.distance
            """,
            (blob, limit),
        ).fetchall()
        return [(row["node_id"], row["distance"]) for row in rows]

    def _set_meta(self, key: str, value: str) -> None:
        with Session(self.engine) as session:
            row = session.get(MetaRow, key)
            if row is None:
                row = MetaRow(key=key, value=value)
            else:
                row.value = value
            session.add(row)
            session.commit()

    def _apply_node(self, row: Any, node: Node) -> None:
        row.body = node.body
        row.type = node.type.value
        row.title = node.title
        row.original_document_name = node.original_document_name
        row.source_path = node.source_path
        row.source_ranges_json = json.dumps(node.source_ranges)
        row.source_version = node.source_version
        row.source_material_hash = node.source_material_hash
        row.entity = node.entity
        row.claims_json = json.dumps(node.claims)
        row.keywords_json = json.dumps(node.keywords)
        row.summary = node.summary
        row.cluster = node.cluster
        row.status = node.status.value
        row.created_at = node.created_at
        row.updated_at = node.updated_at

    def _reindex_fts(self, node: Node) -> None:
        self.connection.execute("DELETE FROM nodes_fts WHERE node_id=?", (node.id,))
        if node.status == NodeStatus.deleted:
            return
        text = " ".join(
            filter(None, [node.title, node.summary, node.body, " ".join(node.keywords)])
        )
        self.connection.execute(
            "INSERT INTO nodes_fts(node_id, text) VALUES(?, ?)", (node.id, text)
        )

    def _delete_fts_record(self, node_id: str) -> None:
        self.connection.execute("DELETE FROM nodes_fts WHERE node_id=?", (node_id,))
        self.connection.commit()

    def _delete_search_records(self, node_id: str) -> None:
        self._delete_fts_record(node_id)
        if self._dim is None:
            return
        self.connection.execute("DELETE FROM vec_body WHERE node_id=?", (node_id,))
        self.connection.execute("DELETE FROM vec_summary WHERE node_id=?", (node_id,))
        self.connection.commit()


def _node_from_record(row: Any) -> Node:
    return Node(
        id=row.id,
        body=row.body,
        type=row.type,
        title=row.title or "",
        original_document_name=row.original_document_name,
        source_path=row.source_path,
        source_ranges=[tuple(r) for r in json.loads(row.source_ranges_json or "[]")],
        source_version=row.source_version,
        source_material_hash=row.source_material_hash,
        entity=row.entity or "",
        claims=json.loads(row.claims_json or "[]"),
        keywords=json.loads(row.keywords_json or "[]"),
        summary=row.summary or "",
        cluster=row.cluster,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _node_from_sql_row(row: sqlite3.Row) -> Node:
    return Node(
        id=row["id"],
        body=row["body"],
        type=row["type"],
        title=row["title"] or "",
        original_document_name=row["original_document_name"],
        source_path=row["source_path"],
        source_ranges=[tuple(r) for r in json.loads(row["source_ranges_json"] or "[]")],
        source_version=row["source_version"],
        source_material_hash=row["source_material_hash"],
        entity=row["entity"] or "",
        claims=json.loads(row["claims_json"] or "[]"),
        keywords=json.loads(row["keywords_json"] or "[]"),
        summary=row["summary"] or "",
        cluster=row["cluster"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _edge_from_record(row: Any) -> Edge:
    return Edge(
        id=row.id,
        source_node_id=row.source_node_id,
        target_node_id=row.target_node_id,
        label=row.label,
        summary=row.summary or "",
        created_at=row.created_at,
    )


Database = SQLModelDatabase
