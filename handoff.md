# LLM Wiki — Implementation Handoff

## Purpose of this document

This is the working handoff for the next implementation phase. It records:

- the current source compiler in [`md.py`](md.py);
- the non-negotiable source-coverage invariant;
- the agreed document-subgraph model;
- the two graph node classes, edge contract, update model, and query behavior;
- the planned `graph/` submodule that will implement the knowledge layer without
  turning `md.py` into the whole application.

This document is a design contract, not a replacement for source code. `md.py`
remains the canonical implementation of the current source-compilation phase.

## User requirements, quoted

> User said: "make sure no line is skipped, skipping any line is a killer, each line should belong somewhere, period"

> User said: "lets store a line range summary in a file first, what each 100 line contains, (show it previous 100 lines too so the llm knows what context there is + the line range summay till now) keep appending those summary in md"

> User said: "once all h1 folders are made then go to h2 splitting, now once h2 folders are made then there would be broken down into files. no further down then its too nested"

> User said: "given any kind of document, we can have a self growing knowledge base, a self growing wiki like deepwiki which have connections etc across document, communities clusters, if i throw in unrelated it shoould be its own cluster, if i show it code it should be seperate linked to the docs involved in it"

> User said: "I want it queryable (by LLM/normal document wiki search, elastic search, keyword search) and vieable, i want a UI to view the current documents etc too just like in @image.png but thats for later"

> User said: "instead of a weak link make a strong link with some overlap, so these would be pseudo nodes, which will act as a agent cache, if an agent somehow came across a connection, so we will store that weak connecction for later, so our queries will actually get faster over time as already existing weak relation which were explored would be cached"

> User said: "the problem with these is that information updates, if a in future we send a new version of docuemnt, we would need to update the absolute edges first, then the syntheises ones, so making it more and more hierachial is complexity"

> User said: "there are absolute nodes (from docs) and synthetic nodes (one made from multi hop querying by llm, a wiki doc made by query multiple times of graph and llm making a discovery, a new case and a new howto that doesnt exist directly, and next time if do same query that doc will come up instant, thats what it means by self growing too), and all edges between them have types/expalantion and a strength number (0-1)"

> User said: "while ingesting a large doc, we cant just ingest an absoulte doc as it is ... a md file in itself is not independant entity ... its first related to the whole document itself, and probably a small cluster by itself first, with a common topic/keyword that should be held by each page, it cannot exists as independant floating group of facts ... for ingesting big docs (at bootstrap or later ingests) it should make it a subgraph first"

## Current state: `md.py`

`md.py` is a Python batch source compiler for a local OpenAI-compatible LLM
server. Runtime settings are currently module constants at the top of the file:

- `SOURCE_PATH` and `OUTPUT_ROOT` point to `input/` and `output/` in this repo.
- The default model is `gemma4` using `OPENAI_BASE_URL` or
  `http://localhost:8000/v1`.
- The default phase is `all`, which runs generation, verification, then repair.
- The batch collector currently accepts a single Markdown file or top-level
  `*.md` files in the configured input directory.

### Current source-compilation flow

The default `phase_generate` is hierarchical and lossless:

```text
Input Markdown
  ↓
Chunk into roughly 100-line ranges, preserving code fences/tables where possible
  ↓
Append a factual summary of every chunk to _planning/chunk-summaries.md
  ↓
Each summary call sees the previous 100 raw source lines and all earlier summaries
  ↓
Plan all H1 ranges from the completed summary ledger
  ↓
Plan whether each H1 has direct leaf pages or H2 folders
  ↓
Plan final leaf-page ranges for H2 sections
  ↓
Reject an invalid partition or safely collapse it to one parent range
  ↓
Assert that leaf ranges are exactly a contiguous 1…N partition
  ↓
Render source-local Markdown tree and indexes
```

The rendered shape is similar to:

```text
output/<source-name>/
├── index.md
├── _planning/
│   ├── chunk-summaries.md
│   ├── topic-index.md
│   └── coverage.json
├── 01-getting-started/
│   ├── index.md
│   └── 01-installation/
│       ├── index.md
│       └── 001-install.md
└── 02-reference/
    ├── index.md
    └── 001-cli-reference.md
```

### Current safety properties

- Every leaf page contains frontmatter with its original `source_lines` range.
- `partition_or_fallback` accepts only chunk-aligned, gap-free, non-overlapping
  ranges. Invalid LLM plans become a single safe parent range instead of losing
  text.
- `assert_exact_coverage` runs before rendering and fails unless leaf ranges
  cover every source line exactly once.
- The renderer copies raw assigned source lines into the leaf page and preserves
  leading/trailing blank lines.
