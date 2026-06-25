"""Article SQLAlchemy Database Model"""

from sqlalchemy import Column, String, Text, DateTime, Float, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datetime import datetime
from src.models.base import BaseModel
from src.models.article import ArticleStatus


class ArticleDB(BaseModel):
    """Article model for database"""
    
    __tablename__ = "articles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    source = Column(String(200), nullable=False, index=True)
    source_url = Column(String(1000), nullable=False, unique=True, index=True)
    published_at = Column(DateTime, nullable=False, index=True)
    author = Column(String(300), nullable=True)
    image_url = Column(String(1000), nullable=True)
    source_id = Column(String(500), nullable=True, index=True)
    
    # NLP Processing
    sentiment = Column(String(20), nullable=True, index=True)
    sentiment_score = Column(Float, nullable=True)
    keywords = Column(ARRAY(String), nullable=True, default=[])
    embeddings = Column(ARRAY(Float), nullable=True)
    
    # Processing Status
    status = Column(SQLEnum(ArticleStatus), nullable=False, default=ArticleStatus.PENDING, index=True)
    error_message = Column(Text, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    
    # Indexing
    __table_args__ = (
        Index('idx_article_source_published', 'source', 'published_at'),
        Index('idx_article_sentiment_status', 'sentiment', 'status'),
        Index('idx_article_created_at', 'created_at'),
    )
