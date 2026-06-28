# graph — flow reference

Every runtime path through the graph package, as ASCII flows. Function names map
to `engine.py` (facade), `runtime.py` (`GraphRuntime`/`GraphQuery`/`GraphExogenous`/
`GraphAnalytics`), `revisions.py` (`GraphRevisions`), `md_ingest.py`
(`MarkdownIngest`), and `agent.py` (`QueryAgent`).

---

## 0. Entrypoints (CLI → DomainEngine)

```
python -m graph.cli <cmd>
   │
   ├─ init      ─▶ DomainEngine(settings)            # just open/create the DB
   ├─ add DIR   ─▶ engine.ingest_md_output(DIR)      # first ingest of a doc
   ├─ query T V ─▶ engine.query(type, value)         # one-shot lookup
   ├─ ask Q     ─▶ engine.ask(question)              # agent reasoning loop
   ├─ recon F   ─▶ engine.recon(F)                   # new / unchanged / changed?
   ├─ cascade D ─▶ engine.cascading_update(D)        # apply a revised md output
   ├─ get       ─▶ engine.get()                      # dump nodes + edges
   ├─ health N? ─▶ engine.health(node?)              # metrics
   ├─ update ID ─▶ engine.update(id, body)           # replace one node body
   └─ delete ID ─▶ engine.delete(id)                 # hard delete
```

Node types: **endogenous** = source-of-truth chunks from markdown.
**exogenous** = LLM-synthesized (agent answers, regenerated derived notes).

Node lifecycle:

```
        ingest / persist
             │
             ▼
          active ──────supersede──────▶ superseded   (new version exists)
             │  \
             │   \──lost all supports──▶ stale        (exogenous, orphaned)
             │
          delete ─────────────────────▶ (row removed + edges + vectors)
```

---

## 1. First ingest of a document — `ingest_md_output(dir)`

```
md.py output dir
   │
   ▼
MarkdownIngest.load_md_output(dir)            # see §2
   │  returns (nodes[], follows-edges[])
   ▼
version = _source_version_for_nodes(nodes)    # hash of all source bodies
   │
   ▼
for each node:                                # see §3 (ingest one node)
   node.source_version = version
   engine.ingest(node)
   │
   ▼
revisions._replace_structural_edges(doc, follows_edges)
   │   delete old "follows" edges for this doc, re-add the new ones
   ▼
database.record_source(doc, version)          # remember the doc hash
```

---

## 2. Markdown parse — `MarkdownIngest.load_md_output`

```
out_dir
   │
   ├─ manifest.json present? ──yes──▶ OLD layout: _load_old_manifest_output
   │                                    • read manifest.files[]
   │                                    • each leaf .md → _build_old_layout_node
   │                                    • group by section dir
   │                                    • _structural_edges: link adjacent pages
   │                                      within each section ("follows")
   │
   └─ no manifest ──▶ NEW layout: _load_new_planning_docs_output
                        • read _planning/metadata.json + coverage.json
                        • docs/*.md sorted by leading number
                        • each → _build_new_layout_node
                        • _linear_structural_edges: chain all pages in order
                          ("follows")

per leaf file:
   text ─▶ _split_frontmatter ─▶ (meta, body)
        body empty? ─▶ SKIP
        node_id = make_node_id(body, document_name)   # hash of body
        Node(type=endogenous, title, summary, source_ranges, cluster, body)
```

Key: `node_id` is a hash of the **body**. Same body ⇒ same id (this drives exact
revision matching in §8). Keywords/claims/entity/summary are filled later, not here.

---

## 3. Ingest one node — `engine.ingest(node)`

