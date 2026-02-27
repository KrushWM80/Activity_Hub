# Official Sora 2 API Integration Guide

## 🎉 Sora 2 is Now Available!

**Status:** ✅ Official API Released  
**Documentation:** https://platform.openai.com/docs/guides/video  
**Integration Time:** 2-4 hours  
**Implementation:** ✅ Complete - `src/providers/sora_provider.py`

---

## 📋 Quick Reference

### Models Available

| Model | Speed | Quality | Best For | Cost |
|-------|-------|---------|----------|------|
| **sora-2** | ⚡ Fast | Good | Rapid iteration, social media, prototypes | Lower |
| **sora-2-pro** | 🐌 Slower | Excellent | Production, marketing, high-res cinematic | Higher |

### API Endpoints

```
Base URL: https://api.openai.com/v1/videos

POST   /videos                    - Create video (returns job)
GET    /videos/{video_id}         - Get job status & progress
GET    /videos/{video_id}/content - Download MP4 (when completed)
GET    /videos                    - List all videos
DELETE /videos/{video_id}         - Delete video
POST   /videos/{video_id}/remix   - Remix existing video
```

### Authentication

```bash
# Set your API key
export OPENAI_API_KEY="sk-your-key-here"

# All requests use Bearer token
Authorization: Bearer $OPENAI_API_KEY
```

---

## 🚀 Integration Steps

### Step 1: Get API Access

1. Visit: https://platform.openai.com/
2. Sign in with OpenAI account
3. Navigate to API keys
4. Create new API key with Sora access
5. Save key securely

**Enterprise Access:**
- Contact Walmart's OpenAI account manager
- Request Sora API access
- Negotiate volume pricing
- Get dedicated support

### Step 2: Install Dependencies

```bash
# Option 1: Use official OpenAI SDK (recommended)
pip install openai>=1.60.0

# Option 2: Use requests library (what we've implemented)
pip install requests>=2.31.0
```

### Step 3: Configure Zorro

#### Update `.env`:
```bash
# Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-key-here

# Optional: Specify model preference
SORA_MODEL=sora-2-pro  # or sora-2
```

#### Update `config/config.yaml`:
```yaml
video:
  generator:
    provider: "sora"  # Use Sora as primary provider
    
    # Sora-specific settings
    sora:
      model: "sora-2-pro"  # or "sora-2"
      api_endpoint: "https://api.openai.com/v1/videos"
      timeout: 600  # 10 minutes max wait
      poll_interval: 10  # Check status every 10 seconds
      max_retries: 3
```

### Step 4: Register Provider

The provider is already implemented! Just register it in `src/core/video_generator.py`:

```python
def _create_provider(self, provider_name: str) -> BaseVideoGenerator:
    # ... existing providers ...
    
    elif provider_name.lower() in ["sora", "openai_sora", "openai"]:
        from ..providers.sora_provider import SoraVideoProvider
        return SoraVideoProvider()
    
    else:
        raise ModelLoadError(f"Unknown provider: {provider_name}")
```

### Step 5: Update GUI

Update `app.py` to include Sora in provider selection:

```python
# Provider selection
provider = st.selectbox(
    "Video Provider",
    ["sora", "walmart_media_studio", "modelscope"],
    help="Select the AI video generation provider"
)

# Show provider info
if provider == "sora":
    st.success("✅ **OpenAI Sora 2** - Best-in-class video quality")
    
    # Model selection
    model = st.radio(
        "Sora Model",
        ["sora-2", "sora-2-pro"],
        help="sora-2: Fast, good quality | sora-2-pro: Slower, excellent quality"
    )
    
    if model == "sora-2":
        st.info("⚡ Fast generation - Ideal for iteration and social media")
    else:
        st.info("🎬 High quality - Ideal for production and marketing")
```

### Step 6: Test Integration

```python
# test_sora_integration.py
from src.providers.sora_provider import SoraVideoProvider
from src.models.video_models import VideoPrompt

def test_sora():
    # Create provider
    provider = SoraVideoProvider(model="sora-2")
    
    # Check availability
    if not provider.is_available():
        print("❌ Sora API not available")
        return
    
    print("✅ Sora API available")
    print(f"Model: {provider.model}")
    
    # Create test prompt
    prompt = VideoPrompt(
        id="test_sora_001",
        enhanced_description="A professional training scene in a modern Walmart store, "
                           "associates engaged with digital tablets, bright lighting, "
                           "clean aisles, encouraging atmosphere",
        duration=10,
        width=1920,
        height=1080
    )
    
    # Generate video
    print(f"\n🎬 Generating video with {provider.model}...")
    result = provider.generate_video(prompt)
    
    if result.error_message:
        print(f"❌ Generation failed: {result.error_message}")
    else:
        print(f"✅ Video generated successfully!")
        print(f"   Path: {result.path}")
        print(f"   Duration: {result.duration}s")
        print(f"   Size: {result.file_size / 1024 / 1024:.2f}MB")
        print(f"   Model: {result.model_used}")

if __name__ == "__main__":
    test_sora()
```

