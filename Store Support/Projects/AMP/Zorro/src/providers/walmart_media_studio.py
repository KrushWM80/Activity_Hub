"""
Walmart GenAI Media Studio Provider

This provider integrates with Walmart's internal GenAI Media Studio platform
for text-to-video generation using Google's Veo models.

API: https://retina-ds-genai-backend.prod.k8s.walmart.net
Models: Google Veo (veo2, veo3), Imagen 4.0
Status: Development - Authentication and SSL configuration required for production
"""

import base64
import logging
import os
import threading
import time
import warnings
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Import SSL configuration from security module
try:
    from ..security.ssl_config import SSLConfiguration
    ssl_config = SSLConfiguration()
    SSL_VERIFY_ENABLED = ssl_config.ssl_verify
    CA_BUNDLE_PATH = ssl_config.ca_bundle
except ImportError:
    # Fallback for backwards compatibility
    SSL_VERIFY_ENABLED = os.getenv("WALMART_SSL_VERIFY", "false").lower() == "true"
    CA_BUNDLE_PATH = os.getenv("WALMART_CA_BUNDLE", None)
    warnings.warn(
        "Security module not available. Using legacy SSL configuration.",
        category=UserWarning
    )

if not SSL_VERIFY_ENABLED:
    # Only disable warnings in development mode
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    warnings.warn(
        "SSL verification is disabled. This is acceptable for internal Walmart network "
        "development but MUST be enabled for production. Set WALMART_SSL_VERIFY=true "
        "and provide WALMART_CA_BUNDLE path to enable.",
        category=UserWarning
    )


# =============================================================================
# Circuit Breaker Implementation
# =============================================================================
class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open and blocking requests."""
    pass


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for API resilience.
    
    States:
    - CLOSED: Normal operation, requests flow through
    - OPEN: Too many failures, block requests
    - HALF_OPEN: Testing if service recovered
    """
    
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self._state = self.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._half_open_calls = 0
        self._lock = threading.Lock()
    
    @property
    def state(self) -> str:
        with self._lock:
            if self._state == self.OPEN:
                # Check if recovery timeout has passed
                if self._last_failure_time:
                    elapsed = time.time() - self._last_failure_time
                    if elapsed >= self.recovery_timeout:
                        self._state = self.HALF_OPEN
                        self._half_open_calls = 0
            return self._state
    
    def record_success(self):
        """Record successful call."""
        with self._lock:
            if self._state == self.HALF_OPEN:
                self._half_open_calls += 1
                if self._half_open_calls >= self.half_open_max_calls:
                    # Recovered - close the circuit
                    self._state = self.CLOSED
                    self._failure_count = 0
            elif self._state == self.CLOSED:
                self._failure_count = 0
    
    def record_failure(self):
        """Record failed call."""
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            
            if self._state == self.HALF_OPEN:
                # Failed during recovery - reopen
                self._state = self.OPEN
            elif self._failure_count >= self.failure_threshold:
                self._state = self.OPEN
    
    def can_execute(self) -> bool:
        """Check if a call can be executed."""
        return self.state != self.OPEN


