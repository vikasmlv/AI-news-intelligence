"""Logging configuration and utilities."""

import logging
import json
from typing import Optional
from datetime import datetime

from pythonjsonlogger import jsonlogger

from src.config import get_settings


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Setup application logger with JSON formatting.

    Args:
        name: Logger name (typically __name__)
        level: Log level (defaults to settings.log_level)

    Returns:
        Configured logger instance
    """
    settings = get_settings()
    logger = logging.getLogger(name)
    logger.setLevel(level or settings.log_level)

    # Console handler with JSON formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level or settings.log_level)

    # JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s',
        timestamp=True,
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger(__name__)
