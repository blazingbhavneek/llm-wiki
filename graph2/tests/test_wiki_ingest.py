from __future__ import annotations

import json
from pathlib import Path

from ..md_ingest import MarkdownIngest


def test_load_output_wiki_layout(tmp_path: Path) -> None:
    root = tmp_path / "output_wiki"
    raw = root / "raw" / "cuda-guide"
    concepts = root / "concepts"
    indexes = root / "indexes"
    planning = root / "_planning"

    raw.mkdir(parents=True)
    concepts.mkdir(parents=True)
    indexes.mkdir(parents=True)
    planning.mkdir(parents=True)

    (raw / "original.md").write_text(
        "# CUDA Guide\n"
        "Memory is allocated on device.\n"
        "Streams overlap copies with kernels.\n",
        encoding="utf-8",
    )
    (raw / "coverage.json").write_text(
        json.dumps({"source_line_count": 3, "file_count": 1}),
        encoding="utf-8",
    )
    (raw / "metadata.json").write_text(
        json.dumps({"original_file_name": "cuda-guide.md"}),
        encoding="utf-8",
    )
    (concepts / "cuda-memory.md").write_text(
        "# CUDA Memory\n\n"
        "CUDA device memory allocation is covered by [cuda-guide:L1-L2].\n",
        encoding="utf-8",
    )
    (indexes / "home.md").write_text(
        "# Global Wiki\n\n"
        "- [CUDA Memory](../concepts/cuda-memory.md)\n",
        encoding="utf-8",
    )
    (planning / "page_metadata.json").write_text(
        json.dumps(
            {
                "pages": {
                    "concept/cuda-memory": {
                        "title": "CUDA Memory",
                        "summary": "Source-backed CUDA memory notes.",
                        "aliases": ["device memory"],
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    nodes, edges = MarkdownIngest().load_md_output(root)

    by_title = {node.title: node for node in nodes}
    assert "Source Document: cuda-guide.md" in by_title
    assert "CUDA Memory" in by_title

    source = by_title["Source Document: cuda-guide.md"]
    page = by_title["CUDA Memory"]
    assert source.original_document_name == "global_wiki"
    assert page.original_document_name == "global_wiki"
    assert page.source_ranges == [(1, 2)]
    assert "Graph Source References" in page.body
    assert page.keywords[:2] == ["concept/cuda-memory", "concept"]

    labels = {edge.label for edge in edges}
    assert "wiki_cites_source" in labels
    assert "source_supports_wiki" in labels
    assert "wiki_links_to" in labels
