from __future__ import annotations

import asyncio
import re
from pathlib import Path

from wiki_gen.models import (
    COVERAGE_EXCERPT_CONTEXT_LINES,
    COVERAGE_PAGE_CHAR_LIMIT,
    CoverageCheckResult,
    FactCheckResult,
    GeneratedPage,
    SourceChunk,
)
from wiki_gen.prompts import (
    build_coverage_check_prompt,
    build_fact_check_prompt,
    render_source_spans,
)
from wiki_new.llm import structured_ainvoke
from wiki_new.utils import write_json

SOURCE_REF_RE = re.compile(r"\[([A-Za-z0-9_.-]+):L(\d+)-L(\d+)\]")


async def fact_check_page(*, llm, page: GeneratedPage) -> FactCheckResult:
    try:
        raw = await structured_ainvoke(
            llm,
            FactCheckResult,
            build_fact_check_prompt(
                page_slug=page.slug,
                page_content=page.content,
                source_blocks=render_source_spans(page.source_spans),
            ),
            max_output_tokens=1800,
            phase=f"wiki_gen.fact_check.{page.slug}",
            enable_thinking=False,
        )
        return FactCheckResult.model_validate(raw)
    except Exception as exc:  # noqa: BLE001
        return FactCheckResult(
            passed=False,
            repair_instruction=f"Fact-check judge failed; conservatively regenerate closer to cited source. Error: {exc}",
            reason=str(exc),
        )


async def fact_check_pages_bounded(
    *,
    llm,
    pages: list[GeneratedPage],
    concurrency: int,
) -> dict[str, FactCheckResult]:
    semaphore = asyncio.Semaphore(concurrency)

    async def run(page: GeneratedPage) -> tuple[str, FactCheckResult]:
        async with semaphore:
            print(f"[FactCheck] {page.slug}")
            return page.slug, await fact_check_page(llm=llm, page=page)

    pairs = await asyncio.gather(*(run(page) for page in pages))
    return dict(pairs)


def page_overlaps_chunk(page: GeneratedPage, chunk: SourceChunk) -> bool:
    for span in page.source_spans:
        if span.doc_id != chunk.doc_id:
            continue
        if span.line_start <= chunk.line_end and chunk.line_start <= span.line_end:
            return True
    return False


def build_pages_by_doc(pages: list[GeneratedPage]) -> dict[str, list[GeneratedPage]]:
    by_doc: dict[str, list[GeneratedPage]] = {}
    for page in pages:
        for doc_id in sorted({span.doc_id for span in page.source_spans}):
            by_doc.setdefault(doc_id, []).append(page)
    return by_doc


def _citation_overlaps_chunk(match: re.Match[str], chunk: SourceChunk) -> bool:
    doc_id, start_raw, end_raw = match.groups()
    if doc_id != chunk.doc_id:
        return False
    start = int(start_raw)
    end = int(end_raw)
    return start <= chunk.line_end and chunk.line_start <= end


def _excerpt_page_content(page: GeneratedPage, chunk: SourceChunk) -> str:
    content = page.content
    if len(content) <= COVERAGE_PAGE_CHAR_LIMIT:
        return content

    lines = content.splitlines()
    selected: set[int] = set()
    radius = max(0, COVERAGE_EXCERPT_CONTEXT_LINES)

    for index, line in enumerate(lines):
        if any(
            _citation_overlaps_chunk(match, chunk)
            for match in SOURCE_REF_RE.finditer(line)
        ):
            for line_index in range(
                max(0, index - radius), min(len(lines), index + radius + 1)
            ):
                selected.add(line_index)

    if not selected:
        return content[:COVERAGE_PAGE_CHAR_LIMIT].rstrip() + "\n...[truncated]"

    excerpt_lines: list[str] = []
    previous = -2
    for index in sorted(selected):
        if index != previous + 1 and excerpt_lines:
            excerpt_lines.append("...")
        excerpt_lines.append(lines[index])
        previous = index

    excerpt = "\n".join(excerpt_lines)
    if len(excerpt) > COVERAGE_PAGE_CHAR_LIMIT:
        excerpt = excerpt[:COVERAGE_PAGE_CHAR_LIMIT].rstrip() + "\n...[truncated]"
    return excerpt


def render_relevant_pages_for_chunk(
    pages: list[GeneratedPage], chunk: SourceChunk
) -> str:
    blocks: list[str] = []
    for page in pages:
        if not page_overlaps_chunk(page, chunk):
            continue
        refs = [
            span.ref
            for span in page.source_spans
            if span.doc_id == chunk.doc_id
            and span.line_start <= chunk.line_end
            and chunk.line_start <= span.line_end
        ]
        blocks.append(
            f"<page slug={page.slug!r} title={page.title!r} refs={refs}>\n"
            f"{_excerpt_page_content(page, chunk)}\n"
            "</page>"
        )
    return "\n\n".join(blocks)


async def coverage_check_chunk(
    *,
    llm,
    chunk: SourceChunk,
    pages: list[GeneratedPage],
) -> CoverageCheckResult:
    relevant = render_relevant_pages_for_chunk(pages, chunk)
    try:
        raw = await structured_ainvoke(
            llm,
            CoverageCheckResult,
            build_coverage_check_prompt(
                chunk=chunk,
                relevant_pages=relevant,
            ),
            max_output_tokens=1800,
            phase=f"wiki_gen.coverage.{chunk.doc_id}",
            enable_thinking=False,
        )
        return CoverageCheckResult.model_validate(raw)
    except Exception as exc:  # noqa: BLE001
        return CoverageCheckResult(
            passed=False,
            repair_instruction=f"Coverage judge failed for {chunk.chunk_id}: {exc}",
            reason=str(exc),
        )


async def coverage_check_chunks_bounded(
    *,
    llm,
    chunks: list[SourceChunk],
    pages: list[GeneratedPage],
    concurrency: int,
) -> dict[str, CoverageCheckResult]:
    semaphore = asyncio.Semaphore(concurrency)
    pages_by_doc = build_pages_by_doc(pages)

    async def run(chunk: SourceChunk) -> tuple[str, CoverageCheckResult]:
        async with semaphore:
            print(f"[Coverage] {chunk.chunk_id}")
            return chunk.chunk_id, await coverage_check_chunk(
                llm=llm,
                chunk=chunk,
                pages=pages_by_doc.get(chunk.doc_id, []),
            )

    pairs = await asyncio.gather(*(run(chunk) for chunk in chunks))
    return dict(pairs)


def write_fact_check_audit(
    output_root: Path, results: dict[str, FactCheckResult]
) -> None:
    write_json(
        output_root / "_planning" / "fact_check.json",
        {
            "pages": {
                slug: result.model_dump() for slug, result in sorted(results.items())
            }
        },
    )


def write_coverage_audit(
    output_root: Path, results: dict[str, CoverageCheckResult]
) -> None:
    write_json(
        output_root / "_planning" / "line_coverage.json",
        {
            "chunks": {
                chunk_id: result.model_dump()
                for chunk_id, result in sorted(results.items())
            }
        },
    )
