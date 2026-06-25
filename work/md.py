#!/usr/bin/env python3

"""
Markdown Wiki Maker

Implements:
1. Sequential Generation
2. Parallel Verification
3. Repair Pass

Designed for a local OpenAI-compatible LLM server.

Example:

python wiki_maker.py 
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional
from types import SimpleNamespace
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------
# Runtime config
# ---------------------------------------------------------------------

SOURCE_PATH = "/home/seigyo/llm-wiki/input/"
OUTPUT_ROOT = "/home/seigyo/llm-wiki/output/"

PHASE = "all"  # all | generate | generate-flat | verify | repair

BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://10.160.144.101:51021/v1")
API_KEY = os.environ.get("OPENAI_API_KEY", "local")

GEN_MODEL = "openai/gpt-oss-120b"
VERIFY_MODEL = "openai/gpt-oss-120b"

GENERATION_LINES = 500
VERIFICATION_LINES = 25
MAX_CHUNK_EXTRA = 50

# Concurrency inside verification for one file.
CONCURRENCY = 20

# Number of input markdown files processed at the same time.
FILE_CONCURRENCY = 5

TEMPERATURE = 0.3
TIMEOUT = 300

CLEAN_OUTPUT = True

PARTITION_RETRY_ATTEMPTS = 3

# ---------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------


class FileRef(BaseModel):
    title: str = ""
    filename: str = ""


class NewFileRef(BaseModel):
    title: str = ""
    filename: str = ""
    summary: str = ""


class GenerationDecision(BaseModel):
    action: Literal["append", "new", "split", "ignore"]
    current_file: FileRef = Field(default_factory=FileRef)
    new_file: NewFileRef = Field(default_factory=NewFileRef)

    # Inclusive source line ranges, using real source line numbers shown to the LLM.
    # Example: [101, 150]
    current_source_range: Optional[list[int]] = None
    new_source_range: Optional[list[int]] = None

    reason: str = ""

class VerificationResult(BaseModel):
    answer: Literal["YES", "NO"]
    missing_facts: list[str] = Field(default_factory=list)
    hallucinations: list[str] = Field(default_factory=list)
    reason: str = ""


class RepairResult(BaseModel):
    markdown_patch: str = ""
    reason: str = ""


class ChunkSummary(BaseModel):
    """A factual description of one source chunk; it never owns source text."""

    summary: str = ""
    topics: list[str] = Field(default_factory=list)
    suggested_heading: str = ""


class TopicRange(BaseModel):
    """A named, contiguous source range used at one level of the wiki tree."""

    title: str = ""
    summary: str = ""
    source_range: Optional[list[int]] = None


class H1Plan(BaseModel):
    sections: list[TopicRange] = Field(default_factory=list)


class H1Layout(BaseModel):
    """Sections are H2 folders when use_h2_folders is true, otherwise leaf pages."""

    use_h2_folders: bool = False
    sections: list[TopicRange] = Field(default_factory=list)


class LeafPagePlan(BaseModel):
    pages: list[TopicRange] = Field(default_factory=list)


@dataclass
class CurrentFileState:
    title: str
    filename: str
    summary: str
    line_count: int


# ---------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------

def range_to_markdown(
    source_lines: list[str],
    source_range: Optional[list[int]],
) -> str:
    """
    Convert an inclusive 1-based source range [start, end] to raw Markdown.

    Important:
    - Uses original source lines.
    - Does NOT include line number prefixes.
    """
    if not source_range or len(source_range) != 2:
        return ""

    start, end = int(source_range[0]), int(source_range[1])

    if start > end:
        return ""

    # Convert 1-based inclusive to Python slice.
    return "\n".join(source_lines[start - 1 : end])


def clamp_range_to_chunk(
    source_range: Optional[list[int]],
    chunk_start: int,
    chunk_end: int,
) -> Optional[list[int]]:
    """
    Clamp an LLM-provided inclusive source range to the current chunk.
    """
    if not source_range or len(source_range) != 2:
        return None

    start, end = int(source_range[0]), int(source_range[1])

    start = max(start, chunk_start)
    end = min(end, chunk_end)

    if start > end:
        return None

    return [start, end]


def full_chunk_range(source_start: int, source_end: int) -> list[int]:
    return [source_start, source_end]


def split_chunk_ranges(source_start: int, source_end: int) -> tuple[list[int], list[int]]:
    midpoint = source_start + ((source_end - source_start) // 2)
    return [source_start, midpoint], [midpoint + 1, source_end]

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def count_file_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8").splitlines())


def ensure_md_suffix(filename: str) -> str:
    filename = filename.strip()
    if not filename.endswith(".md"):
        filename += ".md"
    return filename


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s.-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-.")
    return text or "untitled"


def clean_filename_hint(filename: str, title: str) -> str:
    filename = filename.strip()
    if filename:
        stem = Path(filename).stem
    else:
        stem = title

    stem = re.sub(r"^\d{3,}-", "", stem)
    stem = slugify(stem)

    return ensure_md_suffix(stem)


def make_numbered_filename(index: int, filename_hint: str, title: str) -> str:
    clean = clean_filename_hint(filename_hint, title)
    stem = Path(clean).stem
    return f"{index:03d}-{stem}.md"


def get_next_file_index(out_dir: Path) -> int:
    max_index = 0
    for path in out_dir.glob("*.md"):
        match = re.match(r"^(\d{3,})-", path.name)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def make_unique_filename(out_dir: Path, index: int, filename_hint: str, title: str) -> str:
    filename = make_numbered_filename(index, filename_hint, title)
    path = out_dir / filename

    if not path.exists():
        return filename

    stem = Path(filename).stem
    suffix = Path(filename).suffix

    counter = 2
    while True:
        candidate = f"{stem}-{counter}{suffix}"
        if not (out_dir / candidate).exists():
            return candidate
        counter += 1


def append_markdown(path: Path, markdown: str) -> int:
    markdown = markdown.strip()
    if not markdown:
        return 0

    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    path.write_text(existing + separator + markdown + "\n", encoding="utf-8")

    return len(markdown.splitlines())


def numbered_source_lines(lines: list[str], start_line_number: int) -> str:
    cleaned_lines = []
    for line in lines:
        # Strip base64 data from img tags before sending to the LLM
        if "data:image/" in line:
            line = re.sub(r'src=["\']data:image/[^"\']+["\']', 'src=""', line)
        cleaned_lines.append(line)
        
    return "\n".join(
        f"{start_line_number + i}: {line}" for i, line in enumerate(cleaned_lines)
    )


def last_n_lines_from_file(path: Path, n: int = 100) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[-n:])


def extract_json_from_text(text: str) -> Any:
    """
    Fallback parser for models that return JSON wrapped in prose or fences.
    """

    text = text.strip()

    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    first = text.find("{")
    last = text.rfind("}")

    if first != -1 and last != -1 and last > first:
        return json.loads(text[first : last + 1])

    raise ValueError("Could not extract valid JSON from LLM response.")


# ---------------------------------------------------------------------
# Markdown chunking
# ---------------------------------------------------------------------


def is_fence_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def is_tableish_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False

    if stripped.startswith("|") and "|" in stripped[1:]:
        return True

    if re.match(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", stripped):
        return True

    return False


def chunk_source_lines_preserving_tables(
    lines: list[str],
    target_size: int = 100,
    max_extra: int = 30,
) -> list[tuple[int, int]]:
    """
    Returns zero-based half-open ranges: [(start, end), ...]

    Tries to avoid cutting inside fenced code blocks, Markdown tables,
    and <image-unit> blocks.
    """

    chunks: list[tuple[int, int]] = []
    n = len(lines)
    start = 0

    # Precompute states to correctly handle blocks spanning across chunk boundaries
    fence_state = []
    in_f = False
    for line in lines:
        if is_fence_line(line):
            in_f = not in_f
        fence_state.append(in_f)

    img_state = []
    in_i = False
    for line in lines:
        if "<image-unit>" in line:
            in_i = True
        if "</image-unit>" in line:
            in_i = False
        img_state.append(in_i)

    while start < n:
        end = min(start + target_size, n)

        extra = 0

        while end < n and extra < max_extra:
            cut_inside_table = (
                end > start
                and (
                    is_tableish_line(lines[end - 1])
                    or is_tableish_line(lines[end])
                )
            )

            # Check if we are inside a fence or an image unit at the proposed cut point.
            # The cut point is after line `end - 1`.
            inside_block = fence_state[end - 1] or img_state[end - 1]

            if not inside_block and not cut_inside_table:
                break

            end += 1
            extra += 1

        chunks.append((start, end))
        start = end

    return chunks


def fixed_windows(lines: list[str], window_size: int = 25) -> list[tuple[int, int]]:
    return [(i, min(i + window_size, len(lines))) for i in range(0, len(lines), window_size)]


# ---------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------


def init_manifest(source_path: Path) -> dict[str, Any]:
    return {
        "source": str(source_path),
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "files": [],
        "chunks": [],
        "planning": {},
        "coverage": [],
        "verification_flags": [],
    }


def find_file_record(manifest: dict[str, Any], filename: str) -> Optional[dict[str, Any]]:
    for record in manifest["files"]:
        if record["filename"] == filename:
            return record
    return None


def add_or_update_file_record(
    manifest: dict[str, Any],
    filename: str,
    title: str,
    summary: str,
    source_start: int,
    source_end: int,
) -> None:
    record = find_file_record(manifest, filename)
    new_range = [source_start, source_end]

    if record is None:
        manifest["files"].append(
            {
                "filename": filename,
                "title": title,
                "summary": summary,
                "source_ranges": [new_range],
                "_merged_source_ranges": [new_range],
            }
        )
    else:
        record["source_ranges"].append(new_range)
        record["source_ranges"].sort(key=lambda r: r[0])

        # Merge overlapping or adjacent ranges
        merged = []
        for start, end in record["source_ranges"]:
            if not merged:
                merged.append([start, end])
            else:
                last = merged[-1]
                if start <= last[1] + 1:
                    last[1] = max(last[1], end)
                else:
                    merged.append([start, end])
                    print(f"[WARNING] Discontinuous source ranges in {filename}: {record['source_ranges']}")
        
        record["_merged_source_ranges"] = merged


def update_markdown_frontmatter(path: Path, new_merged_ranges: list[list[int]]) -> None:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return  # unexpected format

    # Split into frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return

    _, front_str, body = parts

    # Parse existing frontmatter (simple YAML-like)
    lines = front_str.strip().splitlines()
    new_front_lines = []
    for line in lines:
        if line.startswith("source_lines:"):
            # Replace this line
            new_front_lines.append(f"source_lines: {json.dumps(new_merged_ranges)}")
        else:
            new_front_lines.append(line)

    new_front_str = "\n".join(new_front_lines)
    new_content = f"---\n{new_front_str}\n---\n{body}"

    path.write_text(new_content, encoding="utf-8")


def create_markdown_file(
    path: Path,
    title: str,
    summary: str,
    source_start: int,
    source_end: int,
    body: str,
) -> None:
    title = title.strip() or "Untitled"
    summary = summary.strip()
    # Keep `body` unchanged: leading and trailing blank source lines are owned
    # by this page just as much as non-blank source lines are.

    content = f"""---
