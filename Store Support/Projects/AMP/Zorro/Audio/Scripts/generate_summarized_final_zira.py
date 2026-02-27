#!/usr/bin/env python3
"""
Generate Zira MP4 audio for Summarized Weekly Messages - Week 4
This is the FINAL, CORRECTED version from the morning's work.
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

def main():
    """Generate MP4 audio for Zira voice with correct script"""
    
    # CORRECT SCRIPT - As provided this morning
    week_script = """Hello! Your Week 4 Weekly Messages are Here!

Please Visit the Landing Page to access full content.

Entertainment Area Weekly Messages:

Dept. 72: PC Software Display Setup
Week 50 shipment: magnetic frame plus scannable insert (set immediately; ignore Hold for Anderson). Place on Electronics cash wrap near POS; message must face customer. Insert scannable sheet for checkout purchase. Upcoming POS prompt will remind associates to suggest PC software with laptop purchases. Featured SKUs: Norton VPN and 360 tiers, McAfee Total Protection, HR Block 2025 Basic and Deluxe. Actions: Install new placemat at cash wrap. Ensure price tags are printed and placed on laptop PC software fixtures. Questions: submit store ticket or email Tyler Jackson.

Dept. 72: Digital Storage Update
Industry-wide inventory constraints on SSDs and PC memory. Working to improve in-stocks for Week 16 modulars. Impacted items with no current restock date include select Kingston FURY DDR5 memory, NVIDIA RTX 5070 Ti, Samsung T7 and T9 portable SSDs, Samsung 990 EVO and PRO SSDs, and Seagate One Touch SSD. Supply improvements ongoing; may pivot to alternative SKUs as needed.

Fresh Area Weekly Messages:

Dept. 93: Lent is Here
Focus on 41 to 60 shrimp, salmon, and tilapia. Set features, aisle-locate items, and work seafood mods daily. Prepare for increased Lent demand.

Dept. 93: 4 lb Great Value Tilapia Rollback
Rollback: seventeen dollars and forty-seven cents. Expect twenty percent lift, thirty units per week. Stock up and merchandise prominently.

Dept. 93: St. Patrick's Day
Corned beef shipments building now. Feature corned beef and cabbage; no early markdowns. Watch for Corned Beef Kit and use lookup tool.

Dept. 93: Pork Rollbacks
Grilling season opportunity. Multiple pork items on Rollback. Clearly flag savings to drive unit sales.

Fashion Area Weekly Messages:

