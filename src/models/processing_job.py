"""Processing Job Database Model"""

from sqlalchemy import Column, String, Integer, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datetime import datetime
from src.models.base import BaseModel


class ProcessingJob(BaseModel):
    """Processing job tracking model"""
    
    __tablename__ = "processing_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type = Column(String(100), nullable=False, index=True)  # sentiment, topic_clustering, embedding, etc.
    status = Column(String(50), nullable=False, default="pending", index=True)  # pending, running, completed, failed
    article_ids = Column(ARRAY(UUID), nullable=False, default=[])
    progress = Column(Integer, nullable=False, default=0)  # 0-100
    total_articles = Column(Integer, nullable=False, default=0)
    processed_articles = Column(Integer, nullable=False, default=0)
    result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    __table_args__ = (
        Index('idx_job_type_status', 'job_type', 'status'),
        Index('idx_job_status_created', 'status', 'created_at'),
    )
