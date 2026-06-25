"""Article Database Model"""

from sqlalchemy import Column, String, Text, DateTime, Float, JSON, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datetime import datetime
from src.models.base import BaseModel


class Article(BaseModel):
    """Article model for news articles"""
    
    __tablename__ = "articles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    source = Column(String(200), nullable=False, index=True)
    source_url = Column(String(1000), nullable=False, unique=True)
    published_at = Column(DateTime, nullable=False, index=True)
    
    # NLP Processing
    sentiment = Column(String(20), nullable=True, index=True)  # positive, negative, neutral
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    topics = Column(ARRAY(String), nullable=True)  # Array of topic tags
    keywords = Column(ARRAY(String), nullable=True)  # Extracted keywords
    
    # Processing Status
    processing_status = Column(String(50), nullable=False, default="pending", index=True)  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Metadata
    language = Column(String(10), nullable=True)
    content_length = Column(String(50), nullable=True)  # short, medium, long
    popularity_score = Column(Float, nullable=True)  # 0-1
    
    # Indexing
    __table_args__ = (
        Index('idx_article_source_published', 'source', 'published_at'),
        Index('idx_article_sentiment_processed', 'sentiment', 'processing_status'),
    )
