from __future__ import annotations

import asyncio
from pathlib import Path

from wiki_new.planning import (
    _apply_section_judge_decision,
    ConceptFilePlan,
    build_concept_split_prompt,
    build_streaming_boundary_judge_prompt,
    judge_concept_plan,
    plan_concept_files_streaming,
    render_concept_files,
    validate_concept_partition,
)


def test_validate_concept_partition_preserves_model_ranges_without_manual_merge() -> None:
    source_lines = [
        "## Contents",
        "1 Overview .... 2",
        "1.1 Scope .... 3",
        "1.2 Memory Model .... 7",
        "2 Runtime Library .... 10",
        "3 Glossary .... 20",
        "4 References .... 30",
        "5 Appendix .... 40",
        "6 Index .... 50",
        "7 Examples .... 60",
        "8 Notes .... 70",
        "9 Revision History .... 80",
    ]

    accepted, error = validate_concept_partition(
        files=[
            ConceptFilePlan(
                title="Contents Part 1",
                filename="contents-part1.md",
                source_start=1,
                source_end=6,
                summary="",
            ),
            ConceptFilePlan(
                title="Contents Part 2",
                filename="contents-part2.md",
                source_start=7,
                source_end=12,
                summary="",
            ),
        ],
        source_lines=source_lines,
        source_start=1,
        source_end=12,
        label="test",
    )

    assert error is None
    assert accepted is not None
    assert [(item.source_start, item.source_end) for item in accepted] == [
        (1, 6),
        (7, 12),
    ]


def test_validate_concept_partition_preserves_small_ranges_without_manual_merge() -> None:
    source_lines = [
        "9 CUDA-Enabled GPUs 157",
        "10 C++ Language Extensions 159",
        "10.1 Function Execution Space Specifiers 159",
        "10.1.1 __global__ 159",
    ]

    accepted, error = validate_concept_partition(
        files=[
            ConceptFilePlan(
                title="GPUs",
                filename="gpus.md",
                source_start=1,
                source_end=1,
                summary="",
            ),
            ConceptFilePlan(
                title="Extensions",
                filename="extensions.md",
                source_start=2,
                source_end=4,
                summary="",
            ),
        ],
        source_lines=source_lines,
        source_start=1,
        source_end=4,
        label="test",
    )

    assert error is None
    assert accepted is not None
    assert [(item.source_start, item.source_end) for item in accepted] == [
        (1, 1),
        (2, 4),
    ]


def test_apply_section_judge_decision_adjusts_boundary_with_previous() -> None:
    files = [
        ConceptFilePlan(
            title="Intro",
            filename="intro.md",
            source_start=1,
            source_end=3,
            summary="",
        ),
        ConceptFilePlan(
            title="Next",
            filename="next.md",
            source_start=4,
            source_end=5,
            summary="",
        ),
    ]

    revised, applied = _apply_section_judge_decision(
        files,
        target_index=1,
        action="adjust_boundary_with_previous",
        new_boundary_line=3,
    )

    assert applied is True
    assert [(item.source_start, item.source_end) for item in revised] == [
        (1, 2),
        (3, 5),
    ]


def test_validate_concept_partition_keeps_distinct_prose_sections() -> None:
    source_lines = [
        "## Memory Model",
        "The OpenMP API provides a relaxed consistency memory model with shared state across threads and devices.",
        "Each thread may observe updates at different times until synchronization occurs between participating threads.",
        "These guarantees define when reads and writes become visible to other execution agents in the program.",
        "## Data Environment",
        "A construct that creates a data environment establishes new rules for how variables are shared or privatized.",
        "The original variable and any private copies have defined relationships that depend on the directive and clauses.",
        "These rules are part of the executable semantics rather than navigation or front-matter metadata.",
    ]

    accepted, error = validate_concept_partition(
        files=[
            ConceptFilePlan(
                title="Memory Model",
                filename="memory-model.md",
                source_start=1,
                source_end=4,
                summary="",
            ),
            ConceptFilePlan(
                title="Data Environment",
                filename="data-environment.md",
                source_start=5,
                source_end=8,
                summary="",
            ),
        ],
        source_lines=source_lines,
        source_start=1,
        source_end=8,
        label="test",
    )

    assert error is None
    assert accepted is not None
    assert [(item.source_start, item.source_end) for item in accepted] == [
        (1, 4),
        (5, 8),
    ]


