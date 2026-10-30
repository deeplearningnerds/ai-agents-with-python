from fastmcp.tools import tool

from mcp_server.db import query_to_markdown


@tool(annotations={"readOnlyHint": True})
def get_sales_summary() -> str:
    """
    Return key sales KPIs and revenue breakdowns.

    This tool returns total revenue, order count, customer count, units sold,
    and the top countries and categories by revenue.
    Use this tool for general questions about sales performance.
    """
    kpi_query = """
        SELECT
            COUNT(*) AS sales_rows,
            COUNT(DISTINCT order_id) AS order_count,
            COUNT(DISTINCT customer_id) AS customer_count,
            ROUND(SUM(total_amount), 2) AS total_revenue,
            ROUND(AVG(total_amount), 2) AS avg_line_revenue,
            SUM(quantity) AS units_sold
        FROM sales
    """
    country_query = """
        SELECT
            country_name,
            COUNT(DISTINCT order_id) AS order_count,
            SUM(quantity) AS units_sold,
            ROUND(SUM(total_amount), 2) AS total_revenue
        FROM sales
        GROUP BY country_name
        ORDER BY total_revenue DESC, country_name ASC
        LIMIT 5
    """
    category_query = """
        SELECT
            category,
            COUNT(DISTINCT order_id) AS order_count,
            SUM(quantity) AS units_sold,
            ROUND(SUM(total_amount), 2) AS total_revenue
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC, category ASC
        LIMIT 5
    """
    return (
        "Sales KPIs:\n"
        f"{query_to_markdown(kpi_query)}\n\n"
        "Top countries by revenue:\n"
        f"{query_to_markdown(country_query)}\n\n"
        "Top categories by revenue:\n"
        f"{query_to_markdown(category_query)}"
    )
