# LLM Wiki — Real Implementation Plan

Replaces the stubbed `graph/` package. No fake heuristics: real embeddings,
real LLM summary/keyword/edge/cluster ops, real full-text + vector search.
`legacy/` is reference-only (over-built; do not revive).

## Decisions

- **Vector index:** `sqlite-vec` — vectors live in the same SQLite file as
  nodes/edges. One file, no second server, no Chroma.
- **Embeddings:** OpenAI-compatible embed server by default
  (`ruri-v3-310m @ :51025`), automatic fallback to local HuggingFace GPU
  (RTX 5060 Ti) when the server is unreachable. Single `Embedder` abstraction.
- **Chat LLM:** OpenAI-compatible via `langchain_openai.ChatOpenAI`
  (work-pc default `gpt-oss-120b @ :51021`). Endpoint/model from env/config.
- **Chunking:** consume `md.py` hierarchical output. Never re-split markdown.
- **Scope this pass:** core pipeline. MasterAgent query-agent, cascading
  fact-check update, clustering, query-time exogenous growth = pass 2 (stubbed
  with explicit `NotImplementedError`, not fake logic).

## Brain-dead points being killed

| Old stub | Real replacement |
|---|---|
| `split_markdown_text` flat regex | consume `md.py` manifest + leaf frontmatter |
| `extract_keywords` stopword+count | LLM structured keyword extraction |
| edges via literal keyword overlap | embedding KNN candidates → LLM judge/label |
| cluster = first heading slice | (pass 2) embedding clusters + LLM labels |
| O(n) python cosine scan | sqlite-vec KNN |
| keyword search = token count | SQLite FTS5 (BM25) |
| `recon` returns advice string | doc-hash identity check → ingest vs update route |
| `summary_embedding` dead | second sqlite-vec table, queried |

## Package layout (`graph/`)

```
config.py        Settings: endpoints, models, db path, embed backend; env-driven
models.py        Pydantic: Node, Edge, NodeType, GraphStats, QueryResult, EdgeSuggestion
database.py      SQLite: nodes, edges, nodes_fts (FTS5), vec_body/vec_summary (sqlite-vec)
embeddings.py    Embedder: remote OpenAI-compat -> HF GPU fallback; batched embed_documents/query
llm_client.py    LlmClient: invoke(history), summarize, extract_keywords, structured output
prompts.py       system / summary / keyword / edge-judge prompts
md_ingest.py     md.py output -> Node list + structural parent/child edges
edges.py         semantic edge builder: KNN candidates -> LLM judge -> labeled bidir edges
engine.py        DomainEngine: ingest, md_to_nodes, query, recon, update, delete, get, health
health.py        real metrics: degree dist, density, edge overlap, isolated, clusters
cli.py           init / add / query / get / health / delete / update
agent.py         AgentClient (tool loop) — port new/agent_client.py        [pass 2 use]
master_agent.py  MasterAgent + specialist cache — port new/master_agent.py [pass 2]
tests/
```

## Component detail

