from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

from wiki_gen.assign import assign_chunks_bounded, missing_ranges_for_chunk
from wiki_gen.catalog import load_catalog, write_catalog
from wiki_gen.generate import (
    build_page_plans,
    generate_page,
    generate_pages_bounded,
    hydrate_pages_with_cumulative_sources,
    write_page_metadata,
    write_page_sources,
    write_source_excerpt_page,
)
from wiki_gen.io import ensure_output_dirs, load_embed_corpus, write_planning_json
from wiki_gen.judges import (
    coverage_check_chunks_bounded,
    fact_check_pages_bounded,
    write_coverage_audit,
    write_fact_check_audit,
)
from wiki_gen.models import (
    API_KEY,
    ASSIGN_CONCURRENCY,
    BASE_URL,
    CLEAN_OUTPUT,
    COVERAGE_PAGE_CHAR_LIMIT,
    EMBED_ROOT,
    FACT_REPAIR_ATTEMPTS,
    GEN_MODEL,
    JUDGE_CONCURRENCY,
    OUTPUT_ROOT,
    PAGE_CONCURRENCY,
    RESEARCH_CONCURRENCY,
    RESEARCH_CONTEXT_LINES,
    TEMPERATURE,
    TIMEOUT,
    VERIFY_MODEL,
    CoverageCheckResult,
    FactCheckResult,
    GeneratedPage,
    PagePlan,
    SourceChunk,
    SourceSpan,
)
from wiki_gen.research import research_page_plan, research_page_plans_bounded
from wiki_new.llm import get_llm_cache_stats, make_llm
from wiki_new.utils import slugify, write_json


def write_doc_assignments(output_root: Path, assignments) -> None:
    by_doc: dict[str, list[dict]] = {}
    for item in assignments:
        by_doc.setdefault(item.doc_id, []).append(item.model_dump())

    for doc_id, rows in by_doc.items():
        write_json(
            output_root / "raw" / doc_id / "assignments.json", {"assignments": rows}
        )

    write_planning_json(
        output_root,
        "assignments.json",
        {"assignments": [item.model_dump() for item in assignments]},
    )


def write_assignment_coverage_gate(output_root: Path, chunks, assignments) -> None:
    by_chunk: dict[str, list] = {}
    for item in assignments:
        by_chunk.setdefault(item.chunk_id, []).append(item)

    rows = []
    for chunk in chunks:
        missing = missing_ranges_for_chunk(
            chunk=chunk,
            assignments=by_chunk.get(chunk.chunk_id, []),
        )
        rows.append(
            {
                "doc_id": chunk.doc_id,
                "chunk_id": chunk.chunk_id,
                "line_start": chunk.line_start,
                "line_end": chunk.line_end,
                "passed": not missing,
                "missing_ranges": [
                    {"line_start": start, "line_end": end} for start, end in missing
                ],
            }
        )
    write_planning_json(output_root, "assignment_coverage_gate.json", {"chunks": rows})


def write_indexes(output_root: Path, pages: list[GeneratedPage]) -> None:
    by_type: dict[str, list[GeneratedPage]] = {
        "summary": [],
        "entity": [],
        "concept": [],
    }
    for page in pages:
        by_type.setdefault(page.page_type, []).append(page)

    for items in by_type.values():
        items.sort(key=lambda page: page.title.lower())

    def page_link(page: GeneratedPage) -> str:
        rel = Path(page.path).relative_to(output_root).as_posix()
        return f"- [{page.title}](../{rel}) — {page.summary}"

    home = ["# Global Wiki", ""]
    home.append("## Document Summaries")
    home.extend(page_link(page) for page in by_type.get("summary", []))
    home.append("")
    home.append("## Entities")
    home.extend(page_link(page) for page in by_type.get("entity", []))
    home.append("")
    home.append("## Concepts")
    home.extend(page_link(page) for page in by_type.get("concept", []))
    home.append("")
    (output_root / "indexes" / "home.md").write_text("\n".join(home), encoding="utf-8")

    for page_type, filename, title in [
        ("entity", "entities.md", "Entities"),
        ("concept", "concepts.md", "Concepts"),
        ("summary", "summaries.md", "Document Summaries"),
    ]:
        lines = [f"# {title}", ""]
        lines.extend(page_link(page) for page in by_type.get(page_type, []))
        lines.append("")
        (output_root / "indexes" / filename).write_text(
            "\n".join(lines), encoding="utf-8"
        )


