from __future__ import annotations

import re

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from agent.config import settings
from agent.mcp_client import MCPToolClient

_history_store: dict[str, list[BaseMessage]] = {}
_client = MCPToolClient(settings.mcp_server_url)
_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Du bist ein hilfsbereiter Datenassistent fuer ein Demo-Projekt. "
            "Beantworte Fragen auf Deutsch. "
            "Nutze die bereitgestellten Datenkontexte, wenn vorhanden. "
            "Wenn Daten fehlen oder unklar sind, sage das klar.",
        ),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{message}"),
        (
            "system",
            "Zusatzkontext aus MCP-Tools:\n{context}\n\n"
            "Wenn kein Zusatzkontext vorhanden ist, beantworte die Frage allgemein.",
        ),
    ]
)


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )


def _extract_region(message: str) -> str:
    lowered = message.lower()
    for region in ("north", "south", "east", "west"):
        if region in lowered:
            return region
    return ""


def _extract_customer_name(message: str) -> str:
    patterns = [
        r"kunde\s+(.+)",
        r"customer\s+(.+)",
        r"bestellungen\s+von\s+(.+)",
        r"orders\s+for\s+(.+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" ?.,")
    return ""


async def _build_context(message: str) -> str:
    lowered = message.lower()
    sections: list[str] = []

    if any(keyword in lowered for keyword in ("spalte", "schema", "daten", "table", "tabelle")):
        result = await _client.call_tool("list_available_data", {})
        sections.append(f"Verfuegbare Daten:\n{result}")

    if any(keyword in lowered for keyword in ("umsatz", "sales", "region", "overview", "ueberblick")):
        region = _extract_region(message)
        payload: dict[str, object] = {"limit": 5}
        if region:
            payload["region"] = region
        result = await _client.call_tool("get_sales_overview", payload)
        sections.append(f"Sales Overview:\n{result}")

    if any(keyword in lowered for keyword in ("produkt", "product", "top")):
        result = await _client.call_tool("get_top_products", {"limit": 5})
        sections.append(f"Top Produkte:\n{result}")

    if any(keyword in lowered for keyword in ("kunde", "customer", "bestellung", "order")):
        customer_name = _extract_customer_name(message)
        if customer_name:
            result = await _client.call_tool(
                "find_customer_orders",
                {"customer_name": customer_name, "limit": 10},
            )
            sections.append(f"Kundenbestellungen fuer {customer_name}:\n{result}")

    return "\n\n".join(sections).strip() or "Kein zusaetzlicher Datenkontext abgefragt."


async def run_agent(message: str, session_id: str) -> str:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please configure it in the .env file.")

    history = _history_store.setdefault(session_id, [])
    context = await _build_context(message)
    prompt_value = _prompt.invoke(
        {
            "message": message,
            "chat_history": history,
            "context": context,
        }
    )
    result = await _get_llm().ainvoke(prompt_value)
    answer = str(result.content).strip()

    history.append(HumanMessage(content=message))
    history.append(AIMessage(content=answer))

    return answer
