"""Offline pipeline test: db / FTS5 / sqlite-vec / edges / query / health.

No network. Fakes injected for embeddings + LLM. Requires sqlite-vec installed.
Run: python -m pytest graph/tests/ -q
"""

from __future__ import annotations

import tempfile
import json
from pathlib import Path

from ..config import Settings
from ..engine import DomainEngine
from ..ids import make_node_id
from ..models import Node, NodeType
from .fakes import FakeEmbedder, FakeLlm


def _engine() -> DomainEngine:
    tmp = Path(tempfile.mkdtemp()) / "wiki.sqlite"
    settings = Settings(database_path=str(tmp), edge_candidate_k=5, vector_query_k=10)
    return DomainEngine(settings, embedder=FakeEmbedder(), llm_client=FakeLlm())


def _node(body: str, doc: str = "test.md") -> Node:
    return Node(id=make_node_id(body, doc), body=body, type=NodeType.endogenous,
                original_document_name=doc)


def _md_output(root: Path, name: str, bodies: list[tuple[str, str]]) -> Path:
    out = root / name
    section = out / "01-manual"
    section.mkdir(parents=True)
    files = []
    for index, (title, body) in enumerate(bodies, start=1):
        filename = f"01-manual/{index:03d}-{title}.md"
        files.append({
            "filename": filename,
            "title": title,
            "summary": title,
            "source_ranges": [[index, index]],
        })
        (out / filename).write_text(
            f"---\ntitle: {title}\n---\n{body}\n",
            encoding="utf-8",
        )
    (out / "manifest.json").write_text(
        json.dumps({"source": "/missing/manual.md", "files": files}),
        encoding="utf-8",
    )
    return out


def test_ingest_query_edges_health() -> None:
    eng = _engine()
    try:
        a = _node("SYCL device selection on GPU using dpcpp compiler queue")
        b = _node("GPU queue submission with SYCL kernels and device memory")
        c = _node("Cooking pasta requires boiling water and salt")
        for n in (a, b, c):
            eng.ingest(n)

        # keyword search (FTS5)
        kw = eng.query("keyword", "GPU SYCL")
        kw_ids = {n.id for n in kw.nodes}
        assert a.id in kw_ids and b.id in kw_ids
        assert c.id not in kw_ids

        # vector search (sqlite-vec) — gpu nodes rank above pasta
        vec = eng.query("vector", "run a kernel on the GPU device")
        assert vec.nodes, "vector search returned nothing"
        top_ids = {n.id for n in vec.nodes[:2]}
        assert a.id in top_ids or b.id in top_ids

        # semantic edges: a<->b share keywords; pasta isolated
        _, edges = eng.get()
        linked = {(e.source_node_id, e.target_node_id) for e in edges}
        assert (a.id, b.id) in linked or (b.id, a.id) in linked

        # id query returns node + its edges
        idq = eng.query("id", a.id)
        assert idq.nodes and idq.nodes[0].id == a.id

        # health metrics are real numbers
        h = eng.health()
        assert h.total_nodes == 3
        assert h.endogenous_nodes == 3
        assert h.avg_degree >= 0.0
        assert 0.0 <= h.density <= 1.0
        assert h.isolated_nodes >= 1  # pasta node
    finally:
        eng.close()


def test_delete_and_recon() -> None:
    eng = _engine()
    try:
        n = _node("oneAPI environment setup with setvars script")
        eng.ingest(n)
        eng.delete(n.id)
        assert eng.query("id", n.id).nodes == []

        src = Path(tempfile.mkdtemp()) / "doc.md"
        src.write_text("# title\nbody text", encoding="utf-8")
        assert eng.recon(src)["status"] == "new"
    finally:
        eng.close()


def test_cascading_update_supersedes_changed_source_node() -> None:
    eng = _engine()
    root = Path(tempfile.mkdtemp())
    try:
        v1 = _md_output(root, "v1", [
            ("omega", "omegaapi takes parameter alpha.\nomegaapi returns int."),
            ("setup", "setupguide uses a config file."),
        ])
        eng.ingest_md_output(v1)

        old_omega = next(
            n for n in eng.database.get_nodes_by_document("manual.md", active_only=True)
            if "alpha" in n.body
        )
        exo1 = eng.create_exogenous_node(
            "agent note: call omegaapi with alpha",
            [old_omega.id],
            origin="agent-1",
        )
        exo2 = eng.create_exogenous_node(
            "higher level note based on agent note",
            [exo1.id],
            origin="agent-2",
        )

        v2 = _md_output(root, "v2", [
            ("omega", "omegaapi takes parameter beta.\nomegaapi returns int."),
            ("setup", "setupguide uses a config file."),
        ])
        actions = eng.cascading_update(v2)

        assert any(a.startswith(f"superseded:{old_omega.id}->") for a in actions)
        assert eng.database.get_node(old_omega.id).status.value == "superseded"
        assert eng.database.get_node(exo1.id).status.value == "superseded"
        assert eng.database.get_node(exo2.id).status.value == "superseded"
        assert any(a.startswith(f"regenerated-exogenous:{exo1.id}->") for a in actions)
        assert any(a.startswith(f"regenerated-exogenous:{exo2.id}->") for a in actions)

        active = eng.database.get_nodes_by_document("manual.md", active_only=True)
        assert any("beta" in n.body for n in active)
        assert any("setupguide" in n.body for n in active)
        active_exo = [n for n in eng.database.get_all_nodes() if n.type == NodeType.exogenous and n.status.value == "active"]
        assert any("beta" in n.body for n in active_exo)

        edges = eng.database.get_edges_for_node(old_omega.id)
        assert any(e.label == "superseded_by" for e in edges)

        second = eng.cascading_update(v2)
        assert not any(a.startswith(("superseded:", "new:", "stale:")) for a in second)
    finally:
        eng.close()


def test_cascading_update_stales_exogenous_with_removed_support() -> None:
    eng = _engine()
    root = Path(tempfile.mkdtemp())
    try:
        v1 = _md_output(root, "v1", [
            ("omega", "omegaapi takes parameter alpha."),
            ("setup", "setupguide uses a config file."),
        ])
        eng.ingest_md_output(v1)
        old_omega = next(
            n for n in eng.database.get_nodes_by_document("manual.md", active_only=True)
            if "omegaapi" in n.body
        )
        exo = eng.create_exogenous_node(
            "agent note: omegaapi exists",
            [old_omega.id],
            origin="removed-support-agent",
        )

        v2 = _md_output(root, "v2", [
            ("setup", "setupguide uses a config file."),
        ])
        actions = eng.cascading_update(v2)

        assert any(a == f"stale:{old_omega.id}" for a in actions)
        assert any(a == f"stale-exogenous:{exo.id}" for a in actions)
        assert eng.database.get_node(exo.id).status.value == "stale"
    finally:
        eng.close()


def test_cascading_update_reorder_does_not_supersede() -> None:
    eng = _engine()
    root = Path(tempfile.mkdtemp())
    try:
        first = "alphaapi defines a queue.\nalphaapi submits work."
        second = "betaconfig controls the runtime.\nbetaconfig sets timeout."
        v1 = _md_output(root, "v1", [("alpha", first), ("beta", second)])
        eng.ingest_md_output(v1)

        v2 = _md_output(root, "v2", [("beta", second), ("alpha", first)])
        actions = eng.cascading_update(v2)

        assert all(not a.startswith("superseded:") for a in actions)
        assert all(not a.startswith("new:") for a in actions)
        nodes = eng.database.get_nodes_by_document("manual.md")
        assert all(n.status.value == "active" for n in nodes)
    finally:
        eng.close()
