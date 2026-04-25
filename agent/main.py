from fastapi import FastAPI

from agent.schemas import ChatRequest, ChatResponse
from agent.service import run_agent

app = FastAPI(
    title="AI Agent API",
    version="0.1.0",
    description="FastAPI wrapper around a LangChain OpenAI agent.",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    answer = await run_agent(message=request.message, session_id=request.session_id)
    return ChatResponse(answer=answer, session_id=request.session_id)
