"""Shared chat client with persistent history and retryable one-off queries."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from .base import BaseLlmClient


class LlmClient(BaseLlmClient):
    """Small chat wrapper with persistent history and simple retries."""

    def __init__(
        self,
        model: str,
        base_url: str,
        api_key: str,
        *,
        system_prompt: str = "",
        temperature: float = 0.0,
        timeout: int = 300,
        retry_attempts: int = 3,
        retry_delay_seconds: float = 1.0,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.timeout = timeout
        self.retry_attempts = max(0, retry_attempts)
        self.retry_delay_seconds = max(0.0, retry_delay_seconds)
        self._ensure_endpoint_available()

        from langchain_core.messages import SystemMessage
        from langchain_openai import ChatOpenAI

        self._llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
            timeout=self.timeout,
            # TEMPORARY: disable model thinking for faster ingest. Remove to re-enable.
            # model_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        )
        self.message_history = []
        if system_prompt.strip():
            self.message_history.append(SystemMessage(content=system_prompt))

    def invoke(self, prompt: str) -> str:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("prompt must not be empty")

        from langchain_core.messages import AIMessage, HumanMessage

        user_message = HumanMessage(content=prompt)
        messages = [*self.message_history, user_message]
        reply = self.run_messages(messages)
        self.message_history.append(user_message)
        self.message_history.append(AIMessage(content=reply))
        return reply

    def invoke_structured(self, prompt: str, output_model: type[Any]) -> Any:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("prompt must not be empty")

        from langchain_core.messages import AIMessage, HumanMessage

        user_message = HumanMessage(content=prompt)
        messages = [*self.message_history, user_message]
        result = self.run_messages_structured(messages, output_model)
        self.message_history.append(user_message)
        self.message_history.append(AIMessage(content=self._stringify_output(result)))
        return result

    def run_messages(self, messages: list[Any]) -> str:
        return self._run_with_retries(
            lambda: self._response_text(self._llm.invoke(messages))
        )

    def run_messages_structured(
        self,
        messages: list[Any],
        output_model: type[Any],
    ) -> Any:
        return self._run_with_retries(
            lambda: self._llm.with_structured_output(output_model).invoke(messages)
        )

    def complete(self, system_prompt: str, user_content: str) -> str:
        from langchain_core.messages import HumanMessage, SystemMessage

        return self.run_messages(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_content),
            ]
        )

    def complete_structured(
        self,
        system_prompt: str,
        user_content: str,
        output_model: type[Any],
    ) -> Any:
        from langchain_core.messages import HumanMessage, SystemMessage

        return self.run_messages_structured(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_content),
            ],
            output_model,
        )

    def reset_history(self) -> None:
        from langchain_core.messages import SystemMessage

        self.message_history = []
        if self.system_prompt.strip():
            self.message_history.append(SystemMessage(content=self.system_prompt))

    def _ensure_endpoint_available(self) -> None:
        models_url = self._models_url()
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        request = urllib.request.Request(models_url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, TimeoutError, ValueError, urllib.error.URLError) as exc:
            raise RuntimeError(
                f"LLM endpoint unavailable at {models_url}: {exc}"
            ) from exc

        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise RuntimeError(
                f"LLM endpoint at {models_url} returned an invalid /models payload"
            )

    def _models_url(self) -> str:
        base_url = self.base_url.rstrip("/")
        if base_url.endswith("/v1"):
            return f"{base_url}/models"
        return f"{base_url}/v1/models"

    def _run_with_retries(self, fn) -> Any:
        last_error: Exception | None = None
        for attempt in range(self.retry_attempts + 1):
            try:
                return fn()
            except Exception as exc:  # retry any runtime query failure
                last_error = exc
                if attempt >= self.retry_attempts:
                    break
                time.sleep(self.retry_delay_seconds)
        assert last_error is not None
        raise last_error

    def _response_text(self, response: Any) -> str:
        content = getattr(response, "content", response)
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and isinstance(item.get("text"), str):
                    parts.append(item["text"])
                else:
                    parts.append(str(item))
            return "\n".join(part for part in parts if part).strip()
        return str(content or "").strip()

    def _stringify_output(self, result: Any) -> str:
        if hasattr(result, "model_dump_json"):
            return result.model_dump_json()
        if isinstance(result, (dict, list)):
            return json.dumps(result, ensure_ascii=False)
        return str(result)