- `_planning/coverage.json` maps every source range to exactly one leaf file.
- A legacy flat generator remains available via `PHASE = "generate-flat"`.
- Existing verification checks source windows against generated pages in parallel.
  Existing repair appends a repair addendum when verification reports a loss.

### What `md.py` is not responsible for

`md.py` does **not** currently provide a global catalog, cross-document graph,
incremental graph invalidation, keyword/Elasticsearch/vector search, LLM query
retrieval, synthetic knowledge pages, community detection, or UI. Do not add all
of that logic to this file. It is the source compiler that feeds the next layer.

### Current integration contract emitted by `md.py`

The graph layer will consume, for each compiled source:

- the source-local output root;
- `manifest.json`, including the original source path and leaf file records;
- leaf-page frontmatter, especially `source_lines`;
- `_planning/topic-index.md` and the directory path for document context;
- `_planning/coverage.json` as a hard validation artifact.

Only generated leaf pages with source ranges are source-content records. Root/H1/H2
`index.md` files are navigation/context records, not independent source facts.

## Agreed knowledge model

There are exactly two graph node classes.

| Node class | Meaning | Examples |
|---|---|---|
| `absolute` | Directly grounded in source documents | document, section, source page, concept, entity, code module, API |
| `synthetic` | Durable Markdown compiled by an LLM from a valuable multi-hop query | discovery, how-to, case, comparison, investigation |

Subtypes do not introduce a third node class. A concept or code symbol extracted
from a document is still an `absolute` node because it has direct source evidence.

Every edge, regardless of source or target node class, must have:

```text
type          e.g. contains, mentions, supports, explains, applies_to,
              implements, depends_on, contradicts, derives_from
explanation   short human-readable reason for this exact relationship
strength      number in [0.0, 1.0], used for graph traversal/ranking
status        active | stale | rejected
evidence      direct source version and line-range references when applicable
created_by    bootstrap | ingest | query | review
```

`strength` represents retrieval/traversal value. It must never hide the absence
of evidence. An active factual edge requires source evidence.

## Large documents are document subgraphs

A leaf page from a large document is an absolute source fragment, not a global,
independent floating group of facts. It belongs to a document version and a
section path before it is linked outside its document.

```text
Absolute document root
├── contains [1.0] → H1 section
│   ├── contains [1.0] → H2 section
│   │   ├── contains [1.0] → leaf source page
│   │   └── local relation → leaf source page
│   └── contains [1.0] → leaf source page
└── has_topic → absolute concepts
```

Each page inherits document context as metadata:

```yaml
node_class: absolute
node_subtype: source_page
document_id: research-phosphorus
source_version: sha256:...
section_path: [Carbon source optimization, Low-temperature operation]
document_topics: [phosphorus removal, PAO enrichment]
local_topics: [acetate, temperature, DPAO]
source_ranges: [[401, 530]]
```

Document-level topics improve ranking and extraction context. They do **not**
automatically create edges between every page in the document, which would make
each book a misleading clique.

The first representation of a large source is therefore a coherent local cluster
with strong structural/local relationships and a small number of high-confidence
external links. An unrelated document begins as its own local cluster. A small
Markdown document uses the same model with one document root and one/few leaves.

## Synthetic knowledge nodes

A synthetic node is a Markdown wiki page written after an LLM traverses multiple
graph nodes and produces a durable result that does not exist directly in one
source: a discovery, a new case, a comparison, or a how-to.

```text
Absolute node A ──supports──┐
Absolute node B ──explains──┼── Synthetic how-to / discovery / case
Absolute node C ──contrasts─┘
```

Synthetic nodes are stored under `wiki/synthetic/`, indexed immediately, and
retrieved on the next equivalent query. They are the durable agent-memory/cache
mechanism that makes repeated queries faster.

Creation triggers:

- the same semantic query recurs;
- the user explicitly saves a result;
- a query finds a high-value, evidence-backed cross-document conclusion;
- a useful how-to/case/comparison is missing.

Before creating a synthetic node, search for an equivalent existing synthetic
node and refresh or extend it rather than creating a duplicate.

Every synthetic node stores a flattened closure of its absolute dependencies:

```yaml
node_class: synthetic
kind: howto | discovery | case | comparison | investigation
status: active | stale | review
creation_query: "..."
absolute_dependencies: [absolute-node-id, ...]
source_version_fingerprint: "..."
times_retrieved: 0
times_confirmed: 0
times_refreshed: 0
```

If a synthetic node used another synthetic node while being written, it must
still record the underlying absolute dependencies. This flattening is the key to
avoiding recursive synthetic update chains.

## Source updates and invalidation

