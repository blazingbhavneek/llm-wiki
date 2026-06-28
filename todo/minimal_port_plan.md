# Minimal Paper-Port Plan (with theory)

Goal: take the **headline idea** from each research paper and land an easy
version of it in `graph/`, reusing seams we already have. This doc explains the
theory first, then exactly what we build and what happens at each stage.

Two papers:
- **LLM-Wiki — "Retrieval as Reasoning"** (`paper_llm_wiki_retrieval_as_reasoning.md`)
- **Zep / Graphiti — Temporal Knowledge Graph for Agent Memory** (`paper_graphiti_temporal_kg.md`)

---

# Part 1 — Theory

## 1.1 LLM-Wiki: retrieval as reasoning

**Claim of the paper.** Classic RAG is the wrong shape for multi-hop questions.
RAG = flatten documents into chunks, embed them, do ONE nearest-neighbor lookup,
stuff the hits into the prompt. That works for "what is X" but fails when the
answer needs you to find A, learn that A points to B, then check B against C.
A single lookup can't do that chain.

**Their reframe.** Treat the knowledge base as a structure the agent *navigates*,
not a bag it *dips into once*. Knowledge is:
- **compilable** — raw sources are compiled into cleaner "wiki pages" per concept,
- **composable** — pages link to each other (bidirectional links are first-class),
- **self-evolving** — the structure is corrected over time from its own failures.

**The interface is the point.** Instead of `query(text) -> chunks`, the agent
gets three tools and calls them in a loop, deciding the next move from what it
has seen so far:
- `search(query)` — find candidate pages,
- `read(page)` — pull a page's full content,
- `follow_link(page)` — jump to linked pages.

The agent keeps calling tools until it decides it has **sufficient evidence**,
then answers. This is "retrieval as reasoning": retrieval steps ARE reasoning
steps, interleaved, not a one-shot prefetch.

**Extra machinery in the full paper (we are NOT porting all of it):**
- **Error Book** — a persistent log of structural/semantic failures (dead links,
  wrong groupings, missing pages). Periodically the system reads the Error Book
  and *fixes the wiki structure*. This is the "self-evolving" part.
- **Compiled/curated pages** — sources are synthesized into per-concept pages,
  more polished than raw chunks.
- **Multi-agent refinement** — several agents share and improve the same pages.

**Reported result.** Beats HippoRAG 2, LightRAG, GraphRAG by 2.0–8.1 F1 on
multi-hop benchmarks. Their stated key insight: *the shape of the retrieval
interface matters as much as retrieval quality.*

### How this maps to us
- We **already have** `search`/`read`/`follow_link` (engine.py:117-130). What's
  missing is the **loop** that lets an LLM drive them. That loop is the headline
  feature, and it's cheap because the tools exist.
- Our **endogenous nodes** (source chunks) ≈ their raw sources; our **exogenous
  nodes** (LLM-synthesized) ≈ their compiled pages. We already have the node type
  and a builder (`create_exogenous_node`); we just don't generate them at query
  time yet — the agent loop will.
- Our **semantic edges are already bidirectional** (runtime.py:309-325) = their
  first-class bidirectional links.
- We **skip** the Error Book and multi-agent refinement (the hard, self-evolving
  parts) for this minimal cut.

## 1.2 Graphiti: temporal knowledge graph

**Problem the paper attacks.** An agent's memory graph can't just append facts
forever. Facts change ("lives in Tokyo" → later "lives in Osaka"), contradict
each other, and the same entity shows up under different names. A naive graph
ends up with stale facts presented as current, and one real thing fragmented
into many nodes.

**Bi-temporal model.** Every `EntityEdge` (a fact) carries up to four timestamps:
- `valid_at` — when the fact became true *in the world*,
- `invalid_at` — when it stopped being true *in the world*,
- `expired_at` — when the *system* marked it invalid (bookkeeping time),
- `reference_time` — timestamp of the episode that produced it.

Two timelines: **event time** (`valid_at`/`invalid_at`) vs **system/ingestion
time** (`expired_at`/`reference_time`). Facts are **never deleted, only
invalidated** — the full history stays so you can ask "what was true at time T."

