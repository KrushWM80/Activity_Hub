"""Unit tests for main pipeline orchestrator."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.core.pipeline import VideoGenerationPipeline
from src.models.message import ActivityMessage
from src.models.prompt import VideoPrompt
from src.models.video import GeneratedVideo, AccessibilityMetadata
from src.utils.exceptions import (
    PipelineError,
    MessageProcessingError,
    PromptGenerationError,
    VideoGenerationError
)


class TestVideoGenerationPipeline:
    """Test end-to-end video generation pipeline."""
    
    def test_initialization(self):
        """Test pipeline initialization."""
        pipeline = VideoGenerationPipeline()
        
        assert pipeline.message_processor is not None
        assert pipeline.prompt_generator is not None
        assert pipeline.video_generator is not None
        assert pipeline.video_editor is not None
        assert pipeline.accessibility_enhancer is not None
    
    def test_generate_success(self):
        """Test successful end-to-end generation."""
        # Create mocks
        mock_processor = Mock()
        mock_prompt_gen = Mock()
        mock_video_gen = Mock()
        mock_editor = Mock()
        mock_accessibility = Mock()
        
        # Setup mock returns
        processed_msg = ActivityMessage(
            content="Test message",
            category="training",
            priority="medium"
        )
        mock_processor.process.return_value = processed_msg
        
        prompt = VideoPrompt(
            enhanced_prompt="Enhanced test prompt",
            style="professional",
            mood="informative"
        )
        mock_prompt_gen.generate.return_value = prompt
        
        video = GeneratedVideo(
            id="test123",
            path="output/test.mp4",
            duration=10.0,
            prompt_used="Enhanced test prompt",
            model_used="modelscope"
        )
        mock_video_gen.generate.return_value = video
        
        accessibility = AccessibilityMetadata(
            has_captions=True,
            has_audio_description=True,
            wcag_level="AAA"
        )
        mock_accessibility.enhance_video.return_value = accessibility
        
        # Create pipeline with mocks
        pipeline = VideoGenerationPipeline(
            message_processor=mock_processor,
            prompt_generator=mock_prompt_gen,
            video_generator=mock_video_gen,
            video_editor=mock_editor,
            accessibility_enhancer=mock_accessibility
        )
        
        # Generate
        result = pipeline.generate(
            message_content="Test message",
            message_category="training"
        )
        
        # Verify
        assert result.id == "test123"
        assert result.path == "output/test.mp4"
        assert result.accessibility.has_captions is True
        
        # Verify all stages called
        mock_processor.process.assert_called_once()
        mock_prompt_gen.generate.assert_called_once()
        mock_video_gen.generate.assert_called_once()
        mock_accessibility.enhance_video.assert_called_once()
    
    def test_generate_skip_editing(self):
        """Test generation with editing disabled."""
        mock_processor = Mock()
        mock_prompt_gen = Mock()
        mock_video_gen = Mock()
        mock_editor = Mock()
        
        # Setup returns
        processed_msg = ActivityMessage(
            content="Test",
            category="general",
            priority="medium"
        )
        mock_processor.process.return_value = processed_msg
        
        prompt = VideoPrompt(
            enhanced_prompt="Test",
            style="casual",
            mood="neutral"
        )
        mock_prompt_gen.generate.return_value = prompt
        
        video = GeneratedVideo(
            id="test123",
            path="test.mp4",
            duration=10.0,
            prompt_used="Test",
            model_used="modelscope"
        )
        mock_video_gen.generate.return_value = video
        
        pipeline = VideoGenerationPipeline(
            message_processor=mock_processor,
            prompt_generator=mock_prompt_gen,
            video_generator=mock_video_gen,
            video_editor=mock_editor
        )
        
        result = pipeline.generate(
            message_content="Test",
            apply_editing=False,
            add_accessibility=False
        )
        
        # Editor should not be called
        mock_editor.add_fade_transition.assert_not_called()
    
    def test_generate_message_processing_error(self):
        """Test error handling in message processing stage."""
        mock_processor = Mock()
        mock_processor.process.side_effect = MessageProcessingError("Invalid message")
        
        pipeline = VideoGenerationPipeline(message_processor=mock_processor)
        
        with pytest.raises(PipelineError) as exc_info:
            pipeline.generate(message_content="")
        
        assert "pipeline failed" in str(exc_info.value).lower()
    
    def test_generate_prompt_generation_error(self):
        """Test error handling in prompt generation stage."""
        mock_processor = Mock()
        mock_prompt_gen = Mock()
        
        processed_msg = ActivityMessage(
            content="Test",
            category="general",
            priority="medium"
        )
        mock_processor.process.return_value = processed_msg
        mock_prompt_gen.generate.side_effect = PromptGenerationError("LLM failed")
        
        pipeline = VideoGenerationPipeline(
            message_processor=mock_processor,
            prompt_generator=mock_prompt_gen
        )
        
        with pytest.raises(PipelineError):
            pipeline.generate(message_content="Test")
    
    def test_generate_video_generation_error(self):
        """Test error handling in video generation stage."""
        mock_processor = Mock()
        mock_prompt_gen = Mock()
        mock_video_gen = Mock()
        
        processed_msg = ActivityMessage(
            content="Test",
            category="general",
            priority="medium"
        )
        mock_processor.process.return_value = processed_msg
        
        prompt = VideoPrompt(
            enhanced_prompt="Test",
            style="casual",
            mood="neutral"
        )
        mock_prompt_gen.generate.return_value = prompt
        
        mock_video_gen.generate.side_effect = VideoGenerationError("Model failed")
        
        pipeline = VideoGenerationPipeline(
            message_processor=mock_processor,
            prompt_generator=mock_prompt_gen,
            video_generator=mock_video_gen
        )
        
        with pytest.raises(PipelineError):
            pipeline.generate(message_content="Test")
    
    def test_edit_video_with_fade(self):
        """Test video editing with fade transitions."""
        mock_editor = Mock()
        mock_editor.add_fade_transition.return_value = "edited_video.mp4"
        
        pipeline = VideoGenerationPipeline(video_editor=mock_editor)
        
        video = GeneratedVideo(
            id="test123",
            path="original.mp4",
            duration=10.0,
            prompt_used="Test",
            model_used="modelscope"
        )
        
        edited = pipeline._edit_video(video, add_fade=True)
        
        assert edited.path == "edited_video.mp4"
        mock_editor.add_fade_transition.assert_called_once()
    
    def test_edit_video_with_trim(self):
        """Test video editing with trimming."""
        mock_editor = Mock()
        mock_editor.trim.return_value = "trimmed_video.mp4"
        
        pipeline = VideoGenerationPipeline(video_editor=mock_editor)
        
        video = GeneratedVideo(
            id="test123",
            path="original.mp4",
            duration=10.0,
            prompt_used="Test",
            model_used="modelscope"
        )
        
        edited = pipeline._edit_video(video, add_fade=False, trim_duration=5.0)
        
        assert edited.path == "trimmed_video.mp4"
        mock_editor.trim.assert_called_once()
    
    def test_edit_video_error_handling(self):
        """Test error handling in video editing."""
        mock_editor = Mock()
        mock_editor.add_fade_transition.side_effect = Exception("FFmpeg error")
        
        pipeline = VideoGenerationPipeline(video_editor=mock_editor)
        
        video = GeneratedVideo(
            id="test123",
            path="original.mp4",
            duration=10.0,
            prompt_used="Test",
            model_used="modelscope"
        )
        
        # Should return original video on error
        edited = pipeline._edit_video(video, add_fade=True)
        assert edited.path == "original.mp4"
    
    def test_add_accessibility(self):
        """Test accessibility enhancement."""
        mock_accessibility = Mock()
        
        metadata = AccessibilityMetadata(
            has_captions=True,
            has_audio_description=True,
            wcag_level="AAA"
        )
        mock_accessibility.enhance_video.return_value = metadata
        
        pipeline = VideoGenerationPipeline(
            accessibility_enhancer=mock_accessibility
        )
        
        video = GeneratedVideo(
            id="test123",
            path="test.mp4",
            duration=10.0,
            prompt_used="Test",
            model_used="modelscope"
        )
        
        result = pipeline._add_accessibility(video, "Original message")
        
        assert result.has_captions is True
        assert result.wcag_level == "AAA"
        mock_accessibility.enhance_video.assert_called_once()
    
    def test_generate_batch(self):
        """Test batch generation of multiple videos."""
        mock_processor = Mock()
        mock_prompt_gen = Mock()
        mock_video_gen = Mock()
        
        # Setup mocks
        processed_msg = ActivityMessage(
            content="Test",
            category="general",
            priority="medium"
        )
        mock_processor.process.return_value = processed_msg
        
        prompt = VideoPrompt(
            enhanced_prompt="Test",
            style="casual",
            mood="neutral"
        )
        mock_prompt_gen.generate.return_value = prompt
        
        video = GeneratedVideo(
            id="test123",
            path="test.mp4",
            duration=10.0,
            prompt_used="Test",
            model_used="modelscope"
        )
        mock_video_gen.generate.return_value = video
        
        pipeline = VideoGenerationPipeline(
            message_processor=mock_processor,
            prompt_generator=mock_prompt_gen,
            video_generator=mock_video_gen
        )
        
        messages = [
            {"message_content": "Message 1", "message_category": "training"},
            {"message_content": "Message 2", "message_category": "recognition"}
        ]
        
        results = pipeline.generate_batch(messages)
        
        assert len(results) == 2
        assert all(isinstance(r, GeneratedVideo) for r in results)
    
    def test_generate_batch_partial_failure(self):
        """Test batch generation with some failures."""
        pipeline = VideoGenerationPipeline()
        
        with patch.object(pipeline, 'generate') as mock_generate:
            # First succeeds, second fails, third succeeds
            mock_generate.side_effect = [
                GeneratedVideo(
                    id="1",
                    path="video1.mp4",
                    duration=10.0,
                    prompt_used="Test",
                    model_used="modelscope"
                ),
                Exception("Generation failed"),
                GeneratedVideo(
                    id="3",
                    path="video3.mp4",
                    duration=10.0,
                    prompt_used="Test",
                    model_used="modelscope"
                )
            ]
            
            messages = [
                {"message_content": "Message 1"},
                {"message_content": "Message 2"},
                {"message_content": "Message 3"}
            ]
            
            results = pipeline.generate_batch(messages)
            
            # Should have 2 successful results (1st and 3rd)
            assert len(results) == 2
    
    def test_get_error_stage(self):
        """Test error stage identification."""
        pipeline = VideoGenerationPipeline()
        
        assert pipeline._get_error_stage(
            MessageProcessingError("test")
        ) == "message_processing"
        
        assert pipeline._get_error_stage(
            PromptGenerationError("test")
        ) == "prompt_generation"
        
        assert pipeline._get_error_stage(
            VideoGenerationError("test")
        ) == "video_generation"
        
        assert pipeline._get_error_stage(
            Exception("test")
        ) == "unknown"
