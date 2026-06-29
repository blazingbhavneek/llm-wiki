from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from wiki_new.utils import numbered_source_lines

from wiki_gen.catalog import render_catalog_for_prompt
from wiki_gen.models import PagePlan, SourceChunk, WikiCatalogEntry


def build_assignment_prompt(
    *,
    chunk: SourceChunk,
    catalog: list[WikiCatalogEntry],
) -> list:
    chunk_lines = chunk.text.splitlines()
    numbered = numbered_source_lines(chunk_lines, chunk.line_start)

    return [
        SystemMessage(
            content=(
                "You are a precise wiki planning agent. You decide how a source "
                "line range should be represented in a GLOBAL wiki shared by many "
                "documents. You do not write the page body. You only assign every "
                "meaningful source line range to either a new global page, an "
                "existing global page, or an explicit ignore record for non-content."
            )
        ),
        HumanMessage(
            content=(
                f"Document: {chunk.doc_id}\n"
                f"Chunk id: {chunk.chunk_id}\n"
                f"Chunk title hint: {chunk.title}\n"
                f"Global original-document line range: {chunk.line_start}-{chunk.line_end}\n\n"
                "Relevant existing global wiki pages:\n"
                f"{render_catalog_for_prompt(catalog)}\n\n"
                "Rules:\n"
                "- Use ONLY global original-document line numbers shown below.\n"
                "- Cover the entire chunk range with assignments. Split into "
                "smaller contiguous ranges when different facts belong to different pages.\n"
                "- Prefer ASSIMILATE when an existing page is about the exact same "
                "entity/concept. Do not create duplicates.\n"
                "- Use NEW_PAGE for a significant entity/concept that does not exist yet.\n"
                "- Use IGNORE only for pure scaffolding, empty lines, boilerplate, "
                "page numbers, copyright/front matter, table-of-contents filler, "
                "or references that carry no useful wiki fact. Ignored ranges still "
                "must be explicit.\n"
                "- target_slug format must be one of: entity/<slug>, concept/<slug>, "
                "summary/<doc-slug>. Use lowercase hyphenated slugs.\n"
                "- page_type must be entity or concept for new/assimilated topical pages.\n"
                "- Do not cite or mention local chunk-file line numbers.\n\n"
                "Source lines:\n"
                f"{numbered}"
            )
        ),
    ]


def build_assignment_repair_prompt(
    *,
    chunk: SourceChunk,
    previous_json: str,
    missing_ranges: list[tuple[int, int]],
    catalog: list[WikiCatalogEntry],
) -> list:
    numbered = numbered_source_lines(chunk.text.splitlines(), chunk.line_start)
    missing = ", ".join(f"{start}-{end}" for start, end in missing_ranges)
    return [
        SystemMessage(
            content=(
                "You repair wiki line-range assignments. Return complete corrected "
                "assignments only, not commentary."
            )
        ),
        HumanMessage(
            content=(
                f"Document: {chunk.doc_id}\n"
                f"Chunk id: {chunk.chunk_id}\n"
                f"Required full range: {chunk.line_start}-{chunk.line_end}\n"
                f"Missing or uncovered ranges: {missing}\n\n"
                "Previous assignment JSON:\n"
                f"{previous_json}\n\n"
                "Relevant existing global wiki pages:\n"
                f"{render_catalog_for_prompt(catalog)}\n\n"
                "Repair rules:\n"
                "- Return assignments that cover the full required range.\n"
                "- Every line must be assigned to new_page, assimilate, or ignore.\n"
                "- Use only global original-document line numbers.\n\n"
                "Source lines:\n"
                f"{numbered}"
            )
        ),
    ]


def render_source_spans(spans) -> str:
    blocks = []
    for span in spans:
        blocks.append(
            f"<source doc={span.doc_id!r} lines={span.line_start}-{span.line_end} "
            f"ref={span.ref!r}>\n{span.text}\n</source>"
        )
    return "\n\n".join(blocks)


def render_document_contexts(contexts) -> str:
    blocks = []
    for ctx in contexts:
        blocks.append(
            f"<document_context doc={ctx.doc_id!r} lines={ctx.line_start}-{ctx.line_end} "
            f"path={ctx.source_path!r}>\n{ctx.text}\n</document_context>"
        )
    return "\n\n".join(blocks)


def build_page_research_prompt(
    *,
    plan: PagePlan,
    doc_id: str,
    document_context: str,
    assigned_source_blocks: str,
) -> list:
    return [
        SystemMessage(
            content=(
                "You are a wiki research subagent. You read ONE full original "
                "document for ONE target wiki page, then report compact findings "
                "to a lead page writer. You do not write the final page."
            )
        ),
        HumanMessage(
            content=(
                f"Target page slug: {plan.slug}\n"
                f"Target page type: {plan.page_type}\n"
                f"Target title: {plan.title}\n"
                f"Assigned document: {doc_id}\n\n"
                "Full original document context, with global line numbers:\n"
                f"{document_context}\n\n"
                "Assigned source evidence for this target page from this document:\n"
                f"{assigned_source_blocks}\n\n"
                "Research rules:\n"
                "- Read the full original document context before reporting.\n"
                "- Explain how the assigned evidence fits into the document's broader structure.\n"
                "- Return compact findings only; the lead page writer will write the page.\n"
                "- Every fact you report must be supported by an assigned source evidence range.\n"
                "- Use citations exactly like doc_id:Lstart-Lend. Do not cite chunk-local lines.\n"
                "- Use full document context for framing, terminology, caveats, and clash detection, "
                "but do not introduce facts that are only present outside assigned evidence.\n"
                "- Flag contradictions or scope clashes with existing target meaning if the document suggests them.\n"
            )
        ),
    ]


