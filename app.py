"""FastAPI backend exposing the graph DomainEngine to the frontend.

Run:
    pip install fastapi "uvicorn[standard]"
    WIKI_DB=.wiki/test.sqlite uvicorn app:app --reload --port 8787

Every endpoint is a thin wrapper over `graph.DomainEngine` (see graph/flow.md).
The engine's SQLite connection is thread-bound, so ALL engine access is funneled
through a single dedicated worker thread (a 1-worker executor). The engine is also
constructed on that thread. This both fixes the cross-thread SQLite error and
serializes access (SQLite has no concurrent writers anyway).

Node/Edge payloads are the raw pydantic models; the frontend computes its own
layout (x/y) and view styling from node.type / node.status / edge.label.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from graph import DomainEngine, Settings

# region ENGINE LIFECYCLE
engine: DomainEngine | None = None
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="engine")


async def _run(fn, *args, **kwargs):
    """Run a (blocking) engine call on the single engine thread."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, lambda: fn(*args, **kwargs))


@asynccontextmanager
async def lifespan(_: FastAPI):
    global engine
    loop = asyncio.get_running_loop()
    engine = await loop.run_in_executor(_executor, lambda: DomainEngine(Settings.from_env()))
    try:
        yield
    finally:
        if engine is not None:
            await loop.run_in_executor(_executor, engine.close)
        engine = None
        _executor.shutdown(wait=True)


def _engine() -> DomainEngine:
    if engine is None:
        raise HTTPException(status_code=503, detail="engine not ready")
    return engine


# endregion ENGINE LIFECYCLE

app = FastAPI(title="LLM-Wiki API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# region REQUEST MODELS
class AskBody(BaseModel):
    question: str


class UpdateBody(BaseModel):
    body: str


class ExogenousBody(BaseModel):
    body: str
    source_node_ids: list[str] = []
    origin: str | None = None


# endregion REQUEST MODELS


# region GRAPH
@app.get("/api/graph")
async def get_graph() -> dict:
    nodes, edges = await _run(lambda: _engine().get())
    return {
        "nodes": [n.model_dump() for n in nodes],
        "edges": [e.model_dump() for e in edges],
    }


@app.get("/api/health")
async def get_health(node_id: str | None = None) -> dict:
    stats = await _run(lambda: _engine().health(node_id))
    return stats.model_dump()


@app.post("/api/recluster")
async def recluster(resolution: float = 1.0) -> dict:
    return await _run(lambda: _engine().recluster(resolution=resolution))


# endregion GRAPH


# region NODES
@app.get("/api/node/{node_id}")
async def read_node(node_id: str) -> dict:
    node = await _run(lambda: _engine().read(node_id))
    if node is None:
        raise HTTPException(status_code=404, detail="node not found")
    return node.model_dump()


@app.get("/api/node/{node_id}/links")
async def node_links(node_id: str, direction: str = "both", label: str | None = None) -> list[dict]:
    pairs = await _run(lambda: _engine().follow_link(node_id, label=label, direction=direction))
    return [{"edge": edge.model_dump(), "node": node.model_dump()} for edge, node in pairs]


@app.put("/api/node/{node_id}")
async def update_node(node_id: str, payload: UpdateBody) -> dict:
    try:
        node = await _run(lambda: _engine().update(node_id, payload.body))
    except Exception as exc:  # noqa: BLE001 - surface as 400
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return node.model_dump()


@app.delete("/api/node/{node_id}")
async def delete_node(node_id: str) -> dict:
    await _run(lambda: _engine().delete(node_id))
    return {"deleted": node_id}


# endregion NODES


# region SEARCH + AGENT
@app.get("/api/search")
async def search(q: str, limit: int | None = None) -> list[dict]:
    nodes = await _run(lambda: _engine().search(q, limit))
    return [n.model_dump() for n in nodes]


@app.post("/api/ask")
async def ask(payload: AskBody) -> dict:
    # persist=False: the chat answer is a draft. The user saves it via /api/exogenous.
    answer = await _run(lambda: _engine().ask(payload.question, persist=False))
    return answer.model_dump()


@app.post("/api/exogenous")
async def create_exogenous(payload: ExogenousBody) -> dict:
    node = await _run(
        lambda: _engine().create_exogenous_node(
            payload.body, payload.source_node_ids, origin=payload.origin
        )
    )
    return node.model_dump()


# endregion SEARCH + AGENT
