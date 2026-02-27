"""Message processing module for validating and preparing activity messages."""

from typing import List, Tuple

from ..models.message import (
    ActivityMessage,
    MessageValidationResult,
)
from ..utils import (
    ContentSanitizer,
    LoggerMixin,
    MessageValidator,
    expand_abbreviations,
    get_logger,
    log_execution_time,
)
from ..utils.exceptions import (
    MessageSanitizationError,
)


class MessageProcessor(LoggerMixin):
    """
    Processes and validates Walmart activity messages.
    
    This class handles:
    - Message validation (length, content, format)
    - Content sanitization (HTML stripping, XSS prevention)
    - Abbreviation expansion
    - Profanity filtering
    - Metadata extraction
    
    Attributes:
        validator: Message validator instance
        sanitizer: Content sanitizer instance
        walmart_terms: Dictionary of Walmart-specific abbreviations
    
    Example:
        >>> processor = MessageProcessor()
        >>> message = ActivityMessage(
        ...     id="msg_001",
        ...     content="Complete CBL by Friday",
        ...     sender="Training Team"
        ... )
        >>> result = processor.process(message)
        >>> print(result.is_valid)
        True
    """
    
    def __init__(
        self,
        min_message_length: int = 10,
        max_message_length: int = 500,
        enable_profanity_filter: bool = True,
        expand_walmart_abbreviations: bool = True,
        walmart_terms: dict = None
    ):
        """
        Initialize message processor.
        
        Args:
            min_message_length: Minimum message length
            max_message_length: Maximum message length
            enable_profanity_filter: Enable profanity checking
            expand_walmart_abbreviations: Expand Walmart abbreviations
            walmart_terms: Custom abbreviation dictionary
        """
        self.validator = MessageValidator(
            min_length=min_message_length,
            max_length=max_message_length,
            profanity_check=enable_profanity_filter
        )
        self.sanitizer = ContentSanitizer()
        self.expand_walmart_abbreviations = expand_walmart_abbreviations
        self.walmart_terms = walmart_terms or {
            "GWP": "Great Workplace",
            "OBW": "One Best Way",
            "CBL": "Computer Based Learning",
            "PTO": "Paid Time Off",
            "SM": "Store Manager",
            "ASM": "Assistant Store Manager",
            "AP": "Asset Protection",
            "TLE": "Tire and Lube Express",
        }
        
        self.logger.info(
            "message_processor_initialized",
            min_length=min_message_length,
            max_length=max_message_length,
            profanity_filter=enable_profanity_filter
        )
    
    @log_execution_time(get_logger("MessageProcessor"))
    def process(self, message: ActivityMessage) -> MessageValidationResult:
        """
        Process and validate an activity message.
        
        This method performs the complete message processing pipeline:
        1. Content sanitization
        2. Validation checks
        3. Abbreviation expansion (if enabled)
        4. Warning generation
        
        Args:
            message: Activity message to process
        
        Returns:
            MessageValidationResult: Validation result with sanitized content
            
        Raises:
            MessageValidationError: If message fails critical validation
            
        Example:
            >>> message = ActivityMessage(id="1", content="Test message", sender="System")
            >>> result = processor.process(message)
            >>> print(result.sanitized_content)
        """
        self.logger.info(
            "processing_message",
            message_id=message.id,
            category=message.category,
            priority=message.priority
        )
        
        errors = []
        warnings = []
        
        try:
            # Step 1: Sanitize content
            sanitized_content = self.sanitizer.sanitize(message.content)
            
            if not sanitized_content:
                errors.append("Message content is empty after sanitization")
                self.logger.warning(
                    "empty_after_sanitization",
                    message_id=message.id,
                    original=message.content[:50]
                )
            
            # Step 2: Validate sanitized content
            is_valid, validation_errors = self.validator.validate(sanitized_content)
            errors.extend(validation_errors)
            
            # Step 3: Expand abbreviations if enabled
            if self.expand_walmart_abbreviations and sanitized_content:
                original_content = sanitized_content
                sanitized_content = expand_abbreviations(
                    sanitized_content,
                    self.walmart_terms
                )
                
                # Track which abbreviations were expanded
                if sanitized_content != original_content:
                    expanded_abbrs = self._find_expanded_abbreviations(
                        original_content,
                        sanitized_content
                    )
                    if expanded_abbrs:
                        warnings.append(
                            f"Expanded abbreviations: {', '.join(expanded_abbrs)}"
                        )
                        self.logger.debug(
                            "abbreviations_expanded",
                            message_id=message.id,
                            abbreviations=expanded_abbrs
                        )
            
            # Step 4: Additional content checks
            content_warnings = self._check_content_quality(sanitized_content)
            warnings.extend(content_warnings)
            
            # Create validation result
            result = MessageValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                sanitized_content=sanitized_content if len(errors) == 0 else None
            )
            
            self.logger.info(
                "message_processed",
                message_id=message.id,
                is_valid=result.is_valid,
                error_count=len(errors),
                warning_count=len(warnings)
            )
            
            return result
            
        except Exception as e:
            self.logger.error(
                "processing_failed",
                message_id=message.id,
                error=str(e),
                exc_info=True
            )
            raise MessageSanitizationError(
                f"Failed to process message: {str(e)}",
                details={"message_id": message.id}
            )
    
    def validate_only(self, content: str) -> Tuple[bool, List[str]]:
        """
        Validate message content without sanitization.
        
        Useful for quick validation checks without modifying content.
        
        Args:
            content: Message content to validate
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
            
        Example:
            >>> is_valid, errors = processor.validate_only("Short")
            >>> print(is_valid, errors)
            False ['Message too short...']
        """
        return self.validator.validate(content)
    
    def sanitize_only(self, content: str) -> str:
        """
        Sanitize message content without validation.
        
        Useful for cleaning content before validation or storage.
        
        Args:
            content: Message content to sanitize
        
        Returns:
            str: Sanitized content
            
        Example:
            >>> clean = processor.sanitize_only("<script>alert('xss')</script>Hello")
            >>> print(clean)
            Hello
        """
        return self.sanitizer.sanitize(content)
    
    def _find_expanded_abbreviations(
        self,
        original: str,
        expanded: str
    ) -> List[str]:
        """
        Find which abbreviations were expanded.
        
        Args:
            original: Original content
            expanded: Content after expansion
        
        Returns:
            List[str]: List of abbreviations that were expanded
        """
        expanded_abbrs = []
        
        for abbr in self.walmart_terms.keys():
            if abbr in original and abbr not in expanded:
                expanded_abbrs.append(abbr)
        
        return expanded_abbrs
    
    def _check_content_quality(self, content: str) -> List[str]:
        """
        Check content quality and generate warnings.
        
        Args:
            content: Content to check
        
        Returns:
            List[str]: List of quality warnings
        """
        warnings = []
        
        if not content:
            return warnings
        
        # Check for all caps (shouting)
        if content.isupper() and len(content) > 10:
            warnings.append("Message is in all caps")
        
        # Check for excessive exclamation marks
        exclamation_count = content.count('!')
        if exclamation_count > 3:
            warnings.append(f"Excessive exclamation marks ({exclamation_count})")
        
        # Check for very short sentences
        words = content.split()
        if len(words) < 5:
            warnings.append("Message is very brief")
        
        # Check for missing punctuation
        if not content.rstrip().endswith(('.', '!', '?')):
            warnings.append("Message missing ending punctuation")
        
        return warnings
    
    def extract_metadata(self, message: ActivityMessage) -> dict:
        """
        Extract metadata from message for analytics.
        
        Args:
            message: Activity message
        
        Returns:
            dict: Extracted metadata
            
        Example:
            >>> metadata = processor.extract_metadata(message)
            >>> print(metadata['word_count'])
        """
        content = message.content
        
        metadata = {
            "word_count": len(content.split()),
            "character_count": len(content),
            "sentence_count": content.count('.') + content.count('!') + content.count('?'),
            "has_urls": bool(self.validator._extract_urls(content)),
            "has_html": self.validator._contains_html(content),
            "category": message.category.value,
            "priority": message.priority.value,
            "created_at": message.created_at.isoformat(),
        }
        
        return metadata
