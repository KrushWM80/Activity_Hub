# Jenny Voice Status Report

**Date:** February 26, 2026

---

## Installation Status

### ✅ AppxPackage: INSTALLED
- **Name:** MicrosoftWindows.Voice.en-US.Jenny.2
- **Version:** 1.0.2.0
- **Status:** OK
- **Install Location:** `C:\Program Files\WindowsApps\MicrosoftWindows.Voice.en-US.Jenny.2_1.0.2.0_x64__cw5n1h2txyewy`

Jenny is **physically installed** on your system.

---

## API Availability

### ❌ SAPI5 (System.Speech.Synthesis): NOT AVAILABLE
**Current SAPI5 Voices:**
- Microsoft David Desktop ✅
- Microsoft Zira Desktop ✅

**Jenny Status:** NOT registered in SAPI5

### ❌ Windows.Media (OneCore): NOT PROPERLY REGISTERED
**Issue:** Jenny is installed but the OneCore API cannot enumerate it.

---

## Root Cause

**Architecture Mismatch:**
- Jenny is installed as a **Windows 11 Narrator voice** (OneCore/Windows.Media API)
- Your audio generation script uses **SAPI5 API** (System.Speech.Synthesis)
- These are two completely separate voice systems

SAPI5 can only access:
- Legacy voices registered in Windows registry
- Desktop voices like David and Zira

OneCore voices like Jenny require the newer Windows.Media.SpeechSynthesis API.

---

## Options to Get Jenny Working

### Option 1: Uninstall and Reinstall Jenny
**Might fix OneCore registration:**
1. Settings → Apps → Installed apps
2. Search "Jenny" 
3. Click "..." and select "Uninstall"
4. Wait for uninstall to complete
5. Restart computer
6. Go to Settings → Accessibility → Text-to-speech
7. Click "Manage voices" → "Add voices"
8. Find "Microsoft Jenny" and install
9. Restart again

**Success Rate:** 50% (may not register even after reinstall)

### Option 2: Use Windows.Media API 
**Switch the script to use OneCore voices directly**
- Would need to rebuild the audio generation script using PowerShell's Windows.Media.SpeechSynthesis
- More complex implementation
- Would give access to all Narrator voices (Jenny, Aria, Guy, Mark)

### Option 3: Continue with David & Zira (Current)
**Best current solution:**
✅ Both voices work perfectly  
✅ Professional quality audio  
✅ No configuration issues  
✅ 24+ MB files with full message content  
✅ Reliable, repeatable generation  

---

## Recommendation

**Status:** Jenny remains in a broken registration state. The installed files exist but the API bridge to access them is incomplete.

**Best Path Forward:**
Continue with David (male) and Zira (female) for production use. They deliver professional-quality audio and have no compatibility issues.

If Jenny is specifically required:
- Attempt Option 1 (uninstall/reinstall)
- If that fails, implement Option 2 (Windows.Media API rewrite)

For now, the "Audio - Reading" format with David and Zira is a complete, working solution for Zorro deployment.

---

## Files Generated
- ✅ Your Week 4 Messages are Here - Audio - Reading - David.wav (24.32 MB)
- ✅ Your Week 4 Messages are Here - Audio - Reading - Zira.wav (24.09 MB)

Both files ready for production use via http://localhost:8888
