# Graph Organization Plan

## Intent

- Split the current mess into a few readable files.
- Keep the package flat.
- Keep each implementation file under `800` lines.
- Add light compatibility seams for future TODO work.
- Do **not** pre-implement future TODO APIs or future files now.

## Region Rule

Every implementation file should use:

```python
# region NAME
...
# endregion NAME
```

## Core Package

```text
graph/
  __init__.py
  engine.py
  runtime.py
  revisions.py
  md_ingest.py
  models.py
  cli.py
  utils.py
```

## Optional Later Files

Do not create these now.

```text
graph/
  agent.py
  master_agent.py
```

They become real only when the TODO for agent-driven retrieval actually starts.

## `__init__.py`

```text
__init__.py
├─ DomainEngine
├─ Settings
├─ Node
├─ Edge
├─ NodeType
├─ NodeStatus
├─ ClaimExtraction
├─ QueryResult
└─ GraphStats
```

Exports only.

## `engine.py`

```text
engine.py
└─ class DomainEngine
   ├─ data
   │  ├─ settings
   │  ├─ database
   │  ├─ embedder
   │  ├─ llm
   │  ├─ ingest: MarkdownIngest
   │  ├─ runtime: GraphRuntime
   │  ├─ query: GraphQuery
   │  ├─ exogenous: GraphExogenous
   │  ├─ analytics: GraphAnalytics
   │  └─ revisions: GraphRevisions
   ├─ # region LIFECYCLE
   │  ├─ __init__(settings=None, embedder=None, llm_client=None)
   │  └─ close()
   ├─ # region INGEST API
   │  ├─ md_to_nodes(md_output_dir)
   │  ├─ ingest(node)
   │  └─ ingest_md_output(md_output_dir)
   ├─ # region QUERY API
   │  └─ query(query_type, value)
   ├─ # region TOOL COMPATIBILITY API
   │  ├─ search(text, limit=None)
   │  ├─ read(node_id)
   │  └─ follow_link(node_id, label=None, direction="both", limit=None)
   ├─ # region GRAPH API
   │  ├─ get()
   │  ├─ health(node_id=None)
   │  └─ recluster(resolution=1.0)
   ├─ # region SOURCE UPDATE API
   │  ├─ recon(source_file)
   │  ├─ update(node_id, body)
   │  ├─ delete(node_id)
   │  └─ cascading_update(source_file)
   ├─ # region EXOGENOUS API
   │  └─ create_exogenous_node(body, source_node_ids, origin=None)
   └─ # region FUTURE COMPATIBILITY
      └─ reserved comments only:
         - agent-driven query will plug in here later
         - maintain/stale-refresh can be exposed here later
```

### Notes

- `engine.py` is only the facade.
- No prompt text.
- No long private algorithms.
- Future TODO compatibility means the facade already owns `search/read/follow_link`, but nothing more.

## `runtime.py`

