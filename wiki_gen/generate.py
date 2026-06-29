from __future__ import annotations

import asyncio
import json
from pathlib import Path

from wiki_new.llm import structured_ainvoke
from wiki_new.planning import join_original_source_lines
from wiki_new.utils import numbered_source_lines, read_lines, write_json

from wiki_gen.catalog import slug_to_path
from wiki_gen.io import span_ref_dict
from wiki_gen.models import (
    DocumentContext,
    GeneratedPage,
    PageDraftResult,
    PagePlan,
    SourceSpan,
    WikiAssignment,
)
from wiki_gen.prompts import build_page_generation_prompt


def _span_text_cache(span: SourceSpan, cache: dict[str, list[str]]) -> SourceSpan:
    if span.source_path not in cache:
        cache[span.source_path] = read_lines(Path(span.source_path))
    lines = cache[span.source_path]
    text = join_original_source_lines(lines[span.line_start - 1 : span.line_end])
    return span.model_copy(update={"text": text})


def _document_context(
    *,
    doc_id: str,
    source_path: str,
    cache: dict[str, list[str]],
) -> DocumentContext:
    if source_path not in cache:
        cache[source_path] = read_lines(Path(source_path))
    lines = cache[source_path]
    return DocumentContext(
        doc_id=doc_id,
        source_path=source_path,
        line_start=1,
        line_end=len(lines),
        text=numbered_source_lines(lines, 1),
    )


def ensure_document_contexts(plan: PagePlan) -> PagePlan:
    cache: dict[str, list[str]] = {}
    contexts = list(plan.document_contexts)
    seen = {ctx.source_path for ctx in contexts}

    for span in plan.source_spans:
        if span.source_path in seen:
            continue
        contexts.append(
            _document_context(
                doc_id=span.doc_id,
                source_path=span.source_path,
                cache=cache,
            )
        )
        seen.add(span.source_path)

    if len(contexts) == len(plan.document_contexts):
        return plan
    return plan.model_copy(update={"document_contexts": contexts})


def build_page_plans(assignments: list[WikiAssignment], chunks_by_id: dict[str, object], output_root: Path) -> list[PagePlan]:
    del chunks_by_id
    grouped: dict[str, list[WikiAssignment]] = {}
    for assignment in assignments:
        if assignment.action == "ignore" or not assignment.target_slug:
            continue
        grouped.setdefault(assignment.target_slug, []).append(assignment)

    cache: dict[str, list[str]] = {}
    plans: list[PagePlan] = []
    for slug, items in sorted(grouped.items()):
        first = items[0]
        page_type = first.page_type or ("entity" if slug.startswith("entity/") else "summary" if slug.startswith("summary/") else "concept")
        title = first.title or slug.split("/", 1)[-1].replace("-", " ").title()
        summary = first.summary or ""
        aliases: list[str] = []
        spans: list[SourceSpan] = []
        contexts: list[DocumentContext] = []
        seen_spans: set[tuple[str, int, int]] = set()
        seen_contexts: set[str] = set()

        for item in items:
            if item.title and title == slug:
                title = item.title
            if item.summary and not summary:
                summary = item.summary
            for alias in item.aliases:
                if alias and alias not in aliases:
                    aliases.append(alias)

            source_path = ""
            # Source paths are copied under output_wiki/raw/<doc_id>/original.md.
            source_path = str(output_root / "raw" / item.doc_id / "original.md")
            if source_path not in seen_contexts:
                contexts.append(
                    _document_context(
                        doc_id=item.doc_id,
                        source_path=source_path,
                        cache=cache,
                    )
                )
                seen_contexts.add(source_path)

            key = (source_path, item.line_start, item.line_end)
            if key in seen_spans:
                continue
            seen_spans.add(key)
            spans.append(
                _span_text_cache(
                    SourceSpan(
                        doc_id=item.doc_id,
                        source_path=source_path,
                        line_start=item.line_start,
                        line_end=item.line_end,
                    ),
                    cache,
                )
            )

        page_path = slug_to_path(output_root, slug, page_type)
        existing = page_path.read_text(encoding="utf-8") if page_path.exists() else ""
        plans.append(
            PagePlan(
                slug=slug,
                page_type=page_type,
                title=title,
                summary=summary,
                aliases=aliases,
                source_spans=spans,
                document_contexts=contexts,
                existing_content=existing,
            )
        )

    return plans


def deterministic_page(plan: PagePlan, reason: str) -> PageDraftResult:
    title, summary, content = source_excerpt_content(plan, reason)
    return PageDraftResult(
        title=title,
        summary=summary,
        content=content,
        aliases=plan.aliases,
    )


def source_excerpt_content(plan: PagePlan, reason: str) -> tuple[str, str, str]:
    title = plan.title or plan.slug.split("/", 1)[-1].replace("-", " ").title()
    summary = (
        plan.summary
        or f"Verbatim source-backed fallback page for {title}."
    )
    lines = [
        f"# {title}",
        "",
        summary,
        "",
        "> Deterministic fallback: the normal synthesis path could not be verified. "
        "This page preserves the full source evidence verbatim with original line citations.",
        f"> Reason: {reason}",
        "",
    ]
    for span in plan.source_spans:
        lines.extend(
            [
                f"## Source {span.ref}",
                "",
                f"Citation: [{span.ref}]",
                "",
                "````text",
                span.text.rstrip(),
                "````",
                "",
            ]
        )
    return title, summary, "\n".join(lines).rstrip() + "\n"


