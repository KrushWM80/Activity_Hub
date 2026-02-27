# Zorro - Enterprise AI Video Content Generation Platform

> **Current Status**: 🟢 **PHASE 1 PRODUCTION** - Pilot Active, Scaling to Phase 2 (January 21, 2026)

A production-ready system for converting Walmart US Store activity messages into engaging, accessible, brand-consistent video clips using AI-powered generation and enterprise design template management.

**🚀 [View Current Status Update](STATUS_UPDATE_JAN21.md)** | **📖 [Full README](README_CURRENT.md)** | **🔴 [Action Items](MANUAL_ACTION_ITEMS.md)**

## ⚡ Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure your environment
cp .env.example .env
# Edit .env with API keys

# Launch the web interface
streamlit run app.py
```

Navigate to **http://localhost:8501**

---

## 🎯 What Zorro Does

Zorro transforms text-based messages into professional video content while maintaining brand consistency through:

- **Design Studio**: Create and manage reusable design templates (characters, logos, environments, colors)
- **Character Consistency**: Ensure characters look and behave identically across multiple videos
- **Content Pipeline**: Automated message processing → prompt generation → video creation
- **Enterprise Governance**: Approval workflows, compliance enforcement, usage tracking
- **Accessibility**: WCAG AAA compliant captions, audio descriptions, transcripts

---

## 🎬 Core Features

### Design Studio (Fully Implemented)
- Create design elements once, reuse unlimited times
- Character prompt builder for consistent character appearance
- Brand governance and approval workflows
- Pre-loaded example templates ready to use

### Content Generation
- Intelligent message processing (Walmart abbreviation expansion, validation)
- LLM-enhanced prompt generation
- Video generation via Walmart GenAI Media Studio
- Automatic accessibility features

### Web Interface
- Intuitive Streamlit UI (no coding required)
- 5-page design studio with full CRUD
- Video preview and generation history
- Governance dashboards

---

## 📊 Project Status

| Component | Status | Details |
|-----------|--------|---------|
| **Core Platform** | ✅ Complete | Message processing, video gen, web UI |
| **Design Studio** | ✅ Complete | Template management, CRUD, governance |
| **Character System** | ✅ Complete | Prompt builder, 4300+ char prompts |
| **API Integration** | ✅ 95% | Walmart Media Studio working, FFmpeg pending |
| **Documentation** | ✅ Complete | 1000+ lines across guides |

**Latest Documentation:**
- [Current Status (Dec 3)](STATUS_UPDATE_DEC3.md) - Latest executive summary
- [Full README](README_CURRENT.md) - Complete technical overview
- [Design Studio Guide](DESIGN_STUDIO_GUIDE.md) - Feature documentation
- [Quick Start](QUICKSTART_GUI.md) - 30-second tutorial

---

## 🏗️ Architecture

```
Activity Message → Processor → Prompt Generator → Video Generator → Accessibility Engine → Library
```

**Design Studio Integration:**
```
Design Elements (Characters, Logos, Environments) 
    ↓
Master Prompts (Consistency-enforced)
    ↓
Reuse in Video Creation
    ↓
