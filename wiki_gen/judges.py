from __future__ import annotations

import asyncio
from pathlib import Path

from wiki_new.llm import structured_ainvoke
from wiki_new.utils import write_json

from wiki_gen.models import (
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


def render_relevant_pages_for_chunk(pages: list[GeneratedPage], chunk: SourceChunk) -> str:
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
            f"{page.content}\n"
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

    async def run(chunk: SourceChunk) -> tuple[str, CoverageCheckResult]:
        async with semaphore:
            print(f"[Coverage] {chunk.chunk_id}")
            return chunk.chunk_id, await coverage_check_chunk(llm=llm, chunk=chunk, pages=pages)

    pairs = await asyncio.gather(*(run(chunk) for chunk in chunks))
    return dict(pairs)


def write_fact_check_audit(output_root: Path, results: dict[str, FactCheckResult]) -> None:
    write_json(
        output_root / "_planning" / "fact_check.json",
        {"pages": {slug: result.model_dump() for slug, result in sorted(results.items())}},
    )


def write_coverage_audit(output_root: Path, results: dict[str, CoverageCheckResult]) -> None:
    write_json(
        output_root / "_planning" / "line_coverage.json",
        {"chunks": {chunk_id: result.model_dump() for chunk_id, result in sorted(results.items())}},
    )