def render_research_reports(reports) -> str:
    if not reports:
        return "(none)"

    blocks = []
    for report in reports:
        fact_lines = [
            f"- {fact.claim} [{fact.citation}]"
            + (f" note={fact.note}" if fact.note else "")
            for fact in report.facts
        ]
        blocks.append(
            f"<research_report doc={report.doc_id!r}>\n"
            f"scope: {report.scope}\n"
            f"context_summary: {report.context_summary}\n"
            f"facts:\n" + ("\n".join(fact_lines) if fact_lines else "(none)") + "\n"
            f"caveats: {report.caveats}\n"
            f"contradictions: {report.contradictions}\n"
            f"related_terms: {report.related_terms}\n"
            f"recommended_structure: {report.recommended_structure}\n"
            "</research_report>"
        )
    return "\n\n".join(blocks)


def build_page_generation_prompt(
    *,
    plan: PagePlan,
    repair_instruction: str = "",
) -> list:
    source_blocks = render_source_spans(plan.source_spans)
    research_reports = render_research_reports(plan.research_reports)
    existing = plan.existing_content.strip() or "(new page)"
    repair = (
        f"\nRepair instruction from judge:\n{repair_instruction}\n"
        if repair_instruction
        else ""
    )
    return [
        SystemMessage(
            content=(
                "You are a wiki editor. Generate or update one global wiki page "
                "from research reports produced by subagents that each read a full "
                "original source document. Preserve useful existing content when it "
                "is still supported. Every new factual claim must carry an inline "
                "citation using the exact [doc_id:Lstart-Lend] reference from the "
                "assigned source evidence."
            )
        ),
        HumanMessage(
            content=(
                f"Page slug: {plan.slug}\n"
                f"Page type: {plan.page_type}\n"
                f"Page title: {plan.title}\n"
                f"Aliases: {plan.aliases}\n"
                f"Current summary hint: {plan.summary}\n"
                f"{repair}\n"
                "Existing page content:\n"
                f"{existing}\n\n"
                "Research subagent reports. Each subagent read one full original "
                "document and compressed the relevant context for this page:\n"
                f"{research_reports}\n\n"
                "Assigned source evidence. These are the ranges this page is "
                "responsible for representing and citing:\n"
                f"{source_blocks}\n\n"
                "Rules:\n"
                "- Output a concise, self-contained wiki page in Markdown.\n"
                "- Use the research reports to add the right framing, scope, "
                "definitions, prerequisites, and caveats from the original documents.\n"
                "- Do not treat an assigned span as an isolated snippet. Explain how "
                "it fits into the surrounding document when the reports make that clear.\n"
                "- Stay close to the source; do not invent facts or implications.\n"
                "- Use '# {title}' as the first Markdown heading.\n"
                "- Do not add filler or marketing prose.\n"
                "- Use citations exactly like [sycl:L9437-L9999].\n"
                "- A citation must point to the original document line range, not a chunk file.\n"
                "- New factual claims must be supported by the assigned source evidence. "
                "Research reports may guide framing, but do not introduce uncited "
                "facts that are not present in assigned source evidence.\n"
                "- If multiple source spans support one sentence, cite the most direct range.\n"
                "- summary must be one sentence for index listing.\n"
            )
        ),
    ]


def build_fact_check_prompt(*, page_slug: str, page_content: str, source_blocks: str) -> list:
    return [
        SystemMessage(
            content=(
                "You are a strict citation fact checker. Check that the page is "
                "fully supported by the cited original-document source lines."
            )
        ),
        HumanMessage(
            content=(
                f"Page slug: {page_slug}\n\n"
                "Page markdown:\n"
                f"{page_content}\n\n"
                "Available cited source spans:\n"
                f"{source_blocks}\n\n"
                "Checks:\n"
                "- Every factual claim must be supported by the cited source spans.\n"
                "- Inline citations must use [doc_id:Lstart-Lend] and must match an available span.\n"
                "- Flag hallucinations, over-generalizations, and citations that point to the wrong evidence.\n"
                "- If repair is needed, provide a concrete repair instruction.\n"
            )
        ),
    ]


def build_coverage_check_prompt(
    *,
    chunk: SourceChunk,
    relevant_pages: str,
) -> list:
    numbered = numbered_source_lines(chunk.text.splitlines(), chunk.line_start)
    return [
        SystemMessage(
            content=(
                "You are a source coverage judge. You decide whether a source "
                "chunk's meaningful information is represented in the current "
                "global wiki pages."
            )
        ),
        HumanMessage(
            content=(
                f"Document: {chunk.doc_id}\n"
                f"Chunk id: {chunk.chunk_id}\n"
                f"Required line range: {chunk.line_start}-{chunk.line_end}\n\n"
                "Source chunk lines:\n"
                f"{numbered}\n\n"
                "Current wiki pages that cite or were assigned from this chunk:\n"
                f"{relevant_pages or '(none)'}\n\n"
                "Checks:\n"
                "- Meaningful facts, definitions, procedures, code semantics, tables, and image captions should be represented.\n"
                "- Pure boilerplate/non-content may be listed as non_content_ranges.\n"
                "- Return missing_ranges for source line ranges whose information is not represented.\n"
                "- Use only global original-document line numbers.\n"
            )
        ),
    ]
