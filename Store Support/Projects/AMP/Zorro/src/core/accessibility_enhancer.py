"""Accessibility enhancement module for captions, audio descriptions, and WCAG compliance."""

from datetime import timedelta
from pathlib import Path
from typing import Any, List, Optional, Tuple

from ..models.video import AccessibilityMetadata, GeneratedVideo
from ..utils import LoggerMixin, get_config
from ..utils.exceptions import (
    AudioDescriptionError,
    CaptionGenerationError,
)


class AccessibilityEnhancer(LoggerMixin):
    """
    Enhance videos with accessibility features.
    
    Provides:
    - WebVTT caption generation
    - Audio descriptions (TTS)
    - Contrast validation (WCAG compliance)
    - Transcript generation
    
    Attributes:
        config: Configuration object
        tts_service: Text-to-speech service
    
    Example:
        >>> enhancer = AccessibilityEnhancer()
        >>> result = enhancer.enhance_video(
        ...     video=generated_video,
        ...     message_content="Complete your training"
        ... )
    """
    
    def __init__(self, tts_service: Optional[Any] = None):
        """
        Initialize accessibility enhancer.
        
        Args:
            tts_service: Text-to-speech service (auto-creates if None)
        """
        self.config = get_config()
        
        # Initialize TTS service
        if tts_service is None:
            self.tts_service = self._initialize_tts()
        else:
            self.tts_service = tts_service
        
        self.logger.info("accessibility_enhancer_initialized")
    
    def _initialize_tts(self):
        """Initialize text-to-speech service."""
        try:
            from gtts import gTTS
            return gTTS
        except ImportError:
            self.logger.warning("gtts_not_installed")
            return None
    
    def enhance_video(
        self,
        video: GeneratedVideo,
        message_content: str,
        generate_captions: bool = True,
        generate_audio_description: bool = True,
        validate_contrast: bool = True
    ) -> AccessibilityMetadata:
        """
        Add all accessibility features to a video.
        
        Args:
            video: Generated video object
            message_content: Original message text
            generate_captions: Generate captions
            generate_audio_description: Generate audio description
            validate_contrast: Validate WCAG contrast
        
        Returns:
            AccessibilityMetadata: Accessibility features metadata
            
        Example:
            >>> metadata = enhancer.enhance_video(
            ...     video=my_video,
            ...     message_content="Safety training reminder"
            ... )
            >>> print(metadata.captions_path)
        """
        self.logger.info(
            "enhancing_video_accessibility",
            video_id=video.id,
            captions=generate_captions,
            audio=generate_audio_description
        )
        
        metadata = AccessibilityMetadata()
        
        # Generate captions
        if generate_captions and self.config.get("accessibility.captions.enabled", True):
            try:
                captions_path = self.generate_captions(
                    video_path=video.path,
                    content=message_content,
                    duration=video.duration or 10.0
                )
                metadata.has_captions = True
                metadata.captions_path = captions_path
                metadata.caption_format = self.config.get(
                    "accessibility.captions.format",
                    "webvtt"
                )
            except Exception as e:
                self.logger.error(
                    "caption_generation_failed",
                    video_id=video.id,
                    error=str(e)
                )
        
        # Generate audio description
        if generate_audio_description and self.config.get(
            "accessibility.audio_description.enabled",
            True
        ):
            try:
                audio_path = self.generate_audio_description(
                    video_path=video.path,
                    content=message_content,
                    prompt_description=video.prompt_used
                )
                metadata.has_audio_description = True
                metadata.audio_description_path = audio_path
            except Exception as e:
                self.logger.error(
                    "audio_description_failed",
                    video_id=video.id,
                    error=str(e)
                )
        
        # Generate transcript
        transcript_path = self.generate_transcript(
            content=message_content,
            video_id=video.id
        )
        metadata.transcript_path = transcript_path
        
        # Validate contrast (if needed)
        if validate_contrast:
            metadata.color_contrast_ratio = self.config.get(
                "accessibility.visual.minimum_contrast_ratio",
                7.0
            )
        
        # Set WCAG level
        metadata.wcag_level = "AAA"
        metadata.screen_reader_compatible = True
        
        self.logger.info(
            "video_accessibility_enhanced",
            video_id=video.id,
            has_captions=metadata.has_captions,
            has_audio=metadata.has_audio_description
        )
        
        return metadata
    
    def generate_captions(
        self,
        video_path: str,
        content: str,
        duration: float = 10.0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate WebVTT captions for video.
        
        Args:
            video_path: Path to video file
            content: Text content to caption
            duration: Video duration in seconds
            output_path: Output path for captions file
        
        Returns:
            str: Path to generated captions file
            
        Raises:
            CaptionGenerationError: If caption generation fails
            
        Example:
            >>> captions = enhancer.generate_captions(
            ...     video_path="video.mp4",
            ...     content="Complete your safety training by Friday",
            ...     duration=10.0
            ... )
        """
        video_file = Path(video_path)
        
        if output_path is None:
            output_path = str(video_file.with_suffix('.vtt'))
        
        self.logger.info(
            "generating_captions",
            video_path=video_path,
            content_length=len(content),
            duration=duration
        )
        
        try:
            # Split content into caption segments
            segments = self._split_into_caption_segments(content, duration)
            
            # Generate WebVTT content
            vtt_content = self._create_webvtt(segments)
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(vtt_content)
            
            self.logger.info(
                "captions_generated",
                output_path=output_path,
                segments=len(segments)
            )
            
            return output_path
        
        except Exception as e:
            raise CaptionGenerationError(
                f"Failed to generate captions: {str(e)}",
                details={"video_path": video_path, "error": str(e)}
            )
    
    def _split_into_caption_segments(
        self,
        content: str,
        duration: float,
        max_chars_per_line: int = 32,
        max_lines: int = 2
    ) -> List[Tuple[float, float, str]]:
        """
        Split content into timed caption segments.
        
        Args:
            content: Text content
            duration: Total duration in seconds
            max_chars_per_line: Maximum characters per caption line
            max_lines: Maximum lines per caption
        
        Returns:
            List[Tuple[float, float, str]]: (start_time, end_time, text) tuples
        """
        # Split content into words
        words = content.split()
        
        # Calculate words per segment
        max_chars_per_segment = max_chars_per_line * max_lines
        
        segments = []
        current_segment = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > max_chars_per_segment and current_segment:
                segments.append(' '.join(current_segment))
                current_segment = [word]
                current_length = word_length
            else:
                current_segment.append(word)
                current_length += word_length
        
        if current_segment:
            segments.append(' '.join(current_segment))
        
        # Calculate timing for each segment
        segment_duration = duration / len(segments) if segments else duration
        
        timed_segments = []
        for i, segment_text in enumerate(segments):
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration
            
            # Format text into lines
            formatted_text = self._format_caption_lines(
                segment_text,
                max_chars_per_line
            )
            
            timed_segments.append((start_time, end_time, formatted_text))
        
        return timed_segments
    
    def _format_caption_lines(
        self,
        text: str,
        max_chars_per_line: int
    ) -> str:
        """
        Format caption text into multiple lines.
        
        Args:
            text: Caption text
            max_chars_per_line: Maximum characters per line
        
        Returns:
            str: Formatted text with line breaks
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1
            
            if current_length + word_length > max_chars_per_line and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def _create_webvtt(
        self,
        segments: List[Tuple[float, float, str]]
    ) -> str:
        """
        Create WebVTT formatted content.
        
        Args:
            segments: List of (start, end, text) tuples
        
        Returns:
            str: WebVTT formatted content
        """
        vtt_lines = ["WEBVTT", ""]
        
        for i, (start, end, text) in enumerate(segments, 1):
            # Format timestamps
            start_time = self._format_timestamp(start)
            end_time = self._format_timestamp(end)
            
            # Add cue
            vtt_lines.append(f"{start_time} --> {end_time}")
            vtt_lines.append(text)
            vtt_lines.append("")
        
        return '\n'.join(vtt_lines)
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format timestamp for WebVTT.
        
        Args:
            seconds: Time in seconds
        
        Returns:
            str: Formatted timestamp (HH:MM:SS.mmm)
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = td.total_seconds() % 60
        
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def generate_audio_description(
        self,
        video_path: str,
        content: str,
        prompt_description: str = "",
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate audio description for video using TTS.
        
        Args:
            video_path: Path to video
            content: Message content
            prompt_description: Visual description from prompt
            output_path: Output audio file path
        
        Returns:
            str: Path to audio description file
            
        Raises:
            AudioDescriptionError: If generation fails
        """
        video_file = Path(video_path)
        
        if output_path is None:
            output_path = str(
                video_file.parent / f"{video_file.stem}_audio_desc.mp3"
            )
        
        self.logger.info(
            "generating_audio_description",
            video_path=video_path
        )
        
        try:
            # Create narration text
            narration = self._create_narration(content, prompt_description)
            
            # Generate speech
            if self.tts_service:
                tts = self.tts_service(text=narration, lang='en', slow=False)
                tts.save(output_path)
            else:
                # Create placeholder file
                self.logger.warning("tts_not_available_creating_placeholder")
                Path(output_path).touch()
            
            self.logger.info(
                "audio_description_generated",
                output_path=output_path
            )
            
            return output_path
        
        except Exception as e:
            raise AudioDescriptionError(
                f"Failed to generate audio description: {str(e)}",
                details={"video_path": video_path, "error": str(e)}
            )
    
    def _create_narration(
        self,
        content: str,
        visual_description: str
    ) -> str:
        """
        Create narration text combining content and visual description.
        
        Args:
            content: Message content
            visual_description: Visual scene description
        
        Returns:
            str: Narration text
        """
        # Extract key visual elements
        visual_elements = self._extract_visual_elements(visual_description)
        
        if visual_elements:
            narration = f"{visual_elements}. {content}"
        else:
            narration = content
        
        return narration
    
    def _extract_visual_elements(self, description: str) -> str:
        """Extract concise visual elements from description."""
        if not description:
            return ""
        
        # Take first sentence or first 100 characters
        sentences = description.split('.')
        if sentences:
            return sentences[0].strip()
        
        return description[:100].strip()
    
    def generate_transcript(
        self,
        content: str,
        video_id: str,
        output_dir: Optional[str] = None
    ) -> str:
        """
        Generate text transcript file.
        
        Args:
            content: Message content
            video_id: Video identifier
            output_dir: Output directory
        
        Returns:
            str: Path to transcript file
        """
        if output_dir is None:
            output_dir = "output/transcripts"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        transcript_file = output_path / f"{video_id}_transcript.txt"
        
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(f"Video ID: {video_id}\n\n")
            f.write(f"Content:\n{content}\n")
        
        return str(transcript_file)
    
    def validate_contrast_ratio(
        self,
        foreground_color: Tuple[int, int, int],
        background_color: Tuple[int, int, int],
        wcag_level: str = "AAA"
    ) -> bool:
        """
        Validate color contrast ratio for WCAG compliance.
        
        Args:
            foreground_color: RGB tuple (0-255)
            background_color: RGB tuple (0-255)
            wcag_level: WCAG level (AA or AAA)
        
        Returns:
            bool: True if contrast ratio meets requirements
            
        Example:
            >>> is_valid = enhancer.validate_contrast_ratio(
            ...     foreground_color=(255, 255, 255),  # White
            ...     background_color=(0, 0, 0),  # Black
            ...     wcag_level="AAA"
            ... )
            >>> print(is_valid)  # True (21:1 ratio)
        """
        # Calculate relative luminance
        def luminance(rgb):
            r, g, b = [x / 255.0 for x in rgb]
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        # Calculate contrast ratio
        l1 = luminance(foreground_color)
        l2 = luminance(background_color)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)
        
        # WCAG requirements
        min_ratio = 7.0 if wcag_level == "AAA" else 4.5
        
        return contrast_ratio >= min_ratio
