"""Use Windows.Media.SpeechSynthesis API (newer approach that supports Narrator voices)."""

import subprocess
import os
from datetime import datetime

message_body = """WEEK TWO: STORE OPERATIONS UPDATE

FOOD AND CONSUMABLES section.

Beauty Department: Complete lipstick reset. Organize nail polish alphabetically. Review expiration dates. Restock sample section. Feature new skincare line.

Food Department: Organize dairy section. Rebrand organic products. Stock high-demand items. Deep clean coolers. Process new deliveries.

Fresh Department: Reset produce display. Verify expiration dates. Organize frozen items. Clean prep areas. Update pricing labels.

GENERAL MERCHANDISE: Entertainment reset, Fashion spring collection, Hardlines seasonal stock, Home décor, and Seasonal displays.

OPERATIONS: Asset Protection security walks, Backroom organization and FIFO, Front End efficiency, Store Fulfillment accuracy, and People scheduling."""

output_file = f"Store Support/Projects/AMP/Zorro/output/podcasts/amp_podcast_91202b13_jenny_narrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

# Use Windows.Media.SpeechSynthesis API which supports all Narrator voices
ps_script = f"""
Add-Type -AssemblyName System.Runtime.WindowsRuntime

# Load WinRT APIs
[Windows.Foundation.Metadata.ApiInformation,Windows.Foundation.Metadata,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime] | Out-Null

# Get all available voices in Windows 11
$voices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
Write-Host "Available Windows.Media voices:"
foreach ($voice in $voices) {{
    Write-Host "  - $($voice.DisplayName) [$($voice.Language)]"
}}

Write-Host ""

# Find and use Jenny voice
$jennyVoice = $voices | Where-Object {{ $_.DisplayName -like "*Jenny*" }}

if ($jennyVoice) {{
    Write-Host "✓ Found Jenny voice: $($jennyVoice.DisplayName)"
    Write-Host "  Language: $($jennyVoice.Language)"
    Write-Host ""
    Write-Host "Generating audio..."
    
    $synthesizer = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    $synthesizer.Voice = $jennyVoice
    
    # Set output file
    $audioFile = New-Object Windows.Storage.StorageFile  # This won't work directly
    
    Write-Host "Note: Windows.Media API requires complex stream handling"
    Write-Host "      This approach works but needs stream file writing"
    
}} else {{
    Write-Host "✗ Jenny voice not found"
    Write-Host ""
    Write-Host "Available voices:"
    $voices | ForEach-Object {{ Write-Host "  - $($_.DisplayName)" }}
}}
"""

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 70)
print("USING WINDOWS.MEDIA SPEECHSYNTHESIS API")
print("=" * 70)
print()
print("This is the modern Windows 11 API that supports Narrator voices...")
print()

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_script],
    capture_output=True,
    text=True,
    timeout=15
)

print(result.stdout)

if "Jenny" in result.stdout and "Found" in result.stdout:
    print()
    print("=" * 70)
    print("✓ JENNY FOUND IN WINDOWS.MEDIA API!")
    print("=" * 70)
    print()
    print("However, the Windows.Media API requires complex stream handling.")
    print("Standard PowerShell/System.Speech cannot directly create WAV files with it.")
    print()
    print("RECOMMENDATION:")
    print()
    print("Option 1: Use 'Aria' voice (if you also installed it)")
    print("  It may be more compatible with SAPI5")
    print()
    print("Option 2: Generate with David or Zira (the working SAPI5 voices)")
    print("  Run: python generate_both_voices.py")
    print()
    print("Option 3: Use a Python library with full Windows.Media support")
    print("  Try edge-tts (works with Microsoft Azure TTS)")
    print("  or use a different TTS solution")
    print()
else:
    print()
    print("=" * 70)
    print("ALTERNATIVE SOLUTION")
    print("=" * 70)
    print()
    print("Since Jenny won't work with SAPI5, here are your best options:")
    print()
    print("1. GENERATE WITH BOTH DAVID & ZIRA (SAPI5 voices)")
    print("   These are the highest quality built-in voices")
    print("   Run: python generate_both_voices.py")
    print()
    print("2. TRY INSTALLING 'ARIA' VOICE")
    print("   Settings > Accessibility > Text-to-speech > Manage voices")
    print("   Add 'Microsoft Aria' (might work better than Jenny)")
    print()
    print("3. USE EDGE-TTS WITH NEURAL VOICES")
    print("   Online service with high-quality voices")
    print("   Run: pip install edge-tts")
    print("   Then: edge-tts --voice en-US-Jenny --file output.mp3")
    print()
