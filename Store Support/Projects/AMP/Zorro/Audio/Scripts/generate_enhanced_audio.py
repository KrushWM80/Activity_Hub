#!/usr/bin/env python3
"""
Enhanced Weekly Message Audio - Segment-Based Synthesis
=======================================================
Since edge-tts doesn't support inner SSML tags (<break>, <emphasis>),
this script achieves similar delivery by:

1. Breaking the script into logical segments (headers, content, transitions)
2. Synthesizing each segment with edge-tts using different rate/pitch settings
3. Generating silence gaps of varying durations
4. Concatenating everything with FFmpeg into a polished MP4

Result: Natural pacing with pauses between sections, emphasis on headers,
and professional delivery — all with Jenny Neural quality.
"""

import asyncio
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


FFMPEG = Path("C:\\ffmpeg\\bin\\ffmpeg.exe")
VOICE = "en-US-JennyNeural"


@dataclass
class Segment:
    """A segment of audio to synthesize or a silence gap."""
    text: Optional[str] = None      # Text to synthesize (None = silence)
    silence_ms: int = 0             # Silence duration in ms (0 = speech)
    rate: str = "+0%"               # Speech rate adjustment
    pitch: str = "+0Hz"             # Pitch adjustment
    volume: str = "+0%"             # Volume adjustment
    label: str = ""                 # Description for logging