**Conflict pipeline, per new episode ingested:**
1. LLM extracts candidate edges (facts) from the new content.
2. **Fast dedup** — exact text match against existing edges (cheap, no LLM).
3. **Slow dedup** — hybrid search (vector + keyword) finds existing edges between
   the same endpoints; an LLM arbitrates them, returning an `EdgeDuplicate`:
   - `duplicate_facts` — indices of existing facts that say the same thing,
   - `contradicted_facts` — indices that conflict (either direction).
   Hard rule: never call two facts duplicates if numbers, dates, or qualifiers
   differ — those are contradictions, not duplicates.
4. **Temporal invalidation** — an old edge gets `invalid_at` set when
   `old.invalid_at <= new.valid_at` (the new fact supersedes it in time).
5. **Race protection** — a Redis cache of recently resolved edges so parallel
   ingestion doesn't double-resolve.

**Entity dedup (nodes).** Each newly extracted entity is LLM-checked against
candidate existing entities. It is *context-aware* to avoid false merges
("Java" the island vs Java the language). On a match, summaries are merged into
one canonical node. Batched for throughput.

**Provenance.** Every edge keeps the list of **episode IDs** that produced it, so
any fact traces back to its raw source.

**Paper's own listed weaknesses (where WE are actually ahead):**
- No propagation — it invalidates the one contradicted edge but does NOT walk
  downstream to fix knowledge derived from it.
- No hierarchy-aware ingestion (flat episodes, not structured chunks).
- No source-vs-derived node distinction.
- No graph-level cascade when an upstream fact changes.

### How this maps to us
- **Bi-temporal edges** → add `valid_at` / `invalid_at` / `expired_at` /
  `source_episode_ids` to our `Edge`. Today our edges have none.
- **Contradiction invalidation** → our edge-building LLM **already emits a
  `"contradicts"` label** (EDGE_PROMPT, runtime.py:54-64) but nothing acts on it.
  Minimal port: when a new edge says `contradicts`, set `invalid_at`/`expired_at`
  on the older edge between the same pair. No new LLM call — we reuse the label.
- **Provenance** → store the node ids that produced an edge in
  `source_episode_ids` (our "episodes" are source chunks).
- **Entity dedup** → minimal version: detect a same-real-world-entity neighbor at
  ingest and link with a `same-as` edge. We do **detection only, no destructive
  merge** (full merge is risky and not minimal).
