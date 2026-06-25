"""Application configuration management."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    app_name: str = Field(default="AI News Intelligence")
    app_env: str = Field(default="development", validation_alias="APP_ENV")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # Database
    database_url: str = Field(validation_alias="DATABASE_URL")
    database_pool_size: int = Field(default=10)
    database_max_overflow: int = Field(default=20)

    # News APIs
    newsapi_key: Optional[str] = Field(default=None, validation_alias="NEWSAPI_KEY")
    guardian_api_key: Optional[str] = Field(default=None, validation_alias="GUARDIAN_API_KEY")
    nytimes_api_key: Optional[str] = Field(default=None, validation_alias="NYTIMES_API_KEY")

    # AWS
    aws_region: str = Field(default="us-east-1", validation_alias="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(default=None, validation_alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, validation_alias="AWS_SECRET_ACCESS_KEY")
    aws_s3_bucket: Optional[str] = Field(default=None, validation_alias="AWS_S3_BUCKET")

    # LLM
    openai_api_key: Optional[str] = Field(default=None, validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", validation_alias="OPENAI_MODEL")
    embedding_model: str = Field(default="text-embedding-3-small", validation_alias="EMBEDDING_MODEL")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379", validation_alias="REDIS_URL")
    redis_db: int = Field(default=0, validation_alias="REDIS_DB")

    # API
    api_host: str = Field(default="0.0.0.0", validation_alias="API_HOST")
    api_port: int = Field(default=8000, validation_alias="API_PORT")
    api_workers: int = Field(default=4, validation_alias="API_WORKERS")

    # Processing
    max_retries: int = Field(default=3, validation_alias="MAX_RETRIES")
    request_timeout: int = Field(default=30, validation_alias="REQUEST_TIMEOUT")
    batch_size: int = Field(default=100, validation_alias="BATCH_SIZE")
    processing_threads: int = Field(default=4, validation_alias="PROCESSING_THREADS")

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
