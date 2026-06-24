"""Raw-Markdown import that delegates compilation to the unchanged ``md.py``.

The graph layer never reimplements document splitting. For a new or updated raw
Markdown source it compiles to an output staging directory, validates the
lossless tree, promotes that tree, and then activates the catalog version.
"""

from __future__ import annotations

import asyncio
import hashlib
import shutil
import uuid
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

from .ingest import Ingestor
from .llm import LLMClient
from .policy import Policy
from .source_tree import read_compiled_document
from .store import Store


def _source_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()[:12]


def _compiler_args(source: Path, out_dir: Path) -> SimpleNamespace:
    # Importing md.py is deliberate: this keeps one source compiler and one
    # coverage invariant for batch compilation and graph raw-source ingest.
    import md as source_compiler

    return SimpleNamespace(
        source=str(source),
        out=str(out_dir),
        phase="generate",
        base_url=source_compiler.BASE_URL,
        api_key=source_compiler.API_KEY,
        gen_model=source_compiler.GEN_MODEL,
        verify_model=source_compiler.VERIFY_MODEL,
        generation_lines=source_compiler.GENERATION_LINES,
        verification_lines=source_compiler.VERIFICATION_LINES,
        max_chunk_extra=source_compiler.MAX_CHUNK_EXTRA,
        concurrency=source_compiler.CONCURRENCY,
        temperature=source_compiler.TEMPERATURE,
        timeout=source_compiler.TIMEOUT,
        clean=True,
    )


def compile_and_ingest(
    store: Store,
    source_path: Path | str,
    output_parent: Path | str = "output",
    llm: Optional[LLMClient] = None,
    policy: Optional[Policy] = None,
) -> str:
    """Compile a raw Markdown file with ``md.py`` then atomically ingest it.

    The previous compiled tree remains untouched until the staging tree passed
    md.py's coverage validation and the graph catalog activation succeeded.
    """
    source = Path(source_path).resolve()
    if not source.is_file() or source.suffix.lower() != ".md":
        raise ValueError(f"expected a Markdown source file, got: {source}")

    output_parent = Path(output_parent)
    output_parent.mkdir(parents=True, exist_ok=True)
    target = output_parent / source.stem
    staging_parent = output_parent / ".staging"
    staging_parent.mkdir(parents=True, exist_ok=True)
    staging = staging_parent / f"{source.stem}-{_source_hash(source)}-{uuid.uuid4().hex[:8]}"

    try:
        import md as source_compiler

        asyncio.run(source_compiler.phase_generate(_compiler_args(source, staging)))
        # Read once before promotion so coverage/manifest failures cannot replace
        # the active source-local tree.
        read_compiled_document(staging)

        backup: Optional[Path] = None
        promoted = False
        try:
            if target.exists():
                backup = staging_parent / f"{target.name}-backup-{uuid.uuid4().hex[:8]}"
                target.rename(backup)
            staging.rename(target)
            promoted = True
            doc = read_compiled_document(target)
            version = Ingestor(store, llm, policy).ingest_document(doc)
        except Exception:
            if promoted and target.exists():
                shutil.rmtree(target)
            if backup and backup.exists():
                backup.rename(target)
            raise
        else:
            if backup and backup.exists():
                shutil.rmtree(backup)
            return version
    finally:
        if staging.exists():
            shutil.rmtree(staging)
