"""
Top-level orchestration: hierarchical generation, verification, repair, and
the batch runner. main() is the package entrypoint (../md.py calls it).
Imports from generate: phase_generate_flat (the flat phase it dispatches to).
Imports from planning: the partition-retry loop and tree-render helpers.
Imports from prompts: chunk-summary, H1/layout/leaf, verification, repair builders.
Imports from llm: make_llm, structured_ainvoke.
Imports from models: config constants + ChunkSummary/H1Plan/H1Layout/
LeafPagePlan/RepairResult/VerificationResult.
Imports from utils: chunking, manifest, window and IO helpers.

Package `wiki/` — lossless Markdown wiki generator. Module layout
(low-level to high-level; imports only ever point downward in this list):

- models.py    Runtime config constants (SOURCE_PATH, OUTPUT_ROOT, BASE_URL,
               GEN_MODEL, GENERATION_LINES, ... PARTITION_RETRY_ATTEMPTS) and all
               Pydantic schemas + the CurrentFileState dataclass (FileRef,
               NewFileRef, GenerationDecision, VerificationResult, RepairResult,
               ChunkSummary, TopicRange, H1Plan, H1Layout, LeafPagePlan).
               No wiki imports.
- utils.py     Pure stdlib helpers: line-range/markdown (range_to_markdown,
               clamp_range_to_chunk, split_chunk_ranges), file/JSON IO
               (read_lines, write_json, load_json), filenames/slugs
               (slugify, make_unique_filename), source chunking
               (chunk_source_lines_preserving_tables, fixed_windows), manifest +
               markdown-file records (init_manifest, add_or_update_file_record,
               create_markdown_file, add_chunk_record,
               find_best_target_for_source_window, overlap_size),
               extract_json_from_text. No wiki imports.
- llm.py       LLM client: make_llm, structured_ainvoke (structured-output call
               with JSON fallback). Imports: utils.
- prompts.py   All prompt builders build_*_prompt (chunk summary, H1 plan, H1
               layout, leaf page, generation, verification, repair).
               Imports: models.
- planning.py  Hierarchy planning + tree rendering: chunk-summary ledger
               (format_summary_ledger, summaries_for_range), exact-partition
               validation (validate_exact_partition,
               structured_partition_ainvoke_with_retries, partition_or_fallback,
               assert_exact_coverage) and the wiki-tree writers
               (render_hierarchical_wiki, write_navigation_index,
               write_topic_plan_document, hierarchy_to_manifest,
               planned_leaf_pages). Imports: models, utils, llm.
- generate.py  Flat (non-hierarchical) generation phase: enforce_generation_rules,
               parse_part_number, forced_part_ref, phase_generate_flat.
               Imports: models, utils, prompts, llm.
- phases.py    Hierarchical generation (phase_generate), verification
               (verify_one_window, phase_verify), repair (phase_repair) and the
               batch runner / entrypoint (collect_source_files,
               make_config_for_source, process_one_source, async_main, main).
               Imports: generate, planning, prompts, utils, llm, models.

Entrypoint: ../md.py is a thin shim that calls wiki.phases.main.
"""
from __future__ import annotations

import argparse
import asyncio
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional

from langchain_openai import ChatOpenAI

from wiki.models import (
    API_KEY,
    BASE_URL,
    CLEAN_OUTPUT,
    CONCURRENCY,
    ChunkSummary,
    FILE_CONCURRENCY,
    GENERATION_LINES,
    GEN_MODEL,
    H1Layout,
    H1Plan,
    LeafPagePlan,
    MAX_CHUNK_EXTRA,
    OUTPUT_ROOT,
    PARTITION_RETRY_ATTEMPTS,
    PHASE,
    RepairResult,
    SOURCE_PATH,
    TEMPERATURE,
    TIMEOUT,
    VERIFICATION_LINES,
    VERIFY_MODEL,
    VerificationResult,
)
from wiki.utils import (
    append_markdown,
    chunk_source_lines_preserving_tables,
    find_best_target_for_source_window,
    fixed_windows,
    init_manifest,
    load_json,
    numbered_source_lines,
    read_lines,
    utc_now_iso,
    write_json,
)
from wiki.prompts import (
    build_chunk_summary_prompt,
    build_h1_layout_prompt,
    build_h1_plan_prompt,
    build_leaf_page_plan_prompt,
    build_repair_prompt,
    build_verification_prompt,
)
from wiki.planning import (
    allowed_chunk_ranges,
    append_chunk_summary_document,
    assert_exact_coverage,
    format_summary_ledger,
    hierarchy_to_manifest,
    initialize_chunk_summary_document,
    planned_leaf_pages,
    render_hierarchical_wiki,
    structured_partition_ainvoke_with_retries,
    summaries_for_range,
    write_topic_plan_document,
)
from wiki.generate import phase_generate_flat
from wiki.llm import make_llm, structured_ainvoke


