# Zorro Audio - Template Library

## Available Templates

### 1. Weekly Messages Audio Template - Summarized

**Status:** ✅ ACTIVE - First Template Prototype  
**Created:** February 27, 2026  
**Template Type:** Weekly Recurring Series  
**Frequency:** 52 times per year (weekly updates)

#### Template Details
| Aspect | Value |
|--------|-------|
| **Name** | Weekly Messages Audio Template - Summarized |
| **Recurrence** | Every week |
| **Default Voice** | Zira (Female) |
| **Duration** | ~4:30 minutes |
| **Content Sections** | 3 areas (Entertainment, Fresh, Fashion) |
| **Branding** | Custom thumbnail ("Listen Now - Audio Message") |
| **Output Format** | Vimeo-compatible MP4 (H.264 + AAC) |
| **File Size** | ~3.83 MB per variation |

#### Script Structure
```
[INTRO]
Hello! Your Week [X] Weekly Messages are Here!
Please Visit the Landing Page to access full content.

[ENTERTAINMENT AREA]
(Department 72 messages)

[FRESH AREA]
(Department 93 messages)

[FASHION AREA]
(Department 29 messages)

[OUTRO]
That's your Week [X] Weekly Messages, Have a Great Week!
```

#### Generation Instructions
1. Prepare content for current week
2. Run: `python Scripts/generate_summarized_final_zira.py`
3. Output files in: `output/podcasts/`
4. Files created:
   - `Weekly Messages Audio Template - Summarized - Week [X] - Zira.wav`
   - `Weekly Messages Audio Template - Summarized - Week [X] - Zira.mp4`
   - `Weekly Messages Audio Template - Summarized - Week [X] - Zira - Vimeo.mp4`

#### Content Source
- **Provider:** AMP Activities (Merchant Messages)
- **Departments:** 72 (Entertainment), 93 (Fresh), 29 (Fashion)
- **Filter:** Messages containing "Summarized:" sections
- **Frequency:** Weekly update

#### First Deployment
- **Created:** February 27, 2026
- **Voice:** Zira (Female)
- **Content:** Departments from Week 4 AMP Activities
- **Deployment:** Dashboard + Vimeo upload

#### Variations Created
- **Week 4** (Feb 27, 2026) - Initial template creation
- **Future Weeks** - To be populated as needed

---

## Requesting a New Template

### Process Overview
1. Fill out [Requirements Questionnaire](REQUIREMENTS_QUESTIONNAIRE.md)
2. Submit to Zorro team for review
3. Team designs template structure
4. Sample generation and approval
5. Creation of generation script
6. Production deployment

### Key Questions to Answer
- **Frequency:** How often will this template be used?
- **Content:** What content goes in each section?
- **Voice:** Which voice(s) needed?
- **Distribution:** Vimeo? Dashboard? Email?
- **Branding:** Custom thumbnail or standard?

### Timeline for New Templates
- **Initial Design:** 2-4 hours
- **Per-Use After:** 10-15 minutes
- **Reusability:** Multiple years (typically)

---

## Active Generation Scripts

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `generate_both_voices.py` | Generate full Week 4 messages as audio | Message body | David + Zira WAV (24 MB each) |
| `generate_summarized_final_zira.py` | Generate summarized messages as Vimeo MP4 | Week script | WAV + MP4 + Vimeo MP4 |
| `convert_wav_to_mp4_installer.py` | Convert WAV files to MP4 | *.wav files | *.mp4 files |
| `convert_standard_to_vimeo.py` | Convert standard MP4 to Vimeo format | *.mp4 files | *-Vimeo.mp4 files |
| `create_audio_thumbnail.py` | Generate standard thumbnail | (none) | merch_msg_thumbnail.jpeg |
| `podcast_server.py` | Dashboard web server | (none) | HTTP server @ :8888 |

---

## Folder Structure

```
Store Support/Projects/AMP/Zorro/Audio/
├── Templates/
│   ├── weekly-messages-summarized/
│   │   ├── generate_template.py
│   │   ├── script_template.md
│   │   ├── thumbnail.jpeg
│   │   └── README.md
│   └── [future-templates]/
│
├── Scripts/
│   ├── generate_both_voices.py
│   ├── generate_summarized_final_zira.py
│   ├── convert_wav_to_mp4_installer.py
│   ├── convert_standard_to_vimeo.py
│   ├── create_audio_thumbnail.py
│   └── podcast_server.py
│
├── Output/
│   ├── podcasts/ [Generated MP4 files]
│   └── archive/ [Old versions]
│
└── Documentation/
    ├── AUDIO_PROCESS_GUIDE.md
    ├── REQUIREMENTS_QUESTIONNAIRE.md
    ├── PROCESS_FLOW_DIAGRAMS.md
    ├── TEMPLATE_LIBRARY.md (THIS FILE)
    └── README.md
```

---

## Dashboard Access

**Server:** `podcast_server.py`  
**URL:** `http://localhost:8888`  
**Port:** 8888

### Dashboard Features
- 🎵 Audio player with native controls
- 📥 Download button
- 📋 Copy link button
- 🗑️ Delete button with confirmation
- 🔄 Auto-refresh every 5 seconds

### Running the Server
```bash
# From Zorro/Audio/Scripts directory
python podcast_server.py

# Or from Activity-Hub root
python "Store Support/Projects/AMP/Zorro/Audio/Scripts/podcast_server.py"
```

Server will display:
```
======================================================================
PODCAST SERVER RUNNING
======================================================================

🎙️  Access at: http://localhost:8888

Serving podcasts from:
  C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\AMP\Zorro\output\podcasts

Press Ctrl+C to stop
```

---

## Maintenance & Updates

### Archive Old Versions
1. Move old MP4 files to `Output/archive/`
2. Keep latest 2-3 weeks on dashboard
3. Maintain indefinite archive for compliance

### Update Thumbnail
```bash
# Edit create_audio_thumbnail.py to change colors/text
python Scripts/create_audio_thumbnail.py
```

### Monitor File Sizes
- **WAV:** 10-25 MB (intermediate, delete after conversion)
- **Standard MP4:** 2-6 MB (intermediate, delete if Vimeo created)
- **Vimeo MP4:** 3-9 MB (final, keep for distribution)

---

## Knowledge Base Status
✅ **Documented:** February 27, 2026  
✅ **Version:** 1.0  
✅ **Status:** Active - Ready for new template requests  
✅ **Last Updated:** February 27, 2026
