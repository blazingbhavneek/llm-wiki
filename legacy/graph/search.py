"""Search backends behind one interface (handoff.md "Simplification boundaries").

FTS5 is the default and only source of truth. Elasticsearch and vector search
are optional adapters added later without changing ingest or query. The query
service depends only on the SearchBackend protocol.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

from .store import Store

_FTS_SPECIAL = re.compile(r'["^*():]')


@dataclass
class SearchHit:
    node_id: str
    score: float


class SearchBackend(Protocol):
    def search(self, query: str, limit: int = 20) -> list[SearchHit]: ...


def _sanitize_fts_query(query: str) -> str:
    """Turn free text into a safe FTS5 OR query of bare terms."""
    cleaned = _FTS_SPECIAL.sub(" ", query)
    terms = [t for t in cleaned.split() if t]
    if not terms:
        return ""
    return " OR ".join(terms)


class Fts5Backend:
    """SQLite FTS5 over node titles, aliases, summaries, and Markdown text."""

    name = "fts5"

    def __init__(self, store: Store):
        self.store = store

    def search(self, query: str, limit: int = 20) -> list[SearchHit]:
        match = _sanitize_fts_query(query)
        if not match:
            return []
        return [
            SearchHit(node_id=nid, score=score)
            for nid, score in self.store.fts_search(match, limit)
        ]

    def exact_title(self, query: str, limit: int = 10) -> list[SearchHit]:
        rows = self.store.conn.execute(
            "SELECT id FROM nodes WHERE lower(title)=lower(?) AND status='active' "
            "LIMIT ?",
            (query.strip(), limit),
        ).fetchall()
        # exact-title matches rank above any fuzzy FTS hit
        return [SearchHit(node_id=r["id"], score=1000.0) for r in rows]
