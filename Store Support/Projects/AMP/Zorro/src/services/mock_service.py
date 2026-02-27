"""
Mock/Demo Video Provider - For testing without model downloads
"""
import time
import uuid
from pathlib import Path
from typing import Dict, Optional

from ..utils import get_logger


class MockVideoProvider:
    """
    Mock video provider for demo/testing purposes.
    Simulates video generation without requiring model downloads.
    """
    
    def __init__(self):
        self.logger = get_logger("MockVideoProvider")
        self.logger.info("mock_provider_initialized", mode="demo")
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        duration: int = 10,
        fps: int = 24,
        resolution: Dict[str, int] = None,
        video_id: str = None,
        output_dir: str = "output/videos"
    ) -> str:
        """
        Simulate video generation.
        
        Creates a placeholder video file for demo purposes.
        """
        if resolution is None:
            resolution = {"width": 1920, "height": 1080}
        
        video_id = video_id or f"demo_{uuid.uuid4().hex[:12]}"
        output_path = Path(output_dir) / f"{video_id}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(
            "generating_demo_video",
            video_id=video_id,
            prompt_length=len(prompt),
            duration=duration
        )
        
        # Simulate processing time
        time.sleep(2)  # 2 second delay to simulate generation
        
        # Create a tiny placeholder MP4 file
        # This is a minimal valid MP4 header
        mp4_header = bytes([
            0x00, 0x00, 0x00, 0x20, 0x66, 0x74, 0x79, 0x70,
            0x69, 0x73, 0x6F, 0x6D, 0x00, 0x00, 0x02, 0x00,
            0x69, 0x73, 0x6F, 0x6D, 0x69, 0x73, 0x6F, 0x32,
            0x6D, 0x70, 0x34, 0x31, 0x00, 0x00, 0x00, 0x08,
        ])
        
        with open(output_path, 'wb') as f:
            f.write(mp4_header)
            # Add some padding to make it look realistic
            f.write(b'\x00' * 1024)
        
        self.logger.info(
            "demo_video_created",
            video_id=video_id,
            path=str(output_path),
            file_size=output_path.stat().st_size
        )
        
        return str(output_path)
    
    def is_available(self) -> bool:
        """Mock provider is always available."""
        return True