Guaranteed Brand Consistency
```

---

## 📚 Documentation Index

### For Quick Start
- [Quick Start GUI](QUICKSTART_GUI.md) - 30 seconds
- [Visual Guide](VISUAL_GUIDE.md) - Screenshots

### For Feature Details
- [Design Studio Guide](DESIGN_STUDIO_GUIDE.md) - Template management
- [Character Prompt Guide](CHARACTER_PROMPT_GUIDE.md) - Character system
- [Full README](README_CURRENT.md) - Complete reference

### For Integration
- [API Integration Guide](API_INTEGRATION_GUIDE.md) - External systems
- [Walmart Integration](README_WALMART.md) - Walmart Media Studio
- [Sora Integration](SORA_OFFICIAL_API.md) - OpenAI Sora 2

### For Administration
- [Status Update (Dec 3)](STATUS_UPDATE_DEC3.md) - Current status
- [Executive Summary](EXECUTIVE_SUMMARY.md) - High-level overview

---

## 💻 System Requirements

- Python 3.9+
- 4GB RAM (minimum)
- Internet connection
- FFmpeg (optional, for thumbnail extraction)

### API Keys Required
- OpenAI API key (optional, for prompt enhancement)
- Walmart SSO credentials (for Media Studio access)

---

## 🎨 Design Studio Features

### Create Design Elements
✨ Characters with detailed appearance and personality  
✨ Logos with brand colors and usage guidelines  
✨ Environments with scene descriptions  
✨ Color palettes with brand specifications  

### Manage Elements
📋 Full CRUD operations (Create, Read, Update, Delete)  
✅ Approval workflows for brand compliance  
📊 Usage tracking and analytics  
🔐 Facility-level access control  

### Reuse at Scale
♻️ Apply elements to unlimited videos  
🎭 Automatic character consistency  
🚀 50% faster content creation  
📦 Pre-loaded example templates  

---

## 🚀 Key Innovations

### Character Consistency System
Unique approach ensuring characters appear and behave identically across multiple videos through sophisticated prompt engineering.

### Enterprise Design Templates
Scalable template management enabling corporate branding at 4000+ facility scale.

### Accessibility First
WCAG AAA compliance built into core architecture, not bolted on.

---

## 📈 Deliverables

**Code**: 2000+ lines of production code  
**Tests**: 70%+ coverage with comprehensive test suite  
**Documentation**: 1000+ lines across multiple guides  
**Examples**: 5 pre-loaded design elements ready to use  

---

## 🔧 Troubleshooting

### FFmpeg Not Found
FFmpeg is required for thumbnail extraction. [See installation guide](README_CURRENT.md#fFmpeg-installation)

### Design Element Save Fails
Check that all required fields are filled in and prompt is under 5000 characters.

### Video Generation Times Out
Walmart Media Studio may be busy. Try again in a few minutes.

For more help, see [Full README](README_CURRENT.md) or contact #help-genai-media-studio

---

## 📋 Roadmap

### ✅ Phase 1 (Complete - Dec 3, 2025)
- Core platform and design studio
- Character consistency system
- Web interface
- Documentation

### 🔄 Phase 2 (Next)
- FFmpeg integration for thumbnails
- Character consistency validation
- Content creator workflows
- Production deployment

### 📅 Phase 3 (Planned)
- Multi-tenant support
- Advanced analytics
- Mobile UI
- API for third-party integrations

---

## 🤝 Support

- **Design Questions**: [Design Studio Guide](DESIGN_STUDIO_GUIDE.md)
- **Technical Issues**: [Full README](README_CURRENT.md#troubleshooting)
- **Status Updates**: [Status Update (Dec 3)](STATUS_UPDATE_DEC3.md)
- **Slack**: #help-genai-media-studio

---

## 📄 License

Internal Walmart project. All rights reserved.

---

**Last Updated**: January 21, 2026  
**Current Version**: 1.1.0 (Phase 1 Production)  
**Next Review**: February 1, 2026
│ Accessibility Layer │
│ (Captions/Audio)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Final Video Output  │
└─────────────────────┘
```

## 📁 Project Structure

