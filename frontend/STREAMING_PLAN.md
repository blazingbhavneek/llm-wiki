# Streaming progress plan (step-level agent activity)

Goal: surface live agent progress in the chat UI — "searching X", "found N pages",
"spawned 3 explorers", "Explorer 1 reading <page>", etc. — like ChatGPT/Claude tool-use
trays. NOT token-level streaming (deferred to a later step; schema leaves room for it).

## Decisions (locked)
- **Transport:** `POST /api/ask/stream` + `fetch` `ReadableStream` reader parsing SSE
  frames. Question goes in the body (no URL length limit, POST only). EventSource
  rejected (GET-only, question in URL).
- **Tray UX:** activity steps collapse once the answer arrives. Header
  `Answer in N steps ▸` expands the full step log on click.

## Architecture — events escape a blocked thread
`engine.ask` runs on the **1-worker engine executor** and blocks it for the whole agent
run. Subagents run on child threads *inside* that call. Progress must be emitted from
those threads and bridged to the async HTTP response.

Bridge: a thread-safe `queue.Queue`.
- Agent + subagents push event dicts into the queue (thread-safe, works from child threads).
- The async SSE endpoint drains the queue and yields frames while the `engine.ask` future
  runs on the executor.
- On completion: push final `answer` event + sentinel; generator flushes and closes.

```
client ──SSE──> /api/ask/stream
                   │  submit engine.ask(q, on_event=push) ─► engine thread ─► subagent threads
                   │  async loop: ev = await run_in_executor(None, queue.get)
                   └─ yield "data: {ev}\n\n"  ... until sentinel, then final answer
```

## Event schema (step-level)
```
{type:"search",            phase:"main"|"sub", agent?:n, query}
{type:"candidates",        count, nodes:[{id,title}]}        # "pages being searched"
{type:"subagents_spawned", starts:[{id,title}]}
{type:"subagent_start",    agent, node:{id,title}}
{type:"read",              agent, node:{id,title}}
{type:"follow_link",       agent, node:{id,title}, neighbors}
{type:"subagent_done",     agent, cited:[id]}
{type:"compiling"}
{type:"answer",            answer, cited_node_ids, steps}     # terminal
{type:"error",             message}
```
Each event tagged `agent` (subagent index) so the UI groups "Explorer 1 → reading X".

## Backend changes
1. **`graph/agent.py`** — thread an optional `emit(event: dict)` callback through
   `ask → _run_loop → _dispatch_main / _run_subagents / _run_one_subagent / _dispatch_tools`.
   Emit at: each `search` (+ candidate titles), `explore` spawn (start-node titles),
   per-subagent start, each `read`/`follow_link` (with resolved node title), subagent done,
   compiling, final answer. Default `emit=None` → no-op (non-stream path + tests unchanged).
   **No langchain import — just a callback; graph boundary stays clean.**
2. **`graph/engine.py`** — `ask(question, persist=False, on_event=None)` passes `on_event`
   to `agent.ask`.
3. **`app.py`** — add `POST /api/ask/stream`:
   - make a `queue.Queue`; `on_event = queue.put_nowait`.
   - submit `engine.ask(q, on_event=...)` to the executor → future.
   - async generator: loop `await loop.run_in_executor(None, queue.get)`, yield SSE `data:`
     frames; on terminal/sentinel yield final + stop.
   - `StreamingResponse(..., media_type="text/event-stream")`, ~15s heartbeat comment to
     survive proxies.
   - keep existing `/api/ask` as a non-stream fallback.

## Frontend changes
1. **`src/api.js`** — `askStream(question, onEvent)`: `fetch` POST with a `ReadableStream`
   reader, split on `\n\n`, `JSON.parse` each `data:` line, call `onEvent(ev)`.
2. **`src/App.jsx` `ask`** — replace `await api.ask` with `askStream`. Maintain a live
   in-progress assistant message holding an `activity[]` array; append a line per event;
   on `answer` finalize to the current title/text/refs/canSave shape. Bonus: light up cited
   nodes in the graph live as `subagent_done`/`answer` arrive.
3. **`src/components/ChatPanel.jsx`** — render an **activity tray** on the streaming
   message: spinner + grouped step lines ("Searching 'cuda streams'", "Found 20 pages",
   "Spawned 3 explorers", "Explorer 1 · reading *Stream Memory Model*"). On completion
   collapse to `Answer in N steps ▸` with an expandable step log. Style like existing cards.

## Build sequence
1. Backend `emit` plumbing + `/api/ask/stream` (test with `curl -N`).
2. `api.js askStream` + minimal App.jsx wiring (log events).
3. ChatPanel activity tray UI + collapse.
4. Live graph highlight (optional polish).

## Trade-offs / notes
- **SSE over WebSocket** — one-way server→client, simplest, reconnect-friendly.
- **1-worker executor**: during a streamed ask, other engine calls (opening a ref node,
  graph refresh) queue behind it — already true today. Not raising worker count (sqlite is
  thread-bound). Optionally disable ref clicks until the answer lands.
- **Cancel on disconnect**: v1 can't interrupt a mid-flight LLM call; if the client drops,
  events stop being consumed and the run finishes on the engine thread. Acceptable for now.
- **Token streaming**: deferred; `answer` could later arrive in chunks under the same schema.