# ── Script segments with delivery instructions ──────────────────────────────
SEGMENTS = [
    # ── Intro ──
    Segment(text="Hello!", rate="-5%", pitch="+2Hz", label="Greeting"),
    Segment(silence_ms=300, label="pause"),
    Segment(text="Your Week 4 Weekly Messages are here.", rate="-5%", label="Intro"),
    Segment(silence_ms=400, label="pause"),
    Segment(text="Please visit the landing page to access full content.", rate="+0%", label="Intro instruction"),
    Segment(silence_ms=700, label="section break"),

    # ── Food & Consumables ──
    Segment(text="Food and Consumables Merchant Messages.", rate="-10%", pitch="+1Hz", label="GROUP HEADER"),
    Segment(silence_ms=500, label="pause"),

    # Beauty and Consumables
    Segment(text="Beauty and Consumables Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 13: Tide Evo is a category-defining innovation from the number one laundry brand. "
             "It reinvents detergent as a lightweight, waterless sheet with no fillers, no plastic bottles, and sustainable packaging. "
             "Backed by three billion plus national impressions, "
             "in-store displays begin March seventh, with a full rollout by April eleventh.",
        rate="-2%", label="Dept 13 - Tide Evo"
    ),
    Segment(silence_ms=500, label="pause"),
    Segment(
        text="Department 40: The Health and Wellness wall is being modularized to create a more cohesive and better merchandised space. "
             "This will improve tracking, maximize space use, increase sell-through, reduce nil picks, "
             "and strengthen OPD performance on top categories. "
             "Changes begin in March with the quarterly relay.",
        rate="+0%", label="Dept 40 - Health & Wellness"
    ),
    Segment(silence_ms=700, label="section break"),

    # Food Area
    Segment(text="Food Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 90: Fairlife supply is improving. "
             "Starting week five, expect increased shipments and better in-stocks. "
             "A new production facility is now shipping, boosting capacity. "
             "Fairlife continues to grow rapidly, up twenty-five percent in two years, "
             "with another fifteen percent expected this year.",
        rate="+0%", label="Dept 90 - Fairlife"
    ),
    Segment(silence_ms=400, label="pause"),
    Segment(
        text="Department 95: Gatorade twenty-ounce eight-packs "
             "now feature a lower everyday price of six dollars and ninety-eight cents. "
             "This investment is designed to reengage customers and drive demand.",
        rate="+0%", label="Dept 95 - Gatorade price"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Also in Department 95: Gatorade introduces lower sugar and no artificial options. "
             "Customers get the same taste and electrolytes, with seventy-five percent less sugar.",
        rate="+0%", label="Dept 95 - Gatorade sugar"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="On the Border tortilla chips are selling fast, but nil picks are rising. "
             "Ensure the sidecounter is checked daily and kept full.",
        rate="+0%", label="Dept 95 - On the Border"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Poppi beverages transition to Pepsi direct store delivery beginning March second. "
             "This means improved in-stocks, faster replenishment, and reduced manual ordering.",
        rate="+0%", label="Dept 95 - Poppi"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Energy sidekicks are being updated to increase holding power and support seasonal items.",
        rate="+0%", label="Dept 95 - Energy"
    ),
    Segment(silence_ms=700, label="section break"),

    # Fresh Area
    Segment(text="Fresh Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="There is a temporary shortage of Prima Della pre-sliced honey roasted turkey. "
             "Replenishment is expected to resume between weeks eight and thirteen.",
        rate="+0%", label="Fresh - Prima Della"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 93: Lent is here. Focus on shrimp, salmon, and tilapia. "
             "Great Value tilapia is on rollback at seventeen dollars and forty-seven cents, "
             "with an expected twenty percent lift.",
        rate="+0%", label="Dept 93 - Lent"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Produce in-stock risks continue due to weather impacts. "
             "Monitor key items like cilantro, green onions, corn, and berries.",
        rate="+0%", label="Fresh - Produce"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 81: Prepare now for Easter staples, including Brown and Serve rolls. "
             "Plan cross merchandising near the ham section.",
        rate="+0%", label="Dept 81 - Easter"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 98: Spring feature planning is underway. "
             "Highlight angel food items and build seasonal displays like strawberry shortcake destinations.",
        rate="+0%", label="Dept 98 - Spring"
    ),
    Segment(silence_ms=700, label="section break"),

    # ── General Merchandise ──
    Segment(text="General Merchandise Merchant Messages.", rate="-10%", pitch="+1Hz", label="GROUP HEADER"),
    Segment(silence_ms=500, label="pause"),

    # Entertainment
    Segment(text="Entertainment Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 72: Samsung soundbars are being discontinued and replaced with JBL models. "
             "Ensure proper placement and updated pricing.",
        rate="+0%", label="Dept 72 - Samsung/JBL"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="PC software displays should be set immediately at the electronics cash wrap. "
             "Associates will be prompted to suggest software with laptop purchases.",
        rate="+0%", label="Entertainment - PC software"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 85: Graduation season is here. "
             "Remind customers about Walmart Photo products both in-store and online.",
        rate="+0%", label="Dept 85 - Graduation"
    ),
    Segment(silence_ms=600, label="pause"),

    # Fashion
    Segment(text="Fashion Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="New sleepwear assortments are arriving, including licensed sets and updated No Boundaries items.",
        rate="+0%", label="Fashion - Sleepwear"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Claire's jewelry is transitioning to Walmart-owned inventory in phases.",
        rate="+0%", label="Fashion - Claire's"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Ensure Women's Plus Core Wall is set correctly with updated instructions.",
        rate="+0%", label="Fashion - Plus Core"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Additional rack fixtures have been delivered to support kids' assortment expansion.",
        rate="+0%", label="Fashion - Kids racks"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Updated spring fashion guides are now available on Better Way.",
        rate="+0%", label="Fashion - Spring guides"
    ),
    Segment(silence_ms=700, label="section break"),

    # Hardlines
    Segment(text="Hardlines Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Water sports modular items are delayed. Use available inventory to fill space.",
        rate="+0%", label="Hardlines - Water sports"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Hart inventory is selling down. Flex and relabel as needed.",
        rate="+0%", label="Hardlines - Hart"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Updated water exchange pricing takes effect week four.",
        rate="+0%", label="Hardlines - Water exchange"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Heaters are selling out. Transition space to fans and maintain shoppability.",
        rate="+0%", label="Hardlines - Heaters"
    ),
    Segment(silence_ms=700, label="section break"),

    # Home
    Segment(text="Home Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 74: A major bulk storage reset is coming in week seven, with significant item deletions.",
        rate="+0%", label="Dept 74 - Bulk storage"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Updated labeling will improve picking accuracy and reduce nil picks.",
        rate="+0%", label="Home - Labeling"
    ),
    Segment(silence_ms=700, label="section break"),

    # Seasonal
    Segment(text="Seasonal Area.", rate="-5%", pitch="+1Hz", label="AREA HEADER"),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Easter arrives early this year with a shorter selling window. "
             "Prioritize eggs, baskets, and seasonal features.",
        rate="+0%", label="Seasonal - Easter"
    ),
    Segment(silence_ms=700, label="section break"),

    # ── Operations ──
    Segment(text="Operations Messages.", rate="-10%", pitch="+1Hz", label="GROUP HEADER"),
    Segment(silence_ms=500, label="pause"),

    Segment(
        text="Asset Protection: Maybelline modular delays continue in select stores. "
             "Set as close as possible and expect updates by week seven.",
        rate="+0%", label="AP - Maybelline"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Auto Care: Affirm is no longer accepted in-store. "
             "The new buy-now-pay-later option is OnePay Later with Klarna.",
        rate="+0%", label="Auto Care - Affirm"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Backroom: Join DSD Office Hours for real-time support.",
        rate="+0%", label="Backroom - DSD"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Frontend: Friendliest Front End Spring Edition begins February twenty-eighth.",
        rate="+0%", label="Frontend - Spring"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Pickup: Oversized picking safety updates will automatically split heavy item orders.",
        rate="+0%", label="Pickup - Oversized"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="People: Continue using My Assistant and AI to improve efficiency.",
        rate="+0%", label="People - AI"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Total Store: Clean floor safety remains critical. "
             "Address spills immediately and keep aisles clear.",
        rate="+0%", label="Total Store - Safety"
    ),
    Segment(silence_ms=300, label="pause"),
    Segment(
        text="Department 79: Spring Baby Days runs through April seventeenth.",
        rate="+0%", label="Dept 79 - Baby Days"
    ),
    Segment(silence_ms=700, label="section break"),

    # ── Outro ──
    Segment(text="That's your Week 4 Weekly Messages.", rate="-5%", pitch="+1Hz", label="Outro"),
    Segment(silence_ms=400, label="pause"),
    Segment(text="Have a great week.", rate="-8%", pitch="+2Hz", label="Sign-off"),
]


