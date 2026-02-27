"""
OpenAI Sora 2 Video Provider

Integrates Zorro with OpenAI's Sora 2 text-to-video AI models.
Supports both sora-2 (fast) and sora-2-pro (high quality) models.

Official API: https://platform.openai.com/docs/guides/video
"""

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Literal, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..models.video_models import GeneratedVideo, VideoPrompt
from .base_provider import BaseVideoProvider

logger = logging.getLogger(__name__)


class SoraVideoProvider(BaseVideoProvider):
    """
    Video generation provider using OpenAI Sora 2.
    
    Models:
    - sora-2: Fast, flexible, good quality (social media, prototypes)
    - sora-2-pro: Higher quality, slower (production, marketing)
    
    Requires:
    - OPENAI_API_KEY environment variable
    - Sora API access enabled on your OpenAI account
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Literal["sora-2", "sora-2-pro"] = "sora-2",
        api_endpoint: str = "https://api.openai.com/v1/videos",
        timeout: int = 600,
        max_retries: int = 3,
        poll_interval: int = 10
    ):
        """
        Initialize Sora provider.
        
        Args:
            api_key: OpenAI API key (default: from OPENAI_API_KEY env var)
            model: "sora-2" (fast) or "sora-2-pro" (high quality)
            api_endpoint: Sora API base endpoint
            timeout: Maximum wait time for video generation (seconds)
            max_retries: Maximum retry attempts for API calls
            poll_interval: Seconds between status polls
        """
        super().__init__()
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.model = model
        self.api_endpoint = api_endpoint
        self.timeout = timeout
        self.max_retries = max_retries
        self.poll_interval = poll_interval
        
        # Session with retry logic
        self.session = self._create_session()
        
        logger.info(f"Initialized Sora provider: model={self.model}, endpoint={self.api_endpoint}")
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_video(self, prompt: VideoPrompt) -> GeneratedVideo:
        """
        Generate video using OpenAI Sora 2.
        
        Args:
            prompt: Video prompt with description and parameters
            
        Returns:
            GeneratedVideo with path, metadata, or error
        """
        try:
            logger.info(f"Generating video via Sora: {prompt.id} (model={self.model})")
            
            # Prepare request payload
            payload = self._prepare_payload(prompt)
            
            # Submit generation request
            job_response = self._submit_request(payload)
            
            if not job_response:
                return self._create_failed_video(prompt, "Failed to submit job to Sora API")
            
            video_id = job_response.get("id")
            if not video_id:
                return self._create_failed_video(prompt, "No video ID returned from Sora API")
            
            logger.info(f"Sora job submitted: {video_id}, status={job_response.get('status')}")
            
            # Poll for completion
            completed_job = self._poll_for_completion(video_id)
            
            if not completed_job or completed_job.get("status") != "completed":
                error = completed_job.get("error", "Video generation timed out or failed")
                return self._create_failed_video(prompt, error)
            
            # Download video
            video_path = self._download_video(video_id, prompt.id)
            
            if not video_path:
                return self._create_failed_video(prompt, "Failed to download generated video")
            
            # Create success result
            return GeneratedVideo(
                id=prompt.id,
                path=str(video_path),
                prompt=prompt.enhanced_description,
                duration=float(completed_job.get("seconds", 10)),
                resolution=completed_job.get("size", "1920x1080"),
                model_used=f"openai-{self.model}",
                generation_time=time.time() - job_response.get("created_at", time.time()),
                file_size=video_path.stat().st_size if video_path.exists() else 0,
                metadata={
                    "provider": "openai_sora",
                    "model": self.model,
                    "job_id": video_id,
                    "api_version": "v1",
                    "created_at": completed_job.get("created_at"),
                    "size": completed_job.get("size"),
                    "seconds": completed_job.get("seconds")
                }
            )
            
        except Exception as e:
            logger.error(f"Sora generation failed: {e}", exc_info=True)
            return self._create_failed_video(prompt, str(e))
    
    def _prepare_payload(self, prompt: VideoPrompt) -> Dict[str, Any]:
        """
        Prepare API request payload following official Sora 2 schema.
        
        Args:
            prompt: Video prompt
            
        Returns:
            Request payload dictionary
        """
        # Determine size (Sora uses string format like "1920x1080")
        width = prompt.width or 1920
        height = prompt.height or 1080
        size = f"{width}x{height}"
        
        # Determine duration (Sora uses string format)
        duration = str(prompt.duration or 10)
        
        payload = {
            "model": self.model,
            "prompt": prompt.enhanced_description,
            "size": size,
            "seconds": duration
        }
        
        # Add optional input reference image if provided
        # Note: This would require multipart/form-data encoding
        # For now, text-only prompts
        
        return payload
    
    def _submit_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Submit video generation request to Sora API.
        
        Official endpoint: POST https://api.openai.com/v1/videos
        
        Args:
            payload: Request payload
            
        Returns:
            Job response data or None if failed
        """
        try:
            logger.info("Submitting request to Sora API")
            logger.debug(f"Payload: {payload}")
            
            response = self.session.post(
                self.api_endpoint,
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Job submitted successfully: {data.get('id')}")
            return data
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"API request failed: {e}")
            
            # Provide helpful error messages
            if e.response.status_code == 401:
                logger.error("Authentication failed. Check OPENAI_API_KEY.")
            elif e.response.status_code == 403:
                logger.error("Access denied. Sora API may not be enabled on your account.")
            elif e.response.status_code == 429:
                logger.error("Rate limit exceeded. Try again later.")
            elif e.response.status_code == 400:
                # Content violation or invalid parameters
                error_detail = e.response.json().get("error", {})
                logger.error(f"Bad request: {error_detail}")
            
            return None
            
        except Exception as e:
            logger.error(f"Request submission error: {e}")
            return None
    
    def _poll_for_completion(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Poll for video generation completion.
        
        Official endpoint: GET https://api.openai.com/v1/videos/{video_id}
        
        States: queued, in_progress, completed, failed
        
        Args:
            video_id: Video job ID
            
        Returns:
            Completed job data or None if timeout/failed
        """
        start_time = time.time()
        last_progress = 0
        
        logger.info(f"Polling for completion: {video_id}")
        
        while time.time() - start_time < self.timeout:
            try:
                response = self.session.get(
                    f"{self.api_endpoint}/{video_id}",
                    headers=self._get_headers(),
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                status = data.get("status")
                progress = data.get("progress", 0)
                
                # Log progress updates
                if progress > last_progress:
                    logger.info(f"Job {video_id}: {status} - {progress}%")
                    last_progress = progress
                
                if status == "completed":
                    logger.info(f"Video generation completed: {video_id}")
                    return data
                
                elif status == "failed":
                    error_msg = data.get("error", "Unknown error")
                    logger.error(f"Video generation failed: {error_msg}")
                    return data  # Return with failed status
                
                # Still processing (queued or in_progress)
                time.sleep(self.poll_interval)
                
            except Exception as e:
                logger.error(f"Polling error: {e}")
                time.sleep(self.poll_interval)
        
        logger.error(f"Video generation timed out after {self.timeout}s")
        return None
    
    def _download_video(self, video_id: str, local_id: str) -> Optional[Path]:
        """
        Download generated video from Sora API.
        
        Official endpoint: GET https://api.openai.com/v1/videos/{video_id}/content
        
        Args:
            video_id: Sora video ID
            local_id: Local identifier for filename
            
        Returns:
            Path to downloaded video or None
        """
        try:
            logger.info(f"Downloading video: {video_id}")
            
            # Create output directory
            output_dir = Path("output/videos")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{local_id}_sora_{self.model}.mp4"
            
            # Download video content
            response = self.session.get(
                f"{self.api_endpoint}/{video_id}/content",
                headers=self._get_headers(),
                timeout=self.timeout,
                stream=True
            )
            response.raise_for_status()
            
            # Save to file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size_mb = output_path.stat().st_size / 1024 / 1024
            logger.info(f"Video downloaded: {output_path} ({file_size_mb:.2f}MB)")
            return output_path
            
        except Exception as e:
            logger.error(f"Video download failed: {e}")
            return None
    
    def _create_failed_video(self, prompt: VideoPrompt, error_message: str) -> GeneratedVideo:
        """
        Create a failed video result.
        
        Args:
            prompt: Original video prompt
            error_message: Error description
            
        Returns:
            GeneratedVideo with error information
        """
        logger.error(f"Video generation failed for {prompt.id}: {error_message}")
        
        return GeneratedVideo(
            id=prompt.id,
            path=f"output/videos/{prompt.id}_failed.mp4",  # Placeholder
            prompt=prompt.enhanced_description,
            duration=0.0,
            resolution="0x0",
            model_used=f"openai-{self.model}",
            generation_time=0.0,
            file_size=0,
            error_message=error_message,
            metadata={
                "provider": "openai_sora",
                "model": self.model,
                "error": error_message,
                "failed_at": time.time()
            }
        )
    
    def is_available(self) -> bool:
        """
        Check if Sora API is available and accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Try to list videos as a health check
            response = self.session.get(
                f"{self.api_endpoint}?limit=1",
                headers=self._get_headers(),
                timeout=10
            )
            return response.status_code == 200
            
        except Exception as e:
            logger.warning(f"Sora API health check failed: {e}")
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get provider information.
        
        Returns:
            Provider metadata dictionary
        """
        return {
            "name": "OpenAI Sora 2",
            "provider": "openai_sora",
            "model": self.model,
            "models_available": ["sora-2", "sora-2-pro"],
            "api_endpoint": self.api_endpoint,
            "authenticated": bool(self.api_key),
            "available": self.is_available(),
            "documentation": "https://platform.openai.com/docs/guides/video",
            "features": [
                "text-to-video",
                "image-reference support",
                "video remix",
                "webhook notifications",
                "multiple quality tiers"
            ],
            "model_details": {
                "sora-2": "Fast, flexible, good quality - ideal for rapid iteration",
                "sora-2-pro": "Higher quality, slower - ideal for production"
            }
        }
    
    def remix_video(self, video_id: str, new_prompt: str) -> Optional[Dict[str, Any]]:
        """
        Remix an existing Sora video with a new prompt.
        
        Official endpoint: POST https://api.openai.com/v1/videos/{video_id}/remix
        
        Args:
            video_id: ID of existing Sora video
            new_prompt: New prompt describing the change
            
        Returns:
            New job data or None if failed
        """
        try:
            logger.info(f"Remixing video {video_id}")
            
            response = self.session.post(
                f"{self.api_endpoint}/{video_id}/remix",
                json={"prompt": new_prompt},
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Remix job created: {data.get('id')}")
            return data
            
        except Exception as e:
            logger.error(f"Remix failed: {e}")
            return None
    
    def delete_video(self, video_id: str) -> bool:
        """
        Delete a video from OpenAI's storage.
        
        Official endpoint: DELETE https://api.openai.com/v1/videos/{video_id}
        
        Args:
            video_id: Sora video ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            response = self.session.delete(
                f"{self.api_endpoint}/{video_id}",
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(f"Video deleted: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return False
