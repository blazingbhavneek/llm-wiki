"""Pydantic schema shared across the package."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import os

from pydantic import BaseModel, Field

# region TIMESTAMPS
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# endregion TIMESTAMPS

# region SETTINGS
@dataclass
class Settings:
    """All tunables for one engine instance."""

    chat_base_url: str = "http://180.21.170.235:42374/v1"
    chat_api_key: str = "local"
    chat_model: str = "nvidia/Qwen3.6-35B-A3B-NVFP4"
    chat_temperature: float = 0.2

    embed_backend: str = "server"
    embed_base_url: str = "http://localhost:8080/v1"
    embed_api_key: str = "local"
    embed_model: str = "cl-nagoya/ruri-v3-30m"
    hf_embed_model: str = "cl-nagoya/ruri-v3-30m"
    hf_device: str = "cuda:0"
    embed_dim: int = 768

    database_path: str = ".wiki/wiki.sqlite"

    edge_candidate_k: int = 12
    vector_query_k: int = 1
    cascade_max_hops: int = 2
    cascade_max_nodes: int = 50
    agent_max_steps: int = 6
    agent_patience: int = 3
    search_rrf_k: int = 60
    entity_dedup: bool = True

    @classmethod
    def from_env(cls) -> "Settings":
        env = os.environ.get
        return cls(
            chat_base_url=env("OPENAI_BASE_URL", cls.chat_base_url),
            chat_api_key=env("OPENAI_API_KEY", cls.chat_api_key),
            chat_model=env("WIKI_MODEL", cls.chat_model),
            chat_temperature=float(env("WIKI_TEMPERATURE", cls.chat_temperature)),
            embed_backend=env("WIKI_EMBED_BACKEND", cls.embed_backend),
            embed_base_url=env(
                "WIKI_EMBED_BASE_URL",
                env("OPENAI_EMBED_BASE_URL", cls.embed_base_url),
            ),
            embed_api_key=env("WIKI_EMBED_API_KEY", cls.embed_api_key),
            embed_model=env("WIKI_EMBED_MODEL", cls.embed_model),
            hf_embed_model=env("WIKI_HF_EMBED_MODEL", cls.hf_embed_model),
            hf_device=env("WIKI_HF_DEVICE", cls.hf_device),
            embed_dim=int(env("WIKI_EMBED_DIM", cls.embed_dim)),
            database_path=env("WIKI_DB", cls.database_path),
            edge_candidate_k=int(env("WIKI_EDGE_K", cls.edge_candidate_k)),
            vector_query_k=int(env("WIKI_VECTOR_K", cls.vector_query_k)),
            cascade_max_hops=int(env("WIKI_CASCADE_MAX_HOPS", cls.cascade_max_hops)),
            cascade_max_nodes=int(env("WIKI_CASCADE_MAX_NODES", cls.cascade_max_nodes)),
            agent_max_steps=int(env("WIKI_AGENT_MAX_STEPS", cls.agent_max_steps)),
            agent_patience=int(env("WIKI_AGENT_PATIENCE", cls.agent_patience)),
            search_rrf_k=int(env("WIKI_SEARCH_RRF_K", cls.search_rrf_k)),
            entity_dedup=env("WIKI_ENTITY_DEDUP", "1" if cls.entity_dedup else "0")
            not in {"0", "false", "False", ""},
        )


# endregion SETTINGS

# region ENUMS
class NodeType(str, Enum):
    endogenous = "endogenous"
    exogenous = "exogenous"


class NodeStatus(str, Enum):
    active = "active"
    stale = "stale"
    superseded = "superseded"
    deleted = "deleted"


# endregion ENUMS

# region CORE GRAPH MODELS
class Node(BaseModel):
    id: str
    body: str
    type: NodeType = NodeType.endogenous
    title: str = ""
    original_document_name: str | None = None
    source_path: str | None = None
    source_ranges: list[tuple[int, int]] = Field(default_factory=list)
    source_version: str | None = None
    source_material_hash: str | None = None
    entity: str = ""
    claims: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    summary: str = ""
    cluster: str | None = None
    status: NodeStatus = NodeStatus.active
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)


class Edge(BaseModel):
    id: str
    source_node_id: str
    target_node_id: str
    label: str
    summary: str = ""
    created_at: str = Field(default_factory=now_iso)
    valid_at: str | None = None
    invalid_at: str | None = None
    expired_at: str | None = None
    source_episode_ids: list[str] = Field(default_factory=list)


# endregion CORE GRAPH MODELS

# region LLM EXCHANGE MODELS
class EdgeSuggestion(BaseModel):
    target_node_id: str
    label: str = "related"
    summary: str = ""


class EdgeSuggestions(BaseModel):
    edges: list[EdgeSuggestion] = Field(default_factory=list)


class Keywords(BaseModel):
    keywords: list[str] = Field(default_factory=list)


class ClaimExtraction(BaseModel):
    entity: str = ""
    claims: list[str] = Field(default_factory=list)


class EntityMatch(BaseModel):
    is_same: bool = False
    target_node_id: str | None = None


# endregion LLM EXCHANGE MODELS

# region QUERY AND METRICS
class QueryResult(BaseModel):
    query_type: str
    value: str
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)


class AgentAnswer(BaseModel):
    question: str
    answer: str = ""
    cited_node_ids: list[str] = Field(default_factory=list)
    exogenous_node_id: str | None = None
    steps: int = 0


class GraphStats(BaseModel):
    total_nodes: int
    active_nodes: int
    endogenous_nodes: int
    exogenous_nodes: int
    total_edges: int
    isolated_nodes: int
    avg_degree: float
    density: float
    mean_neighbor_overlap: float
    clusters: dict[str, int] = Field(default_factory=dict)
    target_node_id: str | None = None


# endregion QUERY AND METRICS

# region FUTURE COMPATIBILITY
# add tool-result models here later only if needed.
# add temporal edge fields here later only if needed.
# add query-cache model here later only if needed.
# endregion FUTURE COMPATIBILITY
