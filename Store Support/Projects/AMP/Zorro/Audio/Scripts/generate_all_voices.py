#!/usr/bin/env python3
"""
Generate audio with all available voices - Jenny, David, Zira
Uses unified audio_pipeline with automatic fallback support

Features:
- Jenny Neural (Premium) as primary voice
- Automatic fallback to David/Zira if Jenny unavailable
- Generates 3 voices from single message
- Compatible with convert_wav_to_mp4_installer.py pipeline
- Professional quality output ready for MP4 conversion

Date: March 10, 2026
Status: Production Ready
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Import the audio pipeline (Jenny + fallback support)
audio_dir = Path(__file__).parent.parent
sys.path.insert(0, str(audio_dir))

try:
    from audio_pipeline import AudioPipeline, Voice, synthesize_activity_message
except ImportError as e:
    print(f"❌ Error: Could not import audio_pipeline")
    print(f"   Make sure audio_pipeline.py is in: {audio_dir}")
    print(f"   Error: {e}")
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

def main():
    """Generate audio with all 3 voices"""
    
    print("\n" + "=" * 100)
    print("MULTI-VOICE AUDIO GENERATION - JENNY + DAVID + ZIRA")
    print("=" * 100)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Message Length: {len(message_body)} characters")
    print(f"Output Folder: ../output/podcasts/")
    print("\n" + "=" * 100 + "\n")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "output" / "podcasts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Voices to generate (Jenny preferred, fallback to David/Zira)
    voices_to_generate = [
        (Voice.JENNY, "Jenny", "🎤 Primary (Neural Premium)"),
        (Voice.DAVID, "David", "🎙️  Fallback 1 (Neural)"),
        (Voice.ZIRA, "Zira", "🎙️  Fallback 2 (Neural)"),
    ]
    
    results = {}
    
    for voice, label, description in voices_to_generate:
        print(f"\n{description}")
        print(f"Voice: {voice.value}")
        print("-" * 100)
        
        try:
            # Use unified synthesis function with fallback support
            success, audio_file = synthesize_activity_message(
                message_text=message_body,
                voice=voice,
                output_dir=str(output_dir)
            )
            
            if success and audio_file and os.path.exists(audio_file):
                file_size_mb = os.path.getsize(audio_file) / (1024 * 1024)
                file_name = os.path.basename(audio_file)
                
                print(f"✅ SUCCESS: {label}")
                print(f"   File: {file_name}")
                print(f"   Size: {file_size_mb:.2f} MB")
                
                results[label] = {
                    'success': True,
                    'file': file_name,
                    'size_mb': file_size_mb,
                    'path': audio_file
                }
            else:
                print(f"❌ FAILED: {label}")
                print(f"   Could not generate audio file")
                results[label] = {'success': False, 'reason': 'No audio file generated'}
                
        except Exception as e:
            print(f"❌ ERROR: {label}")
            print(f"   {str(e)[:100]}")
            results[label] = {'success': False, 'reason': str(e)[:100]}
    
    # Print summary
    print("\n" + "=" * 100)
    print("GENERATION SUMMARY")
    print("=" * 100)
    
    successful = sum(1 for r in results.values() if r.get('success', False))
    total = len(results)
    
    print(f"\n✅ Successful: {successful}/{total}")
    
    for label, result in results.items():
        if result.get('success'):
            print(f"   • {label}: {result['file']} ({result['size_mb']:.2f} MB)")
        else:
            print(f"   • {label}: FAILED - {result.get('reason', 'Unknown error')}")
    
    print("\n" + "-" * 100)
    print("NEXT STEPS:")
    print("-" * 100)
    print(f"1. Convert WAV files to MP4:")
    print(f"   python convert_wav_to_mp4_installer.py")
    print(f"\n2. Convert MP4 to Vimeo-compatible format:")
    print(f"   python convert_standard_to_vimeo.py")
    print(f"\n3. View on dashboard:")
    print(f"   http://localhost:8888")
    print("\n" + "=" * 100 + "\n")
    
    # Return exit code based on success
    return 0 if successful == total else 1

if __name__ == "__main__":
    exit(main())