def test_validate_concept_partition_preserves_large_ranges_without_manual_merge() -> None:
    source_lines = [
        "10 C++ Language Extensions 159",
        "10.1 Function Execution Space Specifiers 159",
        "10.1.1 __global__ 159",
        "10.1.2 __device__ 160",
        "10.1.3 __host__ 160",
        "10.2 Variable Memory Space Specifiers 161",
        "10.2.1 __device__ 161",
        "10.2.2 __constant__ 162",
        "10.8 Texture Functions 172",
        "10.8.1 Texture Object API 172",
        "10.8.1.1 tex1Dfetch() 172",
        "10.8.1.2 tex1D() 172",
        "10.14 Atomic Functions 184",
        "10.14.1 Arithmetic Functions 187",
        "10.14.1.1 atomicAdd() 187",
        "10.14.1.2 atomicSub() 188",
    ]

    accepted, error = validate_concept_partition(
        files=[
            ConceptFilePlan(
                title="Extensions Part 1",
                filename="extensions-part1.md",
                source_start=1,
                source_end=8,
                summary="",
            ),
            ConceptFilePlan(
                title="Extensions Part 2",
                filename="extensions-part2.md",
                source_start=9,
                source_end=16,
                summary="",
            ),
        ],
        source_lines=source_lines,
        source_start=1,
        source_end=16,
        label="test",
    )

    assert error is None
    assert accepted is not None
    assert [(item.source_start, item.source_end) for item in accepted] == [
        (1, 8),
        (9, 16),
    ]


def test_render_concept_files_replaces_existing_docs(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "001-stale.md").write_text("stale\n", encoding="utf-8")
    (docs_dir / "002-other.md").write_text("stale\n", encoding="utf-8")

    coverage = render_concept_files(
        docs_dir=docs_dir,
        source_lines=["alpha", "beta", "gamma", "delta"],
        files=[
            ConceptFilePlan(
                title="Alpha",
                filename="alpha.md",
                source_start=1,
                source_end=2,
                summary="",
            ),
            ConceptFilePlan(
                title="Gamma",
                filename="gamma.md",
                source_start=3,
                source_end=4,
                summary="",
            ),
        ],
        manifest={"files": [], "chunks": []},
        output_root=tmp_path,
    )

    assert [item["filename"] for item in coverage] == [
        "docs/001-alpha.md",
        "docs/002-gamma.md",
    ]
    assert sorted(path.name for path in docs_dir.glob("*.md")) == [
        "001-alpha.md",
        "002-gamma.md",
    ]


def test_build_concept_split_prompt_targets_logical_sections() -> None:
    messages = build_concept_split_prompt(
        source_start=1,
        source_end=10,
        source_block="1 | demo",
        pending=None,
        last_error=None,
    )

    system_text = messages[0].content
    user_text = messages[1].content

    assert "logical reader-facing document sections" in system_text
    assert "Do NOT atomize the document into every possible concept" in system_text
    assert "500-700 lines should be rare" in user_text
    assert "Do NOT create continuation pages merely because a chunk boundary was reached" in user_text
    assert "Boundary hygiene matters" not in user_text


def test_judge_prompt_mentions_boundary_hygiene() -> None:
    from wiki_new.planning import build_section_judge_prompt

    files = [
        ConceptFilePlan(
            title="Intro",
            filename="intro.md",
            source_start=1,
            source_end=3,
            summary="",
        ),
        ConceptFilePlan(
            title="Next",
            filename="next.md",
            source_start=4,
            source_end=5,
            summary="",
        ),
    ]
    source_lines = [
        "intro paragraph",
        "more intro",
        "## Next Section",
        "next body line 1",
        "next body line 2",
    ]

    messages = build_section_judge_prompt(
        files=files,
        source_lines=source_lines,
        target_index=1,
    )

    assert "boundary should be pristine" in messages[0].content
    assert "Boundary hygiene matters" in messages[1].content
    assert "adjust_boundary_with_previous" in messages[1].content
    assert "Return only the final decision" in messages[1].content


def test_streaming_boundary_judge_prompt_mentions_next_raw_lines() -> None:
    previous = ConceptFilePlan(
        title="Front Matter",
        filename="front-matter.md",
        source_start=1,
        source_end=3,
        summary="",
    )
    target = ConceptFilePlan(
        title="Contents",
        filename="contents.md",
        source_start=4,
        source_end=6,
        summary="",
    )
    source_lines = [
        "preface",
        "copyright",
        "blank",
        "## Contents",
        "1 Overview .... 2",
        "2 API .... 9",
        "## Chapter 1",
        "Body line 1",
        "Body line 2",
    ]

    messages = build_streaming_boundary_judge_prompt(
        previous=previous,
        target=target,
        source_lines=source_lines,
        lookahead_lines=3,
        target_is_provisional_tail=True,
    )

    assert "NEXT 3 RAW SOURCE LINES" in messages[1].content
    assert "first-pass streaming check" in messages[1].content
    assert "merge_into_previous" in messages[1].content
    assert "carry-over tail" in messages[1].content
    assert "clear new chapter or major section later in its own range" in messages[1].content
    assert "merged_line_count" in messages[1].content


