"""Processing job data models."""

from datetime import datetime
from typing import Optional, Any, Dict
from enum import Enum

from pydantic import BaseModel, Field


class ProcessingJobStatus(str, Enum):
    """Processing job status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProcessingJob(BaseModel):
    """Processing job model."""
    id: int
    job_type: str = Field(..., description="Type of processing job")
    status: ProcessingJobStatus
    article_ids: list[int] = Field(default_factory=list)
    progress: int = Field(default=0, ge=0, le=100)
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
