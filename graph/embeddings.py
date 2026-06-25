"""Real embeddings.

Default backend talks to an OpenAI-compatible embedding server. If that server
is unreachable it falls back, once, to a local HuggingFace model on the GPU.
There is no fake/hashed embedding path anywhere.
"""

from __future__ import annotations

import logging

from .config import Settings

log = logging.getLogger(__name__)


class Embedder:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._backend = settings.embed_backend
        self._client = None  # lazily built
        self._dim: int | None = None

    # ── backend construction ────────────────────────────────────────────

    def _build_server(self):
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(
            model=self.settings.embed_model,
            base_url=self.settings.embed_base_url,
            api_key=self.settings.embed_api_key,
            check_embedding_ctx_length=False,
        )

    def _build_hf(self):
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name=self.settings.hf_embed_model,
            model_kwargs={"device": self.settings.hf_device},
        )

    def _ensure_client(self):
        if self._client is not None:
            return self._client
        if self._backend == "hf":
            self._client = self._build_hf()
        else:
            self._client = self._build_server()
        return self._client

    def _fallback_to_hf(self, err: Exception) -> None:
        log.warning("embed server unreachable (%s); falling back to local HF GPU", err)
        self._backend = "hf"
        self._client = self._build_hf()

    # ── public api ──────────────────────────────────────────────────────

    @property
    def dim(self) -> int:
        if self._dim is None:
            self._dim = len(self.embed_query("dimension probe"))
        return self._dim

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        client = self._ensure_client()
        try:
            vectors = client.embed_documents(texts)
        except Exception as err:  # connection/timeout -> try local GPU once
            if self._backend != "server":
                raise
            self._fallback_to_hf(err)
            vectors = self._client.embed_documents(texts)
        self._dim = len(vectors[0])
        return vectors

    def embed_query(self, text: str) -> list[float]:
        client = self._ensure_client()
        try:
            vector = client.embed_query(text)
        except Exception as err:
            if self._backend != "server":
                raise
            self._fallback_to_hf(err)
            vector = self._client.embed_query(text)
        self._dim = len(vector)
        return vector