title: {yaml_quote(title)}
summary: {yaml_quote(summary)}
source_lines: [[{source_start}, {source_end}]]
---

# {title}

{body}
"""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def add_chunk_record(
    manifest: dict[str, Any],
    source_start: int,
    source_end: int,
    action: str,
    targets: list[dict[str, Any]],
    reason: str,
) -> None:
    manifest["chunks"].append(
        {
            "source_start": source_start,
            "source_end": source_end,
            "action": action,
            "targets": targets,
            "reason": reason,
        }
    )
    manifest["updated_at"] = utc_now_iso()


def overlap_size(a_start: int, a_end: int, b_start: int, b_end: int) -> int:
    return max(0, min(a_end, b_end) - max(a_start, b_start) + 1)


def find_best_target_for_source_window(
    manifest: dict[str, Any],
    source_start: int,
    source_end: int,
) -> Optional[str]:
    """
    Returns the filename with the largest overlap for this source window.
    """

    best_filename: Optional[str] = None
    best_overlap = 0

    for chunk in manifest.get("chunks", []):
        for target in chunk.get("targets", []):
            t_start = int(target["source_start"])
            t_end = int(target["source_end"])
            size = overlap_size(source_start, source_end, t_start, t_end)

            if size > best_overlap:
                best_overlap = size
                best_filename = target["filename"]

    return best_filename


# ---------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------


def make_llm(
    model: str,
    base_url: str,
    api_key: str,
    temperature: float = 0.0,
    timeout: int = 300,
) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=temperature,
        timeout=timeout,
        max_tokens=64000,
    )


async def structured_ainvoke(
    llm: ChatOpenAI,
    schema_cls: type[BaseModel],
    messages: list[Any],
) -> BaseModel:
    """
    Uses LangChain with_structured_output first.

    If the local server does not support structured output, falls back to
    JSON-only prompting and manual Pydantic validation.
    """

    try:
        structured = llm.with_structured_output(schema_cls)
        result = await structured.ainvoke(messages)

        if isinstance(result, schema_cls):
            return result

        return schema_cls.model_validate(result)

    except Exception:
        schema_json = json.dumps(schema_cls.model_json_schema(), indent=2)

        fallback_messages = list(messages)
        fallback_messages.append(
            HumanMessage(
                content=(
                    "Return ONLY valid JSON matching this JSON Schema. "
                    "Do not include Markdown fences, comments, or prose.\n\n"
                    f"{schema_json}"
                )
            )
        )

        raw = await llm.ainvoke(fallback_messages)
        text = raw.content if hasattr(raw, "content") else str(raw)
        data = extract_json_from_text(text)
        return schema_cls.model_validate(data)


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


# ---------------------------------------------------------------------
# Generation phase
# ---------------------------------------------------------------------


def build_chunk_summary_prompt(
    previous_source_block: str,
    prior_summary_ledger: str,
    source_block: str,
    source_start: int,
    source_end: int,
) -> list[Any]:
    return [
        SystemMessage(
            content=(
                "You summarize source chunks for a later wiki-planning pass. "
                "Do not rewrite or omit source content. Describe every meaningful "
                "topic, instruction, command, warning, and transition in the current "
                "range so a later planner can choose safe page boundaries."
                "Keep your answer very very short, 2-3 lines max per field"
            )
        ),
        HumanMessage(
            content=f"""
