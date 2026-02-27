"""ModelScope text-to-video generation service."""

import time
from pathlib import Path
from typing import Any, Dict, Optional

import torch

from ..core.video_generator import BaseVideoGenerator
from ..utils import LoggerMixin, get_config
from ..utils.exceptions import (
    InsufficientResourcesError,
    ModelLoadError,
    VideoGenerationError,
    VideoRenderError,
)


class ModelScopeVideoGenerator(BaseVideoGenerator, LoggerMixin):
    """
    ModelScope text-to-video generator.
    
    Uses the DAMO-VILAB text-to-video model from ModelScope.
    Supports both CPU and GPU (CUDA) execution.
    
    Model: damo-vilab/text-to-video-ms-1.7b
    
    Attributes:
        pipe: Diffusion pipeline for video generation
        device: Device for computation (cuda/cpu)
        model_loaded: Whether model is loaded
    
    Example:
        >>> generator = ModelScopeVideoGenerator()
        >>> video_path = generator.generate(
        ...     prompt="A professional training scene",
        ...     duration=10,
        ...     fps=24
        ... )
    """
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        Initialize ModelScope video generator.
        
        Args:
            model_name: Model identifier (uses config if None)
            device: Device to use (cuda/cpu/mps, auto-detects if None)
        """
        self.config = get_config()
        
        # Set model name
        if model_name is None:
            model_name = self.config.get(
                "video.generator.model_name",
                "damo-vilab/text-to-video-ms-1.7b"
            )
        self.model_name = model_name
        
        # Determine device
        if device is None:
            device = self._determine_device()
        self.device = device
        
        # Model state
        self.pipe = None
        self.model_loaded = False
        
        self.logger.info(
            "modelscope_generator_initialized",
            model=self.model_name,
            device=self.device
        )
        
        # Load model
        try:
            self._load_model()
        except Exception as e:
            self.logger.error(
                "model_load_failed",
                error=str(e),
                exc_info=True
            )
            # Don't raise - allow lazy loading
    
    def _determine_device(self) -> str:
        """
        Determine best available device.
        
        Returns:
            str: Device name (cuda, mps, or cpu)
        """
        # Check config first
        config_device = self.config.get("video.generator.device", "auto")
        
        if config_device != "auto":
            return config_device
        
        # Auto-detect
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        else:
            self.logger.warning(
                "gpu_not_available",
                message="GPU not available, using CPU (will be slower)"
            )
            return "cpu"
    
    def _load_model(self) -> None:
        """
        Load the ModelScope text-to-video model.
        
        Raises:
            ModelLoadError: If model cannot be loaded
        """
        if self.model_loaded:
            return
        
        self.logger.info("loading_model", model=self.model_name, device=self.device)
        
        try:
            from diffusers import DiffusionPipeline
            from diffusers.utils import export_to_video

            # Store export function for later use
            self._export_to_video = export_to_video
            
            # Load pipeline
            self.pipe = DiffusionPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
            )
            
            # Move to device
            self.pipe = self.pipe.to(self.device)
            
            # Enable optimizations if CUDA
            if self.device == "cuda":
                # Enable memory efficient attention if available
                try:
                    self.pipe.enable_model_cpu_offload()
                    self.logger.info("enabled_cpu_offload")
                except Exception as e:
                    self.logger.warning("cpu_offload_failed", error=str(e))
            
            self.model_loaded = True
            
            self.logger.info(
                "model_loaded_successfully",
                model=self.model_name,
                device=self.device
            )
        
        except ImportError as e:
            raise ModelLoadError(
                "Failed to import diffusers library. Install with: pip install diffusers",
                details={"error": str(e)}
            )
        except Exception as e:
            raise ModelLoadError(
                f"Failed to load ModelScope model: {str(e)}",
                details={"model": self.model_name, "error": str(e)}
            )
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        duration: int = 10,
        fps: int = 24,
        resolution: Dict[str, int] = None,
        video_id: Optional[str] = None,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate video from text prompt using ModelScope.
        
        Args:
            prompt: Text description for video
            negative_prompt: Elements to avoid
            duration: Video duration in seconds
            fps: Frames per second
            resolution: Video resolution (width/height)
            video_id: Unique identifier for output file
            output_dir: Output directory path
            **kwargs: Additional generation parameters
        
        Returns:
            str: Path to generated video file
            
        Raises:
            VideoGenerationError: On generation failure
            
        Example:
            >>> path = generator.generate(
            ...     prompt="A beautiful sunset over mountains",
            ...     duration=10,
            ...     fps=24
            ... )
        """
        # Ensure model is loaded
        if not self.model_loaded:
            self._load_model()
        
        if not self.model_loaded:
            raise VideoGenerationError(
                "Model not loaded. Cannot generate video.",
                details={"model": self.model_name}
            )
        
        # Set defaults
        if resolution is None:
            resolution = {"width": 512, "height": 512}  # ModelScope default
        if video_id is None:
            video_id = f"video_{int(time.time())}"
        if output_dir is None:
            output_dir = "output/videos"
        
        # Prepare output path
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        video_file = output_path / f"{video_id}.mp4"
        
        self.logger.info(
            "generating_video",
            video_id=video_id,
            prompt_length=len(prompt),
            duration=duration,
            fps=fps,
            resolution=resolution
        )
        
        start_time = time.time()
        
        try:
            # Get generation parameters from config
            num_inference_steps = self.config.get(
                "video.generator.num_inference_steps",
                kwargs.get("num_inference_steps", 25)
            )
            guidance_scale = self.config.get(
                "video.generator.guidance_scale",
                kwargs.get("guidance_scale", 9.0)
            )
            
            # Calculate number of frames
            num_frames = int(duration * fps / 8)  # ModelScope generates 8 fps
            num_frames = max(16, min(num_frames, 24))  # Clamp to 16-24 frames
            
            self.logger.debug(
                "generation_parameters",
                num_frames=num_frames,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale
            )
            
            # Generate video frames
            video_frames = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                num_frames=num_frames,
                height=resolution["height"],
                width=resolution["width"],
            ).frames
            
            # Export to video file
            self._export_to_video(video_frames, str(video_file), fps=fps)
            
            generation_time = time.time() - start_time
            file_size = video_file.stat().st_size
            
            self.logger.info(
                "video_generated",
                video_id=video_id,
                path=str(video_file),
                generation_time=f"{generation_time:.2f}s",
                file_size_mb=f"{file_size / (1024 * 1024):.2f}"
            )
            
            return str(video_file)
        
        except torch.cuda.OutOfMemoryError as e:
            raise InsufficientResourcesError(
                "GPU out of memory. Try reducing resolution or using CPU.",
                details={
                    "device": self.device,
                    "resolution": resolution,
                    "error": str(e)
                }
            )
        except Exception as e:
            self.logger.error(
                "generation_failed",
                video_id=video_id,
                error=str(e),
                exc_info=True
            )
            raise VideoRenderError(
                f"Video generation failed: {str(e)}",
                details={
                    "video_id": video_id,
                    "prompt": prompt[:100],
                    "error": str(e)
                }
            )
    
    def is_available(self) -> bool:
        """
        Check if ModelScope generator is available.
        
        Returns:
            bool: True if model is loaded and ready
        """
        return self.model_loaded
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            dict: Model information including name, device, status
        """
        return {
            "provider": "ModelScope",
            "model_name": self.model_name,
            "device": self.device,
            "loaded": self.model_loaded,
            "cuda_available": torch.cuda.is_available(),
            "gpu_memory": self._get_gpu_memory() if torch.cuda.is_available() else None,
        }
    
    def _get_gpu_memory(self) -> Dict[str, float]:
        """
        Get GPU memory information.
        
        Returns:
            dict: GPU memory stats in GB
        """
        if not torch.cuda.is_available():
            return {}
        
        return {
            "allocated_gb": torch.cuda.memory_allocated() / 1e9,
            "reserved_gb": torch.cuda.memory_reserved() / 1e9,
            "total_gb": torch.cuda.get_device_properties(0).total_memory / 1e9,
        }
    
    def unload_model(self) -> None:
        """
        Unload model from memory to free resources.
        """
        if self.pipe is not None:
            del self.pipe
            self.pipe = None
            self.model_loaded = False
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            self.logger.info("model_unloaded")
