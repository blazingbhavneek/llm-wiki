"""
Hardcoded runtime config + schemas for the embedding-hybrid wiki chunker.

This package is a structure-agnostic alternative to wiki_new. Instead of asking
a small local LLM to emit a full partition through a ~100-line keyhole (which
shreds headingless / OCR'd markdown), it chunks in two reliable stages:

- Method A (deterministic): paragraph-block embeddings -> cosine distance
  between consecutive blocks -> high-distance gaps are candidate boundaries.
- Method B (LumberChunker-style): the LLM only CONFIRMS a single candidate
  boundary at a time (yes/no), never invents ranges.

Boundaries are gated by size (TARGET_LINES min, MAX_LINES hard cap) so output is
"fewer, larger" pages. Rendering, coverage validation, enrichment and the JSON
writers are reused verbatim from wiki_new.planning.

Entrypoint: ../md2.py calls wiki_embed.phases.main
"""

from __future__ import annotations

import os
from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------
# Runtime config (hardcoded, mirrors wiki_new.models style)
# ---------------------------------------------------------------------

SOURCE_PATH = "/run/media/blaze/Common/Code/llm-wiki/input"
OUTPUT_ROOT = "/run/media/blaze/Common/Code/llm-wiki/output_embed"

PHASE = "all"  # all | generate

# Chat LLM (boundary confirmation + enrichment).
BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://180.21.170.235:42374/v1")
API_KEY = os.environ.get("OPENAI_API_KEY", "local")

GEN_MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"
VERIFY_MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"

TEMPERATURE = 0.0
TIMEOUT = 300

# Number of input markdown files processed at the same time.
FILE_CONCURRENCY = 4

CLEAN_OUTPUT = True

# ---------------------------------------------------------------------
# Segmentation knobs
# ---------------------------------------------------------------------

# A section must reach TARGET_LINES before any boundary may be taken, and is
# force-cut once it reaches MAX_LINES even without a semantic boundary.
TARGET_LINES = 300
MAX_LINES = 700

# Top (100 - SEM_PERCENTILE)% of consecutive-block distances are candidate cuts.
SEM_PERCENTILE = 85.0

# Method B: have the LLM refine each size-eligible semantic boundary by picking
# the exact start-of-next-section line within a window around the dip.
USE_LLM_CONFIRM = True

# Numbered source lines shown before/after the candidate dip in the refine
# prompt. The LLM may move the cut anywhere inside this window.
REFINE_BACK_LINES = 40
REFINE_FWD_LINES = 60

# Blocks embedded per server round-trip.
EMBED_BATCH = 64

# How many embedding batches are in flight at once. >1 speeds up the server
# backend a lot; keep low (1-2) for a single local HF GPU model.
EMBED_CONCURRENCY = 8

# How many boundary-refine LLM calls run at once. Anchors are independent, so
# they refine in parallel; cap to the chat server's comfortable concurrency.
REFINE_CONCURRENCY = 8

# ---------------------------------------------------------------------
# Embedding backend (consumed by embeddings.Embedder via graph.models.Settings)
# ---------------------------------------------------------------------

EMBED_BACKEND = os.environ.get("WIKI_EMBED_BACKEND", "server")
EMBED_BASE_URL = os.environ.get(
    "WIKI_EMBED_BASE_URL",
    os.environ.get("OPENAI_EMBED_BASE_URL", "http://localhost:8080/v1"),
)
EMBED_API_KEY = os.environ.get("WIKI_EMBED_API_KEY", "local")
EMBED_MODEL = os.environ.get("WIKI_EMBED_MODEL", "/run/media/blaze/Common/Code/llm-wiki/Qwen/Qwen3-Embedding-0.6B")
HF_EMBED_MODEL = os.environ.get("WIKI_HF_EMBED_MODEL", "/run/media/blaze/Common/Code/llm-wiki/Qwen/Qwen3-Embedding-0.6B")
HF_DEVICE = os.environ.get("WIKI_HF_DEVICE", "cuda:0")


def build_embedder():
    """Construct the shared Embedder using the hardcoded backend config."""
    from graph.models import Settings
    from embeddings.embedder import Embedder

    settings = Settings(
        embed_backend=EMBED_BACKEND,
        embed_base_url=EMBED_BASE_URL,
        embed_api_key=EMBED_API_KEY,
        embed_model=EMBED_MODEL,
        hf_embed_model=HF_EMBED_MODEL,
        hf_device=HF_DEVICE,
    )
    return Embedder(settings)


# ---------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------


class BoundaryDecision(BaseModel):
    """Exact-line boundary refinement around a semantic dip.

    action "cut": boundary_line is the exact 1-based source line where the next
    section begins (may be moved past a trailing summary/recap of the previous
    section). action "keep": no real boundary here; merge across the dip.
    """

    action: Literal["cut", "keep"] = "cut"
    boundary_line: int | None = None
    reason: str = Field(default="")