Current source range: {source_start}–{source_end}.

Previous 100 source lines, included only for context:
```text
{previous_source_block or "(This is the first source chunk.)"}
```

Line-range summary ledger accumulated before this chunk:
```markdown
{prior_summary_ledger}
```

Current numbered source lines to summarize:
```text
{source_block}
```

Return one concise factual summary of this exact range. `topics` should list the
important subjects in source order. `suggested_heading` should be a short label
for this range. Do not claim facts not present in the source.
""",
        ),
    ]


def build_h1_plan_prompt(
    summary_ledger: str,
    source_line_count: int,
    chunk_ranges: list[list[int]],
) -> list[Any]:
    return [
        SystemMessage(
            content=(
                "You are the first pass of a lossless Markdown wiki planner. "
                "Plan only top-level H1 guide sections from the chunk summaries. "
                "Do not write Markdown or source content."
            )
        ),
        HumanMessage(
            content=f"""
Create H1 sections for source lines 1–{source_line_count}.

The returned `sections` source ranges MUST be a contiguous exact partition of
the whole document: first range starts at 1, each next range starts one line
after the previous range, and the final range ends at {source_line_count}.
There must be no gaps and no overlaps.

Choose boundaries only at these chunk ranges; each returned range must begin at
one listed range start and end at one listed range end:
{json.dumps(chunk_ranges)}

Chunk summary ledger:
```markdown
{summary_ledger}
```

Use a small number of reader-facing guide titles. Each section needs a concise
summary and an inclusive `source_range`.
""",
        ),
    ]


def build_h1_layout_prompt(
    h1: TopicRange,
    summary_ledger: str,
    chunk_ranges: list[list[int]],
) -> list[Any]:
    source_start, source_end = h1.source_range or [0, 0]
    return [
        SystemMessage(
            content=(
                "You decide whether one H1 wiki guide needs H2 folders. "
                "Plan ranges only; do not write Markdown or source text."
            )
        ),
        HumanMessage(
            content=f"""
H1 guide: {h1.title}
H1 source range: {source_start}–{source_end}
H1 summary: {h1.summary}

Decide whether this guide has enough distinct major subtopics to use H2 folders.
Set `use_h2_folders` to true only when H2 folders improve navigation. If false,
`sections` must be the final leaf pages directly inside the H1 folder. If true,
`sections` must be the H2 folder ranges; a later pass will make leaf pages.

In either case, `sections` must exactly and contiguously partition {source_start}–{source_end},
with no gap or overlap. Use only these chunk ranges:
{json.dumps(chunk_ranges)}

Relevant chunk summaries:
```markdown
{summary_ledger}
```
""",
        ),
    ]


def build_leaf_page_plan_prompt(
    parent: TopicRange,
    parent_label: str,
    summary_ledger: str,
    chunk_ranges: list[list[int]],
) -> list[Any]:
    source_start, source_end = parent.source_range or [0, 0]
    return [
        SystemMessage(
            content=(
                "You create the final page plan for one lossless wiki section. "
                "Plan only page titles, summaries, and exact source ranges."
            )
        ),
        HumanMessage(
            content=f"""
Parent {parent_label}: {parent.title}
Source range: {source_start}–{source_end}
Summary: {parent.summary}

Return reader-sized leaf pages. Their `pages` ranges MUST be an exact contiguous
partition of {source_start}–{source_end}; no source line may be skipped or
assigned twice. Boundaries must use only these complete chunk ranges:
{json.dumps(chunk_ranges)}

