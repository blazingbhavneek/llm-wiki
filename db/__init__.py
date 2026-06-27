"""Storage backends for the graph package.

Change the ``Database`` alias here to try a different store globally.
"""

from .base import BaseDatabase
from .lancedb import LanceDatabase
from .raw_sqlite import RawSqliteDatabase
from .sqlmodel import SQLModelDatabase

Database = RawSqliteDatabase

__all__ = [
    "Database",
    "BaseDatabase",
    "RawSqliteDatabase",
    "SQLModelDatabase",
    "LanceDatabase",
]
