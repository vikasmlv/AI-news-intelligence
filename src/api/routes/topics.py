"""API Routes - Topic Clustering Endpoint"""

from typing import List
from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from collections import Counter

from src.core.database import get_db
from src.services.article_service import ArticleService
from src.models.article import ArticleStatus

router = APIRouter()


class TopicRecord(BaseModel):
    """Topic cluster record"""
    topic_id: str
    name: str
    keywords: List[str]
    article_count: int
    relevance_score: float


class TopicResponse(BaseModel):
    """Topic clustering response"""
    total_topics: int
    topics: List[TopicRecord]
    timestamp: datetime


@router.get("/topics", response_model=TopicResponse)
async def get_topics(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Get topic clusters and classifications
    
    Args:
        limit: Maximum number of topics
    
    Returns:
        TopicResponse: Topic clustering data
    """
    articles, _ = ArticleService.get_articles(
        db, page=1, limit=1000, status=ArticleStatus.COMPLETED
    )
    
    # Extract keywords from articles
    all_keywords = []
    for article in articles:
        if article.keywords:
            all_keywords.extend(article.keywords)
    
    # Count keyword occurrences
    keyword_counts = Counter(all_keywords)
    top_keywords = keyword_counts.most_common(limit)
    
    topics = [
        TopicRecord(
            topic_id=f"topic_{idx}",
            name=keyword,
            keywords=[keyword],
            article_count=count,
            relevance_score=min(1.0, count / 10)  # Normalize score
        )
        for idx, (keyword, count) in enumerate(top_keywords)
    ]
    
    return TopicResponse(
        total_topics=len(topics),
        topics=topics,
        timestamp=datetime.utcnow()
    )


@router.get("/topics/{topic_id}/articles")
async def get_topic_articles(
    topic_id: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Get articles for a specific topic
    
    Args:
        topic_id: Topic identifier
        limit: Maximum number of articles
    
    Returns:
        dict: Articles in topic
    """
    articles, total = ArticleService.get_articles(
        db, page=1, limit=limit
    )
    
    return {
        "topic_id": topic_id,
        "articles": articles,
        "total": total
    }
