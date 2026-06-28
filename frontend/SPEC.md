# LLM-Wiki — Frontend Design Spec

Designer-facing feature spec for the LLM-Wiki UI. Each feature lists what the user
sees/does, the design need, and the backend hook it maps to (so behavior stays
grounded in what the system can actually do).

This is **not a normal doc-page wiki** (no GitHub-style file tree of pages). The
knowledge lives in a graph. The user explores by *chatting with an agent*, *reading
and editing nodes*, and *watching the graph respond*.

> Note on backend-only ops: things like cascade-regeneration, supersede chains, and
> revision matching happen **automatically** inside the backend. The user never
> presses a "cascade" button — they just see results (e.g. a node greys out). Those
> are called out as *system feedback*, not controls.

---

## Layout

```
┌───────────────────────────┬───────────────────────────────────────┐
│                           │  N nodes · M links   [Insights N] [+] │
│        CHAT PANEL         │  [Source/Agent ▾]  Conflict Stale Clu │
│        (left)             ├───────────────────────────────────────┤
│  - ask the agent          │                                       │
│  - streaming answer       │       KNOWLEDGE GRAPH                 │
│  - reasoning trace        │       (force-directed, fills pane)    │
│  - "answer came from →"   │                                       │
│  - "Add to wiki" button   │  - color-mode toggle + legend        │
│  - search / explore box   │  - click node → peek (read/edit/del) │
│                           │  - hover edge → relationship label   │
└───────────────────────────┴───────────────────────────────────────┘
```

- **Left: chat panel.** Conversation with the agent + a search box.
- **Right: knowledge graph.** Force-directed, fills the pane (see `image.png` for tone).
- Simple by default: the graph is the only "browser." Reading, editing, adding, and
  inspecting all happen as peeks/toggles over the graph — no separate page views.
- **Graph data source:** the whole graph (all nodes + edges) loads from one call;
  every view below is a re-style/filter of that same data client-side.

---

## A. Chat & answers

### A1. Ask the agent
Plain chat box. User asks; the agent navigates the graph and answers.
- **Design:** message bubbles, streaming answer text, subtle "thinking…" state.
- **Backend:** `engine.ask(question)` — agent reasoning loop (`flow.md` §12).

