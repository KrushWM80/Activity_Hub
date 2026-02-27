# Zorro AI Video Generation - Stakeholder Meeting
## AMP Message to Video Pipeline

**Date:** January 23, 2026  
**Prepared By:** Robert Isaacs  
**Purpose:** Clarify business requirements and demonstrate AI video generation capabilities

---

## 📋 Executive Summary

**Zorro** converts **AMP (Activity Message Platform) messages** into professional, brand-consistent video content for distribution to **4,700+ Walmart facilities**.

| Component | Status | Ready for Demo |
|-----------|--------|----------------|
| **Video Generation** | ✅ Working | YES - Today |
| **AMP Data Integration** | ✅ Framework Ready | Spark-Playground BigQuery connection |
| **Design Studio** | ✅ Complete | Characters, backgrounds, templates |
| **Accessibility** | ✅ Complete | Captions, transcripts |
| **Audio in Video** | 🟡 In Progress | See Audio Section below |

---

## 🔍 Project Health Assessment (Wibey Review - Jan 23, 2026)

**Overall Rating:** ⭐⭐⭐⭐ (4.2/5) - **Excellent with room for optimization**

| Category | Rating | Notes |
|----------|--------|-------|
| **Architecture** | ⭐⭐⭐⭐⭐ | Excellent separation of concerns |
| **Code Quality** | ⭐⭐⭐⭐ | Type hints, error handling, logging |
| **Documentation** | ⭐⭐⭐⭐ | Multiple guides, architecture diagrams |
| **Testing** | ⭐⭐⭐⭐ | 70%+ coverage, unit + integration tests |
| **Accessibility** | ⭐⭐⭐⭐⭐ | WCAG AAA designed in |
| **Compliance** | ⭐⭐ | **Needs 4-week remediation sprint** |

### ⚠️ Compliance Status: 18% → Target 95%

**5 Critical Issues (Blocking Enterprise Deployment):**

| Issue | Urgency | Effort | Owner |
|-------|---------|--------|-------|
| Exposed API key in .env | **TODAY** | 1 hour | Security |
| SSL verification disabled | Week 1 | 2-3 hours | Backend |
| No audit logging to SIEM | Week 1 | 6-8 hours | DevOps |
| No role-based access control | Week 1-2 | 12 hours | Backend |
| No data retention policy | Week 3 | 4-5 hours | Backend |

**Total Compliance Effort:** 65 hours over 4 weeks

### ✨ Performance Improvements Identified

| Improvement | Effort | Impact |
|-------------|--------|--------|
| Lazy-load pipeline components | 2 hours | 40% faster startup |
| Add caching for repeated messages | 3 hours | 80% faster for repeats |
| Progress tracking UI | 2 hours | Better user experience |
| Error recovery UI with solutions | 2 hours | Fewer support requests |

**Total Improvement Effort:** 24 hours (can run parallel to compliance)

---

## 🎬 Live Demo Available

### ✅ Demo Status: WORKING (Jan 23, 2026 12:55 PM)

**Verified Working:**
- Video generation: ✅ ~37 seconds per video
- SSL fix applied: `WALMART_SSL_VERIFY=false`
- Demo mode: ❌ Disabled (using real API)
- API Response: `status: 200`, `request_id` generated

### Quick Demo Command
```bash
$env:WALMART_SSL_VERIFY = "false"; streamlit run app.py --server.port 8502
```
**URL:** http://localhost:8502

### Demo Flow
1. Enter any AMP-style message (e.g., "Complete your safety training by Friday")
2. Select character and background from Design Studio
3. Click "Generate Video"
4. Video ready in ~37 seconds
5. Download MP4 + captions

### Recent Successful Generations
| Video ID | Duration | Size | Time |
|----------|----------|------|------|
| vid_3ecdd1cef521 | 5s | 1.37 MB | 39s |
| vid_4e77b01438ba | 5s | 1.71 MB | 38s |
| vid_9ef40c09e9a2 | 8s | 2.78 MB | 39s |

---

