"""Custom exceptions for Zorro video generation system."""


class ZorroBaseException(Exception):
    """Base exception for all Zorro errors."""
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


# Message Processing Exceptions
class MessageProcessingError(ZorroBaseException):
    """Base exception for message processing errors."""
    pass


class MessageValidationError(MessageProcessingError):
    """Raised when message validation fails."""
    pass


class MessageSanitizationError(MessageProcessingError):
    """Raised when message sanitization fails."""
    pass


class MessageTooShortError(MessageValidationError):
    """Raised when message is below minimum length."""
    pass


class MessageTooLongError(MessageValidationError):
    """Raised when message exceeds maximum length."""
    pass


class ProfanityDetectedError(MessageValidationError):
    """Raised when profanity is detected in message."""
    pass


# Prompt Generation Exceptions
class PromptGenerationError(ZorroBaseException):
    """Base exception for prompt generation errors."""
    pass


class LLMServiceError(PromptGenerationError):
    """Raised when LLM service fails."""
    pass


class LLMTimeoutError(LLMServiceError):
    """Raised when LLM request times out."""
    pass


class LLMRateLimitError(LLMServiceError):
    """Raised when LLM rate limit is exceeded."""
    pass


class LLMAuthenticationError(LLMServiceError):
    """Raised when LLM authentication fails."""
    pass


class InvalidPromptError(PromptGenerationError):
    """Raised when generated prompt is invalid."""
    pass


# Video Generation Exceptions
class VideoGenerationError(ZorroBaseException):
    """Base exception for video generation errors."""
    pass


class ModelLoadError(VideoGenerationError):
    """Raised when video generation model fails to load."""
    pass


class InsufficientResourcesError(VideoGenerationError):
    """Raised when insufficient GPU/CPU resources."""
    pass


class VideoRenderError(VideoGenerationError):
    """Raised when video rendering fails."""
    pass


class InvalidVideoParametersError(VideoGenerationError):
    """Raised when video generation parameters are invalid."""
    pass


# Video Editing Exceptions
class VideoEditingError(ZorroBaseException):
    """Base exception for video editing errors."""
    pass


class VideoFileNotFoundError(VideoEditingError):
    """Raised when video file is not found."""
    pass


class VideoCorruptedError(VideoEditingError):
    """Raised when video file is corrupted."""
    pass


class UnsupportedFormatError(VideoEditingError):
    """Raised when video format is not supported."""
    pass


class EditOperationError(VideoEditingError):
    """Raised when a video edit operation fails."""
    pass


# Accessibility Exceptions
class AccessibilityError(ZorroBaseException):
    """Base exception for accessibility enhancement errors."""
    pass


class CaptionGenerationError(AccessibilityError):
    """Raised when caption generation fails."""
    pass


class AudioDescriptionError(AccessibilityError):
    """Raised when audio description generation fails."""
    pass


class TTSError(AccessibilityError):
    """Raised when text-to-speech conversion fails."""
    pass


class ContrastValidationError(AccessibilityError):
    """Raised when contrast ratio validation fails."""
    pass


# Configuration Exceptions
class ConfigurationError(ZorroBaseException):
    """Base exception for configuration errors."""
    pass


class MissingConfigError(ConfigurationError):
    """Raised when required configuration is missing."""
    pass


class InvalidConfigError(ConfigurationError):
    """Raised when configuration is invalid."""
    pass


class MissingAPIKeyError(ConfigurationError):
    """Raised when required API key is missing."""
    pass


# File System Exceptions
class FileSystemError(ZorroBaseException):
    """Base exception for file system errors."""
    pass


class OutputDirectoryError(FileSystemError):
    """Raised when output directory operations fail."""
    pass


class DiskSpaceError(FileSystemError):
    """Raised when insufficient disk space."""
    pass


class FilePermissionError(FileSystemError):
    """Raised when file permission is denied."""
    pass


# Pipeline Exceptions
class PipelineError(ZorroBaseException):
    """Base exception for pipeline orchestration errors."""
    pass


class StepExecutionError(PipelineError):
    """Raised when a pipeline step fails."""
    pass


class PipelineTimeoutError(PipelineError):
    """Raised when pipeline execution times out."""
    pass


class DependencyError(PipelineError):
    """Raised when pipeline step dependency is not met."""
    pass
