# Zorro AMP - Quick Reference Guide

**Last Updated:** February 25, 2026
**Status:** ✅ All Systems Operational

---

## 📋 Quick Overview

| Component | Purpose | File | Status |
|-----------|---------|------|--------|
| **Audio/Podcast** | Generate MP3 files from text | `audio_podcast_service.py` | ✅ Tested |
| **Multi-Format** | Create Video/Audio/Infographic | `multi_format_content_manager.py` | ✅ Tested |
| **Analytics** | Track clicks, views, engagement | `analytics_tracker.py` | ✅ Tested |
| **File Optimization** | Compress files 40-60% | Built-in functions | ✅ Tested |

---

## 🎙️ Podcast Generation - 60 Seconds

```python
from src.services.audio_podcast_service import AudioPodcastService, AudioQuality

service = AudioPodcastService()

# Generate a 42-second podcast
podcast = service.generate_podcast_audio(
    content="Your safety message here",
    podcast_title="Safety Brief",
    narrator="professional",  # professional, friendly, energetic, calm
    quality=AudioQuality.MEDIUM,  # LOW (64k), MEDIUM (128k), HIGH (192k), LOSSLESS (320k)
)

print(f"✅ Created: {podcast['filename']}")
print(f"   Duration: {podcast['duration_seconds']}s")
print(f"   Size: {podcast['file_size_mb']}MB")
print(f"   URL: {podcast['download_url']}")
```

**Output Example:**
- File: `podcast_professional_20260225_114734.mp3`
- Duration: 42 seconds
- Size: 0.66 MB
- Quality: 128k bitrate

---

## 🎨 Multi-Format Content - 60 Seconds

```python
from src.services.multi_format_content_manager import (
    MultiFormatContentManager,
    ContentFormat,
    ContentQuality,
)

manager = MultiFormatContentManager()

# Create content in 5 formats from one message
project = manager.create_multi_format_project(
    content="Your message here",
    title="Campaign Name",
    formats=[
        ContentFormat.VIDEO,          # 30-60s MP4 video
        ContentFormat.AUDIO,          # MP3 podcast
        ContentFormat.INFOGRAPHIC,    # Interactive HTML
        ContentFormat.DOCUMENT,       # PDF document
        ContentFormat.INTERACTIVE,    # Interactive HTML
    ],
    quality=ContentQuality.MEDIUM,    # LOW, MEDIUM, HIGH, LOSSLESS
)

# Get download links
downloads = manager.get_distribution_package(
    project_id=project['project_id'],
    include_tracking=True
)

for file_info in downloads['files']:
    print(f"✅ {file_info['format']}: {file_info['download_url']}")
```

**Output Example:**
- PROJECT_WINTER_2026_001
- video: /files/video_output.mp4 (35 MB)
- audio: /files/audio_output.mp3 (0.5 MB)
- infographic: /files/infographic_output.html (1.5 MB)
- document: /files/document_output.pdf (0.3 MB)
- interactive: /files/interactive_output.html (2.0 MB)

---

## 📊 Analytics Tracking - 60 Seconds

```python
from src.services.analytics_tracker import AnalyticsTracker

tracker = AnalyticsTracker()

# Track a view
tracker.track_content_view(
    content_id="PROJECT_001",
    user_id="user_123",
    device_type="mobile",
    platform="email"
)

# Track a click
tracker.track_click(
    content_id="PROJECT_001",
    click_element="download_button",
    user_id="user_123"
)

# Track time spent
tracker.track_time_on_page(
    content_id="PROJECT_001",
    duration_seconds=45,
    user_id="user_123"
)

# Track download
tracker.track_download(
    content_id="PROJECT_001",
    format_type="audio",
    file_size_mb=0.5,
    user_id="user_123"
)

# Get analytics report
report = tracker.get_content_analytics("PROJECT_001")
print(f"Views: {report['views']['total']}")
print(f"Unique users: {report['views']['unique_users']}")
print(f"Click-through rate: {report['clicks']['click_through_rate']}%")
print(f"Downloads: {report['downloads']['total']}")
```

**Report Output:**
```
Views:
  Total: 3
  Unique users: 2
  Avg views/user: 1.5

Clicks:
  Total: 3
  Click elements: {download_audio: 1, share_social: 2}
  CTR: 100%

Downloads:
  Total: 2
  By format: {audio: 1, video: 1}
  Data transferred: 35.5 MB

Engagement:
  Avg time: 45s
  Engagement rate: 200%
  Devices: {mobile: 66%, desktop: 33%}
```

---

## ⚡ File Optimization - 60 Seconds

```python
# Optimize all files for distribution
optimization = manager.optimize_for_distribution(
    project_id="PROJECT_001",
    max_size_mb=10,
)

print(f"Original: {optimization['total_original_size_mb']:.2f} MB")
print(f"Optimized: {optimization['total_optimized_size_mb']:.2f} MB")
print(f"Compression: {optimization['total_compression_ratio']:.2f}x")

# Results:
# Original: 39.30 MB
# Optimized: 23.28 MB
# Compression: 1.69x (43% total savings)
```

**Compression by format:**
- Video: 35 MB → 21 MB (40%)
- Infographic: 1.5 MB → 0.6 MB (60%)
- Audio: 0.5 MB → 0.38 MB (25%)
- Document: 0.3 MB → 0.3 MB (0%)
- Interactive: 2 MB → 1 MB (50%)

---

## 🎯 Narrator Types for Podcasts

