from __future__ import annotations

import json
import sys
import types
from urllib.error import URLError

import pytest

from llm.llm import LlmClient


class _FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _FakeSystemMessage(_FakeMessage):
    pass


class _FakeHumanMessage(_FakeMessage):
    pass


class _FakeAIMessage(_FakeMessage):
    pass


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


def _install_fake_langchain(monkeypatch: pytest.MonkeyPatch, chat_cls: type) -> None:
    messages_module = types.ModuleType("langchain_core.messages")
    messages_module.AIMessage = _FakeAIMessage
    messages_module.HumanMessage = _FakeHumanMessage
    messages_module.SystemMessage = _FakeSystemMessage

    core_module = types.ModuleType("langchain_core")
    core_module.messages = messages_module

    openai_module = types.ModuleType("langchain_openai")
    openai_module.ChatOpenAI = chat_cls

    monkeypatch.setitem(sys.modules, "langchain_core", core_module)
    monkeypatch.setitem(sys.modules, "langchain_core.messages", messages_module)
    monkeypatch.setitem(sys.modules, "langchain_openai", openai_module)


def test_llm_client_checks_models_and_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeChatOpenAI:
        instances: list["FakeChatOpenAI"] = []

        def __init__(self, **_: object) -> None:
            self.calls = 0
            FakeChatOpenAI.instances.append(self)

        def invoke(self, messages: list[_FakeMessage]) -> object:
            self.calls += 1
            assert messages[0].content == "system"
            if self.calls < 3:
                raise RuntimeError("temporary connection error")
            return types.SimpleNamespace(content="ok")

        def with_structured_output(self, output_model: type[object]) -> object:
            raise AssertionError(f"unexpected structured call for {output_model}")

    _install_fake_langchain(monkeypatch, FakeChatOpenAI)
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout=0: _FakeResponse({"data": [{"id": "fake-model"}]}),
    )
    monkeypatch.setattr("llm.llm.time.sleep", lambda seconds: None)

    client = LlmClient(
        model="fake-model",
        base_url="http://example.test/v1",
        api_key="local",
        system_prompt="system",
    )

    reply = client.invoke("hello")

    assert reply == "ok"
    assert FakeChatOpenAI.instances[0].calls == 3
    assert [message.content for message in client.message_history] == ["system", "hello", "ok"]


def test_llm_client_fails_fast_when_models_check_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout=0: (_ for _ in ()).throw(URLError("offline")),
    )

    with pytest.raises(RuntimeError, match="LLM endpoint unavailable"):
        LlmClient(
            model="fake-model",
            base_url="http://example.test/v1",
            api_key="local",
            system_prompt="system",
        )
