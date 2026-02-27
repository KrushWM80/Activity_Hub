"""Unit tests for MessageProcessor."""

import pytest
from datetime import datetime

from src.core.message_processor import MessageProcessor
from src.models.message import ActivityMessage, MessageCategory, MessagePriority
from src.utils.exceptions import MessageValidationError, MessageSanitizationError


class TestMessageProcessor:
    """Test suite for MessageProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create a MessageProcessor instance for testing."""
        return MessageProcessor()
    
    @pytest.fixture
    def valid_message(self):
        """Create a valid test message."""
        return ActivityMessage(
            id="test_001",
            content="Complete your safety training by Friday",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.HIGH,
            sender="Safety Team",
            target_audience="all_associates"
        )
    
    def test_process_valid_message(self, processor, valid_message):
        """Test processing a valid message."""
        result = processor.process(valid_message)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert result.sanitized_content is not None
        assert "safety training" in result.sanitized_content.lower()
    
    def test_process_message_with_html(self, processor):
        """Test processing message containing HTML."""
        message = ActivityMessage(
            id="test_002",
            content="<script>alert('xss')</script>Complete your training",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.MEDIUM,
            sender="System"
        )
        
        result = processor.process(message)
        
        # HTML should be stripped
        assert "<script>" not in result.sanitized_content
        assert "Complete your training" in result.sanitized_content
    
    def test_process_message_too_short(self, processor):
        """Test processing message that's too short."""
        from pydantic import ValidationError
        
        # Should raise ValidationError when creating message with too-short content
        with pytest.raises(ValidationError) as exc_info:
            message = ActivityMessage(
                id="test_003",
                content="Hi",
                category=MessageCategory.ANNOUNCEMENT,
                priority=MessagePriority.LOW,
                sender="Test"
            )
        
        assert "at least 10 characters" in str(exc_info.value)
    
    def test_process_message_too_long(self, processor):
        """Test processing message that's too long."""
        from pydantic import ValidationError
        
        long_content = "A" * 600  # Exceeds max length of 500
        
        # Should raise ValidationError when creating message with too-long content
        with pytest.raises(ValidationError) as exc_info:
            message = ActivityMessage(
                id="test_004",
                content=long_content,
                category=MessageCategory.ANNOUNCEMENT,
                priority=MessagePriority.LOW,
                sender="Test"
            )
        
        assert "at most 500 characters" in str(exc_info.value)
    
    def test_expand_abbreviations(self, processor, valid_message):
        """Test abbreviation expansion."""
        message = ActivityMessage(
            id="test_005",
            content="Complete your CBL and review the OBW procedures",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.MEDIUM,
            sender="Training Team"
        )
        
        result = processor.process(message)
        
        assert result.is_valid is True
        assert "Computer Based Learning" in result.sanitized_content
        assert "One Best Way" in result.sanitized_content
        assert len(result.warnings) > 0
        assert any("CBL" in warning for warning in result.warnings)
    
    def test_sanitize_only(self, processor):
        """Test sanitize_only method."""
        dirty_content = "<b>Hello</b> <script>alert('xss')</script> World"
        clean_content = processor.sanitize_only(dirty_content)
        
        assert "<script>" not in clean_content
        assert "<b>" not in clean_content
        assert "Hello" in clean_content
        assert "World" in clean_content
    
    def test_validate_only(self, processor):
        """Test validate_only method."""
        # Valid content
        is_valid, errors = processor.validate_only("This is a valid message for testing")
        assert is_valid is True
        assert len(errors) == 0
        
        # Too short
        is_valid, errors = processor.validate_only("Hi")
        assert is_valid is False
        assert len(errors) > 0
    
    def test_extract_metadata(self, processor, valid_message):
        """Test metadata extraction."""
        metadata = processor.extract_metadata(valid_message)
        
        assert "word_count" in metadata
        assert "character_count" in metadata
        assert "category" in metadata
        assert metadata["category"] == "training"
        assert metadata["priority"] == "high"
        assert metadata["word_count"] > 0
    
    def test_content_quality_warnings(self, processor):
        """Test content quality warning detection."""
        # All caps message
        message = ActivityMessage(
            id="test_006",
            content="THIS IS ALL CAPS AND SHOULD TRIGGER A WARNING",
            category=MessageCategory.ANNOUNCEMENT,
            priority=MessagePriority.MEDIUM,
            sender="Test"
        )
        
        result = processor.process(message)
        
        assert len(result.warnings) > 0
        assert any("caps" in warning.lower() for warning in result.warnings)
    
    def test_excessive_exclamation_marks(self, processor):
        """Test detection of excessive exclamation marks."""
        message = ActivityMessage(
            id="test_007",
            content="Great job everyone!!!! Amazing work!!!!",
            category=MessageCategory.CELEBRATION,
            priority=MessagePriority.MEDIUM,
            sender="Manager"
        )
        
        result = processor.process(message)
        
        assert result.is_valid is True
        assert any("exclamation" in warning.lower() for warning in result.warnings)
    
    def test_empty_content_after_sanitization(self, processor):
        """Test handling of content that becomes empty after sanitization."""
        message = ActivityMessage(
            id="test_008",
            content="<script></script>",
            category=MessageCategory.ANNOUNCEMENT,
            priority=MessagePriority.LOW,
            sender="Test"
        )
        
        result = processor.process(message)
        
        assert result.is_valid is False
        assert any("empty" in error.lower() for error in result.errors)
    
    def test_multiple_walmart_abbreviations(self, processor):
        """Test expansion of multiple Walmart abbreviations."""
        message = ActivityMessage(
            id="test_009",
            content="Talk to your SM or ASM about GWP and PTO policies",
            category=MessageCategory.POLICY,
            priority=MessagePriority.MEDIUM,
            sender="HR Team"
        )
        
        result = processor.process(message)
        
        assert result.is_valid is True
        assert "Store Manager" in result.sanitized_content
        assert "Assistant Store Manager" in result.sanitized_content
        assert "Great Workplace" in result.sanitized_content
        assert "Paid Time Off" in result.sanitized_content
    
    def test_whitespace_normalization(self, processor):
        """Test normalization of excessive whitespace."""
        message = ActivityMessage(
            id="test_010",
            content="This   has    extra     spaces    between   words",
            category=MessageCategory.ANNOUNCEMENT,
            priority=MessagePriority.LOW,
            sender="Test"
        )
        
        result = processor.process(message)
        
        assert result.is_valid is True
        # Should have single spaces between words
        assert "  " not in result.sanitized_content


