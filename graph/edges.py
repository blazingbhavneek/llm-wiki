"""Semantic edge construction + graph clustering.

Edges: candidates come from embedding KNN (sqlite-vec), NOT literal keyword
overlap. The LLM then judges which candidates truly relate and labels each link.
Edges are written bidirectionally.

Clusters: Louvain community detection over the edge graph (edge multiplicity =
weight). Communities are labelled by their dominant keyword.
"""

from __future__ import annotations

from collections import Counter

from .database import Database
from .ids import make_edge_id
from .models import Edge, Node, NodeStatus


def knn_candidates(
    db: Database, node_id: str, body_vec: list[float],
    summary_vec: list[float] | None, k: int,
) -> list[Node]:
    """Union of nearest neighbours by body- and summary-embedding."""

    ranked: list[str] = []
    probes = [("vec_body", body_vec)]
    if summary_vec:
        probes.append(("vec_summary", summary_vec))
    for table, vec in probes:
        for nid, _dist in db.vector_search(vec, table, k + 1):
            if nid != node_id and nid not in ranked:
                ranked.append(nid)

    candidates: list[Node] = []
    for nid in ranked:
        other = db.get_node(nid)
        if other and other.status == NodeStatus.active:
            candidates.append(other)
    return candidates[:k]


def build_semantic_edges(
    db: Database, llm, node: Node, body_vec: list[float],
    summary_vec: list[float] | None, k: int,
) -> list[Edge]:
    candidates = knn_candidates(db, node.id, body_vec, summary_vec, k)
    suggestions = llm.suggest_edges(node, candidates)
    edges: list[Edge] = []
    for sug in suggestions:
        if sug.target_node_id == node.id:
            continue
        label = sug.label.strip() or "related"
        forward = Edge(
            id=make_edge_id(node.id, sug.target_node_id, label),
            source_node_id=node.id, target_node_id=sug.target_node_id,
            label=label, summary=sug.summary.strip(),
        )
        back = Edge(
            id=make_edge_id(sug.target_node_id, node.id, label),
            source_node_id=sug.target_node_id, target_node_id=node.id,
            label=label, summary=sug.summary.strip(),
        )
        db.upsert_edge(forward)
        db.upsert_edge(back)
        edges.extend([forward, back])
    return edges


# ── clustering ──────────────────────────────────────────────────────────


def louvain_clusters(
    db: Database, resolution: float = 1.0, seed: int = 42, persist: bool = True
) -> dict[str, str]:
    """Assign every active node a cluster via Louvain community detection.

    Builds an undirected weighted graph over active nodes (weight = number of
    edges between a pair), runs Louvain, then labels each community by its most
    common keyword. Returns ``{node_id: cluster_label}`` and, when ``persist``,
    writes the label onto each node's ``cluster`` field.
    """

    import networkx as nx

    nodes = [n for n in db.get_all_nodes() if n.status == NodeStatus.active]
    node_by_id = {n.id: n for n in nodes}

    graph = nx.Graph()
    graph.add_nodes_from(node_by_id)
    for edge in db.get_all_edges():
        u, v = edge.source_node_id, edge.target_node_id
        if u in node_by_id and v in node_by_id and u != v:
            if graph.has_edge(u, v):
                graph[u][v]["weight"] += 1.0
            else:
                graph.add_edge(u, v, weight=1.0)

    communities = nx.community.louvain_communities(
        graph, weight="weight", resolution=resolution, seed=seed
    )

    mapping: dict[str, str] = {}
    used: Counter[str] = Counter()
    for index, members in enumerate(sorted(communities, key=len, reverse=True)):
        label = _community_label(members, node_by_id, index, used)
        for nid in members:
            mapping[nid] = label

    if persist:
        for node in nodes:
            new_label = mapping.get(node.id)
            if new_label and node.cluster != new_label:
                node.cluster = new_label
                db.upsert_node(node)

    return mapping


def _community_label(
    members: set[str], node_by_id: dict[str, Node], index: int, used: Counter
) -> str:
    """Dominant keyword across the community; unique, human-ish."""

    counts: Counter[str] = Counter()
    for nid in members:
        node = node_by_id.get(nid)
        if node:
            counts.update(kw.lower() for kw in node.keywords)
    if counts:
        top = counts.most_common(1)[0][0].title()
    else:
        top = f"Cluster {index + 1}"
    used[top] += 1
    return f"{top} {used[top]}" if used[top] > 1 else top
