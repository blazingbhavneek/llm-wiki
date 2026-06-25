"""SQLite catalog: schema, transactions, repositories, FTS5.

One database, `.wiki/catalog.sqlite`, is the operational source of truth
(handoff.md "Catalog schema plan"). Five ordinary tables plus an FTS5 virtual
table. Evidence/aliases/dependency closures live in JSON fields for now.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional

from .models import Edge, Evidence, Node, dumps, loads, utcnow

SCHEMA_VERSION = 1
COMPILER_VERSION = "md.py/1"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    logical_path TEXT,
    name TEXT,
    current_version_id TEXT,
    source_type TEXT
);

CREATE TABLE IF NOT EXISTS source_versions (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    imported_at TEXT,
    compiler_version TEXT,
    active INTEGER DEFAULT 0,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    node_class TEXT NOT NULL,
    node_subtype TEXT,
    title TEXT,
    markdown_path TEXT,
    source_version_id TEXT,
    document_id TEXT,
    section_path_json TEXT,
    status TEXT DEFAULT 'active',
    metadata_json TEXT,
    created_at TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_nodes_doc ON nodes(document_id);
CREATE INDEX IF NOT EXISTS idx_nodes_class ON nodes(node_class, node_subtype);
CREATE INDEX IF NOT EXISTS idx_nodes_version ON nodes(source_version_id);

CREATE TABLE IF NOT EXISTS edges (
    id TEXT PRIMARY KEY,
    src_id TEXT NOT NULL,
    dst_id TEXT NOT NULL,
    type TEXT NOT NULL,
    explanation TEXT,
    strength REAL DEFAULT 1.0,
    status TEXT DEFAULT 'active',
    evidence_json TEXT,
    dependencies_json TEXT,
    created_by TEXT,
    created_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_edges_src ON edges(src_id);
CREATE INDEX IF NOT EXISTS idx_edges_dst ON edges(dst_id);
CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(type);

CREATE TABLE IF NOT EXISTS query_cache (
    id TEXT PRIMARY KEY,
    query_key TEXT NOT NULL,
    intent TEXT,
    synthetic_node_id TEXT,
    times_used INTEGER DEFAULT 0,
    times_refreshed INTEGER DEFAULT 0,
    created_at TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_query_key ON query_cache(query_key);

CREATE VIRTUAL TABLE IF NOT EXISTS node_fts USING fts5 (
    node_id UNINDEXED,
    title,
    aliases,
    summary,
    body,
    tokenize = 'porter unicode61'
);
"""


