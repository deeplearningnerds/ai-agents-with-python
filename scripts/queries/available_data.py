import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv
from tabulate import tabulate

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

DB_PATH = Path(os.getenv("DUCKDB_PATH", "data/warehouse/sales.duckdb"))
if not DB_PATH.is_absolute():
    DB_PATH = REPO_ROOT / DB_PATH

QUERY = """
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_name = 'sales'
    ORDER BY ordinal_position
"""


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}. Run scripts/load_duckdb.py first."
        )

    with duckdb.connect(str(DB_PATH), read_only=True) as connection:
        result = connection.execute(QUERY)
        columns = [column[0] for column in result.description]
        rows = result.fetchall()

    print(tabulate(rows, headers=columns, tablefmt="simple_outline"))


if __name__ == "__main__":
    main()
