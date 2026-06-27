"""Turn an md.py output directory into graph nodes + structural edges.

Supports both md.py output layouts.

Old layout::

    <out_dir>/manifest.json
    <out_dir>/NN-<doc>/NN-<section>/NNN-<leaf>.md

New layout::

    <out_dir>/_planning/metadata.json
    <out_dir>/_planning/coverage.json
    <out_dir>/docs/001-document-cover.md
    <out_dir>/docs/002-table-of-contents.md
    ...
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .ids import make_edge_id, make_node_id
from .models import Edge, Node, NodeType

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
_NUMBERED_DOC_RE = re.compile(r"^\d+-(.+\.md)$")


def _log(message: str) -> None:
    """Simple print logger for md ingestion debugging."""
    print(f"[md_ingest] {message}", flush=True)


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
            _log(f"WARNING: could not parse source range JSON: {value!r}")
            return []

    out = []

    for pair in value or []:
        if isinstance(pair, (list, tuple)) and len(pair) == 2:
            try:
                out.append((int(pair[0]), int(pair[1])))
            except Exception as exc:
                _log(f"WARNING: invalid source range pair {pair!r}: {exc}")

    return out


def load_md_output(out_dir: str | Path) -> tuple[list[Node], list[Edge]]:
    """Read one md.py output dir. Returns ``(nodes, structural_edges)``.

    Supports:

    - old ``manifest.json`` layout
    - new ``_planning/metadata.json`` + ``_planning/coverage.json`` + ``docs/*.md`` layout
    """

    out_path = Path(out_dir)

    _log("=" * 80)
    _log(f"Starting md.py output ingest")
    _log(f"Input directory: {out_path}")
    _log(f"Absolute path: {out_path.resolve()}")

    if not out_path.exists():
        _log(f"ERROR: input directory does not exist: {out_path}")
        raise FileNotFoundError(f"input directory does not exist: {out_path}")

    if not out_path.is_dir():
        _log(f"ERROR: input path is not a directory: {out_path}")
        raise NotADirectoryError(f"input path is not a directory: {out_path}")

    manifest_path = out_path / "manifest.json"

    if manifest_path.exists():
        _log("Detected OLD md.py layout: manifest.json found")
        nodes, edges = _load_old_manifest_output(out_path)
    else:
        _log("manifest.json not found")
        _log("Trying NEW md.py layout: _planning/metadata.json + _planning/coverage.json + docs/*.md")
        nodes, edges = _load_new_planning_docs_output(out_path)

    _log("-" * 80)
    _log(f"Finished md.py output ingest")
    _log(f"Final node count: {len(nodes)}")
    _log(f"Final structural edge count: {len(edges)}")
    _log("=" * 80)

    return nodes, edges


# ── old manifest.json layout ────────────────────────────────────────────


def _load_old_manifest_output(out_path: Path) -> tuple[list[Node], list[Edge]]:
    manifest_path = out_path / "manifest.json"

    _log("-" * 80)
    _log("Loading old manifest.json layout")
    _log(f"Manifest path: {manifest_path}")

    if not manifest_path.exists():
        _log(f"ERROR: no manifest.json in {out_path}")
        raise FileNotFoundError(f"no manifest.json in {out_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    source_path = manifest.get("source")
    document_name = Path(source_path).name if source_path else out_path.name

    _log(f"Manifest source path: {source_path}")
    _log(f"Resolved document name: {document_name}")

    files = manifest.get("files", [])
    _log(f"Manifest file record count: {len(files)}")

    by_filename = {f["filename"]: f for f in files if f.get("filename")}

    nodes: list[Node] = []

    # section dir, relative parent -> node ids, for sibling edges + cluster.
    sections: dict[str, list[str]] = {}

    for index, (filename, rec) in enumerate(by_filename.items(), start=1):
        leaf = out_path / filename

        _log(f"[old:{index}/{len(by_filename)}] Processing: {filename}")
        _log(f"[old:{index}/{len(by_filename)}] Full path: {leaf}")

        if not leaf.exists():
            _log(f"[old:{index}/{len(by_filename)}] SKIP: file does not exist")
            continue

        text = leaf.read_text(encoding="utf-8", errors="ignore")
        meta, body = _split_frontmatter(text)

        _log(f"[old:{index}/{len(by_filename)}] Frontmatter keys: {sorted(meta.keys())}")

        if not body:
            _log(f"[old:{index}/{len(by_filename)}] SKIP: empty body after frontmatter split")
            continue

        title = rec.get("title") or meta.get("title", "")
        summary = rec.get("summary") or meta.get("summary", "")

        ranges = (
            _parse_ranges(rec.get("source_ranges"))
            or _parse_ranges(meta.get("source_lines"))
        )

        section = str(Path(filename).parent)
        cluster = _humanize(Path(filename).parent.name)

        node_id = make_node_id(body, document_name)

        _log(f"[old:{index}/{len(by_filename)}] Node id: {node_id}")
        _log(f"[old:{index}/{len(by_filename)}] Title: {title!r}")
        _log(f"[old:{index}/{len(by_filename)}] Summary length: {len(summary)}")
        _log(f"[old:{index}/{len(by_filename)}] Body length: {len(body)}")
        _log(f"[old:{index}/{len(by_filename)}] Source ranges: {ranges}")
        _log(f"[old:{index}/{len(by_filename)}] Section: {section}")
        _log(f"[old:{index}/{len(by_filename)}] Cluster: {cluster}")

        node = Node(
            id=node_id,
            body=body,
            type=NodeType.endogenous,
            title=title,
            original_document_name=document_name,
            source_path=source_path,
            source_ranges=ranges,
            summary=summary,
            cluster=cluster,
            keywords=[],
        )

        nodes.append(node)
        sections.setdefault(section, []).append(node.id)

        _log(f"[old:{index}/{len(by_filename)}] Node created successfully")

    _log(f"Old layout node count: {len(nodes)}")
    _log(f"Old layout section count: {len(sections)}")

    edges = _structural_edges(sections)

    _log(f"Old layout structural edge count: {len(edges)}")

    return nodes, edges


# ── new _planning + docs layout ─────────────────────────────────────────


def _load_new_planning_docs_output(out_path: Path) -> tuple[list[Node], list[Edge]]:
    planning_dir = out_path / "_planning"
    docs_dir = out_path / "docs"

    _log("-" * 80)
    _log("Loading new _planning + docs layout")
    _log(f"Planning directory: {planning_dir}")
    _log(f"Docs directory: {docs_dir}")

    if not planning_dir.exists():
        _log(f"WARNING: _planning directory not found: {planning_dir}")
        _log("Continuing with empty metadata/coverage fallback")

    if not docs_dir.exists():
        _log(f"ERROR: no manifest.json and no docs directory found in {out_path}")
        raise FileNotFoundError(
            f"no manifest.json and no docs directory found in {out_path}"
        )

    metadata_path = planning_dir / "metadata.json"
    coverage_path = planning_dir / "coverage.json"

    metadata = _read_json(metadata_path, default={})
    coverage = _read_json(coverage_path, default={})

    document_name = (
        metadata.get("original_file_name")
        or metadata.get("inferred_file_name")
        or out_path.name
    )

    _log(f"Metadata path: {metadata_path}")
    _log(f"Coverage path: {coverage_path}")
    _log(f"Resolved document name: {document_name!r}")

    metadata_files = metadata.get("files", [])
    coverage_files = coverage.get("files", [])

    _log(f"metadata.json files count: {len(metadata_files)}")
    _log(f"coverage.json files count: {len(coverage_files)}")
    _log(f"coverage source_line_count: {coverage.get('source_line_count')}")
    _log(f"coverage file_count: {coverage.get('file_count')}")

    metadata_by_name = {
        item.get("name"): item
        for item in metadata_files
        if item.get("name")
    }

    coverage_by_name = {
        item.get("filename"): item
        for item in coverage_files
        if item.get("filename")
    }

    _log(f"Metadata lookup keys count: {len(metadata_by_name)}")
    _log(f"Coverage lookup keys count: {len(coverage_by_name)}")

    md_files = sorted(docs_dir.glob("*.md"), key=_doc_sort_key)

    _log(f"Markdown files found in docs/: {len(md_files)}")

    for i, md_file in enumerate(md_files, start=1):
        _log(f"  docs file {i:03d}: {md_file.name}")

    nodes: list[Node] = []
    ordered_ids: list[str] = []

    for index, md_file in enumerate(md_files, start=1):
        _log("-" * 80)
        _log(f"[new:{index}/{len(md_files)}] Processing docs file: {md_file.name}")
        _log(f"[new:{index}/{len(md_files)}] Full path: {md_file}")

        text = md_file.read_text(encoding="utf-8", errors="ignore")
        meta, body = _split_frontmatter(text)

        body = body.strip()

        _log(f"[new:{index}/{len(md_files)}] Raw text length: {len(text)}")
        _log(f"[new:{index}/{len(md_files)}] Body length after frontmatter split: {len(body)}")
        _log(f"[new:{index}/{len(md_files)}] Frontmatter keys: {sorted(meta.keys())}")

        if not body:
            _log(f"[new:{index}/{len(md_files)}] SKIP: empty body")
            continue

        canonical_name = _canonical_doc_name(md_file.name)

        _log(f"[new:{index}/{len(md_files)}] Canonical metadata filename: {canonical_name}")

        metadata_rec = metadata_by_name.get(canonical_name, {})
        coverage_rec = coverage_by_name.get(canonical_name, {})

        if metadata_rec:
            _log(f"[new:{index}/{len(md_files)}] metadata.json match: yes")
        else:
            _log(f"[new:{index}/{len(md_files)}] metadata.json match: no")

        if coverage_rec:
            _log(f"[new:{index}/{len(md_files)}] coverage.json match: yes")
        else:
            _log(f"[new:{index}/{len(md_files)}] coverage.json match: no")

        title = (
            coverage_rec.get("title")
            or meta.get("title")
            or metadata_rec.get("header")
            or _title_from_markdown(body)
            or _humanize(canonical_name.removesuffix(".md"))
        )

        summary = (
            coverage_rec.get("summary")
            or meta.get("summary")
            or ""
        )

        cluster = (
            coverage_rec.get("header")
            or metadata_rec.get("header")
            or "General"
        )

        ranges: list[tuple[int, int]] = []

        source_start = coverage_rec.get("source_start")
        source_end = coverage_rec.get("source_end")

        if source_start is not None and source_end is not None:
            try:
                ranges = [(int(source_start), int(source_end))]
            except Exception as exc:
                _log(
                    f"[new:{index}/{len(md_files)}] WARNING: invalid coverage source range "
                    f"source_start={source_start!r}, source_end={source_end!r}: {exc}"
                )
                ranges = []
        else:
            ranges = _parse_ranges(meta.get("source_lines"))

        node_id = make_node_id(body, document_name)

        _log(f"[new:{index}/{len(md_files)}] Node id: {node_id}")
        _log(f"[new:{index}/{len(md_files)}] Title: {title!r}")
        _log(f"[new:{index}/{len(md_files)}] Cluster: {cluster!r}")
        _log(f"[new:{index}/{len(md_files)}] Summary length: {len(summary)}")
        _log(f"[new:{index}/{len(md_files)}] Source ranges: {ranges}")
        _log(f"[new:{index}/{len(md_files)}] Original document name: {document_name!r}")
        _log(f"[new:{index}/{len(md_files)}] Source path stored on node: {str(md_file)!r}")

        node = Node(
            id=node_id,
            body=body,
            type=NodeType.endogenous,
            title=title,
            original_document_name=document_name,
            source_path=str(md_file),
            source_ranges=ranges,
            summary=summary,
            cluster=cluster,
            keywords=[],
        )

        nodes.append(node)
        ordered_ids.append(node.id)

        _log(f"[new:{index}/{len(md_files)}] Node created successfully")

    _log("-" * 80)
    _log(f"New layout node count: {len(nodes)}")

    edges = _linear_structural_edges(ordered_ids)

    _log(f"New layout structural edge count: {len(edges)}")

    return nodes, edges


def _read_json(path: Path, default):
    if not path.exists():
        _log(f"JSON not found, using default: {path}")
        return default

    _log(f"Reading JSON: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _log(f"ERROR: invalid JSON in {path}: {exc}")
        raise

    if isinstance(data, dict):
        _log(f"JSON loaded successfully: {path}")
        _log(f"Top-level JSON keys: {sorted(data.keys())}")
    else:
        _log(f"JSON loaded successfully: {path}")
        _log(f"Top-level JSON type: {type(data).__name__}")

    return data


def _canonical_doc_name(filename: str) -> str:
    """Convert ``001-document-cover.md`` to ``document-cover.md``.

    The new docs directory uses numbered filenames, while metadata.json and
    coverage.json use unnumbered filenames.
    """

    match = _NUMBERED_DOC_RE.match(filename)

    if match:
        return match.group(1)

    return filename


def _doc_sort_key(path: Path) -> tuple[int, str]:
    """Sort ``001-foo.md`` before ``002-bar.md``.

    Files without a numeric prefix are sorted after numbered files.
    """

    first = path.name.split("-", 1)[0]

    if first.isdigit():
        return int(first), path.name

    return 10**9, path.name


def _title_from_markdown(body: str) -> str | None:
    for line in body.splitlines():
        stripped = line.strip()

        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or None

    return None


# ── structural edges ────────────────────────────────────────────────────


def _structural_edges(sections: dict[str, list[str]]) -> list[Edge]:
    """Link consecutive leaf pages within the same section as ``follows``."""

    _log("Building structural edges for old sectioned layout")
    _log(f"Section count: {len(sections)}")

    edges: list[Edge] = []

    for section_name, ids in sections.items():
        _log(f"Section {section_name!r}: {len(ids)} node(s)")

        for prev_id, next_id in zip(ids, ids[1:]):
            edge_id = make_edge_id(prev_id, next_id, "follows")

            _log(f"Creating follows edge: {prev_id} -> {next_id}")

            edges.append(
                Edge(
                    id=edge_id,
                    source_node_id=prev_id,
                    target_node_id=next_id,
                    label="follows",
                    summary="Adjacent page in the same source section.",
                )
            )

    _log(f"Created {len(edges)} old-layout structural follows edge(s)")

    return edges


def _linear_structural_edges(node_ids: list[str]) -> list[Edge]:
    """Link consecutive docs as ``follows`` for the new flat docs layout."""

    _log("Building linear structural edges for new docs layout")
    _log(f"Ordered node id count: {len(node_ids)}")

    edges: list[Edge] = []

    for prev_id, next_id in zip(node_ids, node_ids[1:]):
        edge_id = make_edge_id(prev_id, next_id, "follows")

        _log(f"Creating follows edge: {prev_id} -> {next_id}")

        edges.append(
            Edge(
                id=edge_id,
                source_node_id=prev_id,
                target_node_id=next_id,
                label="follows",
                summary="Next page in the source document.",
            )
        )

    _log(f"Created {len(edges)} new-layout structural follows edge(s)")

    return edges


def _humanize(dirname: str) -> str:
    name = re.sub(r"^\d+-", "", dirname).replace("-", " ").strip()
    return name.title()[:80] or "General"