## 🔗 AMP → Video Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AMP MESSAGE TO VIDEO PIPELINE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   DATA SOURCE (Spark-Playground)          VIDEO GENERATION (Zorro)           │
│   ┌─────────────────────────────┐        ┌─────────────────────────────┐    │
│   │ AMP BigQuery Table          │        │                             │    │
│   │ ─────────────────────────── │        │  1. Message Processor       │    │
│   │ • message_title             │───────►│     - Validate content      │    │
│   │ • message_description       │        │     - Expand abbreviations  │    │
│   │ • business_area             │        │                             │    │
│   │ • priority_level            │        │  2. Prompt Generator        │    │
│   │ • store_number              │        │     - Build video prompt    │    │
│   │ • WM_WEEK_NBR               │        │     - Apply design template │    │
│   │ • SUBDIV_NAME               │        │                             │    │
│   │ • 311 total fields mapped   │        │  3. Video Generator         │    │
│   └─────────────────────────────┘        │     - Walmart Media Studio  │    │
│                                          │     - Google Veo models     │    │
│   Source Table:                          │                             │    │
│   wmt-edw-prod.WW_SOA_DL_VM.             │  4. Accessibility Layer     │    │
│   STORE_OPS_APPLN_ACTV_MGMT_             │     - WebVTT captions       │    │
│   PLAN_MSG_EVENT                         │     - Transcripts           │    │
│                                          │     - Audio description     │    │
│                                          └─────────────────────────────┘    │
│                                                       │                      │
│                                                       ▼                      │
│                                          ┌─────────────────────────────┐    │
│                                          │     OUTPUT                   │    │
│                                          │  • 5-8 second MP4 video     │    │
│                                          │  • WebVTT caption file      │    │
│                                          │  • Transcript text          │    │
│                                          │  • Audio description (MP3)  │    │
│                                          └─────────────────────────────┘    │
│                                                       │                      │
│                                                       ▼                      │
│                                              4,700+ Facilities               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔊 Audio Capabilities - Current State

### What's Available Now

| Feature | Status | Details |
|---------|--------|---------|
| **Silent video generation** | ✅ Working | Walmart Media Studio (Veo) output |
| **WebVTT captions** | ✅ Working | Auto-generated from message text |
| **Text-to-Speech (TTS)** | ✅ Implemented | gTTS generates MP3 audio description |
| **Transcript files** | ✅ Working | Text file with full narration |

### What's NOT Available Yet

| Feature | Status | Timeline | Notes |
|---------|--------|----------|-------|
| **Audio embedded IN video** | 🟡 In Progress | 2-3 weeks | Requires FFmpeg merge step |
| **Native audio from API** | ❌ Not Available | N/A | Veo generates silent videos only |
| **Professional voiceover** | ❌ Not Planned | TBD | Would require external service |

### Recommended Answer for Stakeholders

> **"The Walmart Media Studio API generates silent videos. We have text-to-speech implemented that creates audio files. Merging audio into the final video is a 2-3 week implementation using FFmpeg post-processing. For the pilot phase, we recommend silent videos with captions, which are actually preferred for accessibility compliance."**

### Audio Workaround for Pilot

1. Generate silent video (✅ works now)
2. Generate TTS audio file (✅ works now)
3. User can manually add audio in PowerPoint/video editor if needed
4. OR: Wait 2-3 weeks for automated audio merge

---

## ❓ Questions to Clarify with Stakeholders

### 1. Message Scope
- [ ] Which AMP message **types** should be converted? (Training, Safety, Operations, Announcements, All?)
- [ ] Which **business areas** are priority? (15+ distinct areas in AMP)
- [ ] Filter by **priority level**? (High priority only, or all?)

### 2. Target Audience
- [ ] Which **stores/subdivisions**? (All 4,700+ or specific regions?)
- [ ] Which **user roles** will create videos? (Business Managers, Ops Coordinators?)
- [ ] How many **concurrent users** expected? (Current approval: 2)

### 3. Volume & Scale
| Phase | Proposed Volume | Timeline |
|-------|-----------------|----------|
| Pilot | 1-5 videos/week | Now - Feb 2026 |
| Phase 1 | 10-25 videos/week | Feb 2026 |
| Phase 2 | 50-100 videos/week | Mar 2026 |
| Production | 150-200 videos/week | Q3 2026 |

- [ ] Does this scale align with business expectations?
- [ ] Any peak periods requiring higher volume?

### 4. Audio Requirements
- [ ] Is **silent video + captions** acceptable for pilot?
- [ ] Is **TTS (robotic voice)** acceptable, or need professional voiceover?
- [ ] Priority: Audio NOW vs. launch faster with silent videos?

### 5. Distribution
- [ ] How will videos reach facilities? (Email, Teams, SharePoint, AMP itself?)
- [ ] Need to embed in existing AMP workflow?
- [ ] Any size/format restrictions for distribution channel?

### 6. Compliance
- [ ] **AI Disclosure**: Legal requires watermark identifying AI-generated content - approved?
- [ ] **Brand guidelines**: Any specific Walmart visual standards to follow?
- [ ] **Accessibility mandate**: WCAG AA or AAA compliance required?

---

## 🔍 Program Scope Clarification Questions

