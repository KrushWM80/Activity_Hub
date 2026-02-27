"""Logging configuration and utilities for Zorro."""

import contextvars
import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import structlog
from pythonjsonlogger import jsonlogger

# Context variable for correlation ID (thread-safe)
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    'correlation_id', default=''
)


def get_correlation_id() -> str:
    """Get current correlation ID or generate a new one."""
    cid = correlation_id_var.get()
    if not cid:
        cid = str(uuid.uuid4())[:8]
        correlation_id_var.set(cid)
    return cid


def set_correlation_id(cid: str) -> None:
    """Set correlation ID for current context."""
    correlation_id_var.set(cid)


def add_correlation_id(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Structlog processor to add correlation ID to all log messages."""
    event_dict['correlation_id'] = get_correlation_id()
    return event_dict


def add_service_context(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add standard service context to log messages."""
    event_dict.setdefault('service', 'zorro')
    event_dict.setdefault('version', '1.0.0')
    return event_dict


def setup_logging(
    level: str = "INFO",
    log_format: str = "json",
    output_dir: Optional[str] = None,
    service_name: str = "zorro"
) -> None:
    """
    Configure structured logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format type ("json" or "text")
        output_dir: Directory for log files. If None, logs to stdout only.
        service_name: Name of the service for log context
    
    Example:
        >>> setup_logging(level="DEBUG", log_format="json", output_dir="logs")
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create output directory if specified
    if output_dir:
        log_path = Path(output_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        log_file = log_path / f"{service_name}_{datetime.now():%Y%m%d}.log"
    
    # Configure structlog with correlation ID support
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            add_correlation_id,  # Add correlation ID to all logs
            add_service_context,  # Add service context
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if log_format == "json" 
            else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    
    if log_format == "json":
        console_formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # File handler
    if output_dir:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        
        if log_format == "json":
            file_formatter = jsonlogger.JsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s'
            )
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        handlers=handlers
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__ of the module)
    
    Returns:
        structlog.BoundLogger: Configured logger instance
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("processing_started", message_id="msg_001")
    """
    return structlog.get_logger(name)


class LoggerMixin:
    """
    Mixin class to add logging capability to any class.
    
    Usage:
        >>> class MyService(LoggerMixin):
        ...     def process(self):
        ...         self.logger.info("processing", item="data")
    """
    
    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger instance for this class."""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger


def log_function_call(logger: structlog.BoundLogger):
    """
    Decorator to log function calls with parameters and results.
    
    Args:
        logger: Logger instance to use
        
    Example:
        >>> logger = get_logger(__name__)
        >>> @log_function_call(logger)
        ... def my_function(x, y):
        ...     return x + y
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(
                "function_called",
                function=func.__name__,
                args=args,
                kwargs=kwargs
            )
            try:
                result = func(*args, **kwargs)
                logger.debug(
                    "function_completed",
                    function=func.__name__,
                    result=result
                )
                return result
            except Exception as e:
                logger.error(
                    "function_failed",
                    function=func.__name__,
                    error=str(e),
                    exc_info=True
                )
                raise
        return wrapper
    return decorator


def log_execution_time(logger: structlog.BoundLogger):
    """
    Decorator to log function execution time.
    
    Args:
        logger: Logger instance to use
        
    Example:
        >>> logger = get_logger(__name__)
        >>> @log_execution_time(logger)
        ... def slow_function():
        ...     time.sleep(2)
    """
    import time
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(
                    "execution_completed",
                    function=func.__name__,
                    execution_time=f"{execution_time:.2f}s"
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    "execution_failed",
                    function=func.__name__,
                    execution_time=f"{execution_time:.2f}s",
                    error=str(e)
                )
                raise
        return wrapper
    return decorator
