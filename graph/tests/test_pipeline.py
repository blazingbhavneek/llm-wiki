"""Offline pipeline test: db / FTS5 / sqlite-vec / edges / query / health.

No network. Fakes injected for embeddings + LLM. Requires sqlite-vec installed.
Run: python -m pytest graph/tests/ -q
"""

from __future__ import annotations

import tempfile
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
