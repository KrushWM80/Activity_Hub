"""Video generation module for creating videos from text prompts."""

import time
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

from ..models.prompt import VideoPrompt
from ..models.video import (
    GeneratedVideo,
    GenerationStatus,
    VideoFormat,
    VideoGenerationResult,
    VideoMetadata,
)
from ..utils import (
    LoggerMixin,
    get_config,
    get_logger,
    log_execution_time,
)
from ..utils.exceptions import (
    InvalidVideoParametersError,
    ModelLoadError,
    VideoGenerationError,
)


class BaseVideoGenerator(ABC):
    """
    Abstract base class for video generators.
    
    This defines the interface that all video generation providers
    (ModelScope, Stability AI, RunwayML, etc.) must implement.
    """
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        duration: int = 5,
        fps: int = 24,
        resolution: Dict[str, int] = None,
        **kwargs
    ) -> str:
        """
        Generate video from text prompt.
        
        Args:
            prompt: Text description for video generation
            negative_prompt: Elements to avoid
            duration: Video duration in seconds
            fps: Frames per second
            resolution: Video resolution {"width": int, "height": int}
            **kwargs: Provider-specific parameters
        
        Returns:
            str: Path to generated video file
            
        Raises:
            VideoGenerationError: On generation failure
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if video generator is available and ready.
        
        Returns:
            bool: True if generator can be used
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            dict: Model information
        """
        pass


