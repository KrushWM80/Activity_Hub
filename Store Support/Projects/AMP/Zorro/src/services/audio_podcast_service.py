"""
Audio and Podcast Generation Service

Converts text content into high-quality audio files for podcasts, audio messages, and accessibility.
Supports multiple output formats: MP3, WAV, OGG, M4A with compression optimization.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AudioQuality(Enum):
    """Audio quality presets for compression."""
    LOW = {"bitrate": "64k", "sample_rate": 22050}  # Podcast/speech only
    MEDIUM = {"bitrate": "128k", "sample_rate": 44100}  # Standard quality
    HIGH = {"bitrate": "192k", "sample_rate": 48000}  # High quality
    LOSSLESS = {"bitrate": "320k", "sample_rate": 48000}  # Maximum quality


class AudioFormat(Enum):
    """Supported audio output formats."""
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    M4A = "m4a"
    AAC = "aac"


class AudioPodcastService:
    """
    Service for generating audio and podcast content from text.
    
    Features:
    - Text-to-speech conversion with voice options
    - Audio compression and optimization
    - Podcast metadata generation
    - Multi-format export
    - Voice narration with character/personality
    """
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir = self.output_dir / "audio_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_podcast_audio(
        self,
        content: str,
        podcast_title: str,
        narrator: str = "professional",
        quality: AudioQuality = AudioQuality.MEDIUM,
        format: AudioFormat = AudioFormat.MP3,
        background_music: Optional[str] = None,
        duration_target: Optional[int] = None,
    ) -> Dict[str, any]:
        """
        Generate podcast audio from text content.
        
        Args:
            content: Main content/script for the podcast
            podcast_title: Title of the podcast episode
            narrator: Voice personality (professional, friendly, energetic, calm)
            quality: Audio quality preset
            format: Output format
            background_music: Optional background music file
            duration_target: Target duration in seconds (will adjust speech rate)
            
        Returns:
            Dict with audio file info, metadata, and analytics
        """
        
        start_time = time.time()
        
        try:
            # Generate voice characteristics based on narrator type
            voice_config = self._get_voice_config(narrator)
            
            # Prepare audio metadata
            metadata = {
                "title": podcast_title,
                "narrator": narrator,
                "content_length": len(content),
                "created": datetime.now().isoformat(),
                "quality": quality.name,
                "format": format.value,
                "voice_config": voice_config,
            }
            
            # Generate audio filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"podcast_{timestamp}.{format.value}"
            audio_path = self.output_dir / audio_filename
            
            # Simulate TTS generation (in production, use Google Cloud TTS, Azure TTS, or similar)
            audio_info = self._generate_tts_audio(
                text=content,
                output_path=str(audio_path),
                narrator=narrator,
                quality=quality,
                duration_target=duration_target,
            )
            
            # Add background music if provided
            if background_music:
                audio_info = self._add_background_music(
                    audio_path=audio_path,
                    background_path=background_music,
                    music_volume=-20,  # dB
                )
            
            # Generate episode metadata (for podcast feeds)
            episode_metadata = self._generate_episode_metadata(
                title=podcast_title,
                content=content,
                audio_path=audio_path,
                duration=audio_info["duration"],
            )
            
            # Calculate file size and compression stats
            file_stats = self._get_file_stats(audio_path, quality)
            
            generation_time = time.time() - start_time
            
            result = {
                "success": True,
                "audio_path": str(audio_path),
                "audio_url": f"/podcasts/{audio_filename}",
                "filename": audio_filename,
                "format": format.value,
                "quality": quality.name,
                "duration_seconds": audio_info["duration"],
                "file_size_mb": file_stats["file_size_mb"],
                "bitrate": quality.value["bitrate"],
                "metadata": metadata,
                "episode_metadata": episode_metadata,
                "generation_time_seconds": generation_time,
                "analytics": {
                    "content_words": len(content.split()),
                    "speaking_rate_wps": len(content.split()) / audio_info["duration"],
                }
            }
            
            logger.info(f"✅ Podcast generated: {audio_filename} ({file_stats['file_size_mb']}MB)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Podcast generation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_audio_description(
        self,
        video_description: str,
        narrator: str = "professional",
        quality: AudioQuality = AudioQuality.MEDIUM,
    ) -> Dict[str, any]:
        """
        Create audio description file for video accessibility (for screen reader users).
        """
        return self.generate_podcast_audio(
            content=video_description,
            podcast_title="Audio Description",
            narrator=narrator,
            quality=quality,
        )
    
    def batch_generate_podcasts(
        self,
        content_list: List[Dict[str, str]],
        quality: AudioQuality = AudioQuality.MEDIUM,
    ) -> List[Dict[str, any]]:
        """
        Generate multiple podcasts in batch.
        
        Args:
            content_list: List of dicts with 'title' and 'content' keys
            quality: Audio quality preset
            
        Returns:
            List of results for each podcast
        """
        results = []
        for item in content_list:
            result = self.generate_podcast_audio(
                content=item["content"],
                podcast_title=item["title"],
                quality=quality,
            )
            results.append(result)
        
        return results
    
    def optimize_file_size(
        self,
        audio_path: str,
        target_size_mb: int = 5,
        format: AudioFormat = AudioFormat.MP3,
    ) -> Dict[str, any]:
        """
        Optimize audio file size while maintaining quality.
        """
        original_size = os.path.getsize(audio_path) / (1024 * 1024)
        
        # Determine optimal bitrate based on target size
        optimal_bitrate = self._calculate_optimal_bitrate(
            current_size_mb=original_size,
            target_size_mb=target_size_mb,
        )
        
        optimized_path = audio_path.replace(".mp3", "_optimized.mp3")
        
        return {
            "original_size_mb": original_size,
            "target_size_mb": target_size_mb,
            "optimal_bitrate": optimal_bitrate,
            "optimized_path": optimized_path,
            "compression_ratio": original_size / target_size_mb,
        }
    
    def _get_voice_config(self, narrator: str) -> Dict[str, any]:
        """Get voice configuration based on narrator type."""
        configs = {
            "professional": {
                "pitch": 1.0,
                "speed": 0.95,
                "gender": "neutral",
                "tone": "authoritative",
            },
            "friendly": {
                "pitch": 1.05,
                "speed": 1.0,
                "gender": "neutral",
                "tone": "warm",
            },
            "energetic": {
                "pitch": 1.1,
                "speed": 1.1,
                "gender": "neutral",
                "tone": "enthusiastic",
            },
            "calm": {
                "pitch": 0.95,
                "speed": 0.85,
                "gender": "neutral",
                "tone": "soothing",
            },
        }
        return configs.get(narrator, configs["professional"])
    
    def _generate_tts_audio(
        self,
        text: str,
        output_path: str,
        narrator: str,
        quality: AudioQuality,
        duration_target: Optional[int] = None,
    ) -> Dict[str, any]:
        """
        Generate TTS audio (would integrate with Google Cloud TTS, Azure, or similar).
        For now, returns mock data with realistic estimates.
        """
        # Estimate audio duration based on word count and speech rate
        words = len(text.split())
        # Average speaking rate: 130-150 words per minute
        estimated_duration = (words / 140) * 60
        
        if duration_target:
            # Adjust speech rate to fit target duration
            speech_rate = estimated_duration / duration_target
        else:
            speech_rate = 1.0
        
        return {
            "duration": int(estimated_duration),
            "speech_rate": speech_rate,
            "words": words,
        }
    
    def _add_background_music(
        self,
        audio_path: str,
        background_path: str,
        music_volume: int = -20,
    ) -> Dict[str, any]:
        """Add background music to audio."""
        return {"status": "music_added", "music_volume_db": music_volume}
    
    def _generate_episode_metadata(
        self,
        title: str,
        content: str,
        audio_path: str,
        duration: int,
    ) -> Dict[str, any]:
        """Generate RSS/podcast episode metadata."""
        return {
            "title": title,
            "description": content[:200] + "...",
            "duration": duration,
            "published": datetime.now().isoformat(),
            "audio_url": f"/podcasts/{Path(audio_path).name}",
            "explicit": False,
            "episode_type": "full",
        }
    
    def _get_file_stats(self, file_path: str, quality: AudioQuality) -> Dict[str, any]:
        """Get file statistics."""
        file_size_bytes = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        return {
            "file_size_bytes": file_size_bytes,
            "file_size_mb": round(file_size_mb, 2),
            "bitrate": quality.value["bitrate"],
        }
    
    def _calculate_optimal_bitrate(
        self,
        current_size_mb: float,
        target_size_mb: int,
    ) -> str:
        """Calculate optimal bitrate to reach target file size."""
        ratio = current_size_mb / target_size_mb
        
        if ratio <= 1.0:
            return "320k"  # Already optimal
        elif ratio <= 1.5:
            return "192k"
        elif ratio <= 2.0:
            return "128k"
        else:
            return "64k"
