# Zorro Audio Media Type - Process Documentation

## Overview
Two distinct workflows for audio content creation in Zorro:
1. **Standard Audio Process** - Convert single AMP Activity to audio reading
2. **Audio Template Process** - Create reusable audio template for recurring content

---

## Process 1: Standard Audio from AMP Activity

### When to Use
- Single activity to convert
- One-time audio reading needed
- Quick turnaround (existing content)

### Input Requirements
- Single AMP Activity/Message Body
- Voice selection (David or Zira)

### Process Flow
```
AMP Activity Text
    ↓
Select Voice (David/Zira)
    ↓
Generate WAV (Text-to-Speech)
    ↓
Convert WAV → MP4
    ↓
Convert MP4 → Vimeo-Compatible MP4
    ↓
Output: Ready-to-distribute audio file
```

### Questions to Ask User
1. Which AMP Activity/Message would you like to convert?
2. Preferred voice: David (male) or Zira (female)?
3. Need Vimeo-optimized version? (Yes/No)

### Output Deliverables
- Standard MP4 (for general distribution)
- Vimeo-Compatible MP4 (with thumbnail overlay, if requested)

### Tools Used
- generate_both_voices.py
- convert_wav_to_mp4_installer.py

### Timeline
- ~5-10 minutes per voice

---

## Process 2: Audio Template Creation (NEW)

### When to Use
- Recurring content (weekly, bi-weekly, monthly)
- Multiple variations of same structure
- Content that will be reused throughout period
- Standardized format needed across organization

### Input Requirements
**Comprehensive Template Requirements Questionnaire:**

#### A. Template Identification
1. Template Name (e.g., "Weekly Messages Audio Template - Summarized")
2. Template Type (Weekly, Bi-Weekly, Monthly, etc.)
3. Recurring Frequency (how often will this template be used?)

#### B. Content Structure
4. Opening/Intro Text
   - Example: "Hello! Your Week 4 Weekly Messages are Here!"
   - Variable fields needed? (Week number, date, etc.)
5. Main Content Organization
   - How many sections/categories?
   - Names of sections (e.g., Entertainment Area, Fresh Area, Fashion Area)
   - Will content be pulled from specific sources?
6. Closing/Outro Text
   - Example: "That's your Week 4 Weekly Messages, Have a Great Week!"

#### C. Content Rules
7. Content formatting guidelines (bullet points, full sentences, abbreviations vs. spelled-out)
8. Content source (AMP Activities, Custom, Hybrid?)
9. How is content selected for this template? (Specific departments, all activities, filtered by status?)

#### D. Voice & Narration
10. Voice(s) needed: David, Zira, Both, Other?
11. Speech rate preference: Normal, Slower, Faster?
12. Volume/Audio quality: Standard, Enhanced?

#### E. Visual Branding
13. Thumbnail needed? (Yes/No)
14. If yes, thumbnail design:
    - Background color/theme
    - Text/messaging
    - Logo/icon requirements
    - Any specific brand guidelines?

#### F. Distribution Requirements
15. Vimeo upload required? (Yes/No)
16. Other distribution channels?
17. Need dashboard hosting? (Yes/No)

#### G. Variations
18. How many variations will this template have across its lifecycle?
    - Example: Weekly Messages appears 52 times per year
19. Will content change weekly? (Yes/No) → How significantly?
20. Will voice change between variations? (Yes/No)

### Process Flow
```
Template Requirements Questionnaire
    ↓
Gather & Validate Requirements
    ↓
Design Template Script Structure
    (Intro + Content Sections + Outro framework)
    ↓
Approve Script Template with User
    ↓
Generate Thumbnail (if needed)
    ↓
Generate WAV (populate template with sample content)
    ↓
Convert WAV → MP4
    ↓
Convert MP4 → Vimeo-Compatible MP4
    ↓
Create Template Documentation
    (How to use, what to update each occurrence)
    ↓
Output: Reusable Template Ready for Production
```

### Output Deliverables
- Reusable script template (with variable placeholders)
- Standard MP4 (sample)
- Vimeo-Compatible MP4 (sample)
- Thumbnail image (ready for reuse)
- Template usage guide (how to populate new instances)
- Python generation script (for batch creation)

