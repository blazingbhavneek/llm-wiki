"""Deterministic, offline fakes for tests.

These are TEST doubles (not production stubs): a bag-of-words embedder so KNN is
meaningful, and a rule-based LLM so edge/keyword/summary paths run without a
server. Production code uses the real Embedder / LlmClient.
"""

from __future__ import annotations

import math
import re

from ..models import AgentAnswer, ClaimExtraction, EdgeSuggestion, EntityMatch, Node

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

    def embed_document(self, text: str) -> list[float]:
        return self.embed_query(text)


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
        label = "contradicts" if "contradicts" in _tokens(node.body) else "related"
        out: list[EdgeSuggestion] = []
        for c in candidates:
            if node_kw & set(c.keywords):
                out.append(EdgeSuggestion(
                    target_node_id=c.id, label=label,
                    summary="shares keywords",
                ))
        return out

    def check_entity_duplicate(self, node: Node, candidates: list[Node]) -> EntityMatch:
        if node.entity:
            for c in candidates:
                if c.entity and c.entity == node.entity:
                    return EntityMatch(is_same=True, target_node_id=c.id)
        return EntityMatch(is_same=False)

    def run_agent(self, query_api: object, question: str) -> AgentAnswer:
        hits = query_api.search(question, limit=5)
        cited = [hits[0].id] if hits else []
        answer = f"answer grounded in {cited[0]}" if cited else "no information found"
        return AgentAnswer(
            question=question, answer=answer, cited_node_ids=cited, steps=1
        )

    def regenerate_exogenous(self, previous: Node, support_nodes: list[Node]) -> str:
        support_text = "\n".join(node.body for node in support_nodes)
        return f"regenerated from current supports\n{support_text}".strip()
