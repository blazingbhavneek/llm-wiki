# Project guide

Use this as the compact context file for maintenance or a chat UI. The source of
truth for design decisions is [handoff.md](handoff.md); this file is the map of
what to edit.

## Architecture

```text
md.py
  Raw Markdown → lossless H1/H2/page trees in output/

graph/
  Existing output/ trees → SQLite graph + FTS5 → query results
  Query results → synthetic Markdown cache nodes in .wiki/synthetic/
```

`md.py` and `graph/` have separate responsibilities. Do not add global graph,
search, or synthetic-node behavior to `md.py`.

## Maintained file map

| File | What it contains / when to edit it |
|---|---|
| [md.py](md.py) | Source compiler. Chunks Markdown, plans H1/H2/leaf ranges with an LLM, enforces exact source-line coverage, renders `output/<source>/`, then verifies/repairs. Edit for source splitting, source-tree format, models, or compiler prompts. |
| [handoff.md](handoff.md) | Design contract: source coverage, document subgraphs, absolute/synthetic nodes, evidence, invalidation, policy, and acceptance criteria. Update when the intended architecture changes. |
| [usage.md](usage.md) | Human command reference. Update when CLI behavior changes. |
| [README.md](README.md) | Minimal repository landing page. |
| [.gitignore](.gitignore) | Ignores generated output, Python caches, and `.wiki/` runtime state. |
| [graph/__init__.py](graph/__init__.py) | Package description only. |
| [graph/models.py](graph/models.py) | Data contracts: `Node`, `Edge`, `Evidence`, and compiled-document/page objects. Edit for schema-level graph behavior. |
| [graph/ids.py](graph/ids.py) | Stable deterministic IDs for sources, versions, pages, canonical absolute nodes, synthetic nodes, and edges. Edit only when identity semantics change. |
| [graph/store.py](graph/store.py) | SQLite schema, transactions, node/edge persistence, source versions, FTS5, query cache, evidence merging. Edit for database behavior. |
| [graph/source_tree.py](graph/source_tree.py) | Only adapter that reads `md.py` output. Validates coverage, parses leaf frontmatter, and produces `CompiledDocument`. Edit when the compiler output format changes. |
| [graph/compiler.py](graph/compiler.py) | Raw `.md` import path. Calls unchanged `md.py` into staging, validates/promotes output, then activates graph ingest. Edit for raw-import/staging behavior. |
| [graph/ingest.py](graph/ingest.py) | Bootstrap and incremental ingest. Creates document/page subgraphs, topic links, optional LLM-extracted absolute nodes/edges, caps external edges, and retires old source versions. |
| [graph/llm.py](graph/llm.py) | Optional OpenAI-compatible LLM client and JSON extraction helper. Edit for provider/model behavior. |
| [graph/policy.py](graph/policy.py) | Default graph limits and small YAML policy parser. Edit default fan-out, hop, strength, and synthetic thresholds here. |
| [graph/search.py](graph/search.py) | Search backend interface and FTS5 implementation. Elasticsearch/vector adapters belong here later. |
| [graph/query.py](graph/query.py) | Shared retrieval service: title/FTS seeds, bounded graph traversal, scoring, and source citations. Edit query quality and context assembly here. |
| [graph/synthetic.py](graph/synthetic.py) | Repeated-query cache, synthetic Markdown creation/reuse, flattened absolute dependencies, evidence-backed support edges, and staleness metadata. |
| [graph/maintenance.py](graph/maintenance.py) | Reindexing, stale synthetic refresh, health metrics, and lints. |
| [graph/cli.py](graph/cli.py) | CLI wiring for `bootstrap`, `ingest`, `import`, `query`, and `maintain`. |
| [graph/README.md](graph/README.md) | Graph package overview and commands. |
| [graph/tests/test_pipeline.py](graph/tests/test_pipeline.py) | Deterministic end-to-end regression suite: coverage, document subgraphs, query fan-out, synthetic reuse/staleness, and maintenance. Extend this for every bug fix. |
| [graph/tests/__init__.py](graph/tests/__init__.py) | Test package marker. |

## Code symbol map

Use these names to identify the owning unit from a traceback. Public entry
points and the private helpers most likely to occur in a stack trace are listed
here; inspect the file itself for smaller local helpers.

