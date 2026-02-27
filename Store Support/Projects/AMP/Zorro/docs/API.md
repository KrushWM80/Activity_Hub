# Zorro Video Generation System

## API Documentation

### Table of Contents
- [Core Classes](#core-classes)
- [Models](#models)
- [Services](#services)
- [Utilities](#utilities)
- [Error Handling](#error-handling)

---

## Core Classes

### MessageProcessor

Processes and validates Walmart activity messages.

#### Constructor

```python
MessageProcessor(
    min_message_length: int = 10,
    max_message_length: int = 500,
    enable_profanity_filter: bool = True,
    expand_walmart_abbreviations: bool = True,
    walmart_terms: dict = None
)
```

#### Methods

##### process(message: ActivityMessage) -> MessageValidationResult

Process and validate an activity message.

**Parameters:**
- `message` (ActivityMessage): The message to process

**Returns:**
- `MessageValidationResult`: Validation result with sanitized content

**Example:**
```python
processor = MessageProcessor()
message = ActivityMessage(
    id="msg_001",
    content="Complete your CBL by Friday",
    sender="Training Team"
)
result = processor.process(message)
print(result.sanitized_content)
```

##### validate_only(content: str) -> Tuple[bool, List[str]]

Validate message content without sanitization.

**Parameters:**
- `content` (str): Content to validate

**Returns:**
- `Tuple[bool, List[str]]`: (is_valid, list_of_errors)

---

### PromptGenerator

Generates enhanced video prompts from activity messages using LLM.

#### Constructor

```python
PromptGenerator(
    llm_service: Optional[Any] = None,
    fallback_enabled: bool = True
)
```

#### Methods

##### generate(message: ActivityMessage, sanitized_content: Optional[str] = None) -> PromptGenerationResult

Generate enhanced video prompt from activity message.

**Parameters:**
- `message` (ActivityMessage): Message to convert
- `sanitized_content` (Optional[str]): Pre-sanitized content

**Returns:**
- `PromptGenerationResult`: Generation result with prompt

**Example:**
```python
generator = PromptGenerator()
message = ActivityMessage(...)
result = generator.generate(message)
if result.success:
    print(result.prompt.enhanced_prompt)
```

---

## Models

### ActivityMessage

Represents a Walmart activity message.

**Fields:**
- `id` (str): Unique identifier
- `content` (str): Message text (10-500 chars)
- `category` (MessageCategory): Message category
- `priority` (MessagePriority): Priority level
- `sender` (str): Message sender
- `target_audience` (str): Intended recipients
- `metadata` (Dict): Additional metadata
- `created_at` (datetime): Creation timestamp

**Example:**
```python
message = ActivityMessage(
    id="msg_001",
    content="Complete safety training",
    category=MessageCategory.TRAINING,
    priority=MessagePriority.HIGH,
    sender="Safety Team"
)
```

### VideoPrompt

Enhanced prompt for video generation.

**Fields:**
- `original_message` (str): Source message
- `enhanced_prompt` (str): LLM-enhanced prompt
- `style` (PromptStyle): Visual style
- `mood` (PromptMood): Emotional tone
- `keywords` (List[str]): Key terms
- `duration_hint` (int): Suggested duration
- `negative_prompt` (Optional[str]): Elements to avoid
- `metadata` (Dict): Additional parameters

### GeneratedVideo

Represents a generated video output.

**Fields:**
- `id` (str): Unique identifier
- `path` (str): File path
- `status` (GenerationStatus): Status
- `metadata` (Optional[VideoMetadata]): Technical metadata
- `accessibility` (Optional[AccessibilityMetadata]): Accessibility features
- `generation_time` (float): Generation time in seconds

**Properties:**
- `duration`: Video duration from metadata
- `file_size_mb`: File size in MB
- `is_accessible`: Check if accessibility features present

---

## Services

### LLMService

Service for interacting with Large Language Models.

#### Constructor

```python
LLMService(
    provider: Optional[str] = None,  # "openai", "anthropic", "azure"
    api_key: Optional[str] = None
)
```

#### Methods

##### generate(system_prompt: str, user_prompt: str, max_tokens: int, temperature: float) -> str

Generate text using LLM.

**Parameters:**
- `system_prompt` (str): System/context prompt
- `user_prompt` (str): User query
- `max_tokens` (Optional[int]): Max tokens to generate
- `temperature` (Optional[float]): Sampling temperature

**Returns:**
- `str`: Generated text

**Raises:**
- `LLMServiceError`: On generation failure
- `LLMTimeoutError`: On timeout
- `LLMRateLimitError`: On rate limit

**Example:**
```python
service = LLMService()
response = service.generate(
    system_prompt="You are an expert",
    user_prompt="Create a video prompt",
    max_tokens=500,
    temperature=0.7
)
```

---

## Utilities

### Configuration

#### get_config(reload: bool = False) -> Config

Get global configuration instance.

**Example:**
```python
from src.utils import get_config

config = get_config()
print(config.get("video.default_fps"))
```

#### Config Methods

- `get(key: str, default: Any) -> Any`: Get config value by dot-notation
- `get_api_key(service: str) -> str`: Get API key from environment
- `is_development: bool`: Check if dev environment
- `is_production: bool`: Check if prod environment

### Logging

#### setup_logging(level: str, log_format: str, output_dir: str)

Configure structured logging.

**Example:**
```python
from src.utils import setup_logging, get_logger

setup_logging(level="INFO", log_format="json", output_dir="logs")
logger = get_logger(__name__)
logger.info("application_started")
```

### Validators

#### MessageValidator

Validator for activity messages.

**Methods:**
- `validate(message: str) -> Tuple[bool, List[str]]`: Validate message

#### ContentSanitizer

Sanitize message content.

**Methods:**
- `sanitize(message: str) -> str`: Sanitize and clean content

---

## Error Handling

### Exception Hierarchy

```
ZorroBaseException
├── MessageProcessingError
│   ├── MessageValidationError
│   │   ├── MessageTooShortError
│   │   ├── MessageTooLongError
│   │   └── ProfanityDetectedError
│   └── MessageSanitizationError
├── PromptGenerationError
│   ├── LLMServiceError
│   │   ├── LLMTimeoutError
│   │   ├── LLMRateLimitError
│   │   └── LLMAuthenticationError
│   └── InvalidPromptError
├── VideoGenerationError
├── VideoEditingError
├── AccessibilityError
└── ConfigurationError
    ├── MissingConfigError
    └── InvalidConfigError
```

### Error Handling Example

```python
from src.utils.exceptions import MessageValidationError, LLMServiceError

try:
    result = processor.process(message)
    if not result.is_valid:
        # Handle validation errors
        for error in result.errors:
            logger.error(f"Validation error: {error}")
except MessageValidationError as e:
    logger.error(f"Validation failed: {e.message}", extra=e.details)
except LLMServiceError as e:
    logger.error(f"LLM service failed: {e.message}")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
```

---

## Complete Usage Example

```python
from src.models import ActivityMessage, MessageCategory, MessagePriority
from src.core import MessageProcessor, PromptGenerator
from src.utils import setup_logging, get_logger

# Setup
setup_logging(level="INFO")
logger = get_logger(__name__)

# Create message
message = ActivityMessage(
    id="example_001",
    content="Complete your safety training CBL by Friday",
    category=MessageCategory.TRAINING,
    priority=MessagePriority.HIGH,
    sender="Safety Team"
)

# Process message
processor = MessageProcessor()
validation_result = processor.process(message)

if validation_result.is_valid:
    # Generate prompt
    generator = PromptGenerator()
    prompt_result = generator.generate(
        message,
        sanitized_content=validation_result.sanitized_content
    )
    
    if prompt_result.success:
        prompt = prompt_result.prompt
        logger.info(f"Generated prompt: {prompt.enhanced_prompt}")
        
        # Continue with video generation...
```

---

## Configuration Reference

See `config/config.yaml` for all available configuration options.

Key configuration sections:
- `app`: Application settings
- `video`: Video generation parameters
- `llm`: LLM service configuration
- `accessibility`: Accessibility features
- `logging`: Logging configuration
- `security`: Security settings