async def synthesize_segment(seg: Segment, output_path: Path) -> bool:
    """Synthesize a single text segment with edge-tts."""
    import edge_tts
    comm = edge_tts.Communicate(seg.text, VOICE, rate=seg.rate, pitch=seg.pitch, volume=seg.volume)
    await comm.save(str(output_path))
    return output_path.exists() and output_path.stat().st_size > 0


def generate_silence(duration_ms: int, output_path: Path) -> bool:
    """Generate a silent audio file of specified duration."""
    duration_s = duration_ms / 1000.0
    cmd = [
        str(FFMPEG), "-f", "lavfi", "-i",
        f"anullsrc=r=24000:cl=mono",
        "-t", f"{duration_s:.3f}",
        "-c:a", "libmp3lame", "-b:a", "48k",
        "-y", str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def concatenate_segments(segment_files: list, output_mp4: Path) -> bool:
    """Concatenate all segment MP3s into a single MP4 using FFmpeg."""
    concat_file = output_mp4.parent / "concat_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for sf in segment_files:
            safe_path = str(sf).replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")

    cmd = [
        str(FFMPEG),
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:a", "aac", "-b:a", "256k",
        "-y", str(output_mp4)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    concat_file.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"FFmpeg concat error: {result.stderr[:500]}")
        return False
    return True


async def main():
    if not FFMPEG.exists():
        print(f"ERROR: FFmpeg not found at {FFMPEG}")
        sys.exit(1)

    script_dir = Path(__file__).parent
    zorro_dir = script_dir.parent.parent
    output_dir = zorro_dir / "output" / "Audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_mp4 = output_dir / "Week 4 - SSML Enhanced Test.mp4"

    temp_dir = Path(tempfile.mkdtemp(prefix="zorro_ssml_"))

    speech_count = sum(1 for s in SEGMENTS if s.text)
    silence_count = sum(1 for s in SEGMENTS if s.silence_ms > 0)
    total_silence_ms = sum(s.silence_ms for s in SEGMENTS if s.silence_ms > 0)

    print("=" * 60)
    print("Enhanced Jenny Neural - Segment-Based Synthesis")
    print("=" * 60)
    print(f"Voice: {VOICE}")
    print(f"Segments: {speech_count} speech + {silence_count} silences ({total_silence_ms/1000:.1f}s total pauses)")
    print(f"Output: {output_mp4.name}")
    print(f"Temp dir: {temp_dir}")
    print()

    segment_files = []
    errors = 0

    for i, seg in enumerate(SEGMENTS):
        idx = f"[{i+1:03d}/{len(SEGMENTS):03d}]"

        if seg.silence_ms > 0:
            silence_file = temp_dir / f"seg_{i:03d}_silence_{seg.silence_ms}ms.mp3"
            ok = generate_silence(seg.silence_ms, silence_file)
            if ok:
                segment_files.append(silence_file)
                print(f"  {idx} --- {seg.silence_ms}ms silence ---")
            else:
                print(f"  {idx} ERROR generating silence")
                errors += 1
        else:
            speech_file = temp_dir / f"seg_{i:03d}_speech.mp3"
            print(f"  {idx} {seg.label} (rate={seg.rate}, pitch={seg.pitch})")
            try:
                ok = await synthesize_segment(seg, speech_file)
                if ok:
                    size_kb = speech_file.stat().st_size / 1024
                    segment_files.append(speech_file)
                    print(f"         -> {size_kb:.0f} KB")
                else:
                    print(f"         -> ERROR: no output")
                    errors += 1
            except Exception as e:
                print(f"         -> ERROR: {e}")
                errors += 1

    print()

    if errors > 0:
        print(f"WARNING: {errors} segments failed. Continuing with {len(segment_files)} successful segments.")

    if not segment_files:
        print("ERROR: No segments were generated.")
        shutil.rmtree(temp_dir, ignore_errors=True)
        sys.exit(1)

    print(f"Concatenating {len(segment_files)} segments into MP4...")
    ok = concatenate_segments(segment_files, output_mp4)

    shutil.rmtree(temp_dir, ignore_errors=True)

    if ok and output_mp4.exists():
        size_kb = output_mp4.stat().st_size / 1024
        print()
        print(f"SUCCESS: {output_mp4.name}")
        print(f"  Size: {size_kb:.0f} KB ({size_kb/1024:.1f} MB)")
        print(f"  Location: {output_mp4}")
        print(f"  Dashboard: http://localhost:8888/")
    else:
        print("ERROR: Final concatenation failed.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
