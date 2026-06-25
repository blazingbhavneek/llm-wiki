from __future__ import annotations
import re
from typing import Optional
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain_core.tools import BaseTool as LangChainTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


RunOutput = tuple[str, any]


class AgentClient:

    def __init__(
        self,
        base_url: str,
        api_key: str,
        temperature: float,
        max_output_tokens: Optional[int],
        system_prompt: str,
        model: str,
        tools: list[LangChainTool],
        max_turns: int = 40,
        extra_body: Optional[dict] = None,
    ) -> None:
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.tool_map = {tool.name: tool for tool in tools}

        self.base_llm = ChatOpenAI(          # ← stored for structured-output calls
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=float(temperature),
            max_tokens=int(max_output_tokens) if max_output_tokens else None,
            extra_body=extra_body or {},
        )
        self.llm = self.base_llm.bind_tools(tools)

        self.reset_history()

    async def run(self, prompt: str, output_model: Optional[type[BaseModel]] = None) -> RunOutput:
        if not prompt or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")

        self.message_history.append(HumanMessage(content=prompt))

        for _ in range(self.max_turns):
            try:
                ai_message = await self.llm.ainvoke(self.message_history)
            except Exception as e:
                raise RuntimeError(f"[AgentClient] LLM call failed: {type(e).__name__}: {e}")

            self.message_history.append(ai_message)

            # ✅ Final response (no tool calls)
            if not ai_message.tool_calls:
                content = ai_message.content

                # ✅ Skip empty responses
                if not content or not str(content).strip():
                    continue

                content = str(content).strip()

                if output_model is not None:
                    try:
                        structured_llm = self.base_llm.with_structured_output(output_model)
                        structured_result = await structured_llm.ainvoke(self.message_history)
                        return content, structured_result
                    except Exception as e:
                        raise RuntimeError(f"[AgentClient] Structured parsing failed: {e}")

                return content, content

            # ✅ Tool execution
            for tool_call in ai_message.tool_calls:
                tool_fn = self.tool_map.get(tool_call["name"])
                try:
                    result = (
                        await tool_fn.ainvoke(tool_call["args"])
                        if tool_fn
                        else f"Unknown tool: {tool_call['name']}"
                    )
                except Exception as e:
                    raise RuntimeError(f"[AgentClient] Tool '{tool_call['name']}' failed: {type(e).__name__}: {e}")

                self.message_history.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

        # ✅ MAX TURN FALLBACK (SAFE, NO HALLUCINATION)

        last_content = None

        for m in reversed(self.message_history):
            if isinstance(m, AIMessage):
                content = m.content
                if content and str(content).strip():
                    last_content = str(content).strip()
                    break

        if last_content:
            return last_content, last_content

        raise RuntimeError(
            "[AgentClient] Max turns reached with no valid response. Model failed to produce usable output."
        )
    
    def reset_history(self, system_prompt: Optional[str] = None) -> None:
        if system_prompt is not None:
            self.system_prompt = system_prompt
        self.message_history = [SystemMessage(content=self.system_prompt)]

    @staticmethod
    def _clean_json(text: str) -> str:
        text = text.strip()
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text
