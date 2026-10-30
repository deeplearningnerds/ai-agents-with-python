import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = REPO_ROOT / "data/raw/sales.csv"
load_dotenv(REPO_ROOT / ".env")

DB_PATH = Path(os.getenv("DUCKDB_PATH", "data/warehouse/sales.duckdb"))
if not DB_PATH.is_absolute():
    DB_PATH = REPO_ROOT / DB_PATH


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_PATH}. Put sales.csv into data/raw first."
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(DB_PATH)) as connection:
        # Demo-Tabelle mit der aktuellen CSV-Datei neu erstellen
        connection.execute(
            """
            CREATE OR REPLACE TABLE sales AS
            SELECT *
            FROM read_csv_auto(?, HEADER=TRUE)
            """,
            [str(CSV_PATH)],
        )
        row_count = connection.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        if row_count == 0:
            raise ValueError("The sales table contains no rows.")

    print(f"Loaded data from {CSV_PATH} into {DB_PATH}")


if __name__ == "__main__":
    main()