Relevant chunk summaries:
```markdown
{summary_ledger}
```
""",
        ),
    ]


def build_generation_prompt(
    current: Optional[CurrentFileState],
    context_tail: str,
    source_block: str,
) -> list[Any]:
    system = SystemMessage(
        content=(
            "You are Markdown Wiki Maker. "
            "You are a routing and splitting assistant only. "
            "You do NOT rewrite, summarize, clean, or transform the source text. "
            "Your job is only to decide which numbered source line ranges go into which wiki file. "
            "The script will copy the original source lines into the final Markdown files. "
            "Ignore pure visual noise such as page numbers, repeated headers, and footers."
        )
    )

    if current is None:
        current_context = (
            "There is NO current file yet.\n"
            "You MUST use action 'new' unless all source lines are pure visual noise, "
            "in which case use 'ignore'."
        )
    else:
        current_context = f"""
Current file:
- title: {current.title}
- filename: {current.filename}
- current line count: {current.line_count}
- summary: {current.summary}

STRICT 500-LINE RULE:
If the current file line count is 500 or more, you MUST NOT use 'append'.
You MUST use 'new' and name the file '[Current Title] - Part X'.
"""

    human = HumanMessage(
        content=f"""
Process the next numbered source block.

Each source line is prefixed as:

<line number>: <line content>

Use the visible line numbers to choose exact inclusive source ranges.

Action definitions:
- append: The new lines continue the current topic. Put the full/selected range in current_source_range.
- new: The new lines are a new topic. Put the full/selected range in new_source_range.
- split: Some lines continue current topic, later lines start a new topic. Use both current_source_range and new_source_range.
- ignore: The lines are pure visual noise. Use null ranges.

Use this JSON schema exactly:

{{
  "action": "append | new | split | ignore",
  "current_file": {{
    "title": "Keep same or update slightly",
    "filename": "keep-same-filename.md"
  }},
  "new_file": {{
    "title": "New Topic Title",
    "filename": "new-topic.md",
    "summary": "1-2 sentence summary"
  }},
  "current_source_range": [101, 150],
  "new_source_range": [151, 200],
  "reason": "Brief explanation of the decision"
}}

Range rules:
1. Ranges are inclusive.
2. Use only line numbers that appear in the provided source block.
3. For append, set current_source_range and set new_source_range to null.
4. For new, set new_source_range and set current_source_range to null.
5. For split, set both ranges.
6. For ignore, set both ranges to null.
7. Do NOT return Markdown content.
8. Do NOT rewrite the source lines.
9. The script will copy original source text without line number prefixes.
10. If the current file line count is 500 or more, you MUST NOT use 'append'. You MUST use 'new' and name the file '[Current Title] - Part X'.

{current_context}

Context tail, last 100 lines of already generated current file:
```markdown
{context_tail}
```

