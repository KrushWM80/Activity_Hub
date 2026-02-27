# API Testing Guide - GenAI Media Studio
## December 1, 2025

---

## 🚀 Quick Start (5 minutes)

### Option 1: Using the Built-In Test Script

```powershell
# 1. Navigate to project
cd "c:\Users\hrisaac\OneDrive - Walmart Inc\Documents\VSCode\Projects\zorro"

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Run the test script
python test_walmart_api.py
```

**What it tests:**
- ✅ API connectivity
- ✅ Authentication (SSO token)
- ✅ Provider availability
- ✅ Available models and configurations
- ✅ Video generation (optional)

---

## 📋 Prerequisites

Before testing, you need:

### 1. **API Access Granted** ✅
- Status: Approved by Stephanie (Dec 1, 2025)
- Contact: Oskar Radermecker (oskar.radermecker@walmart.com)
- Endpoint: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs

### 2. **Authentication Mechanism**
- Status: **In progress** (SSO implementation underway)
- What you'll receive from Oskar:
  - SSO token, OR
  - API key, OR
  - OAuth2 credentials
- Timeline: Should arrive this week (Dec 1-6, 2025)

### 3. **Environment Setup**
```bash
# Create or update .env file
notepad .env

# Add this line (replace with actual token when received):
WALMART_SSO_TOKEN=your-token-here

# Optional: Override API endpoint (pre-configured)
WALMART_MEDIA_STUDIO_API=https://retina-ds-genai-backend.prod.k8s.walmart.net
```

### 4. **Python Dependencies**
```bash
# Install all requirements
pip install -r requirements.txt

# Or just the essentials
pip install requests pydantic python-dotenv
```

---

## 🧪 Testing Methods

### METHOD 1: Connection Test Only (Recommended First)

```bash
python test_walmart_api.py
```

**Expected Output:**
```
============================================================
Walmart Media Studio API - Connection Test
============================================================

✅ SSO Token found: sk-proj-abc123...

📡 Initializing Media Studio provider...

📋 Provider Information:
   Name: Walmart GenAI Media Studio
   Endpoint: https://retina-ds-genai-backend.prod.k8s.walmart.net
   Authenticated: True
   Documentation: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs
   Support: #help-genai-media-studio

🔍 Testing API connection...
✅ Media Studio API is available!
   Models: Google Veo, Google Imagen
   Duration range: 4-8 seconds
   Aspect ratios: 16:9, 9:16, 1:1
```

### METHOD 2: Quick Video Generation Test

```python
# test_quick.py
import os
from src.providers.walmart_media_studio import WalmartMediaStudioProvider
from src.models.video_models import VideoPrompt

# Setup
provider = WalmartMediaStudioProvider()
prompt = VideoPrompt(
    text="Walmart associate helping a customer",
    duration=8,
    aspect_ratio="16:9"
)

# Generate
video = provider.generate_video(prompt)

# Results
print(f"Video generated: {video.video_id}")
print(f"Status: {video.status}")
print(f"Duration: {video.duration} seconds")
if video.path:
    print(f"Saved to: {video.path}")
```

**Run it:**
```bash
python test_quick.py
```

### METHOD 3: Full Pipeline Test (End-to-End)

```python
# test_full_pipeline.py
import os
from src.core.pipeline import VideoGenerationPipeline

# Initialize
pipeline = VideoGenerationPipeline()

# Generate with all features
result = pipeline.generate(
    message_content="Thank you for great customer service this week!",
    message_category="recognition",
    message_priority="high",
    apply_editing=True,
    add_accessibility=True,
    add_fade=True,
    trim_duration=8.0
)

# Results
print(f"✅ Video: {result.path}")
print(f"✅ Captions: {result.accessibility.captions_path}")
print(f"✅ Audio: {result.accessibility.audio_description_path}")
print(f"✅ Transcript: {result.accessibility.transcript_path}")
```

**Run it:**
```bash
python test_full_pipeline.py
```

---

## 🐛 Troubleshooting

### Issue 1: "WALMART_SSO_TOKEN not found"

**Problem:**
```
❌ ERROR: WALMART_SSO_TOKEN not found

Please set your SSO token in .env file:
WALMART_SSO_TOKEN=your-token-here
```

**Solution:**
1. Confirm you received authentication credentials from Oskar
2. Create/edit `.env` file in project root
3. Add line: `WALMART_SSO_TOKEN=your-actual-token`
4. Save and retry

**Verify:**
```bash
# Windows PowerShell
echo $env:WALMART_SSO_TOKEN

# If blank, .env not loaded. Restart terminal.
```

### Issue 2: "API not available" / 403 Error

**Problem:**
```
❌ Media Studio API not available

Possible issues:
1. SSO token expired or invalid
2. API access not yet granted
3. Network connectivity issues
```

**Solution:**
1. **Check token validity:**
   - Token may have expired
   - Request new token from Oskar
   - Verify format (should start with `sk-proj-` or similar)

2. **Check network:**
   ```bash
   # Test connectivity to endpoint
   curl https://retina-ds-genai-backend.prod.k8s.walmart.net/docs
   ```

3. **Check API access:**
   - Confirm approval email from Stephanie/Oskar
   - Check project is listed in your API access
   - Message #help-genai-media-studio if still blocked

4. **Check endpoint:**
   - Verify .env has correct endpoint
   - Should be: `https://retina-ds-genai-backend.prod.k8s.walmart.net`
   - NOT: `https://mediagenai.walmart.com/api` (old endpoint)

