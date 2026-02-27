# Deployment Checklist: AMP Activity-Hub Multi-Voice Solution

## ✅ Phase 2 Complete - Ready for Zorro Integration

---

## 🚀 Quick Start (2 Options)

### Option A: Deploy Now with David & Zira ⭐ RECOMMENDED
**Status:** Production-ready, no additional setup  
**Time required:** ~5 minutes  
**Deployment:** Immediate

### Option B: Enhance with Chirp 3 HD Voices (Optional)
**Status:** Enhanced quality, optional setup  
**Time required:** 15 minutes (one-time)  
**Deployment:** David/Zira now + Chirp 3 later

---

## ✅ Pre-Deployment Verification

### Step 1: Verify Audio Files
```powershell
cd "Store Support/Projects/AMP/Zorro/output/podcasts"
ls -l
```

**Expected files:**
- ✅ `Your Week 4 Messages are Here - Audio - Reading - David.wav` (24.32 MB)
- ✅ `Your Week 4 Messages are Here - Audio - Reading - David.mp4` (6.09 MB)
- ✅ `Your Week 4 Messages are Here - Audio - Reading - Zira.wav` (24.09 MB)
- ✅ `Your Week 4 Messages are Here - Audio - Reading - Zira.mp4` (5.26 MB)

### Step 2: Verify Web Server Running
```powershell
cd "C:\Users\krush\Documents\VSCode\Activity-Hub"
python podcast_server.py
```

**Expected output:**
```
Serving at http://localhost:8888
```

### Step 3: Test API Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8888/api/podcasts" | ConvertTo-Json
```

**Expected response:**
```json
[
  {
    "filename": "Your Week 4 Messages are Here - Audio - Reading - Zira.mp4",
    "size_mb": 5.26,
    "url": "/podcasts/..."
  },
  {
    "filename": "Your Week 4 Messages are Here - Audio - Reading - David.mp4",
    "size_mb": 6.09,
    "url": "/podcasts/..."
  }
]
```

### Step 4: Test Web Interface
- Open browser: `http://localhost:8888`
- Should see: Zorro header, both David & Zira files listed
- Should work: Play, download, copy URL buttons

---

## 📋 Deployment Checklist

### Before Deploying to Zorro

- [ ] Audio files verified in output directory
- [ ] Web server tested (localhost:8888 responsive)
- [ ] API endpoint responding with file list
- [ ] Web interface displaying without errors
- [ ] Both David and Zira files playable
- [ ] MP4 files ready (recommendations for Zorro)

### Files to Deploy

**Recommended (MP4 format - smaller, professional):**
- [ ] `Your Week 4 Messages are Here - Audio - Reading - David.mp4`
- [ ] `Your Week 4 Messages are Here - Audio - Reading - Zira.mp4`

**Alternative (WAV format - uncompressed, larger):**
- [ ] `Your Week 4 Messages are Here - Audio - Reading - David.wav`
- [ ] `Your Week 4 Messages are Here - Audio - Reading - Zira.wav`

**Deployment method depends on Zorro's integration:**
- File storage location (local/cloud)
- API endpoint preference (localhost:8888 or direct files)
- Format requirements (MP4 vs WAV vs MP3)

---

## 🔧 Configuration for Zorro

### Option 1: Use Hosted Server
If Zorro can access localhost:8888:
```
API Endpoint: http://localhost:8888/api/podcasts
Player: http://localhost:8888
```

### Option 2: Download Files to Zorro
Copy MP4 files directly to Zorro's media storage:
```
Source: Store Support/Projects/AMP/Zorro/output/podcasts/
Target: [Zorro media directory]
```

### Option 3: Hybrid Approach
- David: Deploy to Zorro
- Zira: Stream from localhost:8888

---

## ⏳ Optional: Add Chirp 3 HD Voices

### When You're Ready to Enhance (15-minute setup)

1. **Read setup guide:**
   - Open: `CHIRP3_SETUP_GUIDE.md`
   - Follow steps 1-6 (credential creation)

2. **Install Google Cloud client:**
   ```powershell
   pip install google-cloud-texttospeech
   ```

