#!/usr/bin/env python3
"""Generate Jenny Neural MP4 audio for Summarized Weekly Messages - Week 4"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from windows_media_synthesizer import WindowsMediaSynthesizer

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

output_dir = Path(__file__).parent.parent.parent / "output" / "Audio"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "Weekly Messages Audio Template - Summarized - Week 4 - Jenny Neural - Vimeo.mp4"

print(f"Generating Jenny Neural audio...")
print(f"Script: {len(week_script)} characters")
print(f"Output: {output_file.name}")

synth = WindowsMediaSynthesizer()
success = synth.synthesize_to_mp4(week_script, str(output_file), voice="Jenny", rate=0.95)

if success:
    size_kb = output_file.stat().st_size / 1024
    print(f"\nSuccess! {output_file.name} ({size_kb:.1f} KB)")
else:
    print("\nFailed to generate audio")
