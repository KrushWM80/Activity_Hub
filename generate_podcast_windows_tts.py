#!/usr/bin/env python3
"""
Professional AMP Podcast Generator using Windows Text-to-Speech
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib

class WindowsTTSPodcastGenerator:
    """Generate podcast using Windows built-in TTS"""
    
    def __init__(self):
        self.output_dir = Path(__file__).parent / "Store Support/Projects/AMP/Zorro/output/podcasts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir = Path(__file__).parent / "Store Support/Projects/AMP/Zorro/output/metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
    
    def create_podcast_script(self):
        """Create the professional podcast script"""
        
        script = """Hello team! Welcome to this week's store briefing. This is Week 4, and we have some exciting updates that will help you succeed on the sales floor.

Your Week 4 Messages Are Here

Please visit the Landing Page to access full content.

Let's dive into what's happening in your store this week.

FOOD AND CONSUMABLES MERCHANT MESSAGES

Beauty and Consumables. We've got some fantastic updates:

Beauty in waiting: Maybelline modular reset hits a snag.
Unbottled brilliance: Tide evo leads the clean scene. 
Rock-a-bye Rollbacks: Spring Baby Days delivers big savings for little ones. 
Modularizing of the Health and Wellness Wall.
Know the clean floor safety tips.

Food Department. Teamwork makes the dream work:

Department 90: Review the update on Fairlife milk supply.
Department 95: Poppi beverages are transitioning to be serviced by Pepsi DSD.
Department 95: Gatorade is launching a new product line with lower sugar and no artificials.
Department 95: Gatorade is lowering the EDLP on 20 ounce 8 packs.
Department 95: Your Energy Drink sidekicks are being updated.
Department 95: Store associates need to keep On The Border tortilla chips stocked on the shelves.
Know the clean floor safety tips.

Fresh Department. Spring is here, and so are exciting opportunities:

Department 80: Temporary shortage of pre-sliced, not bulk, Prima Della Honey Turkey. Expand adjacent items until replenishment resumes between weeks 8 through 13.
Department 93: Fish today, corned beef tomorrow.
Department 93: Lean into Lent sales with this week's item in the spotlight: Great Value tilapia fillets and set your corned beef for Saint Patrick's Day. 
Department 93: Rollbacks can really bring home the bacon, but only if customers know about the sizzling savings! Make sure every pork Rollback is flagged in your department, and watch those pigs fly off the shelves!
Department 94: View estimated recovery dates for key produce items at risk of low inventory due to supply constraints.
Department 94: Keep customers happy: stock packaged corn when bulk is low, check quality before discarding, and watch for updates through early April!
Department 94: Keep shelves full: stock green cabbage, even without outer leaves, for Easter! No shrink, great quality, happy customers!
Department 94: Carrot supply impacted by California weather; sourcing expanded. 2 pound baby peeled carrots on Rollback, in stock 92 to 97 percent.
Department 94: Green asparagus supply ramps up, ensuring fresh options and strong in stock in time to meet the Easter demand!
Department 94: Persistent rainfall continues to impact product quality on mixed veggies, like Brussels sprouts and greens, as supply recovers.
Department 94: The Kiwi season ended; place bulk yellow mangoes in the modular space until Kiwi returns in early May.
Department 81: Prepare for Easter by stocking Brown and Serve Rolls and set up displays near hams for cross merchandising.
Department 98: Build eye catching spring displays, cross merchandise for Strawberry Shortcake, and clean up lingering Mardi Gras inventory. 
Know the clean floor safety tips.

GENERAL MERCHANDISE MERCHANT MESSAGES

Entertainment. Exciting new setups in your store:

Department 85: Celebrate Grads with Walmart Photo Essentials!
Department 72: Install the new PC Software display at electronics cash wrap. Some storage SKUs remain in short supply.
Department 72: Three Samsung soundbars are discontinued due to shortages. Two JBL models will replace them in stores starting February 21 to keep shelves stocked.
Know the clean floor safety tips.

Fashion. Spring is in full effect:

Part 2 of your spring Fashion Guides is here!
Now you can print individual T shirt spinner graphics.
Check our lookup tool to see if your store will get more Kids rack fixtures.
We've got an update on the Claire's jewelry transition in Department 32.
Don't miss our preview of the Department 29 sleepwear update.
Learn more about setting the category 2030 mod in Department 34.
Know the clean floor safety tips.

Hardlines. Get ready for action:

Aim for compliance: Hitting the mark with firearm markdown waves.
Making waves: Water Sports mod delays float in.
Vest in show: Display solutions when hangers are out to sea.
Rolling with the changes: Ball Bin simplified.
Hart to part: Making room for a modular makeover!
Turning down the heat: Shelves cool off before spring reset.
Crystal clear: Water exchange prices get an upgrade. 
Department 18 and 67: Hop to it! Easter 2026 is the last Home Office run New and Now. Shorter sales window, staggered inventory, and new setups mean check the Playbook and set displays early for max sales!
Department 67: Helium sales take flight with new checkout steps. 
Department 67 hops ahead with festive feature program.
Department 67: Dabney Lee endcap extends the celebration, while inventory lasts!
Know the clean floor safety tips.

Home and Seasonal. Spring changes ahead:

Home: We've updated a Mainstays trash can label to make picking easier. We've got a major reset coming to Bulk Storage. Know the clean floor safety tips.