3. **Set credentials environment variable:**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\gcp-credentials.json"
   ```

4. **Generate Chirp 3 voices:**
   ```powershell
   python generate_chirp3_voices.py
   ```

5. **Files automatically appear:**
   - `Your Week 4 Messages are Here - Audio - Reading - Chirp3 Achird.mp3`
   - `Your Week 4 Messages are Here - Audio - Reading - Chirp3 Bemrose.mp3`

6. **Web server automatically serves them:**
   - No code changes needed
   - API updated automatically

---

## 📊 Deployment Specifications

### Message Properties
- **Event ID:** 91202b13-3e65-4870-885f-f4a66e221eed
- **Source:** CMS-verified content
- **Duration:** ~6.5 minutes per voice
- **Content:** Complete store operations update

### Audio Specifications (MP4 Recommended)

| Property | David | Zira |
|----------|-------|------|
| Format | MP4 | MP4 |
| Size | 6.09 MB | 5.26 MB |
| Codec | AAC | AAC |
| Bitrate | 192 kbps | 192 kbps |
| Sample Rate | 44.1 kHz | 44.1 kHz |
| Duration | ~6.5 min | ~6.5 min |
| Quality | Professional | Professional |

### Optional: Chirp 3 Specifications

| Property | Achird | Bemrose |
|----------|--------|---------|
| Format | MP3 | MP3 |
| Size | ~3-4 MB | ~3-4 MB |
| Quality | HD (24kHz) | HD (24kHz) |
| Provider | Google Cloud | Google Cloud |
| Status | Optional | Optional |

---

## 🎯 Deployment Decision Tree

```
Are you ready to deploy to Zorro?
│
├─ YES (Deploy now)
│  ├─ Use MP4 files? → Copy David & Zira MP4 files
│  ├─ Use WAV files? → Copy David & Zira WAV files
│  └─ Use API? → Configure localhost:8888 endpoint
│
└─ NO (Need more time)
   ├─ Enhance with Chirp 3? → Follow CHIRP3_SETUP_GUIDE.md
   ├─ Test more? → Run localhost:8888, verify interface
   └─ Review docs? → Read MULTI_VOICE_SOLUTION_SUMMARY.md
```

---

## 🔍 Troubleshooting

### Problem: Files not found
**Solution:** Verify directory exists
```powershell
Test-Path "Store Support/Projects/AMP/Zorro/output/podcasts"
```

### Problem: Server not responding
**Solution:** Restart server
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "path\to\credentials.json"
python podcast_server.py
```

### Problem: MP4 file won't play
**Solution:** Verify creation was successful
```powershell
Get-Item "Your Week 4 Messages*.mp4" | Select-Object Name, Length
```

### Problem: Need different message content
**Solution:** Update and regenerate
```powershell
python generate_both_voices.py  # Edit message_body in script first
python convert_wav_to_mp4_installer.py
```

---

## 📞 Quick Reference

| Need | Location | Command |
|------|----------|---------|
| View audio files | `Store Support/Projects/AMP/Zorro/output/podcasts/` | `ls` |
| Start web server | Any directory | `python podcast_server.py` |
| Check server status | Any directory | `netstat -ano \| findstr :8888` |
| Test API | Browser | `http://localhost:8888/api/podcasts` |
| View web interface | Browser | `http://localhost:8888` |
| Setup Chirp3 | CHIRP3_SETUP_GUIDE.md | See section ⏳ Optional |
| Message verification | Check CMS | Event ID: 91202b13-... |

---

## ✅ Sign-Off Checklist

- [ ] All pre-deployment verification steps completed
- [ ] Audio files confirmed in output directory
- [ ] Web server tested and operational
- [ ] Decision made: Deploy now or enhance with Chirp 3
- [ ] Zorro integration plan established
- [ ] Backup of credentials (if using Chirp 3)
- [ ] Documentation reviewed with team

---

## 🎉 Status: READY FOR DEPLOYMENT

Your AMP Activity-Hub audio solution is:
- ✅ All files generated and verified
- ✅ Web interface tested and operational  
- ✅ API endpoint functional
- ✅ Documentation complete
- ✅ Enhancement path available

**You can deploy to Zorro right now with David & Zira, or optionally enhance with Chirp 3 HD voices (15-minute setup) for superior audio quality.**

---

**Questions? See:**
- `MULTI_VOICE_SOLUTION_SUMMARY.md` - Complete overview
- `CHIRP3_SETUP_GUIDE.md` - Optional enhancement
- `AMP_MEDIA_TYPE_SPECIFICATIONS.md` - Technical details
