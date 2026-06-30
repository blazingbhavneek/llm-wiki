"""Single-class knowledge graph: everything hangs off `Graph`."""

# models first: it is the leaf that `db` / `embeddings` import. Loading it
# before `.graph` means it is fully cached by the time `.graph` pulls those
# siblings, so there is no re-entrant (circular) import.
from .graph import Graph
from .models import (
    AgentAnswer,
    ClaimExtraction,
    Edge,
    GraphStats,
    Node,
    NodeStatus,
    NodeType,
    QueryResult,
    Settings,
)

__all__ = [
    "Graph",
    "Settings",
    "Node",
    "Edge",
    "NodeType",
    "NodeStatus",
    "ClaimExtraction",
    "QueryResult",
    "GraphStats",
    "AgentAnswer",
]
