# 🖥️ Zorro GUI - Quick Start

## Launch Instructions

### Windows Users

**Option 1: Double-Click** (Easiest)
```
📁 Navigate to project folder
📄 Double-click: start_gui.bat
🎬 Browser opens automatically!
```

**Option 2: Python Script**
```bash
python run_gui.py
```

**Option 3: Streamlit Direct**
```bash
streamlit run app.py
```

### Mac/Linux Users

**Option 1: Python Script**
```bash
python run_gui.py
```

**Option 2: Streamlit Direct**
```bash
streamlit run app.py
```

---

## What Happens Next?

1. **Terminal Shows:**
   ```
   🎬 Launching Zorro Video Generator GUI...
   ============================================================
   📱 The application will open in your default web browser
   🔗 URL: http://localhost:8501
   🛑 Press Ctrl+C to stop the server
   ============================================================

   You can now view your Streamlit app in your browser.

     Local URL: http://localhost:8501
     Network URL: http://192.168.1.x:8501
   ```

2. **Browser Opens:**
   - Automatic launch at `http://localhost:8501`
   - Full-screen web application
   - Ready to use immediately!

3. **You See:**
   ```
   ┌─────────────────────────────────────────────┐
   │   🎬 Zorro AI Video Generator               │
   │   Transform Walmart activity messages       │
   │   into engaging videos                      │
   └─────────────────────────────────────────────┘
   
   [Generate Video] [History] [About]
   ```

---

## First-Time Setup

### Prerequisites Check

Run this to verify your system is ready:

```bash
# Check Python version
python --version
# Should show: Python 3.9 or higher

# Check Streamlit installed
python -m streamlit --version
# Should show: Streamlit, version 1.28.0 or higher

# Check FFmpeg (optional, for video editing)
ffmpeg -version
# Should show FFmpeg version info
```

### Install Missing Dependencies

If anything is missing:

```bash
# Install GUI requirements
pip install streamlit>=1.28.0 watchdog>=3.0.0

# Install FFmpeg (if needed)
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: apt-get install ffmpeg
```

---

## Using the GUI - 30 Second Tutorial

### Step 1: Enter Your Message (5 seconds)
```
Type or click a preset:
"Complete your annual safety training by Friday"
```

### Step 2: Select Options (5 seconds)
```
Category: training
Priority: high
```

### Step 3: Generate! (30-60 seconds)
```
Click: [🎬 Generate Video]
Wait for: "✅ Video generated successfully!"
```

### Step 4: Download (5 seconds)
```
Click: [⬇️ Download Video]
Or: [⬇️ Download Captions]
```

**Total Time: ~1 minute from start to video!**

---

## Key Features at a Glance

### 🎯 Quick Presets
Four ready-to-use message templates:
- 📚 **Training**: Safety training reminder
- ⭐ **Recognition**: Employee celebration
- 🚨 **Alert**: Emergency notification
- 📝 **Reminder**: Task with abbreviations

### ✅ Real-Time Validation
- Character counter (10-500 chars)
- Instant feedback on message length
- Category and priority selection

### 🎨 Video Preview
- Watch inline immediately
- Full video player controls
- Accessibility status indicators

### 📥 One-Click Downloads
- Video file (.mp4)
- Captions (.vtt)
- Transcript (.txt)

### 📊 Generation History
- Last 10 videos
- Re-download anytime
- View metadata

---

## Customization Options

### Sidebar Settings

**Video Provider:**
- ModelScope (default, fastest)
- Stability AI (high quality)
- RunwayML Gen-2 (professional)

**Video Settings:**
- ✓ Apply editing (fades, transitions)
- ✓ Add accessibility (captions, audio)

**Advanced:**
- Duration: 5-30 seconds
- Fade transitions: On/Off
- Trimming: Optional 5-20s

---

## Troubleshooting

### GUI Won't Open?

**Check if server started:**
```bash
# Look for this in terminal:
"You can now view your Streamlit app in your browser"
```

**Manually open browser:**
```
Navigate to: http://localhost:8501
```

**Port already in use?**
```bash
# Kill existing process or use different port
streamlit run app.py --server.port=8502
```

### Video Generation Fails?

**Check terminal output:**
- Look for error messages
- Note any missing dependencies
- Verify API keys (if using Stability/RunwayML)

**Common fixes:**
- Ensure internet connection (for AI models)
- Install FFmpeg for editing features
- Check Python version (3.9+ required)

### Browser Shows "Connection Error"?

**Restart the server:**
```bash
# In terminal, press Ctrl+C
# Then run again:
python run_gui.py
```

---

## Tips for Best Results

### Writing Messages

✅ **DO:**
- Keep 10-500 characters
- Be clear and specific
- Use Walmart abbreviations (CBL, OBW)
- Choose appropriate category

❌ **DON'T:**
- Make too short (< 10 chars)
- Make too long (> 500 chars)
- Use special characters excessively

### Choosing Categories

| Message Type | Category | Priority |
|--------------|----------|----------|
| Training deadline | training | high |
| Employee award | recognition | medium |
| Emergency | alert | critical |
| Task reminder | reminder | medium |
| General update | announcement | low |

### Performance Tips

⚡ **Fast Generation:**
- Use ModelScope provider
- Set duration to 5-10 seconds
- Disable editing for quick tests

🎨 **High Quality:**
- Use Stability AI or RunwayML
- Set duration to 15-20 seconds
- Enable all editing features

---

## Next Steps

Once you're comfortable with the GUI:

1. **Explore Examples**: Try all preset buttons
2. **Customize Settings**: Adjust duration, provider
3. **Review History**: Check past generations
4. **Download Files**: Save videos locally
5. **Read Docs**: Check `docs/GUI_GUIDE.md` for details

---

## Getting Help

### Documentation
- `README.md`: Project overview
- `docs/GUI_GUIDE.md`: Complete GUI manual
- `docs/GUI_FEATURES.md`: Feature showcase
- `docs/API.md`: Python API reference

### Support Channels
- Check terminal for error details
- Review logs in console (F12 in browser)
- Contact Walmart Digital Team

---

**Ready to create your first video? Run `python run_gui.py` now! 🚀**

---

*Zorro Video Generator v1.0 | Walmart US Stores | November 2025*
