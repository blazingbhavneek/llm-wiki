from __future__ import annotations

import asyncio
from pathlib import Path

from wiki_gen.models import (
    RESEARCH_CONTEXT_LINES,
    PagePlan,
    PageResearchReport,
    ResearchFact,
    SourceSpan,
)
from wiki_gen.prompts import build_page_research_prompt, render_source_spans
from wiki_new.llm import structured_ainvoke
from wiki_new.utils import numbered_source_lines, read_lines


def fallback_research_report(
    plan: PagePlan, doc_id: str, reason: str
) -> PageResearchReport:
    facts = []
    for span in plan.source_spans:
        if span.doc_id != doc_id:
            continue
        excerpt = " ".join(
            line.strip() for line in span.text.splitlines() if line.strip()
        )
        if len(excerpt) > 500:
            excerpt = excerpt[:500].rstrip() + "..."
        facts.append(
            ResearchFact(
                claim=excerpt or f"Source evidence is available for {span.ref}.",
                citation=span.ref,
                note="Deterministic fallback because the research subagent failed.",
            )
        )

    return PageResearchReport(
        doc_id=doc_id,
        scope=f"Fallback research report for {plan.slug}.",
        context_summary=f"Research subagent failed: {reason}",
        facts=facts,
        caveats=[
            "Research report is deterministic fallback; page writer must stay close to source evidence."
        ],
    )


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if not merged or start > merged[-1][1] + 1:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return merged


def render_context_windows(
    *,
    spans: list[SourceSpan],
    context_lines: int,
) -> str:
    by_path: dict[str, list[SourceSpan]] = {}
    for span in spans:
        by_path.setdefault(span.source_path, []).append(span)

    blocks: list[str] = []
    for source_path, source_spans in sorted(by_path.items()):
        lines = read_lines(Path(source_path))
        if context_lines < 0:
            blocks.append(
                f"<context_window path={source_path!r} lines=1-{len(lines)}>\n"
                f"{numbered_source_lines(lines, 1)}\n"
                "</context_window>"
            )
            continue

        ranges = _merge_ranges(
            [
                (
                    max(1, span.line_start - context_lines),
                    min(len(lines), span.line_end + context_lines),
                )
                for span in source_spans
            ]
        )
        for start, end in ranges:
            blocks.append(
                f"<context_window path={source_path!r} lines={start}-{end}>\n"
                f"{numbered_source_lines(lines[start - 1 : end], start)}\n"
                "</context_window>"
            )

    return "\n\n".join(blocks)


async def research_one_document_for_page(
    *,
    llm,
    plan: PagePlan,
    doc_id: str,
) -> PageResearchReport:
    spans = [span for span in plan.source_spans if span.doc_id == doc_id]
    if not spans:
        return fallback_research_report(plan, doc_id, "missing assigned spans")

    document_context = render_context_windows(
        spans=spans,
        context_lines=RESEARCH_CONTEXT_LINES,
    )

    try:
        raw = await structured_ainvoke(
            llm,
            PageResearchReport,
            build_page_research_prompt(
                plan=plan,
                doc_id=doc_id,
                document_context=document_context,
                assigned_source_blocks=render_source_spans(spans),
            ),
            max_output_tokens=2500,
            phase=f"wiki_gen.research.{plan.slug}.{doc_id}",
            enable_thinking=False,
        )
        report = PageResearchReport.model_validate(raw)
        if not report.doc_id:
            report = report.model_copy(update={"doc_id": doc_id})
        return report
    except Exception as exc:  # noqa: BLE001
        return fallback_research_report(plan, doc_id, str(exc))


async def research_page_plan(
    *,
    llm,
    plan: PagePlan,
    concurrency: int,
) -> PagePlan:
    doc_ids = sorted({span.doc_id for span in plan.source_spans})
    if not doc_ids:
        return plan

    semaphore = asyncio.Semaphore(max(1, concurrency))

    async def run(doc_id: str) -> PageResearchReport:
        async with semaphore:
            print(f"[Research] {plan.slug} doc={doc_id}")
            return await research_one_document_for_page(
                llm=llm,
                plan=plan,
                doc_id=doc_id,
            )

    reports = await asyncio.gather(*(run(doc_id) for doc_id in doc_ids))
    return plan.model_copy(update={"research_reports": list(reports)})


async def research_page_plans_bounded(
    *,
    llm,
    plans: list[PagePlan],
    page_concurrency: int,
    subagent_concurrency: int,
) -> list[PagePlan]:
    semaphore = asyncio.Semaphore(max(1, page_concurrency))

    async def run(plan: PagePlan) -> PagePlan:
        async with semaphore:
            return await research_page_plan(
                llm=llm,
                plan=plan,
                concurrency=subagent_concurrency,
            )

    return await asyncio.gather(*(run(plan) for plan in plans))
