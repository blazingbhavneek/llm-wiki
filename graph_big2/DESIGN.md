# graph_big2 — design

A behavior-preserving refactor of `graph2/` into one master `Graph` class plus a
few pure leaf modules. Same pipeline, same algorithms, cleaner shape. Mirrors the
`graph_big/` port of `graph/`, but ingests the **global `output_wiki` layout**
produced by `wiki_gen` (not just md.py outputs), and is fully **standalone** — it
carries its own `models`, `db`, and `embeddings` and references nothing in old
`graph2/`.

## File layout

```
graph_big2/
├── graph.py            class Graph ONLY — every graph operation as a method
├── core.py             leaf: ids/hash, scoring, TOKEN_RE, Protocols, ALL prompts
├── utils.py            leaf: agent tool schemas, Subrun, formatters, mermaid subsystem
├── models.py           data only: Node/Edge/enums/DTOs/Settings/now_iso. No internal imports.
├── cli.py              thin argparse → Graph
├── __init__.py         imports .models BEFORE .graph; exports Graph + models
├── db/                 raw SQLite backend (FTS5 + sqlite-vec + WAL), own model types
│   ├── base.py         BaseDatabase ABC
│   ├── raw_sqlite.py   RawSqliteDatabase (the one backend)
│   └── __init__.py     Database = RawSqliteDatabase
└── embeddings/         Embedder + Reranker (server backend, HF fallback)
    ├── embedder.py
    ├── reranker.py
    └── __init__.py
```

## The one rule

All logic lives on `Graph`. The only off-`Graph` state is per-subagent run state,
held in a `utils.Subrun` captured by the dispatch closure — never threaded through
call signatures. The old `graph2` service classes collapse as:

| graph2 | graph_big2 |
|---|---|
| `GraphRuntime` (enrich/embed/edges/dedup) | `Graph` — `ingest one node + enrichment`, `embeddings`, `semantic edges + dedup` regions |
| `GraphQuery` (search/read/follow/traverse) | `Graph` — `query / retrieval` region |
| `GraphExogenous` | `Graph` — `create_exogenous_node`, `link_supports` |
| `GraphAnalytics` | `Graph` — `analytics` region (`health`, `recluster`) |
| `GraphRevisions` | `Graph` — `revision / cascade` region |
| `MarkdownIngest` (3 layouts) | `Graph` — `markdown ingest` region (layout loaders kept as methods) |
| `QueryAgent` (lead + subagents) | `Graph` — `reasoning agent` region + `Subrun` in utils |
| `DomainEngine` facade | gone — `Graph` IS the door; `cli.py` constructs it |
| prompts (in runtime.py) | `core.py` |
| ids/scoring (utils.py) | `core.py` (`TOKEN_RE` is a module constant, not a param) |
| `mermaid.py` | functions in `utils.py`, fix-prompt in `core.py` |

## Markdown ingest — three layouts

`load_md_output()` dispatches on directory shape:
1. `manifest.json` present → `load_old_manifest_output` (section-adjacency `follows`).
2. `raw/` + page-type folders (`entities/concepts/summaries/indexes`) →
   `load_global_wiki_output` (the `wiki_gen` `output_wiki` layout).
3. otherwise `_planning/` + `docs/` → `load_new_planning_docs_output` (linear `follows`).

The global-wiki path builds one **source-anchor** node per preserved `raw/<doc>`
document and one node per wiki page, then emits `follows` (intra-folder order),
`wiki_cites_source` / `source_supports_wiki` (citations to source anchors), and
`wiki_links_to` (inline markdown links between pages).

**Slug normalization (`slug_key`).** `wiki_gen` keys its planning JSON
(`page_sources.json`, `page_metadata.json`, `global_catalog.json`) by the raw page
slug, which is sometimes bare (`assertion`) and sometimes type-prefixed
(`concept/assertion`), while the file is always `<folder>/<stem>.md`. `slug_key`
collapses to the part after the last `/` so folder-derived page slugs match either
style; without it, bare-slug pages would lose their catalog title/summary/aliases
and planning citations. Verified parity on the real `output_wiki`: 475 nodes,
1411 edges (469 `follows` + 471 + 471 citation edges).

`replace_structural_edges` clears `follows` for ordinary documents and
additionally the wiki citation/link labels when re-ingesting `global_wiki`, so a
re-ingest is idempotent.

## Backends & no override hooks

`Graph` calls `llm.complete` / `llm.complete_structured` / `llm.run_tool_loop`
directly (Protocols in `core.py`). The old `getattr(self.llm, "summarize", ...)`
test-override hooks are gone; tests inject a fake that implements the `LlmClient`
Protocol. The reranker is optional — retrieval degrades to fused (BM25 + KNN) order
if it is unavailable.

## Database

One backend: raw SQLite — FTS5 keyword search + sqlite-vec vectors. WAL is on
(`journal_mode=WAL`, `busy_timeout=5000`, `synchronous=NORMAL`) so the single
ingest writer never blocks the HTTP/MCP readers. `db/` imports `graph_big2.models`
only (its own copy), so this package shares no model types with `graph_big`.

## Circular-import resolution

- `models.py` imports nothing internal (pure leaf); `db/` and `embeddings/`
  import their types from it.
- `graph.py` imports `db` lazily (inside `__init__` and the subagent spawn) and
  only as a `TYPE_CHECKING` hint at module top.
- `embeddings/` references `Settings` only under `TYPE_CHECKING`.
- `__init__.py` loads `.models` before `.graph`.

Every import order works (`graph_big2` first, `db` first, `embeddings` first,
`cli` first), and the package imports with old `graph2/` and `graph_big/` both
removed.

## Reasoning agent

Lead + subagent pattern. `ask` → `run_lead` (tools `search` / `explore` / `finish`,
dispatch is a local closure). `explore` spawns a `ThreadPoolExecutor` of
subagents; each builds its **own** `Graph(..., subagent=True)` on its **own** DB
connection (worker thread; the engine connection is thread-bound) and runs
`search` / `read` / `follow_link` / `finish`. Per-subagent state is one `Subrun`.
After the loop, mermaid is repaired (when enabled) and the answer is persisted as
an exogenous node with `supports` edges.

## Verification

```bash
python -m py_compile graph_big2/*.py graph_big2/db/*.py graph_big2/embeddings/*.py
PYTHONPATH=. python -c "from graph_big2 import Graph"
PYTHONPATH=. python -c "from graph_big2.db import Database; from graph_big2 import Graph"
PYTHONPATH=. python -c "from graph_big2.embeddings import Embedder; from graph_big2 import Graph"
PYTHONPATH=. python -c "import graph_big2.cli"
# independence: hide graph2/ and graph_big/, re-import → still works
# offline smoke: fake LlmClient + fake embedder + real sqlite tmp → ingest, search, health
```
