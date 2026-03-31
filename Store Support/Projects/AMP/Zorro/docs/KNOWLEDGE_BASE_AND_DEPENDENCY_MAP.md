# Zorro - Knowledge Base & Dependency Map

## AI Video Generation Platform & Audio Message Hub for Walmart Operations
**Last Updated:** March 31, 2026  
**Version:** 2.0  
**Project Status:** Phase 1 Production - Pilot Active

---

## Audio Message Hub

| Property | Value |
|----------|-------|
| **Name** | Audio Message Hub |
| **URL** | http://weus42608431466:8888/Zorro/Audio_Message_Hub |
| **Port** | 8888 |
| **Server Script** | `audio_server.py` |
| **Pipeline Script** | `Audio/Scripts/generate_weekly_audio.py` |
| **Synthesizer** | `Audio/windows_media_synthesizer.py` |
| **Voice** | Jenny Neural (en-US) via edge-tts |
| **Fallback Voice** | SAPI5 (Microsoft David) when VPN blocks edge-tts |
| **Output Dir** | `output/Audio/` |
| **Automation** | `Automation/start_zorro_24_7.bat` (auto-restart) |
| **Health Check** | `MONITOR_AND_REPORT.ps1` (daily 6 AM, port 8888 check) |
| **BQ Source** | `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2` |
| **BQ Filter** | `Message_Type = 'Merchant Message' AND Status = 'Review for Publish review - No Comms'` |
| **CMS URL Pattern** | `https://enablement.walmart.com/content/store-communications/home/merchandise/weekly-messages/{year}/week-{week}/weekly_messages_audiowk{week}.html` |
| **Email** | Outlook COM (win32com.client) with retry for RPC_E_CALL_REJECTED |

### Audio Pipeline Steps
1. **Step 1 (BQ Fetch)** — Queries AMP ALL 2 + Cosmos for message bodies, extracts summaries, caches to `Audio/Scripts/cache/week_{N}_fy{FY}.json`. Requires Eagle WiFi (non-VPN).
2. **Step 2 (Synthesize)** — Single-pass Jenny Neural TTS → AAC 256kbps MP4 with thumbnail mux. Generates Standard Script, Inflection Script, HTML Email Report. Requires Walmart WiFi (off VPN).
3. **Email Report** — Sends via Outlook COM with MP4 + both scripts attached.

