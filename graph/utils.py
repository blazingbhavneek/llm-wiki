"""Small shared utilities for graph internals."""

from __future__ import annotations

import hashlib
import re
from typing import TYPE_CHECKING, Pattern

if TYPE_CHECKING:
    from .models import Node


# region HASHING
def short_hash(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def source_hash(text: str) -> str:
    """Identity of a whole source document, for recon dedup."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# endregion HASHING

# region IDENTIFIERS
_SLUG_RE = re.compile(r"[^a-z0-9]+")
_DEFAULT_TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")


def slug(text: str, max_length: int = 40) -> str:
    value = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return value[:max_length] or "node"


def make_node_id(body: str, document_name: str | None = None) -> str:
    return f"node:{slug(document_name or 'node', 24)}:{short_hash(body)}"


def make_exogenous_node_id(seed: str) -> str:
    return f"exo:{short_hash(seed)}"


def make_edge_id(source_id: str, target_id: str, label: str) -> str:
    return f"edge:{short_hash(f'{source_id}|{target_id}|{label}', 16)}"


# endregion IDENTIFIERS


# region TEXT MATCHING
def normalize_token(token: str) -> str:
    return token.strip().lower()


def normalize_text(text: str, token_re: Pattern[str] | None = None) -> str:
    matcher = token_re or _DEFAULT_TOKEN_RE
    return " ".join(normalize_token(token) for token in matcher.findall(text.lower()))


def jaccard(left: set[str], right: set[str]) -> float:
    left = {value for value in left if value}
    right = {value for value in right if value}
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def token_jaccard(left: str, right: str, token_re: Pattern[str]) -> float:
    return jaccard(
        {normalize_token(token) for token in token_re.findall(left.lower())},
        {normalize_token(token) for token in token_re.findall(right.lower())},
    )


def claim_keys(node: Node, token_re: Pattern[str]) -> set[str]:
    keys: set[str] = set()
    for claim in node.claims:
        normalized = normalize_text(claim, token_re)
        if normalized:
            keys.add(normalized)
    return keys


# endregion TEXT MATCHING
