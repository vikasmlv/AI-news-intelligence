"""Database Configuration and Session Management"""

import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, QueuePool
from src.core.config import settings
from src.models.base import Base

logger = logging.getLogger(__name__)

# Database URL
DATABASE_URL = settings.DATABASE_URL

# Create engine with connection pooling
if settings.APP_ENV == "production":
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,
        echo=False,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Enable foreign key constraints for SQLite (development only)"""
    if "sqlite" in DATABASE_URL:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing database: {str(e)}")
        raise


def drop_db() -> None:
    """Drop all database tables (for development/testing)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("⚠️ All database tables dropped")
    except Exception as e:
        logger.error(f"❌ Error dropping database: {str(e)}")
        raise
