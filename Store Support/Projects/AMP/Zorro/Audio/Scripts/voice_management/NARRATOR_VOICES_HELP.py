"""Final troubleshooting to enable Narrator voices for SAPI5."""

print("""
================================================================================
GETTING NARRATOR VOICES (JENNY, GUY, ARIA) TO WORK WITH SAPI5
================================================================================

PROBLEM:
  Jenny (and other Narrator voices) are installed in Windows 11 but aren't
  accessible through the SAPI5 API that our Python scripts use.

ROOT CAUSE:
  • Narrator voices use the newer Windows.Media API
  • SAPI5 (System.Speech) doesn't automatically bridge to them
  • Windows needs them to be copied/linked to SAPI5 registry

SOLUTION - Try ONE of these:

================================================================================
METHOD 1: Restart (Most Likely to Work)
================================================================================

Any new voice installation sometimes requires a restart:

  1. Close all PowerShell windows
  2. RESTART YOUR COMPUTER
  3. After restart, open new PowerShell
  4. Run: python list_exact_voices.py
     (Should now show Jenny, Guy, etc.)
  5. Then run: python generate_jenny_guy.py

Try this FIRST before other methods!

================================================================================
METHOD 2: Verify Narrator Setup in Settings
================================================================================

Navigate to verify the installation is complete:

  1. Open Windows Settings (Windows Key + I)
  2. Go to: Accessibility > Text-to-speech
  3. Look at "Voice" section
  4. For each voice (Jenny, Guy), verify:
     ✓ Status shows "Installed" (not "Install")
     ✓ Not grayed out
  5. If any show "Install", click to install them
  6. After installation completes:
     • Close all PowerShell windows
     • Restart your computer
     • Try again

================================================================================
METHOD 3: Register Narrator Voices Manually (Advanced)
================================================================================

Some Windows 11 setups need manual SAPI5 registry entries:

  1. Open Registry Editor (Win+R, type: regedit)
  2. Navigate to: HKEY_LOCAL_MACHINE > SOFTWARE > Microsoft > Speech > Voices > Tokens
  3. Create new key for each Narrator voice
  4. (Detailed steps available if needed)

  NOTE: This is advanced and risky. Try Method 1 first!

================================================================================
METHOD 4: Alternative - Use Aria Instead (May Work Better)
================================================================================

Aria might register better than Jenny:

  1. Settings > Accessibility > Text-to-speech > Manage voices
  2. Click "Add voices"
  3. Find "Microsoft Aria" and install it
  4. Restart computer
  5. Run: python list_exact_voices.py
  6. If Aria appears, run: python generate_jenny_guy.py
     (Update it to use Aria instead)

================================================================================
IMMEDIATE NEXT STEPS
================================================================================

1. Try METHOD 1 (Restart) - easiest and most effective
   • Restart your computer
   • Run: python list_exact_voices.py
   • If Jenny/Guy show up, you're good!

2. If they still don't appear:
   • Try METHOD 2 (Verify in Settings)
   • Ensure voice status is "Installed"
   • Do another restart if needed

3. Current workaround:
   • Use David or Zira (both work perfectly)
   • Access at: http://localhost:8888

================================================================================

Need help? Run: python list_exact_voices.py

That will show exactly what voices are currently available.
""")
