"""Generate podcast with proper assembly loading for SAPI5."""

import os
import sys
import json
from datetime import datetime
import subprocess
import time

message_body = """
WEEK 2 - 2/21 - 2/27

FOOD & CONSUMABLES UPDATE:
The following items need your attention this week:
Beauty Department - Complete lipstick reset, organize nail polish alphabetically, review expiration dates, restock samples, feature new skincare line.
Food Department - Organize dairy section, rebrand organic products, stock items, deep clean coolers, process deliveries.
Fresh Department - Reset produce display for promotion, verify dates, organize frozen items, clean prep areas, update labels.

GENERAL MERCHANDISE:
Entertainment - Reset movie and gaming section by release date.
Fashion - Feature spring collection, organize by size and color.
Hardlines - Stock seasonal items.
Home - Reset décor for season.
Seasonal - Create eye-catching displays.

OPERATIONS PRIORITIES:
Asset Protection - Daily security walks, monitor theft areas.
Backroom - Organize and label, FIFO rotation.
Front End - Process efficiently, maintain checkout.
Store Fulfillment - Pick accurately, maintain schedule.
People - Proper scheduling and training.
""".strip()

def generate_with_sapi5():
    """Generate using Windows SAPI5 via PowerShell with proper assembly loading."""
    
    output_file = os.path.join(
        "Store Support/Projects/AMP/Zorro/output/podcasts",
        f"amp_podcast_91202b13_sapi5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    
    # PowerShell script with assembly loading
    ps_script = f'''
# Load the required assembly
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null

$text = @"
{message_body}
"@

$outputFile = "{output_file}"

# Create SAPI5 synthesizer
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Configure speech
$synthesizer.Rate = -2
$synthesizer.Volume = 100

# Select female voice if available
$voices = $synthesizer.GetInstalledVoices()
Write-Host "Available voices: $($voices.Count)"
foreach ($voice in $voices) {{
    $vinfo = $voice.VoiceInfo
    Write-Host "  - $($vinfo.Name) [$($vinfo.Gender)]"
    if ($vinfo.Gender -eq 'Female') {{
        $synthesizer.SelectVoice($vinfo.Name)
        Write-Host "    Selected: $($vinfo.Name)"
        break
    }}
}}

# Generate audio file
try {{
    Write-Host "Generating audio..."
    $synthesizer.SetOutputToWaveFile($outputFile)
    $synthesizer.Speak($text)
    
    # Important: flush and close properly
    $synthesizer.SetOutputToNull()
    $synthesizer.Dispose()
    
    Start-Sleep -Milliseconds 500
    
    # Verify file was created
    if (Test-Path $outputFile) {{
        $fileInfo = Get-Item $outputFile
        $size = $fileInfo.Length / 1024 / 1024
        Write-Host ""
        Write-Host "✅ SUCCESS! Audio generated:"
        Write-Host "   File: $outputFile"
        Write-Host "   Size: $($size.ToString('F2')) MB"
        
        # Read WAV header to verify
        $bytes = Get-Content $outputFile -Encoding Byte -TotalCount 4
        $header = [System.Text.Encoding]::ASCII.GetString($bytes)
        if ($header -eq 'RIFF') {{
            Write-Host "   Format: Valid WAV file ✓"
        }} else {{
            Write-Host "   Format: Unexpected header ⚠️"
        }}
    }} else {{
        Write-Host "❌ File not created"
        exit 1
    }}
}} catch {{
    Write-Host "❌ Error: $_"
    exit 1
}}
'''
    
    # Write PowerShell script
    ps_file = "temp_generate_podcast_fixed.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    try:
        result = subprocess.run(
            [
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-File", ps_file
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr and "assembly" not in result.stderr.lower():
            print("Warnings:", result.stderr)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
            print(f"\n📻 Access via: http://localhost:8888")
            return output_file
        else:
            print("❌ File generation failed or file too small")
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout waiting for audio generation")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if os.path.exists(ps_file):
            try:
                os.remove(ps_file)
            except:
                pass
    
    return None

# Ensure output directory
os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 60)
print("PODCAST GENERATION - WINDOWS SAPI5 SYNTHESIS")
print("=" * 60)
print()

result = generate_with_sapi5()

if not result:
    print("\n❌ Generation failed - trying fallback...")
    sys.exit(1)
