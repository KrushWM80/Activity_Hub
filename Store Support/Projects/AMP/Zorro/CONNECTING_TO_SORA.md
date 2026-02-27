# Connecting Zorro to Sora & Equivalent Products

## Overview

This guide explains the exact steps needed to integrate Zorro with OpenAI Sora or equivalent text-to-video AI products (Runway Gen-3, Stability AI, Google Veo, etc.).

**Current Status:** Zorro is architecturally ready to support any text-to-video provider. Adding a new provider takes ~2-4 hours of development work.

---

## 🎯 Quick Answer: What's Needed?

### For OpenAI Sora

**Prerequisites:**
1. ✅ Sora API access (currently waitlist/limited availability)
2. ✅ OpenAI API key with Sora enabled
3. ✅ API documentation (request/response schemas)
4. ✅ 2-4 hours of development time

**Steps:**
1. Get API access from OpenAI
2. Create `SoraVideoProvider` class (extends `BaseVideoProvider`)
3. Add configuration to `config.yaml`
4. Test with sample prompts
5. Deploy

**Timeline:** 1 day (assuming immediate API access)

---

## 📋 Detailed Steps: Sora Integration

### Step 1: Obtain Sora API Access (1-7 days)

#### Option A: Direct from OpenAI
```
1. Visit: https://openai.com/sora
2. Join waitlist or apply for API access
3. Provide use case: "Enterprise video generation for Walmart associate communications"
4. Wait for approval (varies: 1 day to several weeks)
5. Receive API key with Sora enabled
```

**Current Status (Nov 2025):** 
- Sora API is in limited beta
- Available to select enterprise customers
- May require OpenAI sales contact
- Pricing not yet publicly released

#### Option B: Through Enterprise Agreement
```
1. Contact Walmart's OpenAI account manager
2. Request Sora API access as part of enterprise agreement
3. Negotiate pricing and SLA
4. Receive dedicated API endpoint
5. Get production support commitment
```

**Advantages:**
- ✅ Better pricing (volume discounts)
- ✅ Dedicated support
- ✅ SLA guarantees
- ✅ Faster approval

### Step 2: Get API Documentation (1 hour)

Once you have access, obtain:

#### Required Documentation
- [ ] API endpoint URL(s)
- [ ] Authentication method (API key, OAuth, etc.)
- [ ] Request schema (parameters, formats)
- [ ] Response schema (status codes, data structures)
- [ ] Rate limits and quotas
- [ ] Error codes and handling
- [ ] Webhook support (for async generation)

#### Example Request/Response (Hypothetical)
```python
# Expected Sora API format (not official - for illustration)
POST https://api.openai.com/v1/sora/generate

Headers:
  Authorization: Bearer sk-...
  Content-Type: application/json

Request Body:
{
  "prompt": "A professional training scene in a Walmart store...",
  "duration": 10,
  "resolution": "1920x1080",
  "fps": 24,
  "aspect_ratio": "16:9",
  "style": "photorealistic"
}

Response:
{
  "id": "sora_abc123",
  "status": "processing",
  "estimated_time": 120,
  "webhook_url": "https://your-app.com/webhook"
}

# Poll for completion
GET https://api.openai.com/v1/sora/generate/sora_abc123

Response (when complete):
{
  "id": "sora_abc123",
  "status": "completed",
  "video_url": "https://cdn.openai.com/videos/abc123.mp4",
  "duration": 10.2,
  "metadata": {
    "resolution": "1920x1080",
    "fps": 24,
    "file_size": 15728640
  }
}
```

### Step 3: Create Sora Provider Class (2-3 hours)

Create `src/providers/sora_provider.py`:

```python
"""
OpenAI Sora Video Provider

Integrates Zorro with OpenAI's Sora text-to-video AI model.
"""

import logging
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.models.video_models import GeneratedVideo, VideoPrompt
from src.providers.base_provider import BaseVideoProvider

logger = logging.getLogger(__name__)


class SoraVideoProvider(BaseVideoProvider):
    """
    Video generation provider using OpenAI Sora.
    
    Requires:
    - OPENAI_API_KEY environment variable
    - Sora API access enabled on your account
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_endpoint: str = "https://api.openai.com/v1/sora",
        timeout: int = 300,
        max_retries: int = 3
    ):
        """
        Initialize Sora provider.
        
        Args:
            api_key: OpenAI API key (default: from OPENAI_API_KEY env var)
            api_endpoint: Sora API endpoint
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        super().__init__()
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.api_endpoint = api_endpoint
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Session with retry logic
        self.session = self._create_session()
        
        logger.info(f"Initialized Sora provider: {self.api_endpoint}")
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic."""
        session = requests.Session()
        
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
        """Get request headers with authentication."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Zorro-VideoGen/1.0"
        }
    
    def generate_video(self, prompt: VideoPrompt) -> GeneratedVideo:
        """
        Generate video using OpenAI Sora.
        
        Args:
            prompt: Video prompt with description and parameters
            
        Returns:
            GeneratedVideo with path, metadata, or error
        """
        try:
            logger.info(f"Generating video via Sora: {prompt.id}")
            
            # Prepare request
            payload = {
                "prompt": prompt.enhanced_description,
                "duration": prompt.duration or 10,
                "resolution": f"{prompt.width}x{prompt.height}" if prompt.width else "1920x1080",
                "fps": prompt.fps or 24,
                "aspect_ratio": prompt.aspect_ratio or "16:9",
                "style": prompt.style or "photorealistic"
            }
            
            # Submit generation request
            response = self.session.post(
                f"{self.api_endpoint}/generate",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            job_id = data.get("id")
            if not job_id:
                return self._create_failed_video(prompt, "No job ID returned from Sora API")
            
            logger.info(f"Sora job submitted: {job_id}")
            
            # Poll for completion
            video_url = self._poll_for_completion(job_id)
            
            if not video_url:
                return self._create_failed_video(prompt, "Video generation timed out")
            
            # Download video
            video_path = self._download_video(video_url, prompt.id)
            
            if not video_path:
                return self._create_failed_video(prompt, "Failed to download video")
            
            # Create success result
            return GeneratedVideo(
                id=prompt.id,
                path=str(video_path),
                prompt=prompt.enhanced_description,
                duration=data.get("duration", 10.0),
                resolution=data.get("metadata", {}).get("resolution", "1920x1080"),
                model_used="openai-sora",
                generation_time=data.get("generation_time", 0.0),
                file_size=video_path.stat().st_size if video_path.exists() else 0,
                metadata={
                    "provider": "openai_sora",
                    "job_id": job_id,
                    "api_version": "v1",
                    "model": "sora"
                }
            )
            
        except Exception as e:
            logger.error(f"Sora generation failed: {e}", exc_info=True)
            return self._create_failed_video(prompt, str(e))
    
    def _poll_for_completion(self, job_id: str, poll_interval: int = 5) -> Optional[str]:
        """Poll for video generation completion."""
        start_time = time.time()
        
        while time.time() - start_time < self.timeout:
            try:
                response = self.session.get(
                    f"{self.api_endpoint}/generate/{job_id}",
                    headers=self._get_headers(),
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                status = data.get("status")
                
                if status == "completed":
                    return data.get("video_url")
                elif status in ["failed", "error"]:
                    logger.error(f"Sora job failed: {data.get('error')}")
                    return None
                
                # Still processing
                time.sleep(poll_interval)
                
            except Exception as e:
                logger.error(f"Polling error: {e}")
                time.sleep(poll_interval)
        
        return None
    
    def _download_video(self, video_url: str, video_id: str) -> Optional[Path]:
        """Download generated video."""
        try:
            output_dir = Path("output/videos")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{video_id}_sora.mp4"
            
            response = self.session.get(video_url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Video downloaded: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return None
    
    def _create_failed_video(self, prompt: VideoPrompt, error_message: str) -> GeneratedVideo:
        """Create failed video result."""
        return GeneratedVideo(
            id=prompt.id,
            path=f"output/videos/{prompt.id}_failed.mp4",
            prompt=prompt.enhanced_description,
            duration=0.0,
            resolution="0x0",
            model_used="openai-sora",
            generation_time=0.0,
            file_size=0,
            error_message=error_message,
            metadata={"provider": "openai_sora", "error": error_message}
        )
    
    def is_available(self) -> bool:
        """Check if Sora API is available."""
        try:
            response = self.session.get(
                f"{self.api_endpoint}/health",
                headers=self._get_headers(),
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
```

