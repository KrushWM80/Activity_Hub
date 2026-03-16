# Zorro Audio Production - README

Welcome to the Zorro Audio folder! This is the centralized location for all audio production for the Activity Hub Weekly Messages.

## What's in This Folder?

- **Scripts/** — Pipeline scripts for automated BQ → TTS → MP4 workflow
- **Scripts/cache/** — JSON cache files for two-phase VPN workflow
- **output/** — Generated MP4 audio files and script text files
- **windows_media_synthesizer.py** — edge-tts Jenny Neural + SAPI5 fallback engine
- **Documentation/** — Process guides and templates

## Quick Start

### Dashboard (Recommended)
The audio server runs at **http://localhost:8888** — started automatically via `Automation/start_zorro_24_7.bat`.

Click **"Weekly Message Audio"** button → popup with two steps:
1. **Fetch Data** (on Eagle WiFi / VPN) — pulls from BigQuery, caches locally
2. **Generate Audio** (on Walmart WiFi / off VPN) — synthesizes with Jenny Neural

### Command Line
```bash
# Phase 1: Fetch data (requires Eagle WiFi / VPN)
python Scripts/generate_weekly_audio.py --week 4 --fy 2027 --phase fetch

# Phase 2: Synthesize audio (requires Walmart WiFi / off VPN)
python Scripts/generate_weekly_audio.py --week 4 --fy 2027 --phase synthesize
```

## Automated Weekly Message Audio Pipeline

### Data Source
- **BigQuery Table**: `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
- **Filter**: `Message_Type = 'Merchant Message'` AND `Status = 'Review for Publish review - No Comms'`
- **Content**: Extracts "Summarized:" text from each event's message body

### Area Groupings (in order)
1. **Food & Consumables**: Beauty and Consumables, Food, Fresh
2. **General Merchandise**: Entertainment, Fashion, Hardlines, Home, Seasonal
3. **Operations**: Asset Protection, Auto Care, Backroom and Claims, Frontend, Pickup, People, Total Store

### Two-Phase Cache System
Required because Eagle WiFi/VPN is needed for BigQuery but blocks Jenny Neural TTS.

| Phase | Network | Action | Time |
|-------|---------|--------|------|
| Fetch | Eagle WiFi (VPN ON) | BQ query + text extraction + cache | ~5 seconds |
| Synthesize | Walmart WiFi (VPN OFF) | TTS synthesis + MP4 encoding | ~2-4 minutes |

Cache stored at: `Scripts/cache/week_{N}_fy{YYYY}.json`

### Audio Pipeline Flow
```
BigQuery (AMP ALL 2)
   ↓ Filter: Merchant Message + Review for Publish - No Comms
Extract Summarized text from message body
   ↓ Regex: Summarize[d]?\s*:\s*(.*) and Summarized\s+(.*)
Group by Area (Food & Consumables → GM → Operations)
   ↓
Build TTS Script (Intro → Groups → Areas → Events → Outro)
   ↓
Save as: output/Audio/Week N - Weekly Messages Audio Script.txt
   ↓
edge-tts Jenny Neural (en-US-JennyNeural)
   ↓
FFmpeg MP4 Encoding (AAC @ 256kbps)
   ↓
output/Audio/Week N - Weekly Messages Audio.mp4
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `Scripts/generate_weekly_audio.py` | **Main pipeline** — BQ fetch, text extraction, TTS, MP4 |
| `windows_media_synthesizer.py` | edge-tts Jenny Neural engine with SAPI5 fallback |
| `../audio_server.py` | Dashboard web server (port 8888) |

## Technical Details

### Dependencies
- Python 3.14+, edge-tts v7.2.7
- FFmpeg at `C:\ffmpeg\bin\ffmpeg.exe` (AAC @ 256kbps)
- BQ Auth: gcloud application_default_credentials.json

### Voice
- **Primary**: en-US-JennyNeural (edge-tts, requires Walmart WiFi)
- **Fallback**: SAPI5 David/Zira (works on any network)

### Output Specifications
- **Format**: MP4 audio (AAC)
- **Bitrate**: 256 kbps
- **Voice**: Jenny Neural (female, natural-sounding)

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
