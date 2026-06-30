"""CLI: bootstrap, ingest, import, query, maintain.

  python -m graph.cli bootstrap [--output output/]
  python -m graph.cli ingest output/<source>/
  python -m graph.cli import input/new.md
  python -m graph.cli query "how do I set up the gpu environment?" [--synthesize]
  python -m graph.cli maintain

State lives under .wiki/ (catalog.sqlite, graph-policy.yml, synthetic/).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .compiler import compile_and_ingest
from .ingest import Ingestor, ingest_path
from .llm import LLMClient
from .maintenance import Maintenance, run_maintenance
from .policy import ensure_policy_file, load_policy
from .query import QueryService
from .store import Store
from .synthetic import SyntheticManager


def _wiki_root(arg: Optional[str]) -> Path:
    return Path(arg or ".wiki")


def _bootstrap_env(wiki_root: Path):
    wiki_root.mkdir(parents=True, exist_ok=True)
    store = Store(wiki_root / "catalog.sqlite")
    policy_path = ensure_policy_file(wiki_root / "graph-policy.yml")
    policy = load_policy(policy_path)
    return store, policy


def cmd_bootstrap(args) -> None:
    store, policy = _bootstrap_env(_wiki_root(args.wiki))
    llm = LLMClient() if args.llm else None
    done = Ingestor(store, llm, policy).bootstrap(args.output)
    print(f"bootstrapped {len(done)} documents: {', '.join(done) or '(none)'}")
    store.close()


def cmd_ingest(args) -> None:
    store, policy = _bootstrap_env(_wiki_root(args.wiki))
    llm = LLMClient() if args.llm else None
    vid = ingest_path(store, args.output_root, llm, policy)
    print(f"ingested -> version {vid}")
    store.close()


def cmd_import(args) -> None:
    """Compile a raw .md with md.py, promote it, then ingest the graph tree."""
    store, policy = _bootstrap_env(_wiki_root(args.wiki))
    llm = LLMClient() if args.llm else None
    try:
        vid = compile_and_ingest(
            store,
            args.source_path,
            output_parent=args.output_parent,
            llm=llm,
            policy=policy,
        )
        print(f"compiled and ingested -> version {vid}")
    finally:
        store.close()


def cmd_query(args) -> None:
    wiki_root = _wiki_root(args.wiki)
    store, policy = _bootstrap_env(wiki_root)
    llm = LLMClient() if args.llm else None
    qs = QueryService(store, policy)
    sm = SyntheticManager(store, policy, wiki_root, llm)

    cached = sm.lookup(args.text)
    if cached:
        print(f"[cache hit] synthetic node {cached.id}")
        if cached.markdown_path and Path(cached.markdown_path).exists():
            print(Path(cached.markdown_path).read_text(encoding="utf-8"))
        store.close()
        return

    result = qs.query(args.text)
    print(f"# Query: {args.text}\n")
    for rn in result.nodes:
        print(
            f"- [{rn.score:6.2f}] hop{rn.hop} {rn.node.node_class}/{rn.node.node_subtype} "
            f"{rn.node.title}  ({rn.node.id})"
        )
    print("\n## Citations")
    for c in result.citations:
        print(
            f"- {c.title}: {c.document_id} {c.source_version_id} lines {c.source_ranges}"
        )

    # An explicit request synthesizes immediately. Otherwise repeated query
    # intent is persisted and creates the planned self-growing cache node once
    # the configured threshold is reached.
    should_synthesize = sm.should_create(args.text, explicit=args.synthesize)
    if should_synthesize:
        node = sm.create_or_refresh(args.text, result, kind=args.kind)
        if node:
            mode = "explicit" if args.synthesize else "repeat-query"
            print(f"\n[synthesized:{mode}] {node.id} -> {node.markdown_path}")
        else:
            print("\n[not synthesized] no absolute evidence (policy refused)")
    store.close()


def cmd_maintain(args) -> None:
    wiki_root = _wiki_root(args.wiki)
    store, policy = _bootstrap_env(wiki_root)
    llm = LLMClient() if args.llm else None
    report = run_maintenance(store, policy, wiki_root, llm)
    print(report.text())
    store.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="graph", description=__doc__)
    p.add_argument("--wiki", default=".wiki", help="state directory (default .wiki)")
    p.add_argument(
        "--llm", action="store_true", help="enable LLM for synthesis/extraction"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bootstrap", help="ingest every output/<source>/ tree")
    b.add_argument("--output", default="output", help="parent of compiled trees")
    b.set_defaults(func=cmd_bootstrap)

    i = sub.add_parser("ingest", help="ingest one compiled output tree")
    i.add_argument("output_root", help="path to output/<source>/")
    i.set_defaults(func=cmd_ingest)

    raw = sub.add_parser("import", help="compile and ingest one raw Markdown file")
    raw.add_argument("source_path", help="path to a raw .md source")
    raw.add_argument("--output-parent", default="output", help="compiled output parent")
    raw.set_defaults(func=cmd_import)

    q = sub.add_parser("query", help="search + traverse + optional synthesize")
    q.add_argument("text")
    q.add_argument("--synthesize", action="store_true")
    q.add_argument(
        "--kind",
        default="discovery",
        choices=["howto", "discovery", "case", "comparison", "investigation"],
    )
    q.set_defaults(func=cmd_query)

    m = sub.add_parser("maintain", help="reindex, refresh stale, health report")
    m.set_defaults(func=cmd_maintain)
    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
