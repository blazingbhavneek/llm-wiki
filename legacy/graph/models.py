"""Node, edge, evidence, and compiled-document contracts.

Two graph node classes only (handoff.md "Agreed knowledge model"):

  absolute   directly grounded in source documents
  synthetic  durable Markdown an LLM compiled from a valuable multi-hop query

Subtypes (document, source_page, topic, concept, ...) never introduce a third
class. Every edge carries type/explanation/strength/status/evidence/created_by.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional

# --------------------------------------------------------------------------
# Constants / vocabularies
# --------------------------------------------------------------------------

NodeClass = Literal["absolute", "synthetic"]

# Common absolute subtypes. Not enforced as an enum so extraction can grow.
SUBTYPE_DOCUMENT = "document"
SUBTYPE_SOURCE_PAGE = "source_page"
SUBTYPE_TOPIC = "topic"
SUBTYPE_CONCEPT = "concept"

# Edge types named in the handoff. Extra types are allowed.
EDGE_TYPES = {
    "contains",
    "mentions",
    "supports",
    "explains",
    "applies_to",
    "implements",
    "depends_on",
    "contradicts",
    "derives_from",
    "has_topic",
    "related",
}

EdgeStatus = Literal["active", "stale", "rejected"]
NodeStatus = Literal["active", "stale", "rejected", "archived", "review"]
CreatedBy = Literal["bootstrap", "ingest", "query", "review"]


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


# --------------------------------------------------------------------------
# Evidence
# --------------------------------------------------------------------------


@dataclass
class Evidence:
    """Exact source-version + line-range backing for a factual edge."""

    source_version_id: str
    document_id: str
    source_ranges: list[list[int]] = field(default_factory=list)
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Evidence":
        return Evidence(
            source_version_id=d.get("source_version_id", ""),
            document_id=d.get("document_id", ""),
            source_ranges=[list(r) for r in d.get("source_ranges", [])],
            note=d.get("note", ""),
        )


# --------------------------------------------------------------------------
# Graph nodes / edges
# --------------------------------------------------------------------------


@dataclass
class Node:
    id: str
    node_class: NodeClass
    node_subtype: str
    title: str
    markdown_path: Optional[str] = None
    source_version_id: Optional[str] = None
    document_id: Optional[str] = None
    section_path: list[str] = field(default_factory=list)
    status: NodeStatus = "active"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utcnow)
    updated_at: str = field(default_factory=utcnow)

    @property
    def summary(self) -> str:
        return str(self.metadata.get("summary", ""))


@dataclass
class Edge:
    id: str
    src_id: str
    dst_id: str
    type: str
    explanation: str = ""
    strength: float = 1.0
    status: EdgeStatus = "active"
    evidence: list[Evidence] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    created_by: CreatedBy = "bootstrap"
    created_at: str = field(default_factory=utcnow)

    def has_evidence(self) -> bool:
        return any(e.source_ranges for e in self.evidence)


# --------------------------------------------------------------------------
# Compiled-document contract (the only shape source_tree exposes)
# --------------------------------------------------------------------------


@dataclass
class CompiledSourcePage:
    markdown_path: Path
    source_ranges: list[list[int]]
    section_path: list[str]
    title: str
    summary: str = ""
    local_topics: list[str] = field(default_factory=list)
    # path relative to the source output root, used as a stable node key part
    rel_path: str = ""


@dataclass
class CompiledDocument:
    source_path: Path
    output_root: Path
    document_id: str
    title: str
    source_sha256: str
    source_line_count: int
    manifest: dict[str, Any]
    document_topics: list[str] = field(default_factory=list)
    source_pages: list[CompiledSourcePage] = field(default_factory=list)

    def exact_coverage(self) -> bool:
        # source_tree sets this flag only after validate_coverage() passes.
        if self.manifest.get("_coverage_validated"):
            return True
        cov = self.manifest.get("coverage", {})
        return bool(isinstance(cov, dict) and cov.get("exact_coverage"))


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def loads(text: Optional[str], default: Any) -> Any:
    if not text:
        return default
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default