async def phase_generate(args: argparse.Namespace) -> None:
    """Plan first, prove leaf coverage, then render the hierarchical wiki tree."""
    source_path = Path(args.source)
    out_dir = Path(args.out)
    manifest_path = out_dir / "manifest.json"

    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if manifest_path.exists() and not args.clean:
        raise RuntimeError(
            f"{manifest_path} already exists. Use --clean to regenerate from scratch."
        )

    source_lines = read_lines(source_path)
    chunks = chunk_source_lines_preserving_tables(
        source_lines,
        target_size=args.generation_lines,
        max_extra=args.max_chunk_extra,
    )
    manifest = init_manifest(source_path)
    planning_dir = out_dir / "_planning"
    summary_path = planning_dir / "chunk-summaries.md"
    topic_plan_path = planning_dir / "topic-index.md"
    coverage_path = planning_dir / "coverage.json"
    initialize_chunk_summary_document(summary_path, source_path)

    llm = make_llm(
        model=args.gen_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=args.temperature,
        timeout=args.timeout,
    )

    summaries: list[dict[str, Any]] = []
    for chunk_number, (start_idx, end_idx) in enumerate(chunks, start=1):
        source_start = start_idx + 1
        source_end = end_idx
        previous_start_idx = max(0, start_idx - 100)
        previous_block = numbered_source_lines(
            source_lines[previous_start_idx:start_idx],
            previous_start_idx + 1,
        )
        source_block = numbered_source_lines(source_lines[start_idx:end_idx], source_start)
        prior_ledger = summary_path.read_text(encoding="utf-8")

        print(
            f"[Planning] Summarizing chunk {chunk_number}/{len(chunks)} "
            f"source lines {source_start}-{source_end}"
        )
        result = await structured_ainvoke(
            llm,
            ChunkSummary,
            build_chunk_summary_prompt(
                previous_source_block=previous_block,
                prior_summary_ledger=prior_ledger,
                source_block=source_block,
                source_start=source_start,
                source_end=source_end,
            ),
        )
        summary = ChunkSummary.model_validate(result)
        record = {
            "source_start": source_start,
            "source_end": source_end,
            **summary.model_dump(),
        }
        summaries.append(record)
        append_chunk_summary_document(summary_path, source_start, source_end, summary)
        manifest["planning"]["chunk_summaries"] = summaries
        manifest["updated_at"] = utc_now_iso()
        write_json(manifest_path, manifest)

    if not source_lines:
        hierarchy: list[dict[str, Any]] = []
    else:
        summary_ledger = format_summary_ledger(summaries)
        all_chunk_ranges = allowed_chunk_ranges(summaries, 1, len(source_lines))
        
        h1_prompt = build_h1_plan_prompt(
            summary_ledger=summary_ledger,
            source_line_count=len(source_lines),
            chunk_ranges=all_chunk_ranges,
        )

        h1_plan, h1_sections = await structured_partition_ainvoke_with_retries(
            llm=llm,
            schema_cls=H1Plan,
            base_messages=h1_prompt,
            extract_topics=lambda plan: plan.sections,
            source_start=1,
            source_end=len(source_lines),
            valid_chunk_ranges=all_chunk_ranges,
            fallback_title=source_path.stem.replace("-", " ").title(),
            fallback_summary="Complete source document.",
            label="H1",
            max_retries=args.partition_retries,
        )

        # Stage 2: decide every H1's shape before any H2 is expanded into pages.
        h1_layouts: list[dict[str, Any]] = []
        for h1 in h1_sections:
            h1_start, h1_end = h1.source_range or [0, 0]
            h1_summaries = summaries_for_range(summaries, h1_start, h1_end)
            h1_ranges = allowed_chunk_ranges(summaries, h1_start, h1_end)
            layout_prompt = build_h1_layout_prompt(
                h1=h1,
                summary_ledger=format_summary_ledger(h1_summaries),
                chunk_ranges=h1_ranges,
            )

            layout, layout_sections = await structured_partition_ainvoke_with_retries(
                llm=llm,
                schema_cls=H1Layout,
                base_messages=layout_prompt,
                extract_topics=lambda plan: plan.sections,
                source_start=h1_start,
                source_end=h1_end,
                valid_chunk_ranges=h1_ranges,
                fallback_title=h1.title,
                fallback_summary=h1.summary or "Source section.",
                label=f"{h1.title} layout",
                max_retries=args.partition_retries,
            )
            h1_layouts.append(
                {
                    "h1": h1,
                    "use_h2_folders": layout.use_h2_folders,
                    "sections": layout_sections,
                }
            )

        # Stage 3: all chosen H2 sections are now split into final files.
        hierarchy = []
        for h1_layout in h1_layouts:
            h1 = h1_layout["h1"]
            if not h1_layout["use_h2_folders"]:
                hierarchy.append(
                    {
                        "h1": h1,
                        "use_h2_folders": False,
                        "groups": [{"topic": h1, "pages": h1_layout["sections"]}],
                    }
                )
                continue

            groups: list[dict[str, Any]] = []
            for h2 in h1_layout["sections"]:
                h2_start, h2_end = h2.source_range or [0, 0]
                h2_summaries = summaries_for_range(summaries, h2_start, h2_end)
                h2_ranges = allowed_chunk_ranges(summaries, h2_start, h2_end)
                leaf_prompt = build_leaf_page_plan_prompt(
                    parent=h2,
                    parent_label="H2 section",
                    summary_ledger=format_summary_ledger(h2_summaries),
                    chunk_ranges=h2_ranges,
                )

                leaf_plan, pages = await structured_partition_ainvoke_with_retries(
                    llm=llm,
                    schema_cls=LeafPagePlan,
                    base_messages=leaf_prompt,
                    extract_topics=lambda plan: plan.pages,
                    source_start=h2_start,
                    source_end=h2_end,
                    valid_chunk_ranges=h2_ranges,
                    fallback_title=h2.title,
                    fallback_summary=h2.summary or "Source section.",
                    label=f"{h2.title} leaf page",
                    max_retries=args.partition_retries,
                )
                groups.append({"topic": h2, "pages": pages})

            hierarchy.append(
                {"h1": h1, "use_h2_folders": True, "groups": groups}
            )

    leaves = planned_leaf_pages(hierarchy)
    assert_exact_coverage(leaves, len(source_lines))
    write_topic_plan_document(topic_plan_path, hierarchy)

    manifest["planning"]["hierarchy"] = hierarchy_to_manifest(hierarchy)
    manifest["planning"]["coverage_verified_at"] = utc_now_iso()
    coverage = render_hierarchical_wiki(out_dir, source_lines, manifest, hierarchy)
    manifest["coverage"] = coverage
    manifest["updated_at"] = utc_now_iso()
    write_json(manifest_path, manifest)
    write_json(
        coverage_path,
        {
            "source": str(source_path),
            "source_line_count": len(source_lines),
            "exact_coverage": True,
            "assignments": coverage,
        },
    )
    print(f"[Generation] Done. Hierarchical wiki written to {out_dir}")

