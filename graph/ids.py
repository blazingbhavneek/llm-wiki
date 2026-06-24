"""Deterministic, stable node/edge id construction.

Stable ids let re-ingest of the same source upsert in place rather than
duplicate, and let topic/concept nodes be shared across documents (a global
topic node is the controlled cross-document link, not page-to-page cliques).
"""

from __future__ import annotations

import hashlib
import re

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slug(text: str, max_len: int = 60) -> str:
    s = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return s[:max_len] or "x"


def short_hash(text: str, n: int = 10) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def source_id(document_id: str) -> str:
    return f"src:{document_id}"


def version_id(document_id: str, sha256: str) -> str:
    return f"ver:{document_id}:{sha256[:12]}"


def doc_node_id(document_id: str) -> str:
    return f"doc:{document_id}"


def page_node_id(document_id: str, rel_path: str) -> str:
    return f"page:{document_id}:{short_hash(rel_path)}"


def topic_node_id(topic: str) -> str:
    # global / cross-document shared identity
    return f"topic:{slug(topic)}"


def concept_node_id(name: str) -> str:
    return f"concept:{slug(name)}"


def absolute_node_id(subtype: str, name: str) -> str:
    """Stable identity for an extracted, document-grounded canonical node."""
    if subtype == "concept":
        return concept_node_id(name)
    return f"{slug(subtype)}:{slug(name)}"


def synthetic_node_id(query_key: str) -> str:
    return f"synthetic:{short_hash(query_key, 12)}"


def edge_id(src_id: str, dst_id: str, etype: str) -> str:
    return f"e:{short_hash(f'{src_id}|{dst_id}|{etype}', 16)}"
