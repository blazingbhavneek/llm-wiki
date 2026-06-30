from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from wiki_gen.models import INPUT_ROOT, EmbedDocument, SourceChunk, SourceSpan
from wiki_new.planning import join_original_source_lines
from wiki_new.utils import read_lines, write_json


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_doc_id(path: Path) -> str:
    return path.name


def planning_dir(embed_doc_dir: Path) -> Path:
    return embed_doc_dir / "_planning"


def discover_embed_documents(embed_root: Path) -> list[Path]:
    if not embed_root.exists():
        raise RuntimeError(f"Embedding output root does not exist: {embed_root}")

    docs: list[Path] = []
    for child in sorted(embed_root.iterdir()):
        if not child.is_dir():
            continue
        if (child / "_planning" / "coverage.json").exists():
            docs.append(child)
    if not docs:
        raise RuntimeError(
            f"No embedded documents with _planning/coverage.json in {embed_root}"
        )
    return docs


def resolve_original_source(embed_doc_dir: Path, metadata: dict[str, Any]) -> Path:
    pdir = planning_dir(embed_doc_dir)
    configured = metadata.get("original_source")
    if configured:
        candidate = pdir / str(configured)
        if candidate.exists():
            return candidate

    original = pdir / "original.md"
    if original.exists():
        return original

    original_name = str(
        metadata.get("original_file_name") or f"{embed_doc_dir.name}.md"
    )
    input_candidate = Path(INPUT_ROOT) / original_name
    if input_candidate.exists():
        return input_candidate

    stem_candidate = Path(INPUT_ROOT) / f"{embed_doc_dir.name}.md"
    if stem_candidate.exists():
        return stem_candidate

    raise RuntimeError(
        f"Could not resolve original source for {embed_doc_dir}. "
        "Run wiki_embed again so _planning/original.md exists."
    )


def copy_if_exists(src: Path, dst: Path) -> None:
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copy_raw_artifacts(
    embed_doc_dir: Path, output_root: Path
) -> tuple[Path, Path, Path | None]:
    pdir = planning_dir(embed_doc_dir)
    coverage_path = pdir / "coverage.json"
    metadata_path = pdir / "metadata.json"
    metadata = load_json(metadata_path) if metadata_path.exists() else {}
    original_source = resolve_original_source(embed_doc_dir, metadata)

    raw_dir = output_root / "raw" / safe_doc_id(embed_doc_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_original = raw_dir / "original.md"
    shutil.copy2(original_source, raw_original)

    raw_coverage = raw_dir / "coverage.json"
    shutil.copy2(coverage_path, raw_coverage)

    raw_metadata: Path | None = None
    if metadata_path.exists():
        raw_metadata = raw_dir / "metadata.json"
        shutil.copy2(metadata_path, raw_metadata)

    copy_if_exists(pdir / "concept-plan.md", raw_dir / "concept-plan.md")
    return raw_original, raw_coverage, raw_metadata


def _chunk_text(source_lines: list[str], start: int, end: int) -> str:
    return join_original_source_lines(source_lines[start - 1 : end])


def load_embed_document(embed_doc_dir: Path, output_root: Path) -> EmbedDocument:
    raw_original, raw_coverage, raw_metadata = copy_raw_artifacts(
        embed_doc_dir, output_root
    )
    coverage = load_json(raw_coverage)
    source_lines = read_lines(raw_original)

    chunks: list[SourceChunk] = []
    for idx, item in enumerate(coverage.get("files", []), start=1):
        start = int(item["source_start"])
        end = int(item["source_end"])
        title = str(item.get("header") or item.get("title") or f"Chunk {idx}")
        chunk_id = f"{safe_doc_id(embed_doc_dir)}:{idx:04d}"
        chunks.append(
            SourceChunk(
                doc_id=safe_doc_id(embed_doc_dir),
                chunk_id=chunk_id,
                title=title,
                filename=str(item.get("filename") or item.get("name") or ""),
                line_start=start,
                line_end=end,
                text=_chunk_text(source_lines, start, end),
                source_path=str(raw_original),
            )
        )

    return EmbedDocument(
        doc_id=safe_doc_id(embed_doc_dir),
        embed_dir=str(embed_doc_dir),
        raw_dir=str(raw_original.parent),
        original_path=str(raw_original),
        coverage_path=str(raw_coverage),
        metadata_path=str(raw_metadata) if raw_metadata else None,
        source_line_count=int(coverage.get("source_line_count") or len(source_lines)),
        chunks=chunks,
    )


def load_embed_corpus(embed_root: Path, output_root: Path) -> list[EmbedDocument]:
    return [
        load_embed_document(embed_doc_dir, output_root)
        for embed_doc_dir in discover_embed_documents(embed_root)
    ]


def source_span_with_text(span: SourceSpan) -> SourceSpan:
    lines = read_lines(Path(span.source_path))
    text = join_original_source_lines(lines[span.line_start - 1 : span.line_end])
    return span.model_copy(update={"text": text})


def span_ref_dict(span: SourceSpan) -> dict[str, Any]:
    return {
        "doc_id": span.doc_id,
        "source_path": span.source_path,
        "line_start": span.line_start,
        "line_end": span.line_end,
        "ref": span.ref,
    }


def ensure_output_dirs(output_root: Path) -> None:
    for rel in [
        "raw",
        "entities",
        "concepts",
        "summaries",
        "indexes",
        "_planning",
    ]:
        (output_root / rel).mkdir(parents=True, exist_ok=True)


def write_planning_json(output_root: Path, name: str, payload: dict[str, Any]) -> None:
    path = output_root / "_planning" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, payload)
