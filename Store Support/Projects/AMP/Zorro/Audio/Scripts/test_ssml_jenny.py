#!/usr/bin/env python3
"""
Test SSML-enhanced delivery with Jenny Neural voice.
Bypasses edge-tts's XML escaping to pass through raw SSML tags
like <break>, <emphasis>, and <prosody>.
"""

import asyncio
import subprocess
import sys
from pathlib import Path

# The SSML inner content — everything inside the outer <prosody> wrapper.
# edge-tts will wrap this in <speak><voice><prosody>...HERE...</prosody></voice></speak>
SSML_INNER = """
Hello! <break time="300ms"/>
Your <emphasis level="moderate">Week 4 Weekly Messages</emphasis> are here.

<break time="400ms"/>
Please visit the landing page to access full content.

<break time="600ms"/>

<emphasis level="moderate">Food and Consumables Merchant Messages.</emphasis>

<break time="400ms"/>
Beauty and Consumables Area.

<break time="300ms"/>
Department 13: <emphasis level="strong">Tide Evo</emphasis> is a category-defining innovation from the number one laundry brand. 
It reinvents detergent as a lightweight, waterless sheet with no fillers, no plastic bottles, and sustainable packaging. 
Backed by <emphasis level="moderate">three billion plus national impressions</emphasis>, 
in-store displays begin March seventh, with a full rollout by April eleventh.

<break time="500ms"/>
Department 40: The Health and Wellness wall is being modularized to create a more cohesive and better merchandised space. 
This will improve tracking, maximize space use, increase sell-through, reduce nil picks, 
and strengthen OPD performance on top categories. 
Changes begin in March with the quarterly relay.

<break time="700ms"/>

<emphasis level="moderate">Food Area.</emphasis>

<break time="300ms"/>
Department 90: <emphasis level="moderate">Fairlife supply is improving.</emphasis> 
Starting week five, expect increased shipments and better in-stocks. 
A new production facility is now shipping, boosting capacity. 
Fairlife continues to grow rapidly, up twenty-five percent in two years, 
with another fifteen percent expected this year.

<break time="400ms"/>
Department 95: <emphasis level="moderate">Gatorade twenty-ounce eight-packs</emphasis> 
now feature a lower everyday price of six dollars and ninety-eight cents. 
This investment is designed to reengage customers and drive demand.

<break time="300ms"/>
Also in Department 95: <emphasis level="moderate">Gatorade introduces lower sugar and no artificial options.</emphasis> 
Customers get the same taste and electrolytes, with seventy-five percent less sugar.

<break time="300ms"/>
On the Border tortilla chips are selling fast, but nil picks are rising. 
Ensure the sidecounter is checked daily and kept full.

<break time="300ms"/>
Poppi beverages transition to Pepsi direct store delivery beginning March second. 
This means improved in-stocks, faster replenishment, and reduced manual ordering.

<break time="300ms"/>
Energy sidekicks are being updated to increase holding power and support seasonal items.

<break time="700ms"/>

<emphasis level="moderate">Fresh Area.</emphasis>

<break time="300ms"/>
There is a temporary shortage of Prima Della pre-sliced honey roasted turkey. 
Replenishment is expected to resume between weeks eight and thirteen.

<break time="300ms"/>
Department 93: Lent is here. Focus on shrimp, salmon, and tilapia. 
Great Value tilapia is on rollback at seventeen dollars and forty-seven cents, 
with an expected twenty percent lift.

<break time="300ms"/>
Produce in-stock risks continue due to weather impacts. 
Monitor key items like cilantro, green onions, corn, and berries.

<break time="300ms"/>
Department 81: Prepare now for Easter staples, including Brown and Serve rolls. 
Plan cross merchandising near the ham section.

<break time="300ms"/>
Department 98: Spring feature planning is underway. 
Highlight angel food items and build seasonal displays like strawberry shortcake destinations.

<break time="700ms"/>

<emphasis level="moderate">General Merchandise Merchant Messages.</emphasis>

<break time="400ms"/>
Entertainment Area.

<break time="300ms"/>
Department 72: Samsung soundbars are being discontinued and replaced with JBL models. 
Ensure proper placement and updated pricing.

<break time="300ms"/>
PC software displays should be set immediately at the electronics cash wrap. 
Associates will be prompted to suggest software with laptop purchases.

<break time="300ms"/>
Department 85: Graduation season is here. 
Remind customers about Walmart Photo products both in-store and online.

<break time="600ms"/>

<emphasis level="moderate">Fashion Area.</emphasis>

<break time="300ms"/>
New sleepwear assortments are arriving, including licensed sets and updated No Boundaries items.

<break time="300ms"/>
Claire's jewelry is transitioning to Walmart-owned inventory in phases.

<break time="300ms"/>
Ensure Women's Plus Core Wall is set correctly with updated instructions.

<break time="300ms"/>
Additional rack fixtures have been delivered to support kids' assortment expansion.

<break time="300ms"/>
Updated spring fashion guides are now available on Better Way.

<break time="700ms"/>

<emphasis level="moderate">Hardlines Area.</emphasis>

<break time="300ms"/>
Water sports modular items are delayed. Use available inventory to fill space.

<break time="300ms"/>
Hart inventory is selling down. Flex and relabel as needed.

<break time="300ms"/>
Updated water exchange pricing takes effect week four.

<break time="300ms"/>
Heaters are selling out. Transition space to fans and maintain shoppability.

<break time="700ms"/>

<emphasis level="moderate">Home Area.</emphasis>

<break time="300ms"/>
Department 74: A major bulk storage reset is coming in week seven, with significant item deletions.

<break time="300ms"/>
Updated labeling will improve picking accuracy and reduce nil picks.

<break time="700ms"/>

<emphasis level="moderate">Seasonal Area.</emphasis>

<break time="300ms"/>
Easter arrives early this year with a shorter selling window. 
Prioritize eggs, baskets, and seasonal features.

<break time="700ms"/>

<emphasis level="moderate">Operations Messages.</emphasis>

<break time="400ms"/>
Asset Protection: Maybelline modular delays continue in select stores. 
Set as close as possible and expect updates by week seven.

<break time="300ms"/>
Auto Care: Affirm is no longer accepted in-store. 
The new buy-now-pay-later option is OnePay Later with Klarna.

<break time="300ms"/>
Backroom: Join DSD Office Hours for real-time support.

<break time="300ms"/>
Frontend: Friendliest Front End Spring Edition begins February twenty-eighth.

<break time="300ms"/>
Pickup: Oversized picking safety updates will automatically split heavy item orders.

<break time="300ms"/>
People: Continue using My Assistant and AI to improve efficiency.

<break time="300ms"/>
Total Store: Clean floor safety remains critical. 
Address spills immediately and keep aisles clear.

<break time="300ms"/>
Department 79: Spring Baby Days runs through April seventeenth.

<break time="600ms"/>

That's your <emphasis level="moderate">Week 4 Weekly Messages.</emphasis>

<break time="300ms"/>
Have a great week.
"""


