"""End-to-end pipeline tests over a tiny synthetic compiled tree.

Runs without an LLM server: structural ingest, FTS search, traversal, synthetic
creation/reuse, source-update invalidation, and maintenance health are all
deterministic. Run: python -m graph.tests.test_pipeline
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from graph.ingest import Ingestor
from graph.maintenance import Maintenance
from graph.policy import DEFAULT_POLICY, Policy
from graph.query import QueryResult, QueryService, RetrievedNode
from graph.source_tree import CoverageError, read_compiled_document, validate_coverage
from graph.store import Store
from graph.synthetic import SyntheticManager


def _write_compiled_tree(root: Path, doc_name: str, pages, source_text: str):
    out = root / doc_name
    (out / "_planning").mkdir(parents=True, exist_ok=True)
    src_path = root / f"{doc_name}.md"
    src_path.write_text(source_text, encoding="utf-8")

    files = []
    assignments = []
    chunk_summaries = []
    for idx, (rel, title, summary, rng, topics) in enumerate(pages, 1):
        page_path = out / rel
        page_path.parent.mkdir(parents=True, exist_ok=True)
        fm = (
            "---\n"
            f'title: "{title}"\n'
            f'summary: "{summary}"\n'
            f"source_lines: [[{rng[0]}, {rng[1]}]]\n"
            "---\n\n"
            f"# {title}\n\n{summary}\n"
        )
        page_path.write_text(fm, encoding="utf-8")
        files.append(
            {
                "filename": rel,
                "title": title,
                "summary": summary,
                "source_ranges": [list(rng)],
            }
        )
        assignments.append({"source_start": rng[0], "source_end": rng[1], "file": rel})
        chunk_summaries.append(
            {
                "source_start": rng[0],
                "source_end": rng[1],
                "summary": summary,
                "topics": topics,
            }
        )

    line_count = max(r[3][1] for r in pages)
    manifest = {
        "source": str(src_path),
        "files": files,
        "planning": {"chunk_summaries": chunk_summaries},
        "coverage": {"exact_coverage": True},
    }
    (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (out / "_planning" / "coverage.json").write_text(
        json.dumps(
            {
                "source": str(src_path),
                "source_line_count": line_count,
                "exact_coverage": True,
                "assignments": assignments,
            }
        ),
        encoding="utf-8",
    )
    (out / "index.md").write_text("# index\n", encoding="utf-8")
    return out, src_path


def main() -> None:
    policy = Policy(dict(DEFAULT_POLICY))
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "output"
        wiki = Path(td) / ".wiki"
        root.mkdir(parents=True)

        # two documents that share a topic -> controlled cross-document link
        out_a, src_a = _write_compiled_tree(
            root,
            "gpu-guide",
            [
                (
                    "01-intro/001-setup.md",
                    "GPU Setup",
                    "Install drivers and toolkit.",
                    (1, 100),
                    ["gpu setup", "drivers"],
                ),
                (
                    "01-intro/002-env.md",
                    "GPU Environment",
                    "Configure environment variables.",
                    (101, 200),
                    ["environment variables", "gpu setup"],
                ),
            ],
            "\n".join(f"line {i}" for i in range(1, 201)),
        )
        _write_compiled_tree(
            root,
            "cpu-guide",
            [
                (
                    "01-intro/001-threads.md",
                    "CPU Threads",
                    "Set thread affinity.",
                    (1, 100),
                    ["gpu setup", "threads"],
                ),
            ],
            "\n".join(f"line {i}" for i in range(1, 101)),
        )

        store = Store(wiki / "catalog.sqlite")
        ing = Ingestor(store)
        done = ing.bootstrap(root)
        assert set(done) == {"gpu-guide", "cpu-guide"}, done

        # nodes built
        docs = [n for n in store.all_nodes() if n.node_subtype == "document"]
        pages = [n for n in store.all_nodes() if n.node_subtype == "source_page"]
        topics = [n for n in store.all_nodes() if n.node_subtype == "topic"]
        assert len(docs) == 2, len(docs)
        assert len(pages) == 3, len(pages)
        # shared "gpu setup" topic node is one global node, not per-doc
        gpu_topic = [t for t in topics if t.title == "gpu setup"]
        assert len(gpu_topic) == 1, gpu_topic

        # contains edges have evidence
        contains = [e for e in store.all_edges() if e.type == "contains"]
        assert contains and all(
            e.has_evidence() for e in contains
        ), "contains needs evidence"

        # cross-document link exists only via shared topic
        topic_edges = store.edges_to(gpu_topic[0].id)
        src_docs = {store.get_node(e.src_id).document_id for e in topic_edges}
        assert {"gpu-guide", "cpu-guide"} <= src_docs, src_docs

        # query + traversal
        qs = QueryService(store, policy)
        res = qs.query("gpu environment setup")
        assert res.nodes, "query returned nothing"
        assert res.citations, "expected citations"

        # A document-root seed cannot flood the context with every leaf page.
        root_result = qs.query("gpu guide")
        local_pages = [
            item
            for item in root_result.nodes
            if item.hop == 1 and item.node.node_subtype == "source_page"
        ]
        assert len(local_pages) <= policy.max_local_pages_from_document

        # synthetic create + reuse
        sm = SyntheticManager(store, policy, wiki)
        node = sm.create_or_refresh("gpu environment setup", res, kind="howto")
        assert node is not None and node.node_class == "synthetic"
        assert node.metadata["absolute_dependencies"], "must flatten deps"
        cached = sm.lookup("gpu environment setup")
        assert cached and cached.id == node.id, "synthetic should be reused"

        # Repeated ordinary queries are persisted and satisfy the auto-create
        # threshold, rather than requiring an explicit save every time.
        assert sm.should_create("recurring gpu setup") is False
        assert sm.should_create("recurring gpu setup") is True

        # A synthetic node seeded only from a canonical topic still receives a
        # source-version fingerprint through its supporting edge evidence.
        topic_result = QueryResult(
            query="topic-only gpu setup",
            nodes=[RetrievedNode(gpu_topic[0], score=1.0, hop=0)],
        )
        topic_synthetic = sm.create_or_refresh("topic-only gpu setup", topic_result)
        assert topic_synthetic is not None
        assert topic_synthetic.metadata["source_version_fingerprint"]

        # update gpu-guide source -> dependent synthetic nodes go stale
        src_a.write_text("CHANGED\n" + src_a.read_text(), encoding="utf-8")
        # rebuild manifest sha by re-reading; simulate edited page content
        doc2 = read_compiled_document(out_a)
        ing.ingest_document(doc2, created_by="ingest")
        refreshed = store.get_node(node.id)
        assert refreshed.status == "stale", refreshed.status
        assert store.get_node(topic_synthetic.id).status == "stale"

        # maintenance health runs and lints
        report = Maintenance(store, policy, wiki).health()
        assert report.metrics["nodes_total"] > 0
        assert "edges_missing_evidence" in report.metrics

        store.close()
    print("ALL PIPELINE TESTS PASSED")


def test_coverage_rejects_empty_nonempty_assignment() -> None:
    """The graph must never accept a nonempty document with no leaf ownership."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "_planning").mkdir()
        (root / "_planning" / "coverage.json").write_text(
            json.dumps(
                {
                    "exact_coverage": True,
                    "source_line_count": 10,
                    "assignments": [],
                }
            ),
            encoding="utf-8",
        )
        try:
            validate_coverage(root)
        except CoverageError:
            return
        raise AssertionError("empty assignments for a nonempty source were accepted")


if __name__ == "__main__":
    main()
    test_coverage_rejects_empty_nonempty_assignment()
