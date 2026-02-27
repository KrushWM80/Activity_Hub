# Retina GenAI Team Meeting - December 5, 2025

## Meeting Agenda: Zorro Video Generation Platform Progress Update

---

## Executive Summary

### Current State: ✅ PRODUCTION READY (Phase 1 MVP)

| Component | Status | Details |
|-----------|--------|---------|
| **Design Studio** | ✅ Complete | Characters, backgrounds, templates, brand assets |
| **Message Queue** | ✅ Complete | AMP message workflow with variable selection |
| **Video Generation** | ✅ Complete | Walmart Media Studio API integration working |
| **Video Trimmer** | ✅ Complete | FFmpeg-based trim and download |
| **Accessibility** | ✅ Complete | Captions, audio descriptions, transcripts |
| **AI Disclosure** | 🔴 Pending | Legal requires watermark/text (new requirement) |

### Meeting Outcome (Dec 5, 2025)

Met with **Stephanie** from Retina GenAI team:
- ✅ **Rate Limits**: Not a concern for our use case
- ✅ **Chargebacks**: No cost model currently
- ✅ **Concurrent Users**: 2 users confirmed OK
- 🔴 **Legal Requirement**: Must add AI-generated content disclosure

### Roadmap

| Phase | Timeline | Focus | Status |
|-------|----------|-------|--------|
| **Pilot** | Dec 2025 | 1-5 videos/week, 2 users | ✅ Ready |
| **Phase 1** | Jan 2026 | 10-25 videos/week, add AI watermark | 🔄 Next |
| **Phase 2** | Feb 2026 | 50-100 videos/week, batch processing | Planned |
| **Phase 3** | Q2 2026 | 100-150 videos/week, scale to 10+ users | Planned |
| **Production** | Q3 2026 | 150-200+ videos/week, full rollout | Planned |

### Next Steps (Immediate)

| Priority | Task | Owner | Target |
|----------|------|-------|--------|
| 🔴 High | Implement AI disclosure watermark/text | Robert | Dec 12 |
| 🟡 Medium | User acceptance testing with pilot group | Robert | Dec 15 |
| 🟡 Medium | Documentation for end users | Robert | Dec 20 |
| 🟢 Low | Batch processing mode | Robert | Jan 2026 |

---

## The Vision
**Streamline production of professional video content for 4,700+ facilities** by converting operational AMP (Activity Message Platform) messages into engaging, brand-consistent videos.

### Target Users
**Business Managers** who need to:
1. Create reusable design elements (characters, backgrounds, brand assets)
2. Rapidly process queued AMP messages into videos
3. Download/embed videos in field communications

### Workflow (NOW COMPLETE ✅)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     DESIGN STUDIO (One-Time Setup) ✅                │
├─────────────────────────────────────────────────────────────────────┤
│  1. Create Characters     → Friendly mascot, associate avatars      │
│  2. Create Backgrounds    → Store aisle, break room, warehouse      │
│  3. Define Brand Elements → Walmart colors, fonts, logos            │
│  4. Save as Templates     → "Safety Video", "Training Announcement" │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION QUEUE (Daily Operations) ✅            │
├─────────────────────────────────────────────────────────────────────┤
│  1. AMP Messages Queue    → Incoming operational messages            │
│  2. Select Message        → "Complete safety training by Friday"     │
│  3. Choose Template       → "Safety Video" template                  │
│  4. Select Variables      → Character: Safety Sam, BG: Training Room │
│  5. Generate Video        → 5-8 second branded video                 │
│  6. Trim & Download       → Quick edit, export MP4                   │
│  7. Embed in Comms        → Ready for field distribution             │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         FIELD DISTRIBUTION                           │
├─────────────────────────────────────────────────────────────────────┤
│  → 4,700+ facilities receive consistent, professional video content │
│  → Accessibility: Captions, audio descriptions, transcripts         │
│  → Brand consistency across all locations                           │
└─────────────────────────────────────────────────────────────────────┘
```

### Scale Requirements
| Metric | Current State | Production Goal |
|--------|---------------|-----------------|
| Videos/Week | 1-5 (pilot ready) | 100-150+ |
| Processing Time | ~1-2 min/video | <1 min/video |
| Queue Capacity | Single + Queue UI | Batch processing |
| Facilities Served | Testing | 4,700+ |

---

## 1. 🎉 Progress Update - Great News!

### Integration Status: WORKING ✅

| Component | Status | Notes |
|-----------|--------|-------|
| API Connectivity | ✅ Working | `retina-ds-genai-backend.prod.k8s.walmart.net` |
| Video Generation | ✅ Working | Successfully generating videos from prompts |
| Authentication | ✅ Working | SSO token authentication implemented |
| Model Access | ✅ Working | veo2, veo3, imagen-4.0 accessible |
| Passthrough Mode | ✅ NEW | Bypasses external LLM, uses Media Studio's AI |

### Recent Fix: Prompt Relevance Issue Resolved
- **Problem**: Videos weren't matching user prompts
- **Root Cause**: External LLM (OpenAI) blocked by Walmart VPN
- **Solution**: Implemented "passthrough mode" - sends user prompts directly to Media Studio's `enhanced_prompt: true` feature
- **Result**: Videos now accurately reflect user intent!

---

## 2. Current Architecture

```
User Input (Design Studio UI)
    ↓
