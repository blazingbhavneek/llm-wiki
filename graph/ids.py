"""Stable ids for nodes and edges."""

from __future__ import annotations

import hashlib
import re

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def short_hash(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def slug(text: str, max_length: int = 40) -> str:
    value = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return value[:max_length] or "node"


def make_node_id(body: str, document_name: str | None = None) -> str:
    return f"node:{slug(document_name or 'node', 24)}:{short_hash(body)}"


def make_exogenous_node_id(seed: str) -> str:
    return f"exo:{short_hash(seed)}"


def make_edge_id(source_id: str, target_id: str, label: str) -> str:
    return f"edge:{short_hash(f'{source_id}|{target_id}|{label}', 16)}"


def source_hash(text: str) -> str:
    """Identity of a whole source document, for recon dedup."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
