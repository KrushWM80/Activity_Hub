# Zorro - Master Documentation Index

## AI Video Generation Platform for Walmart Operations
**Version:** 1.0 | **Status:** Phase 1 Production - Pilot Active  
**Last Updated:** January 23, 2026

---

## 🎯 Quick Start by Role

| Role | Start Here | Then Read | Time |
|------|------------|-----------|------|
| **Business User** | [Quick Start GUI](QUICKSTART_GUI.md) | [Design Studio Guide](DESIGN_STUDIO_GUIDE.md) | 5 min |
| **Developer** | [README.md](README.md) | [Knowledge Base](docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md) | 15 min |
| **DevOps** | [Deployment Guide](DEPLOYMENT_GUIDE.md) | [Docker Setup](Dockerfile) | 10 min |
| **Executive** | [Executive Summary](EXECUTIVE_SUMMARY.md) | [Status Update](STATUS_UPDATE_JAN21.md) | 3 min |
| **API Integrator** | [API Integration Guide](API_INTEGRATION_GUIDE.md) | [API Testing Guide](API_TESTING_GUIDE.md) | 20 min |

---

## 📁 Complete Documentation Map

### Core Documentation
| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Project overview, quick start | All |
| [README_CURRENT.md](README_CURRENT.md) | Complete technical reference | Developers |
| [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | High-level business overview | Leadership |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project status and roadmap | Stakeholders |

### User Guides
| Document | Purpose | Audience |
|----------|---------|----------|
| [QUICKSTART_GUI.md](QUICKSTART_GUI.md) | 30-second tutorial | End users |
| [VISUAL_GUIDE.md](VISUAL_GUIDE.md) | Screenshots and walkthrough | End users |
| [DESIGN_STUDIO_GUIDE.md](DESIGN_STUDIO_GUIDE.md) | Design Studio feature documentation | Business managers |
| [GUI_COMPLETE_OVERVIEW.md](GUI_COMPLETE_OVERVIEW.md) | Full GUI feature reference | All users |

### Technical Documentation
| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md](docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md) | **📌 Architecture & dependencies** | Developers |
| [DESIGN_STUDIO_ARCHITECTURE.md](DESIGN_STUDIO_ARCHITECTURE.md) | Design Studio technical design | Developers |
| [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md) | Walmart Media Studio API | Developers |
| [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) | API testing procedures | QA/Developers |
| [docs/API.md](docs/API.md) | API reference | Developers |
| [docs/ACCESSIBILITY.md](docs/ACCESSIBILITY.md) | WCAG compliance details | Developers |

### Deployment & Configuration
| Document | Purpose | Audience |
|----------|---------|----------|
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Production deployment | DevOps |
| [WALMART_INTEGRATION.md](WALMART_INTEGRATION.md) | Walmart ecosystem integration | DevOps |
| [CONNECTING_TO_SORA.md](CONNECTING_TO_SORA.md) | OpenAI Sora integration (future) | Developers |
| [config/config.yaml](config/config.yaml) | Main configuration file | DevOps |

### Status & Meetings
| Document | Purpose | Audience |
|----------|---------|----------|
| [STATUS_UPDATE_JAN21.md](STATUS_UPDATE_JAN21.md) | Latest status update | All |
| [RETINA_GENAI_MEETING_DEC5.md](RETINA_GENAI_MEETING_DEC5.md) | GenAI team meeting notes | Project team |
| [IMPLEMENTATION_COMPLETE_JAN21.md](IMPLEMENTATION_COMPLETE_JAN21.md) | Implementation milestone | Stakeholders |
| [NEXT_STEPS.md](NEXT_STEPS.md) | Upcoming work items | Project team |
| [MANUAL_ACTION_ITEMS.md](MANUAL_ACTION_ITEMS.md) | Required manual actions | Project team |

### Compliance & Governance
| Document | Purpose | Audience |
|----------|---------|----------|
| [WALMART_COMPLIANCE_REVIEW.md](WALMART_COMPLIANCE_REVIEW.md) | Compliance assessment | Security/Legal |
| [COMPLIANCE_REMEDIATION_PLAN.md](COMPLIANCE_REMEDIATION_PLAN.md) | Remediation roadmap | Security |
| [COMPLIANCE_CODE_EXAMPLES.md](COMPLIANCE_CODE_EXAMPLES.md) | Compliant code patterns | Developers |
| [ENTERPRISE_ARCHITECTURE_REVIEW.md](ENTERPRISE_ARCHITECTURE_REVIEW.md) | EA review status | Architecture |

---

## 🔍 Document Finder

