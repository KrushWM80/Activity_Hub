"""Generate podcast with specific voice - simplified approach."""

import os
import subprocess
from datetime import datetime

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

def generate_voice(voice_name, label):
    """Generate with specific voice."""
    
    output_file = f"../output/podcasts/amp_podcast_91202b13_{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    # Create PowerShell script with simple text input
    ps_commands = f"""
$text = @'
{message_body}
'@

[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$tts.SelectVoice('{voice_name}')
$tts.Rate = -2
$tts.Volume = 100
$tts.SetOutputToWaveFile('{output_file}')
$tts.Speak($text)
$tts.SetOutputToNull()
$tts.Dispose()

if (Test-Path '{output_file}') {{
    $size = [math]::Round((Get-Item '{output_file}').Length / 1MB, 2)
    Write-Host "OK: {label} - ${{size}}MB"
}}
"""
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_commands],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"  Warning: {result.stderr[:100]}")
        
        import time
        time.sleep(1)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
            return os.path.basename(output_file)
            
    except Exception as e:
        print(f"Error: {e}")
    
    return None

os.makedirs("../output/podcasts", exist_ok=True)

print("=" * 70)
print("VOICE COMPARISON - GENERATING BOTH VERSIONS")
print("=" * 70)
print()

print("1️⃣  Generating with Microsoft DAVID (Male voice)...")
david = generate_voice("Microsoft David Desktop", "david_male")
print()

print("2️⃣  Generating with Microsoft ZIRA (Female voice)...")
zira = generate_voice("Microsoft Zira Desktop", "zira_female")
print()

print("=" * 70)
print("RESULTS")
print("=" * 70)
print()

if david:
    print(f"✅ David (Male):  {david}")
if zira:
    print(f"✅ Zira (Female): {zira}")

print()
print("🎙️  Listen and compare at: http://localhost:8888")
print()
print("Which voice do you prefer? David (male) or Zira (female)?")
