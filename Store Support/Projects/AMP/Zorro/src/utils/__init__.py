"""Utility functions and helpers package."""

from .config import Config, get_config, set_config
from .exceptions import (
    AccessibilityError,
    ConfigurationError,
    InvalidConfigError,
    LLMRateLimitError,
    LLMServiceError,
    LLMTimeoutError,
    MessageProcessingError,
    MessageValidationError,
    MissingConfigError,
    PromptGenerationError,
    VideoEditingError,
    VideoGenerationError,
    ZorroBaseException,
)
from .logger import (
    LoggerMixin,
    get_correlation_id,
    get_logger,
    log_execution_time,
    log_function_call,
    set_correlation_id,
    setup_logging,
)
from .settings import Settings, get_settings, settings
from .validators import (
    ContentSanitizer,
    MessageValidator,
    expand_abbreviations,
    is_safe_filename,
    validate_email,
    validate_url,
)

__all__ = [
    # Config
    "Config",
    "get_config",
    "set_config",
    # Settings (new centralized config)
    "settings",
    "get_settings",
    "Settings",
    # Logging
    "setup_logging",
    "get_logger",
    "LoggerMixin",
    "log_function_call",
    "log_execution_time",
    "get_correlation_id",
    "set_correlation_id",
    # Validators
    "MessageValidator",
    "ContentSanitizer",
    "expand_abbreviations",
    "validate_url",
    "validate_email",
    "is_safe_filename",
    # Exceptions
    "ZorroBaseException",
    "MessageProcessingError",
    "MessageValidationError",
    "PromptGenerationError",
    "VideoGenerationError",
    "VideoEditingError",
    "AccessibilityError",
    "ConfigurationError",
    "MissingConfigError",
    "InvalidConfigError",
    "LLMServiceError",
    "LLMTimeoutError",
    "LLMRateLimitError",
]
