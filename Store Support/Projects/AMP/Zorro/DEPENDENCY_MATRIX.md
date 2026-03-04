# Zorro Project - Detailed Dependency Matrix
**Generated:** March 3, 2026

---

## Overview

This document provides a detailed mapping of all dependencies (Python packages, system tools, external services) across the Zorro project's components.

---

## Python Package Dependencies by Component

### 1. Core Pipeline (`src/core/`)

#### pipeline.py
```
Dependencies:
  ✅ pydantic           (Data validation)
  ✅ pydantic-settings  (Configuration)
  ❌ streamlit          (UI rendering)
  ❌ moviepy            (Video editing)
  ❌ openai             (LLM integration)
  ❌ anthropic          (LLM fallback)
  ⚠️ passthrough_mode   (Internal)
```

#### message_processor.py
```
Dependencies:
  ✅ pydantic           (Validation)
  ✅ re                 (Regex - stdlib)
  ✅ json               (stdlib)
  ❌ validators         (Field validation)
```

#### prompt_generator.py
```
Dependencies:
  ✅ pydantic           (Models)
  ❌ openai             (GPT-4 calls)
  ❌ anthropic          (Claude calls)
  ⚠️ passthrough_mode   (Skip LLM)
  ❌ tenacity           (Retry logic)
```

#### video_generator.py
```
Dependencies:
  ✅ pydantic           (Models)
  ❌ requests           (HTTP calls)
  ❌ urllib3            (Connection pooling)
  ⚠️ walmart_media_studio (Provider)
  ⚠️ circuit_breaker    (Resilience)
  ❌ tenacity           (Retries)
```

#### video_editor.py
```
Dependencies:
  ❌ moviepy            (Video editing - CRITICAL)
  ❌ opencv             (Image processing)
  ❌ ffmpeg             (System tool - CRITICAL)
  ❌ pillow             (Image library)
```

#### accessibility_enhancer.py
```
Dependencies:
  ❌ webvtt-py          (Caption format)
  ❌ srt                (Subtitle format)
  ❌ gTTS               (Text-to-speech - CRITICAL)
  ❌ pyttsx3            (Windows TTS - CRITICAL)
  ✅ json               (Transcript output - stdlib)
```

---

### 2. Services (`src/services/`)

#### design_studio_service.py
```
Dependencies:
  ✅ pydantic           (Models)
  ✅ json               (File I/O - stdlib)
  ✅ pathlib            (Path handling - stdlib)
  ✅ uuid               (ID generation - stdlib)
  ❌ structlog          (Logging)
```

#### llm_service.py
```
Dependencies:
  ❌ openai             (OpenAI API)
  ❌ anthropic          (Anthropic API)
  ✅ pydantic           (Models)
  ❌ tenacity           (Retry with backoff)
  ⚠️ passthrough_mode   (Skip LLM)
```

#### character_prompt_builder.py
```
Dependencies:
  ✅ pydantic           (Models)
  ✅ json               (stdlib)
```

---

### 3. Providers (`src/providers/`)

#### walmart_media_studio.py
```
Dependencies:
  ❌ requests           (HTTP client - CRITICAL)
  ❌ urllib3            (Connection management)
  ✅ json               (Serialization - stdlib)
  ✅ time               (Polling delays - stdlib)
  ⚠️ circuit_breaker    (Resilience pattern)
  ⚠️ rate_limiter       (Request limiting)
  ✅ ssl_config.py      (SSL verification)
  ❌ tenacity           (Retry logic)
```

#### sora_provider.py (Future)
```
Dependencies:
  ❌ openai             (Sora 2 API)
  ❌ requests           (HTTP calls)
```

#### base_provider.py
```
Dependencies:
  ✅ abc                (Abstract base - stdlib)
  ✅ pydantic           (Models)
```

---

### 4. Web UI (`src/ui/`)

#### Design Selector Component
```
Dependencies:
  ❌ streamlit          (UI framework - CRITICAL)
  ✅ pydantic           (Models)
  ⚠️ design_studio_service (Service)
```

#### Video Trimmer Component
```
Dependencies:
  ❌ streamlit          (UI - CRITICAL)
  ❌ moviepy            (Video trimming - CRITICAL)
  ❌ ffmpeg             (System tool - CRITICAL)
  ✅ json               (File handling - stdlib)
```

---

### 5. Data Models (`src/models/`)

#### All Model Files
```
Dependencies:
  ✅ pydantic           (Base validation)
  ✅ enum               (Type enums - stdlib)
  ✅ datetime           (Timestamps - stdlib)
  ✅ typing             (Type hints - stdlib)
  ❌ jsonschema         (Schema validation)
```

---

### 6. Main Application (`app.py`)