### Tools Created
- generate_summarized_final_zira.py (example template generator)
- create_audio_thumbnail.py (thumbnail generation)
- convert_standard_to_vimeo.py (standard to Vimeo conversion)

### Timeline
- Initial creation: ~2-4 hours (including requirements gathering)
- Each subsequent use: ~10-15 minutes (just populate content and regenerate)

---

## Real-World Example: Weekly Messages Audio Template - Summarized

### Template Profile
| Aspect | Details |
|--------|---------|
| **Name** | Weekly Messages Audio Template - Summarized |
| **Type** | Weekly recurring template |
| **Frequency** | Every week (52 times/year) |
| **Content Structure** | 3 area sections (Entertainment, Fresh, Fashion) |
| **Voices** | Zira (female) - primary |
| **Variations** | 52 per year (1 per week) |
| **Branding** | Custom thumbnail ("Listen Now - Audio Message") |
| **Distribution** | Vimeo upload + Dashboard hosting |
| **Content Change** | Yes - weekly updates per department |

### Sample Script Template
```
[INTRO]
Hello! Your Week [X] Weekly Messages are Here!
Please Visit the Landing Page to access full content.

[ENTERTAINMENT AREA SECTION]
Dept. [X]: [Activity Title]
[Content from identified AMP activities]

[FRESH AREA SECTION]
Dept. [X]: [Activity Title]
[Content from identified AMP activities]

[FASHION AREA SECTION]
Dept. [X]: [Activity Title]
[Content from identified AMP activities]

[OUTRO]
That's your Week [X] Weekly Messages, Have a Great Week!
```

### Reusability Notes
- Script frame stays constant
- Only content between markers changes weekly
- Voices remain same (Zira)
- Thumbnail reused (no need to regenerate)
- Generation takes ~10 minutes with script populated

---

## Comparison Chart

| Aspect | Standard Audio | Audio Template |
|--------|---|---|
| **Use Case** | Single activity | Recurring series |
| **Setup Time** | 5 min | 2-4 hours initial |
| **Per-Use Time** | 10 min | 10-15 min |
| **Voices** | 1-2 | Defined in template |
| **Content Variation** | None (static) | Updates each use |
| **Reusability** | One-time | 50+ times |
| **Script Structure** | Fixed | Templated with placeholders |
| **Thumbnail** | Optional | Included |
| **Vimeo Ready** | Yes | Yes |
| **Documentation** | Minimal | Detailed usage guide |

---

## File Organization - Zorro Folder Structure

All audio-related files should live in:
```
Store Support/Projects/AMP/Zorro/
├── Audio/
│   ├── Templates/
│   │   ├── weekly-messages-summarized/
│   │   │   ├── generate_template.py
│   │   │   ├── script_template.md
│   │   │   └── thumbnail.jpeg
│   │   └── [other-templates]/
│   │
│   ├── Scripts/
│   │   ├── generate_both_voices.py
│   │   ├── generate_summarized_final_zira.py
│   │   ├── convert_wav_to_mp4_installer.py
│   │   ├── convert_standard_to_vimeo.py
│   │   └── create_audio_thumbnail.py
│   │
│   ├── Output/
│   │   ├── podcasts/
│   │   │   ├── [audio files]
│   │   │   └── merch_msg_thumbnail.jpeg
│   │   └── thumbnails/
│   │
│   └── Documentation/
│       ├── AUDIO_PROCESS_GUIDE.md (this file)
│       ├── TEMPLATE_LIBRARY.md
│       └── REQUIREMENTS_QUESTIONNAIRE.md
```

---

## Next Steps for New Template Requests

When a user requests a new Audio Template:

1. **Send Requirements Questionnaire** (see Section C, questions 1-20)
2. **Validate Responses** - Ensure all critical details captured
3. **Design Template Structure** - Create script framework
4. **Present Sample** - Show draft to user for approval
5. **Build Generation Script** - Create dedicated .py file for template
6. **Test Outputs** - Verify audio quality, Vimeo compatibility
7. **Create Usage Guide** - Document how to populate for future uses
8. **Archive Template** - Move to Templates folder for reuse

---

## Knowledge Base Status
✅ **Documented**: February 27, 2026
✅ **Version**: 1.0
✅ **Status**: Active - Ready for implementation in Zorro platform

