"""Turn an md.py output directory into graph nodes + structural edges.

md.py already produced a hierarchical wiki: ``manifest.json`` plus nested leaf
``.md`` files, each with frontmatter (title, summary, source_lines) and an
LLM-written summary. We DO NOT re-split markdown — we consume that work.

Layout::

    <out_dir>/manifest.json
    <out_dir>/NN-<doc>/NN-<section>/NNN-<leaf>.md   (frontmatter + body)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .ids import make_edge_id, make_node_id
from .models import Edge, Node, NodeType

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def _split_frontmatter(text: str) -> tuple[dict, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    meta: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip().strip('"')
    return meta, m.group(2).strip()


def _parse_ranges(value: str | list | None) -> list[tuple[int, int]]:
    if not value:
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return []
    out = []
    for pair in value or []:
        if isinstance(pair, (list, tuple)) and len(pair) == 2:
            out.append((int(pair[0]), int(pair[1])))
    return out


def load_md_output(out_dir: str | Path) -> tuple[list[Node], list[Edge]]:
    """Read one md.py output dir. Returns (nodes, structural_edges)."""

    out_path = Path(out_dir)
    manifest_path = out_path / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"no manifest.json in {out_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_path = manifest.get("source")
    document_name = Path(source_path).name if source_path else out_path.name

    by_filename = {f["filename"]: f for f in manifest.get("files", [])}

    nodes: list[Node] = []
    # section dir (relative parent) -> node ids, for sibling edges + cluster.
    sections: dict[str, list[str]] = {}

    for filename, rec in by_filename.items():
        leaf = out_path / filename
        if not leaf.exists():
            continue
        meta, body = _split_frontmatter(leaf.read_text(encoding="utf-8"))
        if not body:
            continue
        title = rec.get("title") or meta.get("title", "")
        summary = rec.get("summary") or meta.get("summary", "")
        ranges = _parse_ranges(rec.get("source_ranges")) or _parse_ranges(meta.get("source_lines"))
        section = str(Path(filename).parent)  # e.g. "01-test/01-test-overview"
        cluster = _humanize(Path(filename).parent.name)

        node = Node(
            id=make_node_id(body, document_name),
            body=body,
            type=NodeType.endogenous,
            title=title,
            original_document_name=document_name,
            source_path=source_path,
            source_ranges=ranges,
            summary=summary,
            cluster=cluster,
            keywords=[],  # filled by engine via LLM at ingest
        )
        nodes.append(node)
        sections.setdefault(section, []).append(node.id)

    edges = _structural_edges(sections)
    return nodes, edges


def _structural_edges(sections: dict[str, list[str]]) -> list[Edge]:
    """Link consecutive leaf pages within the same section as ``follows``."""

    edges: list[Edge] = []
    for ids in sections.values():
        for prev_id, next_id in zip(ids, ids[1:]):
            edges.append(
                Edge(
                    id=make_edge_id(prev_id, next_id, "follows"),
                    source_node_id=prev_id,
                    target_node_id=next_id,
                    label="follows",
                    summary="Adjacent page in the same source section.",
                )
            )
    return edges


def _humanize(dirname: str) -> str:
    name = re.sub(r"^\d+-", "", dirname).replace("-", " ").strip()
    return name.title()[:80] or "General"
