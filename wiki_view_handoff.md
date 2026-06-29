# Wiki Hierarchical View Handoff

This document is a handoff for the next agent. It captures the discussion about adding a hierarchical file view for the generated wiki, exposing that structure through an API, and surfacing it in a separate frontend/backend entrypoint without touching the working original `graph/` module.

## Goal

Create a user-facing hierarchical file view for `output_wiki` so the generated wiki is browseable like documentation sites or GitHub docs pages, instead of only being a flat set of canonical wiki pages.

The canonical generated wiki pages should remain the source of truth. The hierarchical view should be a navigation and presentation layer over those canonical pages.

## Directly Relevant Conversation

Verbatim user requests and decisions from the discussion:

> "OOoh also, i want a file view for wiki, curerntly the wiki you generated is flat? but maybe we want to make it viewable for users too? maybe we should group the generated wiki's by what docs were used as sources? and give them hierarchial file view just like a user has for github libs docs pages? dont write code, think about how would we do that, where what etc?"

> "Do we need another llm/agent pass for it?"

> "Doesnt the graph ingest have llm based clustering naming? we also have infered document naming too, cant we use that when the graph is ingested already? use doc name for main folder and cluster name for subfolder name? then organize the pages based on what lines are covered in each doc?"

> "Yes lets go, make a hierarchial view for the docs ingested too, and expose that ordering too as a api? so that we can see it in frontend too? make an app2.py that will expose these extra features?"

## Decisions

1. Keep canonical wiki pages flat.
2. Add a separate hierarchical view layer under `output_wiki/views/`.
3. Use the inferred source document name as the top-level folder name.
4. Use graph clustering labels as optional subfolder labels.
5. Place pages based on which source line ranges they cover.
6. Expose the resulting tree and ordering through an API.
7. Add a separate backend entrypoint, `app2.py`, to expose the new view API and keep it isolated from the original app.
8. Do not touch the working original `graph/` module.

## Recommended Structure

Canonical content stays as-is:

```text
output_wiki/
  raw/
  entities/
  concepts/
  summaries/
  indexes/
  _planning/
```

Add a view layer:

```text
output_wiki/
  views/
    sources/
      CUDA_C_Programming_Guide/
        README.md
        memory-model/
          README.md
        execution/
          README.md
      OpenMP-API-Specification/
        README.md
    navigation.json
```

The `views/` directory should not duplicate canonical page bodies unless there is a strong reason. It should mostly contain navigation pages and links to canonical wiki pages.

## Main Design Constraint

The view layer must not become a second source of truth.

Canonical wiki pages:

- live in `entities/`, `concepts/`, `summaries/`
- keep the actual markdown bodies
- carry the citations/line refs

Hierarchical view pages:

- are generated from canonical wiki metadata and source coverage
- organize pages for human browsing
- link back to canonical pages
- can be regenerated freely

## Source Of Truth For Grouping

Primary:

- `output_wiki/_planning/page_sources.json` when present

Fallback:

- parse markdown citations like `[CUDA_C_Programming_Guide:L1249-L1253]`
- use `raw/<doc_id>/coverage.json`
- use `raw/<doc_id>/metadata.json`

Optional enrichment:

- if the `graph2` DB already has ingested wiki pages, use `node.cluster` as a human-friendly subfolder label

## Hierarchy Rules

1. Top-level folder should be the source document name.
2. Subfolder should be a cluster/topic label when available.
3. Order pages by original source line coverage.
4. A page can appear in multiple folders if it cites multiple source sections.
5. Canonical page links should remain single references, not duplicated bodies.

## LLM / Agent Pass Question

The discussion concluded that a new LLM pass is not required for correctness.

Use deterministic generation first:

- build the tree from source coverage and citation metadata
- map pages to source sections
- write navigation output

Use LLM only optionally for polish:

- nicer folder names
- nicer chapter grouping
- short landing-page blurbs

If the graph has already assigned cluster names, they can be reused as labels, but they should remain labels only, not the source of truth.

## API Shape To Add

The backend should expose the hierarchical view so the frontend can render it.

Suggested API surface:

- `GET /api/wiki/tree`
- `GET /api/wiki/navigation`
- `GET /api/wiki/views`
- `GET /api/wiki/source/{doc_id}`

The exact names can vary, but the API needs to provide:

- source document tree
- folder ordering
- canonical page paths
- source line coverage metadata
- cluster labels if available

## `app2.py` Intent

Create a separate backend entrypoint that:

- wires to `graph2`, not the original `graph`
- exposes the new wiki view endpoints
- keeps the original graph app untouched

This should be a parallel app, not a replacement for `app.py`.

## Frontend Intent

The frontend should be able to render a docs-like tree view.

It should show:

- source document name
- cluster/topic grouping
- canonical wiki pages underneath
- ordered navigation matching source coverage

The current frontend already has a markdown renderer and a main app shell, so the new API can feed a new sidebar/tree panel or a separate wiki-browser mode.

## Existing Repo State To Respect

Already present:

- `graph2/` is a copied isolated graph module
- `graph2` has its own `db/` and `embeddings/` copies
- `graph2` has an `add-wiki` ingest path for `output_wiki`
- `wiki_embed/phases.py` stores `original.md` copies under `_planning`
- `wiki_new/planning.py` can record `original_source`
- `wiki_gen/` exists and is the source of the generated wiki output

Do not reintroduce coupling to the original `graph/` module.

## Practical Implementation Outline

1. Build a view generator in `wiki_gen` or a sibling module.
2. Read `raw/<doc_id>/coverage.json`, `raw/<doc_id>/metadata.json`, and canonical wiki page metadata.
3. Map page source ranges back to source sections.
4. Generate hierarchical navigation pages under `output_wiki/views/`.
5. Write a JSON navigation manifest for the frontend.
6. Add an API in `app2.py` to serve the view tree.
7. Add frontend support to render the tree.

## Important Caution

Do not rely on graph clustering as the only mechanism for hierarchy. Clusters are helpful as labels, but the tree must still be grounded in source coverage and line ranges.

If the cluster labels are missing or poor, the view must still be deterministic and usable.

## Current User Preference

The user explicitly prefers:

- no unnecessary extra LLM passes for correctness
- grouping by source document and then cluster/topic
- exposing ordering through an API
- a separate `app2.py`
- preserving the original graph module as-is

## Suggested Next Step For The Next Agent

Implement the deterministic view generator first, then wire `app2.py` to serve it. Only add LLM-assisted naming if the deterministic grouping feels too raw after the first pass.
