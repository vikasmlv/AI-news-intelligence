"""Logging Configuration and Setup"""

import logging
import json
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup application logging with JSON formatting
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with JSON formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # JSON formatter
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(timestamp)s %(level)s %(name)s %(message)s"
    )
    console_handler.setFormatter(json_formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name: Logger name
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