class Store:
    """Thin repository over a single SQLite connection."""

    def __init__(self, db_path: Path | str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(_SCHEMA)
        self.conn.execute(
            "INSERT OR IGNORE INTO meta(key, value) VALUES ('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )
        self.conn.commit()

    # -- transactions ------------------------------------------------------

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        try:
            yield self.conn
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def close(self) -> None:
        self.conn.close()

    # -- sources / versions ------------------------------------------------

    def upsert_source(
        self, source_id: str, logical_path: str, name: str, source_type: str = "markdown"
    ) -> None:
        self.conn.execute(
            """INSERT INTO sources(id, logical_path, name, source_type)
                 VALUES (?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 logical_path=excluded.logical_path,
                 name=excluded.name,
                 source_type=excluded.source_type""",
            (source_id, logical_path, name, source_type),
        )

    def add_source_version(
        self, version_id: str, source_id: str, sha256: str
    ) -> None:
        self.conn.execute(
            """INSERT OR REPLACE INTO source_versions
                 (id, source_id, sha256, imported_at, compiler_version, active)
               VALUES (?, ?, ?, ?, ?, 0)""",
            (version_id, source_id, sha256, utcnow(), COMPILER_VERSION),
        )

    def activate_version(self, source_id: str, version_id: str) -> None:
        """Atomically make one version current; deactivate siblings."""
        self.conn.execute(
            "UPDATE source_versions SET active=0 WHERE source_id=?", (source_id,)
        )
        self.conn.execute(
            "UPDATE source_versions SET active=1 WHERE id=?", (version_id,)
        )
        self.conn.execute(
            "UPDATE sources SET current_version_id=? WHERE id=?",
            (version_id, source_id),
        )

    def active_version(self, source_id: str) -> Optional[str]:
        row = self.conn.execute(
            "SELECT current_version_id FROM sources WHERE id=?", (source_id,)
        ).fetchone()
        return row["current_version_id"] if row else None

    def version_sha(self, version_id: str) -> Optional[str]:
        row = self.conn.execute(
            "SELECT sha256 FROM source_versions WHERE id=?", (version_id,)
        ).fetchone()
        return row["sha256"] if row else None

    # -- nodes -------------------------------------------------------------

    def upsert_node(self, node: Node) -> None:
        node.updated_at = utcnow()
        self.conn.execute(
            """INSERT INTO nodes
                 (id, node_class, node_subtype, title, markdown_path,
                  source_version_id, document_id, section_path_json, status,
                  metadata_json, created_at, updated_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 node_class=excluded.node_class,
                 node_subtype=excluded.node_subtype,
                 title=excluded.title,
                 markdown_path=excluded.markdown_path,
                 source_version_id=excluded.source_version_id,
                 document_id=excluded.document_id,
                 section_path_json=excluded.section_path_json,
                 status=excluded.status,
                 metadata_json=excluded.metadata_json,
                 updated_at=excluded.updated_at""",
            (
                node.id,
                node.node_class,
                node.node_subtype,
                node.title,
                node.markdown_path,
                node.source_version_id,
                node.document_id,
                dumps(node.section_path),
                node.status,
                dumps(node.metadata),
                node.created_at,
                node.updated_at,
            ),
        )

    def get_node(self, node_id: str) -> Optional[Node]:
        row = self.conn.execute(
            "SELECT * FROM nodes WHERE id=?", (node_id,)
        ).fetchone()
        return _row_to_node(row) if row else None

    def source_versions_for_node(self, node_id: str) -> set[str]:
        """Return every current source version that directly supports a node.

        Source pages carry their version on the node. Canonical topic/concept
        nodes are shared across documents, so their supporting versions live on
        the evidence of their active incident edges.
        """
        versions: set[str] = set()
        node = self.get_node(node_id)
        if node and node.source_version_id:
            versions.add(node.source_version_id)
        for edge in self.edges_touching(node_id, status="active"):
            versions.update(
                evidence.source_version_id
                for evidence in edge.evidence
                if evidence.source_version_id
            )
        return versions

    def set_node_status(self, node_id: str, status: str) -> None:
        self.conn.execute(
            "UPDATE nodes SET status=?, updated_at=? WHERE id=?",
            (status, utcnow(), node_id),
        )

    def nodes_by_version(self, version_id: str) -> list[Node]:
        rows = self.conn.execute(
            "SELECT * FROM nodes WHERE source_version_id=?", (version_id,)
        ).fetchall()
        return [_row_to_node(r) for r in rows]

    def nodes_by_class(self, node_class: str) -> list[Node]:
        rows = self.conn.execute(
            "SELECT * FROM nodes WHERE node_class=?", (node_class,)
        ).fetchall()
        return [_row_to_node(r) for r in rows]

    def all_nodes(self) -> list[Node]:
        rows = self.conn.execute("SELECT * FROM nodes").fetchall()
        return [_row_to_node(r) for r in rows]

    # -- edges -------------------------------------------------------------

    def upsert_edge(self, edge: Edge) -> None:
        existing = self.get_edge(edge.id)
        if existing:
            edge.evidence = _merge_evidence(existing.evidence, edge.evidence)
            edge.dependencies = sorted(set(existing.dependencies) | set(edge.dependencies))
            edge.strength = max(existing.strength, edge.strength)
        self.conn.execute(
            """INSERT INTO edges
                 (id, src_id, dst_id, type, explanation, strength, status,
                  evidence_json, dependencies_json, created_by, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 type=excluded.type,
                 explanation=excluded.explanation,
                 strength=excluded.strength,
                 status=excluded.status,
                 evidence_json=excluded.evidence_json,
                 dependencies_json=excluded.dependencies_json,
                 created_by=excluded.created_by""",
            (
                edge.id,
                edge.src_id,
                edge.dst_id,
                edge.type,
                edge.explanation,
                edge.strength,
                edge.status,
                dumps([e.to_dict() for e in edge.evidence]),
                dumps(edge.dependencies),
                edge.created_by,
                edge.created_at,
            ),
        )

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        row = self.conn.execute(
            "SELECT * FROM edges WHERE id=?", (edge_id,)
        ).fetchone()
        return _row_to_edge(row) if row else None

    def edges_from(self, node_id: str, status: str = "active") -> list[Edge]:
        rows = self.conn.execute(
            "SELECT * FROM edges WHERE src_id=? AND status=?", (node_id, status)
        ).fetchall()
        return [_row_to_edge(r) for r in rows]

    def edges_to(self, node_id: str, status: str = "active") -> list[Edge]:
        rows = self.conn.execute(
            "SELECT * FROM edges WHERE dst_id=? AND status=?", (node_id, status)
        ).fetchall()
        return [_row_to_edge(r) for r in rows]

    def edges_touching(self, node_id: str, status: str = "active") -> list[Edge]:
        rows = self.conn.execute(
            "SELECT * FROM edges WHERE (src_id=? OR dst_id=?) AND status=?",
            (node_id, node_id, status),
        ).fetchall()
        return [_row_to_edge(r) for r in rows]

    def all_edges(self) -> list[Edge]:
        rows = self.conn.execute("SELECT * FROM edges").fetchall()
        return [_row_to_edge(r) for r in rows]

    def set_edge_status_for_version(self, version_id: str, status: str) -> int:
        """Remove retired-version evidence without discarding other support.

        A canonical edge may be supported by several current documents. Retiring
        one source version makes it stale only when no evidence remains.
        """
        changed = 0
        for edge in self.all_edges():
            remaining = [
                evidence
                for evidence in edge.evidence
                if evidence.source_version_id != version_id
            ]
            if len(remaining) != len(edge.evidence):
                next_status = edge.status if remaining else status
                self.conn.execute(
                    "UPDATE edges SET status=?, evidence_json=? WHERE id=?",
                    (next_status, dumps([e.to_dict() for e in remaining]), edge.id),
                )
                changed += 1
        return changed

    # -- FTS5 --------------------------------------------------------------

    def fts_delete(self, node_id: str) -> None:
        self.conn.execute("DELETE FROM node_fts WHERE node_id=?", (node_id,))

    def fts_index(
        self, node_id: str, title: str, aliases: str, summary: str, body: str
    ) -> None:
        self.fts_delete(node_id)
        self.conn.execute(
            "INSERT INTO node_fts(node_id, title, aliases, summary, body) "
            "VALUES (?, ?, ?, ?, ?)",
            (node_id, title, aliases, summary, body),
        )

    def fts_search(self, query: str, limit: int = 20) -> list[tuple[str, float]]:
        """Return (node_id, rank-score) ordered best first. Higher is better."""
        try:
            rows = self.conn.execute(
                "SELECT node_id, bm25(node_fts) AS score FROM node_fts "
                "WHERE node_fts MATCH ? ORDER BY score LIMIT ?",
                (query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            return []
        # bm25 returns lower=better; invert to a positive relevance score.
        return [(r["node_id"], -float(r["score"])) for r in rows]

    # -- query cache -------------------------------------------------------

    def get_cache(self, query_key: str) -> Optional[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM query_cache WHERE query_key=?", (query_key,)
        ).fetchone()

    def upsert_cache(
        self, cache_id: str, query_key: str, intent: str, synthetic_node_id: str
    ) -> None:
        now = utcnow()
        self.conn.execute(
            """INSERT INTO query_cache
                 (id, query_key, intent, synthetic_node_id, times_used,
                  times_refreshed, created_at, updated_at)
                 VALUES (?, ?, ?, ?, 0, 0, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 synthetic_node_id=excluded.synthetic_node_id,
                 updated_at=excluded.updated_at""",
            (cache_id, query_key, intent, synthetic_node_id, now, now),
        )

    def bump_cache_use(self, query_key: str) -> int:
        self.conn.execute(
            "UPDATE query_cache SET times_used=times_used+1, updated_at=? "
            "WHERE query_key=?",
            (utcnow(), query_key),
        )
        row = self.get_cache(query_key)
        return int(row["times_used"]) if row else 0


# --------------------------------------------------------------------------
# Row mappers
# --------------------------------------------------------------------------


def _row_to_node(row: sqlite3.Row) -> Node:
    return Node(
        id=row["id"],
        node_class=row["node_class"],
        node_subtype=row["node_subtype"] or "",
        title=row["title"] or "",
        markdown_path=row["markdown_path"],
        source_version_id=row["source_version_id"],
        document_id=row["document_id"],
        section_path=loads(row["section_path_json"], []),
        status=row["status"] or "active",
        metadata=loads(row["metadata_json"], {}),
        created_at=row["created_at"] or "",
        updated_at=row["updated_at"] or "",
    )


def _row_to_edge(row: sqlite3.Row) -> Edge:
    return Edge(
        id=row["id"],
        src_id=row["src_id"],
        dst_id=row["dst_id"],
        type=row["type"],
        explanation=row["explanation"] or "",
        strength=float(row["strength"] if row["strength"] is not None else 1.0),
        status=row["status"] or "active",
        evidence=[Evidence.from_dict(e) for e in loads(row["evidence_json"], [])],
        dependencies=loads(row["dependencies_json"], []),
        created_by=row["created_by"] or "bootstrap",
        created_at=row["created_at"] or "",
    )


def _merge_evidence(existing: list[Evidence], new: list[Evidence]) -> list[Evidence]:
    unique: dict[tuple[str, str, str, str], Evidence] = {}
    for evidence in [*existing, *new]:
        key = (
            evidence.source_version_id,
            evidence.document_id,
            dumps(evidence.source_ranges),
            evidence.note,
        )
        unique[key] = evidence
    return list(unique.values())
