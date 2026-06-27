#!/usr/bin/env python3

import os
from pathlib import Path
import subprocess
import sys


PDF_DIR = Path("/run/media/blaze/Common/Code/llm-wiki/pdfs")
OUTPUT_DIR = Path("/run/media/blaze/Common/Code/llm-wiki/mineru")
DONE_DIR = OUTPUT_DIR / "_done_markers"

GPU_MEMORY_UTILIZATION = "0.5"   # safer than 0.5
PROCESSING_WINDOW_SIZE = "4"      # use 4; try 8 only if stable


def build_env():
    env = os.environ.copy()

    # MinerU memory controls
    env["MINERU_PROCESSING_WINDOW_SIZE"] = PROCESSING_WINDOW_SIZE
    env["MINERU_PDF_RENDER_THREADS"] = "1"
    env["MINERU_API_MAX_CONCURRENT_REQUESTS"] = "1"

    # CPU thread limits
    env["MINERU_INTRA_OP_NUM_THREADS"] = "2"
    env["MINERU_INTER_OP_NUM_THREADS"] = "1"
    env["OMP_NUM_THREADS"] = "2"
    env["MKL_NUM_THREADS"] = "2"
    env["OPENBLAS_NUM_THREADS"] = "2"
    env["NUMEXPR_NUM_THREADS"] = "2"

    return env


def safe_marker_name(pdf_path: Path) -> str:
    return pdf_path.stem.replace("/", "_") + ".done"


def main():
    if not PDF_DIR.exists():
        print(f"ERROR: PDF directory does not exist: {PDF_DIR}", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DONE_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(
        p for p in PDF_DIR.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        print(f"No PDF files found in: {PDF_DIR}")
        return

    env = build_env()

    print(f"Found {len(pdf_files)} PDF file(s).")
    print(f"PDF dir: {PDF_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"MinerU window size: {PROCESSING_WINDOW_SIZE}")
    print(f"GPU memory utilization: {GPU_MEMORY_UTILIZATION}")
    print("-" * 80)

    completed = 0
    skipped = 0
    failed = 0

    for index, pdf_path in enumerate(pdf_files, start=1):
        done_marker = DONE_DIR / safe_marker_name(pdf_path)

        print(f"[{index}/{len(pdf_files)}] PDF: {pdf_path.name}")

        if done_marker.exists():
            print(f"  SKIP: Already completed: {pdf_path.name}")
            skipped += 1
            print("-" * 80)
            continue

        cmd = [
            "mineru",
            "-p", str(pdf_path),
            "-o", str(OUTPUT_DIR),
            "--gpu-memory-utilization", GPU_MEMORY_UTILIZATION,
        ]

        print("  RUN:", " ".join(cmd))

        try:
            result = subprocess.run(cmd, env=env)
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            sys.exit(130)
        except Exception as e:
            print(f"  ERROR: Failed to start command: {e}", file=sys.stderr)
            failed += 1
            print("-" * 80)
            continue

        if result.returncode == 0:
            done_marker.touch()
            print(f"  DONE: {pdf_path.name}")
            completed += 1
        else:
            print(
                f"  FAILED: {pdf_path.name} returned exit code {result.returncode}",
                file=sys.stderr,
            )
            failed += 1

        print("-" * 80)

    print("Summary")
    print(f"  Total PDFs: {len(pdf_files)}")
    print(f"  Completed:  {completed}")
    print(f"  Skipped:    {skipped}")
    print(f"  Failed:     {failed}")


if __name__ == "__main__":
    main()