Run test:
```bash
python test_sora_integration.py
```

---

## 📖 Official API Usage

### Creating a Video

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create video
video = client.videos.create(
    model="sora-2-pro",
    prompt="A professional training scene in a modern Walmart store",
    size="1920x1080",
    seconds="10"
)

print(f"Job ID: {video.id}")
print(f"Status: {video.status}")
```

### Polling for Completion

```python
# Method 1: Manual polling
import time

while video.status in ['queued', 'in_progress']:
    video = client.videos.retrieve(video.id)
    print(f"Status: {video.status}, Progress: {video.progress}%")
    time.sleep(10)

# Method 2: SDK auto-polling
video = client.videos.create_and_poll(
    model="sora-2-pro",
    prompt="A professional training scene in a modern Walmart store",
    size="1920x1080",
    seconds="10"
)

if video.status == 'completed':
    print("✅ Video completed!")
```

### Downloading Video

```python
if video.status == 'completed':
    # Download video content
    content = client.videos.download_content(video.id)
    
    # Save to file
    with open('video.mp4', 'wb') as f:
        f.write(content.read())
    
    print("✅ Video saved to video.mp4")
```

### Using Image Reference

```python
# Start with a reference image (first frame)
with open('walmart_store.jpg', 'rb') as image_file:
    video = client.videos.create(
        model="sora-2-pro",
        prompt="Camera pans across the store, associates working",
        size="1920x1080",
        seconds="10",
        input_reference=image_file
    )
```

### Remixing a Video

```python
# Remix an existing video
remix_job = client.videos.remix(
    video_id="video_abc123",
    prompt="Change the lighting to warm golden hour tones"
)

# Poll for remix completion
remix_video = client.videos.create_and_poll(remix_job.id)
```

---

## 🎨 Effective Prompting for Sora

### Best Practices

**Be Specific About:**
1. **Shot Type** - Wide, close-up, medium, aerial, tracking, etc.
2. **Subject** - What's the main focus?
3. **Action** - What's happening?
4. **Setting** - Where is this taking place?
5. **Lighting** - Time of day, quality of light
6. **Camera Movement** - Pan, tilt, zoom, static, etc.

### Examples for Walmart

#### Training Video
```
"Medium shot of a Walmart associate in a blue vest demonstrating proper 
shelf stocking technique, bright fluorescent store lighting, modern retail 
environment with organized shelves in background, associate smiling and 
making eye contact with camera, professional and welcoming atmosphere"
```

#### Recognition Video
```
"Wide shot of a Walmart store team gathered in a circle, team leader 
presenting an achievement award to an associate, colleagues clapping and 
smiling, warm overhead lighting, positive and celebratory mood, camera 
slowly pushes in toward the honored associate"
```

#### Safety Alert
```
"Close-up of bright yellow caution sign being placed on wet floor, then 
camera tilts up to show Walmart associate in safety vest securing the area, 
clean modern store interior, high contrast lighting emphasizing the warning 
sign, urgent but professional tone"
```

---

## ⚙️ Configuration Options

### Request Parameters

```python
{
    "model": "sora-2" | "sora-2-pro",
    "prompt": str,  # Required, detailed description
    "size": str,    # "1280x720", "1920x1080", etc.
    "seconds": str, # "5", "8", "10", etc.
    "input_reference": file  # Optional, image file for first frame
}
```

### Response Object

```python
{
    "id": str,              # Unique video job ID
    "object": "video",
    "created_at": int,      # Unix timestamp
    "status": str,          # queued, in_progress, completed, failed
    "progress": int,        # 0-100 (when in_progress)
    "model": str,           # sora-2 or sora-2-pro
    "seconds": str,         # Video duration
    "size": str,            # Resolution
    "error": dict           # Only present if failed
}
```

---

## 🚨 Content Restrictions

### ✅ Allowed
- Professional workplace scenes
- Training scenarios
- Product demonstrations
- Abstract concepts
- Brand-safe content

### ❌ Prohibited
- ❌ Content not suitable for under 18
- ❌ Copyrighted characters (Mickey Mouse, Spider-Man, etc.)
- ❌ Copyrighted music
- ❌ Real people (public figures, celebrities)
- ❌ Input images with human faces

### For Walmart Videos
✅ **Safe:**
- Store interiors (no identifiable associates)
- Products on shelves
- Abstract "teamwork" concepts
- Training demonstrations (generic actors)

⚠️ **Check First:**
- Specific associate images
- Recognizable store locations
- Branded products (non-Walmart)

---

## 💰 Cost Optimization

### Choosing the Right Model

```python
# For rapid iteration and testing
provider = SoraVideoProvider(model="sora-2")
# - Faster generation
# - Lower cost per video
# - Good quality for most uses

