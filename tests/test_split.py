from __future__ import annotations

import asyncio
import json
from pathlib import Path

from split import build_plans_for_source, process_source_file


def test_build_plans_split_large_h2_without_cutting_code_blocks() -> None:
    source_lines = [
        "# Demo",
        "intro line",
        "",
        "## Alpha",
        "alpha text 1",
        "```python",
        "print('a')",
        "print('b')",
        "```",
        "alpha text 2",
        "alpha text 3",
        "alpha text 4",
        "alpha text 5",
        "alpha text 6",
        "",
        "## Beta",
        "beta text",
    ]

    document_title, planned_sections = build_plans_for_source(
        source_lines=source_lines,
        source_path=Path("demo.md"),
        max_lines=8,
    )

    assert document_title == "Demo"

    plans = [item.plan for item in planned_sections]
    headers = [item.header for item in planned_sections]
    assert [(plan.source_start, plan.source_end) for plan in plans] == [
        (1, 3),
        (4, 9),
        (10, 15),
        (16, 17),
    ]
    assert headers == ["Demo", "Alpha", "Alpha", "Beta"]
    assert plans[1].title == "Alpha Part 1"
    assert plans[2].title == "Alpha Part 2"


def test_process_source_file_writes_expected_tree(tmp_path: Path) -> None:
    source_text = "\n".join(
        [
            "# Demo",
            "intro line",
            "",
            "## Alpha",
            "alpha text 1",
            "```python",
            "print('a')",
            "print('b')",
            "```",
            "alpha text 2",
            "alpha text 3",
            "alpha text 4",
            "alpha text 5",
            "alpha text 6",
            "",
            "## Beta",
            "beta text",
            "",
        ]
    )
    source_file = tmp_path / "input" / "demo.md"
    source_file.parent.mkdir(parents=True, exist_ok=True)
    source_file.write_text(source_text, encoding="utf-8")

    async def fake_summary(plan, source_lines):
        return f"Summary {plan.source_start}-{plan.source_end}"

    asyncio.run(
        process_source_file(
            source_file=source_file,
            output_root=tmp_path / "output",
            max_lines=8,
            clean=True,
            summary_provider=fake_summary,
        )
    )

    out_dir = tmp_path / "output" / "demo"
    docs_dir = out_dir / "docs"
    planning_dir = out_dir / "_planning"

    assert docs_dir.is_dir()
    assert planning_dir.is_dir()
    assert sorted(path.name for path in docs_dir.glob("*.md")) == [
        "001-introduction.md",
        "002-alpha-part-1.md",
        "003-alpha-part-2.md",
        "004-beta.md",
    ]
    assert (planning_dir / "concept-plan.md").is_file()
    assert (planning_dir / "coverage.json").is_file()
    assert (planning_dir / "metadata.json").is_file()

    coverage = json.loads((planning_dir / "coverage.json").read_text(encoding="utf-8"))
    metadata = json.loads((planning_dir / "metadata.json").read_text(encoding="utf-8"))

    assert coverage["file_count"] == 4
    assert coverage["files"][1]["summary"] == "Summary 4-9"
    assert coverage["files"][2]["header"] == "Alpha"
    assert metadata["original_file_name"] == "demo.md"
    assert metadata["inferred_file_name"] == "demo.md"
    assert metadata["files"] == [
        {"name": "introduction.md", "header": "Demo"},
        {"name": "alpha-part-1.md", "header": "Alpha"},
        {"name": "alpha-part-2.md", "header": "Alpha"},
        {"name": "beta.md", "header": "Beta"},
    ]
