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
        product_id,
        product_name,
        category,
        SUM(quantity) AS units_sold,
        ROUND(SUM(total_amount), 2) AS total_revenue,
        COUNT(DISTINCT order_id) AS order_count
    FROM sales
    GROUP BY product_id, product_name, category
    ORDER BY total_revenue DESC, product_name ASC, product_id ASC
    LIMIT 5
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