async def verify_one_window(
    semaphore: asyncio.Semaphore,
    llm: ChatOpenAI,
    out_dir: Path,
    manifest: dict[str, Any],
    source_lines: list[str],
    start_idx: int,
    end_idx: int,
) -> Optional[dict[str, Any]]:
    async with semaphore:
        source_start = start_idx + 1
        source_end = end_idx

        target_filename = find_best_target_for_source_window(
            manifest,
            source_start,
            source_end,
        )

        if target_filename is None:
            return None

        target_path = out_dir / target_filename
        if not target_path.exists():
            return {
                "source_start": source_start,
                "source_end": source_end,
                "target_file": target_filename,
                "answer": "YES",
                "missing_facts": [f"Target file does not exist: {target_filename}"],
                "hallucinations": [],
                "reason": "Manifest points to a missing file.",
                "status": "flagged",
            }

        source_block = numbered_source_lines(source_lines[start_idx:end_idx], source_start)
        wiki_content = target_path.read_text(encoding="utf-8")

        messages = build_verification_prompt(
            source_block=source_block,
            target_filename=target_filename,
            wiki_content=wiki_content,
        )

        result = await structured_ainvoke(llm, VerificationResult, messages)
        result = VerificationResult.model_validate(result)

        if result.answer == "YES":
            return {
                "source_start": source_start,
                "source_end": source_end,
                "target_file": target_filename,
                "answer": result.answer,
                "missing_facts": result.missing_facts,
                "hallucinations": result.hallucinations,
                "reason": result.reason,
                "status": "flagged",
            }

        return None


async def phase_verify(args: argparse.Namespace) -> None:
    source_path = Path(args.source)
    out_dir = Path(args.out)
    manifest_path = out_dir / "manifest.json"

    if not manifest_path.exists():
        raise RuntimeError(f"Missing manifest: {manifest_path}")

    source_lines = read_lines(source_path)
    manifest = load_json(manifest_path)

    windows = fixed_windows(source_lines, args.verification_lines)

    llm = make_llm(
        model=args.verify_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=0.0,
        timeout=args.timeout,
    )

    semaphore = asyncio.Semaphore(args.concurrency)

    print(
        f"[Verification] Checking {len(windows)} windows "
        f"with concurrency={args.concurrency}"
    )

    tasks = [
        verify_one_window(
            semaphore=semaphore,
            llm=llm,
            out_dir=out_dir,
            manifest=manifest,
            source_lines=source_lines,
            start_idx=start,
            end_idx=end,
        )
        for start, end in windows
    ]

    results = await asyncio.gather(*tasks)
    flags = [result for result in results if result is not None]

    manifest["verification_flags"] = flags
    manifest["updated_at"] = utc_now_iso()

    write_json(manifest_path, manifest)
    write_json(out_dir / "verification_flags.json", {"flags": flags})

    print(f"[Verification] Done. Flagged windows: {len(flags)}")

