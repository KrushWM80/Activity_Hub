# Zorro Audio Production - README

Welcome to the Zorro Audio folder! This is the centralized location for all audio production, workflow documentation, and template management for the Activity Hub.

## What's in This Folder?

This folder contains everything needed to manage audio content creation for Zorro, including:
- **Scripts** for generating audio files
- **Templates** for recurring audio series
- **Output** where all generated files are stored
- **Documentation** explaining processes and requirements

## Quick Start

### 1. Start the Dashboard Server
```bash
cd Scripts
python podcast_server.py
```
Then open your browser to: **http://localhost:8888**

### 2. Generate Audio from an AMP Activity
```bash
cd Scripts
python generate_both_voices.py
```
This creates David and Zira versions of the full Week 4 messages.

### 3. Create a Summarized Weekly Template
```bash
cd Scripts
python generate_summarized_final_zira.py
```
This creates a summarized version with Vimeo compatibility.

## Folder Structure

```
Audio/
├── Scripts/              ← Run Python scripts from here
├── Templates/            ← Reusable template definitions
├── Output/
│   ├── podcasts/         ← Generated audio files
│   └── archive/          ← Older versions
└── Documentation/        ← Process guides and templates
```

## Key Documentation

| Document | Purpose |
|----------|---------|
| [AUDIO_PROCESS_GUIDE.md](Documentation/AUDIO_PROCESS_GUIDE.md) | **START HERE** - Complete process overview |
| [REQUIREMENTS_QUESTIONNAIRE.md](Documentation/REQUIREMENTS_QUESTIONNAIRE.md) | Form for requesting new templates |
| [PROCESS_FLOW_DIAGRAMS.md](Documentation/PROCESS_FLOW_DIAGRAMS.md) | Visual flowcharts of both processes |
| [TEMPLATE_LIBRARY.md](Documentation/TEMPLATE_LIBRARY.md) | Current templates and how to use them |

## Two Core Workflows

### Workflow 1: Standard Audio (Yesterday's Approach)
Convert any AMP Activity to audio file
- ⏱️ **Time:** ~10 minutes
- 📦 **Output:** MP4 audio file
- 🔄 **Reuse:** One-time use

**Used for:** Single messages, quick conversions, variety

### Workflow 2: Audio Template (Today's Innovation)
Create reusable template for recurring content
- ⏱️ **Time:** 2-4 hours initial, 10 minutes per use
- 📦 **Output:** Template + generation script
- 🔄 **Reuse:** 50+ times per year

**Used for:** Weekly messages, regular series, standardized formats

## Available Templates

### Weekly Messages Audio Template - Summarized ✅ ACTIVE
- **Created:** February 27, 2026
- **Frequency:** Weekly (52/year)
- **Default Voice:** Zira (Female)
- **Format:** Vimeo-compatible MP4
- **Duration:** ~4:30 minutes
- **Departments:** Entertainment (72), Fresh (93), Fashion (29)

## Scripts Reference

All scripts are in the `Scripts/` folder:

| Script | What It Does |
|--------|--------------|
| `generate_both_voices.py` | Creates David + Zira versions of full messages |
| `generate_summarized_final_zira.py` | Creates Zira-only summarized version with Vimeo conversion |
| `convert_wav_to_mp4_installer.py` | Converts WAV files to MP4 |
| `convert_standard_to_vimeo.py` | Adds Vimeo compatibility to existing MP4s |
| `create_audio_thumbnail.py` | Generates standard thumbnail image |
| `podcast_server.py` | Runs dashboard web server |

## Audio Generation Pipeline

```
Text Script
   ↓
PowerShell SAPI5 (TTS)
   ↓
WAV File (10-25 MB)
   ↓
FFmpeg Conversion
   ↓
Standard MP4 (2-6 MB)
   ↓
Vimeo Conversion (add thumbnail)
   ↓
Vimeo-Compatible MP4 (3-9 MB) ← FINAL OUTPUT
```

## Requesting a New Audio Template

If you need a recurring audio series:

1. **Review:** Check [AUDIO_PROCESS_GUIDE.md](Documentation/AUDIO_PROCESS_GUIDE.md)
2. **Fill Out:** [REQUIREMENTS_QUESTIONNAIRE.md](Documentation/REQUIREMENTS_QUESTIONNAIRE.md)
3. **Submit:** Send questionnaire to development team
4. **Timeline:** 2-4 hours for initial setup, then ~10 min per use

## Dashboard Features

The local dashboard (http://localhost:8888) provides:

- 🎵 **Audio Player** - Native controls for each file
- ⬇️ **Download** - Save files locally
- 📋 **Copy Link** - Share URLs
- 🗑️ **Delete** - Remove files (with confirmation)
- 🔄 **Auto-Refresh** - Updates every 5 seconds

## Technical Details

### Dependencies
- Python 3.7+
- FFmpeg 4.0+ (for MP4/Vimeo conversion)
- Pillow (for thumbnail generation)
- Windows PowerShell (for TTS)

### Voice Names
- **David:** "Microsoft David Desktop" (Male)
- **Zira:** "Microsoft Zira Desktop" (Female)

### Audio Specifications
- **Sample Rate:** 44.1 kHz
- **Bit Depth:** 16-bit
- **Format:** MP4 (AAC @ 128k)
- **Video (Vimeo):** H.264, yuv420p
- **Thumbnail:** 1920x1080px JPEG

## File Management

### Keep ✅
- Vimeo-compatible MP4 files (production output)
- Thumbnails (reusable)
- Final DAY MP4s (if needed for distribution)

### Delete ❌
- WAV files (after MP4 conversion)
- Standard MP4s (after Vimeo conversion)
- Temporary/test files
- Obsolete versions (>3 weeks old)

Use the dashboard delete button or clean manually:
```bash
# Remove WAV files
Get-ChildItem *.wav | Remove-Item

# Remove non-Vimeo MP4s
Get-ChildItem "*Reading*.mp4" | Where-Object { $_.Name -notlike "*Vimeo*" } | Remove-Item
```

## Troubleshooting

### FFmpeg Not Found
**Error:** "ffmpeg is not available"
- **Solution:** Install FFmpeg from https://ffmpeg.org/download.html
- Add to PATH: `C:\ffmpeg\bin`

### Voice Not Found
**Error:** "Microsoft Zira Desktop not found"
- **Solution:** Use full voice name: "Microsoft Zira Desktop" (not just "Zira")
- List available: Run `check_sapi5_voices.ps1`

### Server Already Running
**Error:** "Port 8888 already in use"
- **Solution:** Kill existing process: `netstat -ano | findstr :8888`

## Getting Help

1. **Review Documentation:** Check guides in `/Documentation/`
2. **Check Templates:** Look at `TEMPLATE_LIBRARY.md`
3. **Process Flows:** See `PROCESS_FLOW_DIAGRAMS.md` for visual guides
4. **Requirements:** Use `REQUIREMENTS_QUESTIONNAIRE.md` for new templates

## Version History

| Date | Version | Changes |
|------|---------|---------|
| Feb 27, 2026 | 1.0 | Initial release - Template workflow established |
| - | - | (Future updates will be documented here) |

---

**Last Updated:** February 27, 2026  
**Status:** ✅ Active and ready for use  
**Next Steps:** Review [AUDIO_PROCESS_GUIDE.md](Documentation/AUDIO_PROCESS_GUIDE.md) to understand workflows
