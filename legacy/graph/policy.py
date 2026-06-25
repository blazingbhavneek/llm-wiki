"""Versioned graph policy (.wiki/graph-policy.yml).

maintenance.py and query.py both read this for traversal budgets and linting;
no separate policy/health service (handoff.md "Graph policy and health controls").
A tiny flat parser avoids a PyYAML dependency for the simple scalar schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_POLICY: dict[str, Any] = {
    "max_semantic_hops": 2,
    "second_hop_decay": 0.35,
    "max_query_nodes": 30,
    "max_external_edges_per_source_page": 8,
    "max_external_edges_per_document": 25,
    "max_edges_per_expansion": 8,
    "max_local_pages_from_document": 6,
    "contains_traversal_weight": 0.1,
    "max_edges_per_synthetic_node": 10,
    "minimum_active_strength": 0.45,
    "synthetic_repeat_query_threshold": 2,
    "synthetic_requires_absolute_evidence": True,
    "exclude_stale_synthetic_nodes": True,
}

_DEFAULT_YML = "\n".join(
    f"{k}: {str(v).lower() if isinstance(v, bool) else v}"
    for k, v in DEFAULT_POLICY.items()
)


@dataclass
class Policy:
    values: dict[str, Any]

    def __getattr__(self, name: str) -> Any:
        try:
            return self.values[name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise AttributeError(name) from exc

    def get(self, name: str, default: Any = None) -> Any:
        return self.values.get(name, default)


def _coerce(raw: str) -> Any:
    low = raw.lower()
    if low in ("true", "false"):
        return low == "true"
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        return raw


def load_policy(path: Path | str) -> Policy:
    path = Path(path)
    values = dict(DEFAULT_POLICY)
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if not line or ":" not in line:
                continue
            key, _, raw = line.partition(":")
            values[key.strip()] = _coerce(raw.strip())
    return Policy(values)


def ensure_policy_file(path: Path | str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(_DEFAULT_YML + "\n", encoding="utf-8")
    return path
