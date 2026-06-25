"""Pydantic schema shared across the package (matches the canvas).

Embeddings are deliberately NOT fields on ``Node``: vectors live in sqlite-vec
tables keyed by node id, so the Python object stays light and JSON-friendly.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class NodeType(str, Enum):
    endogenous = "endogenous"  # straight from source markdown
    exogenous = "exogenous"    # agent/user-derived cache


class NodeStatus(str, Enum):
    active = "active"
    stale = "stale"
    deleted = "deleted"


class Node(BaseModel):
    id: str
    body: str
    type: NodeType = NodeType.endogenous
    title: str = ""
    original_document_name: str | None = None
    source_path: str | None = None
    source_ranges: list[tuple[int, int]] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    summary: str = ""
    cluster: str | None = None
    status: NodeStatus = NodeStatus.active
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)


class Edge(BaseModel):
    id: str
    source_node_id: str
    target_node_id: str
    label: str
    summary: str = ""
    created_at: str = Field(default_factory=now_iso)


class EdgeSuggestion(BaseModel):
    """One LLM-proposed link from the new node to an existing candidate."""

    target_node_id: str
    label: str = "related"
    summary: str = ""


class EdgeSuggestions(BaseModel):
    edges: list[EdgeSuggestion] = Field(default_factory=list)


class Keywords(BaseModel):
    keywords: list[str] = Field(default_factory=list)


class QueryResult(BaseModel):
    query_type: str
    value: str
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)


class GraphStats(BaseModel):
    total_nodes: int
    active_nodes: int
    endogenous_nodes: int
    exogenous_nodes: int
    total_edges: int
    isolated_nodes: int
    avg_degree: float
    density: float
    mean_neighbor_overlap: float
    clusters: dict[str, int] = Field(default_factory=dict)
    target_node_id: str | None = None
