"""Central configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Finance Controller API"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./aifinance.db"
    SECRET_KEY: str = "super-secret-finance-controller-key-2026"
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
