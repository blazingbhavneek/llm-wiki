from __future__ import annotations

import asyncio
import json
from typing import Iterable

from wiki_new.llm import structured_ainvoke
from wiki_new.utils import slugify

from wiki_gen.catalog import shortlist_catalog
from wiki_gen.models import (
    ASSIGN_REPAIR_ATTEMPTS,
    MAX_CATALOG_ITEMS,
    AssignmentSpan,
    ChunkAssignmentResult,
    SourceChunk,
    WikiAssignment,
    WikiCatalogEntry,
)
from wiki_gen.prompts import build_assignment_prompt, build_assignment_repair_prompt


def _slug_for_assignment(chunk: SourceChunk, item: AssignmentSpan) -> str:
    if item.target_slug:
        return item.target_slug.strip()

    page_type = item.page_type or "concept"
    title = item.title or chunk.title or f"{chunk.doc_id} lines {item.line_start}-{item.line_end}"
    prefix = "entity" if page_type == "entity" else "summary" if page_type == "summary" else "concept"
    return f"{prefix}/{slugify(title)}"


def _fallback_assignment(chunk: SourceChunk, start: int, end: int, reason: str) -> WikiAssignment:
    title = f"{chunk.doc_id} Source Lines {start}-{end}"
    return WikiAssignment(
        doc_id=chunk.doc_id,
        chunk_id=chunk.chunk_id,
        line_start=start,
        line_end=end,
        action="new_page",
        page_type="concept",
        target_slug=f"concept/{slugify(title)}",
        title=title,
        summary="Fallback page created to preserve source coverage.",
        reason=reason,
        generated_by_fallback=True,
    )


def missing_ranges_for_chunk(
    *,
    chunk: SourceChunk,
    assignments: Iterable[WikiAssignment],
) -> list[tuple[int, int]]:
    intervals: list[tuple[int, int]] = []
    for item in assignments:
        start = max(chunk.line_start, int(item.line_start))
        end = min(chunk.line_end, int(item.line_end))
        if start <= end:
            intervals.append((start, end))

    if not intervals:
        return [(chunk.line_start, chunk.line_end)]

    intervals.sort()
    merged: list[tuple[int, int]] = []
    for start, end in intervals:
        if not merged or start > merged[-1][1] + 1:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))

    missing: list[tuple[int, int]] = []
    cursor = chunk.line_start
    for start, end in merged:
        if cursor < start:
            missing.append((cursor, start - 1))
        cursor = max(cursor, end + 1)
    if cursor <= chunk.line_end:
        missing.append((cursor, chunk.line_end))
    return missing


def normalize_assignments(
    *,
    chunk: SourceChunk,
    result: ChunkAssignmentResult,
) -> list[WikiAssignment]:
    normalized: list[WikiAssignment] = []
    for item in result.assignments:
        start = max(chunk.line_start, int(item.line_start))
        end = min(chunk.line_end, int(item.line_end))
        if start > end:
            continue

        action = item.action
        page_type = item.page_type
        target_slug = _slug_for_assignment(chunk, item) if action != "ignore" else None
        title = item.title or chunk.title

        if action != "ignore" and page_type is None:
            page_type = "concept"

        normalized.append(
            WikiAssignment(
                doc_id=chunk.doc_id,
                chunk_id=chunk.chunk_id,
                line_start=start,
                line_end=end,
                action=action,
                page_type=page_type,
                target_slug=target_slug,
                title=title,
                aliases=item.aliases,
                summary=item.summary,
                reason=item.reason,
            )
        )

    normalized.sort(key=lambda item: (item.line_start, item.line_end, item.target_slug or ""))
    return normalized


async def assign_chunk(
    *,
    llm,
    chunk: SourceChunk,
    catalog: list[WikiCatalogEntry],
) -> list[WikiAssignment]:
    shortlist = shortlist_catalog(chunk.text, catalog, limit=MAX_CATALOG_ITEMS)
    try:
        raw = await structured_ainvoke(
            llm,
            ChunkAssignmentResult,
            build_assignment_prompt(
                chunk=chunk,
                catalog=shortlist,
            ),
            max_output_tokens=3000,
        )
        result = ChunkAssignmentResult.model_validate(raw)
    except Exception as exc:  # noqa: BLE001 - fallback preserves coverage
        return [
            _fallback_assignment(
                chunk,
                chunk.line_start,
                chunk.line_end,
                f"assignment agent failed: {exc}",
            )
        ]

    assignments = normalize_assignments(chunk=chunk, result=result)
    missing = missing_ranges_for_chunk(chunk=chunk, assignments=assignments)

    for _ in range(ASSIGN_REPAIR_ATTEMPTS):
        if not missing:
            break
        try:
            raw = await structured_ainvoke(
                llm,
                ChunkAssignmentResult,
                build_assignment_repair_prompt(
                    chunk=chunk,
                    previous_json=json.dumps(
                        [item.model_dump() for item in assignments],
                        ensure_ascii=False,
                        indent=2,
                    ),
                    missing_ranges=missing,
                    catalog=shortlist,
                ),
                max_output_tokens=3000,
            )
            repaired = ChunkAssignmentResult.model_validate(raw)
            assignments = normalize_assignments(chunk=chunk, result=repaired)
            missing = missing_ranges_for_chunk(chunk=chunk, assignments=assignments)
        except Exception:
            break

    if missing:
        return [
            _fallback_assignment(
                chunk,
                chunk.line_start,
                chunk.line_end,
                (
                    "assignment coverage repair failed after "
                    f"{ASSIGN_REPAIR_ATTEMPTS} attempt(s); deterministic "
                    "fallback preserved the whole chunk"
                ),
            )
        ]

    assignments.sort(key=lambda item: (item.line_start, item.line_end, item.target_slug or ""))
    return assignments


async def assign_chunks_bounded(
    *,
    llm,
    chunks: list[SourceChunk],
    catalog: list[WikiCatalogEntry],
    concurrency: int,
) -> list[WikiAssignment]:
    semaphore = asyncio.Semaphore(concurrency)

    async def run(chunk: SourceChunk) -> list[WikiAssignment]:
        async with semaphore:
            print(f"[Assign] {chunk.chunk_id} lines {chunk.line_start}-{chunk.line_end}")
            return await assign_chunk(llm=llm, chunk=chunk, catalog=catalog)

    nested = await asyncio.gather(*(run(chunk) for chunk in chunks))
    return [item for group in nested for item in group]