```text
New version of a source document
  ↓
Compile and validate a new source-local tree in staging
  ↓
Build the new document-scoped absolute subgraph
  ↓
Atomically activate the source version
  ↓
Retire prior-version local pages, edges, and evidence
  ↓
Mark synthetic nodes whose dependency fingerprint includes the old source stale
  ↓
Refresh stale synthetic nodes only when queried, reviewed, or maintained
```

No eager cascade rewrite of synthetic Markdown is allowed. Stale synthetic nodes
are excluded from trusted retrieval until they are refreshed or reviewed.

An absolute global concept/entity remains active when another current source still
supports it. Otherwise it becomes unsupported/archived rather than silently
remaining a current fact.

## Planned `graph/` submodule

Keep `md.py` unchanged. The graph layer is a small, dedicated Python package
that consumes its compiled output. This is intentionally a thin vertical slice:
it preserves every agreed behavior, but combines operational concerns until
scale proves that they need separate services or modules.

```text
md.py owns: raw Markdown → lossless source-local tree
graph/ owns: compiled tree → catalog, graph, search, query, synthetic knowledge
```

Create:

```text
graph/
├── __init__.py
├── models.py             # Node, edge, evidence, compiled-document contracts
├── store.py              # SQLite schema, transactions, repositories, FTS5 setup
├── source_tree.py        # Adapter that reads md.py output/manifests/frontmatter
├── compiler.py           # Raw .md → staged md.py compile → promote → graph ingest
├── ingest.py             # Bootstrap, new/update ingest, extraction, invalidation
├── search.py             # FTS5 now; Elasticsearch/vector adapters behind one interface
├── query.py              # Search, bounded traversal, LLM context assembly
├── synthetic.py          # Reuse/create/refresh/stale synthetic Markdown nodes
├── maintenance.py        # Reindex, lazy stale refresh, lint, health metrics
├── cli.py                # bootstrap, ingest, query, maintain commands
└── tests/
```

`graph/source_tree.py` is the sole dependency on the compiled output format. It
must expose a stable `CompiledDocument` contract so that later changes to
`md.py` do not leak through the graph implementation.

```python
CompiledDocument(
    source_path=Path(...),
    output_root=Path(...),
    manifest=...,
    source_pages=[
        CompiledSourcePage(
            markdown_path=Path(...),
            source_ranges=[[401, 530]],
            section_path=[...],
            title="...",
            summary="...",
        ),
    ],
)
```

## Catalog schema plan

Use one SQLite database, `.wiki/catalog.sqlite`, as the operational source of
truth. It needs five ordinary tables plus an FTS5 virtual table. Evidence,
aliases, document context, dependency closures, and review data are JSON fields
at first; they can be normalized later without changing the public model.

| Table | Key data |
|---|---|
| `sources` | stable ID, logical path/name, current version ID, source type |
| `source_versions` | source ID, SHA-256, imported time, compiler version, active state |
| `nodes` | class/subtype, title, Markdown path, source version, document ID, section path, status, `metadata_json` |
| `edges` | endpoints, type, explanation, strength, status, `evidence_json`, `dependencies_json` |
| `query_cache` | normalized query/intent key, synthetic node ID, use/refresh counters |
| `node_fts` | SQLite FTS5 index over titles, aliases, summaries, and Markdown text |

The simplification does not remove provenance:

- `nodes.metadata_json` contains document topics, aliases, source ranges, and
  generated/updated metadata.
- `edges.evidence_json` contains exact source-version/range evidence.
- `edges.dependencies_json` and synthetic-node metadata contain the flattened
  absolute dependency closure used for staleness checks.
- A source update is one SQLite transaction; there is no initial jobs database
  or background-worker requirement.

## Graph build and ingest behavior

### Initial bootstrap

```text
For every output/<source>/ tree
  1. Validate coverage.json and source-page frontmatter.
  2. Register source and current source version.
  3. Build one document-root node and source-page absolute nodes. Keep H1/H2 in
     each page's section-path metadata; the physical source tree remains the
     navigation hierarchy.
  4. Extract document profile, local topics, local absolute nodes, and local edges.
  5. Resolve high-confidence external links to existing absolute nodes.
  6. Store exact line-range evidence for every factual edge.
  7. Index active page/node Markdown in FTS5. The same search interface can add
     Elasticsearch and vector backends later without changing ingest or query.
```

### New large Markdown document

```text
Hash source → run md.py into staging → validate lossless coverage
→ register document version → build local subgraph → resolve controlled external links
→ activate version → update FTS5 → run optional maintenance on demand
```

### New small Markdown document

Use the same path. Its document subgraph normally has one root and one/few source
pages, rather than special-casing it as a globally independent page.

### Updated document

```text
Create new source version and complete staging subgraph first
→ activate it in one catalog transaction
→ retire prior-version evidence/local edges
→ preserve globally supported absolute nodes
→ mark only dependent synthetic nodes stale
→ refresh lazily on the next matching query or via an explicit maintain command
```