```
Dependencies:
  ❌ streamlit          (Web UI - CRITICAL)
  ✅ pydantic           (Models)
  ❌ requests           (API calls)
  ⚠️ pipeline.py        (Core logic)
  ⚠️ design_studio_service (Services)
  ✅ json               (stdlib)
  ✅ pathlib            (stdlib)
```

---

### 7. Streamlit Pages

#### pages/design_studio.py
```
Dependencies:
  ❌ streamlit          (UI - CRITICAL)
  ⚠️ design_studio_service (CRUD operations)
  ⚠️ design_selector.py (UI component)
  ✅ json               (stdlib)
```

#### pages/message_queue.py
```
Dependencies:
  ❌ streamlit          (UI - CRITICAL)
  ⚠️ pipeline.py        (Video generation)
  ⚠️ video_trimmer.py   (Trimming UI)
  ✅ json               (stdlib)
```

---

## System Tool Dependencies

| Tool | Used By | Purpose | Status | Install |
|------|---------|---------|--------|---------|
| **FFmpeg** | moviepy, video_editor | Video trimming, conversion | ❌ Missing | `choco install ffmpeg` |
| **Python 3.9+** | All | Runtime | ✅ 3.14.3 installed | Already have |
| **pip** | Package management | Dependency installation | ✅ 25.3 | Already have |

---

## External Service Dependencies

| Service | Used By | Purpose | Auth Method | Rate Limit |
|---------|---------|---------|-------------|-----------|
| **Walmart Media Studio API** | walmart_media_studio.py | Video generation (Veo) | SSO Token | 10 req/min, 100 req/hour |
| **OpenAI API** | llm_service.py | Prompt enhancement | API Key | Model-dependent |
| **Anthropic API** | llm_service.py | LLM fallback | API Key | Model-dependent |
| **Google TTS** | accessibility_enhancer.py | Text-to-speech | None/Quota | Daily quota |

---

## Database Dependencies (Phase 2)

| Package | Purpose | Version | Status |
|---------|---------|---------|--------|
| **sqlalchemy** | ORM | 2.0.0+ | ❌ Not installed |
| **psycopg2-binary** | PostgreSQL driver | 2.9.9+ | ❌ Not installed |
| **alembic** | Migrations | 1.13.0+ | ❌ Not installed |
| **redis** | Cache/Queue | 5.0.0+ | ❌ Not installed |
| **celery** | Async tasks | 5.3.0+ | ❌ Not installed |

**Note:** Only needed for Phase 2+ scaling

---

## Complete Package List with Status

### ✅ Already Installed (32 packages)

```
Core Dependencies:
  ✅ pydantic (2.12.5)
  ✅ pydantic_core (2.41.5)
  ✅ python-dotenv (1.0.0)
  ✅ PyYAML (6.0.3)
  ✅ click (8.3.1)
  ✅ requests (2.32.5)
  ✅ cryptography (46.0.5)

Data/Numerical:
  ✅ numpy (2.4.2)
  ✅ pandas (3.0.1)
  ✅ protobuf (6.33.5)

Web Frameworks:
  ✅ fastapi (0.109.0)
  ✅ starlette (0.35.1)
  ✅ uvicorn (0.27.0)
  ✅ httpx (0.28.1)
  ✅ websockets (16.0)

LLM Services:
  ✅ openai (1.10.0)

Google Cloud:
  ✅ google-cloud-bigquery (3.14.1)
  ✅ google-auth (2.27.0)

Utilities:
  ✅ python-dateutil (2.9.0.post0)
  ✅ tqdm (4.67.3)
  ✅ watchfiles (1.1.1)
  ✅ colorama (0.4.6)
  ✅ packaging (26.0)
  ✅ certifi (2026.1.4)
  ✅ pywin32 (311)
  ✅ urllib3 (2.6.3)
  ✅ six (1.17.0)
```

### ❌ Critical Missing (20+ packages)

```
Web UI:
  ❌ streamlit (1.29.0+)

ML/AI Libraries:
  ❌ torch (2.1.0+)
  ❌ diffusers (0.24.0+)
  ❌ transformers (4.35.0+)
  ❌ accelerate (0.25.0+)
  ❌ anthropic (0.7.0+)

Video Processing:
  ❌ moviepy (1.0.3+)
  ❌ opencv-python (4.8.1.78+)
  ❌ pillow (10.1.0+)
  ❌ imageio (2.33.0+)
  ❌ imageio-ffmpeg (0.4.9+)

Audio Processing:
  ❌ pydub (0.25.1+)
  ❌ gTTS (2.4.0+)
  ❌ pyttsx3 (2.90+)

Subtitles/Captions:
  ❌ webvtt-py (0.4.6+)
  ❌ srt (3.5.3+)

Security/Compliance:
  ❌ bleach (6.1.0+)
  ❌ azure-identity (1.15.0+)
  ❌ azure-keyvault-secrets (4.7.0+)

Validation/Logging:
  ❌ validators (0.22.0+)
  ❌ jsonschema (4.20.0+)
  ❌ structlog (23.2.0+)
  ❌ python-json-logger (2.0.7+)
  ❌ tenacity (8.2.3+)
```