```text
runtime.py
├─ # region PROMPTS
│  ├─ GRAPH_SYSTEM_PROMPT
│  ├─ SUMMARY_PROMPT
│  ├─ KEYWORD_PROMPT
│  ├─ CLAIM_PROMPT
│  ├─ REGENERATE_EXOGENOUS_PROMPT
│  └─ EDGE_PROMPT
├─ class GraphRuntime
│  ├─ # region LIFECYCLE
│  │  └─ __init__(database, embedder, llm, settings)
│  ├─ # region ENRICHMENT
│  │  ├─ fill_derived_fields(node)
│  │  ├─ summarize(text)
│  │  ├─ extract_keywords(text)
│  │  └─ extract_claims(text)
│  ├─ # region EMBEDDINGS
│  │  ├─ ensure_vec()
│  │  ├─ store_vectors(node)
│  │  ├─ _text_for_embedding(text)
│  │  ├─ _embed_with_context_fallback(text)
│  │  ├─ _is_context_length_error(exc)
│  │  ├─ _split_lines_into_chunks(lines, chunk_count)
│  │  └─ _mean_vectors(vectors)
│  ├─ # region SEMANTIC EDGES
│  │  ├─ knn_candidates(node_id, body_vec, summary_vec, k)
│  │  ├─ build_semantic_edges(node, body_vec, summary_vec, k)
│  │  ├─ _suggest_edges(node, candidates)
│  │  ├─ _run_text_query(system_prompt, user_content)
│  │  └─ _run_structured_query(system_prompt, user_content, output_model)
│  ├─ # region EXOGENOUS REGENERATION
│  │  └─ regenerate_exogenous_text(previous, support_nodes)
│  └─ # region FUTURE COMPATIBILITY
│     └─ reserved comments only:
│        - entity dedup logic goes here later
│        - contradiction helpers go here only if needed
├─ class GraphQuery
│  ├─ # region LIFECYCLE
│  │  └─ __init__(database, embedder, settings, runtime)
│  ├─ # region PUBLIC API
│  │  ├─ query(query_type, value)
│  │  ├─ search(text, limit=None)
│  │  ├─ read(node_id)
│  │  └─ follow_link(node_id, label=None, direction="both", limit=None)
│  ├─ # region QUERY MODES
│  │  ├─ _query_id(value)
│  │  ├─ _query_keyword(value)
│  │  └─ _query_vector(value)
│  ├─ # region TRAVERSAL
│  │  ├─ _expand_neighborhood(seeds, hops=2)
│  │  └─ _edges_for_nodes(nodes)
│  └─ # region FUTURE COMPATIBILITY
│     └─ reserved comments only:
│        - context_markdown helper can be added here later
│        - agent-facing scoring/traversal tweaks stay here later
├─ class GraphExogenous
│  ├─ # region LIFECYCLE
│  │  └─ __init__(database, runtime, settings)
│  ├─ # region PUBLIC API
│  │  └─ create_exogenous_node(body, source_node_ids, origin=None)
│  ├─ # region SUPPORTS GRAPH
│  │  └─ _link_support_edges(node, source_node_ids)
│  └─ # region FUTURE COMPATIBILITY
│     └─ reserved comments only:
│        - query cache / synthetic reuse goes here later
│        - query-time exogenous growth goes here later
└─ class GraphAnalytics
   ├─ # region LIFECYCLE
   │  └─ __init__(database)
   ├─ # region HEALTH
   │  ├─ health(node_id=None)
   │  └─ _mean_neighbor_overlap(neighbors)
   ├─ # region CLUSTERING
   │  ├─ recluster(resolution=1.0, seed=42, persist=True)
   │  └─ _community_label(members, node_by_id, index, used)
   └─ # region FUTURE COMPATIBILITY
      └─ reserved comments only:
         - maintain/lint logic can be added here later or split later
```

### Notes

- `runtime.py` absorbs current logic from `engine.py` and `edges.py`.
- `GraphQuery.search/read/follow_link` are the only real compatibility seam needed now for future tool-call retrieval.
- No `GraphMaintenance` class yet.

## `revisions.py`

```text
revisions.py
├─ # region CONSTANTS
│  ├─ _CASCADE_MATCH_THRESHOLD
│  └─ _UNCHANGED_CLAIM_THRESHOLD
└─ class GraphRevisions
   ├─ # region LIFECYCLE
   │  └─ __init__(database, settings, runtime, query, exogenous, ingest)
   ├─ # region PUBLIC API
   │  ├─ recon(source_file)
   │  ├─ update_node(node_id, body)
   │  └─ cascading_update(source_file)
   ├─ # region VERSIONING
   │  ├─ _source_version_for_nodes(nodes)
   │  └─ _ensure_revision_metadata(node)
   ├─ # region MATCHING
   │  ├─ _best_revision_match(node, candidates)
   │  ├─ _claims_equivalent(old, new)
   │  └─ _revision_match_score(old, new)
   ├─ # region MUTATION
   │  ├─ _supersede(old, new)
   │  ├─ _replace_structural_edges(document_name, edges)
   │  └─ _mark_stale(node_id)
   ├─ # region CASCADE
   │  ├─ _cascade_dependents(replacements, stale_sources, actions)
   │  ├─ _current_support_nodes(node, replacements)
   │  ├─ _active_replacement_id(node_id)
   │  └─ _regenerate_exogenous_node(old, support_nodes)
   └─ # region FUTURE COMPATIBILITY
      └─ reserved comments only:
         - stronger rewrite matching goes here later
         - temporal/conflict edge logic goes here later
```

### Notes

- All remap/supersede/stale/cascade logic lives here.
- Do not add future temporal fields or conflict logic now.
- Just keep this as the place where that work will land later.

## `md_ingest.py`

