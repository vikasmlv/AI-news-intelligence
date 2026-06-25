"""Sentiment Analysis Service"""

import logging
from typing import Tuple

try:
    from transformers import pipeline
except ImportError:
    pipeline = None

logger = logging.getLogger(__name__)


class SentimentService:
    """Service for sentiment analysis"""

    def __init__(self):
        """Initialize sentiment analyzer"""
        try:
            if pipeline:
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english"
                )
                logger.info("✅ Sentiment analyzer loaded")
            else:
                self.sentiment_pipeline = None
                logger.warning("⚠️ Transformers not installed, sentiment analysis disabled")
        except Exception as e:
            logger.error(f"❌ Error loading sentiment analyzer: {str(e)}")
            self.sentiment_pipeline = None

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (sentiment, confidence_score)
        """
        if not self.sentiment_pipeline:
            logger.warning("Sentiment analyzer not available")
            return "neutral", 0.5

        try:
            # Truncate text to avoid length issues
            text = text[:512]

            result = self.sentiment_pipeline(text)[0]
            label = result["label"].lower()  # POSITIVE, NEGATIVE
            score = result["score"]

            # Map to sentiment
            sentiment = "positive" if label == "positive" else "negative"

            logger.debug(f"Sentiment analysis: {sentiment} ({score:.2f})")
            return sentiment, score
        except Exception as e:
            logger.error(f"❌ Error analyzing sentiment: {str(e)}")
            return "neutral", 0.5

    def batch_analyze_sentiment(self, texts: list) -> list:
        """Analyze sentiment for multiple texts"""
        if not self.sentiment_pipeline:
            return [{"sentiment": "neutral", "score": 0.5} for _ in texts]

        results = []
        for text in texts:
            sentiment, score = self.analyze_sentiment(text)
            results.append({"sentiment": sentiment, "score": score})
        return results


# Global instance
sentiment_service = SentimentService()
