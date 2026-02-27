# Zorro GUI User Guide

## 🖥️ Getting Started

### Launch the Application

```bash
# Quick launch
python run_gui.py

# Or with Streamlit directly
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📋 Main Interface

### 1. Generate Video Tab 🎥

#### Quick Presets
Four ready-to-use example messages:
- **Training**: Safety training reminder
- **Recognition**: Employee achievement celebration
- **Alert**: Emergency notification
- **Reminder**: Task reminder with Walmart abbreviations

#### Message Input
- **Activity Message** (10-500 characters): Your message text
  - Real-time character counter
  - Automatic validation
  - Walmart abbreviations (CBL, OBW, GWP) are auto-expanded

#### Message Details
- **Category**: Select type (training, recognition, alert, etc.)
- **Priority**: Set urgency (low, medium, high, critical)
- **Sender ID**: Optional identifier (e.g., SM_12345)

#### Generate Button
Click **🎬 Generate Video** to create your video
- Processing time: 30-60 seconds
- Real-time progress indicator
- Success notification with balloons 🎈

#### Results Display
After generation:
- **Video Player**: Watch your video inline
- **Metadata**: Video ID, duration, model used
- **Downloads**: 
  - ⬇️ Video file (.mp4)
  - ⬇️ Captions (.vtt)
  - ⬇️ Transcript (.txt)
- **Accessibility Features**: 
  - ✅ Status indicators (captions, audio, WCAG level)
  - Screen reader compatibility check

---

### 2. History Tab 📊

View your recent video generations:
- **Last 10 Videos**: Most recent first
- **Details**: Message, category, priority, timestamp, model
- **Actions**: Download videos from history
- **Clear History**: Remove all entries

---

### 3. About Tab ℹ️

Project information:
- **What is Zorro**: Overview and purpose
- **Key Features**: AI-powered, accessible, fast
- **Technology Stack**: AI models, frameworks
- **Supported Categories**: Full category list
- **Best Practices**: Tips for optimal results
- **Statistics**: Generation metrics

---

## ⚙️ Settings (Sidebar)

### Video Provider
Choose AI model:
- **modelscope**: Fast, reliable (default)
- **stability**: High quality (requires API key)
- **runwayml**: Professional grade (requires API key)

### Video Settings
- **Apply editing**: Enable fade transitions
- **Add accessibility**: Generate captions & audio descriptions

### Advanced Settings
- **Video Duration**: 5-30 seconds (default: 10s)
- **Add fade**: Smooth transitions
- **Enable trimming**: Cut to specific length
  - **Trim to**: 5-20 seconds

---

## 💡 Tips & Best Practices

### Writing Effective Messages

✅ **Good Examples:**
```
"Complete your annual safety training by Friday"
"Congratulations on achieving 100% customer satisfaction!"
"Emergency evacuation drill scheduled for 2 PM today"
"Don't forget to complete your CBL modules this week"
```

❌ **Avoid:**
- Too short: "Do training" (< 10 characters)
- Too long: Multiple paragraphs (> 500 characters)
- Unclear: "Update the thing by sometime"

### Using Walmart Abbreviations

The system automatically expands:
- **CBL** → Computer Based Learning
- **OBW** → One Best Way
- **GWP** → Great Workplace
- **SM** → Store Manager
- **ASM** → Assistant Store Manager
- **DM** → Department Manager

### Choosing Categories

| Category | Use For | Priority |
|----------|---------|----------|
| **Training** | Learning, CBL reminders | Medium-High |
| **Recognition** | Awards, achievements | Medium |
| **Alert** | Urgent notifications | High-Critical |
| **Reminder** | Task deadlines | Low-Medium |
| **Announcement** | General updates | Low-Medium |
| **Celebration** | Team milestones | Medium |

### Accessibility Features

**Always enable** accessibility for:
- Public announcements
- Training materials
- Compliance communications

**Benefits:**
- WCAG AAA compliant (7:1 contrast)
- WebVTT captions for hearing impaired
- Audio descriptions for visually impaired
- Screen reader compatible
- Transcript downloads

---

## 🔧 Troubleshooting

### Video Not Generating

**Check:**
1. Message length (10-500 characters)
2. Internet connection (for AI models)
3. API keys configured (for Stability/RunwayML)
4. FFmpeg installed (for video editing)

**Error Messages:**
- "Message too short" → Add more text
- "Pipeline failed" → Check terminal for details
- "File not found" → Video may still be processing

### Slow Performance

**Solutions:**
- Use ModelScope provider (fastest)
- Reduce video duration to 5-10s
- Disable editing features
- Check GPU availability

### Accessibility Files Missing

**Verify:**
- "Add accessibility features" is checked
- Output directory has write permissions
- gTTS package installed (`pip install gTTS`)

---

## 📥 Download & Export

### Available Downloads

1. **Video File (.mp4)**
   - Full generated video
   - Includes all edits and transitions
   - Compatible with all media players

2. **Captions File (.vtt)**
   - WebVTT format
   - Timed captions
   - Works with HTML5 video players

3. **Transcript (.txt)**
   - Full text transcript
   - Accessibility documentation
   - Plain text format

### File Locations

Default output directory: `outputs/videos/`

Organized by:
```
outputs/
└── videos/
    ├── {video_id}.mp4
    ├── {video_id}_captions.vtt
    ├── {video_id}_audio.mp3
    └── {video_id}_transcript.txt
