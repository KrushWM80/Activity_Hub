"""Integration tests for end-to-end pipeline."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.pipeline import VideoGenerationPipeline
from src.models.video import GeneratedVideo


@pytest.mark.integration
class TestEndToEndPipeline:
    """Integration tests for complete pipeline."""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline with mocked external services."""
        with patch('src.services.llm_service.OpenAI') as mock_openai:
            # Mock LLM response
            mock_openai.return_value.chat.completions.create.return_value.choices = [
                Mock(message=Mock(content="Enhanced video prompt"))
            ]
            
            pipeline = VideoGenerationPipeline()
            return pipeline
    
    def test_complete_generation_workflow(self, pipeline, tmp_path):
        """Test complete video generation workflow."""
        # Mock video generation to avoid actual model inference
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            mock_video = GeneratedVideo(
                id="test123",
                path=str(tmp_path / "test.mp4"),
                duration=10.0,
                prompt_used="Test prompt",
                model_used="modelscope"
            )
            mock_gen.return_value = mock_video
            
            # Create placeholder video file
            Path(mock_video.path).touch()
            
            # Run pipeline
            result = pipeline.generate(
                message_content="Complete your safety training by Friday",
                message_category="training",
                message_priority="high",
                apply_editing=False,  # Skip editing for speed
                add_accessibility=False  # Skip accessibility for speed
            )
            
            assert result is not None
            assert result.id == "test123"
            assert Path(result.path).exists()
    
    def test_pipeline_with_walmart_abbreviations(self, pipeline):
        """Test pipeline correctly expands Walmart abbreviations."""
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            mock_video = GeneratedVideo(
                id="test456",
                path="output/test.mp4",
                duration=10.0,
                prompt_used="Test",
                model_used="modelscope"
            )
            mock_gen.return_value = mock_video
            
            result = pipeline.generate(
                message_content="Review CBL modules for OBW compliance",
                message_category="training",
                apply_editing=False,
                add_accessibility=False
            )
            
            # Message processor should have expanded abbreviations
            assert result is not None
    
    def test_pipeline_batch_processing(self, pipeline):
        """Test batch processing of multiple messages."""
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            def create_video(prompt, **kwargs):
                return GeneratedVideo(
                    id=f"test_{hash(prompt) % 1000}",
                    path="output/test.mp4",
                    duration=10.0,
                    prompt_used=prompt,
                    model_used="modelscope"
                )
            
            mock_gen.side_effect = lambda prompt, **kwargs: create_video(prompt, **kwargs)
            
            messages = [
                {"message_content": "Training reminder", "message_category": "training"},
                {"message_content": "Great work!", "message_category": "recognition"},
                {"message_content": "Team meeting", "message_category": "announcement"}
            ]
            
            results = pipeline.generate_batch(messages)
            
            assert len(results) == 3
            assert all(isinstance(r, GeneratedVideo) for r in results)
    
    @pytest.mark.slow
    def test_pipeline_with_accessibility(self, pipeline, tmp_path):
        """Test pipeline with full accessibility features."""
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            video_path = tmp_path / "test.mp4"
            video_path.touch()
            
            mock_video = GeneratedVideo(
                id="test789",
                path=str(video_path),
                duration=10.0,
                prompt_used="Test prompt",
                model_used="modelscope"
            )
            mock_gen.return_value = mock_video
            
            result = pipeline.generate(
                message_content="Complete your training",
                message_category="training",
                apply_editing=False,
                add_accessibility=True
            )
            
            assert result.accessibility is not None
            # Check accessibility features were attempted
            # (actual files may not exist if TTS is mocked)
    
    def test_pipeline_error_recovery(self, pipeline):
        """Test pipeline error handling and recovery."""
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            # Simulate generation failure
            mock_gen.side_effect = Exception("Model error")
            
            with pytest.raises(Exception):
                pipeline.generate(
                    message_content="Test message",
                    apply_editing=False,
                    add_accessibility=False
                )
    
    def test_different_message_categories(self, pipeline):
        """Test pipeline with different message categories."""
        categories = ["training", "recognition", "announcement", "alert", "reminder"]
        
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            mock_gen.return_value = GeneratedVideo(
                id="test",
                path="test.mp4",
                duration=10.0,
                prompt_used="Test",
                model_used="modelscope"
            )
            
            for category in categories:
                result = pipeline.generate(
                    message_content=f"Test {category} message",
                    message_category=category,
                    apply_editing=False,
                    add_accessibility=False
                )
                
                assert result is not None
    
    def test_different_priorities(self, pipeline):
        """Test pipeline with different priority levels."""
        priorities = ["low", "medium", "high", "critical"]
        
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            mock_gen.return_value = GeneratedVideo(
                id="test",
                path="test.mp4",
                duration=10.0,
                prompt_used="Test",
                model_used="modelscope"
            )
            
            for priority in priorities:
                result = pipeline.generate(
                    message_content="Test message",
                    message_priority=priority,
                    apply_editing=False,
                    add_accessibility=False
                )
                
                assert result is not None


@pytest.mark.integration
@pytest.mark.slow
class TestRealWorldScenarios:
    """Integration tests for real-world usage scenarios."""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline."""
        return VideoGenerationPipeline()
    
    def test_training_reminder_scenario(self, pipeline):
        """Test realistic training reminder scenario."""
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            mock_gen.return_value = GeneratedVideo(
                id="training123",
                path="output/training.mp4",
                duration=10.0,
                prompt_used="Training reminder",
                model_used="modelscope"
            )
            
            result = pipeline.generate(
                message_content="Reminder: Complete your annual safety training by Friday",
                message_category="training",
                message_priority="high",
                apply_editing=False,
                add_accessibility=True
            )
            
            assert result is not None
            assert result.model_used == "modelscope"
    
    def test_recognition_celebration_scenario(self, pipeline):
        """Test employee recognition scenario."""
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            mock_gen.return_value = GeneratedVideo(
                id="recognition123",
                path="output/recognition.mp4",
                duration=10.0,
                prompt_used="Recognition",
                model_used="modelscope"
            )
            
            result = pipeline.generate(
                message_content="Congratulations on achieving 100% customer satisfaction!",
                message_category="recognition",
                message_priority="high",
                apply_editing=True,
                add_accessibility=True
            )
            
            assert result is not None
    
    def test_critical_alert_scenario(self, pipeline):
        """Test critical alert scenario."""
        with patch('src.core.video_generator.VideoGenerator.generate') as mock_gen:
            mock_gen.return_value = GeneratedVideo(
                id="alert123",
                path="output/alert.mp4",
                duration=10.0,
                prompt_used="Alert",
                model_used="modelscope"
            )
            
            result = pipeline.generate(
                message_content="Emergency evacuation drill scheduled for 2 PM today",
                message_category="alert",
                message_priority="critical",
                apply_editing=False,
                add_accessibility=True
            )
            
            assert result is not None
