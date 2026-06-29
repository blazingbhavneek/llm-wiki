from __future__ import annotations

import re
from pathlib import Path

from wiki_new.utils import slugify, write_json

from wiki_gen.models import GeneratedPage, PageType, WikiCatalogEntry


PAGE_DIR_BY_TYPE: dict[PageType, str] = {
    "entity": "entities",
    "concept": "concepts",
    "summary": "summaries",
}

TYPE_BY_PAGE_DIR = {v: k for k, v in PAGE_DIR_BY_TYPE.items()}


def slug_to_path(output_root: Path, slug: str, page_type: PageType | None = None) -> Path:
    if "/" in slug:
        prefix, stem = slug.split("/", 1)
    else:
        prefix, stem = page_type or "concept", slug

    if prefix == "entity":
        folder = "entities"
    elif prefix == "summary":
        folder = "summaries"
    else:
        folder = "concepts"

    return output_root / folder / f"{slugify(stem)}.md"


def path_to_slug(output_root: Path, path: Path) -> tuple[str, PageType] | None:
    try:
        rel = path.relative_to(output_root)
    except ValueError:
        return None
    if len(rel.parts) != 2:
        return None

    folder, filename = rel.parts
    page_type = TYPE_BY_PAGE_DIR.get(folder)
    if page_type is None:
        return None

    stem = Path(filename).stem
    prefix = "entity" if page_type == "entity" else "summary" if page_type == "summary" else "concept"
    return f"{prefix}/{stem}", page_type


def _first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _first_summary(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("---"):
            continue
        if stripped.startswith("SUMMARY:"):
            return stripped.removeprefix("SUMMARY:").strip()
        return stripped[:240]
    return ""


def _citation_refs(markdown: str) -> list[str]:
    refs = set(re.findall(r"\[([A-Za-z0-9_.-]+:L\d+-L\d+)\]", markdown))
    return sorted(refs)


def load_catalog(output_root: Path) -> list[WikiCatalogEntry]:
    entries: list[WikiCatalogEntry] = []
    for folder in ["entities", "concepts", "summaries"]:
        base = output_root / folder
        if not base.exists():
            continue
        for path in sorted(base.glob("*.md")):
            mapped = path_to_slug(output_root, path)
            if mapped is None:
                continue
            slug, page_type = mapped
            text = path.read_text(encoding="utf-8")
            title = _first_heading(text) or Path(path).stem.replace("-", " ").title()
            entries.append(
                WikiCatalogEntry(
                    slug=slug,
                    title=title,
                    page_type=page_type,
                    summary=_first_summary(text),
                    aliases=[],
                    path=str(path),
                    source_refs=_citation_refs(text),
                )
            )
    return entries


def _tokens(text: str) -> set[str]:
    return {
        t
        for t in re.findall(r"[A-Za-z0-9_]{3,}", text.lower())
        if t not in {"the", "and", "for", "that", "with", "from", "this"}
    }


def shortlist_catalog(
    text: str,
    catalog: list[WikiCatalogEntry],
    *,
    limit: int,
) -> list[WikiCatalogEntry]:
    if not catalog:
        return []

    query = _tokens(text)
    scored: list[tuple[int, WikiCatalogEntry]] = []
    for entry in catalog:
        haystack = " ".join([entry.slug, entry.title, entry.summary, " ".join(entry.aliases)])
        score = len(query & _tokens(haystack))
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda item: (-item[0], item[1].slug))
    if scored:
        return [entry for _, entry in scored[:limit]]

    return catalog[:limit]


def render_catalog_for_prompt(entries: list[WikiCatalogEntry]) -> str:
    if not entries:
        return "(none)"

    lines = []
    for entry in entries:
        aliases = f" aliases={entry.aliases}" if entry.aliases else ""
        summary = f" summary={entry.summary}" if entry.summary else ""
        lines.append(
            f"- slug={entry.slug} type={entry.page_type} title={entry.title!r}"
            f"{aliases}{summary}"
        )
    return "\n".join(lines)


def write_catalog(output_root: Path, pages: list[GeneratedPage] | None = None) -> list[WikiCatalogEntry]:
    entries = load_catalog(output_root)
    if pages:
        by_slug = {entry.slug: entry for entry in entries}
        for page in pages:
            by_slug[page.slug] = WikiCatalogEntry(
                slug=page.slug,
                title=page.title,
                page_type=page.page_type,
                summary=page.summary,
                aliases=page.aliases,
                path=page.path,
                source_refs=[span.ref for span in page.source_spans],
            )
        entries = sorted(by_slug.values(), key=lambda item: item.slug)

    write_json(
        output_root / "_planning" / "global_catalog.json",
        {"pages": [entry.model_dump() for entry in entries]},
    )
    return entries

