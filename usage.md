# Usage

Run commands from the repository root.

## Build a graph from existing compiled output

```bash
python -m graph.cli bootstrap --output output
```

This reads every `output/<document>/` tree produced by `md.py`, verifies its
coverage, and builds `.wiki/catalog.sqlite`.

## Search/query the wiki

```bash
python -m graph.cli query "how do I set up GPU development?"
```

The query uses title matching, FTS5 keyword search, and bounded graph traversal.

Run the same semantic query again to create/reuse a synthetic cache/wiki node:

```bash
python -m graph.cli query "how do I set up GPU development?"
```

## Create a synthetic page immediately

```bash
python -m graph.cli query "compare CUDA and SYCL" --synthesize --kind comparison
```

Valid kinds: `howto`, `discovery`, `case`, `comparison`, `investigation`.

## Import a new raw Markdown document

```bash
python -m graph.cli import input/new-document.md
```

This uses the existing `md.py` compiler in a staging directory, validates the
new source tree, promotes it into `output/`, then ingests the document subgraph.

## Enable LLM extraction/synthesis

```bash
python -m graph.cli --llm import input/new-document.md
python -m graph.cli --llm query "how do I configure this?"
```

`--llm` uses `OPENAI_BASE_URL`, `OPENAI_API_KEY`, and `WIKI_MODEL` (default:
`gemma4`). The `--wiki` option must appear before the subcommand:

```bash
python -m graph.cli --wiki /path/to/state bootstrap --output output
```

## Maintenance and tests

```bash
python -m graph.cli maintain
python -m graph.tests.test_pipeline
```

`maintain` rebuilds FTS, refreshes stale synthetic nodes when possible, and
prints graph health/lint results.

## State locations

```text
output/             Compiled, lossless source-local document trees
.wiki/catalog.sqlite Graph catalog and FTS index
.wiki/graph-policy.yml Traversal and graph limits
.wiki/synthetic/    Generated synthetic Markdown knowledge nodes
```
