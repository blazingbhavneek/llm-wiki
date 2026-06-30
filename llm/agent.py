"""Tool-using LLM client.

`AgentClient` extends `LlmClient` with native tool-calling: it binds tool schemas
to the model and runs a bounded reason-act loop, dispatching each tool call back
to a caller-supplied callback. It is the only place that knows the LLM library's
tool-call message shape; callers receive a neutral `ToolLoopResult`.
"""

from __future__ import annotations

from typing import Any, Callable

from pydantic import BaseModel

from .llm import LlmClient


class ToolLoopResult(BaseModel):
    """Neutral result of a tool loop. No LLM-library types cross this boundary."""

    finished_args: dict[str, Any] | None = (
        None  # args of the terminal finish tool, if called
    )
    content: str = ""  # free-text answer when the model stops without finish
    steps: int = 0


class AgentClient(LlmClient):
    """LLM client that can bind tools and drive a reason-act loop."""

    def run_tools(self, messages: list[Any], tools: list[Any]) -> Any:
        """Bind tools and invoke once; returns the raw library AI message."""
        bound = self._llm.bind_tools(tools)
        return self._run_with_retries(lambda: bound.invoke(messages))

    def run_tool_loop(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: list[Any],
        dispatch: Callable[[str, dict[str, Any]], str],
        max_steps: int,
        finish_tool: str = "finish",
        finish_guard: Callable[[dict[str, Any]], str | None] | None = None,
    ) -> ToolLoopResult:
        """Loop: model picks tools, `dispatch` runs them, until finish/no-call/cap.

        `dispatch(name, args) -> observation_text` is supplied by the caller and is
        the only domain-aware part; this client stays domain-agnostic.

        `finish_guard(args) -> reason | None` (optional) can VETO an early finish:
        if it returns a reason string, finish is rejected, the reason is fed back
        as a tool observation, and the loop continues (still bounded by max_steps).
        """
        from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

        messages: list[Any] = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        steps = 0
        for _ in range(max(1, max_steps)):
            steps += 1
            ai = self.run_tools(messages, tools)
            messages.append(ai)
            tool_calls = getattr(ai, "tool_calls", None) or []
            if not tool_calls:
                return ToolLoopResult(content=self._response_text(ai), steps=steps)
            finished: dict[str, Any] | None = None
            for call in tool_calls:
                name = call.get("name")
                args = call.get("args") or {}
                if name == finish_tool:
                    reason = finish_guard(args) if finish_guard else None
                    if reason:
                        messages.append(
                            ToolMessage(content=reason, tool_call_id=call.get("id"))
                        )
                        continue
                    finished = args
                    break
                observation = dispatch(name, args)
                messages.append(
                    ToolMessage(content=observation, tool_call_id=call.get("id"))
                )
            if finished is not None:
                return ToolLoopResult(finished_args=finished, steps=steps)

        return ToolLoopResult(content="", steps=steps)
