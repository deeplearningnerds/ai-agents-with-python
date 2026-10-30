from fastapi import APIRouter

from agent.schemas.chat import ChatRequest, ChatResponse
from agent.services.agent import run_agent

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    answer = await run_agent(message=request.message, session_id=request.session_id)
    return ChatResponse(answer=answer, session_id=request.session_id)
