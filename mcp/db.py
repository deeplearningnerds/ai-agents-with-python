from __future__ import annotations

from pathlib import Path

import duckdb

from mcp.config import settings

REPO_ROOT = Path(__file__).resolve().parents[1]


def get_database_path() -> Path:
    return REPO_ROOT / settings.duckdb_path


def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(get_database_path()), read_only=False)