```
zorro/
├── src/
│   ├── core/                  # Core pipeline components
│   │   ├── message_processor.py
│   │   ├── prompt_generator.py
│   │   ├── video_generator.py
│   │   ├── video_editor.py
│   │   └── accessibility_enhancer.py
│   ├── models/                # Data models and schemas
│   │   ├── message.py
│   │   ├── prompt.py
│   │   └── video.py
│   ├── services/              # External service integrations
│   │   ├── llm_service.py
│   │   ├── modelscope_service.py
│   │   ├── stability_service.py
│   │   └── runwayml_service.py
│   ├── utils/                 # Shared utilities
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── validators.py
│   │   └── exceptions.py
│   └── pipeline.py            # Main orchestration
├── tests/
│   ├── unit/
│   │   ├── test_message_processor.py
│   │   ├── test_prompt_generator.py
│   │   ├── test_video_generator.py
│   │   ├── test_video_editor.py
│   │   └── test_accessibility_enhancer.py
│   ├── integration/
│   │   └── test_pipeline.py
│   ├── mocks/
│   │   └── mock_services.py
│   └── fixtures/
│       └── sample_messages.json
├── config/
│   ├── config.yaml
│   ├── config.dev.yaml
│   └── config.prod.yaml
├── examples/
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── ACCESSIBILITY.md
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── setup.py
└── README.md
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://gecgithub01.walmart.com/hrisaac/zorro.git
cd zorro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (required for video editing)
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: apt-get install ffmpeg
```

### 🖥️ Web GUI (Recommended)

The easiest way to use Zorro is through the web interface:

```bash
# Launch the GUI
python run_gui.py

# Or manually with Streamlit
streamlit run app.py
```

The GUI will open in your browser at `http://localhost:8501` and provides:
- ✨ Visual message input with presets
- 🎨 Real-time video preview
- ⚙️ Easy configuration (provider, duration, accessibility)
- 📊 Generation history
- 📥 One-click downloads (video, captions, transcripts)
- 📈 Statistics dashboard

### Basic Usage (Python API)

```python
from src.core.pipeline import VideoGenerationPipeline

# Initialize pipeline
pipeline = VideoGenerationPipeline()

# Generate video from activity message
result = pipeline.generate(
    message_content="Reminder: Complete safety training by Friday",
    message_category="training",
    message_priority="high"
)

print(f"Video generated: {result.path}")
print(f"Duration: {result.duration}s")
print(f"Captions: {result.accessibility.captions_path}")
```

### CLI Usage

```bash
# Generate video from command line
python -m src "Complete your CBL training by Friday" \
    --category training \
    --priority high \
    --provider modelscope

# Run examples
python examples/usage_examples.py

# Run tests
pytest tests/
```

### Advanced Usage

```python
from src.core.pipeline import VideoGenerationPipeline

pipeline = VideoGenerationPipeline()

# Generate with custom options
result = pipeline.generate(
    message_content="Great job on your customer service scores!",
    message_category="recognition",
    message_priority="high",
    apply_editing=True,      # Add fade transitions
    add_accessibility=True,  # Generate captions & audio
    add_fade=True,
    trim_duration=8.0
)

# Batch generation
messages = [
    {"message_content": "Training reminder", "message_category": "training"},
    {"message_content": "Great work!", "message_category": "recognition"}
]
videos = pipeline.generate_batch(messages)
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
# Video Generation
video_generation:
  default_provider: modelscope
  default_duration: 10
  num_frames: 100
  
# LLM Configuration
llm:
  provider: openai
  model: gpt-4
  max_tokens: 300
  
# Accessibility
accessibility:
  captions:
    enabled: true
    format: webvtt
    max_chars_per_line: 32
  audio_description:
    enabled: true
  visual:
    minimum_contrast_ratio: 7.0
    
# Video Editing
video_editing:
  add_fade: true
  fade_duration: 0.5
```

### Environment Variables

```bash
# Required API keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export STABILITY_API_KEY="your-stability-key"  # Optional
export RUNWAYML_API_KEY="your-runwayml-key"    # Optional
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test suite
pytest tests/unit/test_video_generator.py
```

## 📊 Supported Video Models

| Model | Type | Status | Quality | Speed | Cost |
|-------|------|--------|---------|-------|------|
| ModelScope | Open Source | ✅ Implemented | Good | Fast | Free |
| Zeroscope v2 | Open Source | 🔄 Planned | Better | Medium | Free |
| Stability AI | API | 📝 Stub | High | Fast | Paid |
| RunwayML Gen-2 | API | 📝 Stub | Excellent | Fast | Paid |