async def phase_repair(args: argparse.Namespace) -> None:
    source_path = Path(args.source)
    out_dir = Path(args.out)
    manifest_path = out_dir / "manifest.json"

    if not manifest_path.exists():
        raise RuntimeError(f"Missing manifest: {manifest_path}")

    source_lines = read_lines(source_path)
    manifest = load_json(manifest_path)

    flags = manifest.get("verification_flags", [])

    if not flags:
        print("[Repair] No verification flags found. Nothing to repair.")
        return

    llm = make_llm(
        model=args.verify_model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=0.0,
        timeout=args.timeout,
    )

    repaired_count = 0

    for index, flag in enumerate(flags, start=1):
        if flag.get("status") == "repaired":
            continue

        source_start = int(flag["source_start"])
        source_end = int(flag["source_end"])
        target_filename = flag["target_file"]

        target_path = out_dir / target_filename

        print(
            f"[Repair] {index}/{len(flags)} "
            f"source lines {source_start}-{source_end} -> {target_filename}"
        )

        if not target_path.exists():
            flag["status"] = "repair_failed"
            flag["repair_error"] = f"Target file missing: {target_filename}"
            continue

        source_block = numbered_source_lines(
            source_lines[source_start - 1 : source_end],
            source_start,
        )

        wiki_content = target_path.read_text(encoding="utf-8")

        messages = build_repair_prompt(
            source_block=source_block,
            target_filename=target_filename,
            wiki_content=wiki_content,
            missing_facts=flag.get("missing_facts", []),
            hallucinations=flag.get("hallucinations", []),
        )

        try:
            result = await structured_ainvoke(llm, RepairResult, messages)
            result = RepairResult.model_validate(result)

            patch = result.markdown_patch.strip()

            if patch:
                repair_block = (
                    f"\n\n---\n\n"
                    f"## Repair Addendum: Source lines {source_start}-{source_end}\n\n"
                    f"{patch}\n"
                )
                append_markdown(target_path, repair_block)

            flag["status"] = "repaired"
            flag["repair_reason"] = result.reason
            flag["repaired_at"] = utc_now_iso()
            repaired_count += 1

        except Exception as exc:
            flag["status"] = "repair_failed"
            flag["repair_error"] = str(exc)

        manifest["updated_at"] = utc_now_iso()
        write_json(manifest_path, manifest)

    print(f"[Repair] Done. Repaired flags: {repaired_count}")

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
    """
    Example:
    /input/mpf.md + /output/ -> /output/mpf/
    """
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
        generation_lines=GENERATION_LINES,
        verification_lines=VERIFICATION_LINES,
        max_chunk_extra=MAX_CHUNK_EXTRA,
        concurrency=CONCURRENCY,
        temperature=TEMPERATURE,
        timeout=TIMEOUT,
        clean=CLEAN_OUTPUT,
        partition_retries=PARTITION_RETRY_ATTEMPTS
    )


async def process_one_source(
    semaphore: asyncio.Semaphore,
    source_file: Path,
) -> None:
    async with semaphore:
        config = make_config_for_source(source_file)

        print("=" * 80)
        print(f"[Batch] Starting: {config.source}")
        print(f"[Batch] Output:   {config.out}")
        print("=" * 80)

        try:
            if config.phase == "generate-flat":
                await phase_generate_flat(config)
            elif config.phase in {"all", "generate"}:
                await phase_generate(config)

            if config.phase in {"all", "verify"}:
                await phase_verify(config)

            if config.phase in {"all", "repair"}:
                await phase_repair(config)

            print(f"[Batch] Done: {config.source}")

        except Exception as exc:
            print(f"[Batch] FAILED: {config.source}")
            print(f"[Batch] Error: {exc}")


async def async_main() -> None:
    source_files = collect_source_files(SOURCE_PATH)

    print(f"[Batch] Found {len(source_files)} Markdown file(s).")
    print(f"[Batch] File concurrency: {FILE_CONCURRENCY}")

    semaphore = asyncio.Semaphore(FILE_CONCURRENCY)

    tasks = [
        process_one_source(
            semaphore=semaphore,
            source_file=source_file,
        )
        for source_file in source_files
    ]

    await asyncio.gather(*tasks)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
