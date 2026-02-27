"""Mock services for testing."""

from typing import Optional, Dict, Any
from unittest.mock import Mock


class MockLLMService:
    """Mock LLM service for testing without API calls."""
    
    def __init__(self, should_fail: bool = False, response: Optional[str] = None):
        """
        Initialize mock LLM service.
        
        Args:
            should_fail: Whether to simulate service failure
            response: Custom response to return
        """
        self.should_fail = should_fail
        self.custom_response = response
        self.call_count = 0
        self.last_system_prompt = None
        self.last_user_prompt = None
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """Mock generate method."""
        self.call_count += 1
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        
        if self.should_fail:
            raise Exception("Mock LLM service failure")
        
        if self.custom_response:
            return self.custom_response
        
        # Return a standard mock response
        return (
            "A professional Walmart store environment with bright lighting, "
            "clean aisles, and associates engaged in their tasks. "
            "Modern retail setting with clear signage and organized displays."
        )
    
    def is_available(self) -> bool:
        """Mock availability check."""
        return not self.should_fail
    
    def get_model_info(self) -> Dict[str, Any]:
        """Mock model info."""
        return {
            "provider": "mock",
            "model": "mock-model",
            "available": True
        }


class MockVideoGeneratorService:
    """Mock video generation service for testing."""
    
    def __init__(self, should_fail: bool = False):
        """
        Initialize mock video generator.
        
        Args:
            should_fail: Whether to simulate generation failure
        """
        self.should_fail = should_fail
        self.call_count = 0
        self.last_prompt = None
    
    def generate_video(
        self,
        prompt: str,
        duration: int = 10,
        resolution: Dict[str, int] = None,
        **kwargs
    ) -> str:
        """Mock video generation."""
        self.call_count += 1
        self.last_prompt = prompt
        
        if self.should_fail:
            raise Exception("Mock video generation failure")
        
        # Return mock video path
        return f"output/videos/mock_video_{self.call_count}.mp4"
    
    def is_available(self) -> bool:
        """Mock availability check."""
        return not self.should_fail


class MockAccessibilityService:
    """Mock accessibility enhancement service."""
    
    def __init__(self, should_fail: bool = False):
        """
        Initialize mock accessibility service.
        
        Args:
            should_fail: Whether to simulate service failure
        """
        self.should_fail = should_fail
        self.captions_generated = 0
        self.audio_descriptions_generated = 0
    
    def generate_captions(self, video_path: str, content: str) -> str:
        """Mock caption generation."""
        if self.should_fail:
            raise Exception("Mock caption generation failure")
        
        self.captions_generated += 1
        return f"{video_path}.vtt"
    
    def generate_audio_description(self, video_path: str, content: str) -> str:
        """Mock audio description generation."""
        if self.should_fail:
            raise Exception("Mock audio description failure")
        
        self.audio_descriptions_generated += 1
        return f"{video_path}_desc.mp3"


def create_mock_config(overrides: Optional[Dict[str, Any]] = None) -> Mock:
    """
    Create a mock configuration object.
    
    Args:
        overrides: Configuration values to override
    
    Returns:
        Mock: Mock configuration object
    """
    config = Mock()
    
    default_values = {
        "app.debug": False,
        "app.environment": "test",
        "video.default_duration": 10,
        "video.default_fps": 24,
        "video.default_resolution": {"width": 1920, "height": 1080},
        "llm.provider": "mock",
        "llm.model": "mock-model",
        "llm.temperature": 0.7,
        "llm.max_tokens": 500,
        "llm.timeout": 30,
        "message.min_length": 10,
        "message.max_length": 500,
    }
    
    if overrides:
        default_values.update(overrides)
    
    config.get = lambda key, default=None: default_values.get(key, default)
    config.get_api_key = lambda service: "mock-api-key"
    
    return config


def create_mock_logger() -> Mock:
    """
    Create a mock logger object.
    
    Returns:
        Mock: Mock logger
    """
    logger = Mock()
    logger.debug = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.critical = Mock()
    
    return logger
