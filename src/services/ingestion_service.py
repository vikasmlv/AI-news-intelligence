"""Article Ingestion Service"""

import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.article import Article, ArticleStatus
from src.services.article_service import ArticleService
from src.services.sentiment_service import sentiment_service

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingesting and processing news articles"""

    @staticmethod
    async def ingest_articles(
        db: Session,
        articles_data: List[dict],
    ) -> tuple[int, int]:
        """Ingest articles from news sources
        
        Args:
            db: Database session
            articles_data: List of article dictionaries
            
        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0

        for article_data in articles_data:
            try:
                # Check if article already exists (by URL)
                existing = db.query(Article).filter(
                    Article.source_url == article_data.get("url")
                ).first()

                if existing:
                    logger.debug(f"Article already exists: {article_data.get('url')}")
                    continue

                # Create article
                article = ArticleService.create_article(
                    db=db,
                    title=article_data.get("title", ""),
                    content=article_data.get("content", ""),
                    source=article_data.get("source", "Unknown"),
                    source_url=article_data.get("url", ""),
                    published_at=article_data.get("published_at", datetime.utcnow()),
                    summary=article_data.get("summary"),
                    author=article_data.get("author"),
                    image_url=article_data.get("image_url"),
                    source_id=article_data.get("source_id"),
                )
                successful += 1
            except Exception as e:
                logger.error(f"❌ Error ingesting article: {str(e)}")
                failed += 1

        logger.info(f"📊 Ingestion complete: {successful} successful, {failed} failed")
        return successful, failed

    @staticmethod
    async def process_articles_sentiment(db: Session, limit: int = 100) -> int:
        """Process articles for sentiment analysis
        
        Args:
            db: Database session
            limit: Maximum articles to process
            
        Returns:
            Number of processed articles
        """
        articles = ArticleService.get_pending_articles(db, limit=limit)
        processed = 0

        for article in articles:
            try:
                # Update status to processing
                ArticleService.update_article_status(
                    db, article.id, ArticleStatus.PROCESSING
                )

                # Analyze sentiment
                text_to_analyze = f"{article.title}. {article.content[:500]}"
                sentiment, score = sentiment_service.analyze_sentiment(text_to_analyze)

                # Update article
                ArticleService.update_article_sentiment(
                    db, article.id, sentiment, score
                )

                # Mark as completed
                ArticleService.update_article_status(
                    db, article.id, ArticleStatus.COMPLETED
                )

                processed += 1
                logger.debug(f"Processed article {article.id}: {sentiment}")
            except Exception as e:
                logger.error(f"❌ Error processing article {article.id}: {str(e)}")
                ArticleService.update_article_status(
                    db, article.id, ArticleStatus.FAILED, str(e)
                )

        logger.info(f"✅ Sentiment processing complete: {processed} articles")
        return processed
