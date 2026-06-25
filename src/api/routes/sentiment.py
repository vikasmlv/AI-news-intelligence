"""API Routes - Sentiment Analysis Endpoint"""

from typing import List
from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.article_service import ArticleService
from src.models.article import ArticleStatus

router = APIRouter()


class SentimentRecord(BaseModel):
    """Sentiment analysis record"""
    article_id: str
    title: str
    sentiment: str
    sentiment_score: float

    class Config:
        from_attributes = True


class SentimentResponse(BaseModel):
    """Sentiment analysis response"""
    total_articles: int
    positive: int
    negative: int
    neutral: int
    records: List[SentimentRecord]
    timestamp: datetime


@router.get("/sentiment", response_model=SentimentResponse)
async def get_sentiment_analysis(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get sentiment analysis results
    
    Args:
        limit: Maximum number of results
    
    Returns:
        SentimentResponse: Sentiment analysis data
    """
    articles, _ = ArticleService.get_articles(
        db, page=1, limit=limit, status=ArticleStatus.COMPLETED
    )
    
    positive = sum(1 for a in articles if a.sentiment == "positive")
    negative = sum(1 for a in articles if a.sentiment == "negative")
    neutral = len(articles) - positive - negative
    
    records = [
        SentimentRecord(
            article_id=str(a.id),
            title=a.title,
            sentiment=a.sentiment or "neutral",
            sentiment_score=a.sentiment_score or 0.0
        )
        for a in articles
    ]
    
    return SentimentResponse(
        total_articles=len(articles),
        positive=positive,
        negative=negative,
        neutral=neutral,
        records=records,
        timestamp=datetime.utcnow()
    )


@router.get("/sentiment/stats")
async def get_sentiment_statistics(db: Session = Depends(get_db)):
    """
    Get sentiment statistics and trends
    
    Returns:
        dict: Sentiment statistics
    """
    articles, _ = ArticleService.get_articles(
        db, page=1, limit=1000, status=ArticleStatus.COMPLETED
    )
    
    if not articles:
        return {
            "total": 0,
            "positive_percentage": 0,
            "negative_percentage": 0,
            "neutral_percentage": 0,
            "average_sentiment_score": 0,
            "trend": "no_data"
        }
    
    positive = sum(1 for a in articles if a.sentiment == "positive")
    negative = sum(1 for a in articles if a.sentiment == "negative")
    neutral = len(articles) - positive - negative
    
    avg_score = sum(a.sentiment_score or 0 for a in articles) / len(articles)
    
    return {
        "total": len(articles),
        "positive_percentage": (positive / len(articles)) * 100,
        "negative_percentage": (negative / len(articles)) * 100,
        "neutral_percentage": (neutral / len(articles)) * 100,
        "average_sentiment_score": round(avg_score, 3),
        "trend": "stable"
    }
