"""Main video generation pipeline orchestrator."""

import time
from typing import Any, Dict, List, Optional

from ..core.accessibility_enhancer import AccessibilityEnhancer
from ..core.message_processor import MessageProcessor
from ..core.prompt_generator import PromptGenerator
from ..core.video_editor import VideoEditor
from ..core.video_generator import VideoGenerator
from ..models.message import ActivityMessage
from ..models.prompt import VideoPrompt
from ..models.video import AccessibilityMetadata, GeneratedVideo
from ..services.llm_service import LLMService
from ..utils import LoggerMixin, get_config
from ..utils.exceptions import (
    MessageProcessingError,
    PipelineError,
    PromptGenerationError,
    VideoGenerationError,
)


class VideoGenerationPipeline(LoggerMixin):
    """
    End-to-end pipeline for generating accessible videos from activity messages.
    
    Pipeline stages:
    1. Message Processing: Validate and sanitize input
    2. Prompt Generation: Create enhanced video prompts
    3. Video Generation: Generate video from prompt
    4. Video Editing: Apply post-processing effects
    5. Accessibility Enhancement: Add captions, audio, transcripts
    
    Attributes:
        message_processor: Message validation and processing
        prompt_generator: LLM-powered prompt enhancement
        video_generator: Multi-provider video generation
        video_editor: FFmpeg-based video editing
        accessibility_enhancer: Accessibility features
        config: Configuration object
    
    Example:
        >>> pipeline = VideoGenerationPipeline()
        >>> result = pipeline.generate(
        ...     message_content="Complete your safety training by Friday",
        ...     message_category="training"
        ... )
        >>> print(result.path)
    """
    
    def __init__(
        self,
        message_processor: Optional[MessageProcessor] = None,
        prompt_generator: Optional[PromptGenerator] = None,
        video_generator: Optional[VideoGenerator] = None,
        video_editor: Optional[VideoEditor] = None,
        accessibility_enhancer: Optional[AccessibilityEnhancer] = None
    ):
        """
        Initialize video generation pipeline.
        
        Args:
            message_processor: Custom message processor (auto-creates if None)
            prompt_generator: Custom prompt generator (auto-creates if None)
            video_generator: Custom video generator (auto-creates if None)
            video_editor: Custom video editor (auto-creates if None)
            accessibility_enhancer: Custom accessibility enhancer (auto-creates if None)
        """
        self.config = get_config()
        
        # Initialize components
        self.message_processor = message_processor or MessageProcessor()
        
        if prompt_generator is None:
            llm_service = LLMService()
            self.prompt_generator = PromptGenerator(llm_service=llm_service)
        else:
            self.prompt_generator = prompt_generator
        
        self.video_generator = video_generator or VideoGenerator()
        self.video_editor = video_editor or VideoEditor()
        self.accessibility_enhancer = accessibility_enhancer or AccessibilityEnhancer()
        
        self.logger.info("pipeline_initialized")
    
    def generate(
        self,
        message_content: str,
        message_category: str = "general",
        message_priority: str = "medium",
        sender_id: Optional[str] = None,
        apply_editing: bool = True,
        add_accessibility: bool = True,
        skip_llm_enhancement: bool = False,
        **kwargs
    ) -> GeneratedVideo:
        """
        Generate accessible video from activity message.
        
        Args:
            message_content: Message text content
            message_category: Message category (training, recognition, etc.)
            message_priority: Message priority (low, medium, high, critical)
            sender_id: Message sender identifier
            apply_editing: Apply video post-processing
            add_accessibility: Add accessibility features
            skip_llm_enhancement: If True, use message_content directly as prompt (no LLM enhancement)
            **kwargs: Additional configuration
        
        Returns:
            GeneratedVideo: Generated video with metadata
            
        Raises:
            PipelineError: If any stage fails
            
        Example:
            >>> result = pipeline.generate(
            ...     message_content="Great job on your customer service!",
            ...     message_category="recognition",
            ...     message_priority="high"
            ... )
        """
        start_time = time.time()
        
        self.logger.info(
            "pipeline_started",
            content_length=len(message_content),
            category=message_category,
            priority=message_priority,
            skip_llm=skip_llm_enhancement
        )
        
        try:
            # Stage 1: Process message
            # When using skip_llm_enhancement (passthrough mode), use relaxed validation
            # since the content is a pre-built video prompt, not a raw message
            processed_message = self._process_message(
                content=message_content,
                category=message_category,
                priority=message_priority,
                sender_id=sender_id,
                skip_validation=skip_llm_enhancement
            )
            
            # Stage 2: Generate prompt
            if skip_llm_enhancement:
                # Use message content directly as prompt (for design studio previews)
                video_prompt = self._create_direct_prompt(processed_message)
            else:
                video_prompt = self._generate_prompt(processed_message)
            
            # Stage 3: Generate video
            generated_video = self._generate_video(video_prompt)
            
            # Stage 4: Edit video (optional)
            if apply_editing:
                generated_video = self._edit_video(generated_video, **kwargs)
            
            # Stage 5: Add accessibility (optional)
            if add_accessibility:
                accessibility_metadata = self._add_accessibility(
                    generated_video,
                    message_content
                )
                generated_video.accessibility = accessibility_metadata
            
            # Calculate total time
            total_time = time.time() - start_time
            
            self.logger.info(
                "pipeline_completed",
                video_id=generated_video.id,
                total_time=total_time,
                video_path=generated_video.path
            )
            
            return generated_video
        
        except Exception as e:
            self.logger.error(
                "pipeline_failed",
                error=str(e),
                stage=self._get_error_stage(e)
            )
            raise PipelineError(
                f"Video generation pipeline failed: {str(e)}",
                details={"error": str(e), "stage": self._get_error_stage(e)}
            )
    
    def _process_message(
        self,
        content: str,
        category: str,
        priority: str,
        sender_id: Optional[str],
        skip_validation: bool = False
    ) -> ActivityMessage:
        """
        Process and validate activity message.
        
        Args:
            content: Message content
            category: Message category
            priority: Message priority
            sender_id: Sender identifier
            skip_validation: Skip length validation (for pre-built prompts)
        
        Returns:
            ActivityMessage: Processed message
            
        Raises:
            MessageProcessingError: If processing fails
        """
        self.logger.info("stage_1_processing_message", skip_validation=skip_validation)
        
        try:
            import uuid

            # Create message object with required fields
            message = ActivityMessage(
                id=f"msg_{uuid.uuid4().hex[:12]}",
                content=content,
                category=category,
                priority=priority,
                sender=sender_id or "system",
                sender_id=sender_id
            )
            
            # When skip_validation is True (passthrough mode with pre-built prompts),
            # skip the message processor validation which has a 500 char limit
            if skip_validation:
                self.logger.info(
                    "message_processed_passthrough",
                    content_length=len(content)
                )
                return message
            
            # Process through message processor
            validation_result = self.message_processor.process(message)
            
            # Check if validation passed
            if not validation_result.is_valid:
                raise MessageProcessingError(
                    f"Message validation failed: {', '.join(validation_result.errors)}",
                    details={"errors": validation_result.errors}
                )
            
            # Update message with sanitized content
            if validation_result.sanitized_content:
                message.content = validation_result.sanitized_content
            
            self.logger.info(
                "message_processed",
                warnings=len(validation_result.warnings)
            )
            
            return message
        
        except Exception as e:
            raise MessageProcessingError(
                f"Message processing failed: {str(e)}",
                details={"content": content[:50], "error": str(e)}
            )
    
    def _generate_prompt(self, message: ActivityMessage) -> VideoPrompt:
        """
        Generate enhanced video prompt from message.
        
        Args:
            message: Processed activity message
        
        Returns:
            VideoPrompt: Enhanced video prompt
            
        Raises:
            PromptGenerationError: If generation fails
        """
        self.logger.info("stage_2_generating_prompt")
        
        try:
            result = self.prompt_generator.generate(message)
            
            # Check if generation was successful
            if not result.success:
                raise PromptGenerationError(
                    f"Prompt generation failed: {result.error_message or 'Unknown error'}",
                    details={"message_id": message.id}
                )
            
            # Extract the actual VideoPrompt from the result
            prompt = result.prompt
            
            self.logger.info(
                "prompt_generated",
                style=prompt.style,
                mood=prompt.mood,
                llm_used=result.llm_model_used
            )
            
            return prompt
        
        except Exception as e:
            raise PromptGenerationError(
                f"Prompt generation failed: {str(e)}",
                details={"message_id": message.id, "error": str(e)}
            )
    
    def _create_direct_prompt(self, message: ActivityMessage) -> VideoPrompt:
        """
        Create video prompt directly from message without LLM enhancement.
        
        Used for design studio previews where we want the exact prompt template,
        not an LLM-enhanced version.
        
        Args:
            message: Processed activity message
        
        Returns:
            VideoPrompt: Direct video prompt (no LLM enhancement)
        """
        self.logger.info(
            "stage_2_creating_direct_prompt",
            message_id=message.id
        )
        
        # Create prompt directly from message content
        prompt = VideoPrompt(
            original_message=message.content,
            enhanced_prompt=message.content,  # Use content as-is
            style="cinematic",
            mood="informative",  # Use valid enum value
            keywords=self._extract_keywords_from_text(message.content),
            duration_hint=8,  # 8 second default duration
            metadata={
                "message_id": message.id,
                "sender": message.sender,
                "direct_prompt": True  # Mark as direct (no LLM enhancement)
            }
        )
        
        self.logger.info(
            "direct_prompt_created",
            message_id=message.id,
            content_length=len(message.content)
        )
        
        return prompt
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Simple keyword extraction from text."""
        # Simple implementation: split by common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "from", "is", "are", "was", "be"}
        words = [w.strip('.,!?;:') for w in text.lower().split()]
        return [w for w in words if w and w not in stop_words and len(w) > 3][:5]
    
    def _generate_video(self, prompt: VideoPrompt) -> GeneratedVideo:
        """
        Generate video from prompt.
        
        Args:
            prompt: Video generation prompt
        
        Returns:
            GeneratedVideo: Generated video
            
        Raises:
            VideoGenerationError: If generation fails
        """
        self.logger.info("stage_3_generating_video")
        
        try:
            # Call the correct method name
            result = self.video_generator.generate_video(prompt=prompt)
            
            # Check if generation was successful
            if not result.success:
                error_msg = "Unknown error"
                if result.video and result.video.error_message:
                    error_msg = result.video.error_message
                elif result.warnings:
                    error_msg = "; ".join(result.warnings)
                    
                raise VideoGenerationError(
                    f"Video generation failed: {error_msg}",
                    details={"prompt": prompt.enhanced_prompt[:50]}
                )
            
            # Extract the GeneratedVideo from the result
            video = result.video
            
            self.logger.info(
                "video_generated",
                video_id=video.id,
                duration=video.duration,
                provider=video.generation_params.get("model", "unknown")
            )
            
            return video
        
        except Exception as e:
            raise VideoGenerationError(
                f"Video generation failed: {str(e)}",
                details={"prompt": prompt.enhanced_prompt[:50], "error": str(e)}
            )
    
    def _edit_video(
        self,
        video: GeneratedVideo,
        add_fade: bool = True,
        trim_duration: Optional[float] = None,
        **kwargs
    ) -> GeneratedVideo:
        """
        Apply post-processing edits to video.
        
        Args:
            video: Generated video
            add_fade: Add fade transitions
            trim_duration: Trim to specific duration
            **kwargs: Additional editing options
        
        Returns:
            GeneratedVideo: Edited video
        """
        self.logger.info("stage_4_editing_video")
        
        try:
            edited_path = video.path
            
            # Add fade transitions
            if add_fade and self.config.get("video_editing.add_fade", True):
                fade_duration = self.config.get("video_editing.fade_duration", 0.5)
                edited_path = self.video_editor.add_fade_transition(
                    input_path=edited_path,
                    fade_in_duration=fade_duration,
                    fade_out_duration=fade_duration
                )
            
            # Trim if requested
            if trim_duration:
                edited_path = self.video_editor.trim(
                    input_path=edited_path,
                    start_time=0,
                    end_time=trim_duration
                )
            
            # Update video path
            video.path = edited_path
            
            self.logger.info("video_edited", edited_path=edited_path)
            
            return video
        
        except Exception as e:
            self.logger.warning(
                "video_editing_failed",
                error=str(e),
                message="Continuing with unedited video"
            )
            return video
    
    def _add_accessibility(
        self,
        video: GeneratedVideo,
        original_content: str
    ) -> AccessibilityMetadata:
        """
        Add accessibility features to video.
        
        Args:
            video: Generated video
            original_content: Original message content
        
        Returns:
            AccessibilityMetadata: Accessibility metadata
        """
        self.logger.info("stage_5_adding_accessibility")
        
        try:
            metadata = self.accessibility_enhancer.enhance_video(
                video=video,
                message_content=original_content
            )
            
            self.logger.info(
                "accessibility_added",
                has_captions=metadata.has_captions,
                has_audio=metadata.has_audio_description,
                wcag_level=metadata.wcag_level
            )
            
            return metadata
        
        except Exception as e:
            self.logger.warning(
                "accessibility_enhancement_failed",
                error=str(e),
                message="Continuing without full accessibility"
            )
            return AccessibilityMetadata()
    
    def _get_error_stage(self, error: Exception) -> str:
        """Determine which stage caused the error."""
        if isinstance(error, MessageProcessingError):
            return "message_processing"
        elif isinstance(error, PromptGenerationError):
            return "prompt_generation"
        elif isinstance(error, VideoGenerationError):
            return "video_generation"
        else:
            return "unknown"
    
    def generate_batch(
        self,
        messages: list[Dict[str, Any]],
        max_concurrent: int = 3
    ) -> list[GeneratedVideo]:
        """
        Generate videos for multiple messages in batch.
        
        Args:
            messages: List of message dictionaries
            max_concurrent: Maximum concurrent generations
        
        Returns:
            list[GeneratedVideo]: List of generated videos
            
        Example:
            >>> messages = [
            ...     {"content": "Training reminder", "category": "training"},
            ...     {"content": "Great work!", "category": "recognition"}
            ... ]
            >>> videos = pipeline.generate_batch(messages)
        """
        self.logger.info(
            "batch_generation_started",
            total_messages=len(messages),
            max_concurrent=max_concurrent
        )
        
        results = []
        
        for i, msg_data in enumerate(messages):
            try:
                self.logger.info(
                    "processing_batch_item",
                    index=i + 1,
                    total=len(messages)
                )
                
                video = self.generate(**msg_data)
                results.append(video)
            
            except Exception as e:
                self.logger.error(
                    "batch_item_failed",
                    index=i + 1,
                    error=str(e)
                )
        
        self.logger.info(
            "batch_generation_completed",
            successful=len(results),
            total=len(messages)
        )
        
        return results
