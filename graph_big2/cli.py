"""Command line interface for graph_big2: a thin argparse shell over `Graph`."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .graph import Graph
from .models import Settings


def _print(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


def _graph(args: argparse.Namespace) -> Graph:
    settings = Settings.from_env()
    if args.database:
        settings.database_path = args.database
    return Graph(settings)


# region COMMANDS
def cmd_init(args: argparse.Namespace) -> None:
    graph = _graph(args)
    graph.close()
    print(f"database ready: {graph.settings.database_path}")


def cmd_add(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        nodes = graph.ingest_md_output(args.md_output_dir)
        print(f"ingested {len(nodes)} node(s) from {args.md_output_dir}")
        for node in nodes[:10]:
            print(f"- {node.id}: {node.title or node.summary[:80]}")
    finally:
        graph.close()


def cmd_add_wiki(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        nodes = graph.ingest_wiki_output(args.wiki_output_dir)
        print(f"ingested {len(nodes)} wiki node(s) from {args.wiki_output_dir}")
        for node in nodes[:10]:
            print(f"- {node.id}: {node.title or node.summary[:80]}")
    finally:
        graph.close()


def cmd_query(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        _print(graph.query(args.query_type, args.value).model_dump())
    finally:
        graph.close()


def cmd_ask(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        _print(graph.ask(args.question, persist=not args.no_persist).model_dump())
    finally:
        graph.close()


def cmd_recon(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        _print(graph.recon(args.source_file))
    finally:
        graph.close()


def cmd_cascade(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        _print({"actions": graph.cascading_update(args.md_output_dir)})
    finally:
        graph.close()


def cmd_get(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        nodes, edges = graph.get()
        _print(
            {
                "nodes": [node.model_dump() for node in nodes],
                "edges": [edge.model_dump() for edge in edges],
            }
        )
    finally:
        graph.close()


def cmd_health(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        _print(graph.health(args.node_id).model_dump())
    finally:
        graph.close()


def cmd_delete(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        graph.delete(args.node_id)
        print(f"deleted {args.node_id}")
    finally:
        graph.close()


def cmd_update(args: argparse.Namespace) -> None:
    graph = _graph(args)
    try:
        body = Path(args.markdown_path).read_text(encoding="utf-8")
        node = graph.update_node(args.node_id, body)
        print(f"updated {node.id}")
    finally:
        graph.close()


# endregion COMMANDS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="graph_big2", description="LLM wiki graph")
    parser.add_argument("--database", help="SQLite path (overrides WIKI_GRAPH2_DB)")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("init", help="create the database").set_defaults(
        func=cmd_init
    )

    add = subcommands.add_parser("add", help="ingest an md.py output directory")
    add.add_argument("md_output_dir")
    add.set_defaults(func=cmd_add)

    add_wiki = subcommands.add_parser(
        "add-wiki",
        help="ingest a generated output_wiki global wiki directory",
    )
    add_wiki.add_argument("wiki_output_dir")
    add_wiki.set_defaults(func=cmd_add_wiki)

    query = subcommands.add_parser("query", help="query by keyword, vector, or id")
    query.add_argument("query_type", choices=["keyword", "vector", "id"])
    query.add_argument("value")
    query.set_defaults(func=cmd_query)

    ask = subcommands.add_parser(
        "ask", help="answer a question via the reasoning agent"
    )
    ask.add_argument("question")
    ask.add_argument(
        "--no-persist", action="store_true", help="do not save the answer node"
    )
    ask.set_defaults(func=cmd_ask)

    recon = subcommands.add_parser("recon", help="check if a source doc is new/changed")
    recon.add_argument("source_file")
    recon.set_defaults(func=cmd_recon)

    cascade = subcommands.add_parser(
        "cascade", help="apply a revised md.py output directory"
    )
    cascade.add_argument("md_output_dir")
    cascade.set_defaults(func=cmd_cascade)

    subcommands.add_parser("get", help="dump all nodes and edges").set_defaults(
        func=cmd_get
    )

    health = subcommands.add_parser("health", help="graph health metrics")
    health.add_argument("node_id", nargs="?")
    health.set_defaults(func=cmd_health)

    delete = subcommands.add_parser("delete", help="delete one node")
    delete.add_argument("node_id")
    delete.set_defaults(func=cmd_delete)

    update = subcommands.add_parser(
        "update", help="replace a node body from a markdown file"
    )
    update.add_argument("node_id")
    update.add_argument("markdown_path")
    update.set_defaults(func=cmd_update)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