```
node
 │
 ▼
runtime.node_is_complete(node.id)?  ──yes──▶ return []   # SKIP (idempotent)
 │   node.id = hash(body, doc); exists + active + body-vector stored
 │   ⇒ exact same chunk, same doc, same context, already done.
 │   kills re-processing on re-add / resumes after a crash.
 │ no
 ▼
runtime.fill_derived_fields(node)                       # §4
 │   source_material_hash = hash(body) if missing
 │   summary   = LLM summarize(body)        (if empty)
 │   keywords  = LLM extract_keywords(body) (if empty)
 │   entity+claims = LLM extract_claims(body) (if empty)
 ▼
database.upsert_node(node)                              # row + FTS5 reindex
 │
 ▼
runtime.store_vectors(node)                             # §5
 │   embed body    ─▶ vec_body
 │   embed summary ─▶ vec_summary  (if summary present)
 │   returns (body_vec, summary_vec)
 ▼
runtime.build_semantic_edges(node, body_vec, summary_vec, k)   # §6
 │
 ▼
settings.entity_dedup?  ──yes──▶ runtime.knn_candidates(...)    # §7
 │                               runtime.link_entity_duplicates(node, candidates)
 ▼
returns list[Edge]
```

---

## 4. Derived-field enrichment — `fill_derived_fields`

```
node.body
   │
   ├─ source_material_hash  ← hash(body)          (identity for revision match)
   ├─ summary   ← llm.summarize(body)             (1–3 sentences)
   ├─ keywords  ← llm.extract_keywords(body)      (≤12, dedup)
   ├─ entity    ┐
   └─ claims    ┴ ← llm.extract_claims(body)      (1 entity + ≤20 atomic claims)

each is filled ONLY if empty (md_ingest may pre-fill title/summary).
fallback: entity ← keywords[0] if still empty.
```

Embedding-safe text handling lives in `embeddings.Embedder.embed_document` (NOT
graph): `<image-unit>` blocks become their description text or an "omitted"
marker, base64 data URIs are dropped, and over-long input falls back to
chunked-and-averaged embedding. The stored node body is never mutated — only the
embedded copy. Graph just calls `embedder.embed_document(text)`.

---

## 5. Vectors — `store_vectors`

```
ensure_vec()                       # create vec_body/vec_summary at embedder.dim (once)
   │                               # dim mismatch vs existing DB ⇒ hard error
   ▼
body_vec    = embedder.embed_document(body)     ─▶ set_vector(id, vec_body)
summary_vec = embedder.embed_document(summary)  ─▶ set_vector(id, vec_summary)
#   embed_document = image-strip + context-length fallback, all inside embeddings/
```

Note: `_query_vector` (§13) embeds the raw user query with `embedder.embed_query`
(no image-strip needed for a short query string).

---

## 6. Semantic edges + contradiction — `build_semantic_edges`

```
knn_candidates(node, body_vec, summary_vec, k)
   │   union of KNN over vec_body and vec_summary
   │   keep active nodes only, drop self
   │   collapse_same_as: one representative per same-as cluster (§7) — bounds
   │      edge growth so duplicates don't each spawn their own edges; cap at k
   ▼
_suggest_edges(node, candidates)
   │   LLM gets new node + candidate summaries/bodies
   │   returns EdgeSuggestion[] {target_id, label, summary}
   │   label is a verb phrase: uses / defines / example-of / contradicts / ...
   ▼
for each suggestion:
   label = suggestion.label or "related"
   stamp = now()
   │
   ├─ label == "contradicts"?  ──yes──▶ _invalidate_prior_edges(node, target, stamp)   # §6a
   │
   ├─ build forward  edge  node ─label▶ target   { valid_at=stamp, source_episode_ids=[node,target] }
   ├─ build backward edge  target ─label▶ node   { valid_at=stamp, source_episode_ids=[node,target] }
   └─ upsert both (bidirectional)
```

### 6a. Contradiction invalidation — `_invalidate_prior_edges(src, tgt, stamp)`

This is the Graphiti-style temporal step. A new `contradicts` edge marks the
older fact between the same pair as no-longer-valid (never deleted).

```
for edge in get_edges_for_node(tgt):
   endpoints == {src, tgt}?            ──no──▶ skip
   edge.label == "contradicts"?       ──yes─▶ skip  (don't invalidate contradictions)
   edge.invalid_at already set?       ──yes─▶ skip  (already invalid)
   else:
       edge.invalid_at = stamp        # stopped being true (event time)
       edge.expired_at = stamp        # system marked it (ingestion time)
       upsert_edge(edge)
```

