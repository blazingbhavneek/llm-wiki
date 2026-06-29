from __future__ import annotations

import os
from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------
# Runtime config
# ---------------------------------------------------------------------

EMBED_ROOT = os.environ.get(
    "WIKI_GEN_EMBED_ROOT",
    "/run/media/blaze/Common/Code/llm-wiki/output_embed",
)
OUTPUT_ROOT = os.environ.get(
    "WIKI_GEN_OUTPUT_ROOT",
    "/run/media/blaze/Common/Code/llm-wiki/output_wiki",
)
INPUT_ROOT = os.environ.get(
    "WIKI_GEN_INPUT_ROOT",
    "/run/media/blaze/Common/Code/llm-wiki/input",
)

BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://194.14.47.19:23149/v1")
API_KEY = os.environ.get("OPENAI_API_KEY", "local")
GEN_MODEL = os.environ.get("WIKI_GEN_MODEL", "nvidia/Qwen3.6-35B-A3B-NVFP4")
VERIFY_MODEL = os.environ.get("WIKI_VERIFY_MODEL", GEN_MODEL)

TEMPERATURE = float(os.environ.get("WIKI_GEN_TEMPERATURE", "0.3"))
TIMEOUT = int(os.environ.get("WIKI_GEN_TIMEOUT", "300"))

ASSIGN_CONCURRENCY = int(os.environ.get("WIKI_ASSIGN_CONCURRENCY", "12"))
PAGE_CONCURRENCY = int(os.environ.get("WIKI_PAGE_CONCURRENCY", "6"))
JUDGE_CONCURRENCY = int(os.environ.get("WIKI_JUDGE_CONCURRENCY", "8"))
RESEARCH_CONCURRENCY = int(os.environ.get("WIKI_RESEARCH_CONCURRENCY", "8"))

MAX_CATALOG_ITEMS = int(os.environ.get("WIKI_MAX_CATALOG_ITEMS", "18"))
ASSIGN_REPAIR_ATTEMPTS = int(os.environ.get("WIKI_ASSIGN_REPAIR_ATTEMPTS", "5"))
FACT_REPAIR_ATTEMPTS = int(os.environ.get("WIKI_FACT_REPAIR_ATTEMPTS", "5"))

# Global wiki output should normally be incremental; cleaning would destroy
# pages that later documents are supposed to assimilate into.
CLEAN_OUTPUT = os.environ.get("WIKI_GEN_CLEAN", "0") == "1"

PageType = Literal["summary", "entity", "concept"]
AssignmentAction = Literal["new_page", "assimilate", "ignore"]


# ---------------------------------------------------------------------
# Source evidence
# ---------------------------------------------------------------------


class SourceSpan(BaseModel):
    doc_id: str
    source_path: str
    line_start: int
    line_end: int
    text: str = ""

    @property
    def ref(self) -> str:
        return f"{self.doc_id}:L{self.line_start}-L{self.line_end}"


class DocumentContext(BaseModel):
    doc_id: str
    source_path: str
    line_start: int = 1
    line_end: int
    text: str


class SourceChunk(BaseModel):
    doc_id: str
    chunk_id: str
    title: str
    filename: str
    line_start: int
    line_end: int
    text: str
    source_path: str

    def span(self, line_start: int | None = None, line_end: int | None = None) -> SourceSpan:
        start = self.line_start if line_start is None else line_start
        end = self.line_end if line_end is None else line_end
        return SourceSpan(
            doc_id=self.doc_id,
            source_path=self.source_path,
            line_start=start,
            line_end=end,
            text="",
        )


class EmbedDocument(BaseModel):
    doc_id: str
    embed_dir: str
    raw_dir: str = ""
    original_path: str
    coverage_path: str
    metadata_path: str | None = None
    source_line_count: int
    chunks: list[SourceChunk] = Field(default_factory=list)


# ---------------------------------------------------------------------
# Global page catalog
# ---------------------------------------------------------------------


class WikiCatalogEntry(BaseModel):
    slug: str
    title: str
    page_type: PageType
    summary: str = ""
    aliases: list[str] = Field(default_factory=list)
    path: str = ""
    source_refs: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------
# Pass 0 assignment schemas
# ---------------------------------------------------------------------


class AssignmentSpan(BaseModel):
    line_start: int = Field(description="1-based global original-document start line.")
    line_end: int = Field(description="1-based global original-document end line.")
    action: AssignmentAction
    page_type: PageType | None = None
    target_slug: str | None = Field(
        default=None,
        description="Existing or proposed global wiki slug, e.g. concept/memory-model.",
    )
    title: str | None = None
    aliases: list[str] = Field(default_factory=list)
    summary: str = ""
    reason: str = ""


class ChunkAssignmentResult(BaseModel):
    assignments: list[AssignmentSpan] = Field(default_factory=list)


class WikiAssignment(BaseModel):
    doc_id: str
    chunk_id: str
    line_start: int
    line_end: int
    action: AssignmentAction
    page_type: PageType | None = None
    target_slug: str | None = None
    title: str | None = None
    aliases: list[str] = Field(default_factory=list)
    summary: str = ""
    reason: str = ""
    generated_by_fallback: bool = False

    @property
    def source_ref(self) -> str:
        return f"{self.doc_id}:L{self.line_start}-L{self.line_end}"


# ---------------------------------------------------------------------
# Page generation schemas
# ---------------------------------------------------------------------


class ResearchFact(BaseModel):
    claim: str
    citation: str
    note: str = ""


class PageResearchReport(BaseModel):
    doc_id: str
    scope: str = ""
    context_summary: str = ""
    facts: list[ResearchFact] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    related_terms: list[str] = Field(default_factory=list)
    recommended_structure: list[str] = Field(default_factory=list)


class PagePlan(BaseModel):
    slug: str
    page_type: PageType
    title: str
    summary: str = ""
    aliases: list[str] = Field(default_factory=list)
    source_spans: list[SourceSpan] = Field(default_factory=list)
    document_contexts: list[DocumentContext] = Field(default_factory=list)
    research_reports: list[PageResearchReport] = Field(default_factory=list)
    existing_content: str = ""


class PageDraftResult(BaseModel):
    title: str
    summary: str
    content: str
    aliases: list[str] = Field(default_factory=list)


class GeneratedPage(BaseModel):
    slug: str
    page_type: PageType
    title: str
    summary: str
    content: str
    aliases: list[str] = Field(default_factory=list)
    path: str = ""
    source_spans: list[SourceSpan] = Field(default_factory=list)
    research_reports: list[PageResearchReport] = Field(default_factory=list)
    repaired: bool = False


# ---------------------------------------------------------------------
# Judge schemas
# ---------------------------------------------------------------------


class FactCheckResult(BaseModel):
    passed: bool = False
    unsupported_claims: list[str] = Field(default_factory=list)
    bad_citations: list[str] = Field(default_factory=list)
    repair_instruction: str = ""
    reason: str = ""


class MissingRange(BaseModel):
    line_start: int
    line_end: int
    reason: str = ""


class CoverageCheckResult(BaseModel):
    passed: bool = False
    missing_ranges: list[MissingRange] = Field(default_factory=list)
    non_content_ranges: list[MissingRange] = Field(default_factory=list)
    repair_instruction: str = ""
    reason: str = ""
