from fastmcp import Client
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from agent.config import settings
from agent.services.prompts import SYSTEM_PROMPT

chat_histories = {}
MAX_HISTORY_MESSAGES = 20

MCP_CLIENT = Client(
    settings.mcp_server_url,
    timeout=settings.mcp_client_timeout,
)


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
    )


async def _load_mcp_tools() -> list[BaseTool]:
    async with MCPAdapter(MCP_CLIENT) as adapter:
        return await adapter.list_tools()


async def run_agent(message: str, session_id: str) -> str:
    # Einfachen Chatverlauf pro Sitzung im Arbeitsspeicher halten
    history = chat_histories.setdefault(session_id, [])
    user_message = HumanMessage(content=message)
    current_messages = history + [user_message]

    # Modell und verfügbare Tools vorbereiten
    llm = _get_llm()
    tools = await _load_mcp_tools()

    # LangChain-Agenten aus Modell, Tools und System-Prompt erstellen
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    # Agenten ausführen und die finale Antwort auslesen
    result = await agent.ainvoke({"messages": current_messages})
    final_message = result["messages"][-1]
    answer = final_message.text.strip()

    # Unterhaltung speichern, damit die nächste Anfrage Kontext behält
    history.append(user_message)
    history.append(AIMessage(content=answer))
    chat_histories[session_id] = history[-MAX_HISTORY_MESSAGES:]

    return answer
