from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(
        ..., min_length=1, max_length=4000, description="User message for the agent."
    )
    session_id: str = Field(
        ..., min_length=1, max_length=100, description="Client session identifier."
    )


class ChatResponse(BaseModel):
    answer: str
    session_id: str
