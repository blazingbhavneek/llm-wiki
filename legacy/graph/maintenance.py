"""On-demand maintenance: reindex, lazy stale refresh, lint, health metrics.

No background workers; everything runs from the explicit `maintain` command
(handoff.md "Graph policy and health controls"). Lints the invariants the
handoff calls out: edge-evidence coverage, stale counts, hub concentration,
document subgraphs with no external links, and synthetic dependency health.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .llm import LLMClient
from .models import SUBTYPE_SOURCE_PAGE, SUBTYPE_TOPIC
from .policy import Policy
from .query import QueryService
from .store import Store
from .synthetic import SyntheticManager


@dataclass
class HealthReport:
    metrics: dict = field(default_factory=dict)
    lints: list[str] = field(default_factory=list)

    def text(self) -> str:
        out = ["# Graph health", "", "## Metrics"]
        for k, v in self.metrics.items():
            out.append(f"- {k}: {v}")
        out.append("")
        out.append("## Lints")
        if not self.lints:
            out.append("- (none)")
        for w in self.lints:
            out.append(f"- ⚠ {w}")
        return "\n".join(out)


class Maintenance:
    def __init__(
        self,
        store: Store,
        policy: Policy,
        wiki_dir: Path | str,
        llm: Optional[LLMClient] = None,
    ):
        self.store = store
        self.policy = policy
        self.wiki_dir = Path(wiki_dir)
        self.llm = llm

    # ----------------------------------------------------------- reindex

    def reindex(self) -> int:
        """Rebuild FTS for every active node from its Markdown/summary."""
        count = 0
        for node in self.store.all_nodes():
            if node.status != "active":
                self.store.fts_delete(node.id)
                continue
            body = ""
            if node.markdown_path and Path(node.markdown_path).exists():
                body = Path(node.markdown_path).read_text(encoding="utf-8")
            aliases = " ".join(node.metadata.get("local_topics", []))
            self.store.fts_index(
                node.id, node.title, aliases, node.summary, body or node.summary
            )
            count += 1
        self.store.conn.commit()
        return count

    # --------------------------------------------------- lazy stale refresh

    def refresh_stale_synthetic(self, limit: int = 50) -> int:
        """Lazily refresh stale synthetic nodes (handoff: refresh on maintain)."""
        qs = QueryService(self.store, self.policy)
        sm = SyntheticManager(self.store, self.policy, self.wiki_dir, self.llm)
        refreshed = 0
        for node in self.store.nodes_by_class("synthetic"):
            if node.status != "stale":
                continue
            query = node.metadata.get("creation_query", node.title)
            result = qs.query(query)
            new = sm.create_or_refresh(query, result, kind=node.node_subtype)
            if new is not None:
                refreshed += 1
            else:
                # no live evidence remains; keep it out of trusted retrieval
                self.store.set_node_status(node.id, "review")
            if refreshed >= limit:
                break
        self.store.conn.commit()
        return refreshed

    # ----------------------------------------------------------- health

    def health(self) -> HealthReport:
        report = HealthReport()
        nodes = self.store.all_nodes()
        edges = self.store.all_edges()

        node_status = Counter(n.status for n in nodes)
        edge_status = Counter(e.status for e in edges)
        synth = [n for n in nodes if n.node_class == "synthetic"]

        report.metrics["nodes_total"] = len(nodes)
        report.metrics["nodes_active"] = node_status.get("active", 0)
        report.metrics["nodes_stale"] = node_status.get("stale", 0)
        report.metrics["edges_total"] = len(edges)
        report.metrics["edges_active"] = edge_status.get("active", 0)
        report.metrics["edges_stale"] = edge_status.get("stale", 0)
        report.metrics["edges_rejected"] = edge_status.get("rejected", 0)
        report.metrics["synthetic_total"] = len(synth)

        # edge-evidence coverage for active factual edges
        factual = [e for e in edges if e.status == "active" and e.type not in ("related",)]
        need_ev = [e for e in factual if e.type in ("contains", "has_topic", "supports", "mentions", "implements", "depends_on")]
        missing_ev = [e for e in need_ev if not e.has_evidence() and e.type != "supports"]
        report.metrics["active_factual_edges"] = len(factual)
        report.metrics["edges_missing_evidence"] = len(missing_ev)
        if missing_ev:
            report.lints.append(
                f"{len(missing_ev)} active factual edges lack source evidence"
            )

        # node-degree / hub concentration
        degree: Counter = Counter()
        for e in edges:
            if e.status != "active":
                continue
            degree[e.src_id] += 1
            degree[e.dst_id] += 1
        if degree:
            top = degree.most_common(1)[0]
            report.metrics["max_node_degree"] = top[1]
            total_deg = sum(degree.values())
            report.metrics["hub_concentration"] = round(top[1] / total_deg, 3)

        # document subgraphs with no external (cross-document) links
        report.lints.extend(self._lint_isolated_documents(nodes, edges))

        # synthetic dependency health
        for n in synth:
            if not n.metadata.get("absolute_dependencies"):
                report.lints.append(f"synthetic {n.id} has no absolute dependencies")
            if n.status == "stale":
                report.lints.append(f"synthetic {n.id} is stale (refresh on query/maintain)")

        # synthetic reuse / cache hit rate
        rows = self.store.conn.execute(
            "SELECT COALESCE(SUM(times_used),0) u, COUNT(*) c FROM query_cache"
        ).fetchone()
        report.metrics["query_cache_entries"] = rows["c"]
        report.metrics["query_cache_uses"] = rows["u"]

        return report

    def _lint_isolated_documents(self, nodes, edges) -> list[str]:
        node_doc = {n.id: n.document_id for n in nodes}
        docs = {n.document_id for n in nodes if n.document_id}
        external = {d: False for d in docs}
        for e in edges:
            if e.status != "active":
                continue
            sd, dd = node_doc.get(e.src_id), node_doc.get(e.dst_id)
            if sd and dd and sd != dd:
                external[sd] = True
                external[dd] = True
        out = []
        for d, has_ext in external.items():
            if not has_ext and d:
                out.append(f"document '{d}' has no cross-document links (isolated cluster)")
        return out


def run_maintenance(
    store: Store, policy: Policy, wiki_dir: Path | str, llm: Optional[LLMClient] = None
) -> HealthReport:
    m = Maintenance(store, policy, wiki_dir, llm)
    m.reindex()
    m.refresh_stale_synthetic()
    return m.health()
