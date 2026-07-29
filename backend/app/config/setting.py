from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # -- App --
    APP_NAME: str = "AI Chatbot API"
    APP_ENV: str = "development"
    DEBUG: bool = False

    # -- Database --
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"

    # -- Security / JWT --
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -- Google OAuth --
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # -- Gemini API --
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # -- Rate limit & cache --
    RATE_LIMIT_MAX_REQUESTS: int = 20
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    CACHE_TTL_SECONDS: int = 3600

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
