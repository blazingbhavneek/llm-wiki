# Handoff: port `graph2/` → `graph_big2/`

Do for `graph2/` exactly what was already done for `graph/` → `graph_big/`. This is
a **behavior-preserving refactor**: same pipeline, same algorithms, cleaner shape.
`graph_big/` is your reference implementation — read it before starting and mirror
its structure, naming, and conventions.

> NOTE: `graph2/` is being actively edited toward "fewer files / fewer classes."
> Re-read it fresh when you start; do not trust any earlier snapshot.

## The one rule that drives everything

Collapse the package's many service classes (`runtime`/`engine`/`revisions`/`agent`/
`analytics`/etc.) into **one master class `Graph`** that owns all logic, plus a few
pure leaf modules. The only state that may live off `Graph` is per-question agent
run-state, and that lives in a local dataclass, never threaded through calls.

## Target file layout (≈6 files)

```
graph_big2/
├── graph.py     class Graph ONLY — nothing else in the file
├── utils.py     independent helpers + agent scaffolding (never touch a Graph instance)
├── core.py      leaf: ids/hash, scoring, TOKEN_RE, Protocols, ALL prompts
├── models.py    data only: Node/Edge/enums/DTOs/Settings/now_iso. NO internal imports.
├── cli.py       thin argparse → Graph
└── __init__.py  import .models BEFORE .graph; export Graph + models
```

What goes where:

- **`graph.py`** — the `Graph` class and nothing else. No module-level helper
  functions, no tool-schema classes, no mermaid functions. Just `class Graph`.
- **`utils.py`** — everything independent of a `Graph` instance:
  - agent tool schemas (`search`, `read`, `follow_link`, `explore`, `finish` —
    lowercase pydantic models, names = the tool names) + `LEAD_TOOLS` /
    `SUBAGENT_TOOLS` lists.
  - `Subrun` dataclass (per-subagent run state).
  - pure formatters: `node_ref`, `dedupe`, `clean_node_ref`, `format_node_full`.
  - mermaid subsystem: `validate_mermaid`, `repair_answer_mermaid` (+ its regex).
- **`core.py`** — pure leaf, imports nothing internal but `models`:
  - ids/hash: `short_hash`, `source_hash`, `slug`, `make_node_id`,
    `make_exogenous_node_id`, `make_edge_id`.
  - text/scoring: `normalize_token`, `normalize_text`, `jaccard`, `token_jaccard`,
    `claim_keys`, `match_score(old,new)`, `claims_equivalent(old,new)`.
  - `TOKEN_RE` — a **module constant**, never passed as a parameter.
  - Protocols: `LlmClient`, `EmbedderPort`, `RerankerPort` (replace every `object`/
    untyped dependency hint).
  - ALL prompt strings (system + user templates).
- **`models.py`** — data only, **real definitions** (not re-exports), zero internal
  imports. This is the leaf that `db/` and `embeddings/` import. Includes `Settings`
  (+ `from_env`).

## Style rules (apply to every method)

1. **No debug `print` narration.** Use `logging.getLogger("graph")`. Keep only
   operationally useful `info`/`debug` lines (re-embed progress, ingest counts,
   reranker-unavailable). Delete per-step "called with x=..." spam.
2. **No `# === banner ===` comments.** Group methods with `# region NAME` /
   `# endregion` pairs. Region names (same as reference): `lifecycle`,
   `markdown ingest`, `ingest one node + enrichment`, `embeddings`,
   `semantic edges + dedup`, `query / retrieval`, `revision / cascade`,
   `analytics`, `reasoning agent`.
3. **No leading `_` on method names.** Privacy-by-underscore is banned — it's ugly
   and we don't care. Only true instance-state attributes may keep it (`_emit`,
   `_vec_ready`). Every method is a plain name.
4. **One-line docstring per method** saying what it does. Do NOT over-comment inside
   bodies — only a very few genuinely-important edge-case inline comments.
5. **Inline any private called exactly once** — UNLESS it is a substantial named
   algorithm. Keep as methods: the neighborhood BFS, the cascade BFS, exogenous
   regeneration, and the two md-layout loaders. Inline trivial one-shot payload
   builders and 1-line wrappers (e.g. `_mark_stale` → `db.set_node_status(id, stale)`
   at each call site).
6. **Never thread a variable down a call chain.** Shared state lives on `self` or in
   ONE local object passed once. Concretely: `TOKEN_RE` is a `core` constant (not a
   param); the agent's subagent state is a single `Subrun` captured by a closure, not
   `evidence`/`visited`/`state`/`index` re-passed through every hop.

## Drop the LLM override hooks

The old code does `getattr(self.llm, "summarize", None)` (and the same for
`extract_keywords`/`extract_claims`/`suggest_edges`/`check_entity_duplicate`/
`regenerate_exogenous`/`run_agent`) to let test fakes script behavior. **Remove all
of it.** Call `llm.complete` / `llm.complete_structured` / `llm.run_tool_loop`
directly. Tests inject a fake that *implements the `LlmClient` Protocol* instead of
patching methods. (This is an intentional behavioral divergence vs the old tests —
production behavior is identical.)

## Database

- **One backend only: raw SQLite** (FTS5 keyword + sqlite-vec vectors). Delete the
  `lancedb`/`sqlmodel` alternatives if `graph2/db/` still has them.
- **WAL is required** — in the sqlite connection setup add:
  ```python
  conn.execute("PRAGMA journal_mode=WAL")     # persists on the file
  conn.execute("PRAGMA busy_timeout=5000")    # per-connection
  conn.execute("PRAGMA synchronous=NORMAL")   # per-connection
  ```
  Rationale: one writer (ingest) + many readers (HTTP + MCP processes) concurrently.
