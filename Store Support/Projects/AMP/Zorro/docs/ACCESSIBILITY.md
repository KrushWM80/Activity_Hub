# Accessibility Guidelines

## Overview

Zorro is designed with accessibility as a core principle, ensuring all generated video content is accessible to associates with disabilities, following WCAG AAA standards.

## Features

### 1. Automated Captions (WebVTT)

**What it does:**
- Generates synchronized text captions for all video content
- Supports multiple formats (WebVTT, SRT)
- Includes proper timing and formatting

**Configuration:**
```yaml
accessibility:
  captions:
    enabled: true
    format: "webvtt"
    language: "en-US"
    font_size: 24
    font_family: "Arial"
    background_opacity: 0.8
    position: "bottom"
```

**Best Practices:**
- Captions appear at bottom of screen
- High contrast background (80% opacity)
- Sans-serif fonts (Arial, Helvetica)
- Minimum 24px font size
- Maximum 32 characters per line
- 2-3 lines maximum on screen

### 2. Audio Descriptions

**What it does:**
- Provides narration of visual elements
- Describes actions, settings, and context
- Uses natural-sounding text-to-speech

**Configuration:**
```yaml
accessibility:
  audio_description:
    enabled: true
    voice: "en-US-Neural2-J"
    speed: 1.0
    volume: 0.8
```

**Best Practices:**
- Describe what's happening visually
- Keep descriptions concise
- Use present tense
- Avoid redundancy with dialogue/captions

### 3. High Contrast Text

**What it does:**
- Ensures text overlays meet WCAG AAA contrast ratios
- Validates contrast ratio (minimum 7:1)
- Applies background shading for readability

**Configuration:**
```yaml
accessibility:
  visual:
    high_contrast: true
    minimum_contrast_ratio: 7.0  # WCAG AAA
    text_overlay_background: true
```

**Color Combinations:**
- White text on black background: 21:1
- Black text on white background: 21:1
- Yellow text on black background: 19.5:1

### 4. Color Blindness Considerations

**What it does:**
- Uses color-blind safe palettes
- Doesn't rely solely on color for information
- Tests with color blindness simulators

**Guidelines:**
- Avoid red/green combinations
- Use patterns/textures in addition to color
- Provide text labels for color-coded information

### 5. Screen Reader Compatibility

**What it does:**
- Includes metadata for assistive technologies
- Provides alternative text descriptions
- Structured semantic markup

**Implementation:**
- Video title and description
- Chapter markers with descriptions
- Alt text for thumbnails

## WCAG Compliance

### Level AAA Requirements

We meet or exceed these WCAG AAA criteria:

1. **Contrast (Minimum)**: 7:1 ratio for normal text
2. **Audio Description (Prerecorded)**: Provided for all content
3. **Sign Language**: Available for critical safety messages
4. **Extended Audio Description**: For complex visuals
5. **Captions (Live)**: For any live content

### Testing Checklist

- [ ] Color contrast ratio ≥ 7:1
- [ ] Captions synchronized within 0.5 seconds
- [ ] Audio descriptions don't overlap dialogue
- [ ] Readable by screen readers
- [ ] Works with keyboard navigation
- [ ] Tested with assistive technologies

## Implementation Example

```python
from src.models import GeneratedVideo, AccessibilityMetadata

# Create video with accessibility features
video = GeneratedVideo(
    id="accessible_001",
    path="output/video.mp4",
    accessibility=AccessibilityMetadata(
        has_captions=True,
        captions_path="output/video.vtt",
        caption_format="webvtt",
        has_audio_description=True,
        audio_description_path="output/video_desc.mp3",
        wcag_level="AAA",
        color_contrast_ratio=7.5,
        screen_reader_compatible=True
    )
)

# Verify accessibility
assert video.is_accessible
assert video.accessibility.wcag_level == "AAA"
```

## WebVTT Caption Format

Example caption file:
```
WEBVTT

00:00:00.000 --> 00:00:03.000
Complete your safety training
by Friday.

00:00:03.000 --> 00:00:06.000
This ensures our Great Workplace
standards.

00:00:06.000 --> 00:00:08.000
Contact your Store Manager
with questions.
```

## Audio Description Script Example

```
"A well-lit Walmart store interior.
Associates in blue vests are visible.
Digital training tablets are shown.
Text appears: 'Complete Safety Training by Friday.'
A calendar with Friday highlighted.
Associates complete training successfully."
```

## Accessibility Testing Tools

### Recommended Tools

1. **WAVE (Web Accessibility Evaluation Tool)**
   - Tests contrast ratios
   - Identifies accessibility issues

2. **NVDA / JAWS Screen Readers**
   - Test video metadata
   - Verify caption readability

3. **Color Oracle**
   - Simulates color blindness
   - Tests color combinations

4. **Contrast Checker**
   - Validates WCAG compliance
   - Tests color combinations

### Testing Process

1. Generate video with accessibility features
2. Validate caption timing and sync
3. Check audio description quality
4. Test with screen reader
5. Verify contrast ratios
6. Simulate color blindness
7. Test keyboard navigation

## Legal Compliance

### ADA Compliance

- Title I: Employment accessibility
- Title III: Public accommodations
- Section 508: Federal requirements

### Best Practices for Walmart

1. **All videos must include captions**
2. **Safety videos require audio descriptions**
3. **Critical communications need sign language interpretation**
4. **Alternative formats available upon request**
5. **Regular accessibility audits**

## User Preferences

Support for user customization:

```yaml
user_preferences:
  caption_size: "large"  # small, medium, large
  caption_style: "white_on_black"
  audio_description: "extended"  # brief, standard, extended
  playback_speed: 1.0  # 0.5 - 2.0
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebVTT Standard](https://www.w3.org/TR/webvtt1/)
- [Section 508 Standards](https://www.section508.gov/)
- [ADA Requirements](https://www.ada.gov/)

## Support

For accessibility questions or accommodations:
- Email: accessibility@walmart.com
- Contact your local HR representative
- Call the accessibility helpline

---

**Remember**: Accessibility is not optional—it's essential for ensuring all associates can engage with critical workplace communications.
