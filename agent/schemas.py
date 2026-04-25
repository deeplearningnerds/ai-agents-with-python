from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message for the agent.")
    session_id: str = Field(..., min_length=1, description="Client session identifier.")


class ChatResponse(BaseModel):
    answer: str
    session_id: str
