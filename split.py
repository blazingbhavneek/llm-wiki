from __future__ import annotations

import asyncio
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Awaitable, Callable

from tqdm import tqdm

from wiki_new.llm import make_llm, structured_ainvoke
from wiki_new.models import (
    API_KEY,
    BASE_URL,
    CLEAN_OUTPUT,
    GEN_MODEL,
    GENERATION_LINES,
    OUTPUT_ROOT,
    SOURCE_PATH,
    TEMPERATURE,
    TIMEOUT,
    ChunkSummary,
)
from wiki_new.phases import assert_rendered_docs_match_source
from wiki_new.planning import (
    ConceptFilePlan,
    join_original_source_lines,
    manifest_add_chunk_record,
    manifest_add_file_record,
    normalize_filename,
    numbered_output_filename,
    write_concept_markdown_file,
    write_concept_plan_document,
    write_coverage_json,
    write_metadata_json,
)
from wiki_new.prompts import build_chunk_summary_prompt
from wiki_new.utils import (
    init_manifest,
    is_fence_line,
    is_tableish_line,
    load_json,
    numbered_source_lines,
    read_lines,
    slugify,
    write_json,
)

H1_RE = re.compile(r"^#(?!#)\s+(.*\S)\s*$")
H2_RE = re.compile(r"^##(?!#)\s+(.*\S)\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s+")

SUMMARY_CONCURRENCY = 4


@dataclass(frozen=True)
class SectionRange:
    title: str
    header: str
    slug_hint: str
    source_start: int
    source_end: int


@dataclass(frozen=True)
class PlannedSection:
    plan: ConceptFilePlan
    header: str


@dataclass(frozen=True)
class BoundarySafetyMap:
    source_lines: list[str]
    inside_fence_before: list[bool]
    inside_image_before: list[bool]
    cuts_table: list[bool]

    def is_safe_split(self, split_line: int) -> bool:
        if split_line <= 1 or split_line > len(self.source_lines):
            return True
        return (
            not self.inside_fence_before[split_line]
            and not self.inside_image_before[split_line]
            and not self.cuts_table[split_line]
        )


SummaryProvider = Callable[
    [ConceptFilePlan, list[str]],
    Awaitable[str],
]


def clean_heading_text(text: str) -> str:
    return re.sub(r"\s+#+\s*$", "", text.strip())


