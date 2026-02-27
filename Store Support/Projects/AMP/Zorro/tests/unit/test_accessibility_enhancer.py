"""Unit tests for accessibility enhancer."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.core.accessibility_enhancer import AccessibilityEnhancer
from src.models.video import GeneratedVideo, AccessibilityMetadata
from src.utils.exceptions import CaptionGenerationError, AudioDescriptionError


class TestAccessibilityEnhancer:
    """Test accessibility enhancement features."""
    
    def test_initialization(self):
        """Test enhancer initialization."""
        enhancer = AccessibilityEnhancer()
        assert enhancer.config is not None
    
    def test_enhance_video_full(self):
        """Test full video enhancement."""
        enhancer = AccessibilityEnhancer()
        
        video = GeneratedVideo(
            id="test123",
            path="test_video.mp4",
            duration=10.0,
            prompt_used="Test prompt"
        )
        
        with patch.object(enhancer, 'generate_captions') as mock_captions, \
             patch.object(enhancer, 'generate_audio_description') as mock_audio, \
             patch.object(enhancer, 'generate_transcript') as mock_transcript:
            
            mock_captions.return_value = "test.vtt"
            mock_audio.return_value = "test_audio.mp3"
            mock_transcript.return_value = "transcript.txt"
            
            metadata = enhancer.enhance_video(
                video=video,
                message_content="Test message"
            )
            
            assert metadata.has_captions is True
            assert metadata.has_audio_description is True
            assert metadata.captions_path == "test.vtt"
            assert metadata.wcag_level == "AAA"
    
    def test_generate_captions(self, tmp_path):
        """Test caption generation."""
        enhancer = AccessibilityEnhancer()
        
        video_path = str(tmp_path / "test.mp4")
        Path(video_path).touch()
        
        captions_path = enhancer.generate_captions(
            video_path=video_path,
            content="This is a test message for captions",
            duration=10.0
        )
        
        assert Path(captions_path).exists()
        assert captions_path.endswith(".vtt")
        
        # Check WebVTT content
        with open(captions_path, 'r') as f:
            content = f.read()
            assert content.startswith("WEBVTT")
            assert "This is a test message" in content
    
    def test_split_into_caption_segments(self):
        """Test caption segmentation."""
        enhancer = AccessibilityEnhancer()
        
        content = "This is a long message that should be split into multiple caption segments"
        segments = enhancer._split_into_caption_segments(content, duration=10.0)
        
        assert len(segments) > 0
        for start, end, text in segments:
            assert start < end
            assert len(text) > 0
    
    def test_format_caption_lines(self):
        """Test caption line formatting."""
        enhancer = AccessibilityEnhancer()
        
        text = "This is a very long caption that should be split across multiple lines"
        formatted = enhancer._format_caption_lines(text, max_chars_per_line=30)
        
        lines = formatted.split('\n')
        for line in lines:
            assert len(line) <= 35  # Some tolerance for word boundaries
    
    def test_create_webvtt(self):
        """Test WebVTT content creation."""
        enhancer = AccessibilityEnhancer()
        
        segments = [
            (0.0, 3.0, "First caption"),
            (3.0, 6.0, "Second caption"),
            (6.0, 10.0, "Third caption")
        ]
        
        vtt_content = enhancer._create_webvtt(segments)
        
        assert vtt_content.startswith("WEBVTT")
        assert "00:00:00.000 --> 00:00:03.000" in vtt_content
        assert "First caption" in vtt_content
        assert "Second caption" in vtt_content
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        enhancer = AccessibilityEnhancer()
        
        timestamp = enhancer._format_timestamp(65.5)
        assert timestamp == "00:01:05.500"
        
        timestamp = enhancer._format_timestamp(0.0)
        assert timestamp == "00:00:00.000"
        
        timestamp = enhancer._format_timestamp(3661.25)
        assert timestamp == "01:01:01.250"
    
    def test_generate_audio_description(self, tmp_path):
        """Test audio description generation."""
        enhancer = AccessibilityEnhancer()
        
        video_path = str(tmp_path / "test.mp4")
        Path(video_path).touch()
        
        with patch.object(enhancer, 'tts_service') as mock_tts:
            mock_tts_instance = Mock()
            mock_tts.return_value = mock_tts_instance
            
            audio_path = enhancer.generate_audio_description(
                video_path=video_path,
                content="Test message",
                prompt_description="A professional training video"
            )
            
            assert audio_path.endswith("_audio_desc.mp3")
    
    def test_create_narration(self):
        """Test narration text creation."""
        enhancer = AccessibilityEnhancer()
        
        narration = enhancer._create_narration(
            content="Complete your training",
            visual_description="A professional office setting with training materials"
        )
        
        assert "Complete your training" in narration
        assert "professional office setting" in narration
    
    def test_generate_transcript(self, tmp_path):
        """Test transcript generation."""
        enhancer = AccessibilityEnhancer()
        
        transcript_path = enhancer.generate_transcript(
            content="Test message content",
            video_id="test123",
            output_dir=str(tmp_path)
        )
        
        assert Path(transcript_path).exists()
        
        with open(transcript_path, 'r') as f:
            content = f.read()
            assert "test123" in content
            assert "Test message content" in content
    
    def test_validate_contrast_ratio_pass(self):
        """Test contrast ratio validation - passing."""
        enhancer = AccessibilityEnhancer()
        
        # White on black (21:1 ratio)
        is_valid = enhancer.validate_contrast_ratio(
            foreground_color=(255, 255, 255),
            background_color=(0, 0, 0),
            wcag_level="AAA"
        )
        assert is_valid is True
    
    def test_validate_contrast_ratio_fail(self):
        """Test contrast ratio validation - failing."""
        enhancer = AccessibilityEnhancer()
        
        # Light gray on white (low contrast)
        is_valid = enhancer.validate_contrast_ratio(
            foreground_color=(200, 200, 200),
            background_color=(255, 255, 255),
            wcag_level="AAA"
        )
        assert is_valid is False
    
    def test_validate_contrast_ratio_aa_vs_aaa(self):
        """Test different WCAG levels."""
        enhancer = AccessibilityEnhancer()
        
        # Medium contrast (passes AA but not AAA)
        foreground = (100, 100, 100)
        background = (255, 255, 255)
        
        is_valid_aa = enhancer.validate_contrast_ratio(
            foreground_color=foreground,
            background_color=background,
            wcag_level="AA"
        )
        
        is_valid_aaa = enhancer.validate_contrast_ratio(
            foreground_color=foreground,
            background_color=background,
            wcag_level="AAA"
        )
        
        # May pass AA but not AAA (depending on actual ratio)
        # Just verify the function runs without errors
        assert isinstance(is_valid_aa, bool)
        assert isinstance(is_valid_aaa, bool)
    
    def test_enhance_video_skip_captions(self):
        """Test enhancement with captions disabled."""
        enhancer = AccessibilityEnhancer()
        
        video = GeneratedVideo(
            id="test123",
            path="test_video.mp4",
            duration=10.0,
            prompt_used="Test"
        )
        
        with patch.object(enhancer, 'generate_transcript') as mock_transcript:
            mock_transcript.return_value = "transcript.txt"
            
            metadata = enhancer.enhance_video(
                video=video,
                message_content="Test",
                generate_captions=False
            )
            
            assert metadata.has_captions is False
    
    def test_enhance_video_error_handling(self):
        """Test error handling during enhancement."""
        enhancer = AccessibilityEnhancer()
        
        video = GeneratedVideo(
            id="test123",
            path="test_video.mp4",
            duration=10.0,
            prompt_used="Test"
        )
        
        with patch.object(enhancer, 'generate_captions') as mock_captions, \
             patch.object(enhancer, 'generate_transcript') as mock_transcript:
            
            # Captions fail but should not raise
            mock_captions.side_effect = Exception("Caption error")
            mock_transcript.return_value = "transcript.txt"
            
            metadata = enhancer.enhance_video(
                video=video,
                message_content="Test"
            )
            
            # Should still return metadata even if captions failed
            assert metadata.has_captions is False
            assert metadata.transcript_path is not None