Note: this fires when a prior edge between the pair already exists (e.g. a
`related` edge from an earlier ingest, or via cascade re-evaluation). A brand-new
pair has nothing to invalidate yet — the `contradicts` edge is just recorded with
its provenance for later.

---

## 7. Entity dedup (lite) — `link_entity_duplicates(node, candidates)`

```
candidates empty? ─▶ []
   │
   ▼
_check_entity_duplicate(node, candidates)
   │   LLM: is the new node the SAME real-world entity as exactly one candidate?
   │   conservative; never merges homonyms. returns EntityMatch{is_same, target_id}
   ▼
is_same and target_id valid?  ──no──▶ []
   │ yes
   ▼
add bidirectional "same-as" edge (node ↔ target)   { valid_at, source_episode_ids }
```

Detection only — no destructive node merge. The `same-as` edge links the
duplicates so traversal and clustering treat them as one.

**Use-time collapse** (`runtime.collapse_same_as`): storage keeps every
contextually-distinct node (identical body in a different parent doc may *mean*
something different, so it is never skipped/merged), but cost-sensitive readers
collapse a same-as cluster to one representative:
- `knn_candidates` (§6) — duplicates don't each spawn semantic edges.
- `_current_support_nodes` (§10a) — smaller exogenous regen payload.
Agent `search`/`follow_link` do **not** collapse — the agent sees every context.

---

## 8. Revision check — `recon(file)`

```
read file ─▶ current_hash = source_hash(text)
known = database.get_source(file.name)
   │
   ├─ known is None        ─▶ {status: "new",       action: md_to_nodes+ingest}
   ├─ known.hash == current ─▶ {status: "unchanged", action: skip}
   └─ else                  ─▶ {status: "changed",   action: cascading_update}
```

---

## 9. Revised document — `cascading_update(dir)`

Append-only over source nodes: old bodies are never rewritten in place; changed
chunks create a new active node and supersede the old one.

```
load_md_output(dir) ─▶ (incoming_nodes[], follows_edges[])    # §2
   │  CHEAP pass: stamp source_version + body hash only. NO LLM enrichment yet.
   ▼
active_old = active endogenous nodes for this document   (no metadata forced yet)
   │
   ├─ active_old empty?  ──yes──▶ persist all incoming as new, return "ingested-new:*"
   │
   ▼
PASS 1 — exact match by source_material_hash (no enrichment on either side)
   for each incoming:
      hash hits an unmatched old?  ──yes──▶ mark matched, action "unchanged:OLD"
                                   ──no───▶ push to `pending`
   ▼
   fill_derived_fields ONLY on `pending` (changed/new chunks)
   _ensure_revision_metadata ONLY on unmatched old (backfill claims for fuzzy)
   ⇒ an update that touches 5 of 971 chunks pays LLM for ~5, not 971.

PASS 2 — fuzzy match for pending
   for each pending node:
      best = _best_revision_match(node, unmatched old)        # §9a score
      │
      ├─ best is None OR score < 0.45  ─▶ persist as NEW, action "new:NODE"
      │
      ├─ _claims_equivalent(old, new)? ─▶ action "remapped:OLD"   (reorder, no change)
      │      (claims jaccard ≥ 0.9, or body token jaccard ≥ 0.95)
      │
      └─ else (real change):
             persist new node
             _supersede(old → new)                 # §9b
             replacements[old] = new
             action "superseded:OLD->NEW"

PASS 3 — unmatched old nodes
   for old not matched:
      _mark_stale(old)                              # status → stale
      action "stale:OLD"
   collect into stale_sources

   ▼
_cascade_dependents(replacements, stale_sources, actions)   # §10
_replace_structural_edges(doc, follows_edges)               # refresh "follows"
record_source(doc, version)
return actions[]
```

### 9a. Match score — `_revision_match_score(old, new)`

