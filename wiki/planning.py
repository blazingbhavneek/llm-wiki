"""
Planning + rendering layer for the hierarchical wiki tree.
Imports from models: TopicRange, ChunkSummary.
Imports from utils: range_to_markdown, slugify, make_unique_filename,
append_markdown, yaml_quote, overlap_size, create_markdown_file,
add_or_update_file_record, add_chunk_record.
Imports from llm: structured_ainvoke (used by the partition retry loop).

Package `wiki/` — lossless Markdown wiki generator. Module layout
(low-level to high-level; imports only ever point downward in this list):

- models.py    Runtime config constants (SOURCE_PATH, OUTPUT_ROOT, BASE_URL,
               GEN_MODEL, GENERATION_LINES, ... PARTITION_RETRY_ATTEMPTS) and all
               Pydantic schemas + the CurrentFileState dataclass (FileRef,
               NewFileRef, GenerationDecision, VerificationResult, RepairResult,
               ChunkSummary, TopicRange, H1Plan, H1Layout, LeafPagePlan).
               No wiki imports.
- utils.py     Pure stdlib helpers: line-range/markdown (range_to_markdown,
               clamp_range_to_chunk, split_chunk_ranges), file/JSON IO
               (read_lines, write_json, load_json), filenames/slugs
               (slugify, make_unique_filename), source chunking
               (chunk_source_lines_preserving_tables, fixed_windows), manifest +
               markdown-file records (init_manifest, add_or_update_file_record,
               create_markdown_file, add_chunk_record,
               find_best_target_for_source_window, overlap_size),
               extract_json_from_text. No wiki imports.
- llm.py       LLM client: make_llm, structured_ainvoke (structured-output call
               with JSON fallback). Imports: utils.
- prompts.py   All prompt builders build_*_prompt (chunk summary, H1 plan, H1
               layout, leaf page, generation, verification, repair).
               Imports: models.
- planning.py  Hierarchy planning + tree rendering: chunk-summary ledger
               (format_summary_ledger, summaries_for_range), exact-partition
               validation (validate_exact_partition,
               structured_partition_ainvoke_with_retries, partition_or_fallback,
               assert_exact_coverage) and the wiki-tree writers
               (render_hierarchical_wiki, write_navigation_index,
               write_topic_plan_document, hierarchy_to_manifest,
               planned_leaf_pages). Imports: models, utils, llm.
- generate.py  Flat (non-hierarchical) generation phase: enforce_generation_rules,
               parse_part_number, forced_part_ref, phase_generate_flat.
               Imports: models, utils, prompts, llm.
- phases.py    Hierarchical generation (phase_generate), verification
               (verify_one_window, phase_verify), repair (phase_repair) and the
               batch runner / entrypoint (collect_source_files,
               make_config_for_source, process_one_source, async_main, main).
               Imports: generate, planning, prompts, utils, llm, models.

Entrypoint: ../md.py is a thin shim that calls wiki.phases.main.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from wiki.models import ChunkSummary, TopicRange
from wiki.utils import (
    add_chunk_record,
    add_or_update_file_record,
    append_markdown,
    create_markdown_file,
    make_unique_filename,
    overlap_size,
    range_to_markdown,
    slugify,
    yaml_quote,
)
from wiki.llm import structured_ainvoke

T = TypeVar("T", bound=BaseModel)


# ---------------------------------------------------------------------
# Hierarchical planning helpers
# ---------------------------------------------------------------------


def format_source_range(source_range: list[int]) -> str:
    return f"{source_range[0]}–{source_range[1]}"


def initialize_chunk_summary_document(path: Path, source_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Chunk summaries\n\nSource: `{source_path}`\n",
        encoding="utf-8",
    )


def append_chunk_summary_document(
    path: Path,
    source_start: int,
    source_end: int,
    summary: ChunkSummary,
) -> None:
    topics = ", ".join(summary.topics) or "(no distinct topic identified)"
    heading = summary.suggested_heading.strip() or "Untitled section"
    append_markdown(
        path,
        f"## Source lines {source_start}–{source_end}\n\n"
        f"- Suggested heading: {heading}\n"
        f"- Topics: {topics}\n"
        f"- Summary: {summary.summary.strip()}",
    )


def summaries_for_range(
    summaries: list[dict[str, Any]],
    source_start: int,
    source_end: int,
) -> list[dict[str, Any]]:
    return [
        record
        for record in summaries
        if overlap_size(
            source_start,
            source_end,
            int(record["source_start"]),
            int(record["source_end"]),
        )
        > 0
    ]


def format_summary_ledger(summaries: list[dict[str, Any]]) -> str:
    if not summaries:
        return "(No previous chunk summaries.)"

    entries = []
    for record in summaries:
        topics = ", ".join(record.get("topics", [])) or "no distinct topic"
        entries.append(
            f"- Lines {record['source_start']}–{record['source_end']}: "
            f"{record.get('summary', '').strip()} "
            f"Topics: {topics}."
        )
    return "\n".join(entries)


def allowed_chunk_ranges(
    summaries: list[dict[str, Any]],
    source_start: int,
    source_end: int,
) -> list[list[int]]:
    return [
        [int(record["source_start"]), int(record["source_end"])]
        for record in summaries_for_range(summaries, source_start, source_end)
    ]


def partition_or_fallback(
    topics: list[TopicRange],
    source_start: int,
    source_end: int,
    valid_chunk_ranges: list[list[int]],
    fallback_title: str,
    fallback_summary: str,
    label: str,
) -> list[TopicRange]:
    """Accept only an exact, chunk-aligned partition of a parent source range.

    Planning may degrade to one page if the model returns an invalid plan, but it
    must never produce a gap, an overlap, or a range that cannot be justified by
    the chunk summary ledger.
    """
    if source_start > source_end:
        return []

    allowed_starts = {item[0] for item in valid_chunk_ranges}
    allowed_ends = {item[1] for item in valid_chunk_ranges}
    expected_start = source_start
    accepted: list[TopicRange] = []

    for topic in topics:
        source_range = topic.source_range
        if (
            not source_range
            or len(source_range) != 2
            or source_range[0] != expected_start
            or source_range[0] not in allowed_starts
            or source_range[1] not in allowed_ends
            or source_range[1] < source_range[0]
            or source_range[1] > source_end
        ):
            accepted = []
            break

        accepted.append(
            TopicRange(
                title=topic.title.strip() or fallback_title,
                summary=topic.summary.strip() or fallback_summary,
                source_range=[int(source_range[0]), int(source_range[1])],
            )
        )
        expected_start = int(source_range[1]) + 1

    if accepted and expected_start == source_end + 1:
        return accepted

    print(
        f"[Planning] Invalid {label} partition for source lines "
        f"{source_start}-{source_end}; using one safe fallback range."
    )
    return [
        TopicRange(
            title=fallback_title,
            summary=fallback_summary,
            source_range=[source_start, source_end],
        )
    ]


def assert_exact_coverage(
    leaves: list[TopicRange],
    source_line_count: int,
) -> None:
    """Raise before rendering unless each source line belongs to one leaf page."""
    if source_line_count == 0:
        if leaves:
            raise RuntimeError("An empty source document cannot have leaf pages.")
        return

    expected_start = 1
    for leaf in leaves:
        source_range = leaf.source_range
        if not source_range or len(source_range) != 2:
            raise RuntimeError("Leaf page is missing its source range.")
        start, end = source_range
        if start != expected_start or end < start or end > source_line_count:
            raise RuntimeError(
                "Source coverage is not exact: expected next range to start at "
                f"{expected_start}, got {source_range}."
            )
        expected_start = end + 1

    if expected_start != source_line_count + 1:
        raise RuntimeError(
            "Source coverage is incomplete: expected coverage through line "
            f"{source_line_count}, stopped before line {expected_start}."
        )

def validate_exact_partition(
    topics: list[TopicRange],
    source_start: int,
    source_end: int,
    valid_chunk_ranges: list[list[int]],
    fallback_title: str,
    fallback_summary: str,
    label: str,
) -> tuple[list[TopicRange] | None, str | None]:
    """Validate that topics form an exact, chunk-aligned partition.

    Returns:
        (accepted_topics, None) if valid.
        (None, error_message) if invalid.
    """
    if source_start > source_end:
        return [], None

    allowed_starts = {item[0] for item in valid_chunk_ranges}
    allowed_ends = {item[1] for item in valid_chunk_ranges}

    expected_start = source_start
    accepted: list[TopicRange] = []

    if not topics:
        return (
            None,
            (
                f"{label} partition is empty, but it must cover source lines "
                f"{source_start}-{source_end}."
            ),
        )

    for index, topic in enumerate(topics, start=1):
        source_range = topic.source_range

        if not source_range or len(source_range) != 2:
            return (
                None,
                (
                    f"{label} item {index} has an invalid or missing source_range. "
                    f"Expected [start, end]."
                ),
            )

        item_start = int(source_range[0])
        item_end = int(source_range[1])

        if item_start != expected_start:
            return (
                None,
                (
                    f"{label} item {index} starts at line {item_start}, but expected "
                    f"line {expected_start}. This creates a gap or overlap."
                ),
            )

        if item_start not in allowed_starts:
            return (
                None,
                (
                    f"{label} item {index} starts at line {item_start}, which is not "
                    f"a valid chunk-aligned start. Allowed starts: "
                    f"{sorted(allowed_starts)}."
                ),
            )

        if item_end not in allowed_ends:
            return (
                None,
                (
                    f"{label} item {index} ends at line {item_end}, which is not "
                    f"a valid chunk-aligned end. Allowed ends: "
                    f"{sorted(allowed_ends)}."
                ),
            )

        if item_end < item_start:
            return (
                None,
                (
                    f"{label} item {index} has an invalid range "
                    f"{item_start}-{item_end}: end is before start."
                ),
            )

        if item_end > source_end:
            return (
                None,
                (
                    f"{label} item {index} ends at line {item_end}, but the parent "
                    f"range ends at line {source_end}."
                ),
            )

        accepted.append(
            TopicRange(
                title=topic.title.strip() or fallback_title,
                summary=topic.summary.strip() or fallback_summary,
                source_range=[item_start, item_end],
            )
        )

        expected_start = item_end + 1

    if expected_start != source_end + 1:
        return (
            None,
            (
                f"{label} partition ended at line {expected_start - 1}, but it must "
                f"cover through line {source_end}. Missing lines "
                f"{expected_start}-{source_end}."
            ),
        )

    return accepted, None

async def structured_partition_ainvoke_with_retries(
    llm: ChatOpenAI,
    schema_cls: type[T],
    base_messages: list[Any],
    extract_topics: Callable[[T], list[TopicRange]],
    source_start: int,
    source_end: int,
    valid_chunk_ranges: list[list[int]],
    fallback_title: str,
    fallback_summary: str,
    label: str,
    max_retries: int = 3,
) -> tuple[T, list[TopicRange]]:
    """Invoke the LLM until it returns an exact, chunk-aligned partition.

    Unlike the old fallback behavior, this asks the LLM to repair invalid plans.
    If all retries fail, it raises RuntimeError.
    """
    messages = list(base_messages)
    last_error: str | None = None

    for attempt in range(1, max_retries + 1):
        result = await structured_ainvoke(llm, schema_cls, messages)
        parsed = schema_cls.model_validate(result)

        topics = extract_topics(parsed)

        accepted, error = validate_exact_partition(
            topics=topics,
            source_start=source_start,
            source_end=source_end,
            valid_chunk_ranges=valid_chunk_ranges,
            fallback_title=fallback_title,
            fallback_summary=fallback_summary,
            label=label,
        )

        if accepted is not None:
            return parsed, accepted

        last_error = error

        print(
            f"[Planning] Invalid {label} partition attempt "
            f"{attempt}/{max_retries}: {error}"
        )

        messages.append(
            HumanMessage(
                content=(
                    "The previous plan was invalid and must be corrected.\n\n"
                    f"Validation error:\n{error}\n\n"
                    "What we are trying to do:\n"
                    f"- Create an exact partition of source lines {source_start}-{source_end}.\n"
                    "- Every line in that range must be covered exactly once.\n"
                    "- There must be no gaps.\n"
                    "- There must be no overlaps.\n"
                    "- Every range must be chunk-aligned.\n"
                    f"- Valid chunk ranges are: {valid_chunk_ranges}\n\n"
                    "Return a corrected plan using the same schema as before. "
                    "Do not skip any lines. Do not invent line numbers outside "
                    "the parent range."
                )
            )
        )

    raise RuntimeError(
        f"Unable to produce a valid {label} partition after {max_retries} attempts. "
        f"Last error: {last_error}"
    )

def write_navigation_index(
    path: Path,
    title: str,
    summary: str,
    children: list[dict[str, Any]],
    source_range: Optional[list[int]] = None,
) -> None:
    """Render an index page; indexes navigate source pages but do not own text."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"summary: {yaml_quote(summary)}",
        "generated: true",
        "---",
        "",
        f"# {title}",
        "",
    ]

    if summary:
        lines.extend([summary, ""])

    if source_range:
        lines.extend([f"Source coverage: lines {format_source_range(source_range)}.", ""])

    if children:
        lines.extend(["## Contents", ""])
        for child in children:
            relative_path = Path(
                os.path.relpath(Path(child["path"]), start=path.parent)
            ).as_posix()
            child_summary = child.get("summary", "").strip()
            range_text = format_source_range(child["source_range"])
            suffix = f" — {child_summary}" if child_summary else ""
            lines.append(
                f"- [{child['title']}]({relative_path}){suffix} "
                f"_(source lines {range_text})_"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def hierarchy_to_manifest(hierarchy: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "h1": node["h1"].model_dump(),
            "use_h2_folders": node["use_h2_folders"],
            "groups": [
                {
                    "topic": group["topic"].model_dump(),
                    "pages": [page.model_dump() for page in group["pages"]],
                }
                for group in node["groups"]
            ],
        }
        for node in hierarchy
    ]