class TestMessageValidation:
    """Test suite for message validation edge cases."""
    
    def test_message_with_special_characters(self):
        """Test message with special characters."""
        processor = MessageProcessor()
        
        message = ActivityMessage(
            id="test_011",
            content="Meeting @ 3pm - don't forget! #important",
            category=MessageCategory.REMINDER,
            priority=MessagePriority.MEDIUM,
            sender="Manager"
        )
        
        result = processor.process(message)
        
        # Should handle special characters gracefully
        assert result.is_valid is True
        assert "@" in result.sanitized_content or "3pm" in result.sanitized_content
    
    def test_message_with_numbers(self):
        """Test message with numbers."""
        processor = MessageProcessor()
        
        message = ActivityMessage(
            id="test_012",
            content="Sales target: $50,000 for Q4 2024",
            category=MessageCategory.OPERATIONAL,
            priority=MessagePriority.HIGH,
            sender="Operations"
        )
        
        result = processor.process(message)
        
        assert result.is_valid is True
        assert "50,000" in result.sanitized_content or "50000" in result.sanitized_content
    
    def test_message_missing_punctuation(self):
        """Test message without ending punctuation."""
        processor = MessageProcessor()
        
        message = ActivityMessage(
            id="test_013",
            content="Complete your training by end of day",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.MEDIUM,
            sender="Training"
        )
        
        result = processor.process(message)
        
        assert result.is_valid is True
        assert any("punctuation" in warning.lower() for warning in result.warnings)


@pytest.mark.parametrize("content,expected_valid", [
    ("This is a perfectly valid message for testing", True),
    ("Short", False),
    ("A" * 600, False),
    ("Complete your CBL training today", True),
    ("<script>alert('xss')</script>Valid content", True),
])
def test_parametrized_validation(content, expected_valid):
    """Parametrized test for various message contents."""
    from pydantic import ValidationError
    
    processor = MessageProcessor()
    
    try:
        message = ActivityMessage(
            id="test_param",
            content=content,
            category=MessageCategory.ANNOUNCEMENT,
            priority=MessagePriority.MEDIUM,
            sender="Test"
        )
        
        # If we got here, the message was created successfully
        result = processor.process(message)
        
        if expected_valid:
            assert result.is_valid or len(result.errors) == 0
        else:
            # This shouldn't happen for invalid content
            assert False, f"Expected validation to fail for: {content[:50]}"
    
    except ValidationError as e:
        # Pydantic caught the validation error during model creation
        if expected_valid:
            pytest.fail(f"Expected content to be valid but got ValidationError: {content[:50]}")
        else:
            # This is expected for invalid content
            assert True