New source lines:
```text
{source_block}
```
"""
    )

    return [system, human]

def parse_part_number(title: str) -> tuple[str, int]:
    match = re.search(r"^(.*?)\s+-\s+Part\s+(\d+)$", title.strip(), flags=re.I)
    if match:
        base = match.group(1).strip()
        number = int(match.group(2))
        return base, number

    return title.strip(), 1


def forced_part_ref(current: CurrentFileState) -> NewFileRef:
    base, number = parse_part_number(current.title)
    next_number = number + 1

    title = f"{base} - Part {next_number}"
    filename = slugify(title) + ".md"
    summary = f"Continuation of {base}."

    return NewFileRef(title=title, filename=filename, summary=summary)


def enforce_generation_rules(
    decision: GenerationDecision,
    current: Optional[CurrentFileState],
    source_start: int,
    source_end: int,
) -> GenerationDecision:
    """
    Enforces that every line in [source_start, source_end] is assigned to a file.
    If not, creates a fallback new file for unassigned lines.
    """
    full_set = set(range(source_start, source_end + 1))
    assigned_set = set()

    # Clamp ranges first
    if decision.current_source_range:
        cr = clamp_range_to_chunk(decision.current_source_range, source_start, source_end)
        if cr:
            decision.current_source_range = cr
            assigned_set.update(range(cr[0], cr[1] + 1))

    if decision.new_source_range:
        nr = clamp_range_to_chunk(decision.new_source_range, source_start, source_end)
        if nr:
            decision.new_source_range = nr
            assigned_set.update(range(nr[0], nr[1] + 1))

    unassigned = full_set - assigned_set

    # Handle initial state
    if current is None:
        if decision.action in {"append", "split"} or not decision.new_file.title:
            decision.action = "new"
            decision.current_source_range = None
            decision.new_source_range = full_chunk_range(source_start, source_end)
            if not decision.new_file.title:
                decision.new_file.title = "Introduction"
            if not decision.new_file.filename:
                decision.new_file.filename = "introduction.md"
            if not decision.new_file.summary:
                decision.new_file.summary = "Opening section from the source document."
        assigned_set = full_set
        unassigned = set()

    # Enforce 500-line rule
    elif current and current.line_count >= 500:
        part_ref = forced_part_ref(current)
        decision.action = "new"
        decision.current_source_range = None
        decision.new_source_range = full_chunk_range(source_start, source_end)
        decision.new_file = part_ref
        decision.reason = (
            decision.reason.strip()
            + " Script enforced 500-line hard rule and created a new Part file."
        ).strip()
        assigned_set = full_set
        unassigned = set()

    # Fill missing ranges safely
    elif decision.action == "append":
        if not decision.current_source_range:
            decision.current_source_range = full_chunk_range(source_start, source_end)
        decision.new_source_range = None
        assigned_set = full_set
        unassigned = set()

    elif decision.action == "new":
        if not decision.new_source_range:
            decision.new_source_range = full_chunk_range(source_start, source_end)
        decision.current_source_range = None
        assigned_set = full_set
        unassigned = set()

    elif decision.action == "split":
        if not decision.current_source_range or not decision.new_source_range:
            cr, nr = split_chunk_ranges(source_start, source_end)
            decision.current_source_range = cr
            decision.new_source_range = nr
        assigned_set = full_set
        unassigned = set()

    elif decision.action == "ignore":
        decision.current_source_range = None
        decision.new_source_range = None
        assigned_set = set()
        unassigned = full_set

    # CRITICAL: If any lines remain unassigned, force a new file for them
    if unassigned:
        print(f"[WARNING] Unassigned lines detected: {sorted(unassigned)[:10]}...")
        # Create a minimal fallback file
        min_line, max_line = min(unassigned), max(unassigned)
        fallback_range = [min_line, max_line]

        # Force action to 'split' or handle via new file
        if decision.action == "new":
            # Extend new range
            existing = decision.new_source_range
            if existing:
                decision.new_source_range = [min(existing[0], min_line), max(existing[1], max_line)]
            else:
                decision.new_source_range = fallback_range
        elif decision.action in {"append", "split"} and current:
            # Add fallback as new file
            decision.action = "split"
            decision.new_source_range = fallback_range
            if not decision.new_file.title:
                decision.new_file.title = f"Continuation after line {max_line}"
            if not decision.new_file.filename:
                decision.new_file.filename = f"continuation-{min_line}.md"
            if not decision.new_file.summary:
                decision.new_file.summary = "Auto-created for unassigned lines."

        # Rebuild assigned set
        assigned_set = set(range(source_start, source_end + 1))
        unassigned = set()

    return decision

async def phase_generate_flat(args: argparse.Namespace) -> None:
    source_path = Path(args.source)
    out_dir = Path(args.out)
    manifest_path = out_dir / "manifest.json"

    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    if manifest_path.exists() and not args.clean:
        raise RuntimeError(
            f"{manifest_path} already exists. Use --clean to regenerate from scratch."
        )

    source_lines = read_lines(source_path)
    chunks = chunk_source_lines_preserving_tables(
        source_lines,
        target_size=args.generation_lines,
        max_extra=args.max_chunk_extra,
    )

    manifest = init_manifest(source_path)

    llm = make_llm(
        model=args.gen_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=args.temperature,
        timeout=args.timeout,
    )

    current: Optional[CurrentFileState] = None
    next_index = 1

    for chunk_number, (start_idx, end_idx) in enumerate(chunks, start=1):
        source_start = start_idx + 1
        source_end = end_idx

        print(
            f"[Generation] Chunk {chunk_number}/{len(chunks)} "
            f"source lines {source_start}-{source_end}"
        )

        chunk_lines = source_lines[start_idx:end_idx]
        source_block = numbered_source_lines(chunk_lines, source_start)

        if current is None:
            context_tail = ""
        else:
            context_tail = last_n_lines_from_file(out_dir / current.filename, 100)
            current.line_count = count_file_lines(out_dir / current.filename)

        messages = build_generation_prompt(current, context_tail, source_block)

        decision = await structured_ainvoke(llm, GenerationDecision, messages)

        # Enforce rules: ensures 100% line coverage and handles fallbacks
        decision = enforce_generation_rules(
            decision=decision,
            current=current,
            source_start=source_start,
            source_end=source_end,
        )

        targets: list[dict[str, Any]] = []

        if decision.action == "ignore":
            add_chunk_record(
                manifest=manifest,
                source_start=source_start,
                source_end=source_end,
                action="ignore",
                targets=[],
                reason=decision.reason,
            )
            write_json(manifest_path, manifest)
            continue

        # Helper to refresh the YAML frontmatter of a specific file
        def refresh_frontmatter(filename: str):
            file_record = find_file_record(manifest, filename)
            if file_record:
                merged_ranges = file_record.get("_merged_source_ranges", [[source_start, source_end]])
                update_markdown_frontmatter(out_dir / filename, merged_ranges)

        if decision.action == "append":
            if current is None:
                raise RuntimeError("Internal error: append requested without current file.")

            current_range = decision.current_source_range
            body = range_to_markdown(source_lines, current_range)

            append_markdown(out_dir / current.filename, body)
            current.line_count = count_file_lines(out_dir / current.filename)

            add_or_update_file_record(
                manifest, current.filename, current.title, current.summary,
                current_range[0], current_range[1],
            )
            refresh_frontmatter(current.filename)

            targets.append({
                "filename": current.filename,
                "source_start": current_range[0],
                "source_end": current_range[1],
            })

        elif decision.action == "new":
            new_range = decision.new_source_range
            body = range_to_markdown(source_lines, new_range)

            title = decision.new_file.title.strip() or "Untitled"
            summary = decision.new_file.summary.strip()
            filename = make_unique_filename(
                out_dir, next_index, decision.new_file.filename, title,
            )
            next_index += 1

            create_markdown_file(
                path=out_dir / filename, title=title, summary=summary,
                source_start=new_range[0], source_end=new_range[1], body=body,
            )

            # The new file becomes the current file
            current = CurrentFileState(
                title=title, filename=filename, summary=summary,
                line_count=count_file_lines(out_dir / filename),
            )

            add_or_update_file_record(
                manifest, filename, title, summary, new_range[0], new_range[1],
            )
            refresh_frontmatter(filename)

            targets.append({
                "filename": filename,
                "source_start": new_range[0],
                "source_end": new_range[1],
            })

        elif decision.action == "split":
            if current is None:
                raise RuntimeError("Internal error: split requested without current file.")

            current_range = decision.current_source_range
            new_range = decision.new_source_range

            # 1. Append to the existing current file
            if current_range:
                current_body = range_to_markdown(source_lines, current_range)
                append_markdown(out_dir / current.filename, current_body)
                current.line_count = count_file_lines(out_dir / current.filename)

                add_or_update_file_record(
                    manifest, current.filename, current.title, current.summary,
                    current_range[0], current_range[1],
                )
                refresh_frontmatter(current.filename)

                targets.append({
                    "filename": current.filename,
                    "source_start": current_range[0],
                    "source_end": current_range[1],
                })

            # 2. Create the new file for the remaining lines
            if new_range:
                new_body = range_to_markdown(source_lines, new_range)

                title = decision.new_file.title.strip() or "Untitled"
                summary = decision.new_file.summary.strip()
                filename = make_unique_filename(
                    out_dir, next_index, decision.new_file.filename, title,
                )
                next_index += 1

                create_markdown_file(
                    path=out_dir / filename, title=title, summary=summary,
                    source_start=new_range[0], source_end=new_range[1], body=new_body,
                )

                # The newly created file becomes the current file for the next chunk
                current = CurrentFileState(
                    title=title, filename=filename, summary=summary,
                    line_count=count_file_lines(out_dir / filename),
                )

                add_or_update_file_record(
                    manifest, filename, title, summary, new_range[0], new_range[1],
                )
                refresh_frontmatter(filename)

                targets.append({
                    "filename": filename,
                    "source_start": new_range[0],
                    "source_end": new_range[1],
                })

        else:
            raise RuntimeError(f"Unknown action: {decision.action}")

        add_chunk_record(
            manifest=manifest,
            source_start=source_start,
            source_end=source_end,
            action=decision.action,
            targets=targets,
            reason=decision.reason,
        )

        write_json(manifest_path, manifest)

    print(f"[Generation] Done. Manifest written to {manifest_path}")


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


from typing import Any, Callable, TypeVar
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

T = TypeVar("T", bound=BaseModel)


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


async def phase_generate(args: argparse.Namespace) -> None:
    """Plan first, prove leaf coverage, then render the hierarchical wiki tree."""
    source_path = Path(args.source)
    out_dir = Path(args.out)
    manifest_path = out_dir / "manifest.json"

    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if manifest_path.exists() and not args.clean:
        raise RuntimeError(
            f"{manifest_path} already exists. Use --clean to regenerate from scratch."
        )

    source_lines = read_lines(source_path)
    chunks = chunk_source_lines_preserving_tables(
        source_lines,
        target_size=args.generation_lines,
        max_extra=args.max_chunk_extra,
    )
    manifest = init_manifest(source_path)
    planning_dir = out_dir / "_planning"
    summary_path = planning_dir / "chunk-summaries.md"
    topic_plan_path = planning_dir / "topic-index.md"
    coverage_path = planning_dir / "coverage.json"
    initialize_chunk_summary_document(summary_path, source_path)

    llm = make_llm(
        model=args.gen_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=args.temperature,
        timeout=args.timeout,
    )

    summaries: list[dict[str, Any]] = []
    for chunk_number, (start_idx, end_idx) in enumerate(chunks, start=1):
        source_start = start_idx + 1
        source_end = end_idx
        previous_start_idx = max(0, start_idx - 100)
        previous_block = numbered_source_lines(
            source_lines[previous_start_idx:start_idx],
            previous_start_idx + 1,
        )
        source_block = numbered_source_lines(source_lines[start_idx:end_idx], source_start)
        prior_ledger = summary_path.read_text(encoding="utf-8")

        print(
            f"[Planning] Summarizing chunk {chunk_number}/{len(chunks)} "
            f"source lines {source_start}-{source_end}"
        )
        result = await structured_ainvoke(
            llm,
            ChunkSummary,
            build_chunk_summary_prompt(
                previous_source_block=previous_block,
                prior_summary_ledger=prior_ledger,
                source_block=source_block,
                source_start=source_start,
                source_end=source_end,
            ),
        )
        summary = ChunkSummary.model_validate(result)
        record = {
            "source_start": source_start,
            "source_end": source_end,
            **summary.model_dump(),
        }
        summaries.append(record)
        append_chunk_summary_document(summary_path, source_start, source_end, summary)
        manifest["planning"]["chunk_summaries"] = summaries
        manifest["updated_at"] = utc_now_iso()
        write_json(manifest_path, manifest)

    if not source_lines:
        hierarchy: list[dict[str, Any]] = []
    else:
        summary_ledger = format_summary_ledger(summaries)
        all_chunk_ranges = allowed_chunk_ranges(summaries, 1, len(source_lines))
        
        h1_prompt = build_h1_plan_prompt(
            summary_ledger=summary_ledger,
            source_line_count=len(source_lines),
            chunk_ranges=all_chunk_ranges,
        )

        h1_plan, h1_sections = await structured_partition_ainvoke_with_retries(
            llm=llm,
            schema_cls=H1Plan,
            base_messages=h1_prompt,
            extract_topics=lambda plan: plan.sections,
            source_start=1,
            source_end=len(source_lines),
            valid_chunk_ranges=all_chunk_ranges,
            fallback_title=source_path.stem.replace("-", " ").title(),
            fallback_summary="Complete source document.",
            label="H1",
            max_retries=args.partition_retries,
        )

        # Stage 2: decide every H1's shape before any H2 is expanded into pages.
        h1_layouts: list[dict[str, Any]] = []
        for h1 in h1_sections:
            h1_start, h1_end = h1.source_range or [0, 0]
            h1_summaries = summaries_for_range(summaries, h1_start, h1_end)
            h1_ranges = allowed_chunk_ranges(summaries, h1_start, h1_end)
            layout_prompt = build_h1_layout_prompt(
                h1=h1,
                summary_ledger=format_summary_ledger(h1_summaries),
                chunk_ranges=h1_ranges,
            )

            layout, layout_sections = await structured_partition_ainvoke_with_retries(
                llm=llm,
                schema_cls=H1Layout,
                base_messages=layout_prompt,
                extract_topics=lambda plan: plan.sections,
                source_start=h1_start,
                source_end=h1_end,
                valid_chunk_ranges=h1_ranges,
                fallback_title=h1.title,
                fallback_summary=h1.summary or "Source section.",
                label=f"{h1.title} layout",
                max_retries=args.partition_retries,
            )
            h1_layouts.append(
                {
                    "h1": h1,
                    "use_h2_folders": layout.use_h2_folders,
                    "sections": layout_sections,
                }
            )

        # Stage 3: all chosen H2 sections are now split into final files.
        hierarchy = []
        for h1_layout in h1_layouts:
            h1 = h1_layout["h1"]
            if not h1_layout["use_h2_folders"]:
                hierarchy.append(
                    {
                        "h1": h1,
                        "use_h2_folders": False,
                        "groups": [{"topic": h1, "pages": h1_layout["sections"]}],
                    }
                )
                continue

            groups: list[dict[str, Any]] = []
            for h2 in h1_layout["sections"]:
                h2_start, h2_end = h2.source_range or [0, 0]
                h2_summaries = summaries_for_range(summaries, h2_start, h2_end)
                h2_ranges = allowed_chunk_ranges(summaries, h2_start, h2_end)
                leaf_prompt = build_leaf_page_plan_prompt(
                    parent=h2,
                    parent_label="H2 section",
                    summary_ledger=format_summary_ledger(h2_summaries),
                    chunk_ranges=h2_ranges,
                )

                leaf_plan, pages = await structured_partition_ainvoke_with_retries(
                    llm=llm,
                    schema_cls=LeafPagePlan,
                    base_messages=leaf_prompt,
                    extract_topics=lambda plan: plan.pages,
                    source_start=h2_start,
                    source_end=h2_end,
                    valid_chunk_ranges=h2_ranges,
                    fallback_title=h2.title,
                    fallback_summary=h2.summary or "Source section.",
                    label=f"{h2.title} leaf page",
                    max_retries=args.partition_retries,
                )
                groups.append({"topic": h2, "pages": pages})

            hierarchy.append(
                {"h1": h1, "use_h2_folders": True, "groups": groups}
            )

    leaves = planned_leaf_pages(hierarchy)
    assert_exact_coverage(leaves, len(source_lines))
    write_topic_plan_document(topic_plan_path, hierarchy)

    manifest["planning"]["hierarchy"] = hierarchy_to_manifest(hierarchy)
    manifest["planning"]["coverage_verified_at"] = utc_now_iso()
    coverage = render_hierarchical_wiki(out_dir, source_lines, manifest, hierarchy)
    manifest["coverage"] = coverage
    manifest["updated_at"] = utc_now_iso()
    write_json(manifest_path, manifest)
    write_json(
        coverage_path,
        {
            "source": str(source_path),
            "source_line_count": len(source_lines),
            "exact_coverage": True,
            "assignments": coverage,
        },
    )
    print(f"[Generation] Done. Hierarchical wiki written to {out_dir}")


# ---------------------------------------------------------------------
# Verification phase
# ---------------------------------------------------------------------


def build_verification_prompt(
    source_block: str,
    target_filename: str,
    wiki_content: str,
) -> list[Any]:
    system = SystemMessage(
        content=(
            "You are a strict verification checker. "
            "Your job is to compare source document lines against the generated wiki page. "
            "Ignore page numbers, repeated headers, footers, and pure formatting artifacts. "
            "Do not flag harmless wording changes. "
            "Do flag lost facts, steps, rules, commands, warnings, numeric values, and table data. "
            "Also flag hallucinated claims that are not supported by the source."
        )
    )

    human = HumanMessage(
        content=f"""
