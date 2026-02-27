# ✅ AMP PODCAST - NOW LIVE & WORKING

**Status:** 🟢 **READY TO USE** | Server: Running on localhost:8888 | Date: February 25, 2026

---

## 🎙️ YOUR WORKING LINKS

### **Web Player (Recommended)**
```
http://localhost:8888
```
→ Open in browser to play, download, and manage all podcasts

### **Direct Download Link**
```
http://localhost:8888/podcasts/amp_podcast_91202b13_Seasonal_Promotion_Launch_-_Sp_20260225_124233.wav
```
→ Direct link to podcast file (2.43 MB, 57 seconds)

### **Local File Path** (for email attachment)
```
C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\AMP\Zorro\output\podcasts\amp_podcast_91202b13_Seasonal_Promotion_Launch_-_Sp_20260225_124233.wav
```

---

## 📊 PODCAST DETAILS

| Property | Value |
|----------|-------|
| **Event ID** | 91202b13-3e65-4870-885f-f4a66e221eed |
| **Title** | Seasonal Promotion Launch - Spring Collection |
| **File Name** | amp_podcast_91202b13_Seasonal_Promotion_Launch_-_Sp_20260225_124233.wav |
| **File Format** | WAV (high quality) |
| **File Size** | 2.43 MB |
| **Duration** | 57 seconds |
| **Narrator** | Professional |
| **Tracking ID** | 73ca6d401b579d56 |
| **Created** | February 25, 2026 @ 12:42:33 |

---

## 🚀 HOW TO USE

### **Option 1: Play Online** (Recommended for Testing)
1. Click: **http://localhost:8888**
2. Use web player to listen
3. Click "📋 Copy URL" to get shareable link
4. Click "⬇️ Download" to get file

### **Option 2: Email Distribution**
```
File Path: C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\AMP\Zorro\output\podcasts\amp_podcast_91202b13_Seasonal_Promotion_Launch_-_Sp_20260225_124233.wav

Subject: 📢 Spring Collection Launch - Listen Now (57 sec)

Body:
Listen to today's announcement about our Spring Collection:

You can play it here:
http://localhost:8888/podcasts/amp_podcast_91202b13_Seasonal_Promotion_Launch_-_Sp_20260225_124233.wav

Or download and listen offline.
```

### **Option 3: Direct File Access**
- Right-click the file path above
- Select "Open with" → Choose any media player
- Or drag to your email to attach

---

## 📱 EMBED CODE (For Web/Dashboard)

```html
<audio controls style="width: 100%; max-width: 500px;">
  <source src="http://localhost:8888/podcasts/amp_podcast_91202b13_Seasonal_Promotion_Launch_-_Sp_20260225_124233.wav" type="audio/wav">
  Your browser does not support the audio element.
</audio>
```

---

## 📊 ANALYTICS TRACKING

**Tracking ID:** `73ca6d401b579d56`

Use this ID to track:
- Download count
- Play events
- Listener engagement
- Time on page
- Device type

---

## ⚙️ SERVER MANAGEMENT

### Start Server
```powershell
cd "C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\AMP\Zorro"
python podcast_server.py
```

### Stop Server
Press `Ctrl+C` in the terminal

### Server Endpoints
- `http://localhost:8888/` - Web player interface
- `http://localhost:8888/podcasts/[filename]` - Direct file download
- `http://localhost:8888/metadata/[id].json` - Podcast metadata

---

## ✨ NEXT STEPS

1. **Test:** Open http://localhost:8888 in your browser
2. **Play:** Click the audio player to listen
3. **Download:** Use the download button for permanent copy
4. **Share:** Copy the direct link to email/chat
5. **Create More:** Run `create_real_podcast.py` again for other AMP events

---

## 🔧 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "Cannot reach localhost" | Ensure server is running: `python podcast_server.py` |
| "Connection refused" | Server crashed - restart it |
| "File not found" | Regenerate podcast: `python create_real_podcast.py` |
| "Port already in use" | Change port in `podcast_server.py` line 141 |

---

## 📁 FILE LOCATIONS

```
Store Support/Projects/AMP/Zorro/
├── create_real_podcast.py          ← Generate new podcasts
├── podcast_server.py               ← Start/stop local server
└── output/
    ├── podcasts/                   ← Podcast files
    │   └── amp_podcast_91202b13_...wav
    └── metadata/                   ← Podcast metadata
        └── 8b1a274d.json
```

---

**Status: ✅ LIVE AND WORKING | Server: http://localhost:8888**
