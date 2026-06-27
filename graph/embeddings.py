"""Real embeddings.

Default backend talks to an OpenAI-compatible embedding server.

At init time, if the configured embedding server is unavailable, this falls back
once to a local HuggingFace model on the configured device.

After init, embedding errors are not swallowed:
- context length errors bubble up
- bad requests bubble up
- runtime/model errors bubble up

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
        self._client = None
        self._dim: int | None = None

        # Do availability decision once, up front.
        self._initialize_backend()

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

    # ── initialization / fallback ───────────────────────────────────────

    def _initialize_backend(self) -> None:
        """Build the selected backend.

        If the configured backend is the embedding server, probe it immediately.
        If the probe fails, switch once to local HugFace.

        After this method completes, normal embedding calls do not fallback.
        """

        if self._backend == "hf":
            log.info(
                "using local HF embedding backend: model=%s device=%s",
                self.settings.hf_embed_model,
                self.settings.hf_device,
            )
            self._client = self._build_hf()
            return

        if self._backend != "server":
            raise ValueError(
                f"unsupported embed_backend={self._backend!r}; expected 'server' or 'hf'"
            )

        self._client = self._build_server()

        try:
            vector = self._client.embed_query("embedding server availability probe")
            self._dim = len(vector)
            log.info(
                "embedding server available: model=%s dim=%s base_url=%s",
                self.settings.embed_model,
                self._dim,
                self.settings.embed_base_url,
            )
        except Exception as err:
            self._fallback_to_hf(err)

    def _fallback_to_hf(self, err: Exception) -> None:
        log.warning(
            "embedding server unavailable during startup probe (%s); "
            "falling back to local HF backend: model=%s device=%s",
            err,
            self.settings.hf_embed_model,
            self.settings.hf_device,
        )

        self._backend = "hf"
        self._client = self._build_hf()

        # Optional but useful: probe HF once too, so dim is known early.
        vector = self._client.embed_query("local HF embedding availability probe")
        self._dim = len(vector)

        log.info(
            "local HF embedding backend ready: model=%s dim=%s device=%s",
            self.settings.hf_embed_model,
            self._dim,
            self.settings.hf_device,
        )

    def _ensure_client(self):
        if self._client is None:
            self._initialize_backend()
        return self._client

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

        # No runtime fallback here.
        # If the server/HF backend throws context-length, bad request, CUDA, etc.,
        # let the caller handle it.
        vectors = client.embed_documents(texts)

        if vectors:
            self._dim = len(vectors[0])

        return vectors

    def embed_query(self, text: str) -> list[float]:
        client = self._ensure_client()

        # No runtime fallback here.
        # Context-length errors now bubble up to DomainEngine or caller.
        vector = client.embed_query(text)

        self._dim = len(vector)
        return vector