```

---

## ⌨️ Keyboard Shortcuts

- **Ctrl+C**: Stop server (in terminal)
- **F5**: Refresh page
- **Ctrl+S**: Save settings (browser dependent)

---

## 🚀 Advanced Features

### Custom Configurations

Edit `config/config.yaml` to customize:
- Default video duration
- Output directory
- Model parameters
- Accessibility settings

### Batch Processing

Use Python API for multiple videos:

```python
from src.core.pipeline import VideoGenerationPipeline

pipeline = VideoGenerationPipeline()
messages = ["Message 1", "Message 2", "Message 3"]

for msg in messages:
    result = pipeline.generate(message_content=msg)
    print(f"Generated: {result.path}")
```

### API Integration

The GUI runs on port 8501 and uses Streamlit's session state.
For REST API, see `docs/API.md` for FastAPI wrapper.

---

## 📞 Support

### Common Questions

**Q: How long does video generation take?**
A: 30-60 seconds with ModelScope, up to 2 minutes with other providers

**Q: Can I use custom video styles?**
A: Yes, edit prompt templates in `config/prompt_templates.yaml`

**Q: Is GPU required?**
A: No, but GPU acceleration (CUDA) speeds up generation 3-5x

**Q: How many videos can I generate?**
A: No limit, but history shows only last 10 in GUI

**Q: Can I export history?**
A: Yes, session history is in `st.session_state.generation_history`

### Getting Help

- Check logs in terminal for detailed errors
- Review `README.md` for setup instructions
- See `IMPLEMENTATION_SUMMARY.md` for architecture
- Contact Walmart Digital Team for support

---

## 🔄 Updates & Maintenance

### Updating Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### Clearing Cache

```bash
# Clear Streamlit cache
streamlit cache clear
```

### Resetting Configuration

Delete or rename:
- `config/config.yaml` (will regenerate)
- `.streamlit/config.toml` (Streamlit settings)

---

## 🎓 Learning Resources

### Documentation
- `README.md`: Project overview
- `docs/API.md`: Python API reference
- `docs/ACCESSIBILITY.md`: WCAG compliance guide
- `EXECUTIVE_SUMMARY.md`: Business case and ROI

### Examples
- `examples/usage_examples.py`: 7 usage patterns
- Preset buttons in GUI: Quick templates

---

**Version**: 1.0
**Last Updated**: November 2025
**Platform**: Walmart US Stores Digital Team