```
claim_score   = jaccard(claim_keys(old), claim_keys(new))
keyword_score = jaccard(old.keywords, new.keywords)
body_score    = token_jaccard(old.body, new.body)
entity_bonus  = +0.2 if normalized entities equal else 0

score = min(1.0, max(claim_score, keyword_score*0.8, body_score*0.65) + entity_bonus)
```

Threshold `0.45` decides match-vs-new. `_claims_equivalent` (≥0.9) decides
reorder-vs-real-change.

### 9b. Supersede — `_supersede(old, new)`

```
add edge  old ─superseded_by▶ new
add edge  new ─supersedes────▶ old
set old.status = superseded
```

---

## 10. Cascade to derived nodes — `_cascade_dependents`

When a source node is superseded or staled, exogenous nodes built from it must be
regenerated or staled. BFS over `supports` edges, bounded by
`cascade_max_hops` (default 2) and `cascade_max_nodes` (default 50).

```
frontier = changed/staled source ids @depth 0
guard: hops==0 or nodes==0 ─▶ "cascade-skipped:disabled"

while frontier:
   (changed_id, depth) = pop
   depth+1 > max_hops? ─▶ skip

   for edge in get_outgoing_edges(changed_id, "supports"):
      target = edge.target  (must be active exogenous, unvisited)
      processed >= max_nodes? ─▶ "cascade-cap-hit", STOP
      mark visited

      support_nodes = _current_support_nodes(target, replacements)    # §10a
      │
      ├─ none left ─▶ _mark_stale(target); "stale-exogenous:TARGET"
      │
      ▼
      replacement = _regenerate_exogenous_node(target, support_nodes)  # §10b
      │
      ├─ None (LLM empty) ─▶ _mark_stale(target); "stale-exogenous:TARGET"
      │
      └─ ok ─▶ replacements[target] = replacement
              "regenerated-exogenous:TARGET->NEW"
              enqueue target @depth+1   (cascade can chain upward)
```

### 10a. Resolve live supports — `_current_support_nodes`

```
for incoming "supports" edge of node:
   source_id = replacements.get(source_id, source_id)   # follow the swap
   source superseded? ─▶ hop via "superseded_by" to active replacement
   keep if active
collapse_same_as(supports)   # dedup same-entity supports → smaller regen payload
```

### 10b. Regenerate derived node — `_regenerate_exogenous_node`

```
body = llm.regenerate_exogenous_text(old, support_nodes)   # grounded ONLY in current supports
body empty? ─▶ None  (caller stales it)
   │
   ▼
new exogenous Node (id from old+version+body hash)
_persist_node(new)                       # enrich + embed + semantic edges
_link_support_edges(new, supports)       # fresh "supports" edges
_supersede(old → new)
```

---

## 11. Direct exogenous node — `create_exogenous_node(body, source_ids, origin)`

```
Node(type=exogenous, cluster="Agent Notes", id from origin/body)
   │  fill_derived_fields ─▶ upsert ─▶ store_vectors
   ▼
_link_support_edges(node, source_ids)
   for each existing source id:  source ─supports▶ node
```

This is also the persistence sink for agent answers (§12).

---

## 12. Reasoning agent — `ask(question)` / `QueryAgent`

LLM-Wiki "retrieval as reasoning": the LLM navigates the graph with tools instead
of one lookup, then the answer is saved back as an exogenous node.

