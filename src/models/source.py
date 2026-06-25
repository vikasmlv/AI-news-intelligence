"""News Source Database Model"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from src.models.base import BaseModel


class NewsSource(BaseModel):
    """News source model"""
    
    __tablename__ = "news_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, unique=True, index=True)
    source_type = Column(String(50), nullable=False)  # newsapi, guardian, nytimes, rss, custom
    url = Column(String(1000), nullable=False)
    api_key = Column(String(500), nullable=True)  # Encrypted in production
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    priority = Column(Integer, nullable=False, default=1)  # 1-10, higher = priority
    rate_limit = Column(Integer, nullable=False, default=100)  # Requests per hour
    last_fetched_at = Column(DateTime, nullable=True, index=True)
    article_count = Column(Integer, nullable=False, default=0)
    
    __table_args__ = (
        Index('idx_source_type_active', 'source_type', 'is_active'),
    )