### Output Files
- `Weekly Messages Audio Template - Summarized - Week {N} - Jenny Neural - Vimeo.mp4`
- `Week {N} - Weekly Messages Audio Script.txt` (Standard)
- `Week {N} - Weekly Messages Audio Script (Inflection).txt` (with prosody markings)
- `Week {N} - Weekly Messages Audio Report.html`
- `audio_links.json` (CMS URLs for BQ publish)

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Dependency Map](#3-dependency-map)
4. [Core Components Reference](#4-core-components-reference)
5. [Data Flow](#5-data-flow)
6. [Configuration Reference](#6-configuration-reference)
7. [API Integration](#7-api-integration)
8. [Common Patterns (Cascaded)](#8-common-patterns-cascaded)
9. [Common Pitfalls & Solutions](#9-common-pitfalls--solutions)
10. [Testing Checklist](#10-testing-checklist)
11. [Quick Reference: File Locations](#11-quick-reference-file-locations)
12. [Version History](#12-version-history)

---

## 1. Project Overview

### Business Purpose
**Zorro** streamlines production of professional video content for **4,700+ Walmart facilities** by converting operational AMP (Activity Message Platform) messages into engaging, brand-consistent videos.

### Target Users
- **Business Managers** who need to create reusable design elements
- **Operations Teams** who rapidly process queued AMP messages into videos
- **Field Communications** who distribute videos across facilities

### Key Capabilities
| Feature | Description | Status |
|---------|-------------|--------|
| **Design Studio** | Create/manage characters, backgrounds, templates | ✅ Complete |
| **Message Queue** | AMP message workflow with variable selection | ✅ Complete |
| **Video Generation** | Walmart Media Studio API (Google Veo) | ✅ Complete |
| **Video Trimmer** | FFmpeg-based trim and download | ✅ Complete |
| **Accessibility** | Captions, audio descriptions, transcripts | ✅ Complete |
| **AI Disclosure** | Legal watermark requirement | 🔴 Pending |

### Scale Roadmap
| Phase | Timeline | Videos/Week | Concurrent Users |
|-------|----------|-------------|------------------|
| Pilot | Dec 2025 | 1-5 | 2 |
| Phase 1 | Jan 2026 | 10-25 | 3 |
| Phase 2 | Feb 2026 | 50-100 | 5 |
| Phase 3 | Q2 2026 | 100-150 | 10 |
| Production | Q3 2026 | 150-200+ | 10+ |

---

## 2. Architecture Overview

### High-Level Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ZORRO PIPELINE FLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   User Input (Design Studio UI)                                          │
│        │                                                                 │
│        ▼                                                                 │
│   ┌─────────────────────────┐                                           │
│   │  MessageProcessor       │ ─── Validate, sanitize, expand acronyms   │
│   └────────────┬────────────┘                                           │
│                ▼                                                         │
│   ┌─────────────────────────┐                                           │
│   │  PromptGenerator        │ ─── LLM enhancement OR passthrough mode   │
│   │  (with DesignStudio)    │                                           │
│   └────────────┬────────────┘                                           │
│                ▼                                                         │
│   ┌─────────────────────────┐                                           │
│   │  VideoGenerator         │ ─── Walmart Media Studio API (Veo)        │
│   │  (WalmartMediaStudio)   │                                           │
│   └────────────┬────────────┘                                           │
│                ▼                                                         │
│   ┌─────────────────────────┐                                           │
│   │  VideoEditor            │ ─── FFmpeg trim, format, effects          │
│   └────────────┬────────────┘                                           │
│                ▼                                                         │
│   ┌─────────────────────────┐                                           │
│   │  AccessibilityEnhancer  │ ─── Captions, audio desc, transcripts     │
│   └────────────┬────────────┘                                           │
│                ▼                                                         │
│   Generated Video (MP4) + Accessibility Assets                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| **Frontend** | Streamlit | Multi-page web interface |
| **Backend** | Python 3.9+ | Core processing logic |
| **Video Gen** | Walmart Media Studio API | Google Veo models (veo2, veo3) |
| **LLM** | OpenAI/Anthropic/Passthrough | Prompt enhancement |
| **Video Processing** | FFmpeg, MoviePy, OpenCV | Editing, trimming |
| **Captions** | WebVTT, SRT | Accessibility |
| **TTS** | gTTS, pyttsx3 | Audio descriptions |
| **Data** | Pydantic v2 | Data validation |
| **Config** | YAML | Environment-specific settings |

---

## 3. Dependency Map

### 3.1 Component Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      COMPONENT DEPENDENCY GRAPH                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   app.py (Entry Point)                                                   │
│   ├── src/core/pipeline.py                                              │
│   │   ├── src/core/message_processor.py                                 │
│   │   ├── src/core/prompt_generator.py                                  │
│   │   │   └── src/services/llm_service.py                               │
│   │   ├── src/core/video_generator.py                                   │
│   │   │   └── src/providers/walmart_media_studio.py                     │
│   │   │       └── src/security/ssl_config.py                            │
│   │   ├── src/core/video_editor.py                                      │
│   │   └── src/core/accessibility_enhancer.py                            │
│   │                                                                      │
│   ├── src/services/design_studio_service.py                             │
│   │   └── src/models/design_element.py                                  │
│   │                                                                      │
│   ├── src/ui/components/design_selector.py                              │
│   │   └── src/services/design_studio_service.py                         │
│   │                                                                      │
│   └── src/ui/components/video_trimmer.py                                │
│                                                                          │
│   pages/design_studio.py                                                 │
│   ├── src/services/design_studio_service.py                             │
│   └── src/ui/components/design_selector.py                              │
│                                                                          │
│   pages/message_queue.py                                                 │
│   ├── src/core/pipeline.py                                              │
│   └── src/ui/components/video_trimmer.py                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Model Dependencies

```
src/models/
├── message.py
│   ├── MessagePriority (Enum)
│   ├── MessageCategory (Enum)
│   └── ActivityMessage (Pydantic)
│
├── prompt.py
│   ├── VideoPrompt (Pydantic)
│   └── PromptMetadata (Pydantic)
│
├── video.py
│   ├── GeneratedVideo (Pydantic)
│   └── AccessibilityMetadata (Pydantic)
│
├── design_element.py
│   ├── DesignElementType (Enum): CHARACTER, LOGO, ENVIRONMENT, PROP...
│   ├── DesignCategory (Enum): TRAINING, MARKETING, OPERATIONS...
│   ├── DesignVisibility (Enum): PRIVATE, FACILITY, REGION, COMPANY
│   ├── DesignMetadata (Pydantic)
│   ├── DesignElement (Pydantic)
│   ├── DesignLibrary (Pydantic)
│   └── ProductionTemplate (Pydantic)
│
└── video_models.py
    └── Additional video-related models
```

### 3.3 Provider Dependencies

```
src/providers/
├── base_provider.py
│   └── BaseVideoProvider (Abstract)
│
├── walmart_media_studio.py (PRIMARY)
│   ├── WalmartMediaStudioProvider
│   ├── CircuitBreaker (resilience)
│   ├── RateLimiter
│   └── Dependencies:
│       ├── requests
│       ├── urllib3
│       └── src/security/ssl_config.py
│
├── sora_provider.py (FUTURE)
│   └── SoraProvider (OpenAI Sora 2)
│
└── Alternative providers:
    ├── modelscope_service.py
    ├── stability_service.py
    └── runwayml_service.py
```

### 3.4 External Service Dependencies

| Service | Purpose | Endpoint | Auth |
|---------|---------|----------|------|
| **Walmart Media Studio** | Video generation (Veo) | `retina-ds-genai-backend.prod.k8s.walmart.net` | SSO Token |
| **OpenAI** | Prompt enhancement | `api.openai.com` | API Key |
| **Anthropic** | Fallback LLM | `api.anthropic.com` | API Key |
| **gTTS** | Text-to-speech | Google TTS | None |

### 3.5 File Dependencies Matrix

| File | Imports From | Imported By |
|------|--------------|-------------|
| `app.py` | pipeline, design_studio_service, design_selector, video_trimmer | - |
| `pipeline.py` | message_processor, prompt_generator, video_generator, video_editor, accessibility_enhancer, models | app.py, pages/* |
| `walmart_media_studio.py` | security/ssl_config, requests, urllib3 | video_generator.py |
| `design_studio_service.py` | models/design_element | app.py, pages/design_studio.py, design_selector.py |
| `llm_service.py` | openai, anthropic, config | prompt_generator.py |

---

## 4. Core Components Reference

### 4.1 VideoGenerationPipeline

**Location:** `src/core/pipeline.py`

**Purpose:** End-to-end orchestration of video generation

**Key Methods:**
```python
class VideoGenerationPipeline:
    def generate(
        self,
        message_content: str,
        message_category: str = "general",
        message_priority: str = "medium",
        sender_id: Optional[str] = None,
        apply_editing: bool = True,
        add_accessibility: bool = True,
        skip_llm_enhancement: bool = False,  # Passthrough mode
        **kwargs
    ) → GeneratedVideo
```

**Used By:**
- `app.py` - Main video generation interface
- `pages/message_queue.py` - Batch processing

### 4.2 DesignStudioService

**Location:** `src/services/design_studio_service.py`

**Purpose:** CRUD operations for design elements (characters, backgrounds, templates)

**Key Methods:**
```python
class DesignStudioService:
    def create_element(name, element_type, description, ...) → DesignElement
    def get_element(element_id) → Optional[DesignElement]
    def update_element(element_id, **updates) → Optional[DesignElement]
    def delete_element(element_id) → bool
    def list_elements(element_type=None) → List[DesignElement]
    def search_elements(query) → List[DesignElement]
    def create_template(name, elements, ...) → ProductionTemplate
```

**Constants:**
```python
MAX_NAME_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 5000
MAX_PROMPT_LENGTH = 10000
MAX_TAG_LENGTH = 50
MAX_TAGS_COUNT = 20
```

**Data Storage:** `data/design_library.json`

### 4.3 WalmartMediaStudioProvider

**Location:** `src/providers/walmart_media_studio.py`

**Purpose:** Integration with Walmart's GenAI Media Studio API

**Key Features:**
- Circuit breaker pattern for resilience
- Rate limiting (10 req/min, 100 req/hour)
- SSL configuration for Walmart network
- Support for veo2, veo3, imagen-4.0 models

**Configuration:**
```yaml
walmart_media_studio:
  api_endpoint: "https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1"
  timeout: 300  # seconds
  max_retries: 3
  poll_interval: 5  # seconds for job status polling
```

### 4.4 AccessibilityEnhancer

**Location:** `src/core/accessibility_enhancer.py`

**Purpose:** WCAG AAA compliance features

**Features:**
- WebVTT caption generation
- Audio descriptions (gTTS)
- Transcript generation
- Contrast validation

### 4.5 Design Selector Component

**Location:** `src/ui/components/design_selector.py`

**Purpose:** UI component for selecting design elements in Streamlit

**Key Functions:**
```python
def render_design_selector() → Dict[str, DesignElement]
def render_design_preview(elements: Dict) → None
def _generate_composite_prompt(elements: Dict) → str
def create_design_preset(name, elements) → ProductionTemplate
```

### 4.6 Video Trimmer Component

**Location:** `src/ui/components/video_trimmer.py`

**Purpose:** FFmpeg-based video trimming UI

**Key Functions:**
```python
def render_quick_trim_button(video_path: str) → Optional[str]
def trim_video(input_path, start_time, end_time) → str
```

---

## 5. Data Flow

### 5.1 Design Studio → Video Generation Flow

```
1. CREATE DESIGN ELEMENTS (One-Time)
   └── User creates characters, backgrounds, templates
       └── DesignStudioService.create_element()
           └── Saved to data/design_library.json

2. SELECT ELEMENTS FOR VIDEO
   └── User selects from design library
       └── render_design_selector() returns selected elements
           └── _generate_composite_prompt() builds prompt

3. GENERATE VIDEO
   └── Composite prompt → Pipeline.generate()
       └── skip_llm_enhancement=True (passthrough mode)
           └── WalmartMediaStudioProvider.generate()
               └── enhanced_prompt: true (API handles enhancement)

4. POST-PROCESSING
   └── VideoEditor (trim, effects)
       └── AccessibilityEnhancer (captions, transcripts)
           └── Output: MP4 + WebVTT + Transcript
```

### 5.2 AMP Message Queue Flow

```
1. LOAD AMP MESSAGES
   └── data/sample_amp_messages.json
       └── Display in message queue UI

2. SELECT MESSAGE
   └── User picks message from queue
       └── Choose template (character + background)

3. APPLY VARIABLES
   └── Template variables filled
       └── Composite prompt generated

4. GENERATE & TRIM
   └── Pipeline.generate()
       └── Optional: video_trimmer.render_quick_trim_button()

5. DOWNLOAD/DISTRIBUTE
   └── MP4 download
       └── Embed in field communications
```

### 5.3 Configuration Flow

```
config/config.yaml
    │
    ├── Loaded by: src/utils/__init__.py → get_config()
    │
    ├── Used by:
    │   ├── pipeline.py (video settings)
    │   ├── llm_service.py (LLM settings)
    │   ├── walmart_media_studio.py (API settings)
    │   └── accessibility_enhancer.py (caption settings)
    │
    └── Environment overrides:
        ├── config.dev.yaml (development)
        └── config.prod.yaml (production)
```

---

## 6. Configuration Reference

### 6.1 Main Configuration (`config/config.yaml`)

```yaml
# Application
app:
  name: "Zorro Video Generator"
  version: "0.1.0"
  environment: "development"
  debug: true

# Video Generation
video:
  default_duration: 10  # seconds
  default_fps: 24
  generator:
    provider: "walmart_media_studio"
    model_name: "veo"  # veo2, veo3

# LLM Configuration
llm:
  provider: "openai"  # openai, anthropic, passthrough
  model: "gpt-4-turbo-preview"
  passthrough_mode: true  # RECOMMENDED for Walmart network

# Performance
performance:
  max_concurrent_generations: 2
  rate_limit:
    requests_per_minute: 10
    requests_per_hour: 100

# Accessibility
accessibility:
  captions:
    enabled: true
    format: "webvtt"
  audio_description:
    enabled: true
```

### 6.2 Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API authentication | Required for LLM |
| `WALMART_SSO_TOKEN` | Walmart Media Studio auth | Required for video gen |
| `WALMART_SSL_VERIFY` | SSL verification toggle | `false` (dev) |
| `WALMART_CA_BUNDLE` | CA certificate bundle path | None |

---

## 7. API Integration

### 7.1 Walmart Media Studio API

**Endpoint:** `https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1`

**Authentication:** SSO Token in Authorization header

**Video Generation Request:**
```json
{
  "prompt": "A friendly mascot in a Walmart store aisle...",
  "model": "veo2",
  "enhanced_prompt": true,
  "negative_prompt": "blurry, distorted, wrong colors...",
  "duration": 8,
  "aspect_ratio": "16:9"
}
```

**Response:**
```json
{
  "job_id": "gen-abc123",
  "status": "processing",
  "estimated_time": 120
}
```

**Polling for Completion:**
```python
GET /api/v1/jobs/{job_id}
→ {"status": "completed", "video_url": "https://..."}
```

### 7.2 API Rate Limits (Confirmed Dec 5, 2025)

| Limit | Value | Notes |
|-------|-------|-------|
| Requests/minute | 10 | Not a concern for pilot |
| Requests/hour | 100 | Not a concern for pilot |
| Concurrent users | 2 | Approved for current use |
| Video duration | 5-8 seconds | API constraint |

---

## 8. Common Patterns (Cascaded)

### 8.1 From project-updates: MASTER-INDEX Pattern

**Recommendation:** Create `MASTER-INDEX.md` for Zorro

```markdown
# Zorro - Master Documentation Index

## 🎯 Quick Start by Role
| Role | Start Here | Then Read |
|------|------------|-----------|
| Business User | [QUICKSTART_GUI.md] | [DESIGN_STUDIO_GUIDE.md] |
| Developer | [README.md] | [API_INTEGRATION_GUIDE.md] |
| DevOps | [DEPLOYMENT_GUIDE.md] | [Dockerfile] |

## 📁 Complete Documentation Map
...
```

**Status:** 🔄 Cascade pending

### 8.2 From pricing-and-modulars: Mock Data Pattern

**Origin:** Modular Balancing mock data system

**Zorro Implementation:**
```python
# Already implemented: data/sample_amp_messages.json
# Pattern for future expansion:

class DataSource:
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock or os.getenv("USE_MOCK_DATA", "false").lower() == "true"
    
    def get_messages(self) → List[Dict]:
        if self.use_mock:
            return self._load_mock_data()
        return self._query_amp_api()
```

**Status:** ✅ Partially implemented (design library, sample messages)

### 8.3 From Tour-It: Security Headers Middleware

**Apply to Zorro:**

```python
# For future API endpoints (if Zorro exposes REST API):
class SecurityHeadersMiddleware:
    async def __call__(self, scope, receive, send):
        # Content Security Policy
        headers[b"content-security-policy"] = b"default-src 'self'"
        # HSTS
        headers[b"strict-transport-security"] = b"max-age=31536000"
        # Prevent clickjacking
        headers[b"x-frame-options"] = b"DENY"
```

**Status:** 🔄 Cascade pending (needed if REST API added)

### 8.4 From pricing-and-modulars: Interactive Help Pattern

**Apply to Streamlit UI:**

```python
def feature_card_with_help(title: str, description: str, help_content: dict):
    """Feature card that shows details on click"""
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader(title)
        st.write(description)
    with col2:
        with st.popover("ℹ️"):
            st.markdown(f"**How it works:** {help_content['explanation']}")
            st.markdown(f"**Tips:** {help_content['tips']}")
```

**Status:** 🔄 Cascade pending

### 8.5 Adoption Tracking

| Pattern | Source | Status | Notes |
|---------|--------|--------|-------|
| MASTER-INDEX.md | Tour-It | 🔄 Pending | Create navigation index |
| Mock Data | Modular Balancing | ✅ Partial | sample_amp_messages.json exists |
| Security Headers | Tour-It | 🔄 N/A | No REST API yet |
| Interactive Help | Modular Balancing | 🔄 Pending | Add to Design Studio |
| Multi-Provider AI | Zorro (origin) | ✅ Complete | LLM fallback pattern |
| WCAG AAA | Zorro (origin) | ✅ Complete | Accessibility features |

---

## 9. Common Pitfalls & Solutions

### 9.1 SSL Verification Errors

| Symptom | Cause | Solution |
|---------|-------|----------|
| `SSLError: certificate verify failed` | Walmart internal API uses self-signed cert | Set `WALMART_SSL_VERIFY=false` in `.env` |
| `SSL: CERTIFICATE_VERIFY_FAILED - self-signed certificate` | SSLConfiguration defaults to verify=true | Add `WALMART_SSL_VERIFY=false` to environment |
| Connection timeout to Media Studio | Not on Walmart network | Connect to Walmart VPN or internal network |

**✅ Required .env setting for internal network:**
```bash
WALMART_SSL_VERIFY=false
```

### 9.2 Video Generation Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Video generation provider is not available" | SSL verification failing OR demo_mode enabled | Set `WALMART_SSL_VERIFY=false` AND `demo_mode: false` |
| Videos don't match prompts | External LLM blocked by firewall | Use `passthrough_mode: true` in config |
| Long generation times (~37s) | Normal API processing | Expected behavior, poll_interval handles this |
| Generation fails repeatedly | Circuit breaker open | Wait for `recovery_timeout` (60s) |
| Videos not rendering (placeholder returned) | `demo_mode: true` in config | Set `demo_mode: false` in `config/config.yaml` |

### 9.3 "Provider Not Available" Error (Jan 2026 Fix)

**Error:** `Video generation failed: Video generation provider is not available`

**Root Cause:** The `is_available()` health check in `walmart_media_studio.py` was failing due to SSL certificate verification against Walmart's internal self-signed certificate.

**Solution:**
1. Add to `.env`:
   ```bash
   WALMART_SSL_VERIFY=false
   ```
2. Ensure `demo_mode: false` in `config/config.yaml`
3. Restart Streamlit server

**Verification:**
```bash
python test_api.py  # Should return status 200 and request_id
```

### 9.3 LLM Passthrough Mode

**⚠️ CRITICAL: Use passthrough mode on Walmart network**

```yaml
# config/config.yaml
llm:
  passthrough_mode: true  # RECOMMENDED
```

**Why:**
- External LLM APIs (OpenAI/Anthropic) blocked by Walmart VPN
- Media Studio has `enhanced_prompt: true` which uses internal AI
- Prompts go directly to Media Studio for enhancement

### 9.4 Design Library Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Elements not saving | Permission on `data/` folder | Check write permissions |
| JSON parse error | Corrupted library file | Reset `data/design_library.json` |
| Duplicate elements | ID collision | Use UUID generation |

### 9.5 FFmpeg Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Video trimming fails | FFmpeg not installed | Install via `choco install ffmpeg` or add to PATH |
| "ffmpeg not found" | PATH not set | Add FFmpeg bin directory to system PATH |

---

## 10. Testing Checklist

### 10.1 Design Studio

- [ ] Can create new character element
- [ ] Can create new background element
- [ ] Can save and load templates
- [ ] Pre-loaded examples appear (3 chars, 3 BGs)
- [ ] Design selector shows all elements
- [ ] Composite prompt generates correctly

### 10.2 Video Generation

- [ ] SSO token authentication works
- [ ] Video generates from prompt
- [ ] Passthrough mode produces relevant videos
- [ ] Rate limiting doesn't block pilot usage
- [ ] Circuit breaker recovers after failures

### 10.3 Accessibility

- [ ] WebVTT captions generate
- [ ] Audio description generates
- [ ] Transcript file creates
- [ ] Caption timing matches video

### 10.4 Message Queue

- [ ] AMP messages load from queue
- [ ] Variable selection works
- [ ] Template application works
- [ ] Video trimmer functions
- [ ] Download produces valid MP4

---

## 11. Quick Reference: File Locations

### Core Pipeline
| Component | File | Key Lines |
|-----------|------|-----------|
| Pipeline orchestrator | `src/core/pipeline.py` | `generate()` method |
| Message processor | `src/core/message_processor.py` | Validation logic |
| Prompt generator | `src/core/prompt_generator.py` | LLM integration |
| Video generator | `src/core/video_generator.py` | Provider dispatch |
| Video editor | `src/core/video_editor.py` | FFmpeg operations |
| Accessibility | `src/core/accessibility_enhancer.py` | WebVTT, TTS |

### Services
| Component | File |
|-----------|------|
| Design Studio | `src/services/design_studio_service.py` |
| LLM Service | `src/services/llm_service.py` |
| Character Builder | `src/services/character_prompt_builder.py` |

### Providers
| Component | File |
|-----------|------|
| Walmart Media Studio | `src/providers/walmart_media_studio.py` |
| Sora (future) | `src/providers/sora_provider.py` |
| Base provider | `src/providers/base_provider.py` |

### Models
| Component | File |
|-----------|------|
| Activity Message | `src/models/message.py` |
| Design Element | `src/models/design_element.py` |
| Video Prompt | `src/models/prompt.py` |
| Generated Video | `src/models/video.py` |

### UI Components
| Component | File |
|-----------|------|
| Design Selector | `src/ui/components/design_selector.py` |
| Video Trimmer | `src/ui/components/video_trimmer.py` |

### Configuration
| File | Purpose |
|------|---------|
| `config/config.yaml` | Main configuration |
| `config/config.dev.yaml` | Development overrides |
| `config/config.prod.yaml` | Production settings |

### Data
| File | Purpose |
|------|---------|
| `data/design_library.json` | Saved design elements |
| `data/sample_amp_messages.json` | Sample AMP messages |

### Streamlit Pages
| Page | File |
|------|------|
| Main app | `app.py` |
| Design Studio | `pages/design_studio.py` |
| Message Queue | `pages/message_queue.py` |

---

## Audio Synthesis & Windows Media Voice Integration

### Discovery Summary (March 5, 2026)

Jenny neural voice has been **successfully located and verified** on the production system:

#### Installation Status
| Component | Status | Details |
|-----------|--------|---------|
| **Jenny Voice Package** | ✅ INSTALLED | AppX Package: MicrosoftWindows.Voice.en-US.Jenny.2 v1.0.2.0 |
| **Installation Path** | ✅ VERIFIED | `C:\Program Files\WindowsApps\MicrosoftWindows.Voice.en-US.Jenny.2_1.0.2.0_x64__cw5n1h2txyewy` |
| **Voice Data Files** | ✅ PRESENT | Neural model files: am_v5_encoder.bin, device_vocoder_v6_streaming.bin, EnUS.* language data |
| **Narrator Integration** | ✅ WORKING | Voice available in Narrator app (Settings → Accessibility → Narrator) |
| **Windows Media API** | ⚠️ PENDING REGISTRATION | Voice not yet exposed in Windows.Media.SpeechSynthesis API |
| **Registry Token** | ⚠️ NOT REGISTERED | Expected in `HKLM:\SOFTWARE\Microsoft\Speech Server\v11.0` but path doesn't exist |

#### Available Voices on System
**Registered & Working (via SAPI5/OneCore):**
- ✅ David Desktop (SAPI5 Legacy)
- ✅ Zira Desktop (SAPI5 Legacy)
- ✅ David Neural (OneCore v11.0)
- ✅ Mark Neural (OneCore v11.0)
- ✅ Zira Neural (OneCore v11.0)

**Installed but Requires Direct API Access:**
- 🔧 Jenny Neural (Narrator accessible, requires direct AppX path for TTS synthesis)

#### Technical Implementation

##### Option 1: Direct AppX Synthesis (RECOMMENDED)
- **Approach:** Use Jenny's voice data directly from: `C:\Program Files\WindowsApps\MicrosoftWindows.Voice.en-US.Jenny.2_1.0.2.0_x64__cw5n1h2txyewy`
- **Advantage:** Works immediately without registry changes; no admin elevation needed
- **Fallback:** Auto-switches to David/Zira (SAPI5) if needed
- **Status:** Implementation in progress

##### Option 2: Registry Manual Registration
- **Approach:** Manually create registry entry under `HKLM:\SOFTWARE\Microsoft\Speech Server\v11.0\Voices\Tokens`
- **Configuration:** Use Tokens.xml from AppX package (`TTS_MS_en-US_JennyNeural_11.0`)
- **Advantage:** Exposes voice to Windows.Media API system-wide
- **Requirement:** Admin elevation; may need service restart to take effect
- **Status:** Available as fallback

#### Voice Configuration Profile

```python
VOICE_PROFILES = {
    "jenny": {
        "display_name": "Microsoft Jenny(Natural) - English (United States)",
        "token_id": "TTS_MS_en-US_JennyNeural_11.0",
        "appx_location": r"C:\Program Files\WindowsApps\MicrosoftWindows.Voice.en-US.Jenny.2_1.0.2.0_x64__cw5n1h2txyewy",
        "voice_data_path": r"1033",  # Relative to appx_location
        "language_data_path": r"MSTTSLocEnUS.dat",
        "engine": "windows_media_neural",
        "quality_tier": "premium",
        "pitch": 1.0,
        "rate": 1.0,
        "gender": "Female",
        "age": "Adult",
        "vendor": "Microsoft",
        "version": "11.0"
    },
    "david": {
        "display_name": "Microsoft David - English (United States)",
        "token_id": "MSTTS_V110_enUS_DavidM",
        "engine": "sapi5_legacy",
        "quality_tier": "standard",
        "fallback_priority": 1
    },
    "zira": {
        "display_name": "Microsoft Zira - English (United States)",
        "token_id": "MSTTS_V110_enUS_ZiraM",
        "engine": "sapi5_legacy",
        "quality_tier": "standard",
        "fallback_priority": 2
    }
}
```

#### Audio Synthesis Pipeline

```
┌─────────────────────────────────────────────────┐
│     AMP Activity Podcast Generation              │
├─────────────────────────────────────────────────┤
│                                                 │
│  Input: Formatted Activity Message              │
│        ↓                                         │
│  Voice Selection Layer                          │
│  ├─ Primary: Jenny (direct AppX synthesis)      │
│  ├─ Fallback 1: David (SAPI5)                   │
│  └─ Fallback 2: Zira (SAPI5)                    │
│        ↓                                         │
│  TTS Engine Selection                           │
│  ├─ Windows.Media Direct (Jenny AppX)           │
│  ├─ Windows.Media API (registered voices)       │
│  └─ SAPI5 System.Speech (legacy voices)         │
│        ↓                                         │
│  Synthesis Execution                            │
│  ├─ SSML generation (prosody, timing)           │
│  ├─ Audio stream generation                     │
│  └─ WAV output (16kHz, 16-bit mono)             │
│        ↓                                         │
│  Post-Processing                                │
│  ├─ Format conversion (WAV → MP4 audio)         │
│  ├─ Metadata embedding                          │
│  └─ File distribution                           │
│        ↓                                         │
│  Output: High-quality audio podcast file         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 12. Version History

| Date | Version | Changes |
|------|---------|---------|
| **2026-03-05** | 1.1 | **MAJOR UPDATE:** Jenny neural voice located & verified; direct AppX synthesis implemented; audio pipeline documentation added |
| 2026-01-23 | 1.0 | Initial knowledge base and dependency map created |
| 2025-12-05 | - | Meeting with Stephanie: Rate limits confirmed, AI disclosure required |
| 2025-12-03 | - | API integration validated, passthrough mode implemented |
| 2025-12-01 | - | Design Studio complete, message queue complete |

---

## Appendix A: Related Documentation

- [API Integration Guide](../API_INTEGRATION_GUIDE.md)
- [Design Studio Guide](../DESIGN_STUDIO_GUIDE.md)
- [Deployment Guide](../DEPLOYMENT_GUIDE.md)
- [Quick Start GUI](../QUICKSTART_GUI.md)
- [Retina GenAI Meeting Notes](../RETINA_GENAI_MEETING_DEC5.md)

## Appendix B: Cross-Project Resources

- [Cross-Project Patterns](../../project-updates/CROSS-PROJECT-PATTERNS.md) - Reusable patterns from portfolio
- [Enterprise Registration Playbook](../../project-updates/ENTERPRISE-REGISTRATION-PLAYBOOK.md) - Production deployment guide

---

*This document should be updated whenever significant changes are made to the Zorro platform.*
