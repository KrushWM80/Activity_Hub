# FFmpeg Installation Guide for MP4 Conversion

## Quick Setup (5 minutes)

### Step 1: Download FFmpeg
1. Go to: **https://ffmpeg.org/download.html**
2. Under "Windows builds", click **"Windows builds by Gyan"**
3. Download **"ffmpeg-7.1-full_build.zip"** (or latest full_build)
   - Full build is required, not lite
   - Size: ~200 MB

### Step 2: Extract FFmpeg
1. Extract the ZIP file to: **`C:\ffmpeg`**
   - Your extracted folder should look like:
     ```
     C:\ffmpeg\bin\    (contains ffmpeg.exe)
     C:\ffmpeg\doc\
     C:\ffmpeg\presets\
     ```

### Step 3: Add to System PATH
1. **Right-click "This PC" → Properties**
2. Click **"Advanced system settings"** (left sidebar)
3. Click **"Environment Variables"** button
4. Under "System variables", click **"New"**
   - Variable name: `PATH`
   - Variable value: `C:\ffmpeg\bin`
5. Click **OK** three times
6. **Close and reopen PowerShell/terminal**

### Step 4: Verify Installation
```powershell
ffmpeg -version
```
Should return version information. ✅

### Step 5: Run Conversion
```powershell
python convert_wav_to_mp4_installer.py
```

---

## What Gets Converted

### Input (WAV files - keep as backup)
```
Your Week 4 Messages are Here - Audio - Reading - David.wav     (24.32 MB)
Your Week 4 Messages are Here - Audio - Reading - Zira.wav      (24.09 MB)
```

### Output (MP4 files - for testing)
```
Your Week 4 Messages are Here - Audio - Reading - David.mp4     (~10-12 MB)
Your Week 4 Messages are Here - Audio - Reading - Zira.mp4      (~10-12 MB)
```

**Note:** MP4 files will be smaller due to AAC audio codec compression (192 kbps bitrate)

---

## If You Get Errors

### "ffmpeg not found"
- Ensure PATH was added correctly
- Restart PowerShell after adding PATH
- Verify `C:\ffmpeg\bin\ffmpeg.exe` exists

### "Cannot write output file"
- Make sure podcasts directory exists
- Close any programs playing the WAV files
- Ensure write permissions for `Store Support\Projects\AMP\Zorro\output\podcasts\`

### Conversion is slow
- Normal for 24 MB audio files (5-10 seconds per file)
- Depends on disk speed and computer specs

---

## Alternative: Portable FFmpeg (No Installation)

If system PATH won't work:
1. Download ffmpeg as above
2. Extract to `C:\ffmpeg`
3. In PowerShell, run:
   ```powershell
   $env:PATH = "C:\ffmpeg\bin;$env:PATH"
   python convert_wav_to_mp4_installer.py
   ```

---

## MP4 Specifications

After conversion, both WAV and MP4 will be available:

| Format | Codec | Bitrate | Container | Size | Use Case |
|--------|-------|---------|-----------|------|----------|
| **WAV** | PCM | 1411 kbps | WAV | 24 MB | Archive, lossless backup |
| **MP4** | AAC | 192 kbps | MP4 | ~11 MB | Web delivery, testing, streaming |

Both formats preserve the complete audio message - just different compression levels.

---

## Testing

Once converted, you can test MP4 playback:
```powershell
Start-Process "Store Support\Projects\AMP\Zorro\output\podcasts\Your Week 4 Messages are Here - Audio - Reading - David.mp4"
```

Or access via web server: **http://localhost:8888**