```
engine.ask(question, persist=True)
   │
   ▼
QueryAgent.ask
   │
   ├─ llm has run_agent override? ──yes──▶ scripted (tests/fakes)
   │
   └─ _run_loop: delegate the loop to the LLM client (llm.AgentClient):
        graph builds tools [search, read, follow_link, finish] + a dispatch(name,args)
        callback over GraphQuery, then calls:
           llm.run_tool_loop(AGENT_SYSTEM_PROMPT, question, tools, dispatch, max_steps)
        │   (loop mechanics + bind_tools live in llm/, NOT graph — see boundary note)
        │   repeat up to agent_max_steps (default 6):
        │      model picks tool calls; non-finish calls go to dispatch:
        │         search(text)        ─▶ GraphQuery.search (hybrid) ─▶ observation
        │         read(node_id)       ─▶ GraphQuery.read           ─▶ observation
        │         follow_link(node_id)─▶ GraphQuery.follow_link    ─▶ observation
        │      finish(answer, cited_node_ids) ─▶ stop
        │   patience (agent_patience, default 3): each empty search bumps a
        │      streak (any hit resets it); on streak ≥ patience the observation
        │      tells the model to stop searching and finish with what it read.
        ▼  returns neutral ToolLoopResult{finished_args, content, steps}
        graph reads answer + cited_node_ids from finished_args
        (or falls back to visited node ids if the model never called finish)
        ▼
   AgentAnswer{question, answer, cited_node_ids, steps}
   │
   ▼
persist and citations non-empty?
   │ filter cited ids to ones that still exist
   ▼
exo = create_exogenous_node(answer, valid_cited_ids, origin="agent:<q>")   # §11
answer.exogenous_node_id = exo.id
```

Effect: each answered question grows the graph (a new exogenous node) and records
provenance (`supports` edges to the sources it cited). Later source changes
cascade into that answer node via §10.

---

## 13. Query (one-shot) — `query(type, value)` / `GraphQuery`

```
type == "id"      ─▶ get_node(value) + its edges
type == "keyword" ─▶ FTS5/BM25 keyword_search ─▶ nodes + their edges
type == "vector"  ─▶ embed(value) ─▶ KNN on vec_body ─▶ seeds
                     _expand_neighborhood(seeds, hops=2) ─▶ nodes + edges
```

Tool methods used by the agent (§12) sit on the same class:

```
search(text, limit)            ─▶ HYBRID: RRF-fuse 3 ranked lists
                                    • keyword_search (FTS5/BM25)
                                    • KNN vec_body
                                    • KNN vec_summary
                                    score = Σ 1/(rrf_k + rank); active-only; top limit
                                    embed failure ⇒ degrade to BM25-only
read(node_id)                  ─▶ get_node
follow_link(node_id, label?,   ─▶ outgoing/incoming edges → active neighbor nodes
            direction, limit)     direction ∈ {incoming, outgoing, both}
```

Note: the one-shot `query("keyword", v)` path (§13 above) stays **pure BM25** —
only the agent's `search` tool is hybrid. `_rrf` is the reranker (RRF over BM25 +
both vector signals); no separate cross-encoder pass.

---

## 14. Health & clustering — `GraphAnalytics`

```
health(node?)   ─▶ counts (total/active/endo/exo), edges, isolated, avg_degree,
                   density, mean_neighbor_overlap, cluster histogram
recluster(res)  ─▶ networkx Louvain communities over active nodes+edges
                   label each community by top keyword, persist node.cluster
```

---

## 15. Edge label reference

| label | created by | meaning |
|---|---|---|
| `follows` | md_ingest structural | adjacent page in source order |
| `related`, `uses`, `defines`, `example-of`, `prerequisite-for`, … | LLM `_suggest_edges` | semantic link, bidirectional |
| `contradicts` | LLM `_suggest_edges` | conflicting fact; invalidates prior pair edge (§6a) |
| `same-as` | `link_entity_duplicates` | same real-world entity (§7) |
| `supports` | exogenous creation / cascade | source node backs a derived node |
| `superseded_by` / `supersedes` | `_supersede` | version link between old and new node |

## 16. Edge temporal fields (all backends)

```
valid_at            # when the fact became true (set at edge creation)
invalid_at          # when it stopped being true (set on contradiction)
expired_at          # when the system marked it invalid
source_episode_ids  # node ids that produced this edge (provenance)
```

Stored by `raw_sqlite` (active), `sqlmodel`, and `lancedb` (inherits sqlmodel
edge CRUD). New columns are added by `_ensure_edge_columns` migrations; old DBs
upgrade in place with empty defaults.