## Query behavior

All interfaces—normal wiki search, keyword/Elasticsearch, vector search, LLM
agents, and the future UI—must use the same query service. FTS5 is the default
backend. Elasticsearch and vector search are optional adapters, not additional
sources of truth.

```text
Query
  ↓
Exact title/alias search + FTS5 + optional Elasticsearch/vector adapters
  ↓
Rank absolute pages/nodes and active synthetic nodes as seeds
  ↓
Expand one/two typed graph hops within strict budget
  ↓
Load selected Markdown and exact source citations
  ↓
LLM answer or normal search response
  ↓
Optionally create/refresh a synthetic node if the result has durable value
```

Source-page search should expand locally inside its document subgraph before
making weak global jumps. This retains document context rather than treating a
book page as an isolated fact.

## Graph policy and health controls

Start with a small versioned `.wiki/graph-policy.yml`. `maintenance.py` reads it
for both linting and traversal; no separate policy/health services are needed.

```yaml
max_semantic_hops: 2
second_hop_decay: 0.35
max_query_nodes: 30
max_external_edges_per_source_page: 8
max_external_edges_per_document: 25
max_edges_per_expansion: 8
max_local_pages_from_document: 6
contains_traversal_weight: 0.1
max_edges_per_synthetic_node: 10
minimum_active_strength: 0.45
synthetic_repeat_query_threshold: 2
synthetic_requires_absolute_evidence: true
exclude_stale_synthetic_nodes: true
```

Track and lint:

- line/source coverage and edge-evidence coverage;
- active/stale/rejected edge and synthetic-node counts;
- node-degree distribution, hub concentration, and one/two-hop fan-out;
- document subgraphs with no meaningful external links;
- unrelated clusters incorrectly connected by weak edges;
- synthetic-node reuse/cache-hit rate and duplicate rate;
- synthetic nodes with outdated or missing absolute dependencies.

## Implementation order

1. Define `models.py`, the five-table SQLite schema in `store.py`, the edge
   contract, and the small `graph-policy.yml`.
2. Implement `source_tree.py`; bootstrap existing `output/` trees into document
   roots and source-page absolute nodes, using section paths as metadata.
3. Implement absolute extraction and basic identity resolution inside `ingest.py`.
   Store aliases, evidence, and review flags in JSON metadata initially.
4. Add FTS5 search and bounded typed/weighted traversal in `query.py`.
5. Add staged raw-Markdown import for new/updated large and small documents: call
   the unchanged `md.py`, validate the staged tree, promote it, activate its
   source version, and apply lazy synthetic staleness.
6. Add `synthetic.py`: repeated-query matching, Markdown creation/reuse, flattened
   absolute dependencies, and immediate FTS indexing.
7. Add `maintenance.py`: explicit `maintain` command for stale refresh, linting,
   health metrics, optional embeddings, and an Elasticsearch projection.
8. Expose the same query/graph API to future UI code. The UI must not contain
   ingest, update, graph, or retrieval rules.

## Simplification boundaries

The following concerns remain supported but are deliberately not separate
subsystems in the first implementation:

| Capability | Lean implementation now | Later extraction if needed |
|---|---|---|
| Keyword search | SQLite FTS5 | Elasticsearch projection adapter |
| Vector search | Optional adapter in `search.py` | Dedicated vector store/process |
| Evidence and dependencies | JSON fields on nodes/edges | Normalized evidence/dependency tables |
| Aliases/review | JSON metadata and CLI output | Review queue and dedicated tables/UI |
| Background work | Explicit `maintain` command | Durable job queue/workers |
| H1/H2 graph nodes | `section_path` metadata and existing folders | Explicit structural nodes if graph navigation needs them |
| Communities/health | On-demand metrics in `maintenance.py` | Scheduled analytics and UI panels |

No user-visible knowledge behavior is removed: sources remain lossless and
versioned, large documents remain local subgraphs, typed/weighted/evidenced
edges remain queryable, synthetic Markdown remains reusable agent memory, and
Elasticsearch/vector/community capabilities remain compatible extensions.

## Non-negotiable acceptance criteria

- No source line is lost during `md.py` compilation; every line belongs to one
  leaf source page.
- A large document is represented as a document subgraph before global linking.
- Every active factual edge has source-version and line-range evidence.
- Every synthetic node has flattened absolute dependencies and becomes stale
  when any dependency source version changes.
- Search, LLM retrieval, and later UI use one query service and respect stale
  status, edge type, strength, traversal budgets, and citations.
- New knowledge can make future related queries faster, but the system must not
  turn uncited LLM speculation into trusted graph facts.