- We **skip** the full extract→fast-dedup→slow-dedup→batch-arbitration pipeline
  and the Redis race cache (single-writer SQLite, our scale doesn't need it).
- We **keep our advantages** the paper lacks: cascade propagation
  (revisions.py), hierarchy-aware ingest (md_ingest), endogenous/exogenous split.

## 1.3 One-screen summary of what each paper gives us

| Paper idea | Full-paper version | Our minimal port | Why it's cheap |
|---|---|---|---|
| Retrieval as reasoning | tool loop + compiled pages + Error Book + multi-agent | agent loop over existing `search/read/follow_link`, answer saved as exogenous node | tools already exist; exogenous builder already exists |
| Bi-temporal edges | 4 timestamps, "what was true at T" | `valid_at`/`invalid_at`/`expired_at` + provenance on `Edge` | additive columns, copy node-migration pattern |
| Contradiction handling | extract→dedup→LLM arbitrate→invalidate | act on the `contradicts` label the edge LLM already emits | no extra LLM call |
| Entity resolution | LLM dedup + merge into canonical node | detect + add `same-as` edge (no merge) | reuses KNN candidates already computed |
| Self-evolving structure | Error Book feedback loop | **out of scope** | hard, not minimal |

---

# Part 2 — Where we are today

```
                        ┌──────────────────────────────┐
   input.md ──md.py──▶  │  output/<doc>/ (chunks)       │
                        └───────────────┬──────────────┘
                                        │
                            DomainEngine.ingest
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
  fill metadata               embed body+summary               build edges
  (summary, keywords,         ──▶ sqlite-vec                   KNN ─▶ LLM judge
   claims, entity)                                             ─▶ edges (both ways)
        └───────────────────────────────┴───────────────────────────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │  SQLite graph      │
                              │  nodes + edges     │
                              │  + FTS5 + vectors  │
                              └─────────┬─────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
              query keyword       query vector         query id
              (one FTS lookup)    (one KNN + 2 hops)   (one fetch)
                    └───────────────────┴───────────────────┘
                                        │
                                        ▼
                              flat result set (done)

  Tool methods already exist but nothing drives them in a loop:
     search(text)   read(node_id)   follow_link(node_id)

  Edge today:  id, source, target, label, summary, created_at
     (label CAN be "contradicts" but nobody acts on it — no time fields,
      no record of which nodes produced the edge)
```

Gaps, restated against the theory:
1. **No reasoning loop** (LLM-Wiki) — query is one-shot; can't chain hops itself.
2. **No time on edges** (Graphiti) — a contradicting fact is just appended next
   to the old one; both look equally current.
3. **No entity resolution** (Graphiti) — the same real thing in two chunks stays
   two unlinked nodes.

---

# Part 3 — What we want

```
                            DomainEngine.ingest
                                   │
     ┌─────────────────────────────┼──────────────────────────────┐
     ▼                             ▼                              ▼
  fill metadata            embed ─▶ sqlite-vec            build edges
                                                          KNN ─▶ LLM judge
                                                              │
                                   ┌──────────────────────────┼─────────────────┐
                                   ▼                          ▼                 ▼
                          [NEW] stamp edge          [NEW] if label =      [NEW] entity
                          valid_at + which          "contradicts":        dedup check on
                          nodes made it             set invalid_at +      KNN neighbors:
                          (source_episode_ids)      expired_at on the     same real thing?
                                                    older edge            ─▶ add "same-as"
                                   └──────────────────────────┴─────────────────┘
                                                  │
                                                  ▼
                                        SQLite graph (time-aware edges)

  ── NEW query path: the agent loop (LLM-Wiki) ─────────────────────────

   engine.ask("how do I pick a GPU device?")
        │
        ▼
   ┌─────────────────────────── QueryAgent ───────────────────────────┐
   │  hand the LLM 4 tools via native tool-calling (bind_tools):        │
   │     search   read   follow_link   finish                          │
   │                                                                   │
   │   LLM ──calls──▶ search("GPU device")     ──▶ observation back    │
   │   LLM ──reasons, calls──▶ read(node:...)  ──▶ observation back    │
   │   LLM ──reasons, calls──▶ follow_link(...) ─▶ observation back    │
   │   ... loop until "sufficient evidence", max = agent_max_steps ... │
   │   LLM ──calls──▶ finish(answer, cited_node_ids)                   │
   └───────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
                    [REUSE] create_exogenous_node(answer, cited_ids)
                    saves the answer as an exogenous node + "supports"
                    edges back to every source it cited
                    (= compiled page + provenance + query-time growth)
                                   │
                                   ▼
                      AgentAnswer { question, answer, cited_node_ids,
                                    exogenous_node_id, steps }
```

Theory tie-back:
- The loop = LLM-Wiki "retrieval as reasoning."
- Saving the answer as an exogenous node with `supports` edges = their "compiled
  page" + Graphiti-style provenance, and it makes the graph **self-grow** at
  query time (the cheap slice of "self-evolving").
- Time fields + contradiction handling = Graphiti's bi-temporal model and
  invalidation, in the minimal form.

---

# Part 4 — Stage-by-stage: what happens, when

## Stage A — ingest time (every node added)

| Step | Today | After | Paper basis |
|---|---|---|---|
| build edges | KNN ─▶ LLM ─▶ edge | same | — |
| edge fields | label/summary only | **+ valid_at** (event time), **+ source_episode_ids** (producing node ids) | Graphiti bi-temporal + provenance |
| contradiction | `contradicts` label ignored | **older edge between same pair gets invalid_at + expired_at = now** | Graphiti temporal invalidation |
| duplicate entity | two unlinked nodes | **LLM "same real thing?" check over KNN neighbors ─▶ add `same-as` edge** (detect only, no merge) | Graphiti entity dedup (lite) |

Contradiction detail: in `build_semantic_edges`, when the LLM-proposed label is
`"contradicts"`, look up existing active edges between the same node pair
(via `get_edges_for_node` filtered to the other endpoint — no new DB method),
stamp `invalid_at`/`expired_at = now_iso()` on them, re-`upsert_edge`. Set
`valid_at = now_iso()` on the new edge. Zero extra LLM calls.

## Stage B — query time (new `ask`)

| Step | What happens | Paper basis |
|---|---|---|
| 1 | `engine.ask(question)` starts `QueryAgent` | LLM-Wiki interface |
| 2 | LLM gets 4 tools, loops: search → read → follow_link as it decides | retrieval as reasoning |
| 3 | each tool call hits the **existing** `GraphQuery.search/read/follow_link` | reuse |
| 4 | LLM calls `finish(answer, cited_node_ids)` when evidence is sufficient | their stopping criterion |
| 5 | answer saved via **existing** `create_exogenous_node` ─▶ `supports` edges | compiled page + provenance |
| 6 | returns `AgentAnswer` (answer, citations, exo node id, step count) | — |

Step budget: `settings.agent_max_steps` (default 6) bounds the loop so a confused
model can't spin forever — our pragmatic stand-in for "sufficient evidence."

## Stage C — storage migration (automatic, safe)

- New edge columns added with `ALTER TABLE` exactly like node columns are added
  today (`_ensure_edge_columns`, a copy of `_ensure_node_columns`,
  raw_sqlite.py:101).
- Old databases keep working: new columns default to NULL / `'[]'`.
- Only the active `raw_sqlite` backend is touched; sqlmodel/lancedb read the new
  fields as empty (model defaults), so nothing breaks.

---

# Part 5 — Files touched (small)

```
graph/agent.py        NEW   QueryAgent loop + 4 tool definitions
graph/models.py       edit  Edge time fields, AgentAnswer, EntityMatch, Settings flags
graph/runtime.py      edit  edge provenance + contradiction + entity dedup, 2 prompts
graph/engine.py       edit  ask(), wire QueryAgent, call dedup in ingest()
graph/cli.py          edit  "ask" subcommand
llm/llm.py + base.py  edit  run_tools() wrapper around bind_tools
db/raw_sqlite.py      edit  _ensure_edge_columns + read/write new edge cols
graph/tests/*         edit  fakes + 3 new tests
```

New/changed models (`models.py`):
```python
# Edge gains:
valid_at: str | None = None
invalid_at: str | None = None
expired_at: str | None = None
source_episode_ids: list[str] = Field(default_factory=list)

class AgentAnswer(BaseModel):
    question: str
    answer: str
    cited_node_ids: list[str] = Field(default_factory=list)
    exogenous_node_id: str | None = None
    steps: int = 0

class EntityMatch(BaseModel):
    is_same: bool = False
    target_node_id: str | None = None

# Settings gains: agent_max_steps: int = 6 ; entity_dedup: bool = True
```

---

# Part 6 — How we verify

- `python -m pytest graph/tests/ -q` (offline; fake LLM + fake embedder injected):
  - `test_agent_ask_persists_exogenous` — `ask(q)` returns an answer + cited ids;
    an exogenous node is created with `supports` edges to the cited sources.
  - `test_contradiction_invalidates_prior_edge` — a second, contradicting edge
    sets `invalid_at`/`expired_at` on the older edge; `source_episode_ids` filled.
  - `test_entity_dedup_links_same_as` — a duplicate entity yields a `same-as` edge.
- Fakes get: `FakeLlm.run_agent` (scripted search→read→finish with a citation),
  `check_entity_duplicate`, and a `suggest_edges` branch that emits `contradicts`
  for an arranged pair.
- Live (needs the chat + embed endpoints up):
  `python -m graph.cli ask "how do I select a GPU device?"` then
  `python -m graph.cli get` to see the new answer node and its `supports` edges.

---

# Part 7 — Explicitly out of scope (kept minimal)

| Skipped | From | Why |
|---|---|---|
| Error Book / self-healing structure | LLM-Wiki | hardest part; needs a failure log + periodic restructuring pass |
| Compiled curated pages (offline) | LLM-Wiki | we get a lightweight version free via query-time exogenous nodes |
| Full conflict pipeline (fast+slow dedup, batch arbitration) | Graphiti | high LLM volume; only pays off at many overlapping docs |
| Destructive node merge | Graphiti | risky; `same-as` edge gives most of the benefit safely |
| Redis race cache | Graphiti | single-writer SQLite, our scale doesn't need it |
| Temporal columns on sqlmodel/lancedb backends | Graphiti | only raw_sqlite is active |
