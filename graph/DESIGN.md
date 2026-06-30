# graph — target design

Refactor target for the `graph/` package. Behavior-preserving: tests stay green
at every phase. This replaces the current flat bag of six service objects
(`GraphRuntime`, `GraphQuery`, `GraphExogenous`, `GraphAnalytics`,
`GraphRevisions`, `QueryAgent`) that all share `(db, embedder, llm, settings)`
and reach into each other's `_private` methods.

## Goals

1. Reads like a human wrote it: meaningful names, no debug-print narration, no
   dead placeholder blocks.
2. One door in (`DomainEngine`). Logic in a few real classes, not many fake ones.
3. Dependencies point one way only.

## Hard rules

- **Inline any private called exactly once** — unless it is a substantial named
  algorithm (graph BFS, cascade walk, exogenous regen). One-shot payload builders
  and 1-line wrappers die.
- **No variable threaded down a call chain.** Shared state lives on `self` or in
  one local object passed once. Today `_TOKEN_RE`, `evidence`, `visited`,
  `state`, and the `agent` index get re-passed through every hop — that ends.
- **Arrows point down only.** Leaf never imports a service; service never imports
  an orchestrator; orchestrator never imports the engine. An upward arrow means
  the code is in the wrong layer.
- **No raw `print`.** Use `logging.getLogger("graph")`. Keep only operationally
  useful lines (re-embed progress, ingest counts, reranker-unavailable) at
  `info`/`debug`; delete the per-step narration.

## Why not one `Graph` class

One class holding ingest + enrich + embed + edges + query + revise + cascade +
analytics is ~700 lines: a god-object by size, even if it has one job on paper.
But it is NOT one indivisible thing — it has two genuine internal seams:

- **read vs write** — the query path (search/read/follow/traverse) has a
  different *consumer*: the reasoning agent and its subagents need read-only
  access, on their own DB connections. The write path (ingest/edges/cascade) is
  only ever driven by the engine.
- **build vs revise** — revision/cascade sits *on top of* the build primitives:
  `cascading_update` calls `persist_node`, which calls enrich + embed + edges.
  Revise depends on build; build never depends on revise.

Splitting at those two seams is cohesion-driven (who calls whom, who consumes
what), unlike the old split which was just "everything shares the same deps."

## Structure

```
graph/
├── engine.py    class DomainEngine      ROOT door. wire + expose use-cases. thin.
├── builder.py   class GraphBuilder       write primitives: ingest/enrich/embed/edges/exogenous
├── reviser.py   class GraphReviser        recon/revise/cascade. HOLDS a GraphBuilder.
├── reader.py    class GraphReader         read-only: search/read/follow/query/traverse
├── agent.py     class ReasoningAgent      per-question loop + subagents. HOLDS a GraphReader.
│                + repair_answer_mermaid() module funcs (mermaid validate/repair)
├── analytics.py class Analytics           health + Louvain recluster. read-only.
├── models.py    Node Edge enums · DTOs · Settings(+from_env) · event dataclasses
├── core.py      LEAF: ids/hash · jaccard/match_score · Protocols · prompts. no internal imports.
└── cli.py       thin, calls DomainEngine
```

Down from 6 logic classes / 11 files to **4 logic classes + thin engine / 8 files**.
Each logic class ~250–400 lines, single responsibility, real cohesion.

## Dependency graph (arrows point down)

```
                 cli.py
                   │
              ┌────▼─────────┐
              │ DomainEngine │  wires all, exposes ingest/query/ask/recon/cascade
              └──┬───┬───┬───┬┘
       ┌─────────┘   │   │   └────────────┐
       ▼             ▼   ▼                ▼
  GraphReviser   Analytics  ReasoningAgent
       │                         │
       ▼                         ▼
  GraphBuilder              GraphReader
       └───────────┬─────────────┘
                   ▼
        core.py · models.py · (ports → db/ embeddings/ llm/)
```

- `GraphReviser` → holds `GraphBuilder` (calls `persist_node`, `build_semantic_edges`, `create_exogenous_node`).
- `ReasoningAgent` → holds `GraphReader` (calls `search`/`read`/`follow_link`); each subagent builds its OWN read-only `GraphReader` on its own DB connection.
- `Analytics`, `GraphReader`, `GraphBuilder` → only `core` + `models` + ports.
- Nothing imports `engine`.

## Classes

### `GraphBuilder` — builder.py  (write primitives)

Deps on `self`: `db, embedder, llm, settings, _vec_ready`.

