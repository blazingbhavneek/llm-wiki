# Paper: Zep/Graphiti — Temporal Knowledge Graph for Agent Memory
arxiv: https://arxiv.org/abs/2501.13956
code: https://github.com/getzep/graphiti

## Problem
Knowledge graphs for agents need to handle contradictions, changing facts, and entity merging — not just append new information blindly.

## Core Architecture

### Temporal Validity on Edges
Every `EntityEdge` has:
```python
valid_at: datetime | None      # when fact became true in the world
invalid_at: datetime | None    # when fact stopped being true
expired_at: datetime | None    # when system marked it invalid
reference_time: datetime       # timestamp from the episode that produced it
```
Facts are never deleted — only invalidated. Full temporal history preserved. Query "what was true at time T."

### Conflict Pipeline (per new episode ingested)
1. Extract edges from new content via LLM
2. Fast dedup: exact text match against existing edges
3. Slow dedup: hybrid search (vector + keyword) for candidate edges at same endpoints → LLM arbitrates `duplicate_facts` vs `contradicted_facts`
4. Temporal invalidation: old edge gets `invalid_at` if `old.invalid_at ≤ new.valid_at`
5. Redis cache for recently resolved edges → avoids parallel ingestion races

### Entity Deduplication (nodes)
LLM checks each new extracted entity against candidates. Context-aware — avoids false positives ("Java" island vs language). Batched. On match: merges summaries into canonical node.

### LLM Contradiction Prompt
Returns `EdgeDuplicate`:
- `duplicate_facts`: indices of semantically identical existing facts
- `contradicted_facts`: indices of conflicting facts (either direction)

Rule: never mark as duplicate if key differences in numeric values, dates, or qualifiers.

### Provenance
Every edge carries list of episode IDs → traces back to raw source data.

## Weaknesses
- No propagation: invalidates the one contradicted edge, doesn't walk downstream derived knowledge
- No hierarchy-aware ingestion (flat episodes, not structured chunks)
- No source/derived node distinction
- No graph-level cascade when upstream fact changes