def title_from_path(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").strip().title() or "Document"


def extract_document_title(source_lines: list[str], source_path: Path) -> str:
    in_fence = False
    for line in source_lines:
        if is_fence_line(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = H1_RE.match(line)
        if match:
            return clean_heading_text(match.group(1))
    return title_from_path(source_path)


def build_boundary_safety_map(source_lines: list[str]) -> BoundarySafetyMap:
    line_count = len(source_lines)
    inside_fence_before = [False] * (line_count + 2)
    inside_image_before = [False] * (line_count + 2)
    cuts_table = [False] * (line_count + 2)

    in_fence = False
    in_image = False

    for split_line in range(1, line_count + 2):
        inside_fence_before[split_line] = in_fence
        inside_image_before[split_line] = in_image

        if split_line <= line_count:
            line = source_lines[split_line - 1]
            if is_fence_line(line):
                in_fence = not in_fence
            if "<image-unit>" in line:
                in_image = True
            if "</image-unit>" in line:
                in_image = False

    for split_line in range(2, line_count + 1):
        previous_line = source_lines[split_line - 2]
        current_line = source_lines[split_line - 1]
        cuts_table[split_line] = is_tableish_line(previous_line) and is_tableish_line(
            current_line
        )

    return BoundarySafetyMap(
        source_lines=source_lines,
        inside_fence_before=inside_fence_before,
        inside_image_before=inside_image_before,
        cuts_table=cuts_table,
    )


def find_h2_sections(
    source_lines: list[str], source_path: Path
) -> tuple[str, list[SectionRange]]:
    if not source_lines:
        return title_from_path(source_path), []

    document_title = extract_document_title(source_lines, source_path)
    headings: list[tuple[int, str]] = []
    in_fence = False

    for line_number, line in enumerate(source_lines, start=1):
        if is_fence_line(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = H2_RE.match(line)
        if match:
            headings.append((line_number, clean_heading_text(match.group(1))))

    if not headings:
        return document_title, [
            SectionRange(
                title=document_title,
                header=document_title,
                slug_hint=slugify(document_title) or "document",
                source_start=1,
                source_end=len(source_lines),
            )
        ]

    sections: list[SectionRange] = []

    first_h2_line = headings[0][0]
    if first_h2_line > 1:
        sections.append(
            SectionRange(
                title=f"{document_title} Introduction",
                header=document_title,
                slug_hint="introduction",
                source_start=1,
                source_end=first_h2_line - 1,
            )
        )

    for index, (line_number, heading_text) in enumerate(headings):
        next_line = (
            headings[index + 1][0]
            if index + 1 < len(headings)
            else len(source_lines) + 1
        )
        sections.append(
            SectionRange(
                title=heading_text,
                header=heading_text,
                slug_hint=slugify(heading_text) or f"section-{index + 1}",
                source_start=line_number,
                source_end=next_line - 1,
            )
        )

    return document_title, sections


def boundary_priority(source_lines: list[str], split_line: int) -> int:
    if split_line <= 1 or split_line > len(source_lines):
        return 3

    previous_line = source_lines[split_line - 2].strip()
    current_line = source_lines[split_line - 1].strip()

    if not previous_line or not current_line:
        return 0
    if HEADING_RE.match(current_line):
        return 1
    if HEADING_RE.match(previous_line):
        return 2
    return 3


def choose_safe_boundary_end(
    *,
    safety_map: BoundarySafetyMap,
    part_start: int,
    range_end: int,
    remaining_parts: int,
    max_part_lines: int,
) -> int:
    remaining_lines = range_end - part_start + 1
    min_len = max(1, remaining_lines - ((remaining_parts - 1) * max_part_lines))
    max_len = min(max_part_lines, remaining_lines - (remaining_parts - 1))

    if min_len > max_len:
        raise RuntimeError(
            f"Cannot split source lines {part_start}-{range_end} into {remaining_parts} safe parts."
        )

    target_end = part_start - 1 + (remaining_lines / remaining_parts)
    min_end = part_start + min_len - 1
    max_end = part_start + max_len - 1

    candidates: list[tuple[float, int, int]] = []
    for end_line in range(min_end, max_end + 1):
        split_line = end_line + 1
        if not safety_map.is_safe_split(split_line):
            continue
        candidates.append(
            (
                abs(end_line - target_end),
                boundary_priority(safety_map.source_lines, split_line),
                end_line,
            )
        )

    if not candidates:
        raise RuntimeError(
            f"No safe split boundary found for source lines {part_start}-{range_end} "
            f"with max part size {max_part_lines}."
        )

    return min(candidates)[2]


def split_range_recursively(
    *,
    safety_map: BoundarySafetyMap,
    source_start: int,
    source_end: int,
    max_lines: int,
) -> list[tuple[int, int]]:
    if source_start > source_end:
        return []

    length = source_end - source_start + 1
    if length <= max_lines:
        return [(source_start, source_end)]

    max_part_lines = max_lines - 1
    if max_part_lines <= 0:
        raise ValueError("max_lines must be greater than 1.")

    part_count = max(2, math.ceil(length / max_part_lines))
    parts: list[tuple[int, int]] = []
    cursor = source_start

    for part_index in range(1, part_count + 1):
        if part_index == part_count:
            parts.append((cursor, source_end))
            break

        remaining_parts = part_count - part_index + 1
        end_line = choose_safe_boundary_end(
            safety_map=safety_map,
            part_start=cursor,
            range_end=source_end,
            remaining_parts=remaining_parts,
            max_part_lines=max_part_lines,
        )
        parts.append((cursor, end_line))
        cursor = end_line + 1

    result: list[tuple[int, int]] = []
    for part_start, part_end in parts:
        if part_end - part_start + 1 > max_lines:
            result.extend(
                split_range_recursively(
                    safety_map=safety_map,
                    source_start=part_start,
                    source_end=part_end,
                    max_lines=max_lines,
                )
            )
        else:
            result.append((part_start, part_end))

    return result


def allocate_unique_filename(filename: str, used_filenames: set[str]) -> str:
    candidate = filename
    if candidate not in used_filenames:
        used_filenames.add(candidate)
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix or ".md"
    counter = 2

    while True:
        candidate = f"{stem}-{counter}{suffix}"
        if candidate not in used_filenames:
            used_filenames.add(candidate)
            return candidate
        counter += 1


def read_progress_records(progress_path: Path) -> list[dict[str, str | int]]:
    if not progress_path.exists():
        return []

    data = load_json(progress_path)
    files = data.get("files", [])
    if not isinstance(files, list):
        return []

    return [record for record in files if isinstance(record, dict)]


def build_plans_for_source(
    source_lines: list[str],
    source_path: Path,
    max_lines: int,
) -> tuple[str, list[PlannedSection]]:
    document_title, sections = find_h2_sections(source_lines, source_path)
    safety_map = build_boundary_safety_map(source_lines)
    used_filenames: set[str] = set()
    planned_sections: list[PlannedSection] = []

    for section in sections:
        ranges = split_range_recursively(
            safety_map=safety_map,
            source_start=section.source_start,
            source_end=section.source_end,
            max_lines=max_lines,
        )
        range_count = len(ranges)

        for index, (part_start, part_end) in enumerate(ranges, start=1):
            if range_count == 1:
                part_title = section.title
                slug_base = section.slug_hint
            else:
                part_title = f"{section.title} Part {index}"
                slug_base = f"{section.slug_hint}-part-{index}"

            filename = allocate_unique_filename(
                f"{slugify(slug_base) or 'section'}.md",
                used_filenames,
            )

            planned_sections.append(
                PlannedSection(
                    plan=ConceptFilePlan(
                        title=part_title,
                        filename=filename,
                        source_start=part_start,
                        source_end=part_end,
                        summary="",
                    ),
                    header=section.header,
                )
            )

    return document_title, planned_sections


async def llm_summary_provider(
    llm,
    plan: ConceptFilePlan,
    source_lines: list[str],
) -> str:
    previous_start = max(1, plan.source_start - 100)
    previous_source_block = join_original_source_lines(
        source_lines[previous_start - 1 : plan.source_start - 1]
    ).strip()
    source_block = numbered_source_lines(
        source_lines[plan.source_start - 1 : plan.source_end],
        plan.source_start,
    )

    try:
        result = await structured_ainvoke(
            llm,
            ChunkSummary,
            build_chunk_summary_prompt(
                previous_source_block=previous_source_block,
                prior_summary_ledger="",
                source_block=source_block,
                source_start=plan.source_start,
                source_end=plan.source_end,
            ),
            max_output_tokens=300,
        )
        summary = result.summary.strip()
        if summary:
            return summary
    except Exception:
        pass

    return f"Source lines {plan.source_start}-{plan.source_end}."


async def annotate_summaries(
    planned_sections: list[PlannedSection],
    source_lines: list[str],
    provider: SummaryProvider,
    max_concurrency: int,
    progress_path: Path,
    docs_dir: Path,
    planning_dir: Path,
    output_root: Path,
    manifest: dict[str, object],
    source_file: Path,
    document_title: str,
    committed_records: list[dict[str, object]],
) -> list[PlannedSection]:
    semaphore = asyncio.Semaphore(max_concurrency)
    summaries_by_index: dict[int, str] = {
        int(record["order"]) - 1: str(record.get("summary", ""))
        for record in committed_records
        if "order" in record
    }

    async def summarize(index: int, item: PlannedSection) -> tuple[int, str]:
        async with semaphore:
            print(
                f"[Split] Summarizing chunk {index + 1}/{len(planned_sections)} "
                f"({item.plan.source_start}-{item.plan.source_end})"
            )
            summary = await provider(item.plan, source_lines)
            return index, summary

    remaining_tasks = [
        asyncio.create_task(summarize(index, item))
        for index, item in enumerate(planned_sections)
        if index not in summaries_by_index
    ]

    for future in tqdm(
        asyncio.as_completed(remaining_tasks),
        total=len(remaining_tasks),
        desc="Summarizing chunks",
        unit="chunk",
    ):
        index, summary = await future
        summaries_by_index[index] = summary

        item = planned_sections[index]
        updated_plan = item.plan.model_copy(update={"summary": summary})
        final_filename = numbered_output_filename(
            index=index + 1,
            total=len(planned_sections),
            filename=normalize_filename(
                filename=updated_plan.filename,
                title=updated_plan.title,
            ),
        )
        output_path = docs_dir / final_filename
        source_body = join_original_source_lines(
            source_lines[updated_plan.source_start - 1 : updated_plan.source_end]
        )

        write_concept_markdown_file(path=output_path, source_body=source_body)

        relative_filename = output_path.relative_to(output_root).as_posix()
        summary_text = (
            summary
            or f"Source lines {updated_plan.source_start}-{updated_plan.source_end}."
        )

        manifest_add_file_record(
            manifest=manifest,
            filename=relative_filename,
            title=updated_plan.title,
            summary=summary_text,
            source_start=updated_plan.source_start,
            source_end=updated_plan.source_end,
            order=index + 1,
        )
        manifest_add_chunk_record(
            manifest=manifest,
            filename=relative_filename,
            source_start=updated_plan.source_start,
            source_end=updated_plan.source_end,
            order=index + 1,
        )

        committed_records.append(
            {
                "order": index + 1,
                "filename": relative_filename,
                "title": updated_plan.title,
                "summary": summary_text,
                "source_start": updated_plan.source_start,
                "source_end": updated_plan.source_end,
                "header": item.header,
            }
        )
        write_json(progress_path, {"files": committed_records})
        write_coverage_json(
            path=planning_dir / "coverage.json",
            source_line_count=len(source_lines),
            files=[
                planned_sections[i].plan.model_copy(
                    update={"summary": summaries_by_index[i]}
                )
                for i in sorted(summaries_by_index)
            ],
            headers=[planned_sections[i].header for i in sorted(summaries_by_index)],
        )
        write_metadata_json(
            path=planning_dir / "metadata.json",
            original_file_name=source_file.name,
            inferred_file_name=inferred_filename_for_document(document_title),
            files=[
                planned_sections[i].plan.model_copy(
                    update={"summary": summaries_by_index[i]}
                )
                for i in sorted(summaries_by_index)
            ],
            headers=[planned_sections[i].header for i in sorted(summaries_by_index)],
        )
        print(f"[Split] Committed {relative_filename}")

    annotated: list[PlannedSection] = []
    for index, item in enumerate(planned_sections):
        summary = summaries_by_index[index]
        updated_plan = item.plan.model_copy(update={"summary": summary})
        annotated.append(PlannedSection(plan=updated_plan, header=item.header))

    return annotated


def output_dir_for_source(source_file: Path, output_root: Path) -> Path:
    return output_root / source_file.stem


def collect_source_files(source_path: Path) -> list[Path]:
    if source_path.is_file():
        if source_path.suffix.lower() != ".md":
            raise RuntimeError(f"Source file is not Markdown: {source_path}")
        return [source_path]

    if source_path.is_dir():
        files = sorted(source_path.glob("*.md"))
        if not files:
            raise RuntimeError(f"No .md files found in folder: {source_path}")
        return files

    raise RuntimeError(f"Source path does not exist: {source_path}")


def inferred_filename_for_document(document_title: str) -> str:
    return f"{slugify(document_title) or 'document'}.md"


async def process_source_file(
    *,
    source_file: Path,
    output_root: Path,
    max_lines: int,
    clean: bool,
    summary_provider: SummaryProvider,
) -> None:
    out_dir = output_dir_for_source(source_file, output_root)
    docs_dir = out_dir / "docs"
    planning_dir = out_dir / "_planning"
    progress_path = planning_dir / "progress.json"
    committed_records = read_progress_records(progress_path)
    should_resume = bool(committed_records)

    if clean and out_dir.exists() and not should_resume:
        shutil.rmtree(out_dir)
    elif out_dir.exists() and any(out_dir.iterdir()) and not should_resume:
        raise RuntimeError(
            f"{out_dir} already exists and is not empty. Use --clean to regenerate it."
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    planning_dir.mkdir(parents=True, exist_ok=True)

    source_lines = read_lines(source_file)
    document_title, planned_sections = build_plans_for_source(
        source_lines=source_lines,
        source_path=source_file,
        max_lines=max_lines,
    )
    if committed_records:
        print(f"[Split] Resuming from {len(committed_records)} committed chunks")
    manifest = init_manifest(source_file)
    planned_sections = await annotate_summaries(
        planned_sections=planned_sections,
        source_lines=source_lines,
        provider=summary_provider,
        max_concurrency=max(1, min(SUMMARY_CONCURRENCY, len(planned_sections) or 1)),
        progress_path=progress_path,
        docs_dir=docs_dir,
        planning_dir=planning_dir,
        output_root=output_root,
        manifest=manifest,
        source_file=source_file,
        document_title=document_title,
        committed_records=committed_records,
    )

    plans = [item.plan for item in planned_sections]
    headers = [item.header for item in planned_sections]
    coverage = []
    for index, item in enumerate(planned_sections, start=1):
        normalized = item.plan
        relative_filename = (
            (
                docs_dir
                / numbered_output_filename(
                    index=index,
                    total=len(planned_sections),
                    filename=normalize_filename(
                        filename=normalized.filename, title=normalized.title
                    ),
                )
            )
            .relative_to(out_dir)
            .as_posix()
        )
        summary = (
            normalized.summary
            or f"Source lines {normalized.source_start}-{normalized.source_end}."
        )
        manifest_add_file_record(
            manifest=manifest,
            filename=relative_filename,
            title=normalized.title,
            summary=summary,
            source_start=normalized.source_start,
            source_end=normalized.source_end,
            order=index,
        )
        manifest_add_chunk_record(
            manifest=manifest,
            filename=relative_filename,
            source_start=normalized.source_start,
            source_end=normalized.source_end,
            order=index,
        )
        coverage.append(
            {
                "order": index,
                "source_start": normalized.source_start,
                "source_end": normalized.source_end,
                "filename": relative_filename,
                "title": normalized.title,
                "summary": summary,
            }
        )

    assert_rendered_docs_match_source(
        source_lines=source_lines,
        coverage=coverage,
        output_root=out_dir,
    )

    write_concept_plan_document(
        path=planning_dir / "concept-plan.md",
        source_path=source_file,
        source_line_count=len(source_lines),
        files=plans,
    )
    write_coverage_json(
        path=planning_dir / "coverage.json",
        source_line_count=len(source_lines),
        files=plans,
        headers=headers,
    )
    write_metadata_json(
        path=planning_dir / "metadata.json",
        original_file_name=source_file.name,
        inferred_file_name=inferred_filename_for_document(document_title),
        files=plans,
        headers=headers,
    )

    print(f"[Split] Wrote {len(plans)} docs to {docs_dir}")


async def async_main() -> None:
    source_path = Path(SOURCE_PATH)
    output_root = Path(OUTPUT_ROOT)
    source_files = collect_source_files(source_path)
    llm = make_llm(
        model=GEN_MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        timeout=TIMEOUT,
    )

    async def provider(
        plan: ConceptFilePlan,
        source_lines: list[str],
    ) -> str:
        return await llm_summary_provider(
            llm=llm,
            plan=plan,
            source_lines=source_lines,
        )

    for source_file in source_files:
        print(f"[Split] Processing {source_file}")
        await process_source_file(
            source_file=source_file,
            output_root=output_root,
            max_lines=GENERATION_LINES,
            clean=CLEAN_OUTPUT,
            summary_provider=provider,
        )


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
