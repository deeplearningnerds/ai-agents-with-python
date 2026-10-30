from fastmcp.tools import tool

from mcp_server.db import query_to_markdown


@tool(annotations={"readOnlyHint": True})
def get_order_details(order_id: str) -> str:
    """
    Return all line items for a single order.

    Use this tool when the user asks for details about a specific order,
    an order ID, or the products included in an order.

    Args:
        order_id: The order ID, for example, o24.
    """
    query = """
        SELECT
            order_id,
            sales_date,
            customer_name,
            country_name,
            city,
            product_name,
            category,
            quantity,
            price,
            total_amount,
            currency
        FROM sales
        WHERE lower(order_id) = lower(?)
        ORDER BY sales_id
    """
    return query_to_markdown(query, (order_id,))
