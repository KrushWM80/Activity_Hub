"""PII (Personally Identifiable Information) detection and masking."""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

from ..utils import get_logger

logger = get_logger(__name__)


@dataclass
class PIIMatch:
    """Detected PII match."""
    
    type: str  # email, phone, ssn, credit_card, etc.
    value: str  # The detected value
    start: int  # Start position in text
    end: int  # End position in text
    confidence: float  # Detection confidence (0.0 - 1.0)


class PIIDetector:
    """
    Detect and mask PII in text.
    
    Detects:
    - Email addresses
    - Phone numbers
    - Social Security Numbers (SSN)
    - Credit card numbers
    - IP addresses
    - URLs with potential PII
    
    Example:
        >>> detector = PIIDetector()
        >>> matches = detector.detect("Email me at john@example.com")
        >>> masked = detector.mask("Email me at john@example.com")
        >>> # "Email me at [EMAIL_REDACTED]"
    """
    
    # PII patterns
    PATTERNS = {
        "email": (
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            0.95
        ),
        "phone": (
            r"\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b",
            0.90
        ),
        "ssn": (
            r"\b\d{3}-\d{2}-\d{4}\b",
            0.95
        ),
        "credit_card": (
            r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b",
            0.85
        ),
        "ip_address": (
            r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
            0.70  # Lower confidence as IPs might be legitimate
        ),
    }
    
    MASK_TEMPLATES = {
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "ssn": "[SSN_REDACTED]",
        "credit_card": "[CARD_REDACTED]",
        "ip_address": "[IP_REDACTED]",
    }
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize PII detector.
        
        Args:
            strict_mode: If True, block on any PII detection
        """
        self.strict_mode = strict_mode
        self.compiled_patterns = {
            pii_type: re.compile(pattern, re.IGNORECASE)
            for pii_type, (pattern, _) in self.PATTERNS.items()
        }
    
    def detect(self, text: str) -> List[PIIMatch]:
        """
        Detect PII in text.
        
        Args:
            text: Text to scan
            
        Returns:
            List of PIIMatch objects
        """
        matches = []
        
        for pii_type, pattern in self.compiled_patterns.items():
            confidence = self.PATTERNS[pii_type][1]
            
            for match in pattern.finditer(text):
                pii_match = PIIMatch(
                    type=pii_type,
                    value=match.group(0),
                    start=match.start(),
                    end=match.end(),
                    confidence=confidence
                )
                matches.append(pii_match)
                
                logger.warning(
                    "pii_detected",
                    type=pii_type,
                    confidence=confidence,
                    position=f"{match.start()}-{match.end()}"
                )
        
        return matches
    
    def mask(self, text: str, mask_char: str = "*") -> str:
        """
        Mask PII in text.
        
        Args:
            text: Text to mask
            mask_char: Character to use for masking (or use templates)
            
        Returns:
            str: Text with PII masked
        """
        masked_text = text
        offset = 0
        
        # Sort matches by position
        matches = sorted(self.detect(text), key=lambda m: m.start)
        
        for match in matches:
            # Use template mask
            mask = self.MASK_TEMPLATES.get(match.type, "[REDACTED]")
            
            # Adjust positions for previous replacements
            start = match.start + offset
            end = match.end + offset
            
            # Replace in text
            masked_text = masked_text[:start] + mask + masked_text[end:]
            
            # Update offset
            offset += len(mask) - (match.end - match.start)
        
        return masked_text
    
    def validate(self, text: str) -> Tuple[bool, List[str]]:
        """
        Validate text doesn't contain PII.
        
        Args:
            text: Text to validate
            
        Returns:
            Tuple of (is_valid, list of PII types found)
        """
        matches = self.detect(text)
        
        if not matches:
            return True, []
        
        pii_types = list(set(m.type for m in matches))
        
        if self.strict_mode:
            logger.error(
                "pii_validation_failed",
                pii_types=pii_types,
                count=len(matches)
            )
            return False, pii_types
        
        return True, pii_types
    
    def get_violation_message(self, pii_types: List[str]) -> str:
        """
        Generate user-friendly error message.
        
        Args:
            pii_types: List of detected PII types
            
        Returns:
            str: Error message
        """
        type_names = {
            "email": "email address",
            "phone": "phone number",
            "ssn": "Social Security Number",
            "credit_card": "credit card number",
            "ip_address": "IP address",
        }
        
        detected = [type_names.get(t, t) for t in pii_types]
        
        if len(detected) == 1:
            return f"⚠️ Your message contains a {detected[0]}. Please remove it before proceeding."
        else:
            items = ", ".join(detected[:-1]) + f" and {detected[-1]}"
            return f"⚠️ Your message contains: {items}. Please remove them before proceeding."


# Convenience functions
_detector: PIIDetector = None


def get_detector() -> PIIDetector:
    """Get global PII detector instance."""
    global _detector
    if _detector is None:
        _detector = PIIDetector()
    return _detector


def detect_pii(text: str) -> List[PIIMatch]:
    """Detect PII in text (convenience function)."""
    return get_detector().detect(text)


def mask_pii(text: str) -> str:
    """Mask PII in text (convenience function)."""
    return get_detector().mask(text)
