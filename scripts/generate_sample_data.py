from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "data/raw/orders.csv"

CUSTOMERS = [
    "Acme GmbH",
    "Bergmann Retail",
    "City Shop",
    "DataCraft AG",
    "Elbe Handel",
    "Future Goods",
    "Hanseatic Market",
    "Nordstern Logistics",
    "Rhein Office",
    "Sunrise Stores",
]

REGIONS = ["North", "South", "East", "West"]

PRODUCTS = [
    ("Analytics Suite", "Software", 1499.0),
    ("Support Package", "Service", 499.0),
    ("AI Workshop", "Training", 2499.0),
    ("Automation Audit", "Consulting", 1799.0),
    ("Starter License", "Software", 799.0),
]

STATUSES = ["completed", "processing", "shipped"]


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rng = random.Random(42)
    start_date = date(2025, 1, 1)
    rows: list[dict[str, object]] = []

    for index in range(1, 251):
        customer_name = rng.choice(CUSTOMERS)
        product_name, product_category, unit_price = rng.choice(PRODUCTS)
        quantity = rng.randint(1, 8)
        order_date = start_date + timedelta(days=rng.randint(0, 420))
        revenue = round(quantity * unit_price, 2)

        rows.append(
            {
                "order_id": f"ORD-{index:04d}",
                "order_date": order_date.isoformat(),
                "customer_id": f"CUST-{CUSTOMERS.index(customer_name) + 1:03d}",
                "customer_name": customer_name,
                "region": rng.choice(REGIONS),
                "product_category": product_category,
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "revenue": revenue,
                "status": rng.choice(STATUSES),
            }
        )

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
