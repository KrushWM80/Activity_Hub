#!/usr/bin/env python3
"""
Generate MP4 audio files using audio_pipeline (proper Jenny support)
Converts WAV → MP4 automatically

Features:
- Uses audio_pipeline for proper Jenny voice engine support
- Generates WAV first (audio_pipeline output)
- Converts to MP4 via FFmpeg
- All 3 voices: Jenny, David, Zira
- Ready for dashboard and Vimeo

Date: March 10, 2026
Status: Production - Proper Jenny Engine Support
"""

import os
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
import sys
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent))

try:
    from audio_pipeline import AudioPipeline, Voice
except ImportError as e:
    print(f"❌ Error: Could not import audio_pipeline: {e}")
    print(f"   Make sure audio_pipeline.py is in {current_dir.parent}")
    sys.exit(1)

# Message body - Week 4 full AMP Activities
message_body = """
Hello! Your Week 4 Messages Are Here!

Please Visit the Landing Page to access full content.

Food & Consumables Merchant Messages:

Beauty & Consumables
Beauty in waiting: Maybelline modular reset hits a snag.
Unbottled brilliance: Tide evo leads the clean scene. 
Rock-a-bye Rollbacks: Spring Baby Days delivers big savings for little ones. 
Modularizing of the Health & Wellness Wall
Know the clean floor safety tips.

Food
Dept. 90: Review the update on Fairlife milk supply.
Dept. 95: Poppi beverages are transitioning to be serviced by Pepsi DSD.
Dept. 95: Gatorade is launching a new product line with lower sugar and no artificials.
Dept. 95: Gatorade is lowering the EDLP on 20oz 8-packs.
Dept. 95: Your Energy Drink sidekicks are being updated.
Dept. 95: Store associates need to keep On The Border tortilla chips stocked on the shelves.
Know the clean floor safety tips.

Fresh
Dept. 80: Temporary shortage of pre-sliced not bulk Prima Della Honey Turkey; expand adjacent items until replenishment resumes between weeks 8 through 13.
Dept. 93: Fish today, corned beef tomorrow.
Dept. 93: Lean into Lent sales with this week's item in the spotlight: Great Value tilapia fillets and set your corned beef for St. Patrick's Day. 
Dept. 93: Rollbacks can really bring home the bacon—but only if customers know about the sizzling savings! Make sure every pork Rollback is flagged in your department, and watch those pigs fly off the shelves!
Dept. 94: View estimated recovery dates for key produce items at risk of low inventory due to supply constraints.
Dept. 94: Keep customers happy—stock packaged corn when bulk is low, check quality before discarding, and watch for updates through early April!
Dept. 94: Keep shelves full—stock green cabbage, even without outer leaves, for Easter! No shrink, great quality, happy customers!
Dept. 94: Carrot supply impacted by California weather; sourcing expanded, 2-pound baby peeled carrots on Rollback, in-stock 92 to 97 percent.
Dept. 94: Green asparagus supply ramps up, ensuring fresh options and strong in-stock in time to meet the Easter demand!
Dept. 94: Persistent rainfall continues to impact product quality on mixed veggies—like Brussels sprouts and greens—as supply recovers.
Dept. 94: The Kiwi season ended; place bulk yellow mangoes in the modular space until Kiwi returns in early May.
Dept. 81: Prepare for Easter by stocking Brown and Serve Rolls and set up displays near hams for cross-merchandising.
Dept. 98: Build eye-catching spring displays, cross-merchandise for Strawberry Shortcake, and clean up lingering Mardi Gras inventory. 
Know the clean floor safety tips.

General Merchandise Merchant Messages:

Entertainment
Dept. 85: Celebrate Grads with Walmart Photo Essentials!
Dept. 72: Install the new PC Software display at electronics cash wrap, some storage SKUs remain in short supply.
Dept. 72: Three Samsung soundbars are discontinued due to shortages; two JBL models will replace them in stores starting Feb. 21 to keep shelves stocked.
Know the clean floor safety tips.

Fashion
Part 2 of your spring Fashion Guides is here!
Now you can print individual T-shirt spinner graphics.
Check our lookup tool to see if your store will get more Kids rack fixtures.
We've got an update on the Claire's jewelry transition in Dept. 32.
Don't miss our preview of the Dept. 29 sleepwear update.
Learn more about setting the category 2030 mod in Dept. 34.
Know the clean floor safety tips.

Hardlines
Aim for compliance: Hitting the mark with firearm markdown waves.
Making waves: Water Sports mod delays float in.
Vest in show: Display solutions when hangers are out to sea.
Rolling with the changes: Ball Bin simplified.
Hart to part: Making room for a modular makeover!
Turning down the heat: Shelves cool off before spring reset.
Crystal clear: Water exchange prices get an upgrade. 
Dept. 18 slash 67: Hop to it! Easter 2026 is the last Home Office-run New and Now—shorter sales window, staggered inventory, and new setups mean check the Playbook and set displays early for max sales!
Dept. 67: Helium sales take flight with new checkout steps. 
Dept. 67 hops ahead with festive feature program.
Dept. 67: Dabney Lee endcap extends the celebration while inventory lasts!
Know the clean floor safety tips.

Home
We've updated a Mainstays trash can label to make picking easier.
We've got a major reset coming to Bulk Storage.
Know the clean floor safety tips.

Seasonal
Dept. 16: Starting in week 5, select Kingsford Charcoal items will transition from RDC to HVDC delivery to free up RDC capacity for automation. 
Dept. 18 slash 67: Hop to it! Easter 2026 is the last Home Office-run New and Now—shorter sales window, staggered inventory, and new setups mean check the Playbook and set displays early for max sales!
Dept. 67: Helium sales take flight with new checkout steps. 
Dept. 67 hops ahead with festive feature program.
Dept. 67: Dabney Lee endcap extends the celebration while inventory lasts!
Know the clean floor safety tips.

Operations Messages:

Asset Protection
Know the clean floor safety tips.

Backroom
Join bi-weekly DSD Office Hours on Teams for real-time support and resolution of Direct Store Delivery issues. 
Starting in week 5, select Kingsford Charcoal items will transition from RDC to HVDC delivery to free up RDC capacity for automation. 
Know the clean floor safety tips.

Front End
The Front End Operations Resolution Team is available to answer your questions about the Front End and Financial Services offered in your store.
The Friendliest Front End Spring Edition will launch on Feb. 28.
Reminder! In-store Affirm Lending Tender acceptance ended Jan. 31.
Know the clean floor safety tips.

Store Fulfillment
Oversized pick walks will now automatically split for high-weight, single-item orders to support safer lifting and cart handling.
Know the clean floor safety tips.

People
Keep Calm and Ask My Assistant - AI Tip of the Week
Know the clean floor safety tips.

Thank you and have a Great Day!
"""

