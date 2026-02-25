"""Generate podcast using Windows.Media.SpeechSynthesis API (supports OneCore/Narrator voices)."""

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

def generate_with_windows_media_api(voice_display_name, output_label):
    """Generate podcast using Windows.Media.SpeechSynthesis API."""
    
    output_file = f"Store Support/Projects/AMP/Zorro/output/podcasts/amp_podcast_91202b13_{output_label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    # PowerShell script using Windows.Media.SpeechSynthesis (OneCore API)
    ps_script = f"""
# Add required assemblies for WinRT
Add-Type -AssemblyName System.Runtime.WindowsRuntime
Add-Type -AssemblyName System.IO.Compression

# Load Windows.Media.SpeechSynthesis
[Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Foundation,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null

Write-Host "Using Windows.Media.SpeechSynthesis API (OneCore)"
Write-Host ""

# Get all voices
$allVoices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
Write-Host "Total voices available: $($allVoices.Count)"

# List all voices
Write-Host ""
Write-Host "Available voices:"
foreach ($v in $allVoices) {{
    Write-Host "  • $($v.DisplayName) [$($v.Language)]"
}}

# Find the requested voice
Write-Host ""
Write-Host "Looking for: {voice_display_name}"
$selectedVoice = $allVoices | Where-Object {{ $_.DisplayName -eq "{voice_display_name}" }}

if ($selectedVoice) {{
    Write-Host "✓ Found: $($selectedVoice.DisplayName)"
    Write-Host ""
    Write-Host "Generating audio file..."
    
    # Create synthesizer
    $synthesizer = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    $synthesizer.Voice = $selectedVoice
    
    # Create output file stream
    $file = [Windows.Storage.StorageFile]::GetFileFromPathAsync("{output_file}").AsTask().Result
    
    try {{
        # Create output stream for audio file
        $outputStream = $file.OpenAsync([Windows.Storage.FileAccessMode]::ReadAndWrite).AsTask().Result
        
        # Synthesize speech to stream
        $asyncTask = $synthesizer.SynthesizeTextToStreamAsync($message).AsTask()
        
        # Wait for synthesis to complete
        $null = $asyncTask.Result
        $outputStream.Dispose()
        
        Write-Host "✓ Audio generated: {output_file}"
        
        # Get file size
        $fileInfo = Get-Item "{output_file}"
        $sizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
        Write-Host "  Size: $sizeMB MB"
        
    }} catch {{
        Write-Host "Error during synthesis: $_"
    }}
    
}} else {{
    Write-Host "✗ Voice not found: {voice_display_name}"
    Write-Host ""
    Write-Host "Available voices:"
    $allVoices | ForEach-Object {{ Write-Host "  - $($_.DisplayName)" }}
}}
"""
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
            return os.path.basename(output_file)
            
    except Exception as e:
        print(f"Error: {e}")
    
    return None

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 70)
print("PODCAST GENERATION - WINDOWS.MEDIA.SPEECHSYNTHESIS API")
print("=" * 70)
print()
print("Using OneCore/Narrator voice system (can access Jenny, Aria, Guy, etc.)")
print()

# Try to generate with Jenny
print("Attempting to generate with Microsoft Jenny...")
jenny = generate_with_windows_media_api("Microsoft Jenny", "jenny_windows_media")

print()
print("=" * 70)

if jenny:
    print(f"✅ SUCCESS! Generated with Jenny: {jenny}")
    print(f"🎙️  Listen at: http://localhost:8888")
else:
    print("⚠️  Jenny not accessible via Windows.Media API either")
    print()
    print("This could mean:")
    print("  • Jenny installation is incomplete")
    print("  • Windows.Media API requires additional setup")
    print()
    print("Fallback: Use SAPI 5 voices (David or Zira)")
    print("  Run: python generate_both_voices.py")
