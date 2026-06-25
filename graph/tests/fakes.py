"""Deterministic, offline fakes for tests.

These are TEST doubles (not production stubs): a bag-of-words embedder so KNN is
meaningful, and a rule-based LLM so edge/keyword/summary paths run without a
server. Production code uses the real Embedder / LlmClient.
"""

from __future__ import annotations

import math
import re

from ..models import ClaimExtraction, EdgeSuggestion, Node

_TOKEN = re.compile(r"[a-z0-9]+")
_DIM = 64


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class FakeEmbedder:
    """Hashing bag-of-words vector; shared words -> high cosine similarity."""

    dim = _DIM

    def embed_query(self, text: str) -> list[float]:
        vec = [0.0] * _DIM
        for tok in _tokens(text):
            vec[hash(tok) % _DIM] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]


class FakeLlm:
    def summarize(self, text: str) -> str:
        first = text.strip().splitlines()[0] if text.strip() else ""
        return first[:160]

    def extract_keywords(self, text: str) -> list[str]:
        seen: list[str] = []
        for tok in _tokens(text):
            if len(tok) > 3 and tok not in seen:
                seen.append(tok)
        return seen[:12]

    def extract_claims(self, text: str) -> ClaimExtraction:
        tokens = [tok for tok in _tokens(text) if len(tok) > 3]
        entity = tokens[0] if tokens else ""
        claims: list[str] = []
        for part in re.split(r"[.\n]+", text):
            claim = " ".join(_tokens(part))
            if claim and claim not in claims:
                claims.append(claim)
        return ClaimExtraction(entity=entity, claims=claims[:20])

    def suggest_edges(self, node: Node, candidates: list[Node]) -> list[EdgeSuggestion]:
        node_kw = set(node.keywords)
        out: list[EdgeSuggestion] = []
        for c in candidates:
            if node_kw & set(c.keywords):
                out.append(EdgeSuggestion(
                    target_node_id=c.id, label="related",
                    summary="shares keywords",
                ))
        return out

    def regenerate_exogenous(self, previous: Node, support_nodes: list[Node]) -> str:
        support_text = "\n".join(node.body for node in support_nodes)
        return f"regenerated from current supports\n{support_text}".strip()
