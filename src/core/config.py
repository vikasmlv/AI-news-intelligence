"""Core Configuration Module"""

import logging
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    ENV: str = "development"
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/news_intelligence"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # AWS Configuration
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = "news-intelligence-bucket"
    LAMBDA_INGESTION_FUNCTION: str = "news-ingestion"
    LAMBDA_PROCESSING_FUNCTION: str = "news-processing"
    
    # LLM Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    LLM_MAX_TOKENS: int = 500
    LLM_TEMPERATURE: float = 0.7
    
    # News Sources
    NEWS_API_KEY: str = ""
    GUARDIAN_API_KEY: str = ""
    NYTIMES_API_KEY: str = ""
    
    # Model Paths
    SENTIMENT_MODEL_PATH: str = "./models/sentiment-model"
    TOPIC_MODEL_PATH: str = "./models/topic-model"
    
    # Monitoring
    LOG_LEVEL: str = "INFO"
    CLOUDWATCH_GROUP: str = "/aws/lambda/news-intelligence"
    CLOUDWATCH_STREAM: str = "ingestion"
    
    # Performance
    MAX_CONCURRENT_REQUESTS: int = 100
    REQUEST_TIMEOUT: int = 30
    CACHE_TTL: int = 3600
    
    # Security
    JWT_SECRET: str = "your_jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 3600
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