def ensure_page_heading(content: str, title: str) -> str:
    stripped = content.strip()
    if not stripped:
        return f"# {title}\n"
    if stripped.startswith("# "):
        return stripped + "\n"
    return f"# {title}\n\n{stripped}\n"


async def generate_page(
    *,
    llm,
    plan: PagePlan,
    output_root: Path,
    repair_instruction: str = "",
) -> GeneratedPage:
    plan = ensure_document_contexts(plan)
    try:
        raw = await structured_ainvoke(
            llm,
            PageDraftResult,
            build_page_generation_prompt(plan=plan, repair_instruction=repair_instruction),
            max_output_tokens=5000,
        )
        draft = PageDraftResult.model_validate(raw)
    except Exception as exc:  # noqa: BLE001
        draft = deterministic_page(plan, f"page agent failed: {exc}")

    title = draft.title or plan.title
    content = ensure_page_heading(draft.content, title)
    page_path = slug_to_path(output_root, plan.slug, plan.page_type)
    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text(content, encoding="utf-8")

    return GeneratedPage(
        slug=plan.slug,
        page_type=plan.page_type,
        title=title,
        summary=draft.summary or plan.summary,
        content=content,
        aliases=draft.aliases or plan.aliases,
        path=str(page_path),
        source_spans=plan.source_spans,
        research_reports=plan.research_reports,
        repaired=bool(repair_instruction),
    )


def write_source_excerpt_page(
    *,
    plan: PagePlan,
    output_root: Path,
    reason: str,
) -> GeneratedPage:
    plan = ensure_document_contexts(plan)
    title, summary, content = source_excerpt_content(plan, reason)
    page_path = slug_to_path(output_root, plan.slug, plan.page_type)
    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text(content, encoding="utf-8")
    return GeneratedPage(
        slug=plan.slug,
        page_type=plan.page_type,
        title=title,
        summary=summary,
        content=content,
        aliases=plan.aliases,
        path=str(page_path),
        source_spans=plan.source_spans,
        research_reports=plan.research_reports,
        repaired=True,
    )


async def generate_pages_bounded(
    *,
    llm,
    plans: list[PagePlan],
    output_root: Path,
    concurrency: int,
) -> list[GeneratedPage]:
    semaphore = asyncio.Semaphore(concurrency)

    async def run(plan: PagePlan) -> GeneratedPage:
        async with semaphore:
            print(f"[Page] {plan.slug} spans={len(plan.source_spans)}")
            return await generate_page(llm=llm, plan=plan, output_root=output_root)

    return await asyncio.gather(*(run(plan) for plan in plans))


def load_page_sources(output_root: Path) -> dict[str, list[dict]]:
    path = output_root / "_planning" / "page_sources.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    pages = data.get("pages", {})
    return pages if isinstance(pages, dict) else {}


def write_page_sources(output_root: Path, pages: list[GeneratedPage]) -> None:
    existing = load_page_sources(output_root)
    for page in pages:
        refs = existing.setdefault(page.slug, [])
        seen = {(r.get("doc_id"), r.get("line_start"), r.get("line_end")) for r in refs}
        for span in page.source_spans:
            key = (span.doc_id, span.line_start, span.line_end)
            if key in seen:
                continue
            refs.append(span_ref_dict(span))
            seen.add(key)

    write_json(output_root / "_planning" / "page_sources.json", {"pages": existing})


def write_page_metadata(output_root: Path, pages: list[GeneratedPage]) -> None:
    path = output_root / "_planning" / "page_metadata.json"
    existing: dict[str, dict] = {}
    if path.exists():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            existing = raw.get("pages", {}) if isinstance(raw.get("pages", {}), dict) else {}
        except json.JSONDecodeError:
            existing = {}

    for page in pages:
        existing[page.slug] = {
            "slug": page.slug,
            "page_type": page.page_type,
            "title": page.title,
            "summary": page.summary,
            "aliases": page.aliases,
            "path": page.path,
            "source_refs": [span_ref_dict(span) for span in page.source_spans],
            "research_reports": [report.model_dump() for report in page.research_reports],
        }

    write_json(path, {"pages": existing})


def hydrate_pages_with_cumulative_sources(
    *,
    output_root: Path,
    pages: list[GeneratedPage],
) -> list[GeneratedPage]:
    page_sources = load_page_sources(output_root)
    cache: dict[str, list[str]] = {}
    hydrated: list[GeneratedPage] = []

    for page in pages:
        refs = page_sources.get(page.slug, [])
        spans: list[SourceSpan] = []
        seen: set[tuple[str, int, int]] = set()
        for ref in refs:
            try:
                span = SourceSpan(
                    doc_id=str(ref["doc_id"]),
                    source_path=str(ref["source_path"]),
                    line_start=int(ref["line_start"]),
                    line_end=int(ref["line_end"]),
                )
            except (KeyError, TypeError, ValueError):
                continue
            key = (span.source_path, span.line_start, span.line_end)
            if key in seen:
                continue
            seen.add(key)
            spans.append(_span_text_cache(span, cache))

        if spans:
            hydrated.append(page.model_copy(update={"source_spans": spans}))
        else:
            hydrated.append(page)

    return hydrated
