"""Parallel FastAPI backend for the hierarchical wiki *view* layer.

This is intentionally separate from ``app.py`` (the graph engine API). It serves
the deterministic source/chapter/page navigation built by
``wiki_gen.views.ViewBuilder`` over an ``output_wiki`` directory, plus the raw
markdown of any canonical page so the frontend can render it.

Run:
    pip install fastapi "uvicorn[standard]"
    WIKI_OUTPUT=output_wiki uvicorn app2:app --reload --port 8788

Env:
    WIKI_OUTPUT   path to the generated wiki root (default: ./output_wiki)

The view tree is cached in memory and rebuilt on demand via POST /api/wiki/rebuild.
Optional graph2 cluster labels are NOT required: grouping is purely source-line
based, so the view works even with no graph DB present.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from wiki_gen.views import ViewBuilder

WIKI_ROOT = Path(os.environ.get("WIKI_OUTPUT", "output_wiki")).resolve()

app = FastAPI(title="LLM-Wiki View API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# region VIEW CACHE
_tree: dict[str, Any] | None = None


def _build_tree(write: bool = True) -> dict[str, Any]:
    if not WIKI_ROOT.is_dir():
        raise HTTPException(status_code=503, detail=f"wiki root not found: {WIKI_ROOT}")
    builder = ViewBuilder(WIKI_ROOT)
    return builder.write() if write else builder.build()


def _get_tree() -> dict[str, Any]:
    global _tree
    if _tree is None:
        # Prefer a cached navigation.json; rebuild only if absent.
        nav = WIKI_ROOT / "views" / "navigation.json"
        if nav.exists():
            import json

            _tree = json.loads(nav.read_text(encoding="utf-8"))
        else:
            _tree = _build_tree(write=True)
    return _tree


# endregion VIEW CACHE


# region ENDPOINTS
@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"ok": WIKI_ROOT.is_dir(), "wiki_root": str(WIKI_ROOT)}


@app.get("/api/wiki/navigation")
def navigation() -> dict[str, Any]:
    """Full navigation tree: sources -> sections -> pages, plus orphans."""

    return _get_tree()


@app.get("/api/wiki/tree")
def tree() -> dict[str, Any]:
    """Lightweight tree: source + section headers, no page bodies/summaries."""

    full = _get_tree()
    sources = [
        {
            "doc_id": s["doc_id"],
            "name": s["name"],
            "title": s["title"],
            "page_count": s["page_count"],
            "line_count": s["line_count"],
            "sections": [
                {
                    "header": sec["header"],
                    "title": sec["title"],
                    "page_count": sec["page_count"],
                }
                for sec in s["sections"]
            ],
            "unsectioned_count": len(s["unsectioned"]),
        }
        for s in full["sources"]
    ]
    return {
        "generated_at": full["generated_at"],
        "source_count": full["source_count"],
        "page_count": full["page_count"],
        "orphan_count": full["orphan_count"],
        "sources": sources,
    }


@app.get("/api/wiki/source/{doc_id}")
def source(doc_id: str) -> dict[str, Any]:
    """One source document subtree (all sections + pages)."""

    for s in _get_tree()["sources"]:
        if s["doc_id"] == doc_id:
            return s
    raise HTTPException(status_code=404, detail=f"source not found: {doc_id}")


@app.get("/api/wiki/page")
def page(path: str = Query(..., description="canonical page path, relative to wiki root")) -> dict[str, Any]:
    """Return the raw markdown of a canonical wiki page (read-only, sandboxed)."""

    target = (WIKI_ROOT / path).resolve()
    try:
        target.relative_to(WIKI_ROOT)
    except ValueError:
        raise HTTPException(status_code=400, detail="path escapes wiki root")
    if target.suffix.lower() != ".md" or not target.is_file():
        raise HTTPException(status_code=404, detail=f"page not found: {path}")
    return {
        "path": path,
        "content": target.read_text(encoding="utf-8", errors="ignore"),
    }


@app.post("/api/wiki/rebuild")
def rebuild() -> dict[str, Any]:
    """Regenerate the view layer from current ``output_wiki`` contents."""

    global _tree
    _tree = _build_tree(write=True)
    return {
        "rebuilt": True,
        "source_count": _tree["source_count"],
        "page_count": _tree["page_count"],
        "orphan_count": _tree["orphan_count"],
    }


# endregion ENDPOINTS