async def verify_repair_or_fallback_pages(
    *,
    gen_llm,
    verify_llm,
    plans_by_slug,
    pages: list[GeneratedPage],
    output_root: Path,
) -> tuple[list[GeneratedPage], dict[str, FactCheckResult]]:
    page_by_slug = {page.slug: page for page in pages}
    fact_results: dict[str, FactCheckResult] = {}

    for attempt in range(FACT_REPAIR_ATTEMPTS + 1):
        pages_for_judging = hydrate_pages_with_cumulative_sources(
            output_root=output_root,
            pages=sorted(page_by_slug.values(), key=lambda page: page.slug),
        )
        page_by_slug = {page.slug: page for page in pages_for_judging}
        fact_results = await fact_check_pages_bounded(
            llm=verify_llm,
            pages=pages_for_judging,
            concurrency=JUDGE_CONCURRENCY,
        )
        failed = [
            (slug, result)
            for slug, result in fact_results.items()
            if not result.passed and slug in plans_by_slug
        ]
        if not failed:
            return (
                sorted(page_by_slug.values(), key=lambda page: page.slug),
                fact_results,
            )

        if attempt >= FACT_REPAIR_ATTEMPTS:
            break

        print(
            f"[FactRepair] attempt {attempt + 1}/{FACT_REPAIR_ATTEMPTS}: "
            f"{len(failed)} page(s)"
        )
        semaphore = asyncio.Semaphore(max(1, min(PAGE_CONCURRENCY, len(failed))))

        async def run(slug, result):
            async with semaphore:
                print(f"[Repair] {slug}")
                plan = plans_by_slug[slug]
                current_page = page_by_slug.get(slug)
                if current_page is not None:
                    plan = plan.model_copy(
                        update={
                            "source_spans": current_page.source_spans
                            or plan.source_spans,
                            "existing_content": current_page.content
                            or plan.existing_content,
                            "research_reports": [],
                        }
                    )
                plan = await research_page_plan(
                    llm=gen_llm,
                    plan=plan,
                    concurrency=RESEARCH_CONCURRENCY,
                )
                return await generate_page(
                    llm=gen_llm,
                    plan=plan,
                    output_root=output_root,
                    repair_instruction=result.repair_instruction or result.reason,
                )

        repaired_pages = await asyncio.gather(
            *(run(slug, result) for slug, result in failed)
        )
        for page in repaired_pages:
            page_by_slug[page.slug] = page
        write_page_sources(output_root, repaired_pages)
        write_page_metadata(output_root, repaired_pages)

    exhausted = [
        (slug, result)
        for slug, result in fact_results.items()
        if not result.passed and slug in plans_by_slug
    ]
    if exhausted:
        print(
            "[FactFallback] replacing "
            f"{len(exhausted)} unverified page(s) with source excerpts"
        )
    for slug, result in exhausted:
        plan = plans_by_slug[slug]
        current_page = page_by_slug.get(slug)
        if current_page is not None:
            plan = plan.model_copy(
                update={
                    "source_spans": current_page.source_spans or plan.source_spans,
                    "existing_content": current_page.content or plan.existing_content,
                }
            )
        fallback_page = write_source_excerpt_page(
            plan=plan,
            output_root=output_root,
            reason=(
                f"fact-check repair exhausted after {FACT_REPAIR_ATTEMPTS} "
                f"attempt(s): {result.repair_instruction or result.reason}"
            ),
        )
        page_by_slug[slug] = fallback_page
        fact_results[slug] = FactCheckResult(
            passed=True,
            reason=(
                "Deterministic source-excerpt fallback after fact-check repair "
                "exhaustion; content is verbatim source evidence with original "
                "line citations."
            ),
        )

    final_pages = sorted(page_by_slug.values(), key=lambda page: page.slug)
    write_page_sources(output_root, final_pages)
    write_page_metadata(output_root, final_pages)
    return final_pages, fact_results


