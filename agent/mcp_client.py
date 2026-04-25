from __future__ import annotations

from typing import Any

from fastmcp import Client


def _normalize_mcp_result(result: Any) -> str:
    if isinstance(result, str):
        return result

    content = getattr(result, "content", None)
    if content is None:
        return str(result)

    parts: list[str] = []
    for item in content:
        text = getattr(item, "text", None)
        if text:
            parts.append(text)
            continue
        parts.append(str(item))

    return "\n".join(parts).strip()


class MCPToolClient:
    def __init__(self, server_url: str) -> None:
        self.server_url = server_url

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        async with Client(self.server_url) as client:
            result = await client.call_tool(tool_name, arguments)
        return _normalize_mcp_result(result)
