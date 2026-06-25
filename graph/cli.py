"""Command line interface.

    python -m graph.cli init
    python -m graph.cli add output/test
    python -m graph.cli query keyword "gpu setup"
    python -m graph.cli query vector "how do I select a device"
    python -m graph.cli recon input/test.md
    python -m graph.cli get
    python -m graph.cli health
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import Settings
from .engine import DomainEngine


def _print(value) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


def _engine(args) -> DomainEngine:
    settings = Settings.from_env()
    if args.database:
        settings.database_path = args.database
    return DomainEngine(settings)


def cmd_init(args) -> None:
    eng = _engine(args)
    eng.close()
    print(f"database ready: {eng.settings.database_path}")


def cmd_add(args) -> None:
    eng = _engine(args)
    try:
        nodes = eng.ingest_md_output(args.md_output_dir)
        print(f"ingested {len(nodes)} node(s) from {args.md_output_dir}")
        for node in nodes[:10]:
            print(f"- {node.id}: {node.title or node.summary[:80]}")
    finally:
        eng.close()


def cmd_query(args) -> None:
    eng = _engine(args)
    try:
        _print(eng.query(args.query_type, args.value).model_dump())
    finally:
        eng.close()


def cmd_recon(args) -> None:
    eng = _engine(args)
    try:
        _print(eng.recon(args.source_file))
    finally:
        eng.close()


def cmd_get(args) -> None:
    eng = _engine(args)
    try:
        nodes, edges = eng.get()
        _print({"nodes": [n.model_dump() for n in nodes],
                "edges": [e.model_dump() for e in edges]})
    finally:
        eng.close()


def cmd_health(args) -> None:
    eng = _engine(args)
    try:
        _print(eng.health(args.node_id).model_dump())
    finally:
        eng.close()


def cmd_delete(args) -> None:
    eng = _engine(args)
    try:
        eng.delete(args.node_id)
        print(f"deleted {args.node_id}")
    finally:
        eng.close()


def cmd_update(args) -> None:
    eng = _engine(args)
    try:
        body = Path(args.markdown_path).read_text(encoding="utf-8")
        node = eng.update(args.node_id, body)
        print(f"updated {node.id}")
    finally:
        eng.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="graph", description="LLM wiki graph")
    p.add_argument("--database", help="SQLite path (overrides WIKI_DB)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="create the database").set_defaults(func=cmd_init)

    add = sub.add_parser("add", help="ingest an md.py output directory")
    add.add_argument("md_output_dir")
    add.set_defaults(func=cmd_add)

    q = sub.add_parser("query", help="query by keyword, vector, or id")
    q.add_argument("query_type", choices=["keyword", "vector", "id"])
    q.add_argument("value")
    q.set_defaults(func=cmd_query)

    rec = sub.add_parser("recon", help="check if a source doc is new/changed")
    rec.add_argument("source_file")
    rec.set_defaults(func=cmd_recon)

    sub.add_parser("get", help="dump all nodes and edges").set_defaults(func=cmd_get)

    h = sub.add_parser("health", help="graph health metrics")
    h.add_argument("node_id", nargs="?")
    h.set_defaults(func=cmd_health)

    d = sub.add_parser("delete", help="delete one node")
    d.add_argument("node_id")
    d.set_defaults(func=cmd_delete)

    u = sub.add_parser("update", help="replace a node body from a markdown file")
    u.add_argument("node_id")
    u.add_argument("markdown_path")
    u.set_defaults(func=cmd_update)
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
