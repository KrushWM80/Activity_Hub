# Walmart GenAI Media Studio API - Complete Integration Guide

**Version**: 0.3.141  
**Base URL**: `https://retina-ds-genai-backend.prod.k8s.walmart.net`  
**OpenAPI Spec**: https://retina-ds-genai-backend.prod.k8s.walmart.net/openapi.json  
**Interactive Docs**: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs  
**Approved**: December 1, 2025 (Stephanie Tsai, PM)  

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [Core Endpoints](#core-endpoints)
4. [Request/Response Schemas](#requestresponse-schemas)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Code Examples](#code-examples)

---

## Quick Start

### Installation

```bash
# Install dependencies
pip install requests pydantic python-dotenv

# Set up authentication
echo "WALMART_SSO_TOKEN=your-sso-token" >> .env
```

### Minimal Example

```python
from src.providers.walmart_media_studio import WalmartMediaStudioProvider
from src.models.video_models import VideoPrompt

# Initialize provider
provider = WalmartMediaStudioProvider()

# Create prompt
prompt = VideoPrompt(
    id="demo_001",
    enhanced_description="Professional retail training video",
    duration=5,
    aspect_ratio="16:9"
)

# Generate video
result = provider.generate_video(prompt)
if not result.error_message:
    print(f"✅ Video ready: {result.path}")
else:
    print(f"❌ Error: {result.error_message}")
```

---

## Authentication

### Setup

1. **Obtain SSO Token**:
   - Login to: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs
   - Copy `Authorization` token from browser dev tools
   - Store in `.env` file

2. **Configure Environment**:
   ```bash
   # .env file
   WALMART_MEDIA_STUDIO_API=https://retina-ds-genai-backend.prod.k8s.walmart.net
   WALMART_SSO_TOKEN=your-sso-token-here
   ```

3. **Verify Access**:
   ```bash
   python test_walmart_api.py
   ```

### Token Format

```
Authorization: Bearer {SSO_TOKEN}
```

---

## Core Endpoints

### 1. Generate Video (Async)

**Endpoint**: `POST /api/v1/videos/generate`  
**Purpose**: Submit a video generation request for asynchronous processing  
**Response Time**: Immediate (polling required for result)  
**Typical Duration**: 30 seconds to 5 minutes

#### Request Schema

```python
{
    # Required
    "prompt": str,  # 1-2000 characters - video description
    
    # Model selection (choose one)
    "use_case": Literal[
        "inspirational_scene",
        "product_imagery",
        "image_editing_add",
        "image_editing_remove", 
        "image_editing_scale",
        "motion_graphics"
    ],  # Optional - can omit if using model parameter
    
    "model": str,  # Optional - specific model ID (takes priority)
    
    # Generation parameters
    "duration": float,  # 4-8 seconds (default: 5)
    "aspect_ratio": str,  # "16:9", "9:16", or "1:1" (default: "1:1")
    "model_version": Literal["veo2", "veo3"],  # (default: "veo2")
    
    # Enhancement options
    "enhanced_prompt": bool,  # Auto-enhance prompt (default: True)
    "negative_prompt": str,  # Max 1000 chars - what to avoid
    
    # Advanced options
    "reference_image": str,  # Base64 encoded image for style/layout
    "preserve_layout": bool,  # Use ControlNet for layout preservation
    "seed": int,  # 0-4294967295 for reproducibility
    "person_generation": Literal[
        "allow_adult",  # Include adults in generation
        "dont_allow",   # Don't generate people
        "allow_all"     # Allow all people types (default)
    ]
}
```

#### Response Schema

```python
{
    "status": "pending",  # pending|processing|completed|failed|cancelled
    "message": "Video generation request submitted",
    "request_id": "abc123-def456-ghi789",  # Use for polling
    "polling_url": "/api/v1/videos/status/abc123-def456-ghi789"
}
```

#### Python Example

```python
import requests
import json

url = "https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/videos/generate"

payload = {
    "prompt": "A Walmart associate organizing products on a retail shelf with professional lighting",
    "model_version": "veo2",
    "duration": 5,
    "aspect_ratio": "16:9",
    "enhanced_prompt": True,
    "person_generation": "allow_all"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {sso_token}"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

request_id = data["request_id"]
print(f"✅ Request submitted: {request_id}")
print(f"📍 Poll at: {data['polling_url']}")
```

---

### 2. Get Video Status

**Endpoint**: `GET /api/v1/videos/status/{request_id}`  
**Purpose**: Poll for video generation status and retrieve result  
**Response Time**: ~100ms per poll  
**Polling Interval**: 5-10 seconds recommended

#### Request Parameters

```
request_id: str  # From generation response
```

#### Response Schema

```python
{
    "status": "completed",  # pending|processing|completed|failed|cancelled
    "message": "Video generation completed",
    "request_id": "abc123-def456-ghi789",
    
    # Progress information (during processing)
    "progress": 75,  # 0-100 percentage
    "current_stage": "rendering",  # queued|processing|rendering|finalizing
    
    # Generated video (when status=completed)
    "output": {
        "video": {
            "url": "https://storage.googleapis.com/...",  # Download link
            "base64": None,  # Not provided for large videos
            "duration": 5.0,  # Actual duration
            "metadata": {
                "seed": 12345,
                "model_used": "veo2",
                "generation_time": 45.2  # Seconds
            }
        },
        "enhanced_prompt": "A professional Walmart associate...",
        "original_prompt": "A Walmart associate organizing..."
    }
}
```

#### Python Polling Example

```python
import requests
import time

request_id = "abc123-def456-ghi789"
url = f"https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/videos/status/{request_id}"

headers = {"Authorization": f"Bearer {sso_token}"}

max_wait = 300  # 5 minutes
poll_interval = 5  # 5 seconds
start = time.time()

while time.time() - start < max_wait:
    response = requests.get(url, headers=headers)
    data = response.json()
    
    status = data["status"]
    progress = data.get("progress", 0)
    
    print(f"Status: {status} ({progress}%)")
    
    if status == "completed":
        video_url = data["output"]["video"]["url"]
        print(f"✅ Video ready: {video_url}")
        break
    elif status in ["failed", "cancelled"]:
        print(f"❌ Generation {status}")
        break
    
    time.sleep(poll_interval)
```

---

### 3. Get Available Models

**Endpoint**: `GET /api/v1/models`  
**Purpose**: Retrieve available models and their capabilities  
**Response Time**: ~50ms  
**Cache**: Safe to cache for 1 hour

#### Response Schema

```python
{
    "video_models": [
        {
            "id": "veo2",
            "display_name": "Google Veo 2",
            "description": "Latest video generation model with enhanced quality",
            "supported_use_cases": [
                "inspirational_scene",
                "product_imagery",
                "motion_graphics"
            ],
            "supported_aspect_ratios": ["16:9", "9:16", "1:1"],
            "max_duration": 8  # seconds
        },
        {
            "id": "veo3",
            "display_name": "Google Veo 3",
            "description": "Next-generation Veo model (experimental)",
            "supported_use_cases": [...],
            "supported_aspect_ratios": ["16:9", "9:16", "1:1"],
            "max_duration": 8
        }
    ],
    "image_models": [
        {
            "id": "imagen-4.0-generate",
            "display_name": "Google Imagen 4.0",
            "description": "Image generation model",
            "supported_use_cases": ["product_imagery", "inspirational_scene"],
            "supported_aspect_ratios": ["1:1", "16:9", "9:16"],
            "max_resolution": "4096x4096"
        }
    ]
}
```

#### Python Example

```python
import requests

url = "https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/models"
headers = {"Authorization": f"Bearer {sso_token}"}

response = requests.get(url, headers=headers)
models = response.json()

print("Available Video Models:")
for model in models["video_models"]:
    print(f"  - {model['id']}: {model['display_name']}")
    print(f"    Duration: 0-{model['max_duration']}s")
    print(f"    Aspect ratios: {', '.join(model['supported_aspect_ratios'])}")
```

---

### 4. Suggest Video Prompt

**Endpoint**: `POST /api/v1/videos/suggest-prompt`  
**Purpose**: Analyze image and suggest appropriate video prompt  
**Uses**: Google Gemini 2.0 Flash  
**Features**:
- Detects product on white background vs lifestyle scene
- Suggests 360-degree spin for products
- Suggests animation scenarios for lifestyle images

#### Request Schema

```python
{
    "reference_image": str  # Base64 encoded image
}
```

#### Response Schema

```python
{
    "status": "completed",
    "message": "Prompt suggestion generated",
    "request_id": "xyz789-abc123",
    
    "image_type": "product_white_background",  # or "lifestyle_scene"
    "suggested_prompt": "A professional 360-degree spin of a Walmart...",
    "reasoning": "Image shows product on white background, ideal for rotation animation"
}
```

#### Python Example

```python
import requests
import base64

url = "https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/videos/suggest-prompt"

# Encode image to base64
with open("product.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

payload = {"reference_image": image_base64}
headers = {"Authorization": f"Bearer {sso_token}"}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

print(f"Image Type: {data['image_type']}")
print(f"Suggested Prompt: {data['suggested_prompt']}")
print(f"Reasoning: {data['reasoning']}")

# Use suggested prompt for video generation
video_payload = {
    "prompt": data['suggested_prompt'],
    "model_version": "veo2",
    "duration": 5,
    "aspect_ratio": "16:9"
}
```

---

### 5. Cancel Video Generation

**Endpoint**: `DELETE /api/v1/videos/{request_id}`  
**Purpose**: Cancel an in-progress video generation  
**Status Code**: 200 (success)  
**Response**: Simple string message

#### Python Example

```python
import requests

request_id = "abc123-def456-ghi789"
url = f"https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/videos/{request_id}"
headers = {"Authorization": f"Bearer {sso_token}"}

response = requests.delete(url, headers=headers)

if response.status_code == 200:
    print(f"✅ Video generation cancelled: {request_id}")
else:
    print(f"❌ Failed to cancel: {response.status_code}")
```

---

### 6. Generate Image (Synchronous)

**Endpoint**: `POST /api/v1/images/generate`  
**Purpose**: Generate images synchronously (returns immediately)  
**Response Time**: 10-30 seconds  
**Note**: Blocks until completion (not recommended for production)

#### Request Schema

```python
{
    # Same as video generation
    "prompt": str,  # 1-2000 characters
    "use_case": Literal[...],
    "model": str,
    "aspect_ratio": str,  # "1:1", "16:9", "9:16"
    
    # Image-specific
    "num_images": int,  # 1-4 (default: 1)
    "model_version": str,  # "imagen-4.0-generate"
    
    # Optional
    "enhanced_prompt": bool,
    "negative_prompt": str,
    "seed": int,
    "reference_image": str,
    "user_mask": str,  # For image editing
    "preserve_layout": bool
}
```

#### Response Schema

```python
{
    "status": "completed",
    "message": "Image generation completed",
    "request_id": "img-abc123",
    
    "output": {
        "images": [
            {
                "url": "https://storage.googleapis.com/...",
                "base64": None,
                "metadata": {
                    "seed": 12345,
                    "model_used": "imagen-4.0",
                    "generation_time": 18.5
                }
            }
        ],
        "enhanced_prompt": "A professional retail product...",
        "original_prompt": "A product on shelf"
    }
}
```

---

### 7. Health Check

**Endpoint**: `GET /health`  (Note: No `/api/v1/` prefix)  
**Purpose**: Verify API health and model status  
**Response Time**: ~10ms  
**Use**: Monitoring and diagnostics

#### Response Schema

```python
{
    "status": "healthy",  # healthy|degraded|unhealthy
    "version": "0.3.141",
    "uptime": 3600.5,  # seconds
    "models_status": {
        "veo2": "healthy",
        "veo3": "healthy",
        "imagen-4.0-generate": "healthy"
    }
}
```

#### Python Example

```python
import requests

url = "https://retina-ds-genai-backend.prod.k8s.walmart.net/health"

try:
    response = requests.get(url, timeout=5)
    data = response.json()
    
    print(f"API Status: {data['status']}")
    print(f"Version: {data['version']}")
    print(f"Uptime: {data['uptime']} seconds")
    
    for model, status in data['models_status'].items():
        print(f"  {model}: {status}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ API not accessible: {e}")
```

---

## Request/Response Schemas

### VideoGenerationRequest

All parameters are validated by this schema. Violations result in HTTP 422 errors.

```python
from src.schemas.walmart_schemas import VideoGenerationRequest

# Valid
request = VideoGenerationRequest(
    prompt="Retail shelf organization training",
    model_version="veo2",
    duration=5,
    aspect_ratio="16:9"
)

# Invalid - prompt too short (min 1 char, but empty is invalid)
try:
    VideoGenerationRequest(prompt="")
except Exception as e:
    print(f"Validation error: {e}")

# Invalid - duration out of range
try:
    VideoGenerationRequest(prompt="Valid", duration=10)  # Max 8
except Exception as e:
    print(f"Validation error: {e}")
```

### Validation Rules

| Field | Min | Max | Default | Notes |
|-------|-----|-----|---------|-------|
| `prompt` | 1 char | 2000 chars | - | Required |
| `duration` | 4 sec | 8 sec | 5 | Must be within range |
| `aspect_ratio` | - | - | "1:1" | Must be "16:9", "9:16", or "1:1" |
| `negative_prompt` | - | 1000 chars | - | Optional |
| `num_images` | 1 | 4 | 1 | Image generation only |
| `seed` | 0 | 4294967295 | - | Optional, for reproducibility |

---

## Error Handling

### HTTP Status Codes

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | Success | Request submitted or result ready |
| 401 | Unauthorized | Invalid or expired SSO token |
| 403 | Forbidden | API access not granted |
| 404 | Not Found | Invalid request_id for polling |
| 422 | Validation Error | Prompt too long, duration out of range |
| 429 | Rate Limited | Too many requests |
| 500+ | Server Error | Backend issue |

### Common Errors

#### 401 Unauthorized

```python
{
    "detail": "Invalid authentication credentials"
}
```

**Solution**: Verify SSO token in .env

```bash
# Update .env
WALMART_SSO_TOKEN=your-new-token
```

#### 422 Validation Error

```python
{
    "detail": [
        {
            "loc": ["body", "prompt"],
            "msg": "String should have at most 2000 characters",
            "type": "string_too_long"
        }
    ]
}
```

**Solution**: Check request parameters

```python
# Wrong
VideoGenerationRequest(prompt="x" * 2001)  # Too long

# Right
VideoGenerationRequest(prompt="x" * 2000)  # Exactly at limit
```

#### 404 Not Found

```python
{
    "detail": "Request not found"
}
```

**Solution**: Verify request_id is correct

```python
# Check if request_id exists
print(f"Looking for: {request_id}")

# Verify format (typically UUID-like)
import uuid
uuid.UUID(request_id)  # Should not raise
```

#### 429 Rate Limited

```python
{
    "detail": "Rate limit exceeded. Try again later."
}
```

**Solution**: Implement exponential backoff

```python
import time

def poll_with_backoff(request_id, max_wait=300):
    start = time.time()
    backoff = 1  # Start with 1 second
    
    while time.time() - start < max_wait:
        try:
            response = requests.get(f"/api/v1/videos/status/{request_id}")
            
            if response.status_code == 429:
                print(f"Rate limited. Waiting {backoff}s...")
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)  # Max 60 seconds
                continue
            
            return response.json()
        
        except Exception as e:
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
```

---

## Best Practices

### 1. **Polling Strategy**

✅ **DO**: Implement exponential backoff

```python
import time

def smart_poll(request_id):
    backoff = 5  # Start: 5 seconds
    attempts = 0
    max_attempts = 60
    
    while attempts < max_attempts:
        response = requests.get(f".../status/{request_id}")
        data = response.json()
        
        if data["status"] == "completed":
            return data
        elif data["status"] in ["failed", "cancelled"]:
            raise Exception(f"Generation failed: {data['message']}")
        
        print(f"Polling... ({attempts+1}/{max_attempts}) - Next check in {backoff}s")
        time.sleep(backoff)
        backoff = min(backoff * 1.5, 30)  # Exponential, max 30s
        attempts += 1
    
    raise TimeoutError("Generation timed out")
```

❌ **DON'T**: Poll too frequently

```python
# Bad - overwhelming the API
while True:
    check_status()  # Called thousands of times per minute
```

### 2. **Prompt Engineering**

✅ **DO**: Be specific and detailed

```python
good_prompt = """
Professional training video showing a Walmart associate 
organizing merchandise on a retail shelf. The associate 
is wearing a Walmart uniform, the shelf is well-lit with 
natural and store lighting, shelves are organized with 
products clearly visible. Modern retail environment.
"""
```

❌ **DON'T**: Use vague prompts

```python
bad_prompt = "organize shelf"  # Too vague
```

### 3. **Aspect Ratio Selection**

| Use Case | Ratio | Why |
|----------|-------|-----|
| Training videos | 16:9 | Standard widescreen, TV/monitor native |
| Mobile content | 9:16 | Vertical, optimized for phones |
| Square graphics | 1:1 | Social media, thumbnails |

### 4. **Duration Selection**

- **4 seconds**: Short clips, product highlights
- **5 seconds**: Standard training snippets
- **8 seconds**: Complex procedures, full demonstrations

### 5. **Caching & Optimization**

```python
# Cache model list (valid for 1 hour)
import json
from pathlib import Path

MODELS_CACHE = Path("models_cache.json")

def get_models(use_cache=True):
    if use_cache and MODELS_CACHE.exists():
        with open(MODELS_CACHE) as f:
            return json.load(f)
    
    response = requests.get(".../models")
    models = response.json()
    
    # Save for later
    with open(MODELS_CACHE, "w") as f:
        json.dump(models, f)
    
    return models
```

---

## Code Examples

### Complete Workflow Example

```python
import requests
import time
import base64
from pathlib import Path

class WalmartMediaStudioClient:
    def __init__(self, sso_token: str):
        self.base_url = "https://retina-ds-genai-backend.prod.k8s.walmart.net"
        self.token = sso_token
        self.headers = {
            "Authorization": f"Bearer {sso_token}",
            "Content-Type": "application/json"
        }
    
    def health_check(self):
        """Verify API is accessible"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_models(self):
        """Get available models"""
        response = requests.get(
            f"{self.base_url}/api/v1/models",
            headers=self.headers
        )
        return response.json()
    
    def suggest_prompt(self, image_path: str):
        """Get AI-suggested prompt for image"""
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        response = requests.post(
            f"{self.base_url}/api/v1/videos/suggest-prompt",
            json={"reference_image": image_base64},
            headers=self.headers
        )
        return response.json()
    
    def generate_video(self, prompt: str, **kwargs):
        """Submit video generation request"""
        payload = {
            "prompt": prompt,
            "model_version": kwargs.get("model_version", "veo2"),
            "duration": kwargs.get("duration", 5),
            "aspect_ratio": kwargs.get("aspect_ratio", "16:9"),
            "enhanced_prompt": kwargs.get("enhanced_prompt", True),
            "person_generation": kwargs.get("person_generation", "allow_all")
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/videos/generate",
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    def poll_status(self, request_id: str, timeout: int = 300):
        """Poll until generation completes"""
        start = time.time()
        backoff = 5
        
        while time.time() - start < timeout:
            response = requests.get(
                f"{self.base_url}/api/v1/videos/status/{request_id}",
                headers=self.headers
            )
            data = response.json()
            
            status = data["status"]
            progress = data.get("progress", 0)
            
            print(f"Status: {status} ({progress}%)")
            
            if status == "completed":
                return data
            elif status in ["failed", "cancelled"]:
                raise Exception(f"Generation {status}: {data['message']}")
            
            time.sleep(backoff)
            backoff = min(backoff * 1.5, 30)
        
        raise TimeoutError(f"Generation timed out after {timeout}s")
    
    def download_video(self, video_url: str, output_path: str):
        """Download generated video"""
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return Path(output_path).stat().st_size

# Usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    client = WalmartMediaStudioClient(os.getenv("WALMART_SSO_TOKEN"))
    
    # Check health
    health = client.health_check()
    print(f"✅ API Health: {health['status']}")
    
    # Get available models
    models = client.get_models()
    print(f"📦 Available models: {len(models['video_models'])} video, {len(models['image_models'])} image")
    
    # Generate video
    request = client.generate_video(
        prompt="Professional Walmart associate demonstrating inventory management",
        duration=5,
        aspect_ratio="16:9"
    )
    request_id = request["request_id"]
    print(f"🎬 Generation started: {request_id}")
    
    # Poll for completion
    result = client.poll_status(request_id)
    video_url = result["output"]["video"]["url"]
    print(f"✅ Generation complete: {video_url}")
    
    # Download
    size = client.download_video(video_url, "output.mp4")
    print(f"💾 Downloaded: {size / 1024 / 1024:.2f}MB")
```

---

## Support

- **Slack**: #help-genai-media-studio
- **Docs**: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs
- **OpenAPI**: https://retina-ds-genai-backend.prod.k8s.walmart.net/openapi.json
- **Issues**: Contact Next Gen Content DS team

---

## Changelog

**v0.3.141** (December 1, 2025)
- ✅ Initial production release
- ✅ Video generation (veo2, veo3)
- ✅ Image generation (imagen-4.0)
- ✅ Prompt suggestions
- ✅ Health monitoring
- ✅ SSO authentication