### config.py
`Settings` dataclass from env: `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `WIKI_MODEL`,
`WIKI_EMBED_BASE_URL`, `WIKI_EMBED_MODEL`, `WIKI_EMBED_BACKEND` (`server|hf`),
`WIKI_HF_EMBED_MODEL`, `WIKI_DB`, embed dim. Single source of truth.

### models.py (Pydantic, matches canvas)
- `Node`: id, body, type(endogenous|exogenous), original_document_name,
  source_path, source_ranges, keywords[], summary, cluster, status, created/updated.
  Embeddings NOT stored on the model — they live in sqlite-vec keyed by id.
- `Edge`: id, source_node_id, target_node_id, label, summary, created_at.
- `EdgeSuggestion`: target_node_id, label, summary (LLM structured output).
- `GraphStats`, `QueryResult`.

### database.py
- Tables `nodes`, `edges` (+ indexes).
- `nodes_fts` FTS5 virtual table (body+summary+keywords+title), synced by triggers
  → real BM25 keyword search.
- `vec_body`, `vec_summary` via `sqlite-vec` `vec0` virtual tables (float[dim]).
  `knn(vec, k)` for vector search and edge-candidate retrieval.
- Single connection, `contextvar` singleton + lock (per canvas Domain Engine init).
- CRUD keeps FTS + vec rows in sync on upsert/delete.

### embeddings.py
`Embedder.embed_documents(list)`, `embed_query(str)` → `list[list[float]]`.
Backend `server`: `OpenAIEmbeddings(base_url, model)`. Backend `hf`:
`HuggingFaceEmbeddings(model, device=cuda)`. `server` auto-falls-back to `hf` on
connection error (logged once). Batched. Dim asserted against config.

### llm_client.py
Port of `new/agent_client.py` shape. Methods:
- `summarize(text) -> str` (LLM, facts-only prompt).
- `extract_keywords(text) -> list[str]` via `with_structured_output` (pydantic
  `Keywords(list[str])`) — real, not stopwords.
- `invoke(prompt, output_model=None)` history-keeping chat.
md.py already emits title+summary for leaf nodes, so summarize is only used for
exogenous/updated nodes.

### md_ingest.py
Input: a `md.py` output dir (has `manifest.json`, nested leaf `.md`).
- Read `manifest.json` → source path, files[] (filename, title, summary, source_ranges).
- Each leaf `.md`: strip frontmatter, body = content; node summary = manifest summary,
  title kept; cluster = section dir name (seed only; pass-2 reclusters).
- Build **structural edges**: leaf↔leaf within same section = `sibling`;
  parent section is encoded via `cluster`. (Semantic edges added later in ingest.)
- Returns `list[Node]` with `source_path`, `source_ranges` set (tether for recon/update).

### edges.py
`build_semantic_edges(engine, node, k=12)`:
1. KNN on `vec_body` + `vec_summary` for top-k existing active nodes (sqlite-vec).
2. Pass node + candidate {id, title, summary, keywords} to LLM
   (`with_structured_output(list[EdgeSuggestion])`): "which candidates relate, label, why".
3. Validate target ids ∈ candidates, dedupe, write **bidirectional** edges.
No literal-keyword gate. Embedding recall + LLM precision.

### engine.py — DomainEngine
- `__init__(config)`: open Database, Embedder, LlmClient. contextvar singleton.
- `md_to_nodes(md_output_dir)`: delegate to md_ingest.
- `ingest(node)`: fill missing summary/keywords via LLM, embed body+summary →
  sqlite-vec, persist node, then `build_semantic_edges`.
- `ingest_md_output(dir)`: md_to_nodes → ingest each (structural edges first).
- `query(type, value)`:
  - `id` → node + its edges.
  - `keyword` → FTS5 BM25.
  - `vector` → embed query → sqlite-vec KNN on body (+summary), return hits +
    1–2 hop neighborhood (canvas).
- `recon(md_path_or_dir)`: hash source / match `original_document_name` +
  source hash in DB. New → "ingest" job; known → "cascading_update" job (pass 2).
- `update(node_id, body)`: re-summarize, re-keyword, re-embed, rewrite vec/FTS,
  re-run semantic edges. (Cascade to neighbors = pass 2.)
- `delete(node_id)`: node + edges + vec + FTS rows.
- `get()`: all nodes/edges (ids+summaries) for UI.
- `health()`: delegate health.py.
- `create_exogenous_node(...)`: real node + supports-edges (used by pass-2 growth).

### health.py
Real: node/edge counts by type/status, avg degree, density
(edges / max-possible), degree distribution, isolated nodes, edge-overlap
(Jaccard of neighbor sets sampled), cluster sizes. Flags too-dense/too-sparse.

### cli.py
`init`, `add <md-output-dir>`, `query {keyword|vector|id} <val>`, `get`,
`health [node]`, `delete <id>`, `update <id> <md>`. Engine built from config.

## Dependencies (add to venv)
`langchain-openai langchain-core sqlite-vec pydantic` (core).
`sentence-transformers torch langchain-huggingface` only if HF fallback used.
Note: current `.venv` is near-empty — install step required before run.

## Test
`tests/test_pipeline.py`: fake Embedder (deterministic vectors) + fake LlmClient
(rule-based) injected → exercise db/FTS/vec/edge/query/health WITHOUT network.
Real-endpoint smoke test gated behind env flag.

## Build order
1. config, models
2. database (+FTS5 +sqlite-vec), unit test CRUD/search with fake vectors
3. embeddings, llm_client
4. md_ingest (against existing `output/test`)
5. edges, engine
6. health, cli
7. tests, README
8. pass 2: agent/master_agent port, cascading_update, clustering, exogenous growth