Zorro Streamlit App
    ↓
Prompt Generator (Passthrough Mode)
    ↓ [No external LLM needed]
Walmart Media Studio API
    ↓ [enhanced_prompt: true]
Google Veo Model (veo2/veo3)
    ↓
Generated Video → User
```

### Key Technical Details
- **API Endpoint**: `https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1`
- **Video Duration**: 5-8 seconds (API constraint)
- **Aspect Ratios**: 16:9, 9:16, 1:1
- **Models**: veo2 (stable), veo3 (latest)
- **Negative Prompts**: Supported and being used to improve output quality

---

## 3. 🔧 Work Remaining on My Side

### Design Studio (Element Creation)
| Task | Priority | Status |
|------|----------|--------|
| Character creator UI | High | ✅ Complete |
| Background library | High | ✅ Complete |
| Template save/load | High | ✅ Complete |
| Brand asset management | Medium | ✅ Complete |
| Pre-loaded example designs | High | ✅ Complete (3 chars, 3 BGs) |

### Production Queue (Message Processing)
| Task | Priority | Status |
|------|----------|--------|
| AMP message queue integration | High | ✅ Complete |
| Variable selector (char + BG) | High | ✅ Complete |
| Video trimming tool | Medium | ✅ Complete |
| Download/export functionality | Medium | ✅ Complete |
| Batch processing mode | Low | Future |

### Prompt Engineering & Quality
| Task | Priority | Status |
|------|----------|--------|
| Prompt fine-tuning | High | ✅ Complete |
| Negative prompt optimization | Medium | ✅ Complete |
| Template library expansion | Medium | ✅ Complete |
| Retail scene consistency | High | ✅ Complete |
| Composite prompt validation fix | High | ✅ Complete |

### Accessibility Layer
| Task | Priority | Status |
|------|----------|--------|
| Auto-captions (WebVTT) | Medium | ✅ Complete |
| Audio descriptions | Medium | ✅ Complete |
| Transcript generation | Low | ✅ Complete |

---

## 4. ❓ Questions for the Retina Team

### A. Rate Limits & Quotas

**Current Understanding:**
- Config shows: 10 requests/minute, 100 requests/hour
- Concurrent generations: 2-5 max

**Questions:**
1. What are the **actual production rate limits** for the API?
2. Are there **daily/weekly/monthly quotas** we need to be aware of?
3. Is there a **fair usage policy** or priority queue for enterprise users?
4. What's the **maximum concurrent requests** supported?

---

### B. Scaling Plan - Production Rollout

**Current Pilot Plan:**
- Phase 1: 1 video/week (approved for Dec)
- Phase 2: 5-10 videos/week
- Phase 3: 50-100 videos/week
- Phase 4: 100-150 videos/week

**Scaling Questions:**
1. What's the process to **request increased quotas**?
2. Do you need **business justification** for scale-up?
3. Are there **SLAs** for high-volume enterprise use cases?
4. What **lead time** is needed to increase capacity?
5. Is there a **dedicated queue or priority lane** for approved enterprise projects?

---

### C. Cost Implications

**Questions:**
1. Is there a **chargeback model** for API usage?
2. If so, what's the **cost per video generation**?
3. Are there **cost differences** between veo2 vs veo3?
4. Any **bulk pricing** for high-volume use cases?

---

### D. Technical Capabilities

**Current Observations:**
- `enhanced_prompt: true` works well for prompt enhancement
- Negative prompts help but don't fully prevent background bleeding

**Questions:**
1. Is there a way to **specify scene types** more explicitly (e.g., "retail store only")?
2. Can we provide **reference images** for scene consistency?
3. Are there **style presets** or templates optimized for retail environments?
4. What **prompt best practices** does the team recommend?
5. Any upcoming **model improvements** that might help with scene consistency?

---

### E. API Improvements / Roadmap

**Questions:**
1. Are there **new features** coming to the API?
2. Any plans for **longer video duration** (beyond 8 seconds)?
3. Will there be **video-to-video** or **image-to-video** capabilities?
4. Any **fine-tuning options** for Walmart-specific content?

---

### F. Monitoring & Debugging

**Questions:**
1. Is there a **dashboard** to view our API usage/quota?
2. Can we access **logs** for troubleshooting failed generations?
3. Are there **webhook notifications** for job completion?
4. What's the **typical generation time** we should expect?

---

## 5. Production Scaling Proposal

### Business Case Summary

**Use Case**: Convert AMP (Activity Message Platform) operational messages into professional, brand-consistent video content for cascading to 4,700+ facilities.

**Workflow Overview**:
1. **Design Studio** (One-time setup): Business managers create reusable elements
   - Characters (mascots, associate avatars)
   - Backgrounds (store, warehouse, break room scenes)
   - Brand templates with preset styling
   
2. **Production Queue** (Daily operations): Fast, efficient message processing
   - Select AMP message from queue
   - Choose character + background variables
   - Generate video (5-8 seconds)
   - Trim, download, embed in field communications

**Target Volume** (End State):
| Metric | Current | 6-Month Goal | 12-Month Goal |
|--------|---------|--------------|---------------|
| Videos/Week | 1 (pilot) | 50-100 | 150-200 |
| Concurrent Users | 1-2 | 10-20 | 50+ |
| Categories | 5 | 10+ | 20+ |
| Facilities Reached | Testing | 2,000+ | 4,700+ |

**Business Value**:
- **Consistency**: Same professional quality across 4,700+ locations
- **Speed**: Hours → Minutes to create video content
- **Efficiency**: Reusable templates, batch processing capability
- **Accessibility**: Built-in captions, audio descriptions, transcripts
- **Engagement**: Video content improves message retention vs text

### Requested API Capacity

| Phase | Timeline | Videos/Week | Concurrent | Priority |
|-------|----------|-------------|------------|----------|
| Pilot | Dec 2025 | 1-5 | 2 | Low |
| Phase 1 | Jan 2026 | 10-25 | 3 | Medium |
| Phase 2 | Feb 2026 | 50-100 | 5 | Medium |
| Phase 3 | Q2 2026 | 100-150 | 10 | High |
| Production | Q3 2026 | 150-200+ | 10+ | High |

---

## 6. Demo Ready

If helpful, I can demonstrate:
1. ✅ Design Studio UI with template selection (COMPLETE)
2. ✅ Live video generation from prompt (COMPLETE)
3. ✅ Passthrough mode working (prompts → relevant videos) (COMPLETE)
4. ✅ Negative prompt effectiveness (COMPLETE)
5. ✅ AMP Message Queue workflow (NEW - COMPLETE)
6. ✅ Video trimmer with FFmpeg integration (NEW - COMPLETE)
7. ✅ Pre-loaded characters and backgrounds (NEW - COMPLETE)

---

## 7. Action Items from This Meeting

| Item | Owner | Due Date | Status |
|------|-------|----------|--------|
| ~~Confirm rate limits~~ | Retina Team | | ✅ Not a concern for our use case |
| ~~Provide scaling request process~~ | Retina Team | | ✅ Not needed currently |
| Share prompt best practices | Retina Team | | Pending |
| ~~Submit capacity increase request~~ | Robert | | ✅ Not needed - 2 concurrent users OK |
| ~~Continue prompt engineering~~ | Robert | Ongoing | ✅ Complete |
| ~~Complete UI improvements~~ | Robert | Dec 15 | ✅ Complete |
| ~~Design Studio characters/BGs~~ | Robert | Dec 10 | ✅ Complete |
| ~~Message Queue workflow~~ | Robert | Dec 10 | ✅ Complete |
| ~~Video trimmer tool~~ | Robert | Dec 12 | ✅ Complete |
| **AI Disclosure watermark/text** | Robert | TBD | 🔴 NEW - Legal requirement |

---

## 9. Meeting Outcome - Key Takeaways (Dec 5, 2025)

### Meeting with Stephanie - Summary

| Topic | Outcome |
|-------|---------|
| **Rate Limits** | ✅ Not a concern for our use case - no limits expected to be hit |
| **Chargebacks** | ✅ No chargeback model currently in place |
| **Concurrent Users** | ✅ 2 concurrent users is not an issue |
| **Legal Requirement** | 🔴 **ACTION NEEDED**: Videos must include watermark or accompanying text identifying content as AI-generated |

### New Action Item: AI Disclosure

**Legal Requirement**: All AI-generated videos must be clearly identified as such.

**Options to implement:**
1. **Video Watermark** - Overlay text on video (e.g., "AI Generated Content")
2. **Accompanying Text** - Require disclosure text when video is distributed
3. **Both** - Watermark + text for maximum compliance

**Recommended Implementation:**
- Add optional watermark toggle in video generation settings
- Default to ON for compliance
- Text options: "AI Generated", "Created with AI", "AI-Assisted Content"
- Position: Bottom-right corner, semi-transparent

---

## 10. Contact & Resources

- **Project**: Zorro Video Generator
- **Slack**: #help-genai-media-studio
- **API Docs**: [API Integration Guide](./API_INTEGRATION_GUIDE.md)
- **Design Studio**: [Design Studio Guide](./DESIGN_STUDIO_GUIDE.md)

---

## Appendix: Current Configuration

```yaml
# From config/config.yaml
performance:
  max_concurrent_generations: 2
  rate_limit:
    requests_per_minute: 10
    requests_per_hour: 100

video:
  generator:
    provider: "walmart_media_studio"
    model_name: "veo"
    walmart_media_studio:
      timeout: 300  # seconds
      max_retries: 3
      poll_interval: 5
```

---

**Meeting Date**: December 5, 2025  
**Prepared By**: Robert Isaacs  
**Project**: Zorro AI Video Generator