async def synthesize_ssml(ssml_inner: str, output_mp3: str, voice: str = "en-US-JennyNeural") -> bool:
    """
    Synthesize SSML content with edge-tts by sending complete <speak> blocks.
    
    Option A approach: Build full SSML, pass as bytes, monkey-patch mkssml
    to return it unchanged (no double-wrapping).
    """
    import edge_tts
    import edge_tts.communicate as comm_module

    original_mkssml = comm_module.mkssml

    def mkssml_passthrough(tc, partial_text):
        """If input is already a complete <speak> block, pass it through unchanged."""
        s = partial_text.decode("utf-8") if isinstance(partial_text, (bytes, bytearray)) else str(partial_text)
        if s.strip().startswith("<speak"):
            return s
        return original_mkssml(tc, partial_text)

    comm_module.mkssml = mkssml_passthrough

    try:
        comm = edge_tts.Communicate("dummy", voice, rate="+0%", pitch="+0Hz")

        # Build complete SSML blocks, each under 4096 bytes
        ssml_blocks = _build_ssml_blocks(ssml_inner.strip(), voice)
        
        # Override texts with a generator yielding bytes
        comm.texts = (block.encode("utf-8") for block in ssml_blocks)

        await comm.save(output_mp3)
        return Path(output_mp3).exists() and Path(output_mp3).stat().st_size > 0
    finally:
        comm_module.mkssml = original_mkssml


