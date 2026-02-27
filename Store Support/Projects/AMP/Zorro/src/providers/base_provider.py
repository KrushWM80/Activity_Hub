"""
Base provider class for video generation
"""

from abc import ABC, abstractmethod

from src.models.video_models import GeneratedVideo, VideoPrompt


class BaseVideoProvider(ABC):
    """Base class for video generation providers"""
    
    @abstractmethod
    def generate_video(self, prompt: VideoPrompt) -> GeneratedVideo:
        """Generate video from prompt"""
        pass
    
    def is_available(self) -> bool:
        """Check if provider is available"""
        return True
    
    def get_provider_info(self) -> dict:
        """Get provider information"""
        return {}