# For final production videos
provider = SoraVideoProvider(model="sora-2-pro")
# - Best quality
# - Higher cost
# - Use for executive communications, marketing
```

### Batch Processing Strategy

```python
# Generate draft with sora-2
draft = provider.generate_video(prompt)

# Review and refine prompt based on draft

# Generate final with sora-2-pro
final = provider_pro.generate_video(refined_prompt)
```

---

## 🔧 Advanced Features

### Webhook Notifications

Instead of polling, use webhooks for automatic notifications:

**Configure webhook in OpenAI dashboard:**
1. Go to: https://platform.openai.com/webhooks
2. Add webhook URL: `https://your-app.com/webhooks/sora`
3. Subscribe to events: `video.completed`, `video.failed`

**Webhook payload:**
```json
{
  "id": "evt_abc123",
  "object": "event",
  "created_at": 1758941485,
  "type": "video.completed",  // or "video.failed"
  "data": {
    "id": "video_abc123"  // Video job ID
  }
}
```

**Handle webhook in your app:**
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhooks/sora', methods=['POST'])
def sora_webhook():
    event = request.json
    
    if event['type'] == 'video.completed':
        video_id = event['data']['id']
        # Download and process video
        download_and_save(video_id)
    
    elif event['type'] == 'video.failed':
        video_id = event['data']['id']
        # Handle failure
        log_failure(video_id)
    
    return {'status': 'ok'}
```

### Video Management

```python
# List all videos
videos = client.videos.list(limit=20, order='desc')

for video in videos.data:
    print(f"{video.id}: {video.status}")

# Delete old videos
for video in videos.data:
    if video.created_at < one_week_ago:
        client.videos.delete(video.id)
```

### Downloading Additional Assets

```python
# Download thumbnail
thumbnail = client.videos.download_content(
    video_id,
    variant="thumbnail"
)
with open('thumb.webp', 'wb') as f:
    f.write(thumbnail.read())

# Download spritesheet (for scrubbers/previews)
spritesheet = client.videos.download_content(
    video_id,
    variant="spritesheet"
)
with open('sprite.jpg', 'wb') as f:
    f.write(spritesheet.read())
```

---

## 📊 Integration Checklist

- [ ] **Get API Access**
  - [ ] OpenAI account created
  - [ ] API key generated with Sora access
  - [ ] Key saved in `.env` file
  - [ ] Tested authentication

- [ ] **Configure Zorro**
  - [ ] Updated `config.yaml`
  - [ ] Set `OPENAI_API_KEY` environment variable
  - [ ] Chose default model (sora-2 or sora-2-pro)

- [ ] **Code Integration**
  - [ ] Provider class reviewed (`src/providers/sora_provider.py`)
  - [ ] Provider registered in video generator
  - [ ] GUI updated with Sora option

- [ ] **Testing**
  - [ ] API connection tested
  - [ ] Sample video generated successfully
  - [ ] Both models tested (sora-2 and sora-2-pro)
  - [ ] Error handling verified
  - [ ] Webhook integration tested (if using)

- [ ] **Production Ready**
  - [ ] Content guidelines reviewed
  - [ ] Prompting best practices implemented
  - [ ] Cost optimization strategy in place
  - [ ] Monitoring and logging configured

---

## 🎯 Recommended Workflow

### Phase 1: Rapid Prototyping (Use sora-2)
```python
# Fast iteration for prompt testing
provider = SoraVideoProvider(model="sora-2")

for variation in prompt_variations:
    video = provider.generate_video(variation)
    review_and_score(video)

best_prompt = select_best()
```

### Phase 2: Production (Use sora-2-pro)
```python
# High-quality final output
provider = SoraVideoProvider(model="sora-2-pro")

final_video = provider.generate_video(best_prompt)
add_accessibility_features(final_video)
publish_to_associates()
```

---

## 🚀 Next Steps

1. **This Week:**
   - [ ] Get OpenAI API key with Sora access
   - [ ] Run test script
   - [ ] Generate first test video
   - [ ] Compare sora-2 vs sora-2-pro

2. **Next Month:**
   - [ ] Integrate with production pipeline
   - [ ] Test batch processing
   - [ ] Set up webhook notifications
   - [ ] Create prompt library for common use cases

3. **Production:**
   - [ ] Deploy to Walmart infrastructure
   - [ ] Configure monitoring and alerts
   - [ ] Train team on effective prompting
   - [ ] Launch pilot program

---

**Status:** ✅ Implementation complete - Ready to use once API access obtained!  
**Integration Time:** 2-4 hours  
**Documentation:** This guide + https://platform.openai.com/docs/guides/video