### Step 4: Register Provider (5 minutes)

Update `src/core/video_generator.py`:

```python
def _create_provider(self, provider_name: str) -> BaseVideoGenerator:
    """Create video generation provider instance."""
    
    if provider_name.lower() == "modelscope":
        from ..services.modelscope_service import ModelScopeVideoGenerator
        return ModelScopeVideoGenerator()
    
    elif provider_name.lower() == "stability":
        from ..services.stability_service import StabilityVideoGenerator
        return StabilityVideoGenerator()
    
    elif provider_name.lower() == "runwayml":
        from ..services.runwayml_service import RunwayMLVideoGenerator
        return RunwayMLVideoGenerator()
    
    elif provider_name.lower() in ["walmart_media_studio", "media_studio"]:
        from ..providers.walmart_media_studio import WalmartMediaStudioProvider
        return WalmartMediaStudioProvider()
    
    # ADD THIS:
    elif provider_name.lower() in ["sora", "openai_sora", "openai"]:
        from ..providers.sora_provider import SoraVideoProvider
        return SoraVideoProvider()
    
    else:
        raise ModelLoadError(f"Unknown provider: {provider_name}")
```

### Step 5: Add Configuration (5 minutes)

Update `config/config.yaml`:

```yaml
video:
  generator:
    provider: "sora"  # Change to use Sora
    
    # Sora-specific settings
    sora:
      api_endpoint: "https://api.openai.com/v1/sora"
      timeout: 300
      max_retries: 3
      poll_interval: 5
      default_style: "photorealistic"
```

Update `.env`:

```bash
# OpenAI Sora
OPENAI_API_KEY=sk-your-actual-key-here
SORA_API_ENDPOINT=https://api.openai.com/v1/sora
```

### Step 6: Update GUI (5 minutes)

Update `app.py` to include Sora in provider dropdown:

```python
provider = st.selectbox(
    "Video Provider",
    ["sora", "walmart_media_studio", "modelscope", "stability", "runwayml"],
    help="Select the AI video generation provider"
)

# Show provider info
if provider == "sora":
    st.success("✅ **OpenAI Sora** - Best-in-class video quality")
    st.caption("🔗 Requires API access | 💵 ~$0.20-0.40/video")
elif provider == "walmart_media_studio":
    st.info("✅ **Walmart Media Studio** - Pre-approved, internal")
```

### Step 7: Test Integration (30 minutes)

```python
# Test script: test_sora.py
from src.providers.sora_provider import SoraVideoProvider
from src.models.video_models import VideoPrompt

# Create test prompt
prompt = VideoPrompt(
    id="test_sora_001",
    enhanced_description="A professional training scene in a modern Walmart store",
    duration=10,
    fps=24,
    aspect_ratio="16:9"
)

# Test provider
provider = SoraVideoProvider()

# Check availability
if not provider.is_available():
    print("❌ Sora API not available")
    exit(1)

print("✅ Sora API available")

# Generate test video
print("🎬 Generating video...")
result = provider.generate_video(prompt)

if result.error_message:
    print(f"❌ Generation failed: {result.error_message}")
else:
    print(f"✅ Video generated: {result.path}")
    print(f"   Duration: {result.duration}s")
    print(f"   Size: {result.file_size / 1024 / 1024:.2f}MB")
```

Run test:
```bash
python test_sora.py
```

### Step 8: Deploy (1 hour)

```bash
# 1. Update dependencies
pip install openai>=1.0.0  # If using official SDK

# 2. Run full test suite
pytest tests/

# 3. Update documentation
# Add Sora to README.md, provider docs

# 4. Deploy to production
# Follow your deployment process
```

---

## 🔄 Steps for Alternative Products

The process is similar for any text-to-video AI. Here's the breakdown for major alternatives:

