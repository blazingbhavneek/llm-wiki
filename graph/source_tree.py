"""Adapter over md.py compiled output -- the only dependency on its format.

Exposes a stable `CompiledDocument` contract so later md.py changes do not leak
into the graph implementation (handoff.md "Planned graph/ submodule").

Reads, per compiled source tree under output/<source>/:
  - manifest.json          (source path, leaf file records)
  - _planning/coverage.json (hard lossless-coverage validation artifact)
  - leaf-page frontmatter   (title, summary, source_lines)
  - manifest planning chunk_summaries[].topics (local/document topics)
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Optional

from .models import CompiledDocument, CompiledSourcePage

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


class CoverageError(RuntimeError):
    """Raised when a compiled tree fails the lossless-coverage invariant."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Minimal YAML-ish frontmatter parse for md.py leaf pages.

    md.py emits only flat scalar keys plus `source_lines: [[a, b], ...]`, so a
    tiny parser avoids a PyYAML dependency for the common case.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    body = text[m.end():]
    meta: dict[str, Any] = {}
    for line in m.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            try:
                meta[key] = json.loads(raw)
                continue
            except json.JSONDecodeError:
                pass
        meta[key] = raw.strip().strip('"')
    return meta, body


def validate_coverage(output_root: Path) -> dict[str, Any]:
    """Enforce the non-negotiable lossless-coverage invariant before ingest."""
    cov_path = output_root / "_planning" / "coverage.json"
    if not cov_path.exists():
        raise CoverageError(f"missing coverage.json under {output_root}")
    cov = _read_json(cov_path)
    if not cov.get("exact_coverage", False):
        raise CoverageError(f"coverage.json reports exact_coverage=false for {output_root}")

    assignments = sorted(
        cov.get("assignments", []), key=lambda a: a["source_start"]
    )
    expected = 1
    for a in assignments:
        start = int(a["source_start"])
        end = int(a["source_end"])
        if start != expected or end < start:
            raise CoverageError(
                f"coverage gap/overlap at line {expected} in {output_root}"
            )
        expected = end + 1
    line_count = int(cov.get("source_line_count", 0))
    if expected - 1 != line_count:
        raise CoverageError(
            f"coverage ends at {expected - 1}, expected {line_count} in {output_root}"
        )
    return cov


def _topics_for_range(
    chunk_summaries: list[dict[str, Any]], ranges: list[list[int]]
) -> list[str]:
    """Topics of chunks overlapping a page's source ranges."""
    topics: list[str] = []
    for cs in chunk_summaries:
        cs_a, cs_b = cs.get("source_start", 0), cs.get("source_end", 0)
        for a, b in ranges:
            if cs_a <= b and a <= cs_b:  # overlap
                topics.extend(cs.get("topics", []))
                break
    # de-dup, keep order
    seen: set[str] = set()
    out: list[str] = []
    for t in topics:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def read_compiled_document(output_root: Path | str) -> CompiledDocument:
    """Build the stable CompiledDocument contract for one compiled tree."""
    output_root = Path(output_root)
    manifest = _read_json(output_root / "manifest.json")
    cov = validate_coverage(output_root)
    manifest["_coverage_validated"] = True

    source_path = Path(manifest["source"])
    document_id = output_root.name
    title = document_id.replace("-", " ").title()

    # md.py records the original source in manifest["source"]; it may live on a
    # different machine. Hash it when present, else fall back to coverage info.
    if source_path.exists():
        sha = sha256_file(source_path)
    else:
        sha = hashlib.sha256(
            json.dumps(cov.get("assignments", []), sort_keys=True).encode()
        ).hexdigest()

    chunk_summaries = manifest.get("planning", {}).get("chunk_summaries", [])

    pages: list[CompiledSourcePage] = []
    for rec in manifest.get("files", []):
        rel = rec["filename"]
        page_path = output_root / rel
        if not page_path.exists():
            raise CoverageError(f"manifest leaf page is missing: {page_path}")
        ranges = [list(r) for r in rec.get("source_ranges", [])]
        summary = rec.get("summary", "")
        page_title = rec.get("title", rel)
        section_path: list[str] = []
        if page_path.exists():
            meta, _ = _parse_frontmatter(page_path.read_text(encoding="utf-8"))
            if meta.get("source_lines"):
                ranges = [list(r) for r in meta["source_lines"]]
            summary = meta.get("summary", summary)
            page_title = meta.get("title", page_title)
        # section path = folder names between output_root and the leaf file
        section_path = list(Path(rel).parts[:-1])
        pages.append(
            CompiledSourcePage(
                markdown_path=page_path,
                source_ranges=ranges,
                section_path=section_path,
                title=page_title,
                summary=summary,
                local_topics=_topics_for_range(chunk_summaries, ranges),
                rel_path=rel,
            )
        )

    assigned = {
        (str(a["file"]), int(a["source_start"]), int(a["source_end"]))
        for a in cov.get("assignments", [])
    }
    page_ranges = {
        (page.rel_path, int(start), int(end))
        for page in pages
        for start, end in page.source_ranges
    }
    if assigned != page_ranges:
        raise CoverageError(
            "coverage assignments do not exactly match manifest/frontmatter leaf ranges "
            f"under {output_root}"
        )

    # document topics = most frequent chunk topics across the whole document
    counter: Counter[str] = Counter()
    for cs in chunk_summaries:
        counter.update(cs.get("topics", []))
    document_topics = [t for t, _ in counter.most_common(12)]

    return CompiledDocument(
        source_path=source_path,
        output_root=output_root,
        document_id=document_id,
        title=title,
        source_sha256=sha,
        source_line_count=cov.get("source_line_count", 0),
        manifest=manifest,
        document_topics=document_topics,
        source_pages=pages,
    )


def discover_compiled_documents(parent: Path | str) -> list[Path]:
    """Find every output/<source>/ tree under a parent directory."""
    parent = Path(parent)
    roots: list[Path] = []
    for child in sorted(parent.iterdir()):
        if child.is_dir() and (child / "manifest.json").exists():
            roots.append(child)
    return roots
