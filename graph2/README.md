# graph2 — LLM wiki knowledge graph with generated-wiki ingestion

Real implementation. No heuristic stand-ins: embeddings are real (sqlite-vec),
keyword search is real (FTS5/BM25), summaries / keywords / edges come from the
LLM, and markdown ingestion consumes the hierarchical `md.py` pipeline output.

## Layout

| file | role |
|---|---|
| `models.py` | Pydantic graph models plus `Settings` runtime config |
| `db/` | copied swappable storage backends; `graph2.db.Database` is the active graph backend |
| `embeddings/` | copied `Embedder` / `Reranker` — OpenAI-compat server, HF-GPU fallback |
| `engine.py` | `DomainEngine` facade: public wiring only |
| `runtime.py` | runtime services: enrichment, embeddings, semantic edges, query, exogenous nodes, analytics |
| `revisions.py` | recon / update / supersede / stale / cascade logic |
| `md_ingest.py` | `MarkdownIngest`: `md.py` output dir → nodes + structural edges |
| `cli.py` | `python -m graph2.cli ...` |
| `agent.py` | `QueryAgent`: graph retrieval tools + dispatch + answer persistence; the tool-call loop itself lives in `llm.AgentClient` |

## Pipeline

```
input.md ──md.py──▶ output/<doc>/ (manifest.json + leaf .md hierarchy)
                          │
           MarkdownIngest.load_md_output
                          │  nodes (title/summary/source_ranges) + follows-edges
                          ▼
          DomainEngine.ingest ── GraphRuntime.fill_derived_fields
                          │
                          ├─ embed body+summary ─▶ sqlite-vec
                          │
                          └─ semantic edges ── KNN ─▶ LLM judge ─▶ bidir edges
```

## CLI

```bash
python -m graph2.cli init
python -m graph2.cli add output/test          # ingest an md.py/output_embed dir
python -m graph2.cli add-wiki output_wiki     # ingest generated global wiki pages
python -m graph2.cli query keyword "gpu setup"
python -m graph2.cli query vector "select a device"   # +1-2 hop neighbourhood
python -m graph2.cli query id node:test-md:4564559ce3d6
python -m graph2.cli ask "how do I select a GPU device?"  # agent reasoning loop
python -m graph2.cli recon input/test.md       # new / unchanged / changed
python -m graph2.cli cascade output/test-v2    # append/supersede revised md.py output
python -m graph2.cli health
python -m graph2.cli get
```

## Config (env)

`OPENAI_BASE_URL`, `OPENAI_API_KEY`, `WIKI_MODEL`, `WIKI_EMBED_BACKEND`
(`server`|`hf`), `WIKI_EMBED_BASE_URL`, `WIKI_EMBED_MODEL`, `WIKI_HF_EMBED_MODEL`,
`WIKI_GRAPH2_DB`, `WIKI_EMBED_DIM`. Defaults target the work-pc servers (gpt-oss-120b,
ruri-v3); `server` auto-falls-back to local HF GPU when unreachable.

Cascade safety caps:

- `WIKI_CASCADE_MAX_HOPS` — downstream `supports` hops to regenerate, default `2`
- `WIKI_CASCADE_MAX_NODES` — max exogenous nodes touched per cascade, default `50`

## Dependencies

```
sqlite-vec pydantic            # core storage + schema
langchain-openai langchain-core  # chat + server embeddings
sentence-transformers torch langchain-huggingface  # only for HF embed fallback
pytest                         # tests
```

## Tests

```bash
python -m pytest graph2/tests/ -q   # offline: fake embedder + fake LLM injected
```

## Revision Updates

`cascade` consumes a fresh `md.py` output directory for the revised source. It
matches new source chunks against active nodes using exact body hashes first,
then extracted entity/claim metadata. Identical chunks are left alone, reordered
chunks remap without changing facts, changed chunks create a new active node and
mark the previous one `superseded` with `superseded_by` / `supersedes` edges.

After source changes are applied, cascade walks downstream `supports` edges only.
Supported exogenous nodes are regenerated from their current active supports and
supersede the older derived node. If a derived node loses all active support, it
is marked `stale`. This propagation is bounded by hop and node-count caps.

Source node bodies are append-only: cascade does not rewrite old source material
in place.

## Paper Ports (see `../todo/minimal_port_plan.md`)

- **Retrieval as reasoning** (LLM-Wiki): `engine.ask()` runs `QueryAgent`, which
  hands graph tools (`search/read/follow_link/finish`) + a dispatch callback to
  `llm.AgentClient.run_tool_loop` (native tool-calling lives in the `llm/` module,
  not graph). The final answer is saved as an exogenous node with `supports`
  edges (query-time graph growth + provenance). Bounded by `WIKI_AGENT_MAX_STEPS`
  (default 6).
- **Temporal edges** (Graphiti): edges carry `valid_at` / `invalid_at` /
  `expired_at` / `source_episode_ids`. A new `contradicts` edge invalidates the
  prior edge between the same pair (no extra LLM call).
- **Entity dedup, lite** (Graphiti): at ingest, an LLM same-entity check over KNN
  neighbors links near-duplicates with a `same-as` edge (detection only, no
  destructive merge). Toggle with `WIKI_ENTITY_DEDUP`.

## Still Missing

- Stronger claim matching for heavy rewrites where the local extractor is noisy
- Full Graphiti conflict pipeline (fast/slow dedup + batch arbitration) and
  destructive node merge
- Error Book / self-healing wiki structure (LLM-Wiki)