def generate_mp4_with_voice(voice, voice_display, pipeline, output_dir):
    """Generate WAV via audio_pipeline, then convert to MP4"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    mp4_filename = f"Your Week 4 Messages are Here - Audio - Reading - {voice_display} - {timestamp}.mp4"
    mp4_filepath = Path(output_dir) / mp4_filename
    
    print(f"\n🎤 Generating {voice_display}...")
    
    try:
        # Step 1: Generate WAV using audio_pipeline (proper engine handling)
        result = pipeline.synthesize(
            text=message_body,
            voice=voice,
            add_ssml=True,
            output_file=None  # Return path from synthesize
        )
        
        if not result.success:
            print(f"   ❌ Audio pipeline failed: {result.error_message}")
            return False
        
        wav_filepath = result.audio_file
        
        if not Path(wav_filepath).exists():
            print(f"   ❌ WAV file not created")
            return False
        
        # Step 2: Convert WAV to MP4 using FFmpeg
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(wav_filepath),
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "faststart",
            "-y",
            str(mp4_filepath)
        ]
        
        ffmpeg_result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if mp4_filepath.exists():
            size_mb = mp4_filepath.stat().st_size / (1024 * 1024)
            print(f"   ✅ {voice_display}: {mp4_filename}")
            print(f"      Size: {size_mb:.2f} MB")
            print(f"      Engine: {result.engine_used.value}")
            
            # Clean up WAV
            try:
                Path(wav_filepath).unlink()
            except:
                pass
            
            return True
        else:
            print(f"   ❌ FFmpeg conversion failed")
            if ffmpeg_result.stderr:
                print(f"      Error: {ffmpeg_result.stderr[:100]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return False

def main():
    """Generate MP4 files with all voices using audio_pipeline"""
    
    print("\n" + "=" * 100)
    print("MP4 GENERATION WITH AUDIO_PIPELINE - JENNY + DAVID + ZIRA")
    print("=" * 100)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Message Length: {len(message_body)} characters")
    print(f"Output Folder: ../../output/podcasts/")
    print(f"Format: MP4 (AAC 192k)")
    print(f"Engine: audio_pipeline with multi-voice fallback")
    print("\n" + "=" * 100)
    
    output_dir = Path(__file__).parent.parent.parent / "output" / "podcasts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize audio pipeline
    try:
        pipeline = AudioPipeline(preferred_voice=Voice.JENNY)
    except Exception as e:
        print(f"\n❌ Failed to initialize audio_pipeline: {e}")
        return 1
    
    # Voices to generate in order
    voices = [
        (Voice.JENNY, "Jenny"),
        (Voice.DAVID, "David"),
        (Voice.ZIRA, "Zira"),
    ]
    
    results = {}
    successful = 0
    
    for voice, voice_display in voices:
        if generate_mp4_with_voice(voice, voice_display, pipeline, output_dir):
            results[voice_display] = True
            successful += 1
        else:
            results[voice_display] = False
    
    # Print summary
    print("\n" + "=" * 100)
    print("GENERATION SUMMARY")
    print("=" * 100)
    print(f"\n✅ Generated: {successful}/3 MP4 files")
    print(f"📁 Location: {output_dir.absolute()}")
    
    print("\n" + "-" * 100)
    print("NEXT STEPS:")
    print("-" * 100)
    print(f"1. View on dashboard:")
    print(f"   http://localhost:8888")
    print(f"\n2. Optional: Convert to Vimeo-compatible MP4:")
    print(f"   python convert_standard_to_vimeo.py")
    print("\n" + "=" * 100 + "\n")
    
    return 0 if successful == 3 else 1

if __name__ == "__main__":
    exit(main())
