"""Optional LLM client, mirroring md.py's OpenAI-compatible setup.

The graph layer degrades gracefully when no server is reachable: structural
ingest (document/page/topic nodes, contains/has_topic edges, FTS indexing) is
fully deterministic and needs no LLM. Only synthetic-node authoring and richer
concept extraction call out here, and they no-op when `available` is False.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional


class LLMClient:
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.2,
        timeout: int = 300,
    ):
        self.model = model or os.environ.get("WIKI_MODEL", "gemma4")
        self.base_url = base_url or os.environ.get(
            "OPENAI_BASE_URL", "http://localhost:8000/v1"
        )
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "local")
        self.temperature = temperature
        self.timeout = timeout
        self._llm: Any = None

    @property
    def available(self) -> bool:
        try:
            self._ensure()
            return True
        except Exception:
            return False

    def _ensure(self) -> Any:
        if self._llm is None:
            from langchain_openai import ChatOpenAI  # lazy

            self._llm = ChatOpenAI(
                model=self.model,
                base_url=self.base_url,
                api_key=self.api_key,
                temperature=self.temperature,
                timeout=self.timeout,
                max_tokens=64000,
            )
        return self._llm

    def complete(self, system: str, user: str) -> str:
        from langchain_core.messages import HumanMessage, SystemMessage  # lazy

        llm = self._ensure()
        resp = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
        return resp.content if hasattr(resp, "content") else str(resp)

    def complete_json(self, system: str, user: str) -> Any:
        text = self.complete(
            system + "\nReturn ONLY valid JSON, no fences, no prose.", user
        )
        return _extract_json(text)


def _extract_json(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lstrip().lower().startswith("json"):
            text = text.lstrip()[4:]
    start = text.find("{")
    arr = text.find("[")
    if arr != -1 and (start == -1 or arr < start):
        start = arr
    if start == -1:
        return None
    depth = 0
    open_ch = text[start]
    close_ch = "}" if open_ch == "{" else "]"
    for i in range(start, len(text)):
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None
