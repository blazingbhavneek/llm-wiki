"""Command line interface for the graph package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import DomainEngine
from .models import Settings

# region OUTPUT
def _print(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


# endregion OUTPUT

# region ENGINE BOOTSTRAP
def _engine(args: argparse.Namespace) -> DomainEngine:
    settings = Settings.from_env()
    if args.database:
        settings.database_path = args.database
    return DomainEngine(settings)


# endregion ENGINE BOOTSTRAP

# region COMMANDS
def cmd_init(args: argparse.Namespace) -> None:
    engine = _engine(args)
    engine.close()
    print(f"database ready: {engine.settings.database_path}")


def cmd_add(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        nodes = engine.ingest_md_output(args.md_output_dir)
        print(f"ingested {len(nodes)} node(s) from {args.md_output_dir}")
        for node in nodes[:10]:
            print(f"- {node.id}: {node.title or node.summary[:80]}")
    finally:
        engine.close()


def cmd_query(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        _print(engine.query(args.query_type, args.value).model_dump())
    finally:
        engine.close()


def cmd_ask(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        _print(engine.ask(args.question, persist=not args.no_persist).model_dump())
    finally:
        engine.close()


def cmd_recon(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        _print(engine.recon(args.source_file))
    finally:
        engine.close()


def cmd_cascade(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        _print({"actions": engine.cascading_update(args.md_output_dir)})
    finally:
        engine.close()


def cmd_get(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        nodes, edges = engine.get()
        _print(
            {
                "nodes": [node.model_dump() for node in nodes],
                "edges": [edge.model_dump() for edge in edges],
            }
        )
    finally:
        engine.close()


def cmd_health(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        _print(engine.health(args.node_id).model_dump())
    finally:
        engine.close()


def cmd_delete(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        engine.delete(args.node_id)
        print(f"deleted {args.node_id}")
    finally:
        engine.close()


def cmd_update(args: argparse.Namespace) -> None:
    engine = _engine(args)
    try:
        body = Path(args.markdown_path).read_text(encoding="utf-8")
        node = engine.update(args.node_id, body)
        print(f"updated {node.id}")
    finally:
        engine.close()


# endregion COMMANDS

# region PARSER
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="graph", description="LLM wiki graph")
    parser.add_argument("--database", help="SQLite path (overrides WIKI_DB)")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("init", help="create the database").set_defaults(func=cmd_init)

    add = subcommands.add_parser("add", help="ingest an md.py output directory")
    add.add_argument("md_output_dir")
    add.set_defaults(func=cmd_add)

    query = subcommands.add_parser("query", help="query by keyword, vector, or id")
    query.add_argument("query_type", choices=["keyword", "vector", "id"])
    query.add_argument("value")
    query.set_defaults(func=cmd_query)

    ask = subcommands.add_parser("ask", help="answer a question via the reasoning agent")
    ask.add_argument("question")
    ask.add_argument("--no-persist", action="store_true", help="do not save the answer node")
    ask.set_defaults(func=cmd_ask)

    recon = subcommands.add_parser("recon", help="check if a source doc is new/changed")
    recon.add_argument("source_file")
    recon.set_defaults(func=cmd_recon)

    cascade = subcommands.add_parser("cascade", help="apply a revised md.py output directory")
    cascade.add_argument("md_output_dir")
    cascade.set_defaults(func=cmd_cascade)

    subcommands.add_parser("get", help="dump all nodes and edges").set_defaults(func=cmd_get)

    health = subcommands.add_parser("health", help="graph health metrics")
    health.add_argument("node_id", nargs="?")
    health.set_defaults(func=cmd_health)

    delete = subcommands.add_parser("delete", help="delete one node")
    delete.add_argument("node_id")
    delete.set_defaults(func=cmd_delete)

    update = subcommands.add_parser("update", help="replace a node body from a markdown file")
    update.add_argument("node_id")
    update.add_argument("markdown_path")
    update.set_defaults(func=cmd_update)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


# endregion PARSER

if __name__ == "__main__":
    main()
