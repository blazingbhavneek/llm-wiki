"""
Orchestration + batch runner for the embedding-hybrid chunker.

Segmentation is done by wiki_embed.chunking.segment_source; everything
downstream (exact-slice rendering, coverage validation, header/global-name
enrichment, JSON writers) is reused verbatim from wiki_new.planning, so the
final docs are identical in shape to wiki_new output.

Entrypoint: ../md2.py calls main.
"""

from __future__ import annotations

import argparse
import asyncio
import shutil
from pathlib import Path
from types import SimpleNamespace

from wiki_new.planning import (
    assert_concept_coverage,
    enrich_concept_plan,
    render_concept_files,
    write_concept_plan_document,
    write_coverage_json,
    write_metadata_json,
)
from wiki_new.utils import init_manifest, read_lines, utc_now_iso

from wiki_new.llm import make_llm

from wiki_embed.chunking import segment_source
from wiki_embed.models import (
    API_KEY,
    BASE_URL,
    CLEAN_OUTPUT,
    FILE_CONCURRENCY,
    GEN_MODEL,
    MAX_LINES,
    OUTPUT_ROOT,
    PHASE,
    SEM_PERCENTILE,
    SOURCE_PATH,
    TARGET_LINES,
    TEMPERATURE,
    TIMEOUT,
    USE_LLM_CONFIRM,
    VERIFY_MODEL,
    build_embedder,
)


async def phase_generate(args: argparse.Namespace, embedder) -> None:
    source_path = Path(args.source)
    out_dir = Path(args.out)
    docs_dir = out_dir / "docs"
    tag = source_path.stem

    if args.clean and out_dir.exists():
        print(f"[{tag}] cleaning existing output dir")
        shutil.rmtree(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{tag}] reading source")
    source_lines = read_lines(source_path)
    source_line_count = len(source_lines)
    print(f"[{tag}] {source_line_count} source lines")

    manifest = init_manifest(source_path)

    planning_dir = out_dir / "_planning"
    planning_dir.mkdir(parents=True, exist_ok=True)
    plan_md_path = planning_dir / "concept-plan.md"
    coverage_json_path = planning_dir / "coverage.json"
    metadata_json_path = planning_dir / "metadata.json"
    original_source_path = planning_dir / "original.md"
    shutil.copy2(source_path, original_source_path)

    llm = make_llm(
        model=args.gen_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=args.temperature,
        timeout=TIMEOUT,
    )

    if source_line_count == 0:
        concept_files = []
        coverage = []
        inferred_headers = []
        inferred_global_name = source_path.with_suffix(".md").name
    else:
        print(f"[{tag}] segmenting (embed + boundary confirm)...")
        concept_files = await segment_source(
            llm=llm,
            embedder=embedder,
            source_lines=source_lines,
            tag=tag,
        )

        print(f"[{tag}] validating coverage of {len(concept_files)} section(s)")
        assert_concept_coverage(
            files=concept_files,
            source_line_count=source_line_count,
        )

        print(f"[{tag}] rendering {len(concept_files)} doc file(s)")
        coverage = render_concept_files(
            docs_dir=docs_dir,
            source_lines=source_lines,
            files=concept_files,
            manifest=manifest,
            output_root=out_dir,
        )

        print(f"[{tag}] enriching headers + global name...")
        enrichment_result = await enrich_concept_plan(
            llm=llm,
            original_filename=source_path.name,
            files=concept_files,
        )
        inferred_headers = [f.header for f in enrichment_result.files]
        inferred_global_name = enrichment_result.inferred_file_name

    if source_line_count > 0:
        paired = sorted(
            zip(concept_files, inferred_headers),
            key=lambda x: (x[0].source_start, x[0].source_end),
        )
        ordered_concept_files = [p[0] for p in paired]
        inferred_headers = [p[1] for p in paired]
    else:
        ordered_concept_files = []

    manifest.setdefault("planning", {})
    manifest["planning"]["strategy"] = "embedding_hybrid_semantic_split"
    manifest["planning"]["target_lines"] = TARGET_LINES
    manifest["planning"]["max_lines"] = MAX_LINES
    manifest["planning"]["semantic_percentile"] = SEM_PERCENTILE
    manifest["planning"]["llm_confirm"] = USE_LLM_CONFIRM
    manifest["planning"]["docs_dir"] = "docs"
    manifest["planning"]["original_source"] = "original.md"
    manifest["planning"]["file_count"] = len(ordered_concept_files)
    manifest["planning"]["coverage_verified_at"] = utc_now_iso()
    manifest["planning"]["render_integrity"] = "exact_source_slice_match"
    manifest["planning"]["inferred_global_name"] = inferred_global_name
    manifest["planning"]["files"] = [
        {"order": index, "header": header, **item.model_dump()}
        for index, (item, header) in enumerate(
            zip(ordered_concept_files, inferred_headers), start=1
        )
    ]

    manifest["coverage"] = coverage
    manifest["updated_at"] = utc_now_iso()

    write_concept_plan_document(
        path=plan_md_path,
        source_path=source_path,
        source_line_count=source_line_count,
        files=ordered_concept_files,
    )
    write_coverage_json(
        path=coverage_json_path,
        source_line_count=source_line_count,
        files=ordered_concept_files,
        headers=inferred_headers,
    )
    write_metadata_json(
        path=metadata_json_path,
        original_file_name=source_path.name,
        inferred_file_name=inferred_global_name,
        files=ordered_concept_files,
        headers=inferred_headers,
        original_source="original.md",
    )
    print(f"[{tag}] wrote plan + coverage.json + metadata.json")

    print(
        f"[Generation] Done. Created {len(ordered_concept_files)} "
        f"concept files in {docs_dir}. Global name: {inferred_global_name}"
    )


