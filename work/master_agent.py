from __future__ import annotations
import asyncio
import json
import re
from typing import Optional
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool, BaseTool as LangChainTool
from langchain_openai import ChatOpenAI
from .agent_client import AgentClient
from .prompts import SPECIALIST_PROMPT

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

def build_specialist_memory(
    persist_directory: str,
    embedding_backend: str = "huggingface",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    embedding_base_url: Optional[str] = None,
    embedding_api_key: Optional[str] = "EMPTY",
    collection_name: str = "specialist_cache",
):
    if embedding_backend == "huggingface":
        embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cuda:0"},
        )
    else:
        embeddings = OpenAIEmbeddings(
            model=embedding_model,
            base_url=embedding_base_url,
            api_key=embedding_api_key,
        )

    vectorstore = Chroma(
        persist_directory=persist_directory,
        collection_name=collection_name,
        embedding_function=embeddings,
    )

    return vectorstore

class MasterAgent:
    """
    Master agent that delegates all library lookups to disposable specialist
    sub-agents. Never touches MCP/RAG directly.

    Tool set exposed to the master LLM:
      - ask_specialists(questions: list[str]) — parallel specialist fan-out
      - any extra_tools passed in (e.g. verify_code)

    Optional sliding-window summarization for long-running masters (b3/b4).
    """

    def __init__(
        self,
        system_prompt: str,
        model: str,
        base_url: str,
        api_key: str,
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = None,
        max_turns: int = 10,
        specialist_tools: list[LangChainTool] | None = None,
        specialist_model: str | None = None,
        specialist_base_url: str | None = None,
        specialist_api_key: str | None = None,
        specialist_temperature: float = 0.7,
        specialist_max_turns: int = 5,
        specialist_max_output_tokens: Optional[int] = None,
        extra_tools: list[LangChainTool] | None = None,
        enable_summarization: bool = False,
        summarize_token_limit: int = 48000,
        summarize_target: int = 16000,
        extra_body: Optional[dict] = None,
    ):
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.enable_summarization = enable_summarization
        self.summarize_token_limit = summarize_token_limit
        self.summarize_target = summarize_target
        self.extra_body = extra_body or {}

        self.specialist_tools = specialist_tools or []
        self.specialist_model = specialist_model or model
        self.specialist_base_url = specialist_base_url or base_url
        self.specialist_api_key = specialist_api_key or api_key
        self.specialist_temperature = specialist_temperature
        self.specialist_max_turns = specialist_max_turns
        self.specialist_max_output_tokens = specialist_max_output_tokens

        # ✅ Specialist memory (Chroma cache)
        self.memory = build_specialist_memory(
            persist_directory="logs/chroma_specialist_cache",
            embedding_backend="server",
            embedding_model="cl-nagoya/ruri-v3-310m",
            embedding_base_url="http://10.160.144.101:51025/v1"
        )

        @tool
        async def ask_specialists(questions: list[str]) -> str:
            """Ask a list of questions to specialist agents who have full access
            to the library MCP server, RAG, and documentation.
            All questions are answered in parallel by separate specialists.
            Each specialist is thorough — expect detailed, structured answers.
            Use this whenever you need function signatures, error codes, types,
            preconditions, cleanup requirements, or any library detail.

            Ask at most 3 questions at a time. But Keep them detailed, asking long questions is ok.

            Args:
                questions: List of specific questions about the library.
                        Be precise — one focused question per item.
            """
            return await self._run_specialists(questions)

        self._ask_specialists_tool = ask_specialists

        master_tools: list[LangChainTool] = [ask_specialists]
        if extra_tools:
            master_tools.extend(extra_tools)

        self.tool_map = {t.name: t for t in master_tools}

        self.base_llm = ChatOpenAI(  # ← stored for structured-output calls
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=float(temperature),
            max_tokens=int(max_output_tokens) if max_output_tokens else None,
            extra_body=self.extra_body,
        )
        self.llm = self.base_llm.bind_tools(master_tools)

        self.summarize_llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=0.1,
            max_tokens=4096,
            extra_body=self.extra_body,
        )

        self.message_history: list = []
        self.reset_history()

    async def run(
        self,
        prompt: str,
        output_model: Optional[type[BaseModel]] = None,
    ) -> tuple[str, any]:
        self.message_history.append(HumanMessage(content=prompt))

        last_content = ""
        for _ in range(self.max_turns):
            await self.maybe_summarize()

            try:
                ai_message = await self.llm.ainvoke(self.message_history)
                self.message_history.append(ai_message)
            except Exception as e:
                # Handle all LLM API errors (connection, timeout, rate limit)
                error_msg = f"[LLM API ERROR] {type(e).__name__}: {e}"
                if output_model is not None:
                    return error_msg, None
                return error_msg, error_msg

            if ai_message.content:
                last_content = str(ai_message.content)

            if not ai_message.tool_calls:
                content = str(ai_message.content)
                if output_model is not None:
                    structured_llm = self.base_llm.with_structured_output(
                        output_model, strict=False
                    )
                    try:
                        structured_result = await structured_llm.ainvoke(
                            self.message_history
                        )
                        return last_content, structured_result
                    except Exception:
                        return last_content, None
                return content, content

            for tc in ai_message.tool_calls:
                tool_fn = self.tool_map.get(tc["name"])
                try:
                    result = (
                        await tool_fn.ainvoke(tc["args"])
                        if tool_fn
                        else f"Unknown tool: {tc['name']}"
                    )
                except Exception as e:
                    result = f"Tool error: {type(e).__name__}: {e}"

                self.message_history.append(
                    ToolMessage(content=str(result), tool_call_id=tc["id"])
                )

        # ── Exhausted turns: return last known AI content ─────────────────

        if output_model is not None:
            structured_llm = self.base_llm.with_structured_output(
                output_model, strict=False
            )
            try:
                structured_result = await structured_llm.ainvoke(self.message_history)
                return last_content, structured_result
            except Exception:
                return last_content, None
        else:
            return last_content, last_content

    # ── History ────────────────────────────────────────────────────────

    def reset_history(self, system_prompt: Optional[str] = None) -> None:
        if system_prompt is not None:
            self.system_prompt = system_prompt
        self.message_history = [SystemMessage(content=self.system_prompt)]

    def _estimate_tokens(self) -> int:
        total = 0
        for m in self.message_history:
            content = m.content if isinstance(m.content, str) else json.dumps(m.content)
            total += len(content) // 3
        return total

    # ── Optional summarization ─────────────────────────────────────────

    async def maybe_summarize(self) -> None:
        if not self.enable_summarization:
            return
        if self._estimate_tokens() < self.summarize_token_limit:
            return

        system = self.message_history[0]
        rest = self.message_history[1:]

        keep_recent = 6
        if len(rest) <= keep_recent:
            return

        to_summarize = rest[:-keep_recent]
        recent = rest[-keep_recent:]

        formatted = []
        for m in to_summarize:
            role = type(m).__name__.replace("Message", "")
            content = m.content if isinstance(m.content, str) else json.dumps(m.content)
            if len(content) > 3000:
                content = content[:3000] + "\n...[truncated]"
            formatted.append(f"[{role}]: {content}")

        summary_prompt = (
            "Summarize the key findings from this research session.\n"
            "Be DENSE. Preserve ALL:\n"
            "- Function names and exact signatures\n"
            "- Error code names and exact values\n"
            "- Parameter types and correct ordering\n"
            "- Preconditions and cleanup requirements\n"
            "- Warnings, threading constraints, deprecated flags\n"
            "- Any code written and compiler errors encountered\n\n"
            + "\n".join(formatted)
        )

        summary_msg = await self.summarize_llm.ainvoke(
            [HumanMessage(content=summary_prompt)]
        )

        self.message_history = [
            system,
            SystemMessage(content=f"[PRIOR RESEARCH SUMMARY]\n{summary_msg.content}"),
            *recent,
        ]


    async def _run_single_specialist(self, question: str) -> str:
        if not question or not question.strip():
            raise ValueError("Empty question passed to specialist")

        # ── 1. Retrieval (MMR) ──
        try:
            retriever = self.memory.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": 5,
                    "fetch_k": 10,
                    "lambda_mult": 0.7,
                },
            )
            docs = retriever.invoke(question)
        except Exception as e:
            raise RuntimeError(f"[Specialist] Retrieval failed: {type(e).__name__}: {e}")

        candidates = [d.page_content for d in docs if d.page_content]

        # ── 2. Judge retrieved answers ──
        if candidates:
            combined = "\n\n---\n\n".join(candidates)

            judge_prompt = f"""
    You are a strict judge.

    QUESTION:
    {question}

    CANDIDATE ANSWERS:
    {combined}

    Do these answers sufficiently and correctly answer the question for practical coding purposes?

    Answer ONLY:
    YES or NO
    """
            try:
                resp = await self.base_llm.ainvoke([HumanMessage(content=judge_prompt)])
                decision = str(resp.content) if resp.content else ""
            except Exception as e:
                raise RuntimeError(f"[Specialist] Retrieval judge failed: {type(e).__name__}: {e}")

            if "YES" in decision.upper():
                return combined

        # ── 3. Fallback to agent ──
        agent = AgentClient(
            base_url=self.specialist_base_url,
            api_key=self.specialist_api_key,
            temperature=self.specialist_temperature,
            max_output_tokens=self.specialist_max_output_tokens,
            system_prompt=SPECIALIST_PROMPT,
            model=self.specialist_model,
            tools=self.specialist_tools,
            max_turns=self.specialist_max_turns,
            extra_body=self.extra_body,
        )

        try:
            raw, answer = await agent.run(question)
        except Exception as e:
            raise RuntimeError(f"[Specialist] Agent execution failed: {e}")

        # ✅ Safe fallback
        final_answer = None
        if answer and str(answer).strip():
            final_answer = str(answer).strip()
        elif raw and str(raw).strip():
            final_answer = str(raw).strip()
        else:
            raise RuntimeError("[Specialist] Agent returned empty response")

        # ── 4. Validate answer ──
        judge_prompt = f"""
    You are a strict validator.

    QUESTION:
    {question}

    ANSWER:
    {final_answer}

    Does this sufficiently and correctly answer the question?

    Answer ONLY:
    YES or NO
    """

        try:
            resp = await self.base_llm.ainvoke([HumanMessage(content=judge_prompt)])
            decision = str(resp.content) if resp.content else ""
            good = "YES" in decision.upper()
        except Exception as e:
            raise RuntimeError(f"[Specialist] Validation failed: {type(e).__name__}: {e}")

        # ── 5. Store if valid ──
        if good:
            try:
                doc = Document(
                    page_content=f"Q: {question}\nA: {final_answer}",
                    metadata={"type": "qa_cache"},
                )
                self.memory.add_documents([doc])
            except Exception as e:
                raise RuntimeError(f"[Specialist] Storage failed: {type(e).__name__}: {e}")

        return f"Q: {question}\nA: {final_answer}"


    async def _run_specialists(self, questions: list[str]) -> str:
        if not questions:
            raise ValueError("No questions provided to _run_specialists")

        results = await asyncio.gather(
            *[self._run_single_specialist(q) for q in questions],
            return_exceptions=True,
        )

        combined = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                combined.append(
                    f"Q: {questions[i]}\nA: [ERROR: {type(result).__name__}: {result}]"
                )
            else:
                combined.append(str(result))

        return "\n\n---\n\n".join(combined)

    # ── Main run loop ──────────────────────────────────────────────────

    @staticmethod
    def _clean_json(text: str) -> str:
        text = text.strip()
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text