def test_judge_concept_plan_merges_tiny_section_with_neighbors(monkeypatch) -> None:
    async def fake_structured_ainvoke(llm, schema_cls, messages, max_output_tokens=None):
        return schema_cls(action="merge_previous_target_next", reason="too small")

    monkeypatch.setattr(
        "wiki_new.planning.structured_ainvoke",
        fake_structured_ainvoke,
    )

    files = [
        ConceptFilePlan(
            title="Front Matter",
            filename="front-matter.md",
            source_start=1,
            source_end=4,
            summary="",
        ),
        ConceptFilePlan(
            title="Tiny Bridge",
            filename="tiny-bridge.md",
            source_start=5,
            source_end=5,
            summary="",
        ),
        ConceptFilePlan(
            title="Outline",
            filename="outline.md",
            source_start=6,
            source_end=8,
            summary="",
        ),
    ]
    source_lines = [
        "## Contents",
        "1 Overview .... 2",
        "2 Intro .... 5",
        "3 API .... 9",
        "4 GPUs .... 11",
        "10 C++ Language Extensions 159",
        "10.1 Function Execution Space Specifiers 159",
        "10.1.1 __global__ 159",
    ]

    judged = asyncio.run(
        judge_concept_plan(
            llm=object(),
            source_lines=source_lines,
            files=files,
        )
    )

    assert [(item.source_start, item.source_end) for item in judged] == [(1, 8)]


def test_judge_concept_plan_can_adjust_boundary(monkeypatch) -> None:
    calls = {"count": 0}

    async def fake_structured_ainvoke(llm, schema_cls, messages, max_output_tokens=None):
        calls["count"] += 1
        if calls["count"] == 2:
            return schema_cls(
                action="adjust_boundary_with_previous",
                new_boundary_line=3,
                reason="heading belongs with next section",
            )
        return schema_cls(action="keep", reason="done")

    monkeypatch.setattr(
        "wiki_new.planning.structured_ainvoke",
        fake_structured_ainvoke,
    )

    files = [
        ConceptFilePlan(
            title="Intro",
            filename="intro.md",
            source_start=1,
            source_end=3,
            summary="",
        ),
        ConceptFilePlan(
            title="Next",
            filename="next.md",
            source_start=4,
            source_end=5,
            summary="",
        ),
    ]
    source_lines = [
        "intro paragraph",
        "more intro",
        "## Next Section",
        "next body line 1",
        "next body line 2",
    ]

    judged = asyncio.run(
        judge_concept_plan(
            llm=object(),
            source_lines=source_lines,
            files=files,
        )
    )

    assert [(item.source_start, item.source_end) for item in judged] == [
        (1, 2),
        (3, 5),
    ]


def test_plan_concept_files_streaming_runs_local_judge_before_commit(monkeypatch) -> None:
    source_lines = [f"line {index}" for index in range(1, 9)]
    committed_ranges: list[list[tuple[int, int]]] = []
    judge_calls: list[list[tuple[int, int]]] = []

    monkeypatch.setattr(
        "wiki_new.planning.chunk_source_lines_preserving_tables",
        lambda source_lines, target_size, max_extra: [(0, 5), (5, 8)],
    )

    async def fake_split_window_until_valid(
        *,
        llm,
        source_lines,
        source_start,
        source_end,
        display_start,
        pending,
        label,
        max_output_tokens=3000,
    ):
        del llm, source_lines, display_start, max_output_tokens
        if label == "chunk 1/2":
            assert pending is None
            assert (source_start, source_end) == (1, 5)
            return [
                ConceptFilePlan(
                    title="TOC Part 1",
                    filename="toc-part-1.md",
                    source_start=1,
                    source_end=2,
                    summary="",
                ),
                ConceptFilePlan(
                    title="TOC Part 2",
                    filename="toc-part-2.md",
                    source_start=3,
                    source_end=5,
                    summary="",
                ),
            ]

        assert label == "chunk 2/2"
        assert pending is not None
        assert (source_start, source_end) == (1, 8)
        return [
            ConceptFilePlan(
                title="Front Matter and Intro",
                filename="front-matter-and-intro.md",
                source_start=1,
                source_end=8,
                summary="",
            ),
        ]

    async def fake_judge_streaming_boundaries_once(
        *,
        llm,
        source_lines,
        files,
        max_output_tokens=200,
        lookahead_lines=100,
        provisional_last_section=False,
        label=None,
    ):
        del llm, source_lines, max_output_tokens, lookahead_lines
        judge_calls.append([(item.source_start, item.source_end) for item in files])
        assert label == "chunk 1/2 streaming"
        assert provisional_last_section is True
        return [
            ConceptFilePlan(
                title="Front Matter",
                filename="front-matter.md",
                source_start=1,
                source_end=5,
                summary="",
            ),
        ]

    monkeypatch.setattr(
        "wiki_new.planning.split_window_until_valid",
        fake_split_window_until_valid,
    )
    monkeypatch.setattr(
        "wiki_new.planning.judge_streaming_boundaries_once",
        fake_judge_streaming_boundaries_once,
    )

    def on_commit(items) -> None:
        committed_ranges.append([(item.source_start, item.source_end) for item in items])

    planned = asyncio.run(
        plan_concept_files_streaming(
            llm=object(),
            judge_llm=object(),
            source_lines=source_lines,
            target_lines=5,
            max_extra=0,
            on_commit=on_commit,
        )
    )

    assert judge_calls == [[(1, 2), (3, 5)]]
    assert committed_ranges == [[(1, 8)]]
    assert [(item.source_start, item.source_end) for item in planned] == [(1, 8)]