# ---------------------------------------------------------------------
# Batch runner
# ---------------------------------------------------------------------


def collect_source_files(source_path: str) -> list[Path]:
    path = Path(source_path)
    if path.is_file():
        if path.suffix.lower() != ".md":
            raise RuntimeError(f"Source file is not Markdown: {path}")
        return [path]
    if path.is_dir():
        files = sorted(path.glob("*.md"))
        if not files:
            raise RuntimeError(f"No .md files found in folder: {path}")
        return files
    raise RuntimeError(f"Source path does not exist: {path}")


def output_dir_for_source(source_file: Path, output_root: str) -> Path:
    return Path(output_root) / source_file.stem


def make_config_for_source(source_file: Path) -> SimpleNamespace:
    return SimpleNamespace(
        source=str(source_file),
        out=str(output_dir_for_source(source_file, OUTPUT_ROOT)),
        phase=PHASE,
        base_url=BASE_URL,
        api_key=API_KEY,
        gen_model=GEN_MODEL,
        verify_model=VERIFY_MODEL,
        temperature=TEMPERATURE,
        clean=CLEAN_OUTPUT,
    )


async def process_one_source(
    semaphore: asyncio.Semaphore,
    source_file: Path,
    embedder,
) -> None:
    async with semaphore:
        config = make_config_for_source(source_file)

        print("=" * 80)
        print(f"[Batch] Starting: {config.source}")
        print(f"[Batch] Output:   {config.out}")
        print("=" * 80)

        try:
            if config.phase in {"all", "generate"}:
                await phase_generate(config, embedder)
            else:
                raise RuntimeError(
                    f"Unknown PHASE={config.phase!r}. Supported: 'generate', 'all'."
                )
            print(f"[Batch] Done: {config.source}")
        except Exception as exc:  # noqa: BLE001
            print(f"[Batch] FAILED: {config.source}")
            print(f"[Batch] Error: {exc}")


async def async_main() -> None:
    source_files = collect_source_files(SOURCE_PATH)

    print(f"[Batch] Found {len(source_files)} Markdown file(s).")
    print(f"[Batch] File concurrency: {FILE_CONCURRENCY}")

    # One shared embedder for the whole batch (single backend probe / model load).
    embedder = build_embedder()

    semaphore = asyncio.Semaphore(FILE_CONCURRENCY)
    tasks = [
        process_one_source(
            semaphore=semaphore, source_file=source_file, embedder=embedder
        )
        for source_file in source_files
    ]
    await asyncio.gather(*tasks)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