### Runway Gen-3 Alpha

**Steps:**
1. Get API access: https://runwayml.com/research/gen-3-alpha
2. Create `RunwayGen3Provider` class
3. API endpoint: `https://api.runwayml.com/v1/gen3`
4. Authentication: API key
5. Development time: 2-4 hours

**Current Status:** Gen-3 API in limited beta

### Stability AI (Video)

**Steps:**
1. Get API access: https://platform.stability.ai/
2. Create `StabilityVideoProvider` class
3. API endpoint: `https://api.stability.ai/v2alpha/generation/video`
4. Authentication: API key
5. Development time: 2-4 hours

**Current Status:** Video API in early access

### Google Veo (via Walmart Media Studio)

**Status:** ✅ Already implemented!
- File: `src/providers/walmart_media_studio.py`
- Just need API access from Next Gen Content DS team

### Pika Labs

**Steps:**
1. Get API access: https://pika.art/
2. Create `PikaVideoProvider` class
3. API endpoint: TBD (API not yet public)
4. Development time: 2-4 hours

**Current Status:** API not yet available

### Luma AI (Dream Machine)

**Steps:**
1. Get API access: https://lumalabs.ai/
2. Create `LumaVideoProvider` class
3. API endpoint: TBD (API not yet public)
4. Development time: 2-4 hours

**Current Status:** API waitlist

---

## 📊 Provider Comparison Matrix

| Provider | API Available | Approval Time | Cost/Video | Quality | Integration Time |
|----------|--------------|---------------|------------|---------|------------------|
| **OpenAI Sora** | ⏳ Limited Beta | 1-4 weeks | ~$0.30 | ⭐⭐⭐⭐⭐ | 2-4 hours |
| **Walmart Media Studio (Veo)** | ⏳ Requested | 1-3 days | Internal | ⭐⭐⭐⭐⭐ | ✅ Done |
| **Runway Gen-3** | ⏳ Limited Beta | 1-2 weeks | ~$0.25 | ⭐⭐⭐⭐ | 2-4 hours |
| **Stability AI Video** | ✅ Yes | Instant | ~$0.20 | ⭐⭐⭐⭐ | 2-4 hours |
| **ModelScope** | ✅ Yes | Instant | Free | ⭐⭐⭐ | ✅ Done |
| **Pika Labs** | ❌ No | TBD | TBD | ⭐⭐⭐⭐ | 2-4 hours |
| **Luma Dream Machine** | ❌ No | TBD | TBD | ⭐⭐⭐⭐ | 2-4 hours |

---

## 🎯 Recommended Approach

### Phase 1: Use What's Available Now (This Week)

```
Priority 1: Walmart Media Studio (Google Veo)
✅ Already implemented
⏳ Just needs API access approval
✅ Pre-approved by Walmart
✅ No cost concerns
✅ Best quality (Veo ≈ Sora)

Action: Continue pursuing API access via #help-genai-media-studio
```

### Phase 2: Add Commercial Backup (Next Month)

```
Priority 2: Stability AI Video
✅ API available now
✅ Instant signup
✅ Reasonable pricing (~$0.20/video)
✅ Good quality

Action: Sign up and integrate as fallback provider
Timeline: 1 day to integrate
```

### Phase 3: Add Premium Option (When Available)

```
Priority 3: OpenAI Sora
⏳ Wait for API availability
⏳ Apply for enterprise access
✅ Best quality available
⚠️ Higher cost

Action: Monitor Sora API release, apply when available
Timeline: 2-4 hours to integrate once API is released
```

---

## 🚀 Quick Start: Adding Any Provider

**Generic Template** (copy this for any new provider):

