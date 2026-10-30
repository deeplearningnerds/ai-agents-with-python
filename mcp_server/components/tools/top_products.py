from typing import Annotated

from fastmcp.tools import tool
from pydantic import Field

from mcp_server.db import query_to_markdown


@tool(annotations={"readOnlyHint": True})
def get_top_products(limit: Annotated[int, Field(ge=1, le=20)] = 5) -> str:
    """
    Return products ranked by total revenue.

    Use this tool when the user asks for top products, bestsellers,
    product rankings, or products with the highest revenue.

    Args:
        limit: The maximum number of products to return, from 1 to 20.
    """
    query = """
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
        LIMIT ?
    """
    return query_to_markdown(query, (limit,))
