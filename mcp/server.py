from __future__ import annotations

from fastmcp import FastMCP

from mcp.config import settings
from mcp.db import get_connection, get_database_path

mcp = FastMCP("AI Agents Demo MCP Server")


def _query_to_markdown(query: str, params: tuple = ()) -> str:
    with get_connection() as connection:
        frame = connection.execute(query, params).fetchdf()
    if frame.empty:
        return "Keine Treffer gefunden."
    return frame.to_markdown(index=False)


@mcp.tool()
def list_available_data() -> str:
    database_path = get_database_path()
    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'orders'
        ORDER BY ordinal_position
    """
    schema_table = _query_to_markdown(query)
    return (
        f"Datenbank: {database_path}\n"
        "Tabelle: orders\n"
        "Verfuegbare Spalten:\n"
        f"{schema_table}"
    )


@mcp.tool()
def get_sales_overview(region: str = "", limit: int = 5) -> str:
    base_query = """
        SELECT
            region,
            COUNT(*) AS order_count,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(AVG(revenue), 2) AS avg_order_value
        FROM orders
        {where_clause}
        GROUP BY region
        ORDER BY total_revenue DESC
        LIMIT ?
    """
    params: tuple = (limit,)
    where_clause = ""

    if region:
        where_clause = "WHERE lower(region) = lower(?)"
        params = (region, limit)

    return _query_to_markdown(base_query.format(where_clause=where_clause), params)


@mcp.tool()
def find_customer_orders(customer_name: str, limit: int = 10) -> str:
    query = """
        SELECT
            order_id,
            order_date,
            customer_name,
            region,
            product_name,
            quantity,
            revenue,
            status
        FROM orders
        WHERE lower(customer_name) LIKE lower(?)
        ORDER BY order_date DESC
        LIMIT ?
    """
    return _query_to_markdown(query, (f"%{customer_name}%", limit))


@mcp.tool()
def get_top_products(limit: int = 5) -> str:
    query = """
        SELECT
            product_name,
            product_category,
            SUM(quantity) AS units_sold,
            ROUND(SUM(revenue), 2) AS total_revenue
        FROM orders
        GROUP BY product_name, product_category
        ORDER BY total_revenue DESC
        LIMIT ?
    """
    return _query_to_markdown(query, (limit,))


def run() -> None:
    mcp.run(
        transport="streamable-http",
        host=settings.mcp_host,
        port=settings.mcp_port,
    )


if __name__ == "__main__":
    run()
