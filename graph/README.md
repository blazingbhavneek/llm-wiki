# graph — LLM wiki knowledge graph

Real implementation. No heuristic stand-ins: embeddings are real (sqlite-vec),
keyword search is real (FTS5/BM25), summaries / keywords / edges come from the
LLM, and markdown ingestion consumes the hierarchical `md.py` pipeline output.

## Layout

| file | role |
|---|---|
| `config.py` | `Settings` — endpoints, models, paths (env-driven) |
| `models.py` | Pydantic `Node`, `Edge`, `GraphStats`, `QueryResult` |
| `database.py` | SQLite: nodes, edges, `nodes_fts` (FTS5), `vec_body`/`vec_summary` (sqlite-vec) |
| `embeddings.py` | `Embedder` — OpenAI-compat server, HF-GPU fallback |
| `llm_client.py` | `LlmClient` — summarize, extract_keywords, suggest_edges, invoke |
| `md_ingest.py` | `md.py` output dir → nodes + structural edges |
| `edges.py` | KNN candidates → LLM judge → bidirectional semantic edges |
| `engine.py` | `DomainEngine` — ingest / query / recon / update / delete / get / health |
| `health.py` | degree, density, neighbour-overlap metrics |
| `cli.py` | `python -m graph.cli ...` |
| `agent.py`, `master_agent.py` | pass-2: query agent + specialist cache (ported from `new/`) |

## Pipeline

```
input.md ──md.py──▶ output/<doc>/ (manifest.json + leaf .md hierarchy)
                          │
              md_ingest.load_md_output
                          │  nodes (title/summary/source_ranges) + follows-edges
                          ▼
        DomainEngine.ingest ── LLM keywords ── embed body+summary ─▶ sqlite-vec
                          │
              edges.build_semantic_edges ── KNN ─▶ LLM judge ─▶ bidir edges
```

## CLI

```bash
python -m graph.cli init
python -m graph.cli add output/test          # ingest an md.py output dir
python -m graph.cli query keyword "gpu setup"
python -m graph.cli query vector "select a device"   # +1-2 hop neighbourhood
python -m graph.cli query id node:test-md:4564559ce3d6
python -m graph.cli recon input/test.md       # new / unchanged / changed
python -m graph.cli health
python -m graph.cli get
```

## Config (env)

`OPENAI_BASE_URL`, `OPENAI_API_KEY`, `WIKI_MODEL`, `WIKI_EMBED_BACKEND`
(`server`|`hf`), `WIKI_EMBED_BASE_URL`, `WIKI_EMBED_MODEL`, `WIKI_HF_EMBED_MODEL`,
`WIKI_DB`, `WIKI_EMBED_DIM`. Defaults target the work-pc servers (gpt-oss-120b,
ruri-v3); `server` auto-falls-back to local HF GPU when unreachable.

## Dependencies

```
sqlite-vec pydantic            # core storage + schema
langchain-openai langchain-core  # chat + server embeddings
sentence-transformers torch langchain-huggingface  # only for HF embed fallback
pytest                         # tests
```

## Tests

```bash
python -m pytest graph/tests/ -q   # offline: fake embedder + fake LLM injected
```

## Not yet implemented (pass 2 — raise `NotImplementedError`, not faked)

- `cascading_update` — line-range fact-check + recursive neighbour regeneration
- `recluster` — embedding clustering + LLM cluster labels
- query-time exogenous-node growth (agent cache feeding back into the graph)
- `agent.py` / `master_agent.py` query agent wired into `query`
