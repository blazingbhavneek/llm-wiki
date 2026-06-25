"""SQLite storage: nodes, edges, FTS5 keyword index, sqlite-vec vector index.

One file holds everything. Vectors are stored in ``vec0`` virtual tables keyed
by node id; full-text lives in an FTS5 table kept in sync manually on write.
"""

from __future__ import annotations

import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .models import Edge, Node, NodeStatus, now_iso

_FTS_SPECIAL = re.compile(r'["()*:^]')


def _fts_query(text: str) -> str:
    """Turn free text into a safe FTS5 OR-query of quoted terms."""

    terms = [t for t in _FTS_SPECIAL.sub(" ", text).split() if t]
    return " OR ".join(f'"{t}"' for t in terms)


class Database:
    def __init__(self, path: str | Path = ".wiki/wiki.sqlite") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path))
        self.connection.row_factory = sqlite3.Row
        self._load_vec_extension()
        self._dim: int | None = None
        self._create_core_tables()
        self._restore_dim()

    # ── extension / schema ──────────────────────────────────────────────

    def _load_vec_extension(self) -> None:
        import sqlite_vec

        self.connection.enable_load_extension(True)
        sqlite_vec.load(self.connection)
        self.connection.enable_load_extension(False)

    def _create_core_tables(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);

            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                body TEXT NOT NULL,
                type TEXT NOT NULL,
                title TEXT,
                original_document_name TEXT,
                source_path TEXT,
                source_ranges_json TEXT NOT NULL,
                source_version TEXT,
                source_material_hash TEXT,
                entity TEXT,
                claims_json TEXT NOT NULL DEFAULT '[]',
                keywords_json TEXT NOT NULL,
                summary TEXT,
                cluster TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(type);
            CREATE INDEX IF NOT EXISTS idx_nodes_status ON nodes(status);
            CREATE INDEX IF NOT EXISTS idx_nodes_doc ON nodes(original_document_name);

            CREATE TABLE IF NOT EXISTS edges (
                id TEXT PRIMARY KEY,
                source_node_id TEXT NOT NULL,
                target_node_id TEXT NOT NULL,
                label TEXT NOT NULL,
                summary TEXT,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_node_id);
            CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_node_id);

            CREATE TABLE IF NOT EXISTS sources (
                document_name TEXT PRIMARY KEY,
                source_hash TEXT NOT NULL,
                ingested_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS source_versions (
                document_name TEXT NOT NULL,
                source_hash TEXT NOT NULL,
                ingested_at TEXT NOT NULL,
                PRIMARY KEY(document_name, source_hash)
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS nodes_fts USING fts5(
                node_id UNINDEXED, text
            );
            """
        )
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

    def _restore_dim(self) -> None:
        row = self.connection.execute(
            "SELECT value FROM meta WHERE key = 'embed_dim'"
        ).fetchone()
        if row:
            self._dim = int(row["value"])

    def ensure_vec_tables(self, dim: int) -> None:
        """Create the vec0 tables once the real embedding dim is known."""

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
        self.connection.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES('embed_dim', ?)",
            (str(dim),),
        )
        self.connection.commit()
        self._dim = dim

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        try:
            yield self.connection
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def close(self) -> None:
        self.connection.close()

    # ── nodes ───────────────────────────────────────────────────────────

    def upsert_node(self, node: Node) -> None:
        import json

        existing = self.get_node(node.id)
        if existing:
            node.created_at = existing.created_at
        node.updated_at = now_iso()
        self.connection.execute(
            """
            INSERT INTO nodes (id, body, type, title, original_document_name,
                source_path, source_ranges_json, source_version,
                source_material_hash, entity, claims_json, keywords_json, summary,
                cluster, status, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
                body=excluded.body, type=excluded.type, title=excluded.title,
                original_document_name=excluded.original_document_name,
                source_path=excluded.source_path,
                source_ranges_json=excluded.source_ranges_json,
                source_version=excluded.source_version,
                source_material_hash=excluded.source_material_hash,
                entity=excluded.entity,
                claims_json=excluded.claims_json,
                keywords_json=excluded.keywords_json, summary=excluded.summary,
                cluster=excluded.cluster, status=excluded.status,
                updated_at=excluded.updated_at
            """,
            (
                node.id, node.body, node.type.value, node.title,
                node.original_document_name, node.source_path,
                json.dumps(node.source_ranges), node.source_version,
                node.source_material_hash, node.entity,
                json.dumps(node.claims), json.dumps(node.keywords),
                node.summary, node.cluster, node.status.value,
                node.created_at, node.updated_at,
            ),
        )
        self._reindex_fts(node)
        self.connection.commit()

    def get_node(self, node_id: str) -> Node | None:
        row = self.connection.execute(
            "SELECT * FROM nodes WHERE id = ?", (node_id,)
        ).fetchone()
        return _row_to_node(row) if row else None

    def set_node_status(self, node_id: str, status: NodeStatus) -> None:
        self.connection.execute(
            "UPDATE nodes SET status=?, updated_at=? WHERE id=?",
            (status.value, now_iso(), node_id),
        )
        self.connection.commit()

    def delete_node(self, node_id: str) -> None:
        with self.transaction() as conn:
            conn.execute(
                "DELETE FROM edges WHERE source_node_id=? OR target_node_id=?",
                (node_id, node_id),
            )
            conn.execute("DELETE FROM nodes WHERE id=?", (node_id,))
            conn.execute("DELETE FROM nodes_fts WHERE node_id=?", (node_id,))
            if self._dim is not None:
                conn.execute("DELETE FROM vec_body WHERE node_id=?", (node_id,))
                conn.execute("DELETE FROM vec_summary WHERE node_id=?", (node_id,))

    def get_all_nodes(self, include_deleted: bool = False) -> list[Node]:
        sql = "SELECT * FROM nodes"
        if not include_deleted:
            sql += " WHERE status != 'deleted'"
        sql += " ORDER BY updated_at DESC"
        return [_row_to_node(r) for r in self.connection.execute(sql).fetchall()]

    def get_nodes_by_document(
        self, document_name: str, active_only: bool = False
    ) -> list[Node]:
        sql = "SELECT * FROM nodes WHERE original_document_name=?"
        params: list[str] = [document_name]
        if active_only:
            sql += " AND status='active'"
        sql += " ORDER BY updated_at DESC"
        return [_row_to_node(r) for r in self.connection.execute(sql, params).fetchall()]

    # ── edges ───────────────────────────────────────────────────────────

    def upsert_edge(self, edge: Edge) -> None:
        self.connection.execute(
            """
            INSERT INTO edges (id, source_node_id, target_node_id, label, summary, created_at)
            VALUES (?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET label=excluded.label, summary=excluded.summary
            """,
            (edge.id, edge.source_node_id, edge.target_node_id, edge.label,
             edge.summary, edge.created_at),
        )
        self.connection.commit()

    def get_all_edges(self) -> list[Edge]:
        rows = self.connection.execute(
            "SELECT * FROM edges ORDER BY created_at DESC"
        ).fetchall()
        return [_row_to_edge(r) for r in rows]

    def get_edges_for_node(self, node_id: str) -> list[Edge]:
        rows = self.connection.execute(
            "SELECT * FROM edges WHERE source_node_id=? OR target_node_id=? ORDER BY created_at DESC",
            (node_id, node_id),
        ).fetchall()
        return [_row_to_edge(r) for r in rows]

    def get_outgoing_edges(self, node_id: str, label: str | None = None) -> list[Edge]:
        sql = "SELECT * FROM edges WHERE source_node_id=?"
        params: list[str] = [node_id]
        if label is not None:
            sql += " AND label=?"
            params.append(label)
        sql += " ORDER BY created_at DESC"
        return [_row_to_edge(r) for r in self.connection.execute(sql, params).fetchall()]

    def get_incoming_edges(self, node_id: str, label: str | None = None) -> list[Edge]:
        sql = "SELECT * FROM edges WHERE target_node_id=?"
        params: list[str] = [node_id]
        if label is not None:
            sql += " AND label=?"
            params.append(label)
        sql += " ORDER BY created_at DESC"
        return [_row_to_edge(r) for r in self.connection.execute(sql, params).fetchall()]

    def delete_edges_by_label_for_nodes(self, label: str, node_ids: set[str]) -> None:
        if not node_ids:
            return
        placeholders = ",".join("?" for _ in node_ids)
        params = [label, *node_ids, *node_ids]
        self.connection.execute(
            f"""
            DELETE FROM edges
            WHERE label=?
              AND source_node_id IN ({placeholders})
              AND target_node_id IN ({placeholders})
            """,
            params,
        )
        self.connection.commit()

    # ── sources (recon dedup) ───────────────────────────────────────────

    def record_source(self, document_name: str, source_hash: str) -> None:
        stamp = now_iso()
        with self.transaction() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO sources(document_name, source_hash, ingested_at) VALUES(?,?,?)",
                (document_name, source_hash, stamp),
            )
            conn.execute(
                """
                INSERT OR IGNORE INTO source_versions(document_name, source_hash, ingested_at)
                VALUES(?,?,?)
                """,
                (document_name, source_hash, stamp),
            )

    def get_source(self, document_name: str) -> tuple[str, str] | None:
        row = self.connection.execute(
            "SELECT source_hash, ingested_at FROM sources WHERE document_name=?",
            (document_name,),
        ).fetchone()
        return (row["source_hash"], row["ingested_at"]) if row else None

    # ── search ──────────────────────────────────────────────────────────

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
        return [_row_to_node(r) for r in rows]

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
        """Return (node_id, distance) nearest neighbours; deleted nodes filtered."""

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
        return [(r["node_id"], r["distance"]) for r in rows]


def _row_to_node(row: sqlite3.Row) -> Node:
    import json

    return Node(
        id=row["id"], body=row["body"], type=row["type"], title=row["title"] or "",
        original_document_name=row["original_document_name"],
        source_path=row["source_path"],
        source_ranges=[tuple(r) for r in json.loads(row["source_ranges_json"] or "[]")],
        source_version=row["source_version"],
        source_material_hash=row["source_material_hash"],
        entity=row["entity"] or "",
        claims=json.loads(row["claims_json"] or "[]"),
        keywords=json.loads(row["keywords_json"] or "[]"),
        summary=row["summary"] or "", cluster=row["cluster"], status=row["status"],
        created_at=row["created_at"], updated_at=row["updated_at"],
    )


def _row_to_edge(row: sqlite3.Row) -> Edge:
    return Edge(
        id=row["id"], source_node_id=row["source_node_id"],
        target_node_id=row["target_node_id"], label=row["label"],
        summary=row["summary"] or "", created_at=row["created_at"],
    )
