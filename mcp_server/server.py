from pathlib import Path

from fastmcp import FastMCP
from fastmcp.server.providers import FileSystemProvider

from mcp_server.config import settings

provider = FileSystemProvider(
    root=Path(__file__).parent / "components",
    reload=settings.mcp_reload,
)

mcp = FastMCP(
    "E-Commerce MCP Server",
    providers=[provider],
)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=settings.mcp_host,
        port=settings.mcp_port,
    )
