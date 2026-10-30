from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    agent_api_host: str = "127.0.0.1"
    agent_api_port: int = 8000
    agent_api_reload: bool = True
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    mcp_server_url: str = "http://localhost:9000/mcp"
    mcp_client_timeout: float = 10.0

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