### ⚠️ Phase 2 Only (Not Blocking)

```
  ❌ sqlalchemy (2.0.0+)
  ❌ psycopg2-binary (2.9.9+)
  ❌ alembic (1.13.0+)
  ❌ redis (5.0.0+)
  ❌ celery (5.3.0+)
```

---

## Installation Dependency Order

### Phase 1: Core (Must Have)
```powershell
pip install streamlit                    # Web UI
pip install torch                        # ML runtime
pip install transformers diffusers       # Model libraries
pip install moviepy opencv-python        # Video processing
pip install pydub gTTS pyttsx3           # Audio processing
pip install requests                     # HTTP client
```

### Phase 2: Accessibility & Validation
```powershell
pip install webvtt-py srt                # Caption formats
pip install validators jsonschema        # Validation
pip install bleach                       # Sanitization
pip install tenacity                     # Retry logic
pip install structlog python-json-logger # Logging
```

### Phase 3: Security & Azure (If Using)
```powershell
pip install azure-identity azure-keyvault-secrets
```

### Phase 4: Database (Phase 2 scaling)
```powershell
pip install sqlalchemy psycopg2-binary alembic
pip install redis celery
```

---

## Dependency Risk Assessment

| Risk Level | Package | Reason | Mitigation |
|------------|---------|--------|-----------|
| 🔴 CRITICAL | Streamlit | Web UI won't work without it | Install immediately |
| 🔴 CRITICAL | PyTorch | ML inference won't work | Install immediately |
| 🔴 CRITICAL | FFmpeg | Video trimming required | Install system tool |
| 🟠 HIGH | MoviePy | Video editing won't work | Install immediately |
| 🟠 HIGH | gTTS/pyttsx3 | Accessibility broken | Install immediately |
| 🟠 HIGH | requests | API calls fail | Already installed ✅ |
| 🟡 MEDIUM | WebVTT/SRT | Captions won't work | Install for accessibility |
| 🟡 MEDIUM | Azure SDK | Cloud auth fails | Install if using Azure |
| 🟢 LOW | Tenacity | Retries less resilient | Should install |
| 🟢 LOW | Structlog | Logging less structured | Nice-to-have |

---

## Minimum Viable Setup

To get **basic application running** (MVP):

```powershell
# Required
pip install streamlit pydantic requests

# For video generation
pip install torch diffusers transformers

# For editing
pip install moviepy opencv-python pillow

# For audio
pip install pydub gTTS

# System tool
choco install ffmpeg
```

**Result:** Can generate and edit basic videos, no accessibility features yet

**Time to MVp:** ~1 hour (with network access)

---

## Full Production Setup

To get **all features working**:

```powershell
pip install -r requirements.txt
choco install ffmpeg
# Plus: API keys from Retina team
```

**Result:** All features working, production-ready

**Time:** ~2 hours (with network access)

---

## Dependency Compatibility Notes

### Python Version
- **Required:** 3.9+ (currently running 3.14.3) ✅
- **Note:** PyTorch recommends 3.9-3.11 for stability, but 3.14 should work

### Important Compatibility
```
PyTorch + CUDA: CPU-only version used (no GPU available)
OpenAI + Pydantic: Uses v1 compatibility mode (warning in logs)
Streamlit + Pandas: Compatible, no issues expected
```

### Known Issues
- OpenAI library warns about Python 3.14 compatibility (not blocking)
- Some ML packages have large disk requirements (20+ GB)

---

## Disk Space Requirements

| Component | Size |
|-----------|------|
| Python packages (all) | ~5-8 GB |
| PyTorch models (downloaded on first use) | ~2-3 GB |
| Generated videos (temp) | Variable |
| **TOTAL** | **~10-15 GB** |

**Recommendation:** Ensure at least 20 GB free disk space

---

## Next Steps

### 1. Network Access (CRITICAL BLOCKER)
- Contact IT for PyPI access
- Test: `pip install pytest` (lightweight package)

### 2. Install Core Stack
```powershell
pip install streamlit torch diffusers transformers moviepy
```

### 3. Verify
```powershell
python verify_setup.py
```

### 4. Launch
```powershell
streamlit run app.py
```

---

**Document Version:** 1.0  
**Last Updated:** March 3, 2026  
**Status:** Ready for Reference