def fallback_plan_for_chunk(chunk: SourceChunk, reason: str) -> PagePlan:
    title = f"{chunk.doc_id} Source Lines {chunk.line_start}-{chunk.line_end}"
    return PagePlan(
        slug=f"concept/{slugify(title)}",
        page_type="concept",
        title=title,
        summary=(
            "Verbatim source-backed fallback page preserving chunk coverage. "
            f"Trigger: {reason}"
        ),
        aliases=[],
        source_spans=[
            SourceSpan(
                doc_id=chunk.doc_id,
                source_path=chunk.source_path,
                line_start=chunk.line_start,
                line_end=chunk.line_end,
                text=chunk.text,
            )
        ],
        existing_content="",
    )


def apply_coverage_fallbacks(
    *,
    output_root: Path,
    chunks: list[SourceChunk],
    pages: list[GeneratedPage],
    coverage_results: dict[str, CoverageCheckResult],
) -> tuple[list[GeneratedPage], dict[str, CoverageCheckResult], list[GeneratedPage]]:
    page_by_slug = {page.slug: page for page in pages}
    chunk_by_id = {chunk.chunk_id: chunk for chunk in chunks}

    failed = [
        (chunk_id, result)
        for chunk_id, result in coverage_results.items()
        if not result.passed and chunk_id in chunk_by_id
    ]
    if not failed:
        return pages, coverage_results, []

    print(f"[CoverageFallback] adding {len(failed)} whole-chunk fallback page(s)")
    fallback_pages: list[GeneratedPage] = []
    for chunk_id, result in failed:
        chunk = chunk_by_id[chunk_id]
        plan = fallback_plan_for_chunk(
            chunk,
            result.repair_instruction or result.reason,
        )
        page = write_source_excerpt_page(
            plan=plan,
            output_root=output_root,
            reason=(
                "coverage judge reported missing representation after normal "
                f"generation: {result.repair_instruction or result.reason}"
            ),
        )
        page_by_slug[page.slug] = page
        fallback_pages.append(page)
        coverage_results[chunk_id] = CoverageCheckResult(
            passed=True,
            reason=(
                "Deterministic whole-chunk source fallback added after coverage "
                "judge failure; the full chunk is now represented verbatim with "
                "original line citations."
            ),
        )

    write_page_sources(output_root, fallback_pages)
    write_page_metadata(output_root, fallback_pages)
    return (
        sorted(page_by_slug.values(), key=lambda page: page.slug),
        coverage_results,
        fallback_pages,
    )


