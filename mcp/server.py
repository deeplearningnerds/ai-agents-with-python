from fastmcp import FastMCP

# ------------------------------
# Create FastMCP Server
# ------------------------------
mcp = FastMCP("Deep Learning Nerds MCP Server 📘")

# ------------------------------
# Define Tools
# ------------------------------
@mcp.tool()
def greet_user(name: str) -> str:
    return f"Hello, {name}! Welcome to the Deep learning Nerds Academy"

# ------------------------------
# Run FastMCP Server
# ------------------------------
if __name__ == "__main__":
    mcp.run(transport="streamable-http")