```
narrator="professional"   # Pitch: 1.0, Speed: 0.95, Tone: authoritative
narrator="friendly"       # Pitch: 1.05, Speed: 1.0, Tone: warm
narrator="energetic"      # Pitch: 1.1, Speed: 1.1, Tone: enthusiastic
narrator="calm"          # Pitch: 0.95, Speed: 0.85, Tone: soothing
```

---

## 🎛️ Audio Quality Levels for Podcasts

```
Quality.LOW      → 64k bitrate, 22050 Hz (minimal data usage)
Quality.MEDIUM   → 128k bitrate, 44100 Hz (balanced - DEFAULT)
Quality.HIGH     → 192k bitrate, 48000 Hz (high quality)
Quality.LOSSLESS → 320k bitrate, 48000 Hz (maximum quality)
```

**File Size Estimates (30-second podcast):**
- LOW: 0.24 MB
- MEDIUM: 0.50 MB
- HIGH: 0.75 MB
- LOSSLESS: 1.25 MB

---

## 📈 Analytics Report Categories

### Views & Users
- `views.total` - Total content views
- `views.unique` - Unique views (first time viewing)
- `views.unique_users` - Number of different users
- `views.avg_views_per_user` - Average views per person

### Clicks
- `clicks.total` - Total clicks on content
- `clicks.unique` - Unique clicks (first click per user per element)
- `clicks.click_through_rate` - Clicks / Views percentage
- `clicks.by_element` - Breakdown by clickable element

### Engagement
- `engagement.average_time_seconds` - Average time spent viewing
- `engagement.views_spending_time` - How many users spent time
- `engagement.engagement_rate` - Time interactions / Total views

### Downloads
- `downloads.total` - Total files downloaded
- `downloads.by_format` - Downloads per format (video, audio, etc)
- `downloads.total_data_downloaded_mb` - Total data transferred

### Device & Platform
- `device_distribution` - Mobile, Desktop, Tablet breakdown
- `platform_distribution` - Email, Web, Mobile app, etc

---

## 🚀 Recommended Workflow

### 1. Create Multi-Format Content
```python
manager = MultiFormatContentManager()
project = manager.create_multi_format_project(...)
```

### 2. Optimize for Distribution
```python
optimization = manager.optimize_for_distribution(project['project_id'])
```

### 3. Get Distribution Package
```python
package = manager.get_distribution_package(project['project_id'])
# Ready to send via email, share link, etc
```

### 4. Track User Interactions
```python
tracker = AnalyticsTracker()
# Track views, clicks, downloads, engagement
```

### 5. Get Analytics Report
```python
analytics = tracker.get_content_analytics(content_id)
# View comprehensive engagement metrics
```

---

## 📁 Directory Structure

```
Store Support/Projects/AMP/Zorro/
├── src/services/
│   ├── audio_podcast_service.py
│   ├── multi_format_content_manager.py
│   ├── analytics_tracker.py
│   └── ...
├── output/
│   ├── podcasts/          # MP3 files
│   └── multi_format/      # Multi-format projects
├── analytics_data/         # Tracking events
├── test_standalone_system.py  # ✅ Test file (working)
└── AUDIO_AND_MULTIFORMAT_GUIDE.md
```

---

## ✅ Testing

Run the comprehensive test suite:
```bash
cd "Store Support/Projects/AMP/Zorro"
python test_standalone_system.py
```

**Expected output:** All 5 tests pass with detailed metrics

---

## 📞 Common Tasks

### Generate podcast only
```python
service = AudioPodcastService()
podcast = service.generate_podcast_audio(content, title, narrator="professional")
```

### Generate video + audio only
```python
manager = MultiFormatContentManager()
project = manager.create_multi_format_project(
    content, title,
    formats=[ContentFormat.VIDEO, ContentFormat.AUDIO]
)
```

### Get user's full journey
```python
journey = tracker.get_user_journey("user_123")
```

### Get trending content (last 24 hours)
```python
trending = tracker.get_trending_analytics(hours=24)
```

### Optimize large video file
```python
optimized = service.optimize_file_size(
    audio_path="podcast.mp3",
    target_size_mb=2,
    format=AudioFormat.MP3
)
```

---

## 🎯 File Size Quick Reference

| Format | Typical Size | Optimized | Time to Download (3G) |
|--------|--------------|-----------|----------------------|
| Video | 35 MB | 21 MB | 28s / 17s |
| Audio | 0.5 MB | 0.38 MB | 4ms / 3ms |
| Infographic | 1.5 MB | 0.6 MB | 12ms / 5ms |
| Document | 0.3 MB | 0.3 MB | 2.4ms / 2.4ms |
| Interactive | 2 MB | 1 MB | 16ms / 8ms |

---

## 💡 Pro Tips

1. **For email distribution:** Use MEDIUM quality for audio (0.5 MB)
2. **For web:** Use HIGH quality for better user experience
3. **For accessibility:** Always generate audio descriptions
4. **Track everything:** Use unique user IDs for better analytics
5. **Optimize first:** Always compress before sending links
6. **Batch process:** Generate multiple formats at once to save time

---

## 🔗 Related Documentation

- [Full Audio & Multi-Format Guide](AUDIO_AND_MULTIFORMAT_GUIDE.md)
- [Design Studio Guide](DESIGN_STUDIO_GUIDE.md)
- [API Integration Guide](API_INTEGRATION_GUIDE.md)

---

**Created:** February 25, 2026
**Last Updated:** February 25, 2026
**Status:** ✅ Production Ready
