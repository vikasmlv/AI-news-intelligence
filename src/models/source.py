"""News source data models."""

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Supported news source types."""
    NEWSAPI = "newsapi"
    GUARDIAN = "guardian"
    NYTIMES = "nytimes"
    RSS = "rss"
    CUSTOM = "custom"


class SourceCreate(BaseModel):
    """Create news source request model."""
    name: str = Field(..., min_length=1, max_length=200)
    type: SourceType
    url: str = Field(..., min_length=1)
    api_key: Optional[str] = None
    is_active: bool = True
    priority: int = Field(default=1, ge=1, le=10)
    rate_limit: int = Field(default=100, description="Requests per hour")


class SourceUpdate(BaseModel):
    """Update news source request model."""
    name: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    rate_limit: Optional[int] = None
    last_fetched_at: Optional[datetime] = None


class Source(SourceCreate):
    """News source response model."""
    id: int
    last_fetched_at: Optional[datetime] = None
    article_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