```python
# src/providers/{provider_name}_provider.py

from src.providers.base_provider import BaseVideoProvider
from src.models.video_models import GeneratedVideo, VideoPrompt

class {ProviderName}Provider(BaseVideoProvider):
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("{PROVIDER}_API_KEY")
        self.api_endpoint = "https://api.{provider}.com/v1/video"
    
    def generate_video(self, prompt: VideoPrompt) -> GeneratedVideo:
        # 1. Prepare request
        payload = {
            "prompt": prompt.enhanced_description,
            "duration": prompt.duration
        }
        
        # 2. Submit to API
        response = requests.post(
            f"{self.api_endpoint}/generate",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        # 3. Poll for completion
        job_id = response.json()["id"]
        video_url = self._poll(job_id)
        
        # 4. Download video
        video_path = self._download(video_url, prompt.id)
        
        # 5. Return result
        return GeneratedVideo(
            id=prompt.id,
            path=str(video_path),
            model_used="{provider}",
            # ... other fields
        )
```

**Total time to add new provider: 2-4 hours**

---

## ⚡ Fastest Path to Production

### Option 1: Walmart Media Studio (Recommended)
```
Today:     Post in #help-genai-media-studio
Day 2-3:   Receive API docs
Day 3:     Test integration
Day 4:     Deploy to pilot
Week 2:    Production rollout

Total: 1-2 weeks
```

### Option 2: Stability AI (Backup)
```
Today:     Sign up at platform.stability.ai
Hour 2:    Create provider class
Hour 3:    Test integration
Hour 4:    Deploy

Total: 4 hours
```

### Option 3: Wait for Sora (Premium)
```
Today:     Apply for Sora API access
Week 2-4:  Receive approval
Day 1:     Integrate provider
Day 2:     Deploy

Total: 2-4 weeks + 1 day
```

---

## 📝 Checklist: Integrating Any Provider

- [ ] **Get API Access**
  - [ ] Sign up / apply for access
  - [ ] Receive API key
  - [ ] Confirm quota/limits

- [ ] **Read Documentation**
  - [ ] API endpoint URLs
  - [ ] Authentication method
  - [ ] Request/response formats
  - [ ] Rate limits
  - [ ] Error codes

- [ ] **Create Provider Class**
  - [ ] Extend `BaseVideoProvider`
  - [ ] Implement `generate_video()`
  - [ ] Add error handling
  - [ ] Add retry logic
  - [ ] Add polling for async jobs

- [ ] **Add Configuration**
  - [ ] Update `config.yaml`
  - [ ] Add environment variables
  - [ ] Register in video generator

- [ ] **Test Integration**
  - [ ] Unit tests
  - [ ] Integration tests
  - [ ] Load testing
  - [ ] Error scenarios

- [ ] **Update GUI**
  - [ ] Add to provider dropdown
  - [ ] Add status indicators
  - [ ] Update documentation

- [ ] **Deploy**
  - [ ] Update dependencies
  - [ ] Run full test suite
  - [ ] Deploy to staging
  - [ ] Deploy to production

---

## 💡 Key Insights

### 1. Zorro is Provider-Agnostic
- Can use **any** text-to-video API
- Switching providers takes minutes (change config)
- Can use **multiple** providers simultaneously

### 2. Adding Providers is Fast
- 2-4 hours development time
- Most time spent on API approval, not coding
- Template code makes it straightforward

### 3. Best Strategy: Multiple Providers
```yaml
# config.yaml
providers:
  primary: "walmart_media_studio"    # Best for Walmart
  fallback: "stability_ai"           # If primary fails
  premium: "sora"                    # For high-priority videos
  free: "modelscope"                 # For testing
```

### 4. Cost Optimization
- Use free providers for testing (ModelScope)
- Use internal provider for production (Media Studio)
- Use premium for executive/critical videos (Sora)
- Batch similar requests to same provider

---

## 🎬 Next Steps

### Immediate (This Week)
1. ✅ Walmart Media Studio already implemented
2. ⏳ Continue pursuing API access
3. ⏳ Manual testing via web UI

### Short-term (Next Month)
1. Add Stability AI as backup provider (4 hours)
2. Test with both providers
3. Compare quality and cost

### Long-term (Q1 2026)
1. Add Sora when API available
2. Add other providers as APIs launch
3. Implement smart provider selection (cost vs. quality)

---

**Bottom Line:** Zorro can connect to Sora (or any equivalent) in 2-4 hours once API access is granted. The architecture is already built for this. We're just waiting on API availability! 🚀