### Program Ownership & Governance
- [ ] Who is the **executive sponsor** for this program?
- [ ] Which **business unit** owns the budget and resources? (US Stores Ops, Corporate Comms, Tech?)
- [ ] Is there an existing **program charter** or should we create one?
- [ ] Who has **final approval authority** on video content before distribution?
- [ ] What is the **governance structure**? (Steering committee, regular reviews?)

### Strategic Alignment
- [ ] Does this initiative align with any **existing corporate priorities** or strategic pillars?
- [ ] Are there **other teams** working on similar video/communication initiatives we should coordinate with?
- [ ] Is this considered a **pilot project**, a **proof of concept**, or a **committed program**?
- [ ] What are the **success criteria** that determine if this program continues or expands?
- [ ] What happens if the pilot **fails to meet expectations**? (Pivot, pause, or terminate?)

### Boundaries & Constraints
- [ ] Are there any AMP message types that are **explicitly out of scope**? (e.g., HR-sensitive, legal notices?)
- [ ] Should videos be **store-specific** (personalized per location) or **generic** (same video to all stores)?
- [ ] Are there **language requirements** beyond English? (Spanish, other languages for associates?)
- [ ] Is there a **maximum video length** beyond the 5-8 second API constraint?
- [ ] Are **real associate images/likenesses** allowed, or AI-generated characters only?

### Integration & Dependencies
- [ ] Is the goal to **replace** existing text AMP messages or **supplement** them with video?
- [ ] Should this integrate with the **AMP mobile app** directly, or stand alone?
- [ ] Are there dependencies on other teams? (Legal review, Brand approval, IT security?)
- [ ] Who maintains the **Design Studio templates** long-term? (My team, central design team?)
- [ ] Is there an expectation for **real-time generation** vs. **batch processing**?

### Resource & Support Model
- [ ] Is this a **one-person project** (me) or will additional resources be allocated?
- [ ] Who provides **Tier 1/2 support** if users have issues?
- [ ] What is the expected **support model** after launch? (Self-service, dedicated support?)
- [ ] Is there budget for **external vendors** if needed? (Professional voiceover, cloud infrastructure?)
- [ ] What happens when I'm on **PTO**? Is there a backup owner?

### Measurement & Reporting
- [ ] What **metrics** define success? (Views, engagement, time saved, associate feedback?)
- [ ] How frequently should I provide **status updates**? (Weekly, monthly?)
- [ ] Is there an existing **dashboard or reporting mechanism** I should integrate with?
- [ ] Who is the **audience for reporting**? (Direct manager only, or broader leadership?)
- [ ] Are there **OKRs or KPIs** this project should ladder up to?