| If you need... | Read this |
|----------------|-----------|
| How to create my first video | [Quick Start GUI](QUICKSTART_GUI.md) |
| How to use Design Studio | [Design Studio Guide](DESIGN_STUDIO_GUIDE.md) |
| How the system architecture works | [Knowledge Base](docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md) |
| How to integrate with Media Studio API | [API Integration Guide](API_INTEGRATION_GUIDE.md) |
| How to deploy to production | [Deployment Guide](DEPLOYMENT_GUIDE.md) |
| What the current project status is | [Status Update Jan 21](STATUS_UPDATE_JAN21.md) |
| What was decided in GenAI meeting | [Meeting Notes Dec 5](RETINA_GENAI_MEETING_DEC5.md) |
| What compliance requirements exist | [Compliance Review](WALMART_COMPLIANCE_REVIEW.md) |
| What the rate limits are | [API Integration Guide](API_INTEGRATION_GUIDE.md) |
| How accessibility features work | [Accessibility Docs](docs/ACCESSIBILITY.md) |

---

## 📂 Source Code Structure

```
zorro/
├── app.py                    # Main Streamlit application entry point
├── run_gui.py                # Alternative GUI launcher
├── start_gui.bat             # Windows batch launcher
│
├── config/
│   ├── config.yaml           # Main configuration
│   ├── config.dev.yaml       # Development overrides
│   └── config.prod.yaml      # Production settings
│
├── data/
│   ├── design_library.json   # Saved design elements
│   └── sample_amp_messages.json # Sample AMP messages
│
├── docs/
│   ├── KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md  # 📌 Technical reference
│   ├── ACCESSIBILITY.md      # WCAG compliance
│   ├── API.md                # API reference
│   └── GUI_GUIDE.md          # GUI documentation
│
├── pages/                    # Streamlit multi-page apps
│   ├── design_studio.py      # Design Studio page
│   └── message_queue.py      # Message Queue page
│
├── src/
│   ├── core/                 # Pipeline components
│   │   ├── pipeline.py       # Main orchestrator
│   │   ├── message_processor.py
│   │   ├── prompt_generator.py
│   │   ├── video_generator.py
│   │   ├── video_editor.py
│   │   └── accessibility_enhancer.py
│   │
│   ├── models/               # Pydantic data models
│   │   ├── message.py
│   │   ├── design_element.py
│   │   ├── prompt.py
│   │   └── video.py
│   │
│   ├── providers/            # Video generation providers
│   │   ├── base_provider.py
│   │   ├── walmart_media_studio.py  # Primary provider
│   │   └── sora_provider.py         # Future
│   │
│   ├── services/             # Business logic services
│   │   ├── design_studio_service.py
│   │   ├── llm_service.py
│   │   └── character_prompt_builder.py
│   │
│   └── ui/components/        # Streamlit UI components
│       ├── design_selector.py
│       └── video_trimmer.py
│
├── tests/                    # Test suites
├── output/                   # Generated videos and transcripts
└── examples/                 # Usage examples
```

---

## 🚀 Key Entry Points

| Action | Command / File |
|--------|----------------|
| **Start Web UI** | `streamlit run app.py` or `start_gui.bat` |
| **Run Tests** | `pytest tests/` |
| **Build Docker** | `docker build -t zorro .` |
| **Quick API Test** | `python quick_api_test.py` |

---

## 📊 Current Status (January 2026)

| Component | Status | Notes |
|-----------|--------|-------|
| Design Studio | ✅ Complete | Characters, backgrounds, templates |
| Message Queue | ✅ Complete | AMP workflow with variable selection |
| Video Generation | ✅ Complete | Walmart Media Studio API working |
| Video Trimmer | ✅ Complete | FFmpeg-based trim and download |
| Accessibility | ✅ Complete | Captions, audio descriptions, transcripts |
| AI Disclosure | 🔴 Pending | Legal watermark requirement |

**Phase:** Pilot (1-5 videos/week, 2 concurrent users)

---

## 📞 Contacts & Support

- **Slack:** #help-genai-media-studio
- **Project Lead:** Robert Isaacs
- **API Docs:** [API Integration Guide](API_INTEGRATION_GUIDE.md)
- **Design Guide:** [Design Studio Guide](DESIGN_STUDIO_GUIDE.md)

---

## 📚 Related Resources

### Cross-Project Documentation
- [Cross-Project Patterns](../project-updates/CROSS-PROJECT-PATTERNS.md) - Reusable patterns across portfolio
- [Enterprise Registration Playbook](../project-updates/ENTERPRISE-REGISTRATION-PLAYBOOK.md) - Production deployment guide

### Portfolio Context
- [Portfolio Status Summary](../project-updates/PORTFOLIO-STATUS-SUMMARY-DEC4.md) - Overall portfolio health
- [Project Dashboard](../project-updates/PROJECT-DASHBOARD-AT-A-GLANCE.md) - All projects at a glance

---

*This index follows the MASTER-INDEX pattern from Tour-It (cascaded via CROSS-PROJECT-PATTERNS.md)*
