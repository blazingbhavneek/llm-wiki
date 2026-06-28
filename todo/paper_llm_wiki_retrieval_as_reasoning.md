# Paper: LLM-Wiki — Retrieval as Reasoning
arxiv: https://arxiv.org/abs/2605.25480

## Problem
Traditional RAG = flat chunks + single KNN lookup. Wrong abstraction for agents that need to reason iteratively over knowledge.

## Core Idea
"Retrieval as Reasoning" — knowledge is a compilable, composable, self-evolving structure. Agents navigate it iteratively via tool calls, not one-shot fetches.

## Architecture
- Wiki pages compiled from source docs (more curated than raw chunks)
- Agents call `search`, `read`, `follow_link` as tools in a reasoning loop
- Stops when agent decides evidence is sufficient
- **Error Book**: persistent record of structural/semantic failures that feeds back to fix the wiki structure
- Multi-agent: multiple agents can refine shared wiki entries
- Bidirectional links between pages as first-class primitives

## Results
Beats HippoRAG 2, LightRAG, GraphRAG by 2.0–8.1 F1 on multi-hop reasoning benchmarks.

## Key Insight
The retrieval interface shape matters as much as the retrieval quality. A query→result interface cannot support the kind of iterative evidence gathering agents need for complex reasoning.
