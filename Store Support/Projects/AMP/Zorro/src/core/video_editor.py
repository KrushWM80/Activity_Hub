"""Video editing module for trimming, transitions, and effects."""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from ..utils import LoggerMixin, get_config
from ..utils.exceptions import (
    EditOperationError,
    VideoFileNotFoundError,
)


class VideoEditor(LoggerMixin):
    """
    Video editing service using FFmpeg.
    
    Provides capabilities for:
    - Trimming and cutting
    - Adding transitions
    - Seamless looping
    - Color correction
    - Audio mixing
    - Format conversion
    
    Attributes:
        config: Configuration object
        ffmpeg_path: Path to FFmpeg executable
    
    Example:
        >>> editor = VideoEditor()
        >>> trimmed = editor.trim(
        ...     video_path="input.mp4",
        ...     start_time=2.0,
        ...     end_time=8.0
        ... )
    """
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """
        Initialize video editor.
        
        Args:
            ffmpeg_path: Path to FFmpeg executable (auto-detects if None)
        """
        self.config = get_config()
        
        # Find FFmpeg
        if ffmpeg_path is None:
            ffmpeg_path = self._find_ffmpeg()
        self.ffmpeg_path = ffmpeg_path
        
        # Verify FFmpeg is available
        if not self._verify_ffmpeg():
            self.logger.warning(
                "ffmpeg_not_available",
                message="FFmpeg not found. Video editing features disabled."
            )
        
        self.logger.info(
            "video_editor_initialized",
            ffmpeg_path=self.ffmpeg_path
        )
    
    def _find_ffmpeg(self) -> str:
        """
        Find FFmpeg executable.
        
        Returns:
            str: Path to FFmpeg
        """
        # Try common locations
        import shutil
        
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg:
            return ffmpeg
        
        # Try common installation paths
        common_paths = [
            "ffmpeg",
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
        ]
        
        for path in common_paths:
            if Path(path).exists():
                return path
        
        return "ffmpeg"  # Hope it's in PATH
    
    def _verify_ffmpeg(self) -> bool:
        """
        Verify FFmpeg is available and working.
        
        Returns:
            bool: True if FFmpeg is available
        """
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def trim(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_path: Optional[str] = None
    ) -> str:
        """
        Trim video to specified time range.
        
        Args:
            video_path: Path to input video
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output path (auto-generated if None)
        
        Returns:
            str: Path to trimmed video
            
        Raises:
            VideoFileNotFoundError: If input video not found
            EditOperationError: If trimming fails
            
        Example:
            >>> trimmed = editor.trim("video.mp4", 2.0, 10.0)
        """
        # Validate input
        video_file = Path(video_path)
        if not video_file.exists():
            raise VideoFileNotFoundError(
                f"Video file not found: {video_path}",
                details={"path": video_path}
            )
        
        # Validate times
        if start_time < 0 or end_time <= start_time:
            raise EditOperationError(
                "Invalid time range",
                details={"start": start_time, "end": end_time}
            )
        
        # Generate output path
        if output_path is None:
            output_path = str(
                video_file.parent / f"{video_file.stem}_trimmed{video_file.suffix}"
            )
        
        self.logger.info(
            "trimming_video",
            input=video_path,
            output=output_path,
            start=start_time,
            end=end_time
        )
        
        try:
            # FFmpeg trim command
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-ss", str(start_time),
                "-to", str(end_time),
                "-c", "copy",  # Copy codec (fast)
                "-y",  # Overwrite output
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise EditOperationError(
                    f"FFmpeg trim failed: {result.stderr}",
                    details={"command": " ".join(cmd)}
                )
            
            self.logger.info("video_trimmed", output=output_path)
            return output_path
        
        except subprocess.TimeoutExpired:
            raise EditOperationError("Trim operation timed out")
        except Exception as e:
            raise EditOperationError(
                f"Trim operation failed: {str(e)}",
                details={"error": str(e)}
            )
    
    def add_fade_transition(
        self,
        video_path: str,
        fade_in_duration: float = 0.5,
        fade_out_duration: float = 0.5,
        output_path: Optional[str] = None
    ) -> str:
        """
        Add fade in/out transitions to video.
        
        Args:
            video_path: Path to input video
            fade_in_duration: Fade in duration in seconds
            fade_out_duration: Fade out duration in seconds
            output_path: Output path
        
        Returns:
            str: Path to output video
        """
        video_file = Path(video_path)
        if not video_file.exists():
            raise VideoFileNotFoundError(f"Video not found: {video_path}")
        
        if output_path is None:
            output_path = str(
                video_file.parent / f"{video_file.stem}_faded{video_file.suffix}"
            )
        
        self.logger.info(
            "adding_fade_transitions",
            input=video_path,
            fade_in=fade_in_duration,
            fade_out=fade_out_duration
        )
        
        # Get video duration
        duration = self._get_video_duration(video_path)
        
        # Build filter complex
        fade_out_start = duration - fade_out_duration
        
        filter_complex = (
            f"fade=t=in:st=0:d={fade_in_duration},"
            f"fade=t=out:st={fade_out_start}:d={fade_out_duration}"
        )
        
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-vf", filter_complex,
                "-c:a", "copy",  # Copy audio without re-encoding
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise EditOperationError(f"Fade transition failed: {result.stderr}")
            
            self.logger.info("fade_transitions_added", output=output_path)
            return output_path
        
        except Exception as e:
            raise EditOperationError(f"Failed to add fade: {str(e)}")
    
    def create_seamless_loop(
        self,
        video_path: str,
        blend_duration: float = 0.3,
        output_path: Optional[str] = None
    ) -> str:
        """
        Create a seamless loop by blending end with beginning.
        
        Args:
            video_path: Path to input video
            blend_duration: Duration of blend in seconds
            output_path: Output path
        
        Returns:
            str: Path to looped video
        """
        video_file = Path(video_path)
        if not video_file.exists():
            raise VideoFileNotFoundError(f"Video not found: {video_path}")
        
        if output_path is None:
            output_path = str(
                video_file.parent / f"{video_file.stem}_loop{video_file.suffix}"
            )
        
        self.logger.info(
            "creating_seamless_loop",
            input=video_path,
            blend_duration=blend_duration
        )
        
        # Get video duration
        duration = self._get_video_duration(video_path)
        
        # Extract beginning and end segments
        try:
            # Create crossfade between end and beginning
            filter_complex = (
                f"[0:v]trim=duration={duration}[main];"
                f"[0:v]trim=start={duration - blend_duration}:duration={blend_duration}[end];"
                f"[0:v]trim=duration={blend_duration}[start];"
                f"[end][start]blend=all_expr='A*(1-T/{blend_duration})+B*(T/{blend_duration})'[blend];"
                f"[main][blend]concat=n=2[out]"
            )
            
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-filter_complex", filter_complex,
                "-map", "[out]",
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                # Fallback to simpler loop
                self.logger.warning("complex_loop_failed_using_simple")
                return self._simple_loop(video_path, output_path)
            
            self.logger.info("seamless_loop_created", output=output_path)
            return output_path
        
        except Exception as e:
            self.logger.warning(f"seamless_loop_failed: {e}, using simple loop")
            return self._simple_loop(video_path, output_path)
    
    def _simple_loop(self, video_path: str, output_path: str) -> str:
        """Simple loop without blending."""
        cmd = [
            self.ffmpeg_path,
            "-stream_loop", "1",
            "-i", video_path,
            "-c", "copy",
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            raise EditOperationError(f"Simple loop failed: {result.stderr}")
        
        return output_path
    
    def adjust_colors(
        self,
        video_path: str,
        brightness: float = 0.0,
        contrast: float = 1.0,
        saturation: float = 1.0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Adjust video colors.
        
        Args:
            video_path: Input video path
            brightness: Brightness adjustment (-1.0 to 1.0)
            contrast: Contrast multiplier (0.0 to 3.0)
            saturation: Saturation multiplier (0.0 to 3.0)
            output_path: Output path
        
        Returns:
            str: Path to adjusted video
        """
        video_file = Path(video_path)
        if not video_file.exists():
            raise VideoFileNotFoundError(f"Video not found: {video_path}")
        
        if output_path is None:
            output_path = str(
                video_file.parent / f"{video_file.stem}_adjusted{video_file.suffix}"
            )
        
        self.logger.info(
            "adjusting_colors",
            brightness=brightness,
            contrast=contrast,
            saturation=saturation
        )
        
        # Build eq filter
        filter_str = f"eq=brightness={brightness}:contrast={contrast}:saturation={saturation}"
        
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-vf", filter_str,
                "-c:a", "copy",
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise EditOperationError(f"Color adjustment failed: {result.stderr}")
            
            self.logger.info("colors_adjusted", output=output_path)
            return output_path
        
        except Exception as e:
            raise EditOperationError(f"Color adjustment failed: {str(e)}")
    
    def _get_video_duration(self, video_path: str) -> float:
        """
        Get video duration using FFprobe.
        
        Args:
            video_path: Path to video
        
        Returns:
            float: Duration in seconds
        """
        try:
            ffprobe_path = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
            
            cmd = [
                ffprobe_path,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return float(data["format"]["duration"])
            else:
                # Fallback
                return 10.0
        
        except Exception as e:
            self.logger.warning(f"failed_to_get_duration: {e}")
            return 10.0
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """
        Get detailed video information.
        
        Args:
            video_path: Path to video
        
        Returns:
            dict: Video information (duration, resolution, codec, etc.)
        """
        try:
            ffprobe_path = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
            
            cmd = [
                ffprobe_path,
                "-v", "error",
                "-show_format",
                "-show_streams",
                "-of", "json",
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {}
        
        except Exception as e:
            self.logger.error(f"failed_to_get_video_info: {e}")
            return {}
    
    def is_available(self) -> bool:
        """Check if video editor (FFmpeg) is available."""
        return self._verify_ffmpeg()

    def add_ai_disclosure_watermark(
        self,
        video_path: str,
        text: str = "AI Generated",
        position: str = "bottom_right",
        output_path: Optional[str] = None,
        font_size: int = 18,
        opacity: float = 0.7
    ) -> str:
        """
        Add AI disclosure watermark text to video for legal compliance.
        
        Args:
            video_path: Path to input video
            text: Watermark text (default: "AI Generated")
            position: Position - "bottom_right", "bottom_left", "top_right", "top_left"
            output_path: Output path (auto-generated if None)
            font_size: Font size in pixels
            opacity: Text opacity (0.0 to 1.0)
        
        Returns:
            str: Path to watermarked video
            
        Raises:
            VideoFileNotFoundError: If input video not found
            EditOperationError: If watermarking fails
        """
        video_file = Path(video_path)
        if not video_file.exists():
            raise VideoFileNotFoundError(f"Video not found: {video_path}")
        
        if output_path is None:
            output_path = str(
                video_file.parent / f"{video_file.stem}_watermarked{video_file.suffix}"
            )
        
        self.logger.info(
            "adding_ai_disclosure_watermark",
            input=video_path,
            text=text,
            position=position
        )
        
        # Position mapping for FFmpeg drawtext filter
        position_map = {
            "bottom_right": "x=w-tw-10:y=h-th-10",
            "bottom_left": "x=10:y=h-th-10",
            "top_right": "x=w-tw-10:y=10",
            "top_left": "x=10:y=10",
            "center": "x=(w-tw)/2:y=(h-th)/2"
        }
        
        pos = position_map.get(position, position_map["bottom_right"])
        alpha = min(1.0, max(0.1, opacity))
        
        # Escape special characters in text for FFmpeg
        escaped_text = text.replace("'", "\\'").replace(":", "\\:")
        
        # Build drawtext filter with semi-transparent background box
        filter_str = (
            f"drawtext=text='{escaped_text}':"
            f"{pos}:"
            f"fontsize={font_size}:"
            f"fontcolor=white@{alpha}:"
            f"box=1:"
            f"boxcolor=black@{alpha * 0.5}:"
            f"boxborderw=5"
        )
        
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-vf", filter_str,
                "-c:a", "copy",
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise EditOperationError(
                    f"Watermark addition failed: {result.stderr}",
                    details={"command": " ".join(cmd)}
                )
            
            self.logger.info("ai_disclosure_watermark_added", output=output_path)
            return output_path
        
        except subprocess.TimeoutExpired:
            raise EditOperationError("Watermark operation timed out")
        except Exception as e:
            if isinstance(e, EditOperationError):
                raise
            raise EditOperationError(
                f"Watermark operation failed: {str(e)}",
                details={"error": str(e)}
            )
