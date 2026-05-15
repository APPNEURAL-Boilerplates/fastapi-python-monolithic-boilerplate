from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env."""

    app_name: str = "FastAPI Monolithic Boilerplate"
    app_version: str = "0.1.0"
    environment: Literal["local", "test", "staging", "production"] = "local"
    debug: bool = False

    host: str = "0.0.0.0"
    port: int = 8000
    api_prefix: str = "/api/v1"

    log_level: str = "INFO"

    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
