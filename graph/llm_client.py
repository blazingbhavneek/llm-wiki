"""Chat LLM client (OpenAI-compatible, via langchain).

Real operations only: summarize, extract_keywords, suggest_edges, invoke.
Modelled on new/agent_client.py. Imports langchain lazily so the rest of the
package imports without the chat stack installed (tests inject a fake client).
"""

from __future__ import annotations

from typing import Any

from .config import Settings
from .models import ClaimExtraction, EdgeSuggestion, EdgeSuggestions, Keywords, Node
from .prompts import (
    CLAIM_PROMPT,
    EDGE_PROMPT,
    KEYWORD_PROMPT,
    REGENERATE_EXOGENOUS_PROMPT,
    SUMMARY_PROMPT,
    SYSTEM_PROMPT,
)


class LlmClient:
    def __init__(self, settings: Settings, system_prompt: str = SYSTEM_PROMPT) -> None:
        self.settings = settings
        self.system_prompt = system_prompt
        self._llm = None
        self.message_history: list[tuple[str, str]] = [("system", system_prompt)]

    def _chat(self):
        if self._llm is None:
            from langchain_openai import ChatOpenAI

            self._llm = ChatOpenAI(
                model=self.settings.chat_model,
                api_key=self.settings.chat_api_key,
                base_url=self.settings.chat_base_url,
                temperature=self.settings.chat_temperature,
            )
        return self._llm

    def summarize(self, text: str) -> str:
        if not text.strip():
            return ""
        from langchain_core.messages import HumanMessage, SystemMessage

        resp = self._chat().invoke(
            [SystemMessage(content=SUMMARY_PROMPT), HumanMessage(content=text)]
        )
        return str(resp.content or "").strip()

    def extract_keywords(self, text: str) -> list[str]:
        if not text.strip():
            return []
        from langchain_core.messages import HumanMessage, SystemMessage

        structured = self._chat().with_structured_output(Keywords)
        result: Keywords = structured.invoke(
            [SystemMessage(content=KEYWORD_PROMPT), HumanMessage(content=text[:8000])]
        )
        seen: list[str] = []
        for kw in result.keywords:
            kw = kw.strip()
            if kw and kw.lower() not in {s.lower() for s in seen}:
                seen.append(kw)
        return seen[:12]

    def extract_claims(self, text: str) -> ClaimExtraction:
        if not text.strip():
            return ClaimExtraction()
        from langchain_core.messages import HumanMessage, SystemMessage

        structured = self._chat().with_structured_output(ClaimExtraction)
        result: ClaimExtraction = structured.invoke(
            [SystemMessage(content=CLAIM_PROMPT), HumanMessage(content=text[:12000])]
        )
        claims: list[str] = []
        seen: set[str] = set()
        for claim in result.claims:
            claim = " ".join(claim.strip().split())
            key = claim.lower()
            if claim and key not in seen:
                seen.add(key)
                claims.append(claim)
        return ClaimExtraction(
            entity=" ".join(result.entity.strip().split()),
            claims=claims[:20],
        )

    def suggest_edges(self, node: Node, candidates: list[Node]) -> list[EdgeSuggestion]:
        if not candidates:
            return []
        import json

        from langchain_core.messages import HumanMessage, SystemMessage

        payload = {
            "new_node": {
                "id": node.id, "title": node.title, "summary": node.summary,
                "keywords": node.keywords, "body": node.body[:4000],
            },
            "candidates": [
                {"id": c.id, "title": c.title, "summary": c.summary,
                 "keywords": c.keywords, "body": c.body[:1200]}
                for c in candidates
            ],
        }
        structured = self._chat().with_structured_output(EdgeSuggestions)
        result: EdgeSuggestions = structured.invoke(
            [SystemMessage(content=EDGE_PROMPT),
             HumanMessage(content=json.dumps(payload, ensure_ascii=False))]
        )
        allowed = {c.id for c in candidates}
        return [e for e in result.edges if e.target_node_id in allowed]

    def regenerate_exogenous(self, previous: Node, support_nodes: list[Node]) -> str:
        if not support_nodes:
            return ""
        import json

        from langchain_core.messages import HumanMessage, SystemMessage

        payload = {
            "previous_node": {
                "id": previous.id,
                "title": previous.title,
                "summary": previous.summary,
                "body": previous.body[:4000],
            },
            "current_support_material": [
                {
                    "id": node.id,
                    "title": node.title,
                    "summary": node.summary,
                    "body": node.body[:2500],
                }
                for node in support_nodes[:8]
            ],
        }
        resp = self._chat().invoke(
            [
                SystemMessage(content=REGENERATE_EXOGENOUS_PROMPT),
                HumanMessage(content=json.dumps(payload, ensure_ascii=False)),
            ]
        )
        return str(resp.content or "").strip()

    async def invoke(self, prompt: str, output_model: type | None = None) -> tuple[str, Any]:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

        self.message_history.append(("user", prompt))
        role_map = {"system": SystemMessage, "assistant": AIMessage, "user": HumanMessage}
        messages = [role_map[r](content=c) for r, c in self.message_history]
        llm = self._chat()
        resp = await llm.ainvoke(messages)
        raw = str(resp.content or "").strip()
        self.message_history.append(("assistant", raw))
        if output_model is None:
            return raw, raw
        parsed = await llm.with_structured_output(output_model).ainvoke(messages)
        return raw, parsed