def _build_ssml_blocks(ssml_inner: str, voice: str, max_bytes: int = 3800) -> list:
    """
    Split SSML inner content at section breaks (700ms) and wrap each chunk
    in a complete <speak> envelope so no chunk exceeds max_bytes.
    """
    import re
    
    # Split at 700ms breaks (major section boundaries)
    sections = re.split(r'(<break time="700ms"/>)', ssml_inner)
    
    # Recombine into chunks that fit under max_bytes when wrapped
    wrapper_overhead = (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        f'<voice name="{voice}">'
        '<prosody pitch="+0Hz" rate="+0%" volume="+0%">'
        '</prosody></voice></speak>'
    )
    overhead = len(wrapper_overhead.encode("utf-8"))
    content_limit = max_bytes - overhead
    
    blocks = []
    current = ""
    for section in sections:
        test = current + section
        if len(test.encode("utf-8")) > content_limit and current.strip():
            blocks.append(_wrap_ssml(current.strip(), voice))
            current = section
        else:
            current = test
    if current.strip():
        blocks.append(_wrap_ssml(current.strip(), voice))
    
    return blocks


def _wrap_ssml(content: str, voice: str) -> str:
    """Wrap inner SSML content in a complete <speak> envelope."""
    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        f'<voice name="{voice}">'
        '<prosody pitch="+0Hz" rate="+0%" volume="+0%">'
        f'{content}'
        '</prosody>'
        '</voice>'
        '</speak>'
    )


def convert_to_mp4(input_mp3: str, output_mp4: str) -> bool:
    """Convert MP3 to MP4 with AAC encoding via FFmpeg."""
    ffmpeg = Path("C:\\ffmpeg\\bin\\ffmpeg.exe")
    if not ffmpeg.exists():
        print(f"ERROR: FFmpeg not found at {ffmpeg}")
        return False

    cmd = [str(ffmpeg), "-i", input_mp3, "-c:a", "aac", "-b:a", "256k", "-y", output_mp4]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        return False
    return True


def main():
    script_dir = Path(__file__).parent
    zorro_dir = script_dir.parent.parent
    output_dir = zorro_dir / "output" / "Audio"
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_mp3 = output_dir / "temp_ssml_test.mp3"
    output_mp4 = output_dir / "Week 4 - SSML Enhanced Test.mp4"

    print("=" * 60)
    print("SSML Enhanced Jenny Neural Test")
    print("=" * 60)
    print(f"Voice: en-US-JennyNeural")
    print(f"SSML inner content: {len(SSML_INNER):,} characters")
    print(f"Output: {output_mp4.name}")
    print()

    # Step 1: Synthesize with edge-tts
    print("Step 1: Synthesizing with Jenny Neural (SSML)...")
    try:
        success = asyncio.run(synthesize_ssml(SSML_INNER, str(temp_mp3)))
    except Exception as e:
        print(f"ERROR during synthesis: {e}")
        print("\nMake sure you are on Walmart WiFi (off Eagle WiFi / VPN).")
        sys.exit(1)

    if not success:
        print("ERROR: Synthesis produced no output.")
        sys.exit(1)

    mp3_size = temp_mp3.stat().st_size
    print(f"  MP3 created: {mp3_size:,} bytes ({mp3_size/1024:.0f} KB)")

    # Step 2: Convert to MP4
    print("Step 2: Converting to MP4 (AAC 256kbps)...")
    success = convert_to_mp4(str(temp_mp3), str(output_mp4))
    if not success:
        print("ERROR: MP4 conversion failed.")
        sys.exit(1)

    mp4_size = output_mp4.stat().st_size
    print(f"  MP4 created: {mp4_size:,} bytes ({mp4_size/1024:.0f} KB)")

    # Cleanup
    temp_mp3.unlink(missing_ok=True)

    print()
    print(f"SUCCESS: {output_mp4.name}")
    print(f"  Location: {output_mp4}")
    print(f"  Size: {mp4_size/1024:.0f} KB")
    print(f"  Playable at: http://localhost:8888/")


if __name__ == "__main__":
    main()
