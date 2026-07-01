from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path

from wiki_gen.assign import assign_chunk, missing_ranges_for_chunk
from wiki_gen.catalog import load_catalog, write_catalog
from wiki_gen.generate import (
    build_page_plans,
    generate_page,
    hydrate_pages_with_cumulative_sources,
    write_page_metadata,
    write_page_sources,
    write_source_excerpt_page,
)
from wiki_gen.io import ensure_output_dirs, load_embed_corpus, write_planning_json
from wiki_gen.judges import (
    build_pages_by_doc,
    coverage_check_chunk,
    fact_check_page,
    write_coverage_audit,
    write_fact_check_audit,
)
from wiki_gen.models import (
    API_KEY,
    BASE_URL,
    CLEAN_OUTPUT,
    CONCURRENCY,
    COVERAGE_PAGE_CHAR_LIMIT,
    EMBED_ROOT,
    FACT_REPAIR_ATTEMPTS,
    GEN_MODEL,
    OUTPUT_ROOT,
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
    WikiAssignment,
)
from wiki_gen.progress import (
    add_done,
    done_set,
    is_complete,
    load_progress,
    mark_complete,
    save_progress,
)
from wiki_gen.research import research_page_plan
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
        fact_results = await fact_check_all(
            llm=verify_llm,
            pages=pages_for_judging,
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
        async def run(slug, result):
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
            plan = await research_page_plan(llm=gen_llm, plan=plan)
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


# ---------------------------------------------------------------------
# Stage plumbing: flat task lists, one global concurrency gate (enforced in
# wiki_new.llm), resumable via _planning/progress.json.
# ---------------------------------------------------------------------

PAGE_PLANS_FILE = "page_plans.json"


def load_persisted_assignments(output_root: Path) -> list[WikiAssignment]:
    path = output_root / "_planning" / "assignments.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    out: list[WikiAssignment] = []
    for row in data.get("assignments", []):
        try:
            out.append(WikiAssignment.model_validate(row))
        except Exception:  # noqa: BLE001 - skip corrupt rows
            continue
    return out


def load_persisted_plans(output_root: Path) -> dict[str, PagePlan]:
    path = output_root / "_planning" / PAGE_PLANS_FILE
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out: dict[str, PagePlan] = {}
    for row in data.get("plans", []):
        try:
            plan = PagePlan.model_validate(row)
        except Exception:  # noqa: BLE001
            continue
        out[plan.slug] = plan
    return out


def save_persisted_plans(output_root: Path, plans_by_slug: dict[str, PagePlan]) -> None:
    write_planning_json(
        output_root,
        PAGE_PLANS_FILE,
        {"plans": [plans_by_slug[slug].model_dump() for slug in sorted(plans_by_slug)]},
    )


def load_fact_results(output_root: Path) -> dict[str, FactCheckResult]:
    path = output_root / "_planning" / "fact_check.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out: dict[str, FactCheckResult] = {}
    for slug, row in (data.get("pages") or {}).items():
        try:
            out[slug] = FactCheckResult.model_validate(row)
        except Exception:  # noqa: BLE001
            continue
    return out


def load_coverage_results(output_root: Path) -> dict[str, CoverageCheckResult]:
    path = output_root / "_planning" / "line_coverage.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out: dict[str, CoverageCheckResult] = {}
    for chunk_id, row in (data.get("chunks") or {}).items():
        try:
            out[chunk_id] = CoverageCheckResult.model_validate(row)
        except Exception:  # noqa: BLE001
            continue
    return out


async def fact_check_all(
    *, llm, pages: list[GeneratedPage]
) -> dict[str, FactCheckResult]:
    async def run(page: GeneratedPage) -> tuple[str, FactCheckResult]:
        print(f"[FactCheck] {page.slug}")
        return page.slug, await fact_check_page(llm=llm, page=page)

    pairs = await asyncio.gather(*(run(page) for page in pages))
    return dict(pairs)


async def coverage_check_all(
    *, llm, chunks: list[SourceChunk], pages: list[GeneratedPage]
) -> dict[str, CoverageCheckResult]:
    pages_by_doc = build_pages_by_doc(pages)

    async def run(chunk: SourceChunk) -> tuple[str, CoverageCheckResult]:
        print(f"[Coverage] {chunk.chunk_id}")
        return chunk.chunk_id, await coverage_check_chunk(
            llm=llm,
            chunk=chunk,
            pages=pages_by_doc.get(chunk.doc_id, []),
        )

    pairs = await asyncio.gather(*(run(chunk) for chunk in chunks))
    return dict(pairs)


async def stage_assign(
    *,
    llm,
    chunks: list[SourceChunk],
    catalog,
    output_root: Path,
    progress: dict,
    progress_lock: asyncio.Lock,
) -> list[WikiAssignment]:
    if is_complete(progress, "assign"):
        print("[Stage:assign] complete; loading persisted assignments")
        return load_persisted_assignments(output_root)

    by_chunk: dict[str, list[WikiAssignment]] = {}
    for item in load_persisted_assignments(output_root):
        by_chunk.setdefault(item.chunk_id, []).append(item)

    done = done_set(progress, "assign")
    todo = [chunk for chunk in chunks if chunk.chunk_id not in done]
    print(f"[Stage:assign] {len(todo)} to do, {len(done)} done, {len(chunks)} total")

    io_lock = asyncio.Lock()

    def flatten() -> list[WikiAssignment]:
        return [item for group in by_chunk.values() for item in group]

    async def run(chunk: SourceChunk) -> None:
        result = await assign_chunk(llm=llm, chunk=chunk, catalog=catalog)
        async with io_lock:
            by_chunk[chunk.chunk_id] = result
            write_doc_assignments(output_root, flatten())
        async with progress_lock:
            add_done(progress, "assign", chunk.chunk_id)
            save_progress(output_root, progress)
        print(f"[Assign] {chunk.chunk_id} -> {len(result)} assignment(s)")

    await asyncio.gather(*(run(chunk) for chunk in todo))

    async with progress_lock:
        mark_complete(progress, "assign")
        save_progress(output_root, progress)
    return flatten()


async def stage_research(
    *,
    llm,
    plans: list[PagePlan],
    output_root: Path,
    progress: dict,
    progress_lock: asyncio.Lock,
) -> list[PagePlan]:
    out_by_slug: dict[str, PagePlan] = {plan.slug: plan for plan in plans}
    for slug, plan in load_persisted_plans(output_root).items():
        if slug in out_by_slug:
            out_by_slug[slug] = plan

    if is_complete(progress, "research"):
        print("[Stage:research] complete; loading persisted plans")
        return [out_by_slug[plan.slug] for plan in plans]

    done = done_set(progress, "research")
    todo = [plan for plan in plans if plan.slug not in done]
    print(f"[Stage:research] {len(todo)} to do, {len(done)} done, {len(plans)} total")

    io_lock = asyncio.Lock()

    async def run(plan: PagePlan) -> None:
        researched = await research_page_plan(llm=llm, plan=plan)
        async with io_lock:
            out_by_slug[plan.slug] = researched
            save_persisted_plans(output_root, out_by_slug)
        async with progress_lock:
            add_done(progress, "research", plan.slug)
            save_progress(output_root, progress)
        print(f"[Research] {plan.slug} done")

    await asyncio.gather(*(run(plan) for plan in todo))

    async with progress_lock:
        mark_complete(progress, "research")
        save_progress(output_root, progress)
    return [out_by_slug[plan.slug] for plan in plans]


async def stage_generate(
    *,
    llm,
    plans: list[PagePlan],
    output_root: Path,
    progress: dict,
    progress_lock: asyncio.Lock,
) -> list[GeneratedPage]:
    done = done_set(progress, "generate")
    remaining = sum(1 for plan in plans if plan.slug not in done)
    print(f"[Stage:generate] {remaining} to do, {len(plans) - remaining} cached/done")

    pages_by_slug: dict[str, GeneratedPage] = {}
    io_lock = asyncio.Lock()

    async def run(plan: PagePlan) -> None:
        page = await generate_page(llm=llm, plan=plan, output_root=output_root)
        async with io_lock:
            pages_by_slug[plan.slug] = page
            write_page_sources(output_root, [page])
            write_page_metadata(output_root, [page])
        async with progress_lock:
            add_done(progress, "generate", plan.slug)
            save_progress(output_root, progress)
        print(f"[Page] {plan.slug} spans={len(plan.source_spans)}")

    await asyncio.gather(*(run(plan) for plan in plans))

    async with progress_lock:
        mark_complete(progress, "generate")
        save_progress(output_root, progress)
    return sorted(pages_by_slug.values(), key=lambda page: page.slug)


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
    print(f"[WikiGen] concurrency: {CONCURRENCY} (single global gate)")
    print(
        "[WikiGen] prompt limits: "
        f"research_context={research_context} "
        f"coverage_page_chars={COVERAGE_PAGE_CHAR_LIMIT}"
    )
    print(
        "[WikiGen] LLM cache: enabled unless WIKI_LLM_CACHE=0; "
        "page writing retries thinking then falls back to non-thinking"
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

    progress = load_progress(output_root)
    progress_lock = asyncio.Lock()

    # -- Stage 1: assign every chunk across every document -----------------
    assignments = await stage_assign(
        llm=gen_llm,
        chunks=all_chunks,
        catalog=catalog,
        output_root=output_root,
        progress=progress,
        progress_lock=progress_lock,
    )
    write_assignment_coverage_gate(output_root, all_chunks, assignments)
    print(f"[WikiGen] assignments: {len(assignments)}")

    # -- Stage 2: build page plans (deterministic, global grouping) --------
    chunks_by_id = {chunk.chunk_id: chunk for chunk in all_chunks}
    plans = build_page_plans(assignments, chunks_by_id, output_root)
    print(f"[WikiGen] page plans: {len(plans)}")

    # -- Stage 3: research every plan --------------------------------------
    plans = await stage_research(
        llm=gen_llm,
        plans=plans,
        output_root=output_root,
        progress=progress,
        progress_lock=progress_lock,
    )
    plans_by_slug = {plan.slug: plan for plan in plans}

    # -- Stage 4: generate every page --------------------------------------
    pages = await stage_generate(
        llm=gen_llm,
        plans=plans,
        output_root=output_root,
        progress=progress,
        progress_lock=progress_lock,
    )
    catalog = write_catalog(output_root, pages)
    print(f"[WikiGen] generated/updated pages: {len(pages)}")

    # -- Stage 5: fact-check, repair, deterministic fallback ---------------
    if is_complete(progress, "factcheck"):
        print("[Stage:factcheck] complete; skipping")
        fact_results = load_fact_results(output_root)
        pages = hydrate_pages_with_cumulative_sources(
            output_root=output_root, pages=pages
        )
    else:
        pages, fact_results = await verify_repair_or_fallback_pages(
            gen_llm=gen_llm,
            verify_llm=verify_llm,
            plans_by_slug=plans_by_slug,
            pages=pages,
            output_root=output_root,
        )
        write_page_sources(output_root, pages)
        write_page_metadata(output_root, pages)
        write_fact_check_audit(output_root, fact_results)
        async with progress_lock:
            mark_complete(progress, "factcheck")
            save_progress(output_root, progress)

    pages_for_judging = hydrate_pages_with_cumulative_sources(
        output_root=output_root,
        pages=pages,
    )

    # -- Stage 6: coverage check + whole-chunk fallback --------------------
    if is_complete(progress, "coverage"):
        print("[Stage:coverage] complete; skipping")
        coverage_results = load_coverage_results(output_root)
        pages = pages_for_judging
    else:
        coverage_results = await coverage_check_all(
            llm=verify_llm,
            chunks=all_chunks,
            pages=pages_for_judging,
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
        async with progress_lock:
            mark_complete(progress, "coverage")
            save_progress(output_root, progress)

    # -- Finalize ----------------------------------------------------------
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
    async with progress_lock:
        mark_complete(progress, "finalize")
        save_progress(output_root, progress)

    print(f"[WikiGen] LLM cache stats: {get_llm_cache_stats()}")
    print(f"[WikiGen] done: {len(pages)} page(s), {len(catalog)} catalog entry(s)")


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