def write_topic_plan_document(path: Path, hierarchy: list[dict[str, Any]]) -> None:
    lines = ["# Topic plan", ""]
    for node in hierarchy:
        h1 = node["h1"]
        lines.extend(
            [
                f"## {h1.title} — source lines {format_source_range(h1.source_range or [0, 0])}",
                "",
                h1.summary,
                "",
            ]
        )
        for group in node["groups"]:
            topic = group["topic"]
            if node["use_h2_folders"]:
                lines.extend(
                    [
                        f"### {topic.title} — source lines "
                        f"{format_source_range(topic.source_range or [0, 0])}",
                        "",
                    ]
                )
            for page in group["pages"]:
                lines.append(
                    f"- {page.title}: source lines "
                    f"{format_source_range(page.source_range or [0, 0])}"
                )
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def planned_leaf_pages(hierarchy: list[dict[str, Any]]) -> list[TopicRange]:
    return [
        page
        for node in hierarchy
        for group in node["groups"]
        for page in group["pages"]
    ]


def render_hierarchical_wiki(
    out_dir: Path,
    source_lines: list[str],
    manifest: dict[str, Any],
    hierarchy: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Create the wiki tree only after its leaf ranges passed exact coverage."""
    root_children: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []

    def render_page(directory: Path, page_number: int, page: TopicRange) -> dict[str, Any]:
        source_start, source_end = page.source_range or [0, 0]
        filename = make_unique_filename(directory, page_number, "", page.title)
        page_path = directory / filename
        create_markdown_file(
            path=page_path,
            title=page.title,
            summary=page.summary,
            source_start=source_start,
            source_end=source_end,
            body=range_to_markdown(source_lines, page.source_range),
        )

        relative_filename = page_path.relative_to(out_dir).as_posix()
        add_or_update_file_record(
            manifest,
            relative_filename,
            page.title,
            page.summary,
            source_start,
            source_end,
        )
        add_chunk_record(
            manifest=manifest,
            source_start=source_start,
            source_end=source_end,
            action="planned",
            targets=[
                {
                    "filename": relative_filename,
                    "source_start": source_start,
                    "source_end": source_end,
                }
            ],
            reason="Hierarchical plan leaf page.",
        )
        coverage.append(
            {
                "source_start": source_start,
                "source_end": source_end,
                "file": relative_filename,
            }
        )
        return {
            "title": page.title,
            "summary": page.summary,
            "source_range": [source_start, source_end],
            "path": page_path,
        }

    for h1_number, node in enumerate(hierarchy, start=1):
        h1 = node["h1"]
        h1_directory = out_dir / f"{h1_number:02d}-{slugify(h1.title)}"
        h1_children: list[dict[str, Any]] = []

        if node["use_h2_folders"]:
            for h2_number, group in enumerate(node["groups"], start=1):
                h2 = group["topic"]
                h2_directory = h1_directory / f"{h2_number:02d}-{slugify(h2.title)}"
                page_children = [
                    render_page(h2_directory, page_number, page)
                    for page_number, page in enumerate(group["pages"], start=1)
                ]
                h2_index = h2_directory / "index.md"
                write_navigation_index(
                    path=h2_index,
                    title=h2.title,
                    summary=h2.summary,
                    children=page_children,
                    source_range=h2.source_range,
                )
                h1_children.append(
                    {
                        "title": h2.title,
                        "summary": h2.summary,
                        "source_range": h2.source_range,
                        "path": h2_index,
                    }
                )
        else:
            direct_pages = node["groups"][0]["pages"]
            h1_children = [
                render_page(h1_directory, page_number, page)
                for page_number, page in enumerate(direct_pages, start=1)
            ]

        h1_index = h1_directory / "index.md"
        write_navigation_index(
            path=h1_index,
            title=h1.title,
            summary=h1.summary,
            children=h1_children,
            source_range=h1.source_range,
        )
        root_children.append(
            {
                "title": h1.title,
                "summary": h1.summary,
                "source_range": h1.source_range,
                "path": h1_index,
            }
        )

    write_navigation_index(
        path=out_dir / "index.md",
        title="Wiki index",
        summary="Generated guide index.",
        children=root_children,
    )
    return coverage
