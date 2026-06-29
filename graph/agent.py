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

    def _clean_node_ref(self, value: str) -> str:
        """Clean common LLM-produced node references before exact graph lookup.

        Examples:
        - "`node-id`" -> "node-id"
        - "- node-id | title | summary" -> "node-id"
        - "id: node-id" -> "node-id"
        - "node-id (Some Title)" -> "node-id"
        """
        import re

        text = str(value or "").strip()

        # Remove bullet/list prefix.
        text = re.sub(r"^\s*[-*]\s*", "", text).strip()

        # Remove wrapping quotes/backticks.
        text = text.strip("`'\" \t\r\n")

        # Remove "id:" prefix.
        text = re.sub(r"^id\s*:\s*", "", text, flags=re.IGNORECASE).strip()

        # If the model copied the whole search row, keep only the ID column.
        if "|" in text:
            text = text.split("|", 1)[0].strip()

        # Remove trailing "(title)".
        text = re.sub(r"\s+\([^)]*\)\s*$", "", text).strip()

        # Final cleanup.
        text = text.strip("`'\" \t\r\n,;")

        return text

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

    def _format_node_full_with_request(
        self,
        node: Node | None,
        requested_id: str,
        cleaned_id: str,
    ) -> str:
        if not node:
            return (
                "node not found\n"
                f"requested_id: {requested_id}\n"
                f"cleaned_id: {cleaned_id}"
            )

        note = ""
        if requested_id.strip() != cleaned_id:
            note = (
                f"requested_id: {requested_id}\n"
                f"cleaned_id: {cleaned_id}\n"
            )

        return (
            f"{note}"
            f"id: {node.id}\n"
            f"title: {node.title}\n"
            f"summary: {node.summary}\n"
            f"body:\n{node.body}"
        )

    # region DISPATCH
    def _dispatch(
        self,
        name: str,
        args: dict[str, Any],
        visited: list[str],
        state: dict[str, int],
    ) -> str:
        if name == "search":
            nodes = self.query_api.search(str(args.get("text", "")), limit=10)
            visited.extend(node.id for node in nodes)
            if nodes:
                state["empty_streak"] = 0
                return self._format_nodes(nodes)
            state["empty_streak"] += 1
            return self._empty_search_observation(state["empty_streak"])
        if name == "read":
            requested_id = str(args.get("node_id", ""))
            cleaned_id = self._clean_node_ref(requested_id)

            node = self.query_api.read(cleaned_id)

            if node:
                state["empty_streak"] = 0
                visited.append(node.id)

            return self._format_node_full_with_request(node, requested_id, cleaned_id)
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
        return "\n".join(
            f"- node_id: `{node.id}`\n"
            f"  title: {node.title}\n"
            f"  summary: {node.summary}\n"
            f"  next_action: read this node with read(node_id='{node.id}') if relevant"
            for node in nodes
        )

    def _format_node_full(self, node: Node | None) -> str:
        if not node:
            return "node not found"
        return f"id: {node.id}\ntitle: {node.title}\nsummary: {node.summary}\nbody:\n{node.body}"

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
