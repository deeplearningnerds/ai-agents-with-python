from fastapi import FastAPI

from agent.config import settings
from agent.routers.chat import router as chat_router
from agent.routers.health import router as health_router

app = FastAPI(
    title="AI Agent API",
    version="0.1.0",
    description="FastAPI wrapper around a LangChain OpenAI agent.",
)

app.include_router(health_router)
app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "agent.main:app",
        host=settings.agent_api_host,
        port=settings.agent_api_port,
        reload=settings.agent_api_reload,
    )
