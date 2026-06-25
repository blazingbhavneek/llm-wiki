"""Runtime configuration for the wiki graph.

Everything that points at a model, an endpoint, or a file lives here so the rest
of the package never reads ``os.environ`` directly. Build one ``Settings`` with
``Settings.from_env()`` and pass it around.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """All tunables for one engine instance."""

    # Chat LLM (OpenAI-compatible: vLLM / llama.cpp / work-pc gpt-oss).
    chat_base_url: str = "http://10.160.144.101:51021/v1"
    chat_api_key: str = "local"
    chat_model: str = "openai/gpt-oss-120b"
    chat_temperature: float = 0.2

    # Embeddings. backend = "server" (OpenAI-compatible) or "hf" (local GPU).
    # "server" auto-falls-back to "hf" when the endpoint is unreachable.
    embed_backend: str = "server"
    embed_base_url: str = "http://10.160.144.101:51025/v1"
    embed_api_key: str = "local"
    embed_model: str = "cl-nagoya/ruri-v3-310m"
    hf_embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    hf_device: str = "cuda:0"
    embed_dim: int = 768  # asserted against the live model on first embed.

    # Storage.
    database_path: str = ".wiki/wiki.sqlite"

    # Graph behaviour.
    edge_candidate_k: int = 12  # KNN neighbours considered per new node.
    vector_query_k: int = 20
    cascade_max_hops: int = 2
    cascade_max_nodes: int = 50

    @classmethod
    def from_env(cls) -> "Settings":
        env = os.environ.get
        return cls(
            chat_base_url=env("OPENAI_BASE_URL", cls.chat_base_url),
            chat_api_key=env("OPENAI_API_KEY", cls.chat_api_key),
            chat_model=env("WIKI_MODEL", cls.chat_model),
            chat_temperature=float(env("WIKI_TEMPERATURE", cls.chat_temperature)),
            embed_backend=env("WIKI_EMBED_BACKEND", cls.embed_backend),
            embed_base_url=env("WIKI_EMBED_BASE_URL", env("OPENAI_EMBED_BASE_URL", cls.embed_base_url)),
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
        )
