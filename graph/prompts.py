"""Prompts used by the LLM client and edge builder."""

SYSTEM_PROMPT = "You maintain a concise, factual knowledge-graph wiki."

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