### A2. "Answer came from" — provenance
Every agent answer shows **which nodes it was built from** (the user's core ask).
A row of source chips under the answer; clicking one focuses that node in the graph.
- **Design:** citation chips beneath each answer bubble; hovering a chip previews the
  node, clicking it pans/highlights it in the graph.
- **Backend:** the answer carries `cited_node_ids` (the nodes the agent actually used);
  edges among them are `supports` provenance links (§11, §12).

### A3. Live graph focus during an answer
When an answer arrives, **its source nodes light up; all other nodes dim**
(desaturated). Clicking an old answer re-triggers its focus.
- **Design:** two graph states — *neutral* (all colored) and *focused* (cited bright,
  rest low-opacity grey). The provenance chips (A2) drive this.
- **Backend:** same `cited_node_ids`.

### A3b. Reasoning trace (optional, collapsible)
The agent doesn't do one lookup — it **searches, reads, and follows links** over
several steps. Optionally show that path so the user trusts the answer.
- **Design:** a collapsible "how it got here" strip under the answer — a short list
  like `searched "X" → read node A → followed link → read node B`. Show the step
  count. Collapsed by default.
- **Backend:** the answer reports `steps`; the agent's tools are `search` / `read` /
  `follow_link` / `finish` (`agent.py`).

### A4. Save answer as a node ("Add to wiki")
If the answer is good, a **button turns it into a permanent node**, linked to the
sources it cited. It then lives in the graph like any other knowledge.
- **Design:** button on the answer bubble; on click a new node animates in and draws
  links to its sources. New node uses the *agent* color (see C1).
- **Backend:** `create_exogenous_node(answer, cited_ids, origin)` — adds the node +
  `supports` edges from each cited source (§11).

---

## B. Node interaction (read / edit / delete)

### B1. Peek a node
Click any node → a lightweight panel shows its content. Not a full page.
- **Shows:** `title`, `summary`, `body` (markdown), `entity`, `claims[]`,
  `keywords[]`, `cluster`, source document name (`original_document_name`), and a
  **connection count** ("12 links").
- **Design:** popover or right-docked peek card; markdown-rendered body; claims as a
  list; keywords as tags. Distinguish source vs agent node (color/badge).
- **Backend:** `engine.read(node_id)` / `query("id", node_id)` returns the node + edges
  (§13); `health(node_id)` gives the local connection/degree count. All node fields
  above exist on every node.

### B1b. "Same entity across sources" badge
If the same real-world thing appears in **multiple documents**, show it — e.g. "also
defined in 2 other sources" — and let the user jump between those copies.
- **Design:** a small badge in the peek; clicking lists/links the duplicates.
- **Backend:** `same-as` edges link identical entities across docs (`same_as_group`).
  The system detects duplicates but never destructively merges them.

### B2. Edit a node
User can **edit a node's body**. Saving creates an updated version; the old one is
kept as history and anything derived from it refreshes automatically.
- **Design:** an "Edit" affordance in the peek → editable markdown → Save / Cancel.
  After save, show a brief "updated, N derived notes refreshed" toast.
- **Backend:** `engine.update(node_id, body)` — supersedes the old node and cascades
  to dependents automatically (§9b, §10). *Cascade is automatic — no user control.*

### B3. Delete a node
User can **remove a node** from the graph.
- **Design:** "Delete" in the peek with a confirm step; node + its edges fade out.
- **Backend:** `engine.delete(node_id)` — hard delete of node, edges, vectors.

### B4. Explore neighbors
From a peeked node, **expand its connections** — pull in the nodes it links to.
- **Design:** "show connections" on the peek; graph grows the node's neighborhood;
  links labeled by relationship. Optional **filter by relationship type** (e.g. show
  only "defines" or only "contradicts") and direction (what points *to* this vs *from*).
- **Backend:** `engine.follow_link(node_id, label, direction)` — supports a label
  filter and incoming/outgoing/both (§13).

---

## C. Graph views & color modes

### C1. Source vs Agent colors (primary legend)
Two node kinds, **distinct colors**, so the user always knows what's a real source vs
what the agent made.
- **Source nodes:** source-of-truth, from ingested docs. *(suggest cool/blue family)*
- **Agent nodes:** machine-made — saved answers & derived notes. *(warm/accent family)*
- **Backend:** `node.type` = `endogenous` | `exogenous`.

### C2. Conflict view
Toggle to surface **contradicting facts** — disagreeing nodes, with the older fact
shown as no-longer-valid.
- **Design:** "Conflicts" toggle; contradiction links in alert color (red); the
  superseded prior link faded/struck.
- **Backend:** `contradicts` edge label; a contradiction stamps the prior edge with
  `invalid_at` / `expired_at` (§6a, §16).

### C3. Stale / out-of-date view
Toggle to reveal **aged knowledge** — old versions of sources and orphaned agent
notes. Default graph hides these ("current only").
- **Design:** "Stale" toggle greys/marks `superseded` + `stale` nodes.
- **Backend:** `node.status` = `active` | `superseded` | `stale`.

### C4. Cluster coloring
Color nodes by **topic community**, with a small label per cluster. Optionally a
"recompute clusters" action and a **granularity** control (fewer big clusters ↔ more
small ones).
- **Design:** "Clusters" color mode; nodes tinted by community; optional refresh
  button + a coarse/fine slider.
- **Backend:** `recluster(resolution)` runs Louvain communities, labels by top
  keyword, writes `node.cluster`; `resolution` tunes granularity (§14).

### C5. Color-mode switch
One control to flip how nodes are colored: **Source/Agent · Clusters · Status**.
(`image.png` shows a `Type / Community / Insights` row — same idea.) Legend updates
with the mode.
- **Backend:** `type`, `cluster`, `status` all live on each node — switching is a
  client-side re-style, no recompute.

### C6. Edge relationship labels
**Hover a link** to see how two nodes relate, in plain language.
- **Design:** tooltip on edge hover showing the relationship (e.g. "defines",
  "example of", "contradicts") and the edge's `summary` sentence.
- **Backend:** every `Edge` has a `label` + human `summary` string.

---

## D. Search & navigation

### D1. Find a node
Search box (in chat panel) to **jump to a node** without asking a full question.
- **Design:** type → result list → click pans/highlights the node in the graph.
- **Backend:** `engine.search(text)` — hybrid keyword + vector search (§13).

### D2. Explore by concept (topic neighborhood)
Instead of a question, the user can drop in a **topic** and get the connected
sub-graph around it — a browse-by-concept entry point.
- **Design:** topic input → graph focuses on the matching nodes and their ~2-hop
  neighborhood (the rest dims, like an answer focus). Good for "show me everything
  near X."
- **Backend:** `query("vector", topic)` seeds by semantic match then expands a 2-hop
  neighborhood of active nodes + edges (§13).

### D3. Add a source
A **(+) action to bring a new document into the wiki.** After adding, the system
tells the user whether it's new or an update, and the graph grows.
- **Design:** "+" / upload affordance; show a short status ("new document",
  "updated — N chunks changed"); new nodes animate into the graph.
- **Backend:** `recon(file)` reports `new` / `unchanged` / `changed`; then
  `ingest_md_output` / `cascading_update` does the work automatically.

---

## E. Graph overview & insights

### E1. Header counts
A small header over the graph: **N nodes · M links** — and the source-vs-agent
split (e.g. "84 sources · 21 agent notes"). (`image.png` shows "70 pages · 154 links".)
- **Design:** thin stat strip at top of the graph pane.
- **Backend:** `health()` → `GraphStats`: `total_nodes`, `total_edges`,
  `endogenous_nodes`, `exogenous_nodes` (§14).

### E2. Insights chip
A single **"Insights N"** chip (like the image) that surfaces things worth attention,
opening a short list: number of **conflicts**, **stale/superseded** nodes, and
**isolated** (disconnected) nodes — each clicking filters the graph to them.
- **Design:** a chip in the graph toolbar with a count; click → small list with jump
  links. Drives the same Conflict/Stale filters (C2/C3) plus an "isolated" filter.
- **Backend:** `health()` gives `isolated_nodes` + counts; conflicts = `contradicts`
  edges; stale = `superseded`/`stale` status. All derivable from the loaded graph.

## System feedback (automatic — no user control, but user-visible)

- **Self-healing graph:** editing or re-adding a source makes derived agent notes
  **regenerate or grey out** on their own (cascade, §10). User just watches it happen.
- **Versioning:** old node versions don't vanish — they become `superseded` and are
  visible in the Stale view (C3).
- **Dedup:** the same real-world entity from two docs is linked, not duplicated
  (`same-as`).

---

## Default state

- Graph loads in **Source/Agent color mode**, all nodes colored, **current-only**.
- Asking a question dims the graph and lights up the cited path.
- **Conflicts / Stale / Clusters** are opt-in toggles, off by default.

---

## Node + edge vocabulary (reference for the designer)

**Node kinds** (the primary color split):
| kind | meaning |
|---|---|
| endogenous | source-of-truth chunk from an ingested document |
| exogenous | agent-made node: saved answer or derived note |

**Node status** (age / validity):
| status | meaning |
|---|---|
| active | current, live |
| superseded | a newer version exists |
| stale | agent node that lost the sources it was built from |

**Node fields available in the peek:**
`title`, `summary`, `body` (markdown), `entity`, `claims[]`, `keywords[]`,
`cluster`, `original_document_name`.

**Edge labels** (link styling + hover text):
| label | meaning |
|---|---|
| follows | adjacent page in source order (draw faint) |
| related / uses / defines / example-of / prerequisite-for | semantic links |
| contradicts | conflicting facts (draw alert/red) |
| same-as | two nodes are the same real-world entity (draw dashed) |
| supports | a source node backs an agent node (provenance) |
| superseded_by / supersedes | version link between old and new node |