Here are 25 source lines from the original document.

```text
{source_block}
```

Here is the generated wiki page they were assigned to.

Target file: {target_filename}

```markdown
{wiki_content}
```

Question:
Did any non-trivial information get lost or hallucinated?

Reply using structured JSON:
- answer: "YES" if information was lost or hallucinated.
- answer: "NO" if all important information is preserved.
- missing_facts: list missing facts, if any.
- hallucinations: list unsupported generated claims, if any.
- reason: brief explanation.
"""
    )

    return [system, human]


async def verify_one_window(
    semaphore: asyncio.Semaphore,
    llm: ChatOpenAI,
    out_dir: Path,
    manifest: dict[str, Any],
    source_lines: list[str],
    start_idx: int,
    end_idx: int,
) -> Optional[dict[str, Any]]:
    async with semaphore:
        source_start = start_idx + 1
        source_end = end_idx

        target_filename = find_best_target_for_source_window(
            manifest,
            source_start,
            source_end,
        )

        if target_filename is None:
            return None

        target_path = out_dir / target_filename
        if not target_path.exists():
            return {
                "source_start": source_start,
                "source_end": source_end,
                "target_file": target_filename,
                "answer": "YES",
                "missing_facts": [f"Target file does not exist: {target_filename}"],
                "hallucinations": [],
                "reason": "Manifest points to a missing file.",
                "status": "flagged",
            }

        source_block = numbered_source_lines(source_lines[start_idx:end_idx], source_start)
        wiki_content = target_path.read_text(encoding="utf-8")

        messages = build_verification_prompt(
            source_block=source_block,
            target_filename=target_filename,
            wiki_content=wiki_content,
        )

        result = await structured_ainvoke(llm, VerificationResult, messages)
        result = VerificationResult.model_validate(result)

        if result.answer == "YES":
            return {
                "source_start": source_start,
                "source_end": source_end,
                "target_file": target_filename,
                "answer": result.answer,
                "missing_facts": result.missing_facts,
                "hallucinations": result.hallucinations,
                "reason": result.reason,
                "status": "flagged",
            }

        return None


async def phase_verify(args: argparse.Namespace) -> None:
    source_path = Path(args.source)
    out_dir = Path(args.out)
    manifest_path = out_dir / "manifest.json"

    if not manifest_path.exists():
        raise RuntimeError(f"Missing manifest: {manifest_path}")

    source_lines = read_lines(source_path)
    manifest = load_json(manifest_path)

    windows = fixed_windows(source_lines, args.verification_lines)

    llm = make_llm(
        model=args.verify_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=0.0,
        timeout=args.timeout,
    )

    semaphore = asyncio.Semaphore(args.concurrency)

    print(
        f"[Verification] Checking {len(windows)} windows "
        f"with concurrency={args.concurrency}"
    )

    tasks = [
        verify_one_window(
            semaphore=semaphore,
            llm=llm,
            out_dir=out_dir,
            manifest=manifest,
            source_lines=source_lines,
            start_idx=start,
            end_idx=end,
        )
        for start, end in windows
    ]

    results = await asyncio.gather(*tasks)
    flags = [result for result in results if result is not None]

    manifest["verification_flags"] = flags
    manifest["updated_at"] = utc_now_iso()

    write_json(manifest_path, manifest)
    write_json(out_dir / "verification_flags.json", {"flags": flags})

    print(f"[Verification] Done. Flagged windows: {len(flags)}")


# ---------------------------------------------------------------------
# Repair phase
# ---------------------------------------------------------------------


def build_repair_prompt(
    source_block: str,
    target_filename: str,
    wiki_content: str,
    missing_facts: list[str],
    hallucinations: list[str],
) -> list[Any]:
    system = SystemMessage(
        content=(
            "You are a Markdown repair assistant. "
            "Your job is to create a concise Markdown patch to append to an existing wiki page. "
            "Do not rewrite the whole page. "
            "Do not duplicate facts already present. "
            "Preserve all non-trivial source information. "
            "If there is a hallucination, add a corrective clarification instead of deleting text."
        )
    )

    human = HumanMessage(
        content=f"""
