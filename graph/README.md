# `graph/` — knowledge layer over `md.py`

`md.py` owns: raw Markdown → lossless source-local tree.
`graph/` owns: compiled tree → catalog, graph, search, query, synthetic knowledge.

Implements the design contract in [`../handoff.md`](../handoff.md) as one thin
vertical slice. State lives under `.wiki/` (gitignored): `catalog.sqlite`,
`graph-policy.yml`, `synthetic/`.

## Modules

| File | Role |
|---|---|
| `models.py` | Two node classes (`absolute`/`synthetic`), edge contract, `Evidence`, `CompiledDocument`. |
| `store.py` | SQLite: five tables + FTS5, repositories, transactions. |
| `source_tree.py` | Only reader of `md.py` output; enforces lossless coverage; builds `CompiledDocument`. |
| `compiler.py` | Raw Markdown import: invoke unchanged `md.py` into staging, promote, then ingest. |
| `ids.py` | Deterministic stable node/edge ids (shared global topic identity). |
| `policy.py` | `graph-policy.yml` traversal/lint budgets. |
| `llm.py` | Optional OpenAI-compatible client; everything structural works without it. |
| `ingest.py` | Bootstrap, staged version activation, document subgraphs, invalidation. |
| `search.py` | `SearchBackend` protocol; FTS5 backend (ES/vector are later adapters). |
| `query.py` | One query service: seed → bounded typed/weighted traversal → cited context. |
| `synthetic.py` | Reuse/create/refresh synthetic nodes with flattened absolute deps. |
| `maintenance.py` | Reindex, lazy stale refresh, lint, health metrics. |
| `cli.py` | `bootstrap` / `ingest` / `import` / `query` / `maintain`. |

## Use

```bash
python md.py                                   # compile sources into output/
python -m graph.cli bootstrap --output output  # build catalog + graph
python -m graph.cli import input/new.md         # compile raw Markdown with md.py, then ingest
python -m graph.cli query "gpu environment setup"
python -m graph.cli query "gpu environment setup" --synthesize --kind howto
python -m graph.cli maintain                    # reindex, refresh stale, health
python -m graph.tests.test_pipeline             # end-to-end, no LLM needed
```

Add `--llm` to any command to enable LLM synthesis/extraction against an
OpenAI-compatible server (`OPENAI_BASE_URL`, default `http://localhost:8000/v1`).

## How it maps to the acceptance criteria

- **No lost source line** — `source_tree.validate_coverage` rejects any
  gap/overlap before ingest; `ingest_document` refuses uncovered trees.
- **Document subgraph before global linking** — one document root + page nodes;
  cross-document links exist *only* through shared global topic nodes.
- **Evidenced factual edges** — `contains`/`has_topic` carry source-version +
  line-range `Evidence`; `maintenance.health` lints any that don't.
- **Synthetic staleness** — synthetic nodes store a flattened
  `absolute_dependencies` closure and `source_version_fingerprint`; a source
  update marks them stale; they refresh lazily on query or `maintain`.
- **One query service** — search/LLM/UI all call `QueryService`, which respects
  stale status, edge type, strength, hop budget, and emits citations.
- **No uncited speculation as fact** — `synthetic_requires_absolute_evidence`
  refuses evidence-free synthetic creation.
