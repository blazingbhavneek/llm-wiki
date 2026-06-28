"""Graph-side reasoning retrieval (LLM-Wiki 'retrieval as reasoning').

This is graph logic, not LLM plumbing: it defines the graph's retrieval tools,
dispatches tool calls to `GraphQuery`, and persists the agent's answer as an
exogenous node. The actual tool-calling loop lives in `llm.AgentClient` — graph
only supplies tools + a dispatch callback and never touches the LLM library.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .models import AgentAnswer, Node, Settings
from .runtime import AGENT_SYSTEM_PROMPT, GraphExogenous, GraphQuery


# region TOOL SCHEMAS
class search(BaseModel):
    """Search the wiki for nodes matching a text query."""

    text: str = Field(description="keywords to search for")


class read(BaseModel):
    """Read a node's full body and metadata by id."""

    node_id: str = Field(description="id of the node to read")


class follow_link(BaseModel):
    """Follow edges from a node to its neighboring nodes."""

    node_id: str = Field(description="id of the node to expand")
    direction: str = Field(default="both", description="'incoming', 'outgoing', or 'both'")


class finish(BaseModel):
    """Provide the final answer and the node ids used as evidence."""

    answer: str = Field(description="the final answer, grounded in node content")
    cited_node_ids: list[str] = Field(
        default_factory=list, description="ids of nodes that support the answer"
    )


_TOOLS = [search, read, follow_link, finish]
# endregion TOOL SCHEMAS


class QueryAgent:
    # region LIFECYCLE
    def __init__(
        self,
        query_api: GraphQuery,
        exogenous: GraphExogenous,
        llm: object,
        settings: Settings,
    ) -> None:
        self.query_api = query_api
        self.exogenous = exogenous
        self.llm = llm
        self.settings = settings

    # endregion LIFECYCLE

    # region PUBLIC API
    def ask(self, question: str, persist: bool = True) -> AgentAnswer:
        override = getattr(self.llm, "run_agent", None)
        if callable(override):
            result = override(self.query_api, question)
            answer = (
                result
                if isinstance(result, AgentAnswer)
                else AgentAnswer.model_validate(result)
            )
            answer.question = question
        else:
            answer = self._run_loop(question)

        if persist and answer.cited_node_ids:
            valid_ids = [
                node_id
                for node_id in answer.cited_node_ids
                if self.query_api.read(node_id) is not None
            ]
            if valid_ids:
                exo = self.exogenous.create_exogenous_node(
                    answer.answer,
                    valid_ids,
                    origin=f"agent:{question[:60]}",
                )
                answer.exogenous_node_id = exo.id
        return answer

    # endregion PUBLIC API

    # region LOOP
    def _run_loop(self, question: str) -> AgentAnswer:
        visited: list[str] = []
        state: dict[str, int] = {"empty_streak": 0}

        def dispatch(name: str, args: dict[str, Any]) -> str:
            return self._dispatch(name, args, visited, state)

        result = self.llm.run_tool_loop(
            AGENT_SYSTEM_PROMPT,
            question,
            _TOOLS,
            dispatch,
            self.settings.agent_max_steps,
        )
        if result.finished_args is not None:
            answer_text = str(result.finished_args.get("answer", "")).strip()
            cited = [node_id for node_id in result.finished_args.get("cited_node_ids", []) if node_id]
        else:
            answer_text = result.content
            cited = []

        return AgentAnswer(
            question=question,
            answer=answer_text,
            cited_node_ids=cited or self._dedupe(visited),
            steps=result.steps,
        )

    # endregion LOOP

    # region DISPATCH
    def _dispatch(
        self,
        name: str,
        args: dict[str, Any],
        visited: list[str],
        state: dict[str, int],
    ) -> str:
        if name == "search":
            nodes = self.query_api.search(str(args.get("text", "")), limit=5)
            visited.extend(node.id for node in nodes)
            if nodes:
                state["empty_streak"] = 0
                return self._format_nodes(nodes)
            state["empty_streak"] += 1
            return self._empty_search_observation(state["empty_streak"])
        if name == "read":
            node = self.query_api.read(str(args.get("node_id", "")))
            if node:
                state["empty_streak"] = 0
                visited.append(node.id)
            return self._format_node_full(node)
        if name == "follow_link":
            pairs = self.query_api.follow_link(
                str(args.get("node_id", "")),
                direction=str(args.get("direction", "both")),
            )
            if pairs:
                state["empty_streak"] = 0
            visited.extend(node.id for _edge, node in pairs)
            return self._format_pairs(pairs)
        return f"unknown tool: {name}"

    def _empty_search_observation(self, streak: int) -> str:
        if streak >= self.settings.agent_patience:
            return (
                f"no nodes found ({streak} consecutive empty searches). "
                "Stop searching now: call finish with the best answer supported "
                "by nodes you already read, citing their ids."
            )
        return "no nodes found"

    # endregion DISPATCH

    # region FORMATTING
    def _format_nodes(self, nodes: list[Node]) -> str:
        if not nodes:
            return "no nodes found"
        return "\n".join(f"- {node.id} | {node.title} | {node.summary}" for node in nodes)

    def _format_node_full(self, node: Node | None) -> str:
        if not node:
            return "node not found"
        return f"id: {node.id}\ntitle: {node.title}\nsummary: {node.summary}\nbody:\n{node.body[:4000]}"

    def _format_pairs(self, pairs) -> str:
        if not pairs:
            return "no neighbors"
        return "\n".join(
            f"- [{edge.label}] {node.id} | {node.title} | {node.summary}"
            for edge, node in pairs
        )

    def _dedupe(self, ids: list[str]) -> list[str]:
        seen: list[str] = []
        for node_id in ids:
            if node_id not in seen:
                seen.append(node_id)
        return seen

    # endregion FORMATTING
