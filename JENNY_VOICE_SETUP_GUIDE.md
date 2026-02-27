# Jenny Voice SAPI5 Bridge - Setup Guide

## Overview
This guide enables the Microsoft Jenny voice (Narrator) for use with SAPI5 System.Speech.Synthesis API by bridging OneCore registry entries to SAPI5.

## What This Does
- **Locates** the OneCore Jenny voice registration in Windows registry
- **Exports** the registry configuration 
- **Adapts** paths from OneCore stack to SAPI5 stack
- **Registers** Jenny with SAPI5 so `System.Speech.Synthesis` can access it

## Why It's Needed
- Jenny voice ships as a **OneCore voice** (Windows.Media.SpeechSynthesis API)
- Your audio generation uses **SAPI5** (System.Speech.Synthesis API)
- These are two separate audio stacks with no automatic bridge
- Manual registry bridge connects them

## Prerequisites

**Required:**
- ✅ Windows 10 or Windows 11
- ✅ Jenny voice installed (verify in Settings > Accessibility > Text-to-speech)
- ✅ Administrator PowerShell access
- ✅ Registry Editor (built-in to Windows)

**Optional but recommended:**
- Backup of current system registry (already automated in script)

## Two Approaches

### Option A: Automated (Recommended) ⭐

**Safest and fastest - uses PowerShell script**

**Steps:**

1. **Open PowerShell as Administrator**
   - Press: `Win + X`
   - Select: "Windows PowerShell (Admin)" or "Terminal (Admin)"
   - Confirm: "Do you want to allow this app to make changes?"

2. **Navigate to Activity-Hub directory**
   ```powershell
   cd "C:\Users\krush\Documents\VSCode\Activity-Hub"
   ```

3. **Run the bridge script**
   ```powershell
   .\enable_jenny_sapi5.ps1
   ```

4. **Script will:**
   - ✅ Verify admin privileges
   - ✅ Find Jenny voice in OneCore registry
   - ✅ Create backup of registry (saved to `Registry-Backups/`)
   - ✅ Export OneCore configuration
   - ✅ Create SAPI5-compatible registry entries
   - ✅ Update all path references
   - ✅ Verify changes

5. **Restart PowerShell** (close and reopen)

6. **Verify Jenny is accessible**
   ```powershell
   python check_sapi5_voices.ps1
   ```
   - Should show: `Microsoft Jenny Desktop` ✅

---

### Option B: Manual Registry Edit (Advanced)

**If you prefer manual control or the script doesn't find Jenny**

**Steps:**

1. **Open Registry Editor**
   - Press: `Win + R`
   - Type: `regedit`
   - Press: Enter
   - Confirm: "Do you want to allow this app to make changes?"

2. **Navigate to OneCore voices**
   - Go to: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens`
   - Look for a key containing "Jenny" (e.g., `TTS_MS_EN-US_Jenny_11.0`)

3. **Export the key**
   - Right-click the Jenny key
   - Select: "Export"
   - Save as: `Jenny-OneCore.reg` (e.g., Desktop)

4. **Edit the .reg file**
   - Right-click the .reg file
   - Select: "Open with" > "Notepad"
   - Find and replace all instances:
     - Replace: `Speech_OneCore`
     - With: `Speech`
   - Find and replace the key name:
     - Replace: `TTS_MS_EN-US_Jenny_11.0` (or whatever it is)
     - With: `TTS_MS_EN-US_Jenny_SAPI5`
   - Save the file (Ctrl+S)

5. **Import the modified registry**
   - Close Notepad
   - Double-click the edited .reg file
   - Confirm: "Are you sure you want to add..."
   - Success: "Information has been successfully entered into the registry"

6. **Restart PowerShell**

7. **Verify**
   ```powershell
   python check_sapi5_voices.ps1
   ```

---

## Verification

**After completing either approach:**

```powershell
cd "C:\Users\krush\Documents\VSCode\Activity-Hub"
python check_sapi5_voices.ps1
```

**Expected output:**
```
Available SAPI5 Voices:
  • Microsoft David Desktop (Male)
  • Microsoft Jenny Desktop (Female) ← NEW
  • Microsoft Zira Desktop (Female)
```

---

## Troubleshooting

### Problem: "Jenny not found in OneCore registry"

**Cause:** Jenny voice may not be installed

**Solution:**
1. Go to: Settings > Accessibility > Text-to-speech
2. Look for "Manage voices"
3. Check if Jenny is listed
4. If not, try downloading from Microsoft Store
5. Try Option B (manual) with actual key name from your system

### Problem: "Permission denied when importing .reg"

**Cause:** PowerShell or Registry Editor not opened as Administrator

**Solution:**
1. Close Registry Editor
2. Right-click regedit.exe
3. Select: "Run as administrator"
4. Try importing again

### Problem: Script shows "Path not accessible"

**Cause:** Your Windows build may use different registry path

**Solution:**
1. Use Option B (manual) to locate exact key name
2. Modify the script's `$oneCorePath` variable with correct path
3. Run script again

### Problem: Jenny still not showing after restart

**Cause:** Application may need to reload voice cache

**Solution:**
1. Close all audio generation applications
2. Close all PowerShell windows
3. Open fresh PowerShell (as Admin)
4. Try again: `python check_sapi5_voices.ps1`

### Problem: "Error: 0x80070005 Access Denied"

**Cause:** Registry permissions or antivirus blocking

**Solution:**
1. Temporarily disable antivirus/Windows Defender
2. Run script as Administrator
3. Check that Jenny OneCore key exists (verify with Manual option)
4. Re-enable antivirus when done

---

## After Jenny is Enabled

Once Jenny shows in SAPI5 voices:

1. **Update audio generation script**
   - Edit: `generate_both_voices.py`
   - Add Jenny to voice list:
     ```python
     voices = [
         "Microsoft David Desktop",
         "Microsoft Zira Desktop",
         "Microsoft Jenny Desktop"  # NEW
     ]
     ```

2. **Generate audio with Jenny**
   ```powershell
   python generate_both_voices.py
   ```
   - Will create additional MP4 files for Jenny voice

3. **Convert to MP4**
   ```powershell
   python convert_wav_to_mp4_installer.py
   ```
   - Converts new Jenny files automatically

---

## Registry Backup Recovery

If something goes wrong and you need to undo:

1. Navigate to: `C:\Users\krush\Documents\VSCode\Activity-Hub\Registry-Backups\`
2. Find the backup file with timestamp
3. Double-click the .reg file to restore
4. Windows will merge the original OneCore settings back

---

## References

- **OneCore Path:** `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens`
- **SAPI5 Path:** `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens`
- **Voice Package:** `MicrosoftWindows.Voice.en-US.Jenny`
- **API:** System.Speech.Synthesis (SAPI5)

---

**Ready to proceed? Choose Option A (script) or Option B (manual), then follow the verification steps.**
