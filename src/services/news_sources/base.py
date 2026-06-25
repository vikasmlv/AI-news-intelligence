"""Base News Source Connector"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseNewsConnector(ABC):
    """Base class for news source connectors"""

    def __init__(self, api_key: str):
        """Initialize connector
        
        Args:
            api_key: API key for the news source
        """
        self.api_key = api_key
        self.source_name = self.__class__.__name__

    @abstractmethod
    async def fetch_articles(self, query: str = "") -> List[Dict]:
        """Fetch articles from source
        
        Args:
            query: Search query (optional)
            
        Returns:
            List of article dictionaries
        """
        pass

    @abstractmethod
    async def get_article_details(self, article_id: str) -> Optional[Dict]:
        """Get detailed article information
        
        Args:
            article_id: Article identifier
            
        Returns:
            Article details dictionary or None
        """
        pass

    def _normalize_article(self, article: Dict) -> Dict:
        """Normalize article to standard format
        
        Args:
            article: Raw article from API
            
        Returns:
            Normalized article dictionary
        """
        return {
            "title": article.get("title"),
            "content": article.get("content") or article.get("description"),
            "summary": article.get("summary"),
            "source": article.get("source") or self.source_name,
            "url": article.get("url"),
            "author": article.get("author"),
            "published_at": article.get("published_at") or datetime.utcnow(),
            "image_url": article.get("image_url") or article.get("urlToImage"),
            "source_id": article.get("source_id"),
        }
