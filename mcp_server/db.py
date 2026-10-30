from pathlib import Path

import duckdb

from mcp_server.config import settings

REPO_ROOT = Path(__file__).resolve().parents[1]


def get_database_path() -> Path:
    return REPO_ROOT / settings.duckdb_path


def get_connection() -> duckdb.DuckDBPyConnection:
    # Der MCP-Server liest ausschließlich Analysedaten
    database_path = get_database_path()
    if not database_path.is_file():
        raise FileNotFoundError(
            f"Database not found: {database_path}. Run scripts/load_duckdb.py first."
        )
    return duckdb.connect(str(database_path), read_only=True)


def query_to_markdown(query: str, params: tuple = ()) -> str:
    # Abfrageergebnisse als Markdown zurückgeben, damit das LLM sie leicht lesen kann
    with get_connection() as connection:
        frame = connection.execute(query, params).fetchdf()
    if frame.empty:
        return "No results found."
    return frame.to_markdown(index=False)
