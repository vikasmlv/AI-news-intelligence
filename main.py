#!/usr/bin/env python
"""Run the application"""

import uvicorn
import logging
from src.core.config import settings
from src.core.database import init_db

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Run server
    uvicorn.run(
        "src.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        workers=settings.API_WORKERS if settings.APP_ENV == "production" else 1,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
