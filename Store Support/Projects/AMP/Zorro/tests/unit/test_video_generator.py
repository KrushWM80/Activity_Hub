"""Unit tests for video generator."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.core.video_generator import VideoGenerator, BaseVideoGenerator
from src.utils.exceptions import VideoGenerationError


class MockVideoGenerator(BaseVideoGenerator):
    """Mock video generator for testing."""
    
    def generate(self, prompt: str, **kwargs) -> str:
        return "output/test_video.mp4"
    
    def is_available(self) -> bool:
        return True
    
    def get_model_info(self):
        return {"provider": "mock", "model": "test"}


class TestVideoGenerator:
    """Test video generation orchestrator."""
    
    def test_initialization(self):
        """Test video generator initialization."""
        generator = VideoGenerator(provider="modelscope")
        assert generator.provider == "modelscope"
        assert generator.config is not None
    
    def test_generate_success(self):
        """Test successful video generation."""
        with patch('src.core.video_generator.VideoGenerator._create_provider') as mock_create:
            mock_provider = MockVideoGenerator()
            mock_create.return_value = mock_provider
            
            generator = VideoGenerator(provider="modelscope")
            result = generator.generate(
                prompt="A training video about safety",
                duration=10
            )
            
            assert result.path == "output/test_video.mp4"
            assert result.prompt_used == "A training video about safety"
            assert result.model_used == "modelscope"
    
    def test_generate_with_validation_error(self):
        """Test generation with invalid prompt."""
        generator = VideoGenerator(provider="modelscope")
        
        with pytest.raises(VideoGenerationError):
            generator.generate(prompt="")
    
    def test_provider_creation_modelscope(self):
        """Test ModelScope provider creation."""
        with patch('src.core.video_generator.ModelScopeVideoGenerator') as mock_class:
            mock_instance = Mock()
            mock_class.return_value = mock_instance
            
            generator = VideoGenerator(provider="modelscope")
            provider = generator._create_provider()
            
            assert provider == mock_instance
    
    def test_provider_creation_invalid(self):
        """Test invalid provider."""
        with pytest.raises(VideoGenerationError):
            VideoGenerator(provider="invalid_provider")
    
    def test_extract_metadata(self):
        """Test metadata extraction from video."""
        generator = VideoGenerator(provider="modelscope")
        
        with patch('src.core.video_generator.VideoGenerator._get_video_duration') as mock_duration:
            mock_duration.return_value = 10.5
            
            metadata = generator._extract_metadata("test_video.mp4")
            
            assert metadata["duration"] == 10.5
            assert "file_size" in metadata
    
    def test_get_video_duration_success(self):
        """Test video duration extraction."""
        generator = VideoGenerator()
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "10.5"
            mock_run.return_value.returncode = 0
            
            duration = generator._get_video_duration("test.mp4")
            assert duration == 10.5
    
    def test_get_video_duration_failure(self):
        """Test video duration extraction failure."""
        generator = VideoGenerator()
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("FFprobe error")
            
            duration = generator._get_video_duration("test.mp4")
            assert duration == 0.0


class TestBaseVideoGenerator:
    """Test base video generator interface."""
    
    def test_abstract_methods(self):
        """Test that BaseVideoGenerator is abstract."""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class
            BaseVideoGenerator()
    
    def test_mock_implementation(self):
        """Test mock implementation of abstract class."""
        generator = MockVideoGenerator()
        
        result = generator.generate("test prompt")
        assert result == "output/test_video.mp4"
        
        info = generator.get_model_info()
        assert info["provider"] == "mock"
