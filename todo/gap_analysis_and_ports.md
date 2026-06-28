# Gap Analysis: Ours vs Papers + What to Port

## vs LLM-Wiki Paper (Retrieval as Reasoning)

### Their idea, our gap
| Their Concept | Our State | Gap |
|---|---|---|
| `search/read/follow_link` tool-call loop | Single `query()` call returns result set | Agents can't iterate — retrieval is lookup-shaped |
| Agent decides when evidence is sufficient | Caller gets all results at once | No stopping criterion, no multi-hop agent reasoning |
| Error Book: failures feed back to fix structure | No feedback loop | Wrong edges/stale structure never corrected from query failures |
| Compiled wiki pages (curated per-concept entries) | Raw markdown chunks + metadata | No concept consolidation layer |

### What to port (easy → hard)
**Easy:**
- Expose `search`, `read`, `follow_link` as tool-call-compatible methods on `DomainEngine`
  - `search(query)` → top-k nodes (already have this)
  - `read(node_id)` → full node body + summary (already have this)
  - `follow_link(node_id)` → neighbors via edges (already have this, just wrap it)
  - These three + a reasoning loop = the core of the paper's interface

**Medium:**
- Wire `agent.py` / `master_agent.py` into `query()` so it runs the tool-call loop instead of returning flat results
- Add a stopping condition: agent signals "sufficient evidence" and returns answer

**Hard:**
- Error Book: log when agent marks a retrieval as unhelpful → accumulate → periodic LLM pass to restructure bad edges
- Compiled/curated concept pages (exogenous nodes that synthesize across endogenous sources — we have the type, just not the curation pipeline)

---

## vs Graphiti (Temporal Knowledge Graph)

### Their idea, our gap
| Their Concept | Our State | Gap |
|---|---|---|
| `valid_at` / `invalid_at` on every edge | No temporal fields on `Edge` | Can't represent "fact was true from T1 to T2" |
| Logical contradiction detection (LLM) | Cascade detects source version change only | No way to say "new edge contradicts old edge at fact level" |
| Entity deduplication at ingest | No dedup — same concept = multiple nodes | Graph fragmented; same entity under different names not merged |
| `contradicted_facts` LLM arbitration | Edge prompt includes "contradicts" label but no follow-up | Label applied but old conflicting edge not invalidated |
| Episode provenance on every edge | `source_ranges` on nodes, nothing on edges | Can't trace which source episode produced which edge |
| Fast dedup: exact text match before LLM | No fast path | Every ingest hits LLM for edge building regardless |
| Redis cache for parallel ingest races | Single-writer SQLite | Not a problem at our scale; flag for later |

### What to port (easy → hard)

**Easy — add temporal fields to Edge model:**
```python
# models.py Edge
valid_at: datetime | None = None
invalid_at: datetime | None = None
source_episode_ids: list[str] = Field(default_factory=list)
```
Add columns to DB schema. No logic change needed yet — just future-proofs.

**Easy — episode IDs on edges:**
Track which node IDs / source ranges produced each edge. Already have `source_ranges` on nodes; propagate to edges at build time.

**Medium — entity deduplication on node ingest:**
Before creating a new node, embed its `entity` + `title`, KNN against existing nodes, LLM check: "is this the same real-world entity?" If yes → merge into canonical node (update summary, add source_ranges) rather than create duplicate.
This directly improves graph quality without touching cascade or edges.

**Medium — contradiction detection on new edges:**
When `build_semantic_edges` creates an edge with label `contradicts`, find existing edges between the same pair, LLM arbitrate. If new edge is confirmed contradiction: set `invalid_at` on the old edge, set `valid_at` on the new edge.
Requires temporal fields (above) first.

**Hard — full LLM contradiction pipeline:**
Graphiti-style per-episode: extract all new edges → dedup fast path (exact match) → slow path (hybrid search) → LLM batch arbitration → invalidate contradicted edges. High LLM call volume. Only worthwhile if ingesting many documents with overlapping facts.

---

## Priority Order (recommended)

1. **Temporal fields on Edge** — zero-breaking, enables everything else
2. **Entity deduplication on ingest** — highest ROI for graph quality; self-contained
3. **Wrap `search/read/follow_link` as tool-call methods** — unlocks agent reasoning loop
4. **Wire agent loop into `query()`** — makes retrieval reasoning-shaped
5. **Episode IDs on edges** — provenance for debugging
6. **Contradiction detection on `contradicts`-labeled edges** — correctness
7. **Error Book** — long-term structural quality; lowest urgency

## Our Advantages (don't lose these)
- **Cascade propagation**: Graphiti doesn't walk downstream when upstream fact changes. Keep this.
- **Hierarchy-aware ingestion**: `follows` edges from `md.py` structure. Graphiti uses flat episodes.
- **Endogenous/exogenous distinction**: clean separation of source truth vs derived content.
- **sqlite-vec + FTS5 in one SQLite file**: no infra dependencies.