- **DB decision to confirm with the user:** `graph_big` reuses the shared top-level
  `db/` package, which now imports `graph_big.models` and is WAL+sqlite-only. Decide
  whether `graph_big2` (a) reuses `graph_big.models` so it can share that same `db/`,
  or (b) gets its own model types + its own db copy. Do NOT make the shared `db/`
  import two different model packages.

## Circular-import resolution (do it exactly this way — no guard hacks)

The trap: `db/` and `embeddings/` import the models package; if the package's
`__init__` eagerly imports `.graph`, and `.graph` imports `db`/`embeddings` at module
top, you get a re-entrant import. Fix it structurally:

1. **`models.py`** imports nothing internal (pure leaf). `db/` and `embeddings/`
   import their types from it.
2. **`graph.py`** does NOT import `db` at module top. Use:
   ```python
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from db import Database
   ```
   and a **lazy** `from db import Database` inside `__init__` and inside the subagent
   spawn. `embeddings`/`llm` may stay as top imports (they don't import the models
   package at runtime — see next point).
3. **`embeddings/`** must import `Settings` only as a type hint → put it under
   `if TYPE_CHECKING:` (both `embedder.py` and `reranker.py` already use
   `from __future__ import annotations`, so the hint is a string).
4. **`__init__.py`** loads `.models` BEFORE `.graph`, so the leaf is cached before
   siblings pull it.

Result: every import order works (`graph_big2` first, `db` first, `embeddings`
first, `cli` first) with zero `import graph2` guard lines.

## Independence

`graph_big2/` must have **zero** references to old `graph2/`. Verify:
```bash
grep -rnE "from graph2\.|from graph2 import|^import graph2" graph_big2/ db/ embeddings/ llm/ | grep -v graph_big2   # → empty
mv graph2 graph2_HIDDEN && PYTHONPATH=. .venv/bin/python -c "from graph_big2 import Graph; import graph_big2.cli; print('ok')"; mv graph2_HIDDEN graph2
```

## The Graph class — public surface to preserve

Mirror `graph_big/graph.py`. Public use-cases the CLI/app call:
`ingest_md_output`, `ingest`, `load_md_output`, `query`, `search`, `read`,
`follow_link`, `recon`, `update_node`, `cascading_update`, `create_exogenous_node`,
`get`, `delete`, `health`, `recluster`, `ask`, `close`.

Old → new mapping (adapt to whatever graph2 actually has):

| old (graph2) | new |
|---|---|
| `runtime.*Runtime` (enrich/embed/edges/dedup) | `Graph` methods, `semantic edges + dedup` + `embeddings` regions |
| `*Query` (search/read/follow/traverse) | `Graph` methods, `query / retrieval` region |
| `*Exogenous` | folded into `Graph` (`create_exogenous_node`, `link_supports`) |
| `*Analytics` | `Graph` methods, `analytics` region |
| `*Revisions` | `Graph` methods, `revision / cascade` region |
| `MarkdownIngest` | `Graph` methods, `markdown ingest` region (keep the layout loaders as methods) |
| `QueryAgent` | `Graph` methods, `reasoning agent` region + `Subrun` in utils |
| prompts (wherever they live) | `core.py` |
| `utils.py` ids/scoring | `core.py` |
| `mermaid.py` | functions in `utils.py` |
| `models.py` | `models.py` (real defs) |
| `engine` facade | gone — `Graph` IS the door; `cli.py` constructs it |

## Reasoning agent shape (preserve)

Lead + subagent pattern. `ask` → `run_lead` (tools `search`/`explore`/`finish`,
dispatch is a LOCAL closure). `explore` spawns a `ThreadPoolExecutor` of subagents;
each subagent builds its **own** `Graph(..., subagent=True)` on its **own** DB
connection (worker thread; the engine connection is thread-bound) and runs tools
`search`/`read`/`follow_link`/`finish`. Per-subagent state = one `Subrun` captured by
the dispatch closure. After the loop, repair mermaid (if enabled) and persist the
answer as an exogenous node with `supports` edges.

## Easy-to-miss behavior gaps (check these)

- **Cascade re-clusters.** The old `engine.cascading_update` runs `recluster()` after
  applying the revision. Make sure `Graph.cascading_update` does the same (best-effort
  try/except). (This was missed in the first port and had to be fixed.)
- **Ingest re-clusters** at the end (best-effort).
- **`prepare_embeddings`** runs once at startup (skip when `subagent=True`); rebuilds
  ALL vectors on model/dim change or incomplete coverage.
- **`node_is_complete` skip** in `ingest` (active + body-vector present → skip).
- **Hybrid `search`** = RRF over BM25 + KNN(body) + KNN(summary), then optional
  reranker; degrade to BM25-only if embedding fails.

## Verification before you call it done

```bash
.venv/bin/python -m py_compile graph_big2/*.py
# import orders (all must pass):
PYTHONPATH=. .venv/bin/python -c "from graph_big2 import Graph"
PYTHONPATH=. .venv/bin/python -c "from db import Database; from graph_big2 import Graph"
PYTHONPATH=. .venv/bin/python -c "from embeddings import Embedder; from graph_big2 import Graph"
PYTHONPATH=. .venv/bin/python -c "import graph_big2.cli"
# independence:  hide graph2/, re-import (see above)
# offline smoke: build Graph with a fake LlmClient (complete/complete_structured/
#   run_tool_loop) + fake embedder (dim/embed_document/embed_query) + real sqlite in
#   a tmp path; ingest a few Nodes; assert keyword/vector/search/health work.
```

Write a `graph_big2/DESIGN.md` capturing the final structure (mirror
`graph_big/DESIGN.md`). When done, the old `graph2/` should be deletable with nothing
in the live path referencing it.
```