| method | verdict |
|---|---|
| `ingest(node) -> edges` | KEEP. inline the `node_is_complete` skip-guard at top |
| `fill_derived_fields(node)` | KEEP (reused by reviser). inline `summarize` (one llm.complete) |
| `extract_keywords(text)` | KEEP (dedup loop, reused) |
| `extract_claims(text)` | KEEP (reused by reviser) |
| `prepare_embeddings()` | KEEP (startup). inline `_reembed_all` |
| `ensure_vec()` | KEEP (reused) |
| `store_vectors(node) -> (body_vec, summary_vec)` | KEEP (reused 3×) |
| `build_semantic_edges(node, body_vec, summary_vec, k)` | KEEP. inline `_suggest_edges`, `_invalidate_prior_edges` |
| `knn_candidates(...)` | KEEP (reused) |
| `link_entity_duplicates(node, candidates)` | KEEP. inline `_check_entity_duplicate` |
| `link_supports(node, source_ids)` | KEEP, public (was `_link_support_edges`) |
| `collapse_same_as(nodes)` | KEEP (reused). inline `same_as_group` |
| `create_exogenous_node(body, source_ids, origin)` | KEEP (public + agent persist) |
| `persist_node(node)` | KEEP (reused by reviser 3×) |

### `GraphReviser` — reviser.py  (recon / revise / cascade)

Deps on `self`: `db, settings, builder`. Holds a `GraphBuilder`.

| method | verdict |
|---|---|
| `recon(file)` | KEEP |
| `update_node(id, body)` | KEEP |
| `cascading_update(file) -> actions` | KEEP. inline `_ensure_revision_metadata`, `_best_revision_match`, `_claims_equivalent`, `_active_replacement_id`, `_mark_stale`(→`db.set_node_status(id, stale)`) |
| `source_version_for_nodes(nodes)` | KEEP, public (reused: ingest + cascade) |
| `supersede(old, new)` | KEEP (reused) |
| `replace_structural_edges(doc, edges)` | KEEP (reused) |
| `cascade_dependents(...)` | KEEP (BFS, substantial) |
| `current_support_nodes(node, replacements)` | KEEP (reused in cascade loop) |
| `regenerate_exogenous_node(old, supports)` | KEEP (substantial). inline `regenerate_exogenous_text` |

`match_score(old, new)` and `claims_equivalent(old, new)` move to `core.py` (pure).

### `GraphReader` — reader.py  (read-only)

Deps on `self`: `db, embedder, reranker, settings`. The agent + subagents hold this.

| method | verdict |
|---|---|
| `query(type, value) -> QueryResult` | KEEP. inline `_query_id/_query_keyword/_query_vector/_edges_for_nodes` into one flat dispatch |
| `search(text, limit) -> nodes` | KEEP. inline `_rrf`, `_rerank_nodes` |
| `read(node_id)` | KEEP (public + agent) |
| `follow_link(node_id, ...)` | KEEP (public + agent) |
| `expand_neighborhood(seeds, hops)` | KEEP (25-line BFS, substantial) |

Note: `ensure_vec` lives on the builder; the reader's vector queries call
`db.vector_search` directly and degrade to BM25 on failure (already the case).

### `ReasoningAgent` — agent.py

Deps on `self`: `graph_reader, settings, llm, emit`. Per-question.

**State fix (kills the threading):** today `evidence/visited/state/agent` thread
through `_run_loop → dispatch → _run_subagents → _run_one_subagent →
_dispatch_tools`. Replace with one local `Subrun` data holder per subagent
(`start_id, index, visited, read_ids, streak`), created once; the dispatch is a
closure that captures it. The lead's `evidence` is a local in `ask`, appended
when reports return — never passed into `search`. Merge `_ev` + `_emit` into a
single `self.emit(event)` taking a typed event from `models.py`.

| method | verdict |
|---|---|
| `ask(question, persist, on_event)` | KEEP (the one entry) |
| `_run_lead(question) -> AgentAnswer` | KEEP. dispatch is a local closure |
| `_run_subagent(start_id, siblings, question, index) -> report` | KEEP. builds its own read-only `GraphReader`; dispatch is a local closure |
| `_resolve_distinct_starts(ids)` | KEEP (reused) |
| `_clean_node_ref(value)` | KEEP (reused). hoist `import re` to module top |
| `_render(nodes, kind)` | MERGE `_format_candidates/_format_nodes/_format_pairs/_format_report` into one renderer. DELETE dead `_format_node_full` |

Mermaid stays three module funcs (`repair_answer_mermaid`, `validate_mermaid`,
`_repair_once`) — a real subsystem, not inlined into `ask`.

### `Analytics` — analytics.py

Deps on `self`: `db`. Read-only.