```text
md_ingest.py
└─ class MarkdownIngest
   ├─ # region LIFECYCLE
   │  └─ __init__()
   ├─ # region PUBLIC API
   │  └─ load_md_output(out_dir)
   ├─ # region LAYOUT DISPATCH
   │  ├─ _load_old_manifest_output(out_path)
   │  └─ _load_new_planning_docs_output(out_path)
   ├─ # region OLD LAYOUT HELPERS
   │  └─ _build_old_layout_node(...)
   ├─ # region NEW LAYOUT HELPERS
   │  └─ _build_new_layout_node(...)
   ├─ # region MARKDOWN PARSING
   │  ├─ _split_frontmatter(text)
   │  ├─ _parse_ranges(value)
   │  ├─ _title_from_markdown(body)
   │  └─ _humanize(dirname)
   ├─ # region PLANNING DOC HELPERS
   │  ├─ _read_json(path, default)
   │  ├─ _canonical_doc_name(filename)
   │  └─ _doc_sort_key(path)
   ├─ # region STRUCTURAL EDGES
   │  ├─ _structural_edges(sections)
   │  └─ _linear_structural_edges(node_ids)
   └─ # region LOGGING
      └─ _log(message)
```

### Notes

- Keep this as one file.
- Future TODO work does not require another split here.

## `models.py`

```text
models.py
├─ # region TIMESTAMPS
│  └─ now_iso()
├─ # region SETTINGS
│  └─ class Settings
├─ # region ENUMS
│  ├─ class NodeType
│  └─ class NodeStatus
├─ # region CORE GRAPH MODELS
│  ├─ class Node
│  └─ class Edge
├─ # region LLM EXCHANGE MODELS
│  ├─ class EdgeSuggestion
│  ├─ class EdgeSuggestions
│  ├─ class Keywords
│  └─ class ClaimExtraction
├─ # region QUERY AND METRICS
│  ├─ class QueryResult
│  └─ class GraphStats
└─ # region FUTURE COMPATIBILITY
   └─ reserved comments only:
      - add tool-result models here later only if needed
      - add temporal edge fields here later only if needed
      - add query-cache model here later only if needed
```

### Notes

- Keep the current model file mostly as-is.
- Do not add speculative fields now just for future ideas.

## `cli.py`

```text
cli.py
├─ # region OUTPUT
│  └─ _print(value)
├─ # region ENGINE BOOTSTRAP
│  └─ _engine(args)
├─ # region COMMANDS
│  ├─ cmd_init(args)
│  ├─ cmd_add(args)
│  ├─ cmd_query(args)
│  ├─ cmd_recon(args)
│  ├─ cmd_cascade(args)
│  ├─ cmd_get(args)
│  ├─ cmd_health(args)
│  ├─ cmd_delete(args)
│  └─ cmd_update(args)
└─ # region PARSER
   ├─ build_parser()
   └─ main(argv=None)
```

### Notes

- Keep the current CLI small.
- Do not add `search/read/follow_link/maintain` commands now.
- If those are needed later, add them in this file first before splitting the CLI.

## `utils.py`

```text
utils.py
├─ # region HASHING
│  ├─ short_hash(text, length=12)
│  └─ source_hash(text)
├─ # region IDENTIFIERS
│  ├─ slug(text, max_length=40)
│  ├─ make_node_id(body, document_name=None)
│  ├─ make_exogenous_node_id(seed)
│  └─ make_edge_id(source_id, target_id, label)
└─ # region TEXT MATCHING
   ├─ normalize_token(token)
   ├─ normalize_text(text)
   ├─ jaccard(left, right)
   ├─ token_jaccard(left, right, token_re)
   └─ claim_keys(node, token_re)
```

### Notes

- Only tiny shared helpers live here.
- Do not turn this into a second runtime file.

## Method Placement Rules

- Embeddings, enrichment, semantic edges: `GraphRuntime`
- `search/read/follow_link/query`: `GraphQuery`
- exogenous node creation: `GraphExogenous`
- health and reclustering: `GraphAnalytics`
- remap/supersede/stale/cascade: `GraphRevisions`
- `md.py` output parsing: `MarkdownIngest`
- public wiring only: `DomainEngine`
- tiny helpers only: `utils.py`

## Execution Order

1. Create `runtime.py`.
2. Move `edges.py` into `runtime.py`.
3. Create `revisions.py`.
4. Convert `md_ingest.py` into `MarkdownIngest`.
5. Reduce `engine.py` to a facade.
6. Add `# region ... # endregion ...` everywhere.

## Future Compatibility Summary

The refactor should only make these future moves easier:

- agent can call `search/read/follow_link`
- query-time exogenous growth has a natural home in `GraphExogenous`
- stronger rewrite matching has a natural home in `GraphRevisions`
- temporal/conflict edge logic has a natural home in `GraphRevisions`

Nothing else should be prebuilt now.
