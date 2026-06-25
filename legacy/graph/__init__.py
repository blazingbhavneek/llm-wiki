"""Knowledge-graph layer over md.py compiled output.

md.py owns: raw Markdown -> lossless source-local tree.
graph/ owns: compiled tree -> catalog, graph, search, query, synthetic knowledge.

See handoff.md for the design contract. This package is a thin vertical slice:
one SQLite catalog (.wiki/catalog.sqlite), FTS5 search, typed/weighted/evidenced
edges, document subgraphs, and reusable synthetic Markdown nodes.
"""

from .models import (
    NodeClass,
    Node,
    Edge,
    Evidence,
    CompiledSourcePage,
    CompiledDocument,
)
from .store import Store

__all__ = [
    "NodeClass",
    "Node",
    "Edge",
    "Evidence",
    "CompiledSourcePage",
    "CompiledDocument",
    "Store",
]