### ModelScope Setup

```python
# ModelScope is the default provider and works out of the box
# Requires: torch, diffusers, transformers
# GPU recommended but not required (will fallback to CPU)

from src.core.pipeline import VideoGenerationPipeline

pipeline = VideoGenerationPipeline()
result = pipeline.generate(message_content="Your message here")
```

## 🎨 Accessibility Features

### WCAG AAA Compliance

All generated videos meet WCAG 2.1 Level AAA standards:

- **Auto-generated Captions**: WebVTT format with 32 chars/line, proper timing
- **Audio Descriptions**: TTS narration combining message + visual description
- **Transcripts**: Plain text transcripts for all videos
- **High Contrast**: 7:1 color contrast ratio validation
- **Screen Reader Support**: Complete metadata for assistive technologies

### Generated Accessibility Files

For each video, the following files are created:

```
output/
├── videos/
│   └── {video_id}.mp4                    # Main video
├── captions/
│   └── {video_id}.vtt                    # WebVTT captions
├── audio/
│   └── {video_id}_audio_desc.mp3         # Audio description
└── transcripts/
    └── {video_id}_transcript.txt         # Text transcript
```

### Example Accessibility Check

```python
from src.core.accessibility_enhancer import AccessibilityEnhancer

enhancer = AccessibilityEnhancer()

# Validate color contrast
is_compliant = enhancer.validate_contrast_ratio(
    foreground_color=(255, 255, 255),  # White text
    background_color=(0, 0, 0),        # Black background
    wcag_level="AAA"
)
# Returns: True (21:1 contrast ratio)
```

## 🛡️ Security & Compliance

- Input validation and sanitization
- Secure API key management
- Content filtering for inappropriate material
- Audit logging for compliance
- Rate limiting and quota management

## 📝 Development Guidelines

### Code Standards

- **Style**: Follow PEP 8 (use `black` for formatting)
- **Type Hints**: Required for all function signatures
- **Docstrings**: Google style for all public functions/classes
- **Test Coverage**: Maintain >70% coverage (target: 80%+)
- **Logging**: Use structured logging with context
- **Error Handling**: Custom exceptions with details dict

### Project Structure

```python
# All core components follow this pattern:

from ..utils import get_logger, LoggerMixin
from ..utils.exceptions import CustomError

class MyComponent(LoggerMixin):
    """Component description.
    
    Attributes:
        config: Configuration object
    
    Example:
        >>> component = MyComponent()
        >>> result = component.process(data)
    """
    
    def __init__(self):
        self.config = get_config()
        self.logger.info("component_initialized")
    
    def process(self, data: str) -> Result:
        """Process data.
        
        Args:
            data: Input data
        
        Returns:
            Result: Processed result
            
        Raises:
            CustomError: If processing fails
        """
        try:
            # Implementation
            self.logger.info("processing_complete")
            return result
        except Exception as e:
            raise CustomError(
                f"Processing failed: {str(e)}",
                details={"data": data[:50], "error": str(e)}
            )
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_pipeline.py

# Run with verbose output
pytest -v

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

### Adding a New Video Provider

1. Create service file: `src/services/my_provider_service.py`
2. Implement `BaseVideoGenerator` interface
3. Add to `VideoGenerator._create_provider()`
4. Add configuration to `config/config.yaml`
5. Write unit tests with mocks
6. Update documentation

## 🤝 Contributing

1. Follow the coding standards
2. Write tests for new features
3. Update documentation
4. Submit PR with clear description

## 📄 License

Internal Walmart Project - Proprietary

## 👥 Team

Walmart US Stores - Activity Messages Team

## 📞 Support

For questions or issues, contact: [Your Team Contact]

---

**Note**: This is a production system handling real store communications. Always test thoroughly before deployment.
