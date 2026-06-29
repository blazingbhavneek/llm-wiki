from __future__ import annotations

import asyncio

from wiki_new.llm import structured_ainvoke

from wiki_gen.generate import ensure_document_contexts
from wiki_gen.models import PagePlan, PageResearchReport, ResearchFact
from wiki_gen.prompts import (
    build_page_research_prompt,
    render_source_spans,
)


def fallback_research_report(plan: PagePlan, doc_id: str, reason: str) -> PageResearchReport:
    facts = []
    for span in plan.source_spans:
        if span.doc_id != doc_id:
            continue
        excerpt = " ".join(line.strip() for line in span.text.splitlines() if line.strip())
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
        caveats=["Research report is deterministic fallback; page writer must stay close to source evidence."],
    )


async def research_one_document_for_page(
    *,
    llm,
    plan: PagePlan,
    doc_id: str,
) -> PageResearchReport:
    context = next((ctx for ctx in plan.document_contexts if ctx.doc_id == doc_id), None)
    spans = [span for span in plan.source_spans if span.doc_id == doc_id]
    if context is None or not spans:
        return fallback_research_report(plan, doc_id, "missing document context or assigned spans")

    try:
        raw = await structured_ainvoke(
            llm,
            PageResearchReport,
            build_page_research_prompt(
                plan=plan,
                doc_id=doc_id,
                document_context=context.text,
                assigned_source_blocks=render_source_spans(spans),
            ),
            max_output_tokens=2500,
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
    plan = ensure_document_contexts(plan)
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

