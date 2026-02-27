#!/usr/bin/env python3
"""
Test script to validate model classes and provider integration.
"""

from datetime import datetime, timezone
from src.models.prompt import VideoPrompt, PromptStyle, PromptMood
from src.models.video import GeneratedVideo, GenerationStatus, VideoMetadata

def test_video_prompt_creation():
    """Test creating a VideoPrompt with correct fields."""
    print("Testing VideoPrompt creation...")
    
    prompt = VideoPrompt(
        original_message="Create a training video",
        enhanced_prompt="A professional training video in a modern Walmart store with associates using digital tablets",
        style=PromptStyle.PROFESSIONAL,
        mood=PromptMood.INFORMATIVE,
        keywords=["training", "walmart", "professional"],
        duration_hint=5,
        negative_prompt="blurry, dark, unprofessional",
        metadata={
            "video_id": "test_001",
            "aspect_ratio": "16:9"
        }
    )
    
    print(f"✅ VideoPrompt created successfully")
    print(f"   - original_message: {prompt.original_message}")
    print(f"   - enhanced_prompt: {prompt.enhanced_prompt[:50]}...")
    print(f"   - style: {prompt.style}")
    print(f"   - mood: {prompt.mood}")
    print(f"   - duration_hint: {prompt.duration_hint}")
    print()

def test_video_metadata_creation():
    """Test creating VideoMetadata."""
    print("Testing VideoMetadata creation...")
    
    metadata = VideoMetadata(
        duration=5.0,
        fps=24,
        resolution={"width": 1920, "height": 1080},
        format="mp4",
        codec="h264",
        bitrate=5000,
        file_size=8388608
    )
    
    print(f"✅ VideoMetadata created successfully")
    print(f"   - duration: {metadata.duration}s")
    print(f"   - resolution: {metadata.resolution}")
    print(f"   - file_size: {metadata.file_size} bytes")
    print()

def test_generated_video_creation():
    """Test creating a GeneratedVideo."""
    print("Testing GeneratedVideo creation...")
    
    metadata = VideoMetadata(
        duration=5.0,
        fps=24,
        resolution={"width": 1920, "height": 1080},
        format="mp4",
        codec="h264",
        bitrate=5000,
        file_size=8388608
    )
    
    video = GeneratedVideo(
        id="vid_001",
        path="output/videos/test_001.mp4",
        status=GenerationStatus.COMPLETED,
        prompt_used="A professional training video...",
        metadata=metadata,
        generation_params={
            "model": "veo2",
            "provider": "walmart_media_studio"
        },
        generation_time=45.2,
        tags=["walmart", "media-studio"]
    )
    
    print(f"✅ GeneratedVideo created successfully")
    print(f"   - id: {video.id}")
    print(f"   - status: {video.status}")
    print(f"   - generation_time: {video.generation_time}s")
    print(f"   - file_size_mb: {video.file_size_mb}MB")
    print()

def test_failed_video_creation():
    """Test creating a failed GeneratedVideo."""
    print("Testing failed GeneratedVideo creation...")
    
    metadata = VideoMetadata(
        duration=5.0,
        fps=24,
        resolution={"width": 1920, "height": 1080},
        format="mp4",
        codec="h264",
        bitrate=5000,
        file_size=0
    )
    
    video = GeneratedVideo(
        id="vid_failed_001",
        path="output/videos/vid_failed_001.mp4",
        status=GenerationStatus.FAILED,
        prompt_used="A test prompt...",
        metadata=metadata,
        error_message="API connection failed",
        generation_params={"provider": "walmart_media_studio"},
        tags=[]
    )
    
    print(f"✅ Failed GeneratedVideo created successfully")
    print(f"   - id: {video.id}")
    print(f"   - status: {video.status}")
    print(f"   - error_message: {video.error_message}")
    print()

def test_provider_import():
    """Test that provider imports correctly."""
    print("Testing provider import...")
    
    from src.providers.walmart_media_studio import WalmartMediaStudioProvider
    
    print(f"✅ WalmartMediaStudioProvider imported successfully")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Model and Provider Tests")
    print("=" * 60)
    print()
    
    try:
        test_video_prompt_creation()
        test_video_metadata_creation()
        test_generated_video_creation()
        test_failed_video_creation()
        test_provider_import()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
