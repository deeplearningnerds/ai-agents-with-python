from __future__ import annotations

from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = REPO_ROOT / "data/raw/orders.csv"
DB_PATH = REPO_ROOT / "data/warehouse/demo.duckdb"


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_PATH}. Run scripts/generate_sample_data.py first."
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(DB_PATH)) as connection:
        connection.execute("DROP TABLE IF EXISTS orders")
        connection.execute(
            """
            CREATE TABLE orders AS
            SELECT *
            FROM read_csv_auto(?, HEADER=TRUE)
            """,
            [str(CSV_PATH)],
        )

    print(f"Loaded data from {CSV_PATH} into {DB_PATH}")


if __name__ == "__main__":
    main()
