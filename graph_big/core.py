"""Leaf: pure helpers, scoring, prompts, protocols. Imports nothing internal but models."""

from __future__ import annotations

import hashlib
import re
from typing import Any, Protocol, runtime_checkable

from .models import Node

# Single shared tokenizer. A module constant on purpose: it is never threaded
# through call signatures.
TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


# --- identifiers / hashing ----------------------------------------------------
def short_hash(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def source_hash(text: str) -> str:
    """Identity of a whole source document, for recon dedup."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slug(text: str, max_length: int = 40) -> str:
    value = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return value[:max_length] or "node"


def make_node_id(body: str, document_name: str | None = None) -> str:
    return f"node:{slug(document_name or 'node', 24)}:{short_hash(body)}"


def make_exogenous_node_id(seed: str) -> str:
    return f"exo:{short_hash(seed)}"


def make_edge_id(source_id: str, target_id: str, label: str) -> str:
    return f"edge:{short_hash(f'{source_id}|{target_id}|{label}', 16)}"


# --- text matching / scoring --------------------------------------------------
def normalize_token(token: str) -> str:
    return token.strip().lower()


def normalize_text(text: str) -> str:
    return " ".join(normalize_token(token) for token in TOKEN_RE.findall(text.lower()))


def jaccard(left: set[str], right: set[str]) -> float:
    left = {value for value in left if value}
    right = {value for value in right if value}
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def token_jaccard(left: str, right: str) -> float:
    return jaccard(
        {normalize_token(t) for t in TOKEN_RE.findall(left.lower())},
        {normalize_token(t) for t in TOKEN_RE.findall(right.lower())},
    )


def claim_keys(node: Node) -> set[str]:
    keys: set[str] = set()
    for claim in node.claims:
        normalized = normalize_text(claim)
        if normalized:
            keys.add(normalized)
    return keys


def match_score(old: Node, new: Node) -> float:
    """Revision-match score in [0, 1]: how likely `new` is a revision of `old`."""
    claim_score = jaccard(claim_keys(old), claim_keys(new))
    keyword_score = jaccard(
        {normalize_token(k) for k in old.keywords},
        {normalize_token(k) for k in new.keywords},
    )
    body_score = token_jaccard(old.body, new.body)
    entity_bonus = 0.0
    if old.entity and new.entity:
        entity_bonus = (
            0.2 if normalize_text(old.entity) == normalize_text(new.entity) else 0.0
        )
    return min(
        1.0, max(claim_score, keyword_score * 0.8, body_score * 0.65) + entity_bonus
    )


def claims_equivalent(old: Node, new: Node, unchanged_threshold: float = 0.9) -> bool:
    """True when old/new carry the same facts (reorder, not a real change)."""
    old_claims = claim_keys(old)
    new_claims = claim_keys(new)
    if old_claims and new_claims:
        return jaccard(old_claims, new_claims) >= unchanged_threshold
    return token_jaccard(old.body, new.body) >= 0.95


# --- ports (Protocols) — replace `object` hints -------------------------------
@runtime_checkable
class LlmClient(Protocol):
    def complete(self, system_prompt: str, user_content: str) -> str: ...
    def complete_structured(
        self, system_prompt: str, user_content: str, output_model: type[Any]
    ) -> Any: ...
    def run_tool_loop(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: list[Any],
        dispatch: Any,
        max_steps: int,
        finish_guard: Any = None,
    ) -> Any: ...


@runtime_checkable
class EmbedderPort(Protocol):
    dim: int
    model_name: str

    def embed_document(self, text: str) -> list[float]: ...
    def embed_query(self, text: str) -> list[float]: ...


@runtime_checkable
class RerankerPort(Protocol):
    def top_k(
        self, query: str, items: list[tuple[str, Any]], k: int
    ) -> list[tuple[Any, float]]: ...


# --- prompts ------------------------------------------------------------------
GRAPH_SYSTEM_PROMPT = "You maintain a concise, factual knowledge-graph wiki."

SUMMARY_PROMPT = (
    "Summarize this markdown node for a knowledge graph. Use ONLY facts present "
    "in the text. Keep it to 1-3 sentences. No preamble."
)

KEYWORD_PROMPT = (
    "Extract the salient technical keywords/entities from this text for graph "
    "search: function names, library names, error codes, concepts, proper nouns. "
    "Return the distinct keywords, most important first, at most 12. Lowercase "
    "unless an acronym or identifier."
)

CLAIM_PROMPT = (
    "Extract stable identity facts from this markdown node for revision matching. "
    "Return one primary entity/topic and up to 20 atomic claims. A claim must be "
    "a short factual statement supported directly by the text. Prefer facts that "
    "would remain recognizable if the source document is reordered. Do not infer "
    "or add facts not present in the text."
)

REGENERATE_EXOGENOUS_PROMPT = (
    "Regenerate a derived wiki node after its supporting source material changed. "
    "Use the previous derived node only to understand the intended topic and shape. "
    "The new node body must be supported only by the CURRENT SUPPORT MATERIAL. "
    "Drop stale claims that are no longer supported. Keep the result concise, "
    "factual, and in markdown. No preamble."
)

EDGE_PROMPT = (
    "You maintain a wiki graph. Given a NEW node and a list of CANDIDATE existing "
    "nodes (already pre-filtered by semantic similarity), decide which candidates "
    "the new node should link to and why.\n"
    "Rules:\n"
    "- Only use candidate ids that were given.\n"
    "- A label is a short verb phrase describing how the target relates to the new "
    "node (e.g. 'uses', 'defines', 'example-of', 'prerequisite-for', 'contradicts').\n"
    "- Only propose an edge when the relationship is clearly useful; skip weak ones.\n"
    "- summary: one short clause explaining the link."
)

ENTITY_DEDUP_PROMPT = (
    "You maintain a wiki graph. Given a NEW node and a list of CANDIDATE existing "
    "nodes, decide whether the new node describes the SAME real-world entity/topic "
    "as exactly one candidate.\n"
    "Rules:\n"
    "- Same entity means the same concrete thing (same API, same tool, same concept), "
    "not merely a related or similar topic.\n"
    "- Be conservative: if unsure, answer is_same=false. Never merge homonyms that "
    "refer to different things.\n"
    "- If there is a match, return is_same=true and target_node_id of that candidate; "
    "otherwise is_same=false and target_node_id=null."
)

CLUSTER_NAMER_SYSTEM = (
    "You name one topic cluster for a knowledge graph. Choose a specific name that "
    "distinguishes this cluster from the other names already used. Prefer the most "
    "specific technical subtopic visible in the keywords and sample section titles. "
    "Avoid broad source names like CUDA, SYCL, OpenMP, or oneAPI when a narrower "
    "topic is present. Reply with ONE concise topic name of at most 4 words. No "
    "quotes, no punctuation, no explanation."
)

MAIN_AGENT_SYSTEM_PROMPT = (
    "You are the LEAD researcher answering a question from a knowledge-graph wiki. "
    "You coordinate; you do NOT read nodes yourself.\n\n"
    "You have two capabilities:\n"
    "- search(text): find candidate nodes (already reranked by relevance). Returns "
    "node ids + titles + summaries only.\n"
    "- explore(node_ids): hand a list of DISTINCT starting node ids to a team of "
    "subagents. Each subagent reads and navigates the graph from one starting node "
    "and reports back what it found. Use this to investigate the promising leads.\n"
    "- finish(answer, cited_node_ids): give the final compiled answer.\n\n"
    "How to work:\n"
    "1. Search the main question, then search individual key terms/functions in it. "
    "Do a few searches to surface different parts of the graph.\n"
    "2. From all the candidates, pick the best DISTINCT starting nodes that cover "
    "DIFFERENT sub-topics (avoid near-duplicates so subagents explore different "
    "subgraphs).\n"
    "3. Call explore(node_ids) ONCE with those starting nodes. The team explores in "
    "parallel and returns each subagent's findings and the node bodies it read.\n"
    "4. Read the subagents' reports. If a clear gap remains, you may search again and "
    "run explore once more; otherwise compile.\n"
    "5. Call finish with a thorough answer grounded ONLY in what the subagents "
    "reported, citing the node ids they used as evidence.\n\n"
    "Rules:\n"
    "- You cannot read node bodies directly; rely on the subagents' reports.\n"
    "- Always copy node ids exactly as shown, including any 'node:' prefix.\n"
    "- Do not finish before running explore at least once.\n"
    "- Prefer breadth: give explore distinct starting points rather than several "
    "ids about the same thing."
)

SUBAGENT_SYSTEM_PROMPT = (
    "You are a research subagent exploring ONE region of a knowledge-graph wiki. "
    "A lead researcher gave you a starting node. Investigate it thoroughly and "
    "report concrete, grounded findings.\n\n"
    "Tools:\n"
    "- read(node_id): read a node's full body. START by reading your assigned node.\n"
    "- follow_link(node_id, direction): jump to a node's neighbors to follow "
    "references, examples, prerequisites, related concepts.\n"
    "- search(text): find more nodes by keyword if your region needs them.\n"
    "- finish(answer, cited_node_ids): report your findings + the node ids you read.\n\n"
    "Rules:\n"
    "1. Read your assigned starting node FIRST.\n"
    "2. Follow links and read 2-5 nodes in YOUR region to gather real evidence.\n"
    "3. Stay in your lane: other subagents cover the sibling starting nodes listed "
    "in your task. Do NOT re-explore those; focus on your own subgraph so the team "
    "covers more ground.\n"
    "4. Base your report ONLY on node bodies you actually read.\n"
    "5. Copy node ids exactly, including any 'node:' prefix.\n"
    "6. When done, call finish with a focused summary of what this region says about "
    "the question, citing the node ids you used."
)

MERMAID_INSTRUCTION = (
    "\n\nDiagrams:\n"
    "- If a flowchart, architecture/block diagram, sequence, or data-flow diagram "
    "would make the answer clearer, include ONE Mermaid diagram in a ```mermaid "
    "fenced block as part of your answer.\n"
    "- Only add a diagram when it genuinely helps; skip it otherwise.\n"
    "- Use simple ASCII node IDs (n1, n2, proc_a) and put any spaces/punctuation/"
    'long text inside quoted labels: n1["Linear layer"] --> n2["GEMM"].\n'
    "- The mermaid block must contain ONLY Mermaid syntax (no prose/bullets)."
)

MERMAID_FIX_SYSTEM = (
    "You fix Mermaid diagram syntax so it renders with mermaid-cli (mmdc). "
    "Return ONLY one corrected ```mermaid fenced code block and nothing else."
)
