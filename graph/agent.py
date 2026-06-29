"""Graph-side reasoning retrieval (LLM-Wiki 'retrieval as reasoning').

This is graph logic, not LLM plumbing: it defines the graph's retrieval tools,
dispatches tool calls to `GraphQuery`, orchestrates a lead agent + a team of
exploration subagents, and persists the answer as an exogenous node. The actual
tool-calling loop lives in `llm.AgentClient` — graph only supplies tools + a
dispatch callback and never touches the LLM library.

Separation of concerns:
- The LEAD agent has `search` (to surface candidates) and `explore` (to hand
  disjoint starting nodes to subagents); it cannot read node bodies itself.
- Each SUBAGENT has `search`, `read`, and `follow_link`; it explores one region
  from its assigned starting node and reports findings back to the lead.
Subagents run concurrently (capped by `subagent_concurrency`), each on its own
read-only DB connection so the engine's thread-bound connection is never shared.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from pydantic import BaseModel, Field

from db import Database

from .mermaid import MERMAID_INSTRUCTION, repair_answer_mermaid
from .models import AgentAnswer, Node, Settings
from .runtime import (
    MAIN_AGENT_SYSTEM_PROMPT,
    SUBAGENT_SYSTEM_PROMPT,
    GraphExogenous,
    GraphQuery,
    GraphRuntime,
)


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


class explore(BaseModel):
    """Hand distinct starting node ids to a team of exploration subagents."""

    node_ids: list[str] = Field(
        default_factory=list,
        description="distinct starting node ids, each exploring a different sub-topic",
    )


class finish(BaseModel):
    """Provide the final answer and the node ids used as evidence."""

    answer: str = Field(description="the final answer, grounded in node content")
    cited_node_ids: list[str] = Field(
        default_factory=list, description="ids of nodes that support the answer"
    )


_MAIN_TOOLS = [search, explore, finish]
_SUBAGENT_TOOLS = [search, read, follow_link, finish]
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
        # Progress sink for step-level streaming; replaced per-ask. No-op default
        # keeps the non-streaming path (and tests) unchanged.
        self._emit: Callable[[dict[str, Any]], None] = lambda event: None

    # endregion LIFECYCLE

    def _ev(self, event_type: str, **fields: Any) -> None:
        try:
            self._emit({"type": event_type, **fields})
        except Exception:  # noqa: BLE001 - progress events must never break a run
            pass

    @staticmethod
    def _node_ref(node: Node) -> dict[str, str]:
        return {"id": node.id, "title": node.title or node.entity or node.id}

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
    def ask(
        self,
        question: str,
        persist: bool = True,
        on_event: Callable[[dict[str, Any]], None] | None = None,
    ) -> AgentAnswer:
        self._emit = on_event or (lambda event: None)
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

        # Validate + repair any mermaid the compiler emitted, before it is shown
        # or persisted. Gated by the flag so the default path is untouched.
        if self.settings.enable_mermaid and answer.answer:
            answer.answer = repair_answer_mermaid(
                answer.answer, self.llm, self.settings, self._emit
            )

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

    # region LEAD LOOP
    def _run_loop(self, question: str) -> AgentAnswer:
        # Evidence the subagents actually grounded their reports in; used as the
        # citation fallback if the lead finishes without explicit cited ids.
        evidence: list[str] = []

        def dispatch(name: str, args: dict[str, Any]) -> str:
            return self._dispatch_main(name, args, question, evidence)

        system_prompt = MAIN_AGENT_SYSTEM_PROMPT
        if self.settings.enable_mermaid:
            system_prompt += MERMAID_INSTRUCTION

        result = self.llm.run_tool_loop(
            system_prompt,
            question,
            _MAIN_TOOLS,
            dispatch,
            self.settings.agent_max_steps,
        )
        self._ev("compiling")
        if result.finished_args is not None:
            answer_text = str(result.finished_args.get("answer", "")).strip()
            cited = [node_id for node_id in result.finished_args.get("cited_node_ids", []) if node_id]
        else:
            answer_text = result.content
            cited = []

        return AgentAnswer(
            question=question,
            answer=answer_text,
            cited_node_ids=cited or self._dedupe(evidence),
            steps=result.steps,
        )

    def _dispatch_main(
        self,
        name: str,
        args: dict[str, Any],
        question: str,
        evidence: list[str],
    ) -> str:
        if name == "search":
            query = str(args.get("text", ""))
            self._ev("search", phase="main", query=query)
            nodes = self.query_api.search(query, limit=self.settings.rerank_top_k)
            if not nodes:
                self._ev("candidates", count=0, nodes=[])
                return "no nodes found"
            self._ev(
                "candidates",
                count=len(nodes),
                nodes=[self._node_ref(node) for node in nodes],
            )
            return self._format_candidates(nodes)
        if name == "explore":
            return self._run_subagents(args.get("node_ids", []), question, evidence)
        return f"unknown tool: {name}"

    # endregion LEAD LOOP

    # region SUBAGENT ORCHESTRATION
    def _run_subagents(
        self,
        raw_node_ids: list[Any],
        question: str,
        evidence: list[str],
    ) -> str:
        """Resolve distinct starting nodes, run a disjoint exploration team."""
        starts = self._resolve_distinct_starts(raw_node_ids)
        if not starts:
            return (
                "no valid starting nodes resolved from those ids. Search again and "
                "pass exact node ids from the search results to explore."
            )

        assignments = [
            (start, [other for other in starts if other != start])
            for start in starts
        ]

        start_nodes = [self.query_api.read(start) for start in starts]
        self._ev(
            "subagents_spawned",
            starts=[self._node_ref(node) for node in start_nodes if node],
        )

        max_workers = max(1, self.settings.subagent_concurrency)
        reports: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [
                pool.submit(self._run_one_subagent, start, siblings, question, agent)
                for agent, (start, siblings) in enumerate(assignments, start=1)
            ]
            for future in futures:
                try:
                    reports.append(future.result())
                except Exception as exc:  # noqa: BLE001 - one subagent failing is non-fatal
                    reports.append(
                        {"start": "?", "answer": f"(subagent failed: {exc})", "cited": []}
                    )

        for report in reports:
            for node_id in report.get("cited", []):
                evidence.append(node_id)

        return self._format_reports(reports)

    def _resolve_distinct_starts(self, raw_node_ids: list[Any]) -> list[str]:
        """Clean, resolve and de-duplicate starting ids, capped at subagent_count."""
        resolved: list[str] = []
        seen: set[str] = set()
        for raw in raw_node_ids or []:
            node = self.query_api.read(self._clean_node_ref(str(raw)))
            if node and node.id not in seen:
                seen.add(node.id)
                resolved.append(node.id)
            if len(resolved) >= self.settings.subagent_count:
                break
        return resolved

    def _run_one_subagent(
        self,
        start_id: str,
        sibling_ids: list[str],
        question: str,
        agent: int,
    ) -> dict[str, Any]:
        """Run one subagent on its own read-only DB connection (thread-safe)."""
        database = Database(self.settings.database_path)
        try:
            runtime = GraphRuntime(
                database, self.query_api.embedder, self.llm, self.settings, subagent=True
            )
            sub_query = GraphQuery(
                database,
                self.query_api.embedder,
                self.settings,
                runtime,
                reranker=self.query_api.reranker,
            )

            # Read via THIS subagent's own connection (we are on a worker thread;
            # the engine's connection is thread-bound and must not be touched here).
            start_node = sub_query.read(start_id)
            if start_node is not None:
                self._ev("subagent_start", agent=agent, node=self._node_ref(start_node))

            visited: list[str] = []
            state: dict[str, Any] = {"empty_streak": 0, "read_ids": set()}

            def dispatch(name: str, args: dict[str, Any]) -> str:
                return self._dispatch_tools(sub_query, name, args, visited, state, agent)

            def finish_guard(_args: dict[str, Any]) -> str | None:
                read_count = len(state["read_ids"])
                if read_count < self.settings.subagent_min_reads:
                    return (
                        f"You have read only {read_count} node(s); read at least "
                        f"{self.settings.subagent_min_reads} before finishing. Read "
                        "another relevant node in your region now."
                    )
                return None

            siblings = ", ".join(sibling_ids) if sibling_ids else "(none)"
            user_prompt = (
                f"Question: {question}\n\n"
                f"Your assigned starting node: {start_id}\n"
                f"Sibling agents are covering (do NOT explore these): {siblings}\n\n"
                "Read your starting node first, then follow links / search within your "
                "region. Report what this region says about the question."
            )

            result = self.llm.run_tool_loop(
                SUBAGENT_SYSTEM_PROMPT,
                user_prompt,
                _SUBAGENT_TOOLS,
                dispatch,
                self.settings.subagent_max_steps,
                finish_guard=finish_guard,
            )

            if result.finished_args is not None:
                answer = str(result.finished_args.get("answer", "")).strip()
                cited = [
                    node_id
                    for node_id in result.finished_args.get("cited_node_ids", [])
                    if node_id
                ]
            else:
                answer = result.content
                cited = []

            cited = cited or self._dedupe(visited)
            self._ev("subagent_done", agent=agent, cited=cited)
            return {
                "start": start_id,
                "answer": answer or "(no findings)",
                "cited": cited,
            }
        finally:
            database.close()

    def _format_reports(self, reports: list[dict[str, Any]]) -> str:
        blocks = ["Subagent reports (each explored a different region):"]
        for index, report in enumerate(reports, start=1):
            cited = ", ".join(report.get("cited", [])) or "(none)"
            blocks.append(
                f"\n### Subagent {index} — start node: {report.get('start')}\n"
                f"{report.get('answer', '').strip()}\n"
                f"Evidence node ids: {cited}"
            )
        return "\n".join(blocks)

    # endregion SUBAGENT ORCHESTRATION

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

    # region SUBAGENT DISPATCH
    def _dispatch_tools(
        self,
        query_api: GraphQuery,
        name: str,
        args: dict[str, Any],
        visited: list[str],
        state: dict[str, Any],
        agent: int,
    ) -> str:
        if name == "search":
            query = str(args.get("text", ""))
            self._ev("search", phase="sub", agent=agent, query=query)
            nodes = query_api.search(query, limit=self.settings.rerank_top_k)
            visited.extend(node.id for node in nodes)
            if nodes:
                state["empty_streak"] = 0
                return self._format_nodes(nodes)
            state["empty_streak"] += 1
            return self._empty_search_observation(state["empty_streak"])
        if name == "read":
            requested_id = str(args.get("node_id", ""))
            cleaned_id = self._clean_node_ref(requested_id)

            node = query_api.read(cleaned_id)

            if node:
                read_ids: set[str] = state["read_ids"]
                # Already read: don't re-emit, don't re-count — break read loops.
                if node.id in read_ids:
                    return (
                        f"already read {node.id} ({node.title}). Pick a DIFFERENT "
                        "node, follow a link, or finish."
                    )
                # New read past the ceiling: stop expanding this region.
                if len(read_ids) >= self.settings.subagent_max_reads:
                    return (
                        f"read budget reached ({len(read_ids)}/"
                        f"{self.settings.subagent_max_reads} nodes). Call finish now "
                        "with what you have gathered."
                    )
                state["empty_streak"] = 0
                read_ids.add(node.id)
                visited.append(node.id)
                self._ev("read", agent=agent, node=self._node_ref(node))

            return self._format_node_full_with_request(node, requested_id, cleaned_id)
        if name == "follow_link":
            node_id = str(args.get("node_id", ""))
            pairs = query_api.follow_link(
                node_id,
                direction=str(args.get("direction", "both")),
            )
            if pairs:
                state["empty_streak"] = 0
            visited.extend(node.id for _edge, node in pairs)
            anchor = query_api.read(node_id)
            self._ev(
                "follow_link",
                agent=agent,
                node=self._node_ref(anchor) if anchor else {"id": node_id, "title": node_id},
                neighbors=len(pairs),
            )
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

    # endregion SUBAGENT DISPATCH

    # region FORMATTING
    def _format_candidates(self, nodes: list[Node]) -> str:
        """Lead-facing candidate list: ids to hand to explore (no read action)."""
        if not nodes:
            return "no nodes found"
        return "\n".join(
            f"- node_id: `{node.id}`\n"
            f"  title: {node.title}\n"
            f"  summary: {node.summary}\n"
            f"  next_action: pass this id to explore(node_ids=[...]) if it is a "
            f"promising, distinct lead"
            for node in nodes
        )

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
