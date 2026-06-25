"""NewsAPI.org Connector"""

import logging
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from src.services.news_sources.base import BaseNewsConnector

logger = logging.getLogger(__name__)


class NewsAPIConnector(BaseNewsConnector):
    """NewsAPI.org news source connector"""

    BASE_URL = "https://newsapi.org/v2"

    async def fetch_articles(self, query: str = "", country: str = "us") -> List[Dict]:
        """Fetch articles from NewsAPI
        
        Args:
            query: Search query
            country: Country code (e.g., 'us', 'gb')
            
        Returns:
            List of articles
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Try top-headlines endpoint first
                url = f"{self.BASE_URL}/top-headlines"
                params = {
                    "country": country,
                    "apiKey": self.api_key,
                    "pageSize": 100,
                    "sortBy": "publishedAt",
                }

                if query:
                    url = f"{self.BASE_URL}/everything"
                    params["q"] = query
                    params["sortBy"] = "relevancy"

                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])
                        logger.info(f"✅ Fetched {len(articles)} articles from NewsAPI")
                        return [self._normalize_newsapi_article(a) for a in articles]
                    else:
                        logger.error(f"NewsAPI error: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"❌ Error fetching from NewsAPI: {str(e)}")
            return []

    async def get_article_details(self, article_id: str) -> Optional[Dict]:
        """NewsAPI doesn't support fetching individual articles"""
        return None

    def _normalize_newsapi_article(self, article: Dict) -> Dict:
        """Normalize NewsAPI article format"""
        return {
            "title": article.get("title"),
            "content": article.get("content"),
            "summary": article.get("description"),
            "source": article.get("source", {}).get("name", "NewsAPI"),
            "url": article.get("url"),
            "author": article.get("author"),
            "published_at": article.get("publishedAt"),
            "image_url": article.get("urlToImage"),
            "source_id": article.get("url"),  # Use URL as unique ID
        }
