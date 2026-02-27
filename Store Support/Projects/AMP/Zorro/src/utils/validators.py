"""Validation utilities for Zorro video generation system."""

import re
from typing import List, Optional, Tuple

import bleach
import validators

# Common profanity list (basic set - expand as needed)
PROFANITY_LIST = {
    # Add appropriate terms based on your organization's standards
    # This is a minimal example
    "damn", "hell", "crap"
}


class MessageValidator:
    """
    Validator for activity messages.
    
    Provides comprehensive validation including:
    - Length validation
    - Content filtering (profanity, sensitive content)
    - Format validation
    - URL validation
    - Special character handling
    """
    
    def __init__(
        self,
        min_length: int = 10,
        max_length: int = 500,
        allow_urls: bool = False,
        allow_html: bool = False,
        profanity_check: bool = True
    ):
        """
        Initialize message validator.
        
        Args:
            min_length: Minimum message length
            max_length: Maximum message length
            allow_urls: Whether to allow URLs in messages
            allow_html: Whether to allow HTML tags
            profanity_check: Whether to check for profanity
        """
        self.min_length = min_length
        self.max_length = max_length
        self.allow_urls = allow_urls
        self.allow_html = allow_html
        self.profanity_check = profanity_check
    
    def validate(self, message: str) -> Tuple[bool, List[str]]:
        """
        Validate a message.
        
        Args:
            message: Message content to validate
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
            
        Example:
            >>> validator = MessageValidator()
            >>> is_valid, errors = validator.validate("Complete training by Friday")
            >>> print(is_valid)
            True
        """
        errors = []
        
        # Length validation
        if len(message) < self.min_length:
            errors.append(
                f"Message too short. Minimum length: {self.min_length}"
            )
        
        if len(message) > self.max_length:
            errors.append(
                f"Message too long. Maximum length: {self.max_length}"
            )
        
        # Profanity check
        if self.profanity_check:
            profanity_found = self._check_profanity(message)
            if profanity_found:
                errors.append(f"Inappropriate language detected: {profanity_found}")
        
        # URL validation
        if not self.allow_urls:
            urls = self._extract_urls(message)
            if urls:
                errors.append(f"URLs not allowed: {', '.join(urls)}")
        
        # HTML validation
        if not self.allow_html:
            if self._contains_html(message):
                errors.append("HTML tags not allowed")
        
        # Check for excessive special characters
        if self._has_excessive_special_chars(message):
            errors.append("Message contains too many special characters")
        
        return len(errors) == 0, errors
    
    def _check_profanity(self, message: str) -> Optional[str]:
        """
        Check for profanity in message.
        
        Args:
            message: Message to check
        
        Returns:
            Optional[str]: First profane word found, or None
        """
        words = message.lower().split()
        for word in words:
            # Remove punctuation for checking
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word in PROFANITY_LIST:
                return word
        return None
    
    def _extract_urls(self, message: str) -> List[str]:
        """
        Extract URLs from message.
        
        Args:
            message: Message to check
        
        Returns:
            List[str]: List of URLs found
        """
        # Simple URL pattern
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, message)
        return urls
    
    def _contains_html(self, message: str) -> bool:
        """
        Check if message contains HTML tags.
        
        Args:
            message: Message to check
        
        Returns:
            bool: True if HTML detected
        """
        html_pattern = r'<[^>]+>'
        return bool(re.search(html_pattern, message))
    
    def _has_excessive_special_chars(self, message: str, threshold: float = 0.3) -> bool:
        """
        Check if message has too many special characters.
        
        Args:
            message: Message to check
            threshold: Maximum ratio of special chars to total chars
        
        Returns:
            bool: True if excessive special characters
        """
        if not message:
            return False
        
        special_chars = sum(1 for char in message if not char.isalnum() and not char.isspace())
        ratio = special_chars / len(message)
        
        return ratio > threshold


class ContentSanitizer:
    """
    Sanitize message content for security and consistency.
    
    Provides:
    - HTML stripping/escaping
    - Script injection prevention
    - Whitespace normalization
    - Character encoding normalization
    """
    
    def __init__(self, aggressive: bool = False):
        """
        Initialize content sanitizer.
        
        Args:
            aggressive: Use aggressive sanitization (strips more content)
        """
        self.aggressive = aggressive
    
    def sanitize(self, message: str) -> str:
        """
        Sanitize message content.
        
        Args:
            message: Message to sanitize
        
        Returns:
            str: Sanitized message
            
        Example:
            >>> sanitizer = ContentSanitizer()
            >>> clean = sanitizer.sanitize("<script>alert('xss')</script>Hello")
            >>> print(clean)
            Hello
        """
        if not message:
            return ""
        
        # Remove/escape HTML
        sanitized = bleach.clean(
            message,
            tags=[],  # No tags allowed
            strip=True
        )
        
        # Normalize whitespace
        sanitized = self._normalize_whitespace(sanitized)
        
        # Remove control characters
        sanitized = self._remove_control_chars(sanitized)
        
        # Normalize unicode
        sanitized = sanitized.encode('utf-8', errors='ignore').decode('utf-8')
        
        return sanitized.strip()
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Text to normalize
        
        Returns:
            str: Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _remove_control_chars(self, text: str) -> str:
        """
        Remove control characters from text.
        
        Args:
            text: Text to clean
        
        Returns:
            str: Text without control characters
        """
        # Remove control characters except newline and tab
        return ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')


def expand_abbreviations(text: str, walmart_terms: dict = None) -> str:
    """
    Expand Walmart-specific abbreviations.
    
    Args:
        text: Text containing abbreviations
        walmart_terms: Dictionary of abbreviations and their expansions
    
    Returns:
        str: Text with expanded abbreviations
        
    Example:
        >>> text = "Complete your CBL training"
        >>> expanded = expand_abbreviations(text, {"CBL": "Computer Based Learning"})
        >>> print(expanded)
        Complete your Computer Based Learning training
    """
    if walmart_terms is None:
        walmart_terms = {
            "GWP": "Great Workplace",
            "OBW": "One Best Way",
            "CBL": "Computer Based Learning",
            "PTO": "Paid Time Off",
            "SM": "Store Manager",
            "ASM": "Assistant Store Manager",
        }
    
    for abbr, expansion in walmart_terms.items():
        # Use word boundary to avoid partial matches
        pattern = r'\b' + re.escape(abbr) + r'\b'
        text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
    
    return text


def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL to validate
    
    Returns:
        bool: True if valid URL
        
    Example:
        >>> validate_url("https://walmart.com")
        True
        >>> validate_url("not a url")
        False
    """
    return validators.url(url) is True


def validate_email(email: str) -> bool:
    """
    Validate if a string is a valid email address.
    
    Args:
        email: Email to validate
    
    Returns:
        bool: True if valid email
        
    Example:
        >>> validate_email("user@walmart.com")
        True
    """
    return validators.email(email) is True


def is_safe_filename(filename: str) -> bool:
    """
    Check if a filename is safe (no path traversal, etc.).
    
    Args:
        filename: Filename to check
    
    Returns:
        bool: True if safe
        
    Example:
        >>> is_safe_filename("video.mp4")
        True
        >>> is_safe_filename("../../../etc/passwd")
        False
    """
    # Check for path traversal attempts
    if '..' in filename or filename.startswith('/'):
        return False
    
    # Check for valid characters
    safe_pattern = r'^[a-zA-Z0-9_\-\.]+$'
    return bool(re.match(safe_pattern, filename))
