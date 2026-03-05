# Chirp 3 HD Voices Setup Guide

## Overview

This guide explains how to set up Google Cloud Vertex AI Chirp 3 HD voices for the AMP Activity-Hub. Chirp 3 offers superior audio quality compared to standard voices.

## What is Chirp 3 HD?

- **Provider**: Google Cloud Vertex AI
- **Quality Level**: HD (24kHz sample rate)
- **Available Voices**: 
  - **Achird**: Professional male voice
  - **Bemrose**: Professional female voice
- **Audio Output**: MP3 format
- **Cost**: Pay-per-use (typically $0.004-0.016 per 1,000 words)

## Prerequisites

- ✅ Active Google Cloud Account (or create one at https://cloud.google.com)
- ✅ Billing enabled on your Google Cloud project
- ✅ Python 3.7+ (already have this)
- ✅ VS Code with Activity-Hub workspace open

## Step 1: Create a Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com
   - Sign in with your Google account

2. **Create a new project**
   - Click "Select a Project" dropdown (top left)
   - Click "NEW PROJECT"
   - **Project Name**: `AMP-Activity-Hub-Voices`
   - **Organization**: (optional)
   - Click "CREATE"

3. **Wait for project to be created** (usually takes 1-2 minutes)

## Step 2: Enable the Text-to-Speech API

1. **Select your new project** from the dropdown

2. **Search for Text-to-Speech API**
   - In the search bar, type: "Text-to-Speech API"
   - Click the result

3. **Click "ENABLE"**
   - Wait for the API to be enabled (1-2 minutes)

4. **Verify it's enabled**
   - You should see "APIs & Services" > "Text-to-Speech API" in your dashboard

## Step 3: Create a Service Account and Key

1. **Go to Service Accounts**
   - In left sidebar: APIs & Services > Credentials
   - Click "Create Credentials" (top)
   - Select "Service Account"

2. **Configure Service Account**
   - **Service account name**: `amp-activity-hub-voice-generator`
   - **Service account ID**: (auto-filled, keep as-is)
   - Click "CREATE AND CONTINUE"

3. **Grant Permissions**
   - **Select a role**: Search for "Text-to-Speech Admin"
   - Select: `Cloud Text-to-Speech Admin`
   - Click "CONTINUE"

4. **Create a Key**
   - Click "CREATE KEY"
   - Choose format: **JSON**
   - Click "CREATE"
   - A JSON file will download automatically
   - **IMPORTANT**: Save this file securely

## Step 4: Set Up Environment Variable

1. **Save the JSON credentials file**
   - Rename it to: `gcp-credentials.json`
   - Save to: `C:\Users\krush\Documents\VSCode\Activity-Hub\gcp-credentials.json`
   - ⚠️ **DO NOT** commit this to git! Add to `.gitignore`

2. **Add to .gitignore** (if you have one)
   ```
   gcp-credentials.json
   ```

3. **Set Environment Variable** (Windows PowerShell)
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\Documents\VSCode\Activity-Hub\gcp-credentials.json"
   ```
   
   To make it permanent:
   ```powershell
   [Environment]::SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", "C:\Users\krush\Documents\VSCode\Activity-Hub\gcp-credentials.json", "User")
   ```

4. **Verify it's set**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS
   ```
   Should display the path you just set.

## Step 5: Install Google Cloud Python Client

```powershell
cd "C:\Users\krush\Documents\VSCode\Activity-Hub"
pip install google-cloud-texttospeech
```

Verify installation:
```powershell
pip list | grep google
```

Should show: `google-cloud-texttospeech`

## Step 6: Generate Chirp 3 Voices

1. **Set credentials in PowerShell**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\Documents\VSCode\Activity-Hub\gcp-credentials.json"
   ```

2. **Run the generator**
   ```powershell
   cd "C:\Users\krush\Documents\VSCode\Activity-Hub"
   python generate_chirp3_voices.py
   ```

3. **Expected Output**
   ```
   ============================================================
   GOOGLE CLOUD VERTEX AI - CHIRP 3 HD VOICE GENERATOR
   ============================================================

   ============================================================
   CHIRP 3 HD VOICE GENERATION
   ============================================================

   Available voices: achird (Male), bemrose (Female)

   ============================================================
   Generating Chirp3 HD Achird Voice
   ============================================================
   Voice: en-US-Chirp3-HD-Achird
   Gender: Male
   Language: en-US
   Audio Format: MP3 (HD Quality)

   Generating audio... ✅ Complete
   ...
   
   ============================================================
   GENERATION SUMMARY
   ============================================================

   ✅ Successful: 2/2
      • Your Week 4 Messages are Here - Audio - Reading - Chirp3 Achird.mp3 (X.XX MB)
      • Your Week 4 Messages are Here - Audio - Reading - Chirp3 Bemrose.mp3 (X.XX MB)
   ```

## Step 7: Convert MP3 to MP4 (Optional)

If you want MP4 format in addition to MP3:

```powershell
python convert_wav_to_mp4_installer.py
```

Note: The script is designed for WAV files, but MP3 works too.

## Available Voices

### Achird (Male)
- **Language**: English (US)
- **Style**: Professional, authoritative, clear
- **Best for**: Business presentations, technical content, formal narration
- **Sample**: Corporate updates, store announcements

### Bemrose (Female)
- **Language**: English (US)
- **Style**: Professional, confident, engaging
- **Best for**: Training content, engaging narratives, customer-facing content
- **Sample**: Welcome messages, feature announcements

## Voice Comparison

| Feature | David | Zira | Chirp3-Achird | Chirp3-Bemrose |
|---------|-------|------|---------------|----------------|
| **Quality** | Standard | Standard | HD (24kHz) | HD (24kHz) |
| **Naturalness** | Good | Good | Excellent | Excellent |
| **Gender** | Male | Female | Male | Female |
| **Voice Type** | SAPI5 | SAPI5 | Cloud AI | Cloud AI |
| **Cost** | Free | Free | Pay-per-use | Pay-per-use |
| **File Format** | WAV/MP4 | WAV/MP4 | MP3 | MP3 |

## File Locations

After generation, files are saved to:
```
Store Support\Projects\AMP\Zorro\output\podcasts\
```

Files created:
- `Your Week 4 Messages are Here - Audio - Reading - Chirp3 Achird.mp3`
- `Your Week 4 Messages are Here - Audio - Reading - Chirp3 Bemrose.mp3`

Plus original files:
- `Your Week 4 Messages are Here - Audio - Reading - David.wav`
- `Your Week 4 Messages are Here - Audio - Reading - David.mp4`
- `Your Week 4 Messages are Here - Audio - Reading - Zira.wav`
- `Your Week 4 Messages are Here - Audio - Reading - Zira.mp4`

## Total Voice Options

After generation, you'll have:

✅ **David** (Male, SAPI5) - WAV + MP4  
✅ **Zira** (Female, SAPI5) - WAV + MP4  
✅ **Chirp3-Achird** (Male, Cloud) - MP3  
✅ **Chirp3-Bemrose** (Female, Cloud) - MP3  

**Total: 4 professional voice options** for the Activity-Hub!

## Cost Estimates

Google Cloud Text-to-Speech pricing (as of Feb 2026):
- **Standard voices**: ~$0.004 per 1,000 words
- **Neural voices**: ~$0.016 per 1,000 words

Your message is ~1,800 words:
- **One generation**: ~$0.03 (standard) or ~$0.13 (neural)
- **Cost per voice option** is minimal

## Troubleshooting

### Error: "GOOGLE_APPLICATION_CREDENTIALS not set"

**Solution**: The environment variable wasn't loaded. Try:
1. Close and reopen PowerShell
2. Run again: `python generate_chirp3_voices.py`

### Error: "ModuleNotFoundError: No module named 'google.cloud'"

**Solution**: Install the package:
```powershell
pip install google-cloud-texttospeech
```

### Error: "Permission denied" or "Invalid credentials"

**Solution**: 
1. Verify the JSON file path is correct
2. Check file exists: `Test-Path "C:\Users\krush\Documents\VSCode\Activity-Hub\gcp-credentials.json"`
3. Verify Text-to-Speech API is enabled in Google Cloud Console
4. Check service account has "Cloud Text-to-Speech Admin" role

### Error: "API has not been used in project"

**Solution**: 
1. Go to https://console.cloud.google.com
2. Ensure your project is selected
3. Search for "Text-to-Speech API"
4. Click "Enable"
5. Wait 2-3 minutes before retrying

### Error: "Quota exceeded"

**Solution**: You've hit the quota limit. Options:
- Wait until the quota resets (usually daily)
- Contact Google Cloud support to increase quota
- For now, use David/Zira voices (unlimited, no quota)

## Next Steps

1. ✅ Complete setup above
2. ✅ Generate Chirp3 voices
3. ✅ Verify files in output directory
4. ✅ Test in web player (localhost:8888)
5. ✅ Deploy all 4 voice options to Zorro

## Security Notes

**IMPORTANT**: 
- ⚠️ Never commit `gcp-credentials.json` to git
- ⚠️ Never share your credentials file
- ⚠️ Use service account with minimal permissions
- ✅ Store file securely in your local workspace only
- ✅ Set appropriate folder permissions (restrict to your user)

## Support

If you encounter issues:
1. Check the error message in the terminal
2. Review the Troubleshooting section above
3. Verify each step was completed correctly
4. Check Google Cloud Console for API status

---

**Ready to experience HD voice quality with Chirp 3?** Follow the steps above and run the generator!
