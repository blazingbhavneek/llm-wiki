"""Turn an md.py output directory into graph nodes and structural edges."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import Edge, Node, NodeType
from .utils import make_edge_id, make_node_id

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
_NUMBERED_DOC_RE = re.compile(r"^\d+-(.+\.md)$")


class MarkdownIngest:
    # region LIFECYCLE
    def __init__(self) -> None:
        pass

    # endregion LIFECYCLE

    # region PUBLIC API
    def load_md_output(self, out_dir: str | Path) -> tuple[list[Node], list[Edge]]:
        """Read one md.py output dir and return ``(nodes, structural_edges)``."""

        out_path = Path(out_dir)

        self._log("=" * 80)
        self._log("Starting md.py output ingest")
        self._log(f"Input directory: {out_path}")
        self._log(f"Absolute path: {out_path.resolve()}")

        if not out_path.exists():
            self._log(f"ERROR: input directory does not exist: {out_path}")
            raise FileNotFoundError(f"input directory does not exist: {out_path}")

        if not out_path.is_dir():
            self._log(f"ERROR: input path is not a directory: {out_path}")
            raise NotADirectoryError(f"input path is not a directory: {out_path}")

        manifest_path = out_path / "manifest.json"
        if manifest_path.exists():
            self._log("Detected OLD md.py layout: manifest.json found")
            nodes, edges = self._load_old_manifest_output(out_path)
        else:
            self._log("manifest.json not found")
            self._log(
                "Trying NEW md.py layout: _planning/metadata.json + "
                "_planning/coverage.json + docs/*.md"
            )
            nodes, edges = self._load_new_planning_docs_output(out_path)

        self._log("-" * 80)
        self._log("Finished md.py output ingest")
        self._log(f"Final node count: {len(nodes)}")
        self._log(f"Final structural edge count: {len(edges)}")
        self._log("=" * 80)
        return nodes, edges

    # endregion PUBLIC API

    # region LAYOUT DISPATCH
    def _load_old_manifest_output(
        self, out_path: Path
    ) -> tuple[list[Node], list[Edge]]:
        manifest_path = out_path / "manifest.json"

        self._log("-" * 80)
        self._log("Loading old manifest.json layout")
        self._log(f"Manifest path: {manifest_path}")

        if not manifest_path.exists():
            self._log(f"ERROR: no manifest.json in {out_path}")
            raise FileNotFoundError(f"no manifest.json in {out_path}")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source_path = manifest.get("source")
        document_name = Path(source_path).name if source_path else out_path.name

        self._log(f"Manifest source path: {source_path}")
        self._log(f"Resolved document name: {document_name}")

        files = manifest.get("files", [])
        self._log(f"Manifest file record count: {len(files)}")

        by_filename = {
            record["filename"]: record for record in files if record.get("filename")
        }
        nodes: list[Node] = []
        sections: dict[str, list[str]] = {}

        for index, (filename, record) in enumerate(by_filename.items(), start=1):
            built = self._build_old_layout_node(
                out_path=out_path,
                filename=filename,
                record=record,
                document_name=document_name,
                source_path=source_path,
                index=index,
                total=len(by_filename),
            )
            if built is None:
                continue

            node, section = built
            nodes.append(node)
            sections.setdefault(section, []).append(node.id)

        self._log(f"Old layout node count: {len(nodes)}")
        self._log(f"Old layout section count: {len(sections)}")

        edges = self._structural_edges(sections)
        self._log(f"Old layout structural edge count: {len(edges)}")
        return nodes, edges

    def _load_new_planning_docs_output(
        self,
        out_path: Path,
    ) -> tuple[list[Node], list[Edge]]:
        planning_dir = out_path / "_planning"
        docs_dir = out_path / "docs"

        self._log("-" * 80)
        self._log("Loading new _planning + docs layout")
        self._log(f"Planning directory: {planning_dir}")
        self._log(f"Docs directory: {docs_dir}")

        if not planning_dir.exists():
            self._log(f"WARNING: _planning directory not found: {planning_dir}")
            self._log("Continuing with empty metadata/coverage fallback")

        if not docs_dir.exists():
            self._log(
                f"ERROR: no manifest.json and no docs directory found in {out_path}"
            )
            raise FileNotFoundError(
                f"no manifest.json and no docs directory found in {out_path}"
            )

        metadata_path = planning_dir / "metadata.json"
        coverage_path = planning_dir / "coverage.json"
        metadata = self._read_json(metadata_path, default={})
        coverage = self._read_json(coverage_path, default={})

        document_name = (
            metadata.get("inferred_file_name")
            or metadata.get("original_file_name")
            or out_path.name
        )

        self._log(f"Metadata path: {metadata_path}")
        self._log(f"Coverage path: {coverage_path}")
        self._log(f"Resolved document name: {document_name!r}")

        metadata_files = metadata.get("files", [])
        coverage_files = coverage.get("files", [])
        self._log(f"metadata.json files count: {len(metadata_files)}")
        self._log(f"coverage.json files count: {len(coverage_files)}")
        self._log(f"coverage source_line_count: {coverage.get('source_line_count')}")
        self._log(f"coverage file_count: {coverage.get('file_count')}")

        metadata_by_name = {
            item.get("name"): item for item in metadata_files if item.get("name")
        }
        coverage_by_name = {
            item.get("filename"): item
            for item in coverage_files
            if item.get("filename")
        }
        self._log(f"Metadata lookup keys count: {len(metadata_by_name)}")
        self._log(f"Coverage lookup keys count: {len(coverage_by_name)}")

        md_files = sorted(docs_dir.glob("*.md"), key=self._doc_sort_key)
        self._log(f"Markdown files found in docs/: {len(md_files)}")
        for index, md_file in enumerate(md_files, start=1):
            self._log(f"  docs file {index:03d}: {md_file.name}")

        nodes: list[Node] = []
        ordered_ids: list[str] = []

        for index, md_file in enumerate(md_files, start=1):
            canonical_name = self._canonical_doc_name(md_file.name)
            node = self._build_new_layout_node(
                md_file=md_file,
                document_name=document_name,
                metadata_rec=metadata_by_name.get(canonical_name, {}),
                coverage_rec=coverage_by_name.get(canonical_name, {}),
                index=index,
                total=len(md_files),
            )
            if node is None:
                continue

            nodes.append(node)
            ordered_ids.append(node.id)

        self._log("-" * 80)
        self._log(f"New layout node count: {len(nodes)}")

        edges = self._linear_structural_edges(ordered_ids)
        self._log(f"New layout structural edge count: {len(edges)}")
        return nodes, edges

    # endregion LAYOUT DISPATCH

    # region OLD LAYOUT HELPERS
    def _build_old_layout_node(
        self,
        *,
        out_path: Path,
        filename: str,
        record: dict[str, Any],
        document_name: str,
        source_path: str | None,
        index: int,
        total: int,
    ) -> tuple[Node, str] | None:
        leaf = out_path / filename

        self._log(f"[old:{index}/{total}] Processing: {filename}")
        self._log(f"[old:{index}/{total}] Full path: {leaf}")

        if not leaf.exists():
            self._log(f"[old:{index}/{total}] SKIP: file does not exist")
            return None

        text = leaf.read_text(encoding="utf-8", errors="ignore")
        meta, body = self._split_frontmatter(text)

        self._log(f"[old:{index}/{total}] Frontmatter keys: {sorted(meta.keys())}")
        if not body:
            self._log(f"[old:{index}/{total}] SKIP: empty body after frontmatter split")
            return None

        title = record.get("title") or meta.get("title", "")
        summary = record.get("summary") or meta.get("summary", "")
        ranges = self._parse_ranges(record.get("source_ranges")) or self._parse_ranges(
            meta.get("source_lines")
        )
        section = str(Path(filename).parent)
        cluster = self._humanize(Path(filename).parent.name)
        node_id = make_node_id(body, document_name)

        self._log(f"[old:{index}/{total}] Node id: {node_id}")
        self._log(f"[old:{index}/{total}] Title: {title!r}")
        self._log(f"[old:{index}/{total}] Summary length: {len(summary)}")
        self._log(f"[old:{index}/{total}] Body length: {len(body)}")
        self._log(f"[old:{index}/{total}] Source ranges: {ranges}")
        self._log(f"[old:{index}/{total}] Section: {section}")
        self._log(f"[old:{index}/{total}] Cluster: {cluster}")

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

        self._log(f"[old:{index}/{total}] Node created successfully")
        return node, section

    # endregion OLD LAYOUT HELPERS

    # region NEW LAYOUT HELPERS
    def _build_new_layout_node(
        self,
        *,
        md_file: Path,
        document_name: str,
        metadata_rec: dict[str, Any],
        coverage_rec: dict[str, Any],
        index: int,
        total: int,
    ) -> Node | None:
        self._log("-" * 80)
        self._log(f"[new:{index}/{total}] Processing docs file: {md_file.name}")
        self._log(f"[new:{index}/{total}] Full path: {md_file}")

        text = md_file.read_text(encoding="utf-8", errors="ignore")
        meta, body = self._split_frontmatter(text)
        body = body.strip()

        self._log(f"[new:{index}/{total}] Raw text length: {len(text)}")
        self._log(
            f"[new:{index}/{total}] Body length after frontmatter split: {len(body)}"
        )
        self._log(f"[new:{index}/{total}] Frontmatter keys: {sorted(meta.keys())}")

        if not body:
            self._log(f"[new:{index}/{total}] SKIP: empty body")
            return None

        canonical_name = self._canonical_doc_name(md_file.name)
        self._log(
            f"[new:{index}/{total}] Canonical metadata filename: {canonical_name}"
        )
        self._log(
            f"[new:{index}/{total}] metadata.json match: {'yes' if metadata_rec else 'no'}"
        )
        self._log(
            f"[new:{index}/{total}] coverage.json match: {'yes' if coverage_rec else 'no'}"
        )

        title = (
            coverage_rec.get("title")
            or meta.get("title")
            or metadata_rec.get("header")
            or self._title_from_markdown(body)
            or self._humanize(canonical_name.removesuffix(".md"))
        )
        summary = coverage_rec.get("summary") or meta.get("summary") or ""
        cluster = coverage_rec.get("header") or metadata_rec.get("header") or "General"

        ranges: list[tuple[int, int]] = []
        source_start = coverage_rec.get("source_start")
        source_end = coverage_rec.get("source_end")
        if source_start is not None and source_end is not None:
            try:
                ranges = [(int(source_start), int(source_end))]
            except Exception as exc:
                self._log(
                    f"[new:{index}/{total}] WARNING: invalid coverage source range "
                    f"source_start={source_start!r}, source_end={source_end!r}: {exc}"
                )
                ranges = []
        else:
            ranges = self._parse_ranges(meta.get("source_lines"))

        node_id = make_node_id(body, document_name)
        self._log(f"[new:{index}/{total}] Node id: {node_id}")
        self._log(f"[new:{index}/{total}] Title: {title!r}")
        self._log(f"[new:{index}/{total}] Cluster: {cluster!r}")
        self._log(f"[new:{index}/{total}] Summary length: {len(summary)}")
        self._log(f"[new:{index}/{total}] Source ranges: {ranges}")
        self._log(f"[new:{index}/{total}] Original document name: {document_name!r}")
        self._log(f"[new:{index}/{total}] Source path stored on node: {str(md_file)!r}")

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

        self._log(f"[new:{index}/{total}] Node created successfully")
        return node

    # endregion NEW LAYOUT HELPERS

    # region MARKDOWN PARSING
    def _split_frontmatter(self, text: str) -> tuple[dict[str, str], str]:
        match = _FRONTMATTER_RE.match(text)
        if not match:
            return {}, text

        meta: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')

        return meta, match.group(2).strip()

    def _parse_ranges(self, value: str | list[object] | None) -> list[tuple[int, int]]:
        if not value:
            return []

        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                self._log(f"WARNING: could not parse source range JSON: {value!r}")
                return []

        ranges: list[tuple[int, int]] = []
        for pair in value or []:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                try:
                    ranges.append((int(pair[0]), int(pair[1])))
                except Exception as exc:
                    self._log(f"WARNING: invalid source range pair {pair!r}: {exc}")

        return ranges

    def _title_from_markdown(self, body: str) -> str | None:
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or None
        return None

    def _humanize(self, dirname: str) -> str:
        name = re.sub(r"^\d+-", "", dirname).replace("-", " ").strip()
        return name.title()[:80] or "General"

    # endregion MARKDOWN PARSING

    # region PLANNING DOC HELPERS
    def _read_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            self._log(f"JSON not found, using default: {path}")
            return default

        self._log(f"Reading JSON: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._log(f"ERROR: invalid JSON in {path}: {exc}")
            raise

        self._log(f"JSON loaded successfully: {path}")
        if isinstance(data, dict):
            self._log(f"Top-level JSON keys: {sorted(data.keys())}")
        else:
            self._log(f"Top-level JSON type: {type(data).__name__}")
        return data

    def _canonical_doc_name(self, filename: str) -> str:
        match = _NUMBERED_DOC_RE.match(filename)
        return match.group(1) if match else filename

    def _doc_sort_key(self, path: Path) -> tuple[int, str]:
        first = path.name.split("-", 1)[0]
        if first.isdigit():
            return int(first), path.name
        return 10**9, path.name

    # endregion PLANNING DOC HELPERS

    # region STRUCTURAL EDGES
    def _structural_edges(self, sections: dict[str, list[str]]) -> list[Edge]:
        self._log("Building structural edges for old sectioned layout")
        self._log(f"Section count: {len(sections)}")

        edges: list[Edge] = []
        for section_name, node_ids in sections.items():
            self._log(f"Section {section_name!r}: {len(node_ids)} node(s)")
            for prev_id, next_id in zip(node_ids, node_ids[1:]):
                self._log(f"Creating follows edge: {prev_id} -> {next_id}")
                edges.append(
                    Edge(
                        id=make_edge_id(prev_id, next_id, "follows"),
                        source_node_id=prev_id,
                        target_node_id=next_id,
                        label="follows",
                        summary="Adjacent page in the same source section.",
                    )
                )

        self._log(f"Created {len(edges)} old-layout structural follows edge(s)")
        return edges

    def _linear_structural_edges(self, node_ids: list[str]) -> list[Edge]:
        self._log("Building linear structural edges for new docs layout")
        self._log(f"Ordered node id count: {len(node_ids)}")

        edges: list[Edge] = []
        for prev_id, next_id in zip(node_ids, node_ids[1:]):
            self._log(f"Creating follows edge: {prev_id} -> {next_id}")
            edges.append(
                Edge(
                    id=make_edge_id(prev_id, next_id, "follows"),
                    source_node_id=prev_id,
                    target_node_id=next_id,
                    label="follows",
                    summary="Next page in the source document.",
                )
            )

        self._log(f"Created {len(edges)} new-layout structural follows edge(s)")
        return edges

    # endregion STRUCTURAL EDGES

    # region LOGGING
    def _log(self, message: str) -> None:
        print(f"[md_ingest] {message}", flush=True)

    # endregion LOGGING
