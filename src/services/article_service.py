"""Article Service - Business Logic for Articles"""

import logging
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from src.models.article import Article
from src.models.article import ArticleStatus

logger = logging.getLogger(__name__)


class ArticleService:
    """Service for article operations"""

    @staticmethod
    def create_article(
        db: Session,
        title: str,
        content: str,
        source: str,
        source_url: str,
        published_at: datetime,
        summary: Optional[str] = None,
        author: Optional[str] = None,
        image_url: Optional[str] = None,
        source_id: Optional[str] = None,
    ) -> Article:
        """Create new article"""
        try:
            article = Article(
                title=title,
                content=content,
                source=source,
                source_url=source_url,
                published_at=published_at,
                summary=summary,
                author=author,
                image_url=image_url,
                source_id=source_id,
                status=ArticleStatus.PENDING,
            )
            db.add(article)
            db.commit()
            db.refresh(article)
            logger.info(f"✅ Article created: {article.id}")
            return article
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error creating article: {str(e)}")
            raise

    @staticmethod
    def get_article(db: Session, article_id: UUID) -> Optional[Article]:
        """Get article by ID"""
        return db.query(Article).filter(Article.id == article_id).first()

    @staticmethod
    def get_articles(
        db: Session,
        page: int = 1,
        limit: int = 10,
        source: Optional[str] = None,
        sentiment: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[List[Article], int]:
        """Get paginated articles with filters"""
        query = db.query(Article)

        # Apply filters
        if source:
            query = query.filter(Article.source == source)
        if sentiment:
            query = query.filter(Article.sentiment == sentiment)
        if status:
            query = query.filter(Article.status == status)

        # Count total
        total = query.count()

        # Pagination
        skip = (page - 1) * limit
        articles = query.order_by(desc(Article.published_at)).offset(skip).limit(limit).all()

        return articles, total

    @staticmethod
    def update_article_sentiment(
        db: Session,
        article_id: UUID,
        sentiment: str,
        sentiment_score: float,
    ) -> Optional[Article]:
        """Update article sentiment"""
        try:
            article = db.query(Article).filter(Article.id == article_id).first()
            if article:
                article.sentiment = sentiment
                article.sentiment_score = sentiment_score
                db.commit()
                db.refresh(article)
                logger.info(f"✅ Article sentiment updated: {article_id}")
            return article
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error updating sentiment: {str(e)}")
            raise

    @staticmethod
    def update_article_status(
        db: Session,
        article_id: UUID,
        status: ArticleStatus,
        error_message: Optional[str] = None,
    ) -> Optional[Article]:
        """Update article processing status"""
        try:
            article = db.query(Article).filter(Article.id == article_id).first()
            if article:
                article.status = status
                if error_message:
                    article.error_message = error_message
                if status == ArticleStatus.COMPLETED:
                    article.processed_at = datetime.utcnow()
                db.commit()
                db.refresh(article)
            return article
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error updating article status: {str(e)}")
            raise

    @staticmethod
    def search_articles(db: Session, query_text: str, limit: int = 10) -> List[Article]:
        """Search articles by title or content"""
        return (
            db.query(Article)
            .filter(
                Article.title.ilike(f"%{query_text}%")
                | Article.content.ilike(f"%{query_text}%")
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_pending_articles(db: Session, limit: int = 100) -> List[Article]:
        """Get articles pending processing"""
        return (
            db.query(Article)
            .filter(Article.status == ArticleStatus.PENDING)
            .order_by(Article.created_at)
            .limit(limit)
            .all()
        )