class VideoGenerator(LoggerMixin):
    """
    Main video generator orchestrator.
    
    This class manages video generation using different providers,
    handles output management, metadata extraction, and error recovery.
    
    Attributes:
        provider: Video generation provider instance
        config: Configuration object
        output_dir: Directory for generated videos
    
    Example:
        >>> generator = VideoGenerator()
        >>> prompt = VideoPrompt(
        ...     original_message="Complete training",
        ...     enhanced_prompt="Professional training scene...",
        ...     style=PromptStyle.PROFESSIONAL,
        ...     mood=PromptMood.INFORMATIVE
        ... )
        >>> result = generator.generate_video(prompt)
        >>> print(result.video.path)
    """
    
    def __init__(
        self,
        provider: Optional[BaseVideoGenerator] = None,
        output_dir: Optional[str] = None
    ):
        """
        Initialize video generator.
        
        Args:
            provider: Video generation provider (auto-creates if None)
            output_dir: Output directory (uses config if None)
        """
        self.config = get_config()
        
        # Set up output directory
        if output_dir is None:
            output_dir = self.config.get("video.output.directory", "output/videos")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize provider
        if provider is None:
            provider_name = self.config.get("video.generator.provider", "modelscope")
            self.provider = self._create_provider(provider_name)
        else:
            self.provider = provider
        
        self.logger.info(
            "video_generator_initialized",
            provider=self.provider.__class__.__name__,
            output_dir=str(self.output_dir)
        )
    
    def _create_provider(self, provider_name: str) -> BaseVideoGenerator:
        """
        Create video generation provider instance.
        
        Args:
            provider_name: Name of provider (modelscope, stability, runwayml)
        
        Returns:
            BaseVideoGenerator: Provider instance
            
        Raises:
            ModelLoadError: If provider cannot be loaded
        """
        self.logger.info("loading_video_provider", provider=provider_name)
        
        try:
            if provider_name.lower() == "modelscope":
                from ..services.modelscope_service import ModelScopeVideoGenerator
                return ModelScopeVideoGenerator()
            
            elif provider_name.lower() == "stability":
                from ..services.stability_service import StabilityVideoGenerator
                return StabilityVideoGenerator()
            
            elif provider_name.lower() == "runwayml":
                from ..services.runwayml_service import RunwayMLVideoGenerator
                return RunwayMLVideoGenerator()
            
            elif provider_name.lower() in ["walmart_media_studio", "media_studio", "walmart"]:
                from ..providers.walmart_media_studio import WalmartMediaStudioProvider
                return WalmartMediaStudioProvider()
            
            else:
                raise ModelLoadError(
                    f"Unknown video generation provider: {provider_name}",
                    details={"provider": provider_name}
                )
        
        except ImportError as e:
            raise ModelLoadError(
                f"Failed to import provider {provider_name}: {str(e)}",
                details={"provider": provider_name, "error": str(e)}
            )
        except Exception as e:
            raise ModelLoadError(
                f"Failed to initialize provider {provider_name}: {str(e)}",
                details={"provider": provider_name, "error": str(e)}
            )
    
    @log_execution_time(get_logger("VideoGenerator"))
    def generate_video(
        self,
        prompt: VideoPrompt,
        video_id: Optional[str] = None
    ) -> VideoGenerationResult:
        """
        Generate video from enhanced prompt.
        
        This is the main entry point for video generation. It:
        1. Validates parameters
        2. Generates video using provider
        3. Extracts metadata
        4. Creates output object
        
        Args:
            prompt: Enhanced video prompt
            video_id: Optional custom video ID
        
        Returns:
            VideoGenerationResult: Generation result with video or error
            
        Example:
            >>> result = generator.generate_video(prompt)
            >>> if result.success:
            ...     print(f"Video: {result.video.path}")
            ...     print(f"Duration: {result.video.duration}s")
        """
        start_time = time.time()
        
        # Generate unique ID
        if video_id is None:
            video_id = f"vid_{uuid.uuid4().hex[:12]}"
        
        self.logger.info(
            "generating_video",
            video_id=video_id,
            prompt_length=len(prompt.enhanced_prompt),
            style=prompt.style.value,
            mood=prompt.mood.value
        )
        
        processing_steps = []
        
        try:
            # Step 1: Validate parameters
            self._validate_parameters(prompt)
            processing_steps.append("Parameter validation")
            
            # Step 2: Prepare generation parameters
            duration = prompt.duration_hint or self.config.get("video.default_duration", 5)
            fps = self.config.get("video.default_fps", 24)
            resolution = self.config.get("video.default_resolution", {
                "width": 1920,
                "height": 1080
            })
            
            # Step 3: Generate video
            self.logger.info(
                "calling_provider",
                video_id=video_id,
                duration=duration,
                fps=fps,
                resolution=resolution
            )
            
            video_path = self.provider.generate(
                prompt=prompt.enhanced_prompt,
                negative_prompt=prompt.negative_prompt,
                duration=duration,
                fps=fps,
                resolution=resolution,
                video_id=video_id,
                output_dir=str(self.output_dir)
            )
            processing_steps.append("Video generation")
            
            # Step 4: Extract metadata
            metadata = self._extract_metadata(video_path, duration, fps, resolution)
            processing_steps.append("Metadata extraction")
            
            # Step 5: Create video object
            video = GeneratedVideo(
                id=video_id,
                path=str(video_path),
                status=GenerationStatus.COMPLETED,
                prompt_used=prompt.enhanced_prompt,
                metadata=metadata,
                generation_params={
                    "style": prompt.style.value,
                    "mood": prompt.mood.value,
                    "duration": duration,
                    "fps": fps,
                    "resolution": resolution,
                    "provider": self.provider.__class__.__name__,
                },
                generation_time=time.time() - start_time,
                tags=prompt.keywords
            )
            
            total_time = time.time() - start_time
            
            self.logger.info(
                "video_generated",
                video_id=video_id,
                path=str(video_path),
                duration=metadata.duration,
                file_size_mb=f"{metadata.file_size / (1024 * 1024):.2f}",
                generation_time=f"{total_time:.2f}s"
            )
            
            return VideoGenerationResult(
                success=True,
                video=video,
                processing_steps=processing_steps,
                total_time=total_time,
                warnings=[]
            )
        
        except InvalidVideoParametersError as e:
            self.logger.error(
                "invalid_parameters",
                video_id=video_id,
                error=str(e)
            )
            return VideoGenerationResult(
                success=False,
                video=self._create_failed_video(video_id, prompt, str(e)),
                processing_steps=processing_steps,
                total_time=time.time() - start_time,
                warnings=[str(e)]
            )
        
        except VideoGenerationError as e:
            self.logger.error(
                "generation_failed",
                video_id=video_id,
                error=str(e),
                exc_info=True
            )
            return VideoGenerationResult(
                success=False,
                video=self._create_failed_video(video_id, prompt, str(e)),
                processing_steps=processing_steps,
                total_time=time.time() - start_time,
                warnings=[]
            )
        
        except Exception as e:
            self.logger.error(
                "unexpected_error",
                video_id=video_id,
                error=str(e),
                exc_info=True
            )
            return VideoGenerationResult(
                success=False,
                video=self._create_failed_video(video_id, prompt, str(e)),
                processing_steps=processing_steps,
                total_time=time.time() - start_time,
                warnings=[]
            )
    
    def _validate_parameters(self, prompt: VideoPrompt) -> None:
        """
        Validate generation parameters.
        
        Args:
            prompt: Video prompt to validate
            
        Raises:
            InvalidVideoParametersError: If parameters are invalid
        """
        # Check prompt length
        if len(prompt.enhanced_prompt) < 10:
            raise InvalidVideoParametersError(
                "Enhanced prompt too short (minimum 10 characters)",
                details={"length": len(prompt.enhanced_prompt)}
            )
        
        # Check duration
        if prompt.duration_hint:
            if prompt.duration_hint < 1 or prompt.duration_hint > 60:
                raise InvalidVideoParametersError(
                    "Duration must be between 1 and 60 seconds",
                    details={"duration": prompt.duration_hint}
                )
        
        # Check provider availability
        if not self.provider.is_available():
            raise VideoGenerationError(
                "Video generation provider is not available",
                details={"provider": self.provider.__class__.__name__}
            )
    
    def _extract_metadata(
        self,
        video_path: str,
        duration: int,
        fps: int,
        resolution: Dict[str, int]
    ) -> VideoMetadata:
        """
        Extract metadata from generated video.
        
        Args:
            video_path: Path to video file
            duration: Video duration
            fps: Frames per second
            resolution: Video resolution
        
        Returns:
            VideoMetadata: Extracted metadata
        """
        path = Path(video_path)
        
        # Get file size
        file_size = path.stat().st_size if path.exists() else 0
        
        # Get video format from extension
        video_format = VideoFormat(path.suffix.lstrip('.').lower())
        
        # Get codec from config or default
        codec = self.config.get("video.output.codec", "h264")
        bitrate = self.config.get("video.output.bitrate", "5000k")
        
        return VideoMetadata(
            duration=float(duration),
            fps=fps,
            resolution=resolution,
            format=video_format,
            codec=codec,
            bitrate=bitrate,
            file_size=file_size
        )
    
    def _create_failed_video(
        self,
        video_id: str,
        prompt: VideoPrompt,
        error_message: str
    ) -> GeneratedVideo:
        """
        Create a GeneratedVideo object for failed generation.
        
        Args:
            video_id: Video identifier
            prompt: Original prompt
            error_message: Error description
        
        Returns:
            GeneratedVideo: Failed video object
        """
        return GeneratedVideo(
            id=video_id,
            path=str(self.output_dir / f"{video_id}_failed.mp4"),  # Placeholder path
            status=GenerationStatus.FAILED,
            prompt_used=prompt.enhanced_prompt,
            error_message=error_message,
            generation_params={
                "style": prompt.style.value,
                "mood": prompt.mood.value,
            }
        )
    
    def is_available(self) -> bool:
        """
        Check if video generator is ready to use.
        
        Returns:
            bool: True if generator is available
        """
        return self.provider.is_available()
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about the current provider.
        
        Returns:
            dict: Provider information
        """
        return {
            "name": self.provider.__class__.__name__,
            "available": self.provider.is_available(),
            "model_info": self.provider.get_model_info(),
            "output_dir": str(self.output_dir),
        }
