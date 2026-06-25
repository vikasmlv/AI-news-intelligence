"""API Routes - Articles Endpoint"""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.database import get_db
from src.services.article_service import ArticleService
from src.models.article import ArticleStatus

router = APIRouter()


class ArticleResponse(BaseModel):
    """Article response model"""
    id: str
    title: str
    content: str
    summary: Optional[str]
    source: str
    published_at: datetime
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """Article list response model"""
    total: int
    page: int
    limit: int
    articles: List[ArticleResponse]


@router.get("/articles", response_model=ArticleListResponse)
async def list_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    source: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    List articles with filtering
    
    Args:
        page: Page number
        limit: Results per page
        source: Filter by news source
        sentiment: Filter by sentiment
        status: Filter by processing status
    
    Returns:
        ArticleListResponse: Paginated articles
    """
    articles, total = ArticleService.get_articles(
        db, page=page, limit=limit, source=source, 
        sentiment=sentiment, status=status
    )
    return ArticleListResponse(
        total=total,
        page=page,
        limit=limit,
        articles=articles
    )


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: str,
    db: Session = Depends(get_db),
):
    """
    Get single article by ID
    
    Args:
        article_id: Article identifier
    
    Returns:
        ArticleResponse: Article details
    
    Raises:
        HTTPException: 404 if article not found
    """
    try:
        article = ArticleService.get_article(db, UUID(article_id))
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")


@router.post("/articles/search")
async def search_articles(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Search articles by keyword
    
    Args:
        query: Search query string
        page: Page number
        limit: Results per page
    
    Returns:
        ArticleListResponse: Search results
    """
    articles = ArticleService.search_articles(db, query, limit=limit)
    skip = (page - 1) * limit
    paginated = articles[skip:skip + limit]
    
    return ArticleListResponse(
        total=len(articles),
        page=page,
        limit=limit,
        articles=paginated
    )
