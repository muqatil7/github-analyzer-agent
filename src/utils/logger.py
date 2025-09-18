"""Structured logging configuration for GitHub Analyzer Agent."""

import os
import sys
import logging
from typing import Optional
import structlog
from structlog.typing import FilteringBoundLogger


def setup_logging(log_level: Optional[str] = None, log_format: Optional[str] = None) -> None:
    """Setup structured logging with proper configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format (structured, json, simple)
    """
    # Get configuration from environment or use defaults
    log_level = log_level or os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = log_format or os.getenv("LOG_FORMAT", "structured").lower()
    
    # Configure structlog
    if log_format == "json":
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ]
    elif log_format == "simple":
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:  # structured (default)
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(colors=True, exception_formatter=structlog.dev.better_traceback)
        ]
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level)
    )
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level)),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> FilteringBoundLogger:
    """Get a structured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


# Default logger instance
logger = get_logger(__name__)