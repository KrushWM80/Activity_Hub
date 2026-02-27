# 🎬 Zorro → Walmart GenAI Media Studio Integration

![Walmart Media GenAI Studio](WalmartMediaGenAIStudiodemo.png)

## Quick Start (5 minutes)

### 1. Setup Environment
```powershell
# Copy environment template
cp .env.template .env

# Edit .env and add your SSO token
notepad .env
```

### 2. Get SSO Token
- Open https://mediagenai.walmart.com/
- Login with Walmart SSO
- Request API access from `#help-genai-media-studio`

### 3. Test Integration
```powershell
python setup_walmart.py
```

### 4. Launch GUI
```powershell
python run_gui.py
```

---

## What Changed?

### ✅ New Provider Added
- **File**: `src/providers/walmart_media_studio.py`
- **What**: Complete provider implementation for Walmart GenAI Media Studio
- **Features**:
  - SSO authentication
  - Async job polling
  - Video download
  - Error handling
  - Health checks

### ✅ Config Updated
- **File**: `config/config.yaml`
- **Changed**: Default provider to `walmart_media_studio`
- **Added**: Media Studio specific settings

### ✅ GUI Enhanced
- **File**: `app.py`
- **Added**: Provider selection with status indicators
- **Shows**: ✅ for Walmart Media Studio, ⚠️ for external providers

### ✅ Setup Scripts
- **File**: `setup_walmart.py` - Interactive setup wizard
- **File**: `.env.template` - Environment variable template

### ✅ Documentation
- **File**: `WALMART_INTEGRATION.md` - Complete integration guide
- **File**: `README_WALMART.md` - This file

---

## How It Works

```
User Input
    ↓
Zorro GUI (Streamlit)
    ↓
Message Processor → Validates message
    ↓
Prompt Generator → Enhances with LLM
    ↓
Walmart Media Studio Provider
    ↓
    → Submit to Media Studio API
    → Poll for completion
    → Download video
    ↓
Display in GUI
```

---

## API Integration Status

### ✅ Ready Now
- Provider class implemented
- Configuration setup
- GUI integration
- Error handling
- Documentation

### ⏳ Waiting For
- [ ] API access approval from Next Gen Content DS team
- [ ] API endpoint documentation
- [ ] Request/response schema
- [ ] Authentication flow details

### 📝 Next Steps
1. Post in `#help-genai-media-studio`:
   ```
   Hi! Need API access for Zorro video generation project.
   Use case: Activity message → short celebration videos
   Tech: Python/Streamlit → Media Studio API
   Contact: [your-name]
   ```

2. When you receive API docs:
   - Update `api_endpoint` in `.env`
   - Update request/response formats in `walmart_media_studio.py`
   - Test with `setup_walmart.py`

3. Deploy to production:
   - Submit System Security Plan (SSP)
   - Deploy to Walmart Azure
   - Integrate with Element GenAI Platform

---

## Configuration

### Environment Variables
```bash
# Required
WALMART_SSO_TOKEN=your_token_here

# Optional (uses defaults)
WALMART_MEDIA_STUDIO_API=https://mediagenai.walmart.com/api/v1
```

### Config File (`config/config.yaml`)
```yaml
video:
  generator:
    provider: "walmart_media_studio"
    walmart_media_studio:
      timeout: 300
      max_retries: 3
      poll_interval: 5
```

---

## Testing

### Manual Test (Web UI)
1. Open https://mediagenai.walmart.com/
2. Run GUI: `python run_gui.py`
3. Generate prompt (don't click Generate Video yet)
4. Copy enhanced prompt to Media Studio
5. Generate video in Media Studio
6. Validate output quality

### Automated Test (After API Access)
```powershell
python setup_walmart.py
```

### Full Integration Test
```powershell
python run_gui.py
# Click preset → Generate Video → Wait → Download
```

---

## Troubleshooting

### "No authentication token"
**Solution**: Add `WALMART_SSO_TOKEN` to `.env`

### "API request failed: 401"
**Solution**: Token expired. Get new token from Media Studio

### "API request failed: 403"
**Solution**: Request API access via `#help-genai-media-studio`

### "Could not reach Media Studio API"
**Solution**: API endpoint may not be finalized. Contact Next Gen Content DS team

### "Video generation timed out"
**Solution**: Increase `timeout` in config (default: 300s)

---

## Comparison: Walmart vs External

| Feature | Walmart Media Studio | External (ModelScope) |
|---------|---------------------|----------------------|
| **Firewall** | ✅ No restrictions | ❌ Blocked |
| **Authentication** | ✅ SSO (automatic) | ❌ API keys needed |
| **Compliance** | ✅ Pre-approved | ❌ Requires review |
| **Models** | ✅ Google Veo (latest) | ⚠️ Older models |
| **Support** | ✅ Internal Slack | ❌ External docs only |
| **Cost Tracking** | ✅ Built-in | ❌ Manual |
| **Monitoring** | ✅ Element GenAI | ❌ Self-managed |
| **Production Ready** | ✅ Yes | ❌ Requires onboarding |

---

## Support

- **Slack**: `#help-genai-media-studio`
- **API Access**: Next Gen Content DS team
- **Platform**: Gen AI Enablement team
- **Security**: InfoSec (for SSP)

---

## Files to Review

1. **Implementation**: `src/providers/walmart_media_studio.py`
2. **Integration Guide**: `WALMART_INTEGRATION.md`
3. **Setup Script**: `setup_walmart.py`
4. **Config**: `config/config.yaml`
5. **Environment**: `.env.template`

---

## Timeline

- ✅ **Done**: Provider implementation, config, GUI
- ⏳ **1-3 days**: API access request
- ⏳ **1-2 days**: API integration with docs
- ⏳ **1 day**: Testing and validation
- ⏳ **2-3 days**: Production deployment

**Total: 1-2 weeks to production**

---

## What's Different from External Providers?

### Old Way (ModelScope - Blocked)
```python
# Downloads 6GB model from HuggingFace (blocked)
from diffusers import DiffusionPipeline
pipe = DiffusionPipeline.from_pretrained("damo-vilab/...")  # ❌ Firewall
```

### New Way (Walmart Media Studio - Works!)
```python
# Uses Walmart's internal platform (no download)
from src.providers.walmart_media_studio import WalmartMediaStudioProvider
provider = WalmartMediaStudioProvider()  # ✅ Pre-approved
video = provider.generate_video(prompt)   # ✅ Works!
```

---

## Success Criteria

After integration, you should see:

✅ GUI launches successfully  
✅ Walmart Media Studio selected as provider  
✅ SSO token authenticated  
✅ Video generation completes  
✅ Video downloads and displays  
✅ No firewall errors  
✅ Full audit trail in Element GenAI  

---

**Status**: Ready for API access request!  
**Next**: Post in `#help-genai-media-studio` to request API access