async def async_main() -> None:
    embed_root = Path(EMBED_ROOT)
    output_root = Path(OUTPUT_ROOT)

    if CLEAN_OUTPUT and output_root.exists():
        shutil.rmtree(output_root)
    ensure_output_dirs(output_root)

    print(f"[WikiGen] embed root:  {embed_root}")
    print(f"[WikiGen] output root: {output_root}")
    research_context = (
        "full documents"
        if RESEARCH_CONTEXT_LINES < 0
        else f"+/-{RESEARCH_CONTEXT_LINES} source lines"
    )
    print(
        "[WikiGen] concurrency: "
        f"assign={ASSIGN_CONCURRENCY} page={PAGE_CONCURRENCY} "
        f"research={RESEARCH_CONCURRENCY} judge={JUDGE_CONCURRENCY}"
    )
    print(
        "[WikiGen] prompt limits: "
        f"research_context={research_context} "
        f"coverage_page_chars={COVERAGE_PAGE_CHAR_LIMIT}"
    )
    print(
        "[WikiGen] LLM cache: "
        "enabled unless WIKI_LLM_CACHE=0; "
        "low-risk stages use non-thinking; page writing retries thinking "
        "then falls back to non-thinking"
    )

    docs = load_embed_corpus(embed_root, output_root)
    all_chunks = [chunk for doc in docs for chunk in doc.chunks]
    print(f"[WikiGen] loaded {len(docs)} embedded doc(s), {len(all_chunks)} chunk(s)")

    gen_llm = make_llm(
        model=GEN_MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        timeout=TIMEOUT,
    )
    verify_llm = make_llm(
        model=VERIFY_MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=0.0,
        timeout=TIMEOUT,
    )

    catalog = load_catalog(output_root)
    print(f"[WikiGen] existing catalog pages: {len(catalog)}")

    all_assignments = []
    page_by_slug: dict[str, GeneratedPage] = {}
    plans_by_slug = {}

    for doc in docs:
        print("=" * 80)
        print(f"[WikiGen] document: {doc.doc_id} chunks={len(doc.chunks)}")
        print(f"[WikiGen] catalog visible to pass 0: {len(catalog)} page(s)")
        print("=" * 80)

        doc_assignments = await assign_chunks_bounded(
            llm=gen_llm,
            chunks=doc.chunks,
            catalog=catalog,
            concurrency=ASSIGN_CONCURRENCY,
        )
        all_assignments.extend(doc_assignments)

        chunks_by_id = {chunk.chunk_id: chunk for chunk in doc.chunks}
        plans = build_page_plans(doc_assignments, chunks_by_id, output_root)
        plans = await research_page_plans_bounded(
            llm=gen_llm,
            plans=plans,
            page_concurrency=PAGE_CONCURRENCY,
            subagent_concurrency=RESEARCH_CONCURRENCY,
        )
        plans_by_slug.update({plan.slug: plan for plan in plans})
        print(
            f"[WikiGen] {doc.doc_id}: assignments={len(doc_assignments)} page_plans={len(plans)}"
        )

        doc_pages = await generate_pages_bounded(
            llm=gen_llm,
            plans=plans,
            output_root=output_root,
            concurrency=PAGE_CONCURRENCY,
        )
        write_page_sources(output_root, doc_pages)
        write_page_metadata(output_root, doc_pages)

        for page in doc_pages:
            page_by_slug[page.slug] = page

        # Refresh the global catalog after each document so later pass-0
        # agents can assimilate into pages generated by earlier documents.
        catalog = write_catalog(output_root, list(page_by_slug.values()))

    assignments = all_assignments
    pages = sorted(page_by_slug.values(), key=lambda page: page.slug)
    print(f"[WikiGen] assignments: {len(assignments)}")
    print(f"[WikiGen] generated/updated pages: {len(pages)}")
    write_doc_assignments(output_root, assignments)
    write_assignment_coverage_gate(output_root, all_chunks, assignments)

    pages, fact_results = await verify_repair_or_fallback_pages(
        gen_llm=gen_llm,
        verify_llm=verify_llm,
        plans_by_slug=plans_by_slug,
        pages=pages,
        output_root=output_root,
    )
    write_page_sources(output_root, pages)
    write_page_metadata(output_root, pages)
    pages_for_judging = hydrate_pages_with_cumulative_sources(
        output_root=output_root,
        pages=pages,
    )

    coverage_results = await coverage_check_chunks_bounded(
        llm=verify_llm,
        chunks=all_chunks,
        pages=pages_for_judging,
        concurrency=JUDGE_CONCURRENCY,
    )
    pages, coverage_results, coverage_fallback_pages = apply_coverage_fallbacks(
        output_root=output_root,
        chunks=all_chunks,
        pages=pages_for_judging,
        coverage_results=coverage_results,
    )
    for page in coverage_fallback_pages:
        fact_results[page.slug] = FactCheckResult(
            passed=True,
            reason=(
                "Deterministic whole-chunk source fallback after coverage "
                "failure; content is verbatim source evidence with original "
                "line citations."
            ),
        )
    pages_for_judging = hydrate_pages_with_cumulative_sources(
        output_root=output_root,
        pages=pages,
    )
    write_fact_check_audit(output_root, fact_results)
    write_coverage_audit(output_root, coverage_results)

    catalog = write_catalog(output_root, pages)
    write_indexes(output_root, pages)

    write_planning_json(
        output_root,
        "run_manifest.json",
        {
            "embed_root": str(embed_root),
            "output_root": str(output_root),
            "documents": [doc.model_dump(exclude={"chunks"}) for doc in docs],
            "chunk_count": len(all_chunks),
            "assignment_count": len(assignments),
            "page_count": len(pages),
            "catalog_count": len(catalog),
            "llm_cache": get_llm_cache_stats(),
        },
    )

    print(f"[WikiGen] LLM cache stats: {get_llm_cache_stats()}")
    print(f"[WikiGen] done: {len(pages)} page(s), {len(catalog)} catalog entry(s)")


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
