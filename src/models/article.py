"""Article data models."""

from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, Field


class ArticleStatus(str, Enum):
    """Article processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ArticleCreate(BaseModel):
    """Create article request model."""
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=10)
    summary: Optional[str] = Field(None, max_length=1000)
    source: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    author: Optional[str] = Field(None)
    published_at: datetime
    image_url: Optional[str] = None
    source_id: str = Field(..., description="External source identifier")


class ArticleUpdate(BaseModel):
    """Update article request model."""
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[ArticleStatus] = None
    processed_at: Optional[datetime] = None
    embeddings: Optional[List[float]] = None


class Article(ArticleCreate):
    """Article response model."""
    id: int
    status: ArticleStatus = ArticleStatus.PENDING
    embeddings: Optional[List[float]] = None
    keywords: Optional[List[str]] = None
    sentiment_score: Optional[float] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