| File | Key classes / functions |
|---|---|
| [md.py](md.py) | Models: `FileRef`, `NewFileRef`, `GenerationDecision`, `VerificationResult`, `RepairResult`, `ChunkSummary`, `TopicRange`, `H1Plan`, `H1Layout`, `LeafPagePlan`, `CurrentFileState`. Main entry points: `main`, `async_main`, `process_one_source`, `phase_generate`, `phase_verify`, `phase_repair`. Core guarantees: `chunk_source_lines_preserving_tables`, `partition_or_fallback`, `assert_exact_coverage`, `render_hierarchical_wiki`. |
| [graph/models.py](graph/models.py) | `Evidence`, `Node`, `Edge`, `CompiledSourcePage`, `CompiledDocument`; serialization helpers `dumps`, `loads`. |
| [graph/ids.py](graph/ids.py) | ID builders: `source_id`, `version_id`, `doc_node_id`, `page_node_id`, `topic_node_id`, `concept_node_id`, `absolute_node_id`, `synthetic_node_id`, `edge_id`; helpers `slug`, `short_hash`. |
| [graph/store.py](graph/store.py) | `Store`: `transaction`, source/version methods (`upsert_source`, `add_source_version`, `activate_version`), graph methods (`upsert_node`, `upsert_edge`, `get_node`, `get_edge`, `edges_from`), FTS methods (`fts_index`, `fts_search`), cache methods (`get_cache`, `upsert_cache`, `bump_cache_use`). Helpers `_row_to_node`, `_row_to_edge`, `_merge_evidence`. |
| [graph/source_tree.py](graph/source_tree.py) | `CoverageError`; `validate_coverage`, `read_compiled_document`, `discover_compiled_documents`, `sha256_file`; parsing helpers `_parse_frontmatter`, `_topics_for_range`. |
| [graph/compiler.py](graph/compiler.py) | `compile_and_ingest`; staging helpers `_source_hash`, `_compiler_args`. |
| [graph/ingest.py](graph/ingest.py) | `Ingestor`: `bootstrap`, `ingest_document`, `_build_document_node`, `_build_page_node`, `_link_topic`, `_extract_absolute_facts`, `_add_edge`, `_retire_previous_version`, `_prune_unsupported_canonical_nodes`; module entry `ingest_path`. |
| [graph/llm.py](graph/llm.py) | `LLMClient`: `available`, `complete`, `complete_json`; JSON helper `_extract_json`. |
| [graph/policy.py](graph/policy.py) | `Policy`; `load_policy`, `ensure_policy_file`, `_coerce`. |
| [graph/search.py](graph/search.py) | `SearchHit`, `SearchBackend`, `Fts5Backend`; `Fts5Backend.search`, `Fts5Backend.exact_title`; query sanitizer `_sanitize_fts_query`. |
| [graph/query.py](graph/query.py) | Result types `Citation`, `RetrievedNode`, `QueryResult`; `QueryResult.seeds`, `QueryResult.context_markdown`; `QueryService.query`, `_expand_edges`, `_traversal_strength`, `_citations`. |
| [graph/synthetic.py](graph/synthetic.py) | `SyntheticManager`: `lookup`, `record_query`, `should_create`, `create_or_refresh`, `_absolute_dependencies`, `_source_version_fingerprint`, `_link_dependencies`, `_compose_markdown`; `normalize_query`. |
| [graph/maintenance.py](graph/maintenance.py) | `HealthReport`, `Maintenance`: `reindex`, `refresh_stale_synthetic`, `health`, `_lint_isolated_documents`; module entry `run_maintenance`. |
| [graph/cli.py](graph/cli.py) | CLI commands `cmd_bootstrap`, `cmd_ingest`, `cmd_import`, `cmd_query`, `cmd_maintain`; parser/entry points `build_parser`, `main`; setup helpers `_wiki_root`, `_bootstrap_env`. |
| [graph/tests/test_pipeline.py](graph/tests/test_pipeline.py) | Test entry `main`; regression `test_coverage_rejects_empty_nonempty_assignment`; fixture helper `_write_compiled_tree`. |
| [graph/__init__.py](graph/__init__.py), [graph/tests/__init__.py](graph/tests/__init__.py) | Package markers; no runtime symbols. |

## Generated/runtime files — do not hand-edit

| Path | Meaning |
|---|---|
| `input/` | Raw Markdown inputs used by the compiler. |
| `output/` | Generated source trees, manifests, planning summaries, and coverage maps. Regenerate via `md.py` or `graph import`; do not manually repair generated leaves. |
| `.wiki/catalog.sqlite` | Generated SQLite graph catalog and FTS data. Rebuild with `bootstrap` if needed. |
| `.wiki/graph-policy.yml` | Runtime policy file. Safe to edit policy values intentionally. |
| `.wiki/synthetic/*.md` | Generated/reusable synthetic knowledge pages. They may become stale after source changes. |
| `image.png` | UI reference image, not runtime code. |
| `.claude/settings.local.json` | Local tool settings; do not use as application configuration. |
| `__pycache__/` and `*.pyc` | Python bytecode cache. |

## What to send a chat UI when something needs fixing

Send only the smallest relevant context:

1. This `guide.md` and the relevant section of `handoff.md`.
2. The exact file(s) from the table above.
   Include the matching class/function names from the code symbol map when the
   traceback identifies one.
3. The command run and its complete error/output.
4. A minimal input Markdown or generated `output/<source>/` tree that reproduces it.
5. The expected behavior and the invariant that must remain true.

Example prompt:

```text
Read guide.md and the "Query behavior" section of handoff.md.

Bug: `python -m graph.cli query "..."` returns too many unrelated pages.
Relevant file: graph/query.py.
Expected: retain local document context but stay inside graph-policy fan-out and
hop limits. Do not change md.py or weaken source-line coverage.

Output:
<paste output here>
```

For source-splitting issues, send `md.py`, the source input, its generated
`output/<source>/manifest.json`, `_planning/coverage.json`, and the affected
leaf pages. For graph issues, send the relevant `graph/*.py` files and the
`maintain` report.

## Non-negotiable invariants

- Every source line belongs to exactly one generated leaf source page.
- A large document enters the graph as a local document subgraph first.
- Active factual edges have source-version and line-range evidence.
- Synthetic nodes store flattened absolute dependencies and go stale on source
  updates.
- Query traversal obeys policy budgets and returns citations.
