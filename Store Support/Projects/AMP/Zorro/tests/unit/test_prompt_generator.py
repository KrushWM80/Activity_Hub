"""Unit tests for PromptGenerator."""

import pytest
from unittest.mock import Mock, patch

from src.core.prompt_generator import PromptGenerator
from src.models.message import ActivityMessage, MessageCategory, MessagePriority
from src.models.prompt import PromptStyle, PromptMood
from tests.mocks.mock_services import MockLLMService


class TestPromptGenerator:
    """Test suite for PromptGenerator class."""
    
    @pytest.fixture
    def mock_llm_service(self):
        """Create a mock LLM service."""
        return MockLLMService()
    
    @pytest.fixture
    def generator(self, mock_llm_service):
        """Create a PromptGenerator with mock LLM."""
        return PromptGenerator(llm_service=mock_llm_service, fallback_enabled=True)
    
    @pytest.fixture
    def training_message(self):
        """Create a training message."""
        return ActivityMessage(
            id="test_001",
            content="Complete your safety training by Friday",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.HIGH,
            sender="Safety Team"
        )
    
    def test_generate_prompt_success(self, generator, training_message):
        """Test successful prompt generation."""
        result = generator.generate(training_message)
        
        assert result.success is True
        assert result.prompt is not None
        assert result.error_message is None
        assert len(result.prompt.enhanced_prompt) > 0
        assert result.generation_time >= 0
    
    def test_prompt_style_determination(self, generator, training_message):
        """Test style is correctly determined from message category."""
        result = generator.generate(training_message)
        
        assert result.success is True
        assert result.prompt.style == PromptStyle.PROFESSIONAL
    
    def test_prompt_mood_determination(self, generator):
        """Test mood determination for different priorities."""
        # Urgent message
        urgent_msg = ActivityMessage(
            id="test_002",
            content="Store closing early due to weather",
            category=MessageCategory.ANNOUNCEMENT,
            priority=MessagePriority.URGENT,
            sender="Operations"
        )
        
        result = generator.generate(urgent_msg)
        assert result.prompt.mood == PromptMood.URGENT
        
        # Celebration message
        celebration_msg = ActivityMessage(
            id="test_003",
            content="Great job on achieving 100% satisfaction!",
            category=MessageCategory.CELEBRATION,
            priority=MessagePriority.MEDIUM,
            sender="Manager"
        )
        
        result = generator.generate(celebration_msg)
        assert result.prompt.mood == PromptMood.CELEBRATORY
    
    def test_keyword_extraction(self, generator, training_message):
        """Test keyword extraction from message."""
        result = generator.generate(training_message)
        
        assert result.success is True
        assert len(result.prompt.keywords) > 0
        # Should extract meaningful words, not stop words
        assert all(len(keyword) > 3 for keyword in result.prompt.keywords)
    
    def test_duration_hint_calculation(self, generator):
        """Test duration hint based on content length."""
        # Short message
        short_msg = ActivityMessage(
            id="test_004",
            content="Complete training today",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.MEDIUM,
            sender="Training"
        )
        
        result = generator.generate(short_msg)
        assert result.prompt.duration_hint <= 8
        
        # Long message
        long_msg = ActivityMessage(
            id="test_005",
            content="Please complete your comprehensive safety training module by end of day Friday and make sure to review all materials",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.MEDIUM,
            sender="Training"
        )
        
        result = generator.generate(long_msg)
        assert result.prompt.duration_hint >= 8
    
    def test_negative_prompt_generation(self, generator, training_message):
        """Test negative prompt is generated."""
        result = generator.generate(training_message)
        
        assert result.success is True
        assert result.prompt.negative_prompt is not None
        assert "blurry" in result.prompt.negative_prompt.lower()
    
    def test_fallback_on_llm_failure(self):
        """Test fallback prompt generation when LLM fails."""
        failing_llm = MockLLMService(should_fail=True)
        generator = PromptGenerator(llm_service=failing_llm, fallback_enabled=True)
        
        message = ActivityMessage(
            id="test_006",
            content="Complete your safety training by Friday",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.HIGH,
            sender="Safety"
        )
        
        result = generator.generate(message)
        
        # Should succeed with fallback
        assert result.success is True
        assert result.prompt is not None
        assert result.llm_model_used == "fallback_template"
    
    def test_no_fallback_when_disabled(self):
        """Test error when fallback is disabled and LLM fails."""
        failing_llm = MockLLMService(should_fail=True)
        generator = PromptGenerator(llm_service=failing_llm, fallback_enabled=False)
        
        message = ActivityMessage(
            id="test_007",
            content="Complete your safety training by Friday",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.HIGH,
            sender="Safety"
        )
        
        result = generator.generate(message)
        
        # Should fail
        assert result.success is False
        assert result.error_message is not None
    
    def test_sanitized_content_usage(self, generator, training_message):
        """Test using pre-sanitized content."""
        sanitized = "Complete your Computer Based Learning by Friday"
        
        result = generator.generate(training_message, sanitized_content=sanitized)
        
        assert result.success is True
        # The LLM mock should have received the sanitized content
        assert generator.llm_service.call_count > 0
    
    def test_metadata_inclusion(self, generator, training_message):
        """Test that message metadata is included in prompt."""
        result = generator.generate(training_message)
        
        assert result.success is True
        assert "message_id" in result.prompt.metadata
        assert result.prompt.metadata["message_id"] == training_message.id
        assert "sender" in result.prompt.metadata
    
    def test_different_categories(self, generator):
        """Test prompt generation for different message categories."""
        categories = [
            (MessageCategory.SAFETY, PromptStyle.PROFESSIONAL),
            (MessageCategory.CELEBRATION, PromptStyle.ENERGETIC),
            (MessageCategory.REMINDER, PromptStyle.CASUAL),
            (MessageCategory.POLICY, PromptStyle.PROFESSIONAL),
        ]
        
        for category, expected_style in categories:
            msg = ActivityMessage(
                id=f"test_{category.value}",
                content=f"This is a {category.value} message for testing",
                category=category,
                priority=MessagePriority.MEDIUM,
                sender="Test"
            )
            
            result = generator.generate(msg)
            assert result.success is True
            assert result.prompt.style == expected_style
    
    def test_custom_llm_response(self):
        """Test with custom LLM response."""
        custom_response = "A beautiful cinematic scene in a Walmart store with dramatic lighting"
        mock_llm = MockLLMService(response=custom_response)
        generator = PromptGenerator(llm_service=mock_llm)
        
        message = ActivityMessage(
            id="test_008",
            content="Test message",
            category=MessageCategory.ANNOUNCEMENT,
            priority=MessagePriority.MEDIUM,
            sender="Test"
        )
        
        result = generator.generate(message)
        
        assert result.success is True
        assert result.prompt.enhanced_prompt == custom_response
    
    def test_urgent_priority_reduces_duration(self, generator):
        """Test that urgent messages have shorter duration hints."""
        # Normal priority message
        normal_msg = ActivityMessage(
            id="test_009",
            content="Please complete your training by end of week",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.MEDIUM,
            sender="Training"
        )
        
        # Urgent priority message with same content length
        urgent_msg = ActivityMessage(
            id="test_010",
            content="Please complete your training by end of week",
            category=MessageCategory.TRAINING,
            priority=MessagePriority.URGENT,
            sender="Training"
        )
        
        normal_result = generator.generate(normal_msg)
        urgent_result = generator.generate(urgent_msg)
        
        # Urgent should have shorter or equal duration
        assert urgent_result.prompt.duration_hint <= normal_result.prompt.duration_hint


@pytest.mark.parametrize("category,expected_mood", [
    (MessageCategory.SAFETY, PromptMood.SERIOUS),
    (MessageCategory.TRAINING, PromptMood.INFORMATIVE),
    (MessageCategory.CELEBRATION, PromptMood.CELEBRATORY),
    (MessageCategory.REMINDER, PromptMood.FRIENDLY),
    (MessageCategory.POLICY, PromptMood.SERIOUS),
])
def test_category_mood_mapping(category, expected_mood):
    """Parametrized test for category to mood mapping."""
    mock_llm = MockLLMService()
    generator = PromptGenerator(llm_service=mock_llm)
    
    message = ActivityMessage(
        id="test_param",
        content="Test message for category mood mapping",
        category=category,
        priority=MessagePriority.MEDIUM,
        sender="Test"
    )
    
    result = generator.generate(message)
    assert result.success is True
    assert result.prompt.mood == expected_mood
