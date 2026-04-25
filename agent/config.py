from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    agent_host: str = "0.0.0.0"
    agent_port: int = 8000
    mcp_server_url: str = "http://localhost:9000/mcp"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