Dept. 29: Sleepwear Preview (Week 5 – Young Adult Women's Modular)
New merchandise arriving now. Ensure all updates are set per MBM for consistency and impact.

Licensed Shorty Sets (Category 2053)
Licensed short sleeve tee and tank with shorts sets. Markdown: Week 17, May 23 through 29.

No Boundaries Sidewall (Category 2357 and 2457)
Cloud Core cotton cami and short sets, chemises, tops and pants. Markdown: Week 12, April 18 through 24.

No Boundaries Satin Sets (Category 2405)
Satin cami and shorts sets. Markdown: Week 14, May 2 through 8.

That's your Week 4 Weekly Messages, Have a Great Week!"""
    
    # Output folder
    output_folder = Path("../output/podcasts")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 100)
    print("FINAL SUMMARIZED WEEKLY MESSAGES - ZIRA MP4 GENERATION")
    print("=" * 100)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Voice: Zira (Female)")
    print(f"Script: CORRECTED - Morning Version")
    print(f"Output Folder: {output_folder}")
    print(f"Format: MP4 (via WAV conversion)")
    print("\n" + "=" * 100 + "\n")
    
    # Generate WAV first
    wav_filename = "Weekly Messages Audio Template - Summarized - Week 4 - Zira.wav"
    wav_filepath = output_folder / wav_filename
    
    # Escape single quotes for PowerShell
    script_for_ps = week_script.replace("'", "''")
    
    # PowerShell command to generate WAV
    ps_commands = f"""
$text = @'
{script_for_ps}
'@

[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$tts.SelectVoice('Microsoft Zira Desktop')
$tts.Rate = -2
$tts.Volume = 100
$tts.SetOutputToWaveFile('{wav_filepath}')
$tts.Speak($text)
$tts.SetOutputToNull()
$tts.Dispose()

if (Test-Path '{wav_filepath}') {{
    $size = [math]::Round((Get-Item '{wav_filepath}').Length / 1MB, 2)
    Write-Host "WAV Created: ${{size}}MB"
}}
"""
    
    print(f"Step 1: Generating WAV file...")
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_commands],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if wav_filepath.exists():
            wav_size_mb = wav_filepath.stat().st_size / (1024 * 1024)
            print(f"✅ WAV Created: {wav_filename}")
            print(f"   Size: {wav_size_mb:.2f} MB\n")
        else:
            print(f"❌ Failed to create WAV file")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return
            
    except Exception as e:
        print(f"❌ Error generating WAV: {e}")
        return
    
    # Convert to MP4
    mp4_filename = "Weekly Messages Audio Template - Summarized - Week 4 - Zira.mp4"
    mp4_filepath = output_folder / mp4_filename
    
    print(f"Step 2: Converting WAV to MP4...")
    
    try:
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(wav_filepath),
            "-c:a", "aac",
            "-b:a", "128k",
            "-y",
            str(mp4_filepath)
        ]
        
        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if mp4_filepath.exists():
            mp4_size_mb = mp4_filepath.stat().st_size / (1024 * 1024)
            wav_size_mb = wav_filepath.stat().st_size / (1024 * 1024)
            compression = ((wav_size_mb - mp4_size_mb) / wav_size_mb * 100)
            
            print(f"✅ MP4 Created: {mp4_filename}")
            print(f"   Size: {mp4_size_mb:.2f} MB")
            print(f"   Compression: {compression:.1f}% reduction\n")
            
        else:
            print(f"❌ Failed to create MP4 file")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return
            
    except Exception as e:
        print(f"❌ Error converting to MP4: {e}")
        return
    
    # Step 3: Convert to Vimeo-compatible format with thumbnail
    vimeo_filename = "Weekly Messages Audio Template - Summarized - Week 4 - Zira - Vimeo.mp4"
    vimeo_filepath = output_folder / vimeo_filename
    thumbnail_path = output_folder / "merch_msg_thumbnail.jpeg"
    vimeo_created = False
    
    print(f"Step 3: Converting to Vimeo-compatible format...")
    
    if not thumbnail_path.exists():
        print(f"⚠️  Thumbnail not found at {thumbnail_path}")
        print(f"   Skipping Vimeo conversion (thumbnail required)")
        print(f"   Please add merch_msg_thumbnail.jpeg to the podcasts folder")
    else:
        try:
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-i", str(thumbnail_path),
                "-i", str(mp4_filepath),
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-preset", "medium",
                "-r", "25",
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                str(vimeo_filepath)
            ]
            
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if vimeo_filepath.exists():
                vimeo_size_mb = vimeo_filepath.stat().st_size / (1024 * 1024)
                print(f"✅ Vimeo Format Created: {vimeo_filename}")
                print(f"   Size: {vimeo_size_mb:.2f} MB")
                print(f"   Format: H.264 video + AAC audio (Vimeo optimized)\n")
                vimeo_created = True
            else:
                print(f"❌ Failed to create Vimeo format file")
                if result.stderr:
                    print(f"   Error: {result.stderr}")
                    
        except Exception as e:
            print(f"❌ Error converting to Vimeo format: {e}\n")
    
    # Print summary
    print("\n" + "=" * 100)
    print("GENERATION COMPLETE")
    print("=" * 100)
    print(f"\n✅ Files Created:")
    print(f"   Standard MP4: {mp4_filename}")
    if vimeo_created:
        print(f"   Vimeo Format: {vimeo_filename}")
    print(f"\n✅ Output Location: {output_folder.absolute()}")
    print(f"✅ Voice: Zira (Female)")
    print(f"✅ Dashboard Title: Weekly Messages Audio Template - Summarized - Week 4")
    print("\n" + "=" * 100 + "\n")

if __name__ == "__main__":
    main()