| method | verdict |
|---|---|
| `health(node?)` | KEEP. inline `_mean_neighbor_overlap` |
| `recluster(resolution)` | KEEP. inline `_community_label`. **keep `_tfidf_keywords`** (called per-community in a loop — many calls, not one) |

Cluster-naming prompt + the `_llm_cluster_namer` callback move out of `engine.py`:
the prompt to `core.py`, the callback to `Analytics` (it already only needs `llm`).

### `DomainEngine` — engine.py  (thin door)

Wires `db, embedder, reranker, llm`, builds `GraphBuilder → GraphReviser`,
`GraphReader → ReasoningAgent`, `Analytics`. Calls `builder.prepare_embeddings()`
once at startup. Exposes use-cases only: `ingest_md_output`, `query`, `ask`,
`recon`, `cascading_update`, `get`, `health`, `recluster`, `delete`,
`create_exogenous_node`. NO prompts, NO scoring, NO passthrough reimplementation
— `search/read/follow_link` for tools are reached via `engine.reader`.

## Leaves

### `core.py` — pure, imports nothing internal but `models`

- ids/hash: `short_hash, source_hash, slug, make_node_id, make_exogenous_node_id, make_edge_id`
- text: `normalize_token, normalize_text, jaccard, token_jaccard, claim_keys`.
  **`TOKEN_RE` is a module constant here, never a parameter.**
- scoring: `match_score(old, new)`, `claims_equivalent(old, new)` (moved from reviser)
- Protocols: `GraphStore, Embedder, Reranker, LlmClient` — replaces every `object` hint
- prompts: all strings (the 9 in runtime + cluster-namer + mermaid)

### `models.py` — data only, no logic

`Node, Edge, NodeType, NodeStatus`, DTOs (`EdgeSuggestion(s), Keywords,
ClaimExtraction, EntityMatch`), `QueryResult, AgentAnswer, GraphStats`,
`Settings` (+ grouped sub-configs + `from_env`), and the typed stream events
(`SearchEvent, CandidatesEvent, ReadEvent, FollowEvent, DiagramReady, ...`).

## Inline / delete hit list

Single-use privates inlined: `node_is_complete, summarize, _reembed_all,
_suggest_edges, _invalidate_prior_edges, _check_entity_duplicate, _query_id,
_query_keyword, _query_vector, _edges_for_nodes, _rrf, _rerank_nodes,
_ensure_revision_metadata, _best_revision_match, _claims_equivalent,
_active_replacement_id, _mark_stale, _mean_neighbor_overlap, _community_label,
same_as_group`.
Deleted dead: `_format_node_full`, every `# region FUTURE COMPATIBILITY` block,
`MarkdownIngest.__init__(pass)`.
Threaded vars removed: `_TOKEN_RE` → `core.TOKEN_RE`; `evidence/visited/state/
agent`-index → one `Subrun` + locals.

## Old → new map

| today | tomorrow |
|---|---|
| `runtime.GraphRuntime` (enrich/embed/edges/dedup) | `GraphBuilder` (builder.py) |
| `runtime.GraphQuery` | `GraphReader` (reader.py) |
| `runtime.GraphExogenous` | folded into `GraphBuilder` |
| `runtime.GraphAnalytics` | `Analytics` (analytics.py) |
| `runtime` PROMPTS block | `core.py` |
| `revisions.GraphRevisions` | `GraphReviser` (reviser.py) |
| `md_ingest.MarkdownIngest` | `Ingestor` helper used by `GraphBuilder` (or a band inside builder.py) |
| `agent.QueryAgent` | `ReasoningAgent` (agent.py) |
| `mermaid.py` | module funcs in `agent.py` |
| `utils.py` | `core.py` |
| `models.py` | `models.py` (+ Settings, +events) |

## Phasing (each phase keeps `pytest graph/tests/ -q` green)

1. Kill `print` narration → `logging`. (biggest readability win, lowest risk)
2. Split `runtime.py` → `builder.py` / `reader.py` / `analytics.py`; move prompts
   to `core.py`; rename `revisions.py → reviser.py`, fold exogenous into builder.
3. Protocols in `core.py` → delete `object` hints + the `getattr(llm, ...)`
   override hack (test fakes implement the Protocol instead).
4. Inline the single-use privates; remove threaded vars (`TOKEN_RE`, `Subrun`).
5. Group `Settings`; pull DTOs/events into `models.py`.
6. Make `DomainEngine` the thin door (move cluster-namer prompt/callback out).

Phases 1–2 get ~90% of the "looks human" payoff. 3–6 are the real re-layer.
