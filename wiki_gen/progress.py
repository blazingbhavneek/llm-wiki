"""Resumable-run bookkeeping: a single progress.json under _planning/.

Each pipeline stage records completed item ids (and a `complete` flag) so an
interrupted run can be restarted and skip finished work instead of redoing it.
All mutation happens under the caller's asyncio lock; writes are atomic.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

PROGRESS_VERSION = 1
PROGRESS_FILE = "progress.json"


def _progress_path(output_root: Path) -> Path:
    return output_root / "_planning" / PROGRESS_FILE


def load_progress(output_root: Path) -> dict[str, Any]:
    path = _progress_path(output_root)
    if not path.exists():
        return {"version": PROGRESS_VERSION}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": PROGRESS_VERSION}
    if not isinstance(data, dict) or data.get("version") != PROGRESS_VERSION:
        return {"version": PROGRESS_VERSION}
    return data


def save_progress(output_root: Path, progress: dict[str, Any]) -> None:
    path = _progress_path(output_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(progress, handle, indent=2, ensure_ascii=False)
        tmp_name = handle.name
    Path(tmp_name).replace(path)


def _stage(progress: dict[str, Any], name: str) -> dict[str, Any]:
    stage = progress.setdefault(name, {})
    if not isinstance(stage, dict):
        stage = {}
        progress[name] = stage
    return stage


def is_complete(progress: dict[str, Any], name: str) -> bool:
    return bool(_stage(progress, name).get("complete"))


def mark_complete(progress: dict[str, Any], name: str) -> None:
    _stage(progress, name)["complete"] = True


def done_set(progress: dict[str, Any], name: str) -> set[str]:
    return set(_stage(progress, name).get("done", []))


def add_done(progress: dict[str, Any], name: str, item_id: str) -> None:
    stage = _stage(progress, name)
    done = stage.setdefault("done", [])
    if item_id not in done:
        done.append(item_id)
