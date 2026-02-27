#!/usr/bin/env python3
"""
Generate professional podcasts from Summarized Weekly Messages (SAPI5 Voices)
Week 4, 2027 - Merchant Messages (Review for Publish, No Comms)

Summarized Content Analysis:
Event IDs with "Summarized:" sections:
  1. 41c6ee0f-d310-4522-9941-ee04ac3816cf - Dept. 72: PC New Software Display, Storage Update
  2. ccdd5e91-7684-4242-89b1-38d718e23393 - Dept. 93: Fish today, corned beef tomorrow
  3. e79243bc-6676-4242-aeb0-a0608c2c8869 - Dept. 29: Sleepwear Preview

Output: WAV files (ready for MP4 conversion via FFmpeg)
Voices: David (Male), Zira (Female)
Engine: Windows SAPI5 (PowerShell)
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

def main():
    """Main function to generate audio for summarized weekly messages"""
    
    # Complete week script with intro, organized content, and outro
    week_script = """Hello! Your Week 4 Weekly Messages are Here!

Please Visit the Landing Page to access full content.

Entertainment Area Weekly Messages:

Dept. 72: PC Software Display Setup
Week 50 shipment: magnetic frame plus scannable insert (set immediately; ignore Hold for Anderson). Place on Electronics cash wrap near POS; message must face customer. Insert scannable sheet for checkout purchase. Upcoming POS prompt will remind associates to suggest PC software with laptop purchases. Featured SKUs: Norton VPN and 360 tiers, McAfee Total Protection, HR Block 2025 Basic and Deluxe. Actions: Install new placemat at cash wrap. Ensure price tags are printed and placed on laptop PC software fixtures. Questions: submit store ticket or email Tyler Jackson.

Dept. 72: Digital Storage Update
Industry-wide inventory constraints on SSDs and PC memory. Working to improve in-stocks for Week 16 modulars. Impacted items with no current restock date include select Kingston FURY DDR5 memory, NVIDIA RTX 5070 Ti, Samsung T7 and T9 portable SSDs, Samsung 990 EVO and PRO SSDs, and Seagate One Touch SSD. Supply improvements ongoing; may pivot to alternative SKUs as needed.

Fresh Area Weekly Messages:

Dept. 93: Lent is Here
Focus on forty-one to sixty shrimp, salmon, and tilapia. Set features, aisle-locate items, and work seafood mods daily. Prepare for increased Lent demand.

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
Licensed short sleeve tee and tank with shorts sets. Markdown: Week 17, May twenty-three through twenty-nine.

No Boundaries Sidewall (Category 2357 and 2457)
Cloud Core cotton cami and short sets, chemises, tops and pants. Markdown: Week 12, April eighteen through twenty-four.

No Boundaries Satin Sets (Category 2405)
Satin cami and shorts sets. Markdown: Week 14, May two through eight.

That's your Week 4 Weekly Messages, Have a Great Week!"""
    
    # Output folder path
    output_folder = Path("Store Support/Projects/AMP/Zorro/output/podcasts")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Print header
    print("\n" + "=" * 100)
    print("SUMMARIZED WEEKLY MESSAGES - AUDIO GENERATION (SAPI5)")
    print("=" * 100)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Event Count: 3 Merchant Messages (Week 4, 2027)")
    print(f"Output Folder: {output_folder}")
    print(f"Voices: David (Male), Zira (Female)")
    print(f"Format: WAV (44.1 kHz, 16-bit)")
    print("\n" + "=" * 100 + "\n")
    
    # Track statistics
    total_files = 0
    successful_files = 0
    failed_files = 0
    
    print(f"{'─' * 100}")
    print(f"Week 4 Complete Weekly Messages Script (with intro and outro)")
    print(f"{'─' * 100}")
    print(f"\nCharacter Count: {len(week_script):,}")
    print(f"Word Count: {len(week_script.split()):,}\n")
    
    # Generate audio for both voices
    for voice_name in ['David', 'Zira']:
        try:
            # Generate filename
            filename = f"Summarized Weekly Messages - Audio - Reading - {voice_name}.wav"
            filepath = output_folder / filename
            
            # Escape single quotes in script for PowerShell
            script_for_ps = week_script.replace("'", "''")
            
            # Create PowerShell script with simple text input
            ps_commands = f"""
$text = @'
{script_for_ps}
'@

[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$tts.SelectVoice('{voice_name}')
$tts.Rate = -2
$tts.Volume = 100
$tts.SetOutputToWaveFile('{filepath}')
$tts.Speak($text)
$tts.SetOutputToNull()
$tts.Dispose()

if (Test-Path '{filepath}') {{
    $size = [math]::Round((Get-Item '{filepath}').Length / 1MB, 2)
    Write-Host "OK: {voice_name} - ${{size}}MB"
}}
"""
            
            # Print generation status
            print(f"  Generating: {filename}")
            
            # Run PowerShell command
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_commands],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            total_files += 1
            
            # Check if file was created
            if filepath.exists():
                file_size_mb = filepath.stat().st_size / (1024 * 1024)
                file_size_bytes = filepath.stat().st_size
                print(f"  ✅ Created: {filename}")
                print(f"     Size: {file_size_mb:.2f} MB ({file_size_bytes:,} bytes)\n")
                successful_files += 1
            else:
                print(f"  ❌ Failed to create: {filename}")
                if result.stderr:
                    print(f"     Error: {result.stderr}")
                failed_files += 1
                
        except Exception as e:
            print(f"  ❌ Error generating audio for '{voice_name}': {e}\n")
            failed_files += 1
            total_files += 1
    
    # Print summary
    print("=" * 100)
    print("GENERATION SUMMARY")
    print("=" * 100)
    print(f"Total Files Generated: {total_files}")
    print(f"Successful: {successful_files} ✅")
    if failed_files > 0:
        print(f"Failed: {failed_files} ❌")
    print(f"\nOutput Folder: {output_folder.absolute()}")
    print("=" * 100 + "\n")

if __name__ == "__main__":
    main()
