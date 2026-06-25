"""Application Configuration"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application
    APP_NAME: str = Field(default="AI News Intelligence")
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    # Database
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/news_intelligence")
    DATABASE_POOL_SIZE: int = Field(default=10)
    DATABASE_MAX_OVERFLOW: int = Field(default=20)

    # News APIs
    NEWSAPI_KEY: str = Field(default="")
    GUARDIAN_API_KEY: str = Field(default="")
    NYTIMES_API_KEY: str = Field(default="")

    # LLM
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = Field(default="gpt-4")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small")

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379")
    REDIS_DB: int = Field(default=0)

    # API
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    API_WORKERS: int = Field(default=4)
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])

    # Processing
    MAX_RETRIES: int = Field(default=3)
    REQUEST_TIMEOUT: int = Field(default=30)
    BATCH_SIZE: int = Field(default=100)
    PROCESSING_THREADS: int = Field(default=4)

    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
