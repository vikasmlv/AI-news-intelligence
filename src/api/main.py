"""FastAPI Application Configuration and Setup"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.api.routes import articles, health, sentiment, topics
from src.core.config import settings
from src.core.logging import setup_logging

# Setup logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup/shutdown events"""
    logger.info("🚀 Starting AI News Intelligence Platform")
    
    # Startup
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down AI News Intelligence Platform")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="AI News Intelligence Platform",
        description="Distributed microservice system for news ingestion, LLM-based summarization, sentiment analysis",
        version="0.1.0",
        docs_url="/api/v1/docs",
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan,
    )

    # Middleware Setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
    )

    # API Routes
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(articles.router, prefix="/api/v1", tags=["Articles"])
    app.include_router(sentiment.router, prefix="/api/v1", tags=["Sentiment"])
    app.include_router(topics.router, prefix="/api/v1", tags=["Topics"])

    logger.info("✅ FastAPI application initialized successfully")
    
    return app


# Create app instance
app = create_app()