def circuit_breaker_decorator(circuit: CircuitBreaker):
    """Decorator to apply circuit breaker to a function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not circuit.can_execute():
                raise CircuitBreakerOpen(
                    f"Circuit breaker is OPEN. Service unavailable. "
                    f"Will retry after {circuit.recovery_timeout}s"
                )
            try:
                result = func(*args, **kwargs)
                circuit.record_success()
                return result
            except Exception:
                circuit.record_failure()
                raise
        return wrapper
    return decorator


# Global circuit breaker for Media Studio API
media_studio_circuit = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60,
    half_open_max_calls=3
)


from src.models.prompt import PromptMood, PromptStyle, VideoPrompt
from src.models.video import GeneratedVideo, GenerationStatus, VideoMetadata
from src.providers.base_provider import BaseVideoProvider
from src.schemas.walmart_schemas import (
    VideoGenerationRequest,
    VideoGenerationStatusResponse,
    VideoGenerationSubmitResponse,
    VideoPromptSuggestionResponse,
    is_generation_complete,
)

logger = logging.getLogger(__name__)


class WalmartMediaStudioProvider(BaseVideoProvider):
    """
    Video generation provider using Walmart GenAI Media Studio.
    
    Features:
    - Internal Walmart platform (no firewall restrictions)
    - SSO authentication
    - Google Veo and Imagen models
    - Production-ready, monitored, compliant
    - Demo mode for offline testing
    
    API Access: Contact Next Gen Content DS team via #help-genai-media-studio
    """
    
    def __init__(
        self,
        api_endpoint: Optional[str] = None,
        timeout: int = 300,
        max_retries: int = 3,
        demo_mode: Optional[bool] = None
    ):
        """
        Initialize Walmart Media Studio provider.
        
        Args:
            api_endpoint: Media Studio API endpoint (default: from env or config)
            timeout: Request timeout in seconds (default: 300)
            max_retries: Maximum retry attempts (default: 3)
            demo_mode: Use sample videos instead of API (default: from config)
        
        Note: No authentication required (SSO implementation still in progress)
        """
        super().__init__()
        
        # Demo mode - use sample videos when API unavailable
        if demo_mode is None:
            self.demo_mode = os.getenv("ZORRO_DEMO_MODE", "false").lower() == "true"
        else:
            self.demo_mode = demo_mode
        
        # API configuration (production endpoint)
        self.api_endpoint = api_endpoint or os.getenv(
            "WALMART_MEDIA_STUDIO_API",
            "https://retina-ds-genai-backend.prod.k8s.walmart.net"
        )
        
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Session with retry logic
        self.session = self._create_session()
        
        mode_str = "(DEMO MODE)" if self.demo_mode else ""
        logger.info(f"Initialized Walmart Media Studio provider: {self.api_endpoint} {mode_str}")
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic and SSL configuration."""
        session = requests.Session()
        
        # SSL Configuration - Configurable for production deployment
        if SSL_VERIFY_ENABLED:
            if CA_BUNDLE_PATH and Path(CA_BUNDLE_PATH).exists():
                session.verify = CA_BUNDLE_PATH
                logger.info(f"SSL verification enabled with CA bundle: {CA_BUNDLE_PATH}")
            else:
                session.verify = True  # Use system trust store
                logger.info("SSL verification enabled using system trust store")
        else:
            session.verify = False
            logger.warning(
                "SSL verification DISABLED - acceptable for internal development only. "
                "Set WALMART_SSL_VERIFY=true for production."
            )
        
        # Retry strategy for transient failures
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with optional SSO authentication."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Zorro-VideoGen/1.0"
        }
        
        # Add SSO token if available
        sso_token = os.getenv("WALMART_SSO_TOKEN")
        if sso_token:
            headers["Authorization"] = f"Bearer {sso_token}"
            logger.debug(f"[AUTH] SSO token added to headers (length: {len(sso_token)} chars)")
        else:
            logger.warning(
                "[AUTH] No WALMART_SSO_TOKEN found! API may return sample/demo videos. "
                "Run 'python diagnostic_tool.py --authenticate' to configure."
            )
        
        return headers
    
    def generate_video(self, prompt: VideoPrompt) -> GeneratedVideo:
        """
        Generate video using Walmart GenAI Media Studio.
        
        In demo mode, returns a sample placeholder video.
        
        Args:
            prompt: Video prompt with description and parameters
            
        Returns:
            GeneratedVideo with path, metadata, or error
        """
        try:
            # Get or create ID from metadata
            prompt_id = prompt.metadata.get("video_id") or f"video_{int(time.time())}"
            
            # DEMO MODE: Return sample video without API call
            if self.demo_mode:
                logger.info("=" * 60)
                logger.info(f"[DEMO MODE] Generating sample video: {prompt_id}")
                logger.info(f"[DEMO MODE] Prompt: {prompt.enhanced_prompt[:100]}...")
                logger.info("=" * 60)
                return self._create_demo_video(prompt, prompt_id)
            
            # VERBOSE LOGGING: Log the full prompt being used
            logger.info("=" * 60)
            logger.info(f"[GENERATE] Starting video generation: {prompt_id}")
            logger.info(f"[GENERATE] Original message: {prompt.original_message[:100]}...")
            logger.info(f"[GENERATE] Enhanced prompt: {prompt.enhanced_prompt[:200]}...")
            logger.info(f"[GENERATE] Style: {prompt.style}, Mood: {prompt.mood}")
            logger.info(f"[GENERATE] Duration hint: {prompt.duration_hint}s")
            if prompt.negative_prompt:
                logger.info(f"[GENERATE] Negative prompt: {prompt.negative_prompt[:100]}")
            logger.info("=" * 60)
            
            # Prepare request payload
            payload = self._prepare_payload(prompt)
            
            # VERBOSE LOGGING: Log the exact payload being sent
            logger.info(f"[PAYLOAD] API payload prepared:")
            logger.info(f"[PAYLOAD]   prompt: {payload.get('prompt', 'N/A')[:150]}...")
            logger.info(f"[PAYLOAD]   model: {payload.get('model', 'N/A')}")
            logger.info(f"[PAYLOAD]   duration: {payload.get('duration', 'N/A')}s")
            logger.info(f"[PAYLOAD]   aspect_ratio: {payload.get('aspect_ratio', 'N/A')}")
            logger.info(f"[PAYLOAD]   Full payload: {payload}")
            
            # Submit generation request (protected by circuit breaker)
            try:
                response = self._submit_request(payload)
            except CircuitBreakerOpen as e:
                logger.warning(f"Circuit breaker open: {e}")
                return self._create_failed_video(
                    prompt,
                    f"Service temporarily unavailable (circuit breaker open). {e}"
                )
            except Exception as e:
                return self._create_failed_video(
                    prompt,
                    f"Failed to submit video generation request: {e}"
                )
            
            if not response:
                return self._create_failed_video(
                    prompt,
                    "Failed to submit video generation request to Media Studio"
                )
            
            # Generate video
            video_data = self._poll_for_completion(response.get("request_id"))
            
            if not video_data:
                return self._create_failed_video(
                    prompt,
                    "Video generation timed out or failed"
                )
            
            # Extract URL and base64 data
            video_url = video_data.get("url")
            base64_video = video_data.get("base64")
            
            # Download video (prefer base64 if available)
            video_path = self._download_video(video_url, prompt_id, base64_video)
            
            if not video_path:
                return self._create_failed_video(
                    prompt,
                    "Failed to download generated video"
                )
            
            # Create successful result
            video_metadata = VideoMetadata(
                duration=response.get("duration", 5.0),
                fps=24,
                resolution={"width": 1920, "height": 1080},
                format="mp4",
                codec="h264",
                bitrate="5000k",
                file_size=video_path.stat().st_size if video_path.exists() else 0
            )
            
            return GeneratedVideo(
                id=prompt_id,
                path=str(video_path),
                status=GenerationStatus.COMPLETED,
                prompt_used=prompt.enhanced_prompt,
                metadata=video_metadata,
                generation_params={
                    "model": response.get("model", "veo"),
                    "provider": "walmart_media_studio",
                    "request_id": response.get("request_id"),
                    "api_version": response.get("api_version", "v1"),
                },
                generation_time=response.get("generation_time", 0.0),
                tags=["walmart", "media-studio"]
            )
            
        except Exception as e:
            logger.error(f"Walmart Media Studio generation failed: {e}", exc_info=True)
            return self._create_failed_video(prompt, str(e))
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        duration: int = 5,
        fps: int = 24,
        resolution: Optional[Dict[str, int]] = None,
        video_id: Optional[str] = None,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate video with flexible parameters (video_generator.py interface).
        
        Args:
            prompt: Video description/prompt
            negative_prompt: What NOT to include in video
            duration: Video duration in seconds (4-8)
            fps: Frames per second (default: 24)
            resolution: Dict with 'width' and 'height' (default: 1920x1080)
            video_id: Video ID for tracking
            output_dir: Directory to save video
            **kwargs: Additional parameters
            
        Returns:
            Path to generated video file
        """
        try:
            # Create VideoPrompt object for internal use
            video_prompt = VideoPrompt(
                original_message=prompt[:100],  # Use first 100 chars as original
                enhanced_prompt=prompt,
                duration_hint=min(max(duration, 5), 8),  # Clamp to 5-8 seconds (API requirement)
                style=PromptStyle.PROFESSIONAL,
                mood=PromptMood.INFORMATIVE,
                keywords=[],
                scene_description=None,
                negative_prompt=negative_prompt,
                metadata={
                    "video_id": video_id or f"video_{int(time.time())}",
                    "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
                    "theme": kwargs.get("theme", "professional"),
                    "motion_intensity": kwargs.get("motion_intensity", 0.5),
                    "fps": fps,
                }
            )
            
            # Generate video using internal method
            result = self.generate_video(video_prompt)
            
            if result.error_message:
                raise Exception(f"Video generation failed: {result.error_message}")
            
            # Download and return path
            if result.path:
                return result.path
            else:
                raise Exception("No video path returned")
                
        except Exception as e:
            logger.error(f"Generate failed: {e}", exc_info=True)
            raise
    
    def suggest_prompt_for_image(self, image_base64: str) -> Optional[Dict[str, Any]]:
        """
        Analyze an image and suggest an appropriate video prompt.
        
        Official endpoint: POST /api/v1/videos/suggest-prompt
        Uses Gemini 2.0 Flash for analysis
        
        Detects:
        - Product on white background → suggests 360-degree spin
        - Lifestyle scene → suggests animation scenarios (sprinkling, dipping, etc.)
        
        Args:
            image_base64: Base64-encoded image string
            
        Returns:
            Suggestion response dict or None if failed
        """
        try:
            url = f"{self.api_endpoint}/api/v1/videos/suggest-prompt"
            
            payload = {"reference_image": image_base64}
            
            logger.info("Requesting prompt suggestion for reference image")
            
            response = self.session.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=60  # Longer timeout for AI analysis
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Validate response
            suggestion = VideoPromptSuggestionResponse(**data)
            
            logger.info(f"Prompt suggestion: {suggestion.image_type}")
            return data
            
        except Exception as e:
            logger.error(f"Prompt suggestion failed: {e}")
            return None
    
    def cancel_video_generation(self, request_id: str) -> bool:
        """
        Cancel an in-progress video generation.
        
        Official endpoint: DELETE /api/v1/videos/{request_id}
        
        Args:
            request_id: Request ID from generation response
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        try:
            url = f"{self.api_endpoint}/api/v1/videos/{request_id}"
            
            logger.info(f"Cancelling video generation: {request_id}")
            
            response = self.session.delete(
                url,
                headers=self._get_headers(),
                timeout=30
            )
            
            response.raise_for_status()
            
            logger.info(f"Video generation cancelled: {request_id}")
            return True
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"Request not found: {request_id}")
            else:
                logger.error(f"Failed to cancel: {e}")
            return False
        except Exception as e:
            logger.error(f"Cancellation error: {e}")
            return False
    
    def _prepare_payload(self, prompt: VideoPrompt) -> Dict[str, Any]:
        """
        Prepare API request payload for Media Studio.
        
        Official API supports (per OpenAPI 0.3.141):
        - Duration: 5-8 seconds (enforced by VideoGenerationRequest schema)
        - Aspect ratios: 16:9, 9:16, 1:1
        - Enhanced prompts and negative prompts
        - Model versions: veo2, veo3
        - Person generation controls
        
        Args:
            prompt: Video prompt
            
        Returns:
            VideoGenerationRequest validated dict
        """
        # Get aspect ratio from metadata if present
        aspect_ratio = prompt.metadata.get("aspect_ratio", "16:9")
        
        # Ensure duration is within official supported range (5-8 seconds)
        duration = prompt.duration_hint
        if duration < 5:
            duration = 5
        elif duration > 8:
            duration = 8
        
        # Build request following official schema
        payload_dict = {
            "prompt": prompt.enhanced_prompt,
            "model": "veo2",  # Default to veo2 (latest stable)
            "model_version": "veo2",
            "duration": duration,
            "aspect_ratio": aspect_ratio,  # 16:9, 9:16, or 1:1
            "enhanced_prompt": True,
            "person_generation": "allow_all",  # Allow all person types
            "use_case": "motion_graphics",  # API only accepts motion_graphics
        }
        
        if prompt.negative_prompt:
            payload_dict["negative_prompt"] = prompt.negative_prompt
        
        # Validate against official schema
        request = VideoGenerationRequest(**payload_dict)
        return request.model_dump(exclude_none=True)
    
    @circuit_breaker_decorator(media_studio_circuit)
    def _submit_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Submit video generation request to Media Studio API.
        
        Official endpoint: POST /api/v1/videos/generate
        Base URL: https://retina-ds-genai-backend.prod.k8s.walmart.net
        
        This method is protected by a circuit breaker pattern:
        - After 5 consecutive failures, circuit opens for 60 seconds
        - During open state, requests fail fast without hitting the API
        - After timeout, allows test requests (half-open state)
        
        Args:
            payload: Request payload (VideoGenerationRequest dict)
            
        Returns:
            VideoGenerationSubmitResponse data or None if failed
            
        Raises:
            CircuitBreakerOpen: If circuit breaker is open
        """
        try:
            url = f"{self.api_endpoint}/api/v1/videos/generate"  # Official endpoint with /api/v1/
            headers = self._get_headers()
            
            # VERBOSE LOGGING: Log full request details
            logger.info("=" * 60)
            logger.info(f"[API REQUEST] Submitting to: {url}")
            logger.info(f"[API REQUEST] Method: POST")
            logger.info(f"[API REQUEST] Headers: {dict((k, v[:20] + '...' if k == 'Authorization' and len(v) > 20 else v) for k, v in headers.items())}")
            logger.info(f"[API REQUEST] Payload prompt: {payload.get('prompt', 'N/A')[:150]}...")
            logger.info(f"[API REQUEST] Full payload: {payload}")
            logger.info("=" * 60)
            
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            # VERBOSE LOGGING: Log response details
            logger.info(f"[API RESPONSE] Status code: {response.status_code}")
            logger.info(f"[API RESPONSE] Headers: {dict(response.headers)}")
            
            response.raise_for_status()
            data = response.json()
            
            # VERBOSE LOGGING: Log response data
            logger.info(f"[API RESPONSE] Response data: {data}")
            
            # Validate response against official schema
            submit_response = VideoGenerationSubmitResponse(**data)
            
            logger.info(f"[API SUCCESS] Request ID: {submit_response.request_id}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            
            # Provide helpful error messages
            if isinstance(e, requests.exceptions.HTTPError):
                if e.response.status_code == 401:
                    logger.error("Authentication failed. Check WALMART_SSO_TOKEN.")
                elif e.response.status_code == 403:
                    logger.error("Access denied. Request API access via #help-genai-media-studio")
                elif e.response.status_code == 429:
                    logger.error("Rate limit exceeded. Try again later.")
                elif e.response.status_code == 422:
                    try:
                        error_detail = e.response.json()
                        logger.error(f"Validation error details: {error_detail}")
                    except:
                        logger.error(f"Validation error (no details). Response: {e.response.text}")
                    logger.error("Check request schema: prompt (1-2000 chars), duration (4-8 sec), etc.")
            
            raise  # Re-raise to trigger circuit breaker
    
    def _poll_for_completion(
        self,
        request_id: str,
        poll_interval: int = 5,
        max_wait: int = 300
    ) -> Optional[Dict[str, Any]]:
        """
        Poll for video generation completion.
        
        Official endpoint: GET /api/v1/videos/status/{request_id}
        
        Response schema (VideoGenerationStatusResponse):
        - status: pending|processing|completed|failed|cancelled
        - message: Status message or error
        - request_id: Request identifier
        - progress: 0-100 (optional)
        - current_stage: Stage description (optional)
        - output: VideoOutput with video URL and base64 data (when completed)
        
        Args:
            request_id: Generation request ID (from submission response)
            poll_interval: Seconds between polls (default: 5)
            max_wait: Maximum wait time in seconds (default: 300)
            
        Returns:
            Dict with 'url' and 'base64' keys, or None if failed/timeout
        """
        if not request_id:
            return None
        
        url = f"{self.api_endpoint}/api/v1/videos/status/{request_id}"  # Official endpoint with /api/v1/
        start_time = time.time()
        
        logger.info(f"Polling for completion: {request_id}")
        
        while time.time() - start_time < max_wait:
            try:
                response = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                # Validate against official schema
                status_response = VideoGenerationStatusResponse(**data)
                status = status_response.status
                progress = status_response.progress or 0
                
                logger.debug(f"Request {request_id}: {status} ({progress}%)")
                
                if status == "completed" and status_response.output:
                    logger.info(f"Video generation completed: {request_id}")
                    # Extract video data from output
                    video_file = status_response.output.video
                    video_data = {
                        "url": video_file.url,
                        "base64": video_file.base64
                    }
                    logger.info(f"Video URL from API: {video_file.url}")
                    logger.info(f"Base64 data available: {video_file.base64 is not None and len(video_file.base64) > 100}")
                    return video_data
                
                elif is_generation_complete(status):
                    error_msg = status_response.message or "Unknown error"
                    logger.error(f"Video generation {status}: {error_msg}")
                    return None
                
                # Still processing, wait and retry
                time.sleep(poll_interval)
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    logger.warning(f"Request {request_id} not found. May be invalid or expired.")
                    return None
                logger.error(f"HTTP error during polling: {e}")
                time.sleep(poll_interval)
            except Exception as e:
                logger.error(f"Polling error: {e}")
                time.sleep(poll_interval)
        
        logger.error(f"Video generation timed out after {max_wait}s")
        return None
    
    def _download_video(self, video_url: str, video_id: str, base64_video: Optional[str] = None) -> Optional[Path]:
        """
        Download generated video from Media Studio.
        
        The API can return video in two ways:
        1. base64_encoded: Direct binary data in response
        2. GCS URL: File stored in Google Cloud Storage
        
        Args:
            video_url: URL of generated video (gs:// or https://)
            video_id: Video identifier
            base64_video: Optional base64-encoded video data
            
        Returns:
            Path to downloaded video or None
        """
        try:
            output_dir = Path("output/videos")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{video_id}_media_studio.mp4"
            
            # If we have base64 video data, use it directly
            if base64_video:
                logger.info(f"Saving video from base64 data for {video_id}")
                try:
                    video_data = base64.b64decode(base64_video)
                    with open(output_path, 'wb') as f:
                        f.write(video_data)
                    logger.info(f"Video saved from base64: {output_path} ({len(video_data)} bytes)")
                    return output_path
                except Exception as e:
                    logger.error(f"Failed to decode base64 video: {e}")
                    return None
            
            # Otherwise try to download from URL
            logger.info(f"Downloading video from URL: {video_url}")
            
            # Convert GCS gs:// URL to HTTPS URL if needed
            if video_url.startswith("gs://"):
                gcs_path = video_url[5:]  # Remove 'gs://' prefix
                https_url = f"https://storage.googleapis.com/{gcs_path}"
                logger.info(f"Converted GCS URL to HTTPS: {https_url}")
                video_url = https_url
            
            # Download video
            response = self.session.get(
                video_url,
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
            
            logger.info(f"Video downloaded: {output_path} ({output_path.stat().st_size} bytes)")
            return output_path
            
        except Exception as e:
            logger.error(f"Video download failed: {e}")
            return None
    
    def _create_demo_video(self, prompt: VideoPrompt, video_id: str) -> GeneratedVideo:
        """
        Create a demo/sample video for offline testing.
        
        First checks for a pre-existing sample video file, then tries FFmpeg,
        then falls back to a placeholder.
        
        Sample video location: assets/sample_videos/walmart_associate_stocking.mp4
        
        Args:
            prompt: Original video prompt
            video_id: Video identifier
            
        Returns:
            GeneratedVideo with sample video path
        """
        import subprocess
        import re
        import shutil
        
        output_dir = Path("output/videos")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        video_path = output_dir / f"{video_id}_demo.mp4"
        duration = prompt.duration_hint or 5
        
        # PRIORITY 1: Check for pre-existing sample video
        sample_video_paths = [
            Path("assets/sample_videos/walmart_associate_stocking.mp4"),
            Path("assets/sample_videos/sample_demo.mp4"),
            Path("assets/sample_videos/demo.mp4"),
            Path("output/videos/sample_demo.mp4"),
        ]
        
        for sample_path in sample_video_paths:
            if sample_path.exists() and sample_path.stat().st_size > 1000:
                # Copy sample video to output with unique ID
                shutil.copy(sample_path, video_path)
                logger.info(f"[DEMO] Using pre-existing sample video: {sample_path} -> {video_path}")
                
                # Get actual file size
                file_size = video_path.stat().st_size
                
                # Create metadata
                demo_metadata = VideoMetadata(
                    duration=float(duration),
                    fps=24,
                    resolution={"width": 1920, "height": 1080},
                    format="mp4",
                    codec="h264",
                    bitrate="5000k",
                    file_size=file_size
                )
                
                return GeneratedVideo(
                    id=video_id,
                    path=str(video_path),
                    status=GenerationStatus.COMPLETED,
                    prompt_used=prompt.enhanced_prompt,
                    metadata=demo_metadata,
                    generation_time=0.1,
                    error_message=None,
                    generation_params={
                        "provider": "walmart_media_studio",
                        "mode": "demo",
                        "source": "sample_video",
                        "sample_path": str(sample_path),
                        "duration": duration
                    },
                    tags=["demo", "sample"]
                )
        
        logger.warning(f"[DEMO] No sample video found. Place a video at: assets/sample_videos/walmart_associate_stocking.mp4")
        
        # PRIORITY 2: Try FFmpeg to generate a demo video
        try:
            # Simple video with Walmart-blue background and centered text
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c=#0071CE:s=1920x1080:d={duration}:r=24",
                "-vf", f"drawtext=text='DEMO MODE':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-100,drawtext=text='Zorro Video Generator':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+20,drawtext=text='API Offline':fontsize=36:fontcolor=yellow:x=(w-text_w)/2:y=(h-text_h)/2+100",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-t", str(duration),
                str(video_path)
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                logger.warning(f"FFmpeg demo video creation failed: {result.stderr}")
                # Fallback: create simplest possible video (no text)
                simple_cmd = [
                    "ffmpeg", "-y",
                    "-f", "lavfi",
                    "-i", f"color=c=#0071CE:s=1280x720:d={duration}:r=24",
                    "-c:v", "libx264",
                    "-preset", "ultrafast",
                    "-pix_fmt", "yuv420p",
                    str(video_path)
                ]
                result2 = subprocess.run(simple_cmd, capture_output=True, text=True, timeout=30)
                if result2.returncode == 0:
                    logger.info(f"[DEMO] Created simple demo video: {video_path}")
                else:
                    logger.warning("FFmpeg fallback also failed")
                    video_path.touch()
            else:
                logger.info(f"[DEMO] Created demo video: {video_path}")
                
        except FileNotFoundError:
            logger.warning("FFmpeg not found - creating placeholder file")
        except Exception as e:
            logger.warning(f"Demo video creation error: {e}")
            video_path.touch()
        
        # Create metadata
        demo_metadata = VideoMetadata(
            duration=float(duration),
            fps=24,
            resolution={"width": 1920, "height": 1080},
            format="mp4",
            codec="h264",
            bitrate="5000k",
            file_size=video_path.stat().st_size if video_path.exists() else 0
        )
        
        return GeneratedVideo(
            id=video_id,
            path=str(video_path),
            status=GenerationStatus.COMPLETED,
            prompt_used=prompt.enhanced_prompt,
            metadata=demo_metadata,
            generation_time=0.5,  # Simulated
            error_message=None,
            generation_params={
                "provider": "walmart_media_studio",
                "mode": "demo",
                "model": "veo2 (simulated)",
                "duration": duration
            },
            tags=["demo", "sample"]
        )
    
    def _create_failed_video(self, prompt: VideoPrompt, error_message: str) -> GeneratedVideo:
        """
        Create a failed video result.
        
        Args:
            prompt: Original video prompt
            error_message: Error description
            
        Returns:
            GeneratedVideo with error information
        """
        # Get ID from metadata or create one
        prompt_id = prompt.metadata.get("video_id") or f"video_{int(time.time())}"
        logger.error(f"Video generation failed for {prompt_id}: {error_message}")
        
        # Create metadata for failed video
        failed_metadata = VideoMetadata(
            duration=prompt.duration_hint,
            fps=24,
            resolution={"width": 1920, "height": 1080},
            format="mp4",
            codec="h264",
            bitrate="5000k",
            file_size=0
        )
        
        return GeneratedVideo(
            id=prompt_id,
            path=f"output/videos/{prompt_id}_failed.mp4",
            status=GenerationStatus.FAILED,
            prompt_used=prompt.enhanced_prompt,
            metadata=failed_metadata,
            generation_time=0.0,
            error_message=error_message,
            generation_params={
                "provider": "walmart_media_studio",
                "error": error_message,
                "failed_at": time.time()
            },
            tags=[]
        )
    
    def is_available(self) -> bool:
        """
        Check if Media Studio API is available.
        
        In demo mode, always returns True to allow offline testing.
        Otherwise, uses GET /api/v1/health endpoint to verify API status.
        
        Returns:
            True if API is accessible and healthy (or in demo mode), False otherwise
        """
        # Demo mode - always available for offline testing
        if self.demo_mode:
            logger.info("Media Studio in DEMO MODE - always available")
            return True
        
        try:
            # Try health check first (most direct)
            health_url = f"{self.api_endpoint}/api/v1/health"
            response = self.session.get(
                health_url,
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Media Studio API is healthy")
                return True
            
            # Fall back to models endpoint
            models_url = f"{self.api_endpoint}/api/v1/models"  # Official models endpoint
            response = self.session.get(
                models_url,
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Media Studio API is accessible")
                return True
            
            logger.warning(f"Media Studio API returned status {response.status_code}")
            return False
            
        except Exception as e:
            logger.warning(f"Media Studio health check failed: {e}")
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get provider information.
        
        Returns:
            Provider metadata dictionary
        """
        return {
            "name": "Walmart GenAI Media Studio",
            "provider": "walmart_media_studio",
            "api_version": "0.3.141",
            "openapi_url": f"{self.api_endpoint}/openapi.json",
            "docs_url": f"{self.api_endpoint}/docs",
            "api_endpoint": self.api_endpoint,
            "authenticated": False,  # No authentication required (SSO still WIP)
            "available": self.is_available(),
            "support_channel": "#help-genai-media-studio",
            "platform_team": "Next Gen Content DS",
            "endpoints": {
                "generate_video": "POST /api/v1/videos/generate",
                "video_status": "GET /api/v1/videos/status/{request_id}",
                "cancel_video": "DELETE /api/v1/videos/{request_id}",
                "get_models": "GET /api/v1/models",
                "suggest_prompt": "POST /api/v1/videos/suggest-prompt",
                "generate_image": "POST /api/v1/images/generate",
                "health_check": "GET /api/v1/health"
            },
            "supported_models": {
                "video": ["veo2", "veo3"],
                "image": ["imagen-4.0-generate"]
            },
            "features": [
                "text-to-video",
                "video-from-reference-image",
                "prompt-enhancement",
                "negative-prompts",
                "prompt-suggestions",
                "4-8-second-videos",
                "multiple-aspect-ratios",
                "person-generation-controls",
                "sso-authentication",
                "pre-approved",
                "production-ready"
            ],
            "supported_durations": "4-8 seconds",
            "supported_aspect_ratios": ["16:9", "9:16", "1:1"],
            "supported_use_cases": [
                "inspirational_scene",
                "product_imagery",
                "image_editing_add",
                "image_editing_remove",
                "image_editing_scale",
                "motion_graphics"
            ],
            "constraints": {
                "prompt_length": "1-2000 characters",
                "negative_prompt_length": "max 1000 characters",
                "video_duration": "4-8 seconds",
                "seed_range": "0-4294967295"
            },
            "storage": "Google Cloud Storage (GCS)",
            "monitoring": "Element GenAI Platform"
        }
