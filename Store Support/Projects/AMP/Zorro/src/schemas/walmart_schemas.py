"""
Walmart GenAI Media Studio API Schemas

Official OpenAPI 3.1 schemas matching:
https://retina-ds-genai-backend.prod.k8s.walmart.net/openapi.json

Version: 0.3.141
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

# ============================================================================
# VIDEO GENERATION SCHEMAS
# ============================================================================

class VideoGenerationRequest(BaseModel):
    """Request model for video generation - matches official OpenAPI schema"""
    
    # Video content
    prompt: str = Field(
        ...,
        description="Text prompt for video generation (1-2000 characters)",
        min_length=1,
        max_length=2000
    )
    
    # Model selection
    use_case: Optional[Literal[
        "inspirational_scene",
        "product_imagery", 
        "image_editing_add",
        "image_editing_remove",
        "image_editing_scale",
        "motion_graphics"
    ]] = Field(
        None,
        description="Use case for generation (can be omitted if model parameter is provided)"
    )
    
    model: Optional[str] = Field(
        None,
        description="Specific model to use (takes priority over use_case)"
    )
    
    model_version: Literal["veo2", "veo3"] = Field(
        "veo2",
        description="Video model version to use"
    )
    
    # Duration and aspect ratio
    duration: float = Field(
        5,
        description="Video duration in seconds (4-8 seconds)",
        ge=4,
        le=8
    )
    
    aspect_ratio: str = Field(
        "1:1",
        description="Aspect ratio for the output (16:9, 9:16, or 1:1)"
    )
    
    # Prompt enhancement
    enhanced_prompt: bool = Field(
        True,
        description="Whether to enhance the prompt with AI improvements"
    )
    
    negative_prompt: Optional[str] = Field(
        None,
        description="What to exclude from generation (max 1000 characters)",
        max_length=1000
    )
    
    # Reference and customization
    reference_image: Optional[str] = Field(
        None,
        description="Base64 encoded reference image for style/layout"
    )
    
    user_mask: Optional[str] = Field(
        None,
        description="Base64 encoded reference mask (required for image_editing_add/remove)"
    )
    
    image_reference_type: Literal["none", "style", "layout", "composition"] = Field(
        "none",
        description="Type of image reference"
    )
    
    preserve_layout: bool = Field(
        False,
        description="Whether to preserve the layout from reference image (uses ControlNet)"
    )
    
    reference_images: Optional[List[str]] = Field(
        None,
        description="List of base64 encoded reference images (max 4, only for Gemini/Recontext)"
    )
    
    # Advanced options
    seed: Optional[int] = Field(
        None,
        description="Random seed for reproducible generation",
        ge=0,
        le=4294967295
    )
    
    person_generation: Literal["allow_adult", "dont_allow", "allow_all"] = Field(
        "allow_all",
        description="Person generation settings"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "A vibrant product shot of a Walmart store entrance at sunset with customers walking",
                "model": "veo2",
                "duration": 5,
                "aspect_ratio": "16:9",
                "enhanced_prompt": True,
                "person_generation": "allow_all"
            }
        }


class VideoGenerationSubmitResponse(BaseModel):
    """Response after submitting a video generation request"""
    
    status: Literal["pending", "processing", "completed", "failed", "cancelled"] = Field(
        ...,
        description="Current status of the request"
    )
    
    message: str = Field(
        ...,
        description="Status message"
    )
    
    request_id: str = Field(
        ...,
        description="Unique request ID for polling and cancellation"
    )
    
    polling_url: str = Field(
        ...,
        description="URL endpoint to poll for status updates"
    )


class VideoMetadata(BaseModel):
    """Metadata about video generation"""
    
    seed: int = Field(
        ...,
        description="Seed used for generation"
    )
    
    model_used: str = Field(
        ...,
        description="Model used for generation (veo2, veo3, etc.)"
    )
    
    generation_time: float = Field(
        ...,
        description="Time taken for generation in seconds"
    )


class VideoOutput(BaseModel):
    """Output of generated video with metadata"""
    
    class VideoFile(BaseModel):
        url: str = Field(
            ...,
            description="URL to access the generated video"
        )
        
        base64: Optional[str] = Field(
            None,
            description="Optional base64 encoded video (for small videos)"
        )
        
        duration: float = Field(
            ...,
            description="Duration of generated video in seconds"
        )
        
        metadata: VideoMetadata = Field(
            ...,
            description="Video generation metadata"
        )
    
    video: VideoFile = Field(
        ...,
        description="Generated video with metadata"
    )
    
    enhanced_prompt: str = Field(
        ...,
        description="Final enhanced prompt used for generation"
    )
    
    original_prompt: str = Field(
        ...,
        description="Original user-provided prompt"
    )


class VideoGenerationStatusResponse(BaseModel):
    """Response for polling video generation status"""
    
    status: Literal["pending", "processing", "completed", "failed", "cancelled"] = Field(
        ...,
        description="Current generation status"
    )
    
    message: str = Field(
        ...,
        description="Status message or error description"
    )
    
    request_id: str = Field(
        ...,
        description="Request ID"
    )
    
    progress: Optional[int] = Field(
        None,
        description="Generation progress percentage (0-100)",
        ge=0,
        le=100
    )
    
    current_stage: Optional[str] = Field(
        None,
        description="Current stage of generation (e.g., 'queued', 'processing', 'finalizing')"
    )
    
    output: Optional[VideoOutput] = Field(
        None,
        description="Generated video output (only present when completed)"
    )


# ============================================================================
# IMAGE GENERATION SCHEMAS (for reference)
# ============================================================================

class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""
    
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Text prompt for generation"
    )
    
    use_case: Optional[Literal[
        "inspirational_scene",
        "product_imagery",
        "image_editing_add",
        "image_editing_remove",
        "image_editing_scale",
        "motion_graphics"
    ]] = None
    
    model: Optional[str] = None
    
    aspect_ratio: str = Field(
        "1:1",
        description="Aspect ratio for output"
    )
    
    enhanced_prompt: bool = Field(
        True,
        description="Whether to enhance the prompt"
    )
    
    negative_prompt: Optional[str] = Field(
        None,
        max_length=1000
    )
    
    seed: Optional[int] = Field(
        None,
        ge=0,
        le=4294967295
    )
    
    num_images: int = Field(
        1,
        ge=1,
        le=4,
        description="Number of images to generate (1-4)"
    )
    
    model_version: str = Field(
        "imagen-4.0-generate",
        description="Image model version"
    )
    
    reference_image: Optional[str] = None
    
    user_mask: Optional[str] = None
    
    image_reference_type: Literal["none", "style", "layout", "composition"] = "none"
    
    preserve_layout: bool = False
    
    reference_images: Optional[List[str]] = None


class ImageMetadata(BaseModel):
    """Image generation metadata"""
    
    seed: int
    model_used: str
    generation_time: float


class ImageOutput(BaseModel):
    """Generated image with metadata"""
    
    class Image(BaseModel):
        url: str
        base64: Optional[str] = None
        metadata: ImageMetadata
    
    images: List[Image]
    enhanced_prompt: str
    original_prompt: str


class ImageGenerationResponse(BaseModel):
    """Response for image generation"""
    
    status: Literal["pending", "processing", "completed", "failed", "cancelled"]
    message: str
    request_id: str
    output: Optional[ImageOutput] = None


# ============================================================================
# MODEL INFORMATION SCHEMAS
# ============================================================================

class VideoModelInfo(BaseModel):
    """Information about an available video model"""
    
    id: str = Field(
        ...,
        description="Model identifier (e.g., 'veo2', 'veo3')"
    )
    
    display_name: str = Field(
        ...,
        description="Human-readable model name"
    )
    
    description: str = Field(
        ...,
        description="Detailed model description"
    )
    
    supported_use_cases: List[str] = Field(
        ...,
        description="Use cases this model supports"
    )
    
    supported_aspect_ratios: List[str] = Field(
        ...,
        description="Supported aspect ratios (e.g., ['16:9', '9:16', '1:1'])"
    )
    
    max_duration: int = Field(
        ...,
        description="Maximum duration in seconds"
    )


class ImageModelInfo(BaseModel):
    """Information about an available image model"""
    
    id: str
    display_name: str
    description: str
    supported_use_cases: List[str]
    supported_aspect_ratios: List[str]
    max_resolution: str = Field(
        ...,
        description="Maximum resolution (e.g., '4096x4096')"
    )


class ModelsResponse(BaseModel):
    """Response containing available models"""
    
    image_models: List[ImageModelInfo] = Field(
        ...,
        description="Available image generation models"
    )
    
    video_models: List[VideoModelInfo] = Field(
        ...,
        description="Available video generation models"
    )


# ============================================================================
# PROMPT SUGGESTION SCHEMA
# ============================================================================

class VideoPromptSuggestionRequest(BaseModel):
    """Request model for video prompt suggestions"""
    
    reference_image: str = Field(
        ...,
        description="Base64 encoded reference image to analyze"
    )


class VideoPromptSuggestionResponse(BaseModel):
    """Response with suggested video prompt based on image"""
    
    status: Literal["completed", "failed"] = Field(
        ...,
        description="Suggestion generation status"
    )
    
    message: str = Field(
        ...,
        description="Status message"
    )
    
    request_id: str = Field(
        ...,
        description="Request ID for reference"
    )
    
    image_type: Optional[str] = Field(
        None,
        description="Detected image type (e.g., 'product_white_background', 'lifestyle_scene')"
    )
    
    suggested_prompt: Optional[str] = Field(
        None,
        description="AI-generated video prompt suggestion based on the image"
    )
    
    reasoning: Optional[str] = Field(
        None,
        description="Explanation of why this prompt was suggested"
    )


# ============================================================================
# ERROR AND HEALTH CHECK SCHEMAS
# ============================================================================

class ValidationError(BaseModel):
    """Validation error details"""
    
    loc: List[Union[str, int]] = Field(
        ...,
        description="Location of error in request"
    )
    
    msg: str = Field(
        ...,
        description="Error message"
    )
    
    type: str = Field(
        ...,
        description="Error type"
    )


class HTTPValidationError(BaseModel):
    """HTTP validation error response"""
    
    detail: List[ValidationError] = Field(
        ...,
        description="List of validation errors"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = Field(
        ...,
        description="Overall API status (e.g., 'healthy', 'degraded')"
    )
    
    version: str = Field(
        ...,
        description="API version"
    )
    
    uptime: float = Field(
        ...,
        description="API uptime in seconds"
    )
    
    models_status: Dict[str, str] = Field(
        ...,
        description="Status of each model (e.g., {'veo2': 'healthy', 'veo3': 'healthy'})"
    )


# ============================================================================
# CONVENIENCE TYPES FOR POLLING
# ============================================================================

GenerationStatus = Literal["pending", "processing", "completed", "failed", "cancelled"]


def parse_video_response(data: Dict[str, Any]) -> VideoGenerationStatusResponse:
    """Parse raw API response into VideoGenerationStatusResponse"""
    return VideoGenerationStatusResponse(**data)


def is_generation_complete(status: GenerationStatus) -> bool:
    """Check if generation has reached a terminal state"""
    return status in ["completed", "failed", "cancelled"]