### Future State & Expansion
- [ ] Is the long-term vision to expand beyond AMP to other communication channels?
- [ ] Should this capability be offered to **other business units**? (Sam's Club, DC/FC, Corporate?)
- [ ] Is there interest in **user self-service** (anyone can generate videos) vs. **centralized creation**?
- [ ] What is the **end state vision** in 12-24 months?
- [ ] Are there concerns about **AI replacing jobs** that need to be addressed proactively?

### Risk & Mitigation
- [ ] What happens if the **GenAI Media Studio API** becomes unavailable or deprecated?
- [ ] Are there **content moderation** concerns with AI-generated video?
- [ ] What is the **approval workflow** before a video goes to 4,700 stores?
- [ ] How do we handle **incorrect or inappropriate** AI-generated content?
- [ ] Is there a **rollback plan** if videos cause issues in the field?

---

## ✅ What We Can Demonstrate Today

| Capability | Demo Available |
|------------|---------------|
| Enter message text → Generate video | ✅ YES |
| Select character from Design Studio | ✅ YES |
| Select background/environment | ✅ YES |
| Apply template presets | ✅ YES |
| Generate 5-8 second MP4 | ✅ YES |
| Auto-generate captions (WebVTT) | ✅ YES |
| Trim video to specific length | ✅ YES |
| Download final video | ✅ YES |

---

## 📅 Timeline Commitments (Updated with Compliance Work)

### Immediate Priorities (From Wibey Review)

| Task | Target Date | Effort | Status |
|------|-------------|--------|--------|
| Revoke exposed API key | **Jan 23 (TODAY)** | 1 hour | 🔴 CRITICAL |
| Enable SSL verification | Jan 24-27 | 2-3 hours | 🔴 CRITICAL |
| Implement SIEM audit logging | Jan 27-31 | 6-8 hours | 🔴 CRITICAL |
| Basic RBAC framework | Jan 31-Feb 7 | 12 hours | 🔴 CRITICAL |
| Data retention policy | Feb 7-14 | 4-5 hours | 🔴 CRITICAL |

### Feature Milestones

| Milestone | Target Date | Dependencies |
|-----------|-------------|--------------|
| **Silent video demo** | ✅ TODAY | None - ready now |
| **Compliance Week 1 complete** | Jan 31, 2026 | Security team allocation |
| **AMP BigQuery data connection** | Feb 7, 2026 | BigQuery access confirmation |
| **Compliance 95%+ achieved** | Feb 21, 2026 | 4-week sprint completion |
| **TTS audio merged into video** | Feb 14, 2026 | FFmpeg implementation |
| **Pilot launch (5 videos/week)** | Feb 21, 2026 | Stakeholder + compliance approval |
| **AI disclosure watermark** | Feb 28, 2026 | Legal sign-off |
| **Phase 2 (50 videos/week)** | Mar 2026 | Pilot success metrics |

---

## 🚀 Recommended Next Steps

### Immediate (TODAY - From Wibey Review)
1. 🔴 **Revoke exposed API key** (1 hour - CRITICAL)
2. ✅ Demo video generation capability
3. ⬜ Confirm AMP message types in scope
4. ⬜ Confirm audio requirement (silent OK for pilot?)
5. ⬜ Confirm distribution channel

### This Week (Jan 23-31) - Compliance Sprint Week 1
1. 🔴 Enable SSL verification (2-3 hours)
2. 🔴 Implement SIEM audit logging (6-8 hours)
3. ⬜ Connect Zorro to AMP BigQuery data source
4. ⬜ Allocate security/backend resources for compliance

### Short-Term (Feb 1-14) - Compliance Weeks 2-3
1. 🔴 Complete RBAC framework (12 hours)
2. 🔴 Implement data retention policy (4-5 hours)
3. ⬜ Implement audio merge (if required)
4. ⬜ Add AI disclosure watermark
5. ⬜ User acceptance testing with pilot group

### Medium-Term (Feb 14-28) - Compliance Complete + Pilot
1. ✅ Achieve 95%+ compliance (from current 18%)
2. ⬜ Launch pilot with 1-5 videos/week
3. ⬜ Gather feedback from facilities
4. ⬜ Iterate on templates and design elements

### Optional Performance Improvements (Parallel Track - 24 hours total)
1. ⬜ Lazy-load pipeline components (2h - 40% faster startup)
2. ⬜ Add caching for repeated messages (3h - 80% faster for repeats)
3. ⬜ Progress tracking UI (2h - better UX)
4. ⬜ Error recovery UI (2h - fewer support requests)

---

## 📊 Technical Specifications

### Video Output
- **Duration:** 5-8 seconds (API constraint)
- **Resolution:** 1920x1080 (16:9), 1080x1920 (9:16), 1080x1080 (1:1)
- **Format:** MP4 (H.264)
- **Generation time:** ~1-2 minutes per video

### API Provider
- **Platform:** Walmart GenAI Media Studio
- **Model:** Google Veo (veo2, veo3)
- **Rate limits:** 10 req/min, 100 req/hour (confirmed not a concern)
- **Concurrent users:** 2 (approved for pilot)

### Data Source (AMP)
- **Table:** `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
- **Fields mapped:** 311 (from Tableau schema)
- **Store coverage:** 4,700+ US Walmart stores
- **Calendar integration:** Walmart fiscal calendar with WM weeks

### Compliance Summary (Wibey Review)
- **Current Score:** 18% compliant
- **Target Score:** 95%+ compliant
- **Critical Issues:** 5 (blocking enterprise deployment)
- **Total Effort:** 65 hours over 4 weeks
- **Resources Needed:** 2-3 developers + 1 security lead

---

## 📞 Contacts

| Role | Name | Channel |
|------|------|---------|
| Project Lead | Robert Isaacs | robert.isaacs@walmart.com |
| GenAI Media Studio | Stephanie/Oskar | #help-genai-media-studio |
| AMP Data (Spark-Playground) | — | BigQuery access required |
| Code Review | Wibey | (see START_HERE.md, REVIEW_SUMMARY.md) |

---

## 📎 Related Documentation

- [API Integration Guide](API_INTEGRATION_GUIDE.md)
- [Design Studio Guide](DESIGN_STUDIO_GUIDE.md)
- [Knowledge Base & Dependency Map](docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md)
- [GenAI Meeting Notes (Dec 5)](RETINA_GENAI_MEETING_DEC5.md)
- [AMP BigQuery Integration](../Spark-Playground/Spark-Playground/README.md)

---

**Meeting Date:** January 23, 2026  
**Document Version:** 1.0
