"""Real graph-health metrics (no placeholder counts)."""

from __future__ import annotations

from .models import Edge, GraphStats, Node, NodeStatus, NodeType


def compute_health(
    nodes: list[Node], edges: list[Edge], target_node_id: str | None = None
) -> GraphStats:
    if target_node_id:
        nodes = [n for n in nodes if n.id == target_node_id]
        edges = [
            e for e in edges
            if e.source_node_id == target_node_id or e.target_node_id == target_node_id
        ]

    node_ids = {n.id for n in nodes}
    neighbors: dict[str, set[str]] = {nid: set() for nid in node_ids}
    for e in edges:
        if e.source_node_id in neighbors and e.target_node_id in node_ids:
            neighbors[e.source_node_id].add(e.target_node_id)
        if e.target_node_id in neighbors and e.source_node_id in node_ids:
            neighbors[e.target_node_id].add(e.source_node_id)

    n = len(nodes)
    degrees = [len(neighbors[nid]) for nid in node_ids]
    total_degree = sum(degrees)
    avg_degree = (total_degree / n) if n else 0.0
    max_edges = n * (n - 1) / 2
    undirected_edges = total_degree / 2
    density = (undirected_edges / max_edges) if max_edges else 0.0

    overlap = _mean_neighbor_overlap(neighbors)
    clusters: dict[str, int] = {}
    for node in nodes:
        key = node.cluster or "Unclustered"
        clusters[key] = clusters.get(key, 0) + 1

    return GraphStats(
        total_nodes=n,
        active_nodes=sum(1 for x in nodes if x.status == NodeStatus.active),
        endogenous_nodes=sum(1 for x in nodes if x.type == NodeType.endogenous),
        exogenous_nodes=sum(1 for x in nodes if x.type == NodeType.exogenous),
        total_edges=len(edges),
        isolated_nodes=sum(1 for nid in node_ids if not neighbors[nid]),
        avg_degree=round(avg_degree, 3),
        density=round(density, 5),
        mean_neighbor_overlap=round(overlap, 4),
        clusters=clusters,
        target_node_id=target_node_id,
    )


def _mean_neighbor_overlap(neighbors: dict[str, set[str]]) -> float:
    """Mean Jaccard overlap of neighbour sets across connected pairs.

    High overlap => redundant/too-dense; near-zero with edges => healthy spread.
    """

    pairs = 0
    total = 0.0
    items = list(neighbors.items())
    for nid, nbrs in items:
        for other in nbrs:
            if other <= nid:  # count each unordered pair once
                continue
            a, b = nbrs, neighbors.get(other, set())
            union = a | b
            if union:
                total += len(a & b) / len(union)
                pairs += 1
    return (total / pairs) if pairs else 0.0