### Issue 3: "Connection timeout" / Slow Response

**Problem:**
```
Timeout waiting for API response...
ConnectionError: API request timed out
```

**Solution:**
1. **API may be slow:**
   - Video generation takes 2-5 minutes
   - Increase timeout in config:
     ```yaml
     api:
       timeout: 600  # 10 minutes
     ```

2. **Check API status:**
   - Visit https://retina-ds-genai-backend.prod.k8s.walmart.net/docs
   - Verify endpoint is responding

3. **Network issues:**
   - Check Walmart network connectivity
   - May need to run on Walmart VPN

### Issue 4: "Invalid prompt" / 400 Error

**Problem:**
```
BadRequest: Invalid video prompt
Video prompt must be 10-500 characters
```

**Solution:**
1. Check prompt length: 10-500 characters
2. Avoid special characters that need escaping
3. Use clear, descriptive language
4. Reference API docs for format: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs

---

## 📊 Test Scenarios

### Scenario 1: Verify Connection (No Video Generation)
**Time:** 30 seconds  
**Risk:** None (read-only)
```bash
python test_walmart_api.py
```

**What you'll know:**
- ✅ API is reachable
- ✅ Authentication working
- ✅ Credentials are valid

---

### Scenario 2: Generate 1 Test Video
**Time:** 5-10 minutes  
**Risk:** Minimal (single video, no scale)
```python
from src.providers.walmart_media_studio import WalmartMediaStudioProvider
from src.models.video_models import VideoPrompt

provider = WalmartMediaStudioProvider()
prompt = VideoPrompt(
    text="Walmart store manager greeting customers",
    duration=8,
    aspect_ratio="16:9"
)
video = provider.generate_video(prompt)
print(f"Generated: {video.path}")
```

**What you'll know:**
- ✅ Full API pipeline working
- ✅ Video quality acceptable
- ✅ Generation time reasonable
- ✅ Output format correct

---

### Scenario 3: Batch Test (5 Videos)
**Time:** 20-30 minutes  
**Risk:** Low (small batch test)
```python
from src.core.pipeline import VideoGenerationPipeline

pipeline = VideoGenerationPipeline()

prompts = [
    "Thank you for great customer service",
    "Remember to scan items at checkout",
    "Walmart team meeting this Friday at 2pm",
    "Update your store location in the system",
    "Safety reminder: Spill in aisle 5 cleaned"
]

for prompt in prompts:
    result = pipeline.generate(
        message_content=prompt,
        message_category="training"
    )
    print(f"✅ Generated: {result.path}")
```

**What you'll know:**
- ✅ Batch processing works
- ✅ API performance at scale
- ✅ Consistency across multiple videos
- ✅ Pipeline ready for 1 video/week pilot

---

## ✅ Success Checklist

After running tests, verify:

- [ ] Test script runs without errors
- [ ] SSO token successfully loaded from .env
- [ ] API connectivity confirmed
- [ ] Provider information displays correctly
- [ ] Models and configurations listed
- [ ] (Optional) Test video generated successfully
- [ ] (Optional) Video file exists and playable
- [ ] (Optional) Accessibility files created (captions, audio)

**If all checked:** ✅ **API is ready for production pilot!**

---

## 🎯 Next Steps After Successful Test

### If Everything Works ✅

1. **Document Results**
   - Screenshot successful test output
   - Note generation time and quality
   - Save sample generated video

2. **Update Status**
   ```bash
   git add APPROVAL_MILESTONE_DEC1.md
   git commit -m "test: API integration test successful - ready for pilot"
   ```

3. **Start Pilot (1 video/week)**
   - Schedule first video generation
   - Select sample OneWalmart message
   - Follow full pipeline through accessibility
   - Document results

4. **Prepare for 2-Week Check-In**
   - Collect metrics and learnings
   - Prepare presentation for Stephanie
   - Plan scale-up strategy

### If Issues Found ⚠️

1. **Debug Step-by-Step**
   - Connection test → Provider info → Video generation
   - Note where it fails

2. **Message Oskar**
   - Share error messages
   - Include full test output
   - Ask for guidance

3. **Check Documentation**
   - https://retina-ds-genai-backend.prod.k8s.walmart.net/docs
   - Review endpoint details
   - Check authentication format

---

## 📞 Support

**For API questions:**
- Channel: #help-genai-media-studio
- Contacts: Oskar Radermecker, Stephanie Tsai

**For code issues:**
- Check: src/providers/walmart_media_studio.py
- Reference: README.md, API_GUIDE.md

**For authentication:**
- Wait for Oskar's email with credentials
- Should arrive this week (Dec 1-6, 2025)

---

## 🚀 Timeline

| Date | Task | Status |
|------|------|--------|
| Dec 1 | API access approved | ✅ |
| Dec 1-6 | Await authentication mechanism | ⏳ |
| Dec 2-6 | Configure and test API | 📋 |
| Dec 9-15 | Generate 1 pilot video/week | 📋 |
| Dec 15 | 2-week check-in with Stephanie | 📋 |
| Dec 16+ | Scale to 100-150/week (if approved) | 📋 |

---

**Ready to test?**

1. Wait for authentication credentials from Oskar (this week)
2. Add to .env file
3. Run: `python test_walmart_api.py`
4. Report results!