Seasonal: Department 16: Starting in week 5, select Kingsford Charcoal items will transition from RDC to HVDC delivery to free up RDC capacity for automation.

OPERATIONS MESSAGES

Asset Protection: Know the clean floor safety tips.

Backroom: Join bi-weekly DSD Office Hours on Teams for real time support and resolution of Direct Store Delivery issues. 
Starting in week 5, select Kingsford Charcoal items will transition from RDC to HVDC delivery to free up RDC capacity for automation. 
Know the clean floor safety tips.

Front End: The Front End Operations Resolution Team is available to answer your questions about the Front End and Financial Services offered in your store.
The Friendliest Front End Spring Edition will launch on February 28.
Reminder: In store Affirm Lending Tender acceptance ended January 31.
Know the clean floor safety tips.

Store Fulfillment: Oversized pick walks will now automatically split for high weight, single item orders to support safer lifting and cart handling. Know the clean floor safety tips.

People: Keep Calm and Ask My Assistant. AI Tip of the Week. Know the clean floor safety tips.

That's your Week 4 briefing, team. You've got this. Make it a great week, stay safe, and thanks for your hard work!"""
        
        return script
    
    def generate_with_windows_tts(self, script, title, event_id):
        """Generate audio using Windows PowerShell Text-to-Speech"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = title.replace(' ', '_')[:25]
        filename = f"amp_podcast_{event_id[:8]}_{safe_title}_{timestamp}.wav"
        filepath = self.output_dir / filename
        
        print(f"🎙️  Generating Professional Podcast with Windows TTS")
        print(f"  Title: {title}")
        print(f"  Event ID: {event_id}")
        print(f"  Output: {filename}\n")
        
        try:
            # Create PowerShell script for TTS
            ps_script = f"""
$text = @"
{script}
"@

$OutputFile = "{filepath}"

Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.Rate = 0
$speak.Volume = 100
$speak.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female)
$audioStream = New-Object System.IO.FileStream($OutputFile, [System.IO.FileMode]::Create)
$speak.SetOutputToAudioStream($audioStream, (New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(16000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)))
$speak.Speak($text)
$speak.SetOutputToNull()
$audioStream.Close()
Write-Host "Audio saved to: $OutputFile"
"""
            
            # Save PowerShell script (with UTF-8 encoding)
            ps_file = Path(__file__).parent / f"tts_script_{timestamp}.ps1"
            with open(ps_file, 'w', encoding='utf-8') as f:
                f.write(ps_script)
            
            print("🔧 Running Windows Text-to-Speech synthesizer...\n")
            
            # Execute PowerShell script
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_file)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
            
            # Clean up PS file
            ps_file.unlink()
            
            if filepath.exists():
                file_size = filepath.stat().st_size
                file_size_mb = file_size / (1024 * 1024)
                
                print(f"✅ Audio file created: {file_size_mb:.2f} MB\n")
                
                # Generate metadata
                tracking_id = hashlib.sha256(f"{event_id}{timestamp}".encode()).hexdigest()[:16]
                podcast_id = hashlib.sha256(f"{title}{timestamp}".encode()).hexdigest()[:8]
                
                metadata = {
                    "event_id": event_id,
                    "podcast_id": podcast_id,
                    "title": title,
                    "filename": filename,
                    "filepath": str(filepath),
                    "file_size_bytes": file_size,
                    "file_size_mb": round(file_size_mb, 2),
                    "format": "WAV (Windows Text-to-Speech)",
                    "engine": "System.Speech.Synthesis",
                    "voice": "System Default",
                    "created_date": timestamp,
                    "tracking_id": tracking_id,
                    "local_url": f"http://localhost:8888/podcasts/{filename}",
                    "relative_path": f"output/podcasts/{filename}",
                    "script_length": len(script),
                    "message_source": "wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT"
                }
                
                # Save metadata
                metadata_file = self.metadata_dir / f"{podcast_id}.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                return metadata
            else:
                print("❌ Error: Audio file was not created")
                return None
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """Generate professional podcast"""
    
    print("\n" + "="*80)
    print("🎙️  PROFESSIONAL AMP PODCAST GENERATOR")
    print("  Using Windows System Text-to-Speech")
    print("="*80 + "\n")
    
    try:
        generator = WindowsTTSPodcastGenerator()
        
        # Create script
        print("📝 Creating podcast script from message body...\n")
        script = generator.create_podcast_script()
        
        print(f"✅ Script created: {len(script)} characters\n")
        
        # Generate audio
        result = generator.generate_with_windows_tts(
            script,
            "Your Week 4 Messages Are Here",
            "91202b13-3e65-4870-885f-f4a66e221eed"
        )
        
        if result:
            print("="*80)
            print("✅ PODCAST GENERATION COMPLETE")
            print("="*80)
            print(f"\n📌 Podcast Details:")
            print(f"   Event ID: 91202b13-3e65-4870-885f-f4a66e221eed")
            print(f"   Podcast ID: {result['podcast_id']}")
            print(f"   Title: {result['title']}")
            print(f"   File: {result['filename']}")
            print(f"   Size: {result['file_size_mb']} MB")
            print(f"   Tracking: {result['tracking_id']}")
            
            print(f"\n🔗 Access Your Podcast:")
            print(f"   Web Player: http://localhost:8888")
            print(f"   Direct: {result['local_url']}")
            print(f"   File: {result['filepath']}")
            
            print(f"\n✨ Status: READY FOR DISTRIBUTION")
            print("="*80 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
