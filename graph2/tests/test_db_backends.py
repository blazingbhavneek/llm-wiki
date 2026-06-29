from __future__ import annotations

import importlib.util

import pytest

from ..db import Database
from ..db.raw_sqlite import RawSqliteDatabase


def test_db_package_defaults_to_raw_sqlite() -> None:
    assert Database is RawSqliteDatabase


def test_sqlmodel_backend_has_friendly_missing_dependency_error(tmp_path) -> None:
    from ..db.sqlmodel import SQLModelDatabase

    if importlib.util.find_spec("sqlmodel") is not None:
        pytest.skip("sqlmodel is installed in this environment")

    with pytest.raises(RuntimeError, match="sqlmodel is not installed"):
        SQLModelDatabase(tmp_path / "wiki.sqlite")


def test_lancedb_backend_has_friendly_missing_dependency_error(tmp_path) -> None:
    from ..db.lancedb import LanceDatabase

    if (
        importlib.util.find_spec("sqlmodel") is not None
        and importlib.util.find_spec("lancedb") is not None
    ):
        pytest.skip("sqlmodel and lancedb are installed in this environment")

    with pytest.raises(RuntimeError, match="(sqlmodel|lancedb)"):
        LanceDatabase(tmp_path / "wiki.sqlite")