Repair this wiki page by producing Markdown that can be appended to the file.

Target file: {target_filename}

Flagged source lines:
```text
{source_block}
```

Verifier missing facts:
{json.dumps(missing_facts, indent=2, ensure_ascii=False)}

Verifier hallucinations:
{json.dumps(hallucinations, indent=2, ensure_ascii=False)}

Current target wiki content:
```markdown
{wiki_content}
```

Return structured JSON:
- markdown_patch: Markdown text to append to the target file.
- reason: brief explanation.

The patch should:
1. Add missing facts, steps, rules, commands, warnings, numeric values, and table data.
2. Avoid duplicating content already present.
3. Be ready to append directly to the Markdown file.
"""
    )

    return [system, human]


async def phase_repair(args: argparse.Namespace) -> None:
    source_path = Path(args.source)
    out_dir = Path(args.out)
    manifest_path = out_dir / "manifest.json"

    if not manifest_path.exists():
        raise RuntimeError(f"Missing manifest: {manifest_path}")

    source_lines = read_lines(source_path)
    manifest = load_json(manifest_path)

    flags = manifest.get("verification_flags", [])

    if not flags:
        print("[Repair] No verification flags found. Nothing to repair.")
        return

    llm = make_llm(
        model=args.verify_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=0.0,
        timeout=args.timeout,
    )

    repaired_count = 0

    for index, flag in enumerate(flags, start=1):
        if flag.get("status") == "repaired":
            continue

        source_start = int(flag["source_start"])
        source_end = int(flag["source_end"])
        target_filename = flag["target_file"]

        target_path = out_dir / target_filename

        print(
            f"[Repair] {index}/{len(flags)} "
            f"source lines {source_start}-{source_end} -> {target_filename}"
        )

        if not target_path.exists():
            flag["status"] = "repair_failed"
            flag["repair_error"] = f"Target file missing: {target_filename}"
            continue

        source_block = numbered_source_lines(
            source_lines[source_start - 1 : source_end],
            source_start,
        )

        wiki_content = target_path.read_text(encoding="utf-8")

        messages = build_repair_prompt(
            source_block=source_block,
            target_filename=target_filename,
            wiki_content=wiki_content,
            missing_facts=flag.get("missing_facts", []),
            hallucinations=flag.get("hallucinations", []),
        )

        try:
            result = await structured_ainvoke(llm, RepairResult, messages)
            result = RepairResult.model_validate(result)

            patch = result.markdown_patch.strip()

            if patch:
                repair_block = (
                    f"\n\n---\n\n"
                    f"## Repair Addendum: Source lines {source_start}-{source_end}\n\n"
                    f"{patch}\n"
                )
                append_markdown(target_path, repair_block)

            flag["status"] = "repaired"
            flag["repair_reason"] = result.reason
            flag["repaired_at"] = utc_now_iso()
            repaired_count += 1

        except Exception as exc:
            flag["status"] = "repair_failed"
            flag["repair_error"] = str(exc)

        manifest["updated_at"] = utc_now_iso()
        write_json(manifest_path, manifest)

    print(f"[Repair] Done. Repaired flags: {repaired_count}")

# ---------------------------------------------------------------------
# CLI / batch runner
# ---------------------------------------------------------------------

def collect_source_files(source_path: str) -> list[Path]:
    path = Path(source_path)

    if path.is_file():
        if path.suffix.lower() != ".md":
            raise RuntimeError(f"Source file is not Markdown: {path}")
        return [path]

    if path.is_dir():
        files = sorted(path.glob("*.md"))
        if not files:
            raise RuntimeError(f"No .md files found in folder: {path}")
        return files

    raise RuntimeError(f"Source path does not exist: {path}")


def output_dir_for_source(source_file: Path, output_root: str) -> Path:
    """
    Example:
    /input/mpf.md + /output/ -> /output/mpf/
    """
    return Path(output_root) / source_file.stem


def make_config_for_source(source_file: Path) -> SimpleNamespace:
    return SimpleNamespace(
        source=str(source_file),
        out=str(output_dir_for_source(source_file, OUTPUT_ROOT)),
        phase=PHASE,
        base_url=BASE_URL,
        api_key=API_KEY,
        gen_model=GEN_MODEL,
        verify_model=VERIFY_MODEL,
        generation_lines=GENERATION_LINES,
        verification_lines=VERIFICATION_LINES,
        max_chunk_extra=MAX_CHUNK_EXTRA,
        concurrency=CONCURRENCY,
        temperature=TEMPERATURE,
        timeout=TIMEOUT,
        clean=CLEAN_OUTPUT,
        partition_retries=PARTITION_RETRY_ATTEMPTS
    )


async def process_one_source(
    semaphore: asyncio.Semaphore,
    source_file: Path,
) -> None:
    async with semaphore:
        config = make_config_for_source(source_file)

        print("=" * 80)
        print(f"[Batch] Starting: {config.source}")
        print(f"[Batch] Output:   {config.out}")
        print("=" * 80)

        try:
            if config.phase == "generate-flat":
                await phase_generate_flat(config)
            elif config.phase in {"all", "generate"}:
                await phase_generate(config)

            if config.phase in {"all", "verify"}:
                await phase_verify(config)

            if config.phase in {"all", "repair"}:
                await phase_repair(config)

            print(f"[Batch] Done: {config.source}")

        except Exception as exc:
            print(f"[Batch] FAILED: {config.source}")
            print(f"[Batch] Error: {exc}")


async def async_main() -> None:
    source_files = collect_source_files(SOURCE_PATH)

    print(f"[Batch] Found {len(source_files)} Markdown file(s).")
    print(f"[Batch] File concurrency: {FILE_CONCURRENCY}")

    semaphore = asyncio.Semaphore(FILE_CONCURRENCY)

    tasks = [
        process_one_source(
            semaphore=semaphore,
            source_file=source_file,
        )
        for source_file in source_files
    ]

    await asyncio.gather(*tasks)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
