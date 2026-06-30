"""Deterministic hierarchical view generator for a generated ``output_wiki``.

The canonical wiki pages (``entities/``, ``concepts/``, ``summaries/``,
``indexes/``) stay flat and remain the source of truth. This module builds a
*navigation layer* over them, grounded entirely in source line coverage:

    source document  ->  coverage section (chapter)  ->  canonical pages

No LLM pass is required. Grouping comes from:

  * ``raw/<doc_id>/coverage.json``   — section headers + source line ranges
  * ``raw/<doc_id>/metadata.json``   — inferred / original document name
  * ``_planning/page_metadata.json`` — per-page title / summary / source_refs
  * ``_planning/page_sources.json``  — per-page source line refs (fallback)
  * markdown ``[doc_id:Lx-Ly]`` citations in the page body (final fallback)

A page is filed under every section whose line range covers one of its source
refs, so a page that cites several chapters appears in several places. Pages
are ordered by their first cited source line. Pages with no resolvable source
ref land in an ``orphans`` bucket so the view is always complete.

Output (written by :meth:`ViewBuilder.write`):

  * ``output_wiki/views/navigation.json`` — full tree for the API / frontend
  * ``output_wiki/views/sources/<doc>/README.md`` — per-document landing page
  * ``output_wiki/views/sources/<doc>/<section>.md`` — per-section index page

The view layer never duplicates canonical page bodies; it only links to them.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_PAGE_FOLDERS = {
    "entities": "entity",
    "concepts": "concept",
    "summaries": "summary",
    "indexes": "index",
}
_SOURCE_REF_RE = re.compile(r"\[([A-Za-z0-9_.-]+):L(\d+)-L(\d+)\]")


# region DATA MODEL
@dataclass
class PageRef:
    """A canonical wiki page placed at a source line position."""

    slug: str
    title: str
    summary: str
    path: str  # canonical page path, relative to output_wiki root
    kind: str
    line_start: int
    line_end: int
    refs: list[dict[str, Any]] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "title": self.title,
            "summary": self.summary,
            "path": self.path,
            "kind": self.kind,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "refs": self.refs,
        }


@dataclass
class Section:
    header: str
    title: str
    source_start: int
    source_end: int
    pages: list[PageRef] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "header": self.header,
            "title": self.title,
            "source_start": self.source_start,
            "source_end": self.source_end,
            "page_count": len(self.pages),
            "pages": [page.to_json() for page in self.pages],
        }


@dataclass
class SourceDoc:
    doc_id: str
    name: str
    title: str
    line_count: int
    sections: list[Section] = field(default_factory=list)
    unsectioned: list[PageRef] = field(default_factory=list)

    @property
    def page_count(self) -> int:
        seen = {p.slug for s in self.sections for p in s.pages}
        seen.update(p.slug for p in self.unsectioned)
        return len(seen)

    def to_json(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "name": self.name,
            "title": self.title,
            "line_count": self.line_count,
            "page_count": self.page_count,
            "section_count": len(self.sections),
            "sections": [s.to_json() for s in self.sections if s.pages],
            "unsectioned": [p.to_json() for p in self.unsectioned],
        }


# endregion DATA MODEL


class ViewBuilder:
    # region LIFECYCLE
    def __init__(self, wiki_root: str | Path) -> None:
        self.root = Path(wiki_root)
        if not self.root.is_dir():
            raise NotADirectoryError(f"wiki root not found: {self.root}")

    # endregion LIFECYCLE

    # region PUBLIC API
    def build(self) -> dict[str, Any]:
        """Build and return the navigation tree without writing files."""

        page_meta = self._load_page_metadata()
        page_sources = self._load_page_sources()
        pages = self._collect_pages(page_meta, page_sources)

        docs: dict[str, SourceDoc] = {}
        coverage_index: dict[str, list[Section]] = {}
        for doc_id in self._raw_doc_ids():
            doc, sections = self._build_source_doc(doc_id)
            docs[doc_id] = doc
            coverage_index[doc_id] = sections

        orphans: list[PageRef] = []
        for slug, page in pages.items():
            placed = False
            for ref in page.refs:
                doc_id = ref.get("doc_id")
                doc = docs.get(doc_id)
                if doc is None:
                    continue
                placed |= self._place_page(page, ref, doc, coverage_index[doc_id])
            if not placed:
                orphans.append(page)

        for doc in docs.values():
            self._sort_doc(doc)

        ordered_docs = sorted(
            docs.values(), key=lambda d: (-d.page_count, d.name.lower())
        )
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "wiki_root": str(self.root),
            "source_count": len(ordered_docs),
            "page_count": len(pages),
            "orphan_count": len(orphans),
            "sources": [d.to_json() for d in ordered_docs],
            "orphans": [
                p.to_json() for p in sorted(orphans, key=lambda p: p.title.lower())
            ],
        }

    def write(self) -> dict[str, Any]:
        """Build the tree, write ``views/`` markdown + ``navigation.json``."""

        tree = self.build()
        views = self.root / "views"
        sources_dir = views / "sources"
        sources_dir.mkdir(parents=True, exist_ok=True)

        (views / "navigation.json").write_text(
            json.dumps(tree, indent=2) + "\n", encoding="utf-8"
        )
        self._write_root_readme(views, tree)
        for source in tree["sources"]:
            self._write_source_pages(sources_dir, source)
        return tree

    # endregion PUBLIC API

    # region PAGE COLLECTION
    def _collect_pages(
        self,
        page_meta: dict[str, dict[str, Any]],
        page_sources: dict[str, list[dict[str, Any]]],
    ) -> dict[str, PageRef]:
        pages: dict[str, PageRef] = {}
        for folder, kind in _PAGE_FOLDERS.items():
            base = self.root / folder
            if not base.is_dir():
                continue
            for md_file in sorted(base.glob("*.md")):
                slug = f"{kind}/{md_file.stem}"
                meta = page_meta.get(slug, {})
                text = md_file.read_text(encoding="utf-8", errors="ignore")
                refs = self._merge_refs(
                    meta.get("source_refs") or page_sources.get(slug, []),
                    self._refs_from_markdown(text),
                )
                line_start = min((r["line_start"] for r in refs), default=10**9)
                line_end = max((r["line_end"] for r in refs), default=line_start)
                pages[slug] = PageRef(
                    slug=slug,
                    title=str(
                        meta.get("title")
                        or self._title_from_markdown(text)
                        or md_file.stem
                    ),
                    summary=str(meta.get("summary") or ""),
                    path=md_file.relative_to(self.root).as_posix(),
                    kind=kind,
                    line_start=line_start,
                    line_end=line_end,
                    refs=refs,
                )
        return pages

    def _place_page(
        self,
        page: PageRef,
        ref: dict[str, Any],
        doc: SourceDoc,
        sections: list[Section],
    ) -> bool:
        start = ref.get("line_start")
        end = ref.get("line_end")
        if not isinstance(start, int):
            return False
        target = self._section_for(
            start, end if isinstance(end, int) else start, sections
        )
        bucket = target.pages if target is not None else doc.unsectioned
        if all(p.slug != page.slug for p in bucket):
            bucket.append(page)
        return True

    def _section_for(
        self, start: int, end: int, sections: list[Section]
    ) -> Section | None:
        best: Section | None = None
        best_overlap = 0
        for section in sections:
            overlap = min(end, section.source_end) - max(start, section.source_start)
            if overlap >= 0 and overlap >= best_overlap:
                best_overlap = overlap
                best = section
        return best

    def _sort_doc(self, doc: SourceDoc) -> None:
        doc.sections.sort(key=lambda s: s.source_start)
        for section in doc.sections:
            section.pages.sort(key=lambda p: (p.line_start, p.title.lower()))
        doc.unsectioned.sort(key=lambda p: (p.line_start, p.title.lower()))

    # endregion PAGE COLLECTION

    # region SOURCE DOCS
    def _raw_doc_ids(self) -> list[str]:
        raw = self.root / "raw"
        if not raw.is_dir():
            return []
        return [d.name for d in sorted(raw.iterdir()) if d.is_dir()]

    def _build_source_doc(self, doc_id: str) -> tuple[SourceDoc, list[Section]]:
        raw_dir = self.root / "raw" / doc_id
        coverage = self._read_json(raw_dir / "coverage.json", {})
        metadata = self._read_json(raw_dir / "metadata.json", {})
        name = (
            metadata.get("inferred_file_name")
            or metadata.get("original_file_name")
            or doc_id
        )
        sections: list[Section] = []
        for item in coverage.get("files", []) if isinstance(coverage, dict) else []:
            try:
                start = int(item["source_start"])
                end = int(item["source_end"])
            except (KeyError, TypeError, ValueError):
                continue
            sections.append(
                Section(
                    header=str(item.get("header") or item.get("title") or "Section"),
                    title=str(item.get("title") or item.get("header") or "Section"),
                    source_start=start,
                    source_end=end,
                )
            )
        doc = SourceDoc(
            doc_id=doc_id,
            name=str(name),
            title=self._humanize(str(name)),
            line_count=(
                int(coverage.get("source_line_count") or 0)
                if isinstance(coverage, dict)
                else 0
            ),
            sections=sections,
        )
        return doc, sections

    # endregion SOURCE DOCS

    # region MARKDOWN OUTPUT
    def _write_root_readme(self, views: Path, tree: dict[str, Any]) -> None:
        lines = [
            "# Wiki Source Browser",
            "",
            "Hierarchical navigation over the generated wiki, grouped by source "
            "document and chapter. Pages link back to the canonical wiki files; "
            "this layer is regenerated and never edited by hand.",
            "",
            f"- Sources: **{tree['source_count']}**",
            f"- Pages: **{tree['page_count']}**",
            f"- Orphan pages (no source ref): **{tree['orphan_count']}**",
            "",
            "## Sources",
            "",
        ]
        for source in tree["sources"]:
            rel = f"sources/{self._slugify(source['name'])}/README.md"
            lines.append(
                f"- [{source['title']}]({rel}) — "
                f"{source['page_count']} pages, {source['section_count']} sections"
            )
        (views / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _write_source_pages(self, sources_dir: Path, source: dict[str, Any]) -> None:
        doc_dir = sources_dir / self._slugify(source["name"])
        doc_dir.mkdir(parents=True, exist_ok=True)

        readme = [
            f"# {source['title']}",
            "",
            f"Source document `{source['doc_id']}` "
            f"({source['line_count']} source lines, {source['page_count']} pages).",
            "",
            "## Sections",
            "",
        ]
        for section in source["sections"]:
            anchor = self._slugify(section["header"]) + ".md"
            readme.append(
                f"- [{section['title']}]({anchor}) "
                f"(L{section['source_start']}-L{section['source_end']}, "
                f"{section['page_count']} pages)"
            )
            self._write_section_page(doc_dir, source, section)
        if source["unsectioned"]:
            readme += ["", "## Unsectioned Pages", ""]
            readme += self._page_links(source["unsectioned"], depth=1)
        (doc_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    def _write_section_page(
        self, doc_dir: Path, source: dict[str, Any], section: dict[str, Any]
    ) -> None:
        lines = [
            f"# {section['title']}",
            "",
            f"Part of [{source['title']}](README.md). "
            f"Source lines L{section['source_start']}-L{section['source_end']}.",
            "",
        ]
        lines += self._page_links(section["pages"], depth=1)
        path = doc_dir / (self._slugify(section["header"]) + ".md")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _page_links(self, pages: list[dict[str, Any]], depth: int) -> list[str]:
        # canonical pages live at output_wiki/<folder>/..; views are nested
        # output_wiki/views/sources/<doc>/ -> ../../../ reaches the root.
        prefix = "../" * (depth + 2)
        out: list[str] = []
        for page in pages:
            line = f"- [{page['title']}]({prefix}{page['path']})"
            if page.get("summary"):
                line += f" — {page['summary']}"
            out.append(line)
        return out or ["_(no pages)_"]

    # endregion MARKDOWN OUTPUT

    # region LOADERS / HELPERS
    def _load_page_metadata(self) -> dict[str, dict[str, Any]]:
        payload = self._read_json(self.root / "_planning" / "page_metadata.json", {})
        pages = payload.get("pages", {}) if isinstance(payload, dict) else {}
        return (
            {k: v for k, v in pages.items() if isinstance(v, dict)}
            if isinstance(pages, dict)
            else {}
        )

    def _load_page_sources(self) -> dict[str, list[dict[str, Any]]]:
        payload = self._read_json(self.root / "_planning" / "page_sources.json", {})
        pages = payload.get("pages", {}) if isinstance(payload, dict) else {}
        if not isinstance(pages, dict):
            return {}
        return {
            slug: [r for r in refs if isinstance(r, dict)]
            for slug, refs in pages.items()
            if isinstance(refs, list)
        }

    def _refs_from_markdown(self, text: str) -> list[dict[str, Any]]:
        refs: list[dict[str, Any]] = []
        for doc_id, start, end in _SOURCE_REF_RE.findall(text):
            refs.append(
                {
                    "doc_id": doc_id,
                    "line_start": int(start),
                    "line_end": int(end),
                    "ref": f"{doc_id}:L{start}-L{end}",
                }
            )
        return refs

    def _merge_refs(
        self, left: list[dict[str, Any]], right: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        merged: list[dict[str, Any]] = []
        seen: set[tuple[str, int, int]] = set()
        for ref in [*left, *right]:
            try:
                key = (str(ref["doc_id"]), int(ref["line_start"]), int(ref["line_end"]))
            except (KeyError, TypeError, ValueError):
                continue
            if key in seen:
                continue
            seen.add(key)
            merged.append(
                {
                    "doc_id": key[0],
                    "line_start": key[1],
                    "line_end": key[2],
                    "ref": ref.get("ref") or f"{key[0]}:L{key[1]}-L{key[2]}",
                }
            )
        return merged

    def _title_from_markdown(self, text: str) -> str | None:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or None
            if stripped and not stripped.startswith("---"):
                break
        return None

    def _humanize(self, name: str) -> str:
        stem = re.sub(r"\.md$", "", name)
        return stem.replace("-", " ").replace("_", " ").strip().title() or name

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
        return slug or "section"

    def _read_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return default

    # endregion LOADERS / HELPERS


def build_views(wiki_root: str | Path, write: bool = True) -> dict[str, Any]:
    """Convenience: build (and optionally write) the view tree for ``wiki_root``."""

    builder = ViewBuilder(wiki_root)
    return builder.write() if write else builder.build()
