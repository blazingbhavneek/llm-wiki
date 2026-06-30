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
_MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
_SOURCE_REF_RE = re.compile(r"\[([A-Za-z0-9_.-]+):L(\d+)-L(\d+)\]")
_WIKI_PAGE_FOLDERS = {
    "entities": ("entity", "Wiki Entities"),
    "concepts": ("concept", "Wiki Concepts"),
    "summaries": ("summary", "Wiki Summaries"),
    "indexes": ("index", "Wiki Indexes"),
}
_GLOBAL_WIKI_DOCUMENT = "global_wiki"


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
        wiki_planning_path = out_path / "_planning"
        if manifest_path.exists():
            self._log("Detected OLD md.py layout: manifest.json found")
            nodes, edges = self._load_old_manifest_output(out_path)
        elif self._looks_like_global_wiki_output(out_path):
            self._log("Detected output_wiki layout: global wiki folders found")
            nodes, edges = self._load_global_wiki_output(out_path)
        else:
            self._log("manifest.json not found")
            self._log(
                "Trying NEW md.py layout: _planning/metadata.json + "
                "_planning/coverage.json + docs/*.md"
            )
            if wiki_planning_path.exists():
                self._log(
                    "NOTE: _planning exists but no wiki page folders were detected; "
                    "falling back to docs/*.md layout"
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

    # region GLOBAL WIKI LAYOUT
    def _looks_like_global_wiki_output(self, out_path: Path) -> bool:
        if not (out_path / "raw").is_dir():
            return False
        return any((out_path / folder).is_dir() for folder in _WIKI_PAGE_FOLDERS)

    def _load_global_wiki_output(self, out_path: Path) -> tuple[list[Node], list[Edge]]:
        self._log("-" * 80)
        self._log("Loading output_wiki global wiki layout")
        self._log(f"Wiki root: {out_path}")

        planning_dir = out_path / "_planning"
        page_sources = self._read_json(planning_dir / "page_sources.json", default={})
        page_metadata = self._read_json(planning_dir / "page_metadata.json", default={})
        catalog = self._read_json(planning_dir / "global_catalog.json", default={})
        sources_by_slug = self._extract_page_sources(page_sources)
        metadata_by_slug = self._extract_page_metadata(page_metadata, catalog)

        source_nodes, source_lookup = self._build_wiki_source_nodes(out_path)
        page_nodes, page_files_by_id, page_file_lookup = self._build_wiki_page_nodes(
            out_path=out_path,
            sources_by_slug=sources_by_slug,
            metadata_by_slug=metadata_by_slug,
            source_doc_ids=set(source_lookup),
        )

        nodes = [*source_nodes, *page_nodes]
        edges: list[Edge] = []
        edges.extend(self._wiki_folder_edges(out_path, page_file_lookup))
        edges.extend(
            self._wiki_citation_edges(page_nodes, source_lookup, sources_by_slug)
        )
        edges.extend(
            self._wiki_markdown_link_edges(out_path, page_files_by_id, page_file_lookup)
        )

        self._log(f"Wiki source anchor node count: {len(source_nodes)}")
        self._log(f"Wiki page node count: {len(page_nodes)}")
        self._log(f"Wiki structural/citation edge count: {len(edges)}")
        return nodes, edges

    def _extract_page_sources(self, payload: Any) -> dict[str, list[dict[str, Any]]]:
        if not isinstance(payload, dict):
            return {}
        pages = payload.get("pages", {})
        if not isinstance(pages, dict):
            return {}
        out: dict[str, list[dict[str, Any]]] = {}
        for slug, refs in pages.items():
            if isinstance(slug, str) and isinstance(refs, list):
                # wiki_gen keys planning JSON by the raw page slug, which may be
                # bare ("assertion") or type-prefixed ("concept/assertion").
                # Normalize to the bare stem so folder-derived page slugs match.
                key = self._slug_key(slug)
                out.setdefault(key, []).extend(
                    ref for ref in refs if isinstance(ref, dict)
                )
        return out

    def _extract_page_metadata(
        self,
        metadata_payload: Any,
        catalog_payload: Any,
    ) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}

        for payload in (catalog_payload, metadata_payload):
            if not isinstance(payload, dict):
                continue
            pages = payload.get("pages", {})
            if isinstance(pages, dict):
                items = pages.items()
            elif isinstance(pages, list):
                items = (
                    (item.get("slug"), item) for item in pages if isinstance(item, dict)
                )
            else:
                continue

            for slug, item in items:
                if isinstance(slug, str) and isinstance(item, dict):
                    current = out.setdefault(self._slug_key(slug), {})
                    current.update(item)

        return out

    def _build_wiki_source_nodes(
        self, out_path: Path
    ) -> tuple[list[Node], dict[str, str]]:
        raw_dir = out_path / "raw"
        nodes: list[Node] = []
        lookup: dict[str, str] = {}

        if not raw_dir.exists():
            self._log(f"Wiki raw directory not found: {raw_dir}")
            return nodes, lookup

        raw_doc_dirs = [child for child in sorted(raw_dir.iterdir()) if child.is_dir()]
        self._log(f"Raw source document directory count: {len(raw_doc_dirs)}")

        for index, doc_dir in enumerate(raw_doc_dirs, start=1):
            doc_id = doc_dir.name
            original = doc_dir / "original.md"
            coverage = self._read_json(doc_dir / "coverage.json", default={})
            metadata = self._read_json(doc_dir / "metadata.json", default={})
            if not original.exists():
                self._log(
                    f"[wiki-source:{index}] SKIP: missing original.md in {doc_dir}"
                )
                continue

            line_count = self._source_line_count(original, coverage)
            original_name = (
                metadata.get("inferred_file_name")
                or metadata.get("original_file_name")
                or doc_id
            )
            title = f"Source Document: {original_name}"
            rel_original = self._safe_relative(original, out_path)
            body = self._source_anchor_body(
                title=title,
                doc_id=doc_id,
                original_path=rel_original,
                line_count=line_count,
                metadata=metadata,
                coverage=coverage,
            )
            node_id = make_node_id(body, f"{_GLOBAL_WIKI_DOCUMENT}:source:{doc_id}")
            node = Node(
                id=node_id,
                body=body,
                type=NodeType.endogenous,
                title=title,
                original_document_name=_GLOBAL_WIKI_DOCUMENT,
                source_path=str(original),
                source_ranges=[(1, line_count)] if line_count else [],
                summary=(
                    f"Preserved original source document `{doc_id}` for global wiki "
                    "citations."
                ),
                cluster="Wiki Source Documents",
                keywords=[doc_id, str(original_name), "source", "original"],
            )
            nodes.append(node)
            lookup[doc_id] = node.id
            self._log(
                f"[wiki-source:{index}] Node {node.id} doc_id={doc_id!r} "
                f"lines={line_count}"
            )

        return nodes, lookup

    def _build_wiki_page_nodes(
        self,
        *,
        out_path: Path,
        sources_by_slug: dict[str, list[dict[str, Any]]],
        metadata_by_slug: dict[str, dict[str, Any]],
        source_doc_ids: set[str],
    ) -> tuple[list[Node], dict[str, Path], dict[Path, str]]:
        nodes: list[Node] = []
        files_by_id: dict[str, Path] = {}
        node_id_by_path: dict[Path, str] = {}

        for folder, (page_kind, cluster) in _WIKI_PAGE_FOLDERS.items():
            base = out_path / folder
            if not base.exists():
                continue

            md_files = sorted(base.glob("*.md"))
            self._log(f"Wiki {folder}/ markdown file count: {len(md_files)}")
            for index, md_file in enumerate(md_files, start=1):
                slug = self._wiki_slug(folder, md_file)
                key = self._slug_key(slug)
                text = md_file.read_text(encoding="utf-8", errors="ignore")
                source_refs = self._merge_source_refs(
                    sources_by_slug.get(key, []),
                    self._source_refs_from_markdown(
                        text=text,
                        out_path=out_path,
                        source_doc_ids=source_doc_ids,
                    ),
                )
                if source_refs:
                    sources_by_slug[key] = source_refs
                node = self._build_wiki_page_node(
                    out_path=out_path,
                    md_file=md_file,
                    slug=slug,
                    page_kind=page_kind,
                    cluster=cluster,
                    source_refs=source_refs,
                    metadata=metadata_by_slug.get(key, {}),
                    index=index,
                    total=len(md_files),
                )
                if node is None:
                    continue
                nodes.append(node)
                files_by_id[node.id] = md_file
                node_id_by_path[md_file.resolve()] = node.id

        return nodes, files_by_id, node_id_by_path

    def _build_wiki_page_node(
        self,
        *,
        out_path: Path,
        md_file: Path,
        slug: str,
        page_kind: str,
        cluster: str,
        source_refs: list[dict[str, Any]],
        metadata: dict[str, Any],
        index: int,
        total: int,
    ) -> Node | None:
        self._log("-" * 80)
        self._log(f"[wiki-page:{page_kind}:{index}/{total}] Processing: {md_file}")

        text = md_file.read_text(encoding="utf-8", errors="ignore")
        meta, body = self._split_frontmatter(text)
        body = body.strip()
        if not body:
            self._log(f"[wiki-page:{page_kind}:{index}/{total}] SKIP: empty body")
            return None

        title = (
            str(metadata.get("title") or "").strip()
            or meta.get("title")
            or self._title_from_markdown(body)
            or self._humanize(md_file.stem)
        )
        summary = (
            str(metadata.get("summary") or "").strip()
            or meta.get("summary")
            or self._first_summary_from_markdown(body)
        )
        aliases = self._string_list(metadata.get("aliases"))
        doc_ids = self._doc_ids_from_refs(source_refs)
        ranges = self._source_ranges_from_refs(source_refs)
        body_for_node = self._append_wiki_reference_section(body, source_refs)
        node_id = make_node_id(body_for_node, f"{_GLOBAL_WIKI_DOCUMENT}:{slug}")

        self._log(f"[wiki-page:{page_kind}:{index}/{total}] Slug: {slug}")
        self._log(f"[wiki-page:{page_kind}:{index}/{total}] Node id: {node_id}")
        self._log(f"[wiki-page:{page_kind}:{index}/{total}] Title: {title!r}")
        self._log(
            f"[wiki-page:{page_kind}:{index}/{total}] Source ref count: {len(source_refs)}"
        )
        self._log(f"[wiki-page:{page_kind}:{index}/{total}] Source doc ids: {doc_ids}")

        return Node(
            id=node_id,
            body=body_for_node,
            type=NodeType.endogenous,
            title=title,
            original_document_name=_GLOBAL_WIKI_DOCUMENT,
            source_path=str(md_file),
            source_ranges=ranges,
            summary=summary,
            cluster=cluster,
            keywords=[slug, page_kind, *aliases, *doc_ids],
        )

    def _source_anchor_body(
        self,
        *,
        title: str,
        doc_id: str,
        original_path: str,
        line_count: int,
        metadata: dict[str, Any],
        coverage: dict[str, Any],
    ) -> str:
        lines = [
            f"# {title}",
            "",
            f"Document id: `{doc_id}`.",
            f"Preserved original source: `{original_path}`.",
            f"Global source line range: `L1-L{line_count}`.",
        ]
        original_name = metadata.get("original_file_name")
        inferred_name = metadata.get("inferred_file_name")
        if original_name:
            lines.append(f"Original file name: `{original_name}`.")
        if inferred_name and inferred_name != original_name:
            lines.append(f"Inferred file name: `{inferred_name}`.")
        file_count = coverage.get("file_count")
        if file_count is not None:
            lines.append(f"Chunk artifact count: `{file_count}`.")
        lines.extend(
            [
                "",
                "This node is an anchor for wiki citations; the original document "
                "content remains in the preserved source file rather than being "
                "duplicated inside the graph node.",
            ]
        )
        return "\n".join(lines).strip() + "\n"

    def _append_wiki_reference_section(
        self,
        body: str,
        source_refs: list[dict[str, Any]],
    ) -> str:
        if not source_refs:
            return body

        lines = [body.rstrip(), "", "## Graph Source References"]
        for ref in source_refs:
            doc_id = ref.get("doc_id")
            line_start = ref.get("line_start")
            line_end = ref.get("line_end")
            ref_label = ref.get("ref") or (
                f"{doc_id}:L{line_start}-L{line_end}"
                if doc_id and line_start is not None and line_end is not None
                else ""
            )
            source_path = ref.get("source_path")
            rendered = f"- [{ref_label}]" if ref_label else "- Source reference"
            if source_path:
                rendered += f" `{source_path}`"
            lines.append(rendered)
        return "\n".join(lines).strip() + "\n"

    def _wiki_folder_edges(
        self,
        out_path: Path,
        node_id_by_path: dict[Path, str],
    ) -> list[Edge]:
        edges: list[Edge] = []
        for folder, (_page_kind, cluster) in _WIKI_PAGE_FOLDERS.items():
            base = out_path / folder
            if not base.exists():
                continue
            ordered_ids = [
                node_id_by_path[path.resolve()]
                for path in sorted(base.glob("*.md"))
                if path.resolve() in node_id_by_path
            ]
            for prev_id, next_id in zip(ordered_ids, ordered_ids[1:]):
                edges.append(
                    Edge(
                        id=make_edge_id(prev_id, next_id, "follows"),
                        source_node_id=prev_id,
                        target_node_id=next_id,
                        label="follows",
                        summary=f"Next page in the {cluster.lower()} section.",
                    )
                )
        return edges

    def _wiki_citation_edges(
        self,
        page_nodes: list[Node],
        source_lookup: dict[str, str],
        sources_by_slug: dict[str, list[dict[str, Any]]],
    ) -> list[Edge]:
        page_id_by_slug = {
            self._slug_key(keyword): node.id
            for node in page_nodes
            for keyword in node.keywords[:1]
            if "/" in keyword
        }
        edges: list[Edge] = []

        for slug, refs in sorted(sources_by_slug.items()):
            page_id = page_id_by_slug.get(slug)
            if not page_id:
                continue

            refs_by_doc: dict[str, list[str]] = {}
            for ref in refs:
                doc_id = ref.get("doc_id")
                if not isinstance(doc_id, str):
                    continue
                if doc_id not in source_lookup:
                    continue
                line_start = ref.get("line_start")
                line_end = ref.get("line_end")
                rendered = (
                    f"L{line_start}-L{line_end}"
                    if line_start is not None and line_end is not None
                    else str(ref.get("ref") or "")
                )
                refs_by_doc.setdefault(doc_id, []).append(rendered)

            for doc_id, ranges in sorted(refs_by_doc.items()):
                source_id = source_lookup[doc_id]
                range_text = ", ".join(r for r in ranges if r)
                summary = f"Wiki page `{slug}` cites preserved source `{doc_id}`" + (
                    f" at {range_text}." if range_text else "."
                )
                edges.append(
                    Edge(
                        id=make_edge_id(page_id, source_id, "wiki_cites_source"),
                        source_node_id=page_id,
                        target_node_id=source_id,
                        label="wiki_cites_source",
                        summary=summary,
                    )
                )
                edges.append(
                    Edge(
                        id=make_edge_id(source_id, page_id, "source_supports_wiki"),
                        source_node_id=source_id,
                        target_node_id=page_id,
                        label="source_supports_wiki",
                        summary=summary,
                    )
                )

        return edges

    def _wiki_markdown_link_edges(
        self,
        out_path: Path,
        page_files_by_id: dict[str, Path],
        node_id_by_path: dict[Path, str],
    ) -> list[Edge]:
        del out_path
        edges: list[Edge] = []

        for source_id, path in page_files_by_id.items():
            text = path.read_text(encoding="utf-8", errors="ignore")
            for target in self._markdown_link_targets(path, text):
                target_id = node_id_by_path.get(target)
                if not target_id or target_id == source_id:
                    continue
                edges.append(
                    Edge(
                        id=make_edge_id(source_id, target_id, "wiki_links_to"),
                        source_node_id=source_id,
                        target_node_id=target_id,
                        label="wiki_links_to",
                        summary="Markdown link between generated wiki pages.",
                    )
                )

        return edges

    def _markdown_link_targets(self, path: Path, text: str) -> list[Path]:
        targets: list[Path] = []
        for raw_target in _MARKDOWN_LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (path.parent / target).resolve()
            if candidate.suffix.lower() == ".md":
                targets.append(candidate)
        return targets

    @staticmethod
    def _slug_key(slug: str) -> str:
        """Bare-stem key for slug matching across wiki_gen's mixed slug styles.

        wiki_gen writes planning JSON keyed by the raw page slug, which is
        sometimes bare ("assertion") and sometimes type-prefixed
        ("concept/assertion"); the on-disk file is always ``<folder>/<stem>.md``.
        Collapsing to the part after the last ``/`` makes both styles match the
        folder-derived page slug.
        """

        return slug.rsplit("/", 1)[-1]

    def _wiki_slug(self, folder: str, path: Path) -> str:
        prefix = {
            "entities": "entity",
            "concepts": "concept",
            "summaries": "summary",
            "indexes": "index",
        }.get(folder, folder)
        return f"{prefix}/{path.stem}"

    def _source_line_count(self, original: Path, coverage: dict[str, Any]) -> int:
        raw_count = (
            coverage.get("source_line_count") if isinstance(coverage, dict) else None
        )
        try:
            count = int(raw_count)
            if count > 0:
                return count
        except (TypeError, ValueError):
            pass
        return len(original.read_text(encoding="utf-8", errors="ignore").splitlines())

    def _source_ranges_from_refs(
        self, refs: list[dict[str, Any]]
    ) -> list[tuple[int, int]]:
        ranges: list[tuple[int, int]] = []
        for ref in refs:
            try:
                start = int(ref["line_start"])
                end = int(ref["line_end"])
            except (KeyError, TypeError, ValueError):
                continue
            ranges.append((start, end))
        return ranges

    def _source_refs_from_markdown(
        self,
        *,
        text: str,
        out_path: Path,
        source_doc_ids: set[str],
    ) -> list[dict[str, Any]]:
        refs: list[dict[str, Any]] = []
        for match in _SOURCE_REF_RE.finditer(text):
            doc_id, raw_start, raw_end = match.groups()
            if source_doc_ids and doc_id not in source_doc_ids:
                continue
            start = int(raw_start)
            end = int(raw_end)
            refs.append(
                {
                    "doc_id": doc_id,
                    "source_path": str(out_path / "raw" / doc_id / "original.md"),
                    "line_start": start,
                    "line_end": end,
                    "ref": f"{doc_id}:L{start}-L{end}",
                }
            )
        return refs

    def _merge_source_refs(
        self,
        left: list[dict[str, Any]],
        right: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        merged: list[dict[str, Any]] = []
        seen: set[tuple[str, int, int]] = set()
        for ref in [*left, *right]:
            try:
                key = (str(ref["doc_id"]), int(ref["line_start"]), int(ref["line_end"]))
            except (KeyError, TypeError, ValueError):
                continue
            if key in seen:
                continue
            seen.add(key)
            merged.append(ref)
        return merged

    def _doc_ids_from_refs(self, refs: list[dict[str, Any]]) -> list[str]:
        doc_ids: list[str] = []
        for ref in refs:
            doc_id = ref.get("doc_id")
            if isinstance(doc_id, str) and doc_id not in doc_ids:
                doc_ids.append(doc_id)
        return doc_ids

    def _string_list(self, value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [str(item) for item in value if str(item).strip()]

    def _safe_relative(self, path: Path, root: Path) -> str:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return str(path)

    def _first_summary_from_markdown(self, body: str) -> str:
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("---"):
                continue
            return stripped[:240]
        return ""

    # endregion GLOBAL WIKI LAYOUT

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
