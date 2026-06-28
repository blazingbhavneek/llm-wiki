# Our Implementation: llm-wiki graph/

## What It Is
Knowledge graph built from markdown documents. Source docs → chunked nodes → LLM-enriched metadata → SQLite storage with vector + keyword search.

## Node Types
- **Endogenous**: chunks from source `.md` files (ground truth, append-only)
- **Exogenous**: agent/LLM-synthesized nodes derived from existing graph content (query cache)

## Node Lifecycle
`active` → `superseded` (new version of same chunk) | `stale` (lost all supports) | `deleted`

## Node Fields
```python
id, body, type, title, original_document_name
source_path, source_ranges, source_version, source_material_hash
entity, claims[], keywords[], summary, cluster
status, created_at, updated_at
```
No temporal validity fields. No episode provenance on edges.

## Edge Fields
```python
id, source_node_id, target_node_id, label, summary, created_at
```
Static — no `valid_at`, `invalid_at`, `expired_at`.

## Ingest Pipeline
1. `md.py` → hierarchical chunks → structural `follows` edges
2. Per node: LLM extracts `summary`, `keywords`, `claims`, `entity`
3. Body + summary embedded → stored in sqlite-vec (`vec_body`, `vec_summary`)
4. `build_semantic_edges`: KNN candidates → LLM judges which deserve edges → written bidirectionally

## Edge Building
- KNN from `vec_body` + `vec_summary` union → candidate set
- LLM prompt: given new node + candidates, propose `EdgeSuggestions` with `label` + `summary`
- Labels include "contradicts" as an option but no dedup/conflict check against existing edges
- No entity resolution — same concept in two chunks = two nodes, linked by semantic edges only

## Query Interface
Single call → result set (lookup-shaped, not reasoning-shaped):
- `keyword` → FTS5/BM25 search → nodes + their edges
- `vector` → KNN on `vec_body` → 2-hop neighborhood expansion
- `id` → direct node fetch + edges

## Cascade / Versioning
When source doc changes:
1. New source chunks matched against active nodes via exact body hash, then claim similarity
2. Identical chunk → left alone; reordered → remapped
3. Changed chunk → new `active` node + old marked `superseded`, linked by `supersedes`/`superseded_by` edges
4. Walk downstream `supports` edges → regenerate exogenous nodes from current active supports
5. Exogenous node loses all supports → marked `stale`
6. Bounded by `WIKI_CASCADE_MAX_HOPS` (default 2) and `WIKI_CASCADE_MAX_NODES` (default 50)

## Storage
- SQLite: nodes, edges tables
- FTS5: `nodes_fts` for keyword search
- sqlite-vec: `vec_body`, `vec_summary` for vector search
- No Redis, no external graph DB

## What's Missing (noted in README)
- `agent.py` / `master_agent.py` not wired into query (iterative tool-call retrieval)
- Stronger claim matching for heavy rewrites
- Query-time exogenous-node growth feeding back into graph
