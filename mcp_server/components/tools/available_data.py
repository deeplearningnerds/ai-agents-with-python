from fastmcp.tools import tool

from mcp_server.db import query_to_markdown


@tool(annotations={"readOnlyHint": True})
def list_available_data() -> str:
    """
    Show the sales table and its available columns.

    Use this tool when the user asks which sales data or columns
    are available for analysis.
    """
    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'sales'
        ORDER BY ordinal_position
    """
    schema_table = query_to_markdown(query)
    return (
        "Table: sales\n"
        "Available columns:\n"
        f"{schema_table}"
    )
