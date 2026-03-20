#!/usr/bin/env python3
"""
Enhanced Full-Content Weekly Message Audio - Segment-Based Synthesis
=====================================================================
Uses the FULL original BQ-sourced script content (all 41 events) with
segment-based delivery: varied rate/pitch for headers, silence gaps
between items and sections.

This is a TEST script — does not modify the main pipeline.
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
    text: Optional[str] = None
    silence_ms: int = 0
    rate: str = "+0%"
    pitch: str = "+0Hz"
    volume: str = "+0%"
    label: str = ""


def silence(ms: int, label: str = "pause") -> Segment:
    return Segment(silence_ms=ms, label=label)


def group_header(text: str) -> Segment:
    return Segment(text=text, rate="-10%", pitch="+1Hz", label=f"GROUP: {text}")


def area_header(text: str) -> Segment:
    return Segment(text=text, rate="-5%", pitch="+1Hz", label=f"AREA: {text}")


def content(text: str, label: str) -> Segment:
    return Segment(text=text, rate="+0%", label=label)


def intro(text: str, label: str, rate: str = "-5%", pitch: str = "+2Hz") -> Segment:
    return Segment(text=text, rate=rate, pitch=pitch, label=label)


# ── Full script segments — verbatim from original BQ output ─────────────────

SEGMENTS = [
    # ── Intro ──
    intro("Hello! Your Week 4 Weekly Messages are Here!", "Greeting"),
    silence(400),
    Segment(text="Please Visit the Landing Page to access full content.", rate="-3%", label="Intro instruction"),
    silence(700, "section break"),

    # ═══════════════════════════════════════════════════════════════════════════
    # FOOD & CONSUMABLES
    # ═══════════════════════════════════════════════════════════════════════════
    group_header("Food and Consumables Merchant Messages."),
    silence(500),

    # ── Beauty and Consumables ──
    area_header("Beauty and Consumables Area."),
    silence(300),

    content(
        "Dept. 13: Tide evo is a category-defining innovation from the number one laundry brand, "
        "reinventing detergent as a lightweight, waterless sheet with no fillers, no plastic bottles, "
        "and sustainable packaging. Backed by 3 billion or more national impressions and strong "
        "Walmart.com visibility, in-store displays begin March 7 with a full rollout by April 11.",
        "Dept 13 - Tide Evo"
    ),
    silence(400),

    content(
        "Dept. 40: Modularizing of the Health and Wellness Wall. "
        "The Health and Wellness Wall is being modularized to create a cohesive, better-merchandised "
        "space that improves tracking, maximizes monthly space use, increases sell-through, reduces "
        "Nil Picks, and strengthens OPD performance on top categories. Feature Space and Sales will "
        "be replaced with C110 Modular on the Quarterly Relay starting in March; features will run "
        "only in space designated as Dept. 40 Health and Wellness, with store choice available in "
        "remaining sections.",
        "Dept 40 - Health & Wellness Wall"
    ),
    silence(700, "section break"),

    # ── Food Area ──
    area_header("Food Area."),
    silence(300),

    content(
        "Dept. 90: Fairlife Supply Update. Starting Week 5, February 28 through March 6, expect "
        "increased Fairlife shipments and better in-stocks in Dept. 90. A new Fairlife production "
        "facility is now shipping, boosting capacity to meet demand. Why it matters: Fairlife is "
        "one of the category's fastest growers, up 25% in two years, with another 15% expected "
        "this year. Customers want the lower sugar, higher protein, lactose-free benefits.",
        "Dept 90 - Fairlife"
    ),
    silence(400),

    content(
        "Dept. 95: Gatorade 20-oz 8-packs, lower EDLP. Gatorade is investing in 20-oz 8-packs, "
        "dropping EDLP to $6.98 from $7.98, starting Monday, Feb. 23. The lower price is designed "
        "to reengage customers and drive higher demand for the pack size and the category. To build "
        "awareness, an FSS endcap is planned, Plan IDs 230284 and 230288. Depending on the store, "
        "the feature runs Feb. 21 through March 6 or Feb. 21 through April 3. Feature stores will "
        "receive an initial PO distribution of 20 to 50 cases across five flavors.",
        "Dept 95 - Gatorade EDLP"
    ),
    silence(400),

    content(
        "Dept. 95: Introducing Gatorade Lower Sugar and No Artificials. Gatorade is launching a "
        "Lower Sugar, No Artificials line to address top sports drink concerns: sugar and artificial "
        "colors and flavors. Shoppers get the same taste and electrolytes with 75% less sugar and "
        "no artificial flavors or colors. Launch is Monday, Feb. 23, supported by major media. "
        "Week 5, February 28 through March 6: stores in the FSS plan should build a four-flavor, "
        "28-oz endcap, Plan ID 227476, and will receive DSD PO support.",
        "Dept 95 - Gatorade Lower Sugar"
    ),
    silence(400),

    content(
        "Dept. 95: Keep On The Border Chips In-stock. On The Border Tortilla Chips, item 598056711, "
        "are on Rollback through April and selling fast, but nil picks are rising because product is "
        "missing from the sidecounter. While it's set in the DSD tortilla chip section, it ships "
        "through the warehouse and can be missed during stocking. Take action: Have associates check "
        "the tortilla chip sidecounter daily and keep it full. If you need more product, order "
        "through the Store Feature Order Tool.",
        "Dept 95 - On The Border"
    ),
    silence(400),

    content(
        "Dept. 95: Poppi to Pepsi DSD, effective Monday, March 2. Starting Monday, March 2, Poppi "
        "beverages will transition to Pepsi direct store delivery. Pepsi will own delivery, ordering, "
        "stocking, rotation, merchandising and shelf and display maintenance for all Poppi items, "
        "including modular sets, secondary placements and promos. Why it matters: Expect improved "
        "in-stocks, faster replenishment, less backroom handling and more consistent on-shelf "
        "availability, reducing manual ordering and outs. Take action: Confirm on-hands are accurate "
        "and modulars are set correctly.",
        "Dept 95 - Poppi DSD"
    ),
    silence(400),

    content(
        "Dept. 95: Energy Sidekicks Are Being Updated. Beginning Week 3, permanent Energy sidekicks "
        "are being updated to increase holding power and add seasonal and LTO space. Monster's "
        "permanent sidekick will transition to Alani plus Celsius, using existing Monster fixtures; "
        "Monster will not have a permanent sidekick in stores through Week 8. In Week 9, Monster's "
        "permanent sidekick returns to select stores as an add-on, not a replacement, alongside "
        "existing Red Bull and Alani plus Celsius sidekicks. Suppliers are aligned and expected to "
        "complete modulars to the new standard.",
        "Dept 95 - Energy Sidekicks"
    ),
    silence(700, "section break"),

    # ── Fresh Area ──
    area_header("Fresh Area."),
    silence(300),

    content(
        "Prima Della Pre-Sliced Honey Turkey Shortage. Temporary shortage: Pre-sliced Prima Della "
        "Honey Roasted Turkey Breast, items 578738649 and 671139503, is on supplier constraint, so "
        "replenishment is temporarily turned off. Bulk Prima Della Honey Roasted Turkey is not "
        "impacted, and suppliers will continue shipping pre-sliced product through Week 4. "
        "Replenishment is expected to resume between Weeks 8 and 13. Take action: Keep the Deli "
        "case full by expanding facings of adjacent pre-sliced turkey items and using bulk product "
        "where appropriate.",
        "Fresh - Prima Della Shortage"
    ),
    silence(400),

    content(
        "Dept. 93: Lent focus items. Lent is here. Set Dept. 93 up for success by prioritizing "
        "41/60 shrimp, salmon and tilapia. Ensure features are set, aisle locations are signed, "
        "and seafood modulars are worked daily to protect in-stocks and capture the seasonal lift.",
        "Dept 93 - Lent Focus"
    ),
    silence(300),

    content(
        "Dept. 93: Item in the spotlight, Great Value tilapia on Rollback. Great Value Frozen "
        "Skinless Tilapia Fillets, 4-pound, is on Rollback for $17.47. With Lent demand, plan for "
        "about a 20% lift, roughly 30 units per week, but only if it's on the floor, full and easy "
        "to shop. Stock up and feature it prominently.",
        "Dept 93 - Tilapia Spotlight"
    ),
    silence(300),

    content(
        "Dept. 93: St.",
        "Dept 93 - St."
    ),
    silence(400),

    content(
        "Produce in-stock risks: Easter basket focus. Keep shelves full for Easter basket produce. "
        "Bulk plums are pressured due to early Chile season and nonaccepted varieties, get well "
        "Week 4. Green onions and cilantro are weather-impacted; cilantro improves around Week 5, "
        "green onions around Week 8. Bulk corn is tight after major Florida freeze losses; protect "
        "packaged corn. Carrots and organic lettuces and celery are also weather-impacted. Watch "
        "March through April risk on watermelons, blueberries and cabbage.",
        "Fresh - Produce In-Stock Risks"
    ),
    silence(400),

    content(
        "Dept. 81: Easter Prep and Brown 'N Serve. Prep now for Easter staples in Dept. 81, "
        "including Brown 'N Serve rolls, which are store-managed. Check the backroom regularly for "
        "arrivals and keep the modular home location full. As the holiday nears, plan cross-merchandising "
        "by setting 4-way sides or saddlebag displays near the ham section to drive add-on sales.",
        "Dept 81 - Easter Prep"
    ),
    silence(400),

    content(
        "Dept. 98: Spring Feature Planning and Post-Seasonal Cleanup. Spring is a chance to grow "
        "baskets with solution-driven, high-margin displays. Spotlight angel food items: the 14-ounce "
        "cake ring, item 563001974, for mass displays, the 10-ounce bar, item 662658723, for smaller "
        "occasions, and 6-count dessert shells, item 653323529, as a key add-on. Create a seasonal "
        "destination, especially a Strawberry Shortcake set, by cross-merchandising Bakery with "
        "fresh strawberries from Produce and Cool Whip from Dairy and Frozen across frozen, chilled "
        "and ambient areas.",
        "Dept 98 - Spring Features"
    ),
    silence(700, "section break"),

    # ═══════════════════════════════════════════════════════════════════════════
    # GENERAL MERCHANDISE
    # ═══════════════════════════════════════════════════════════════════════════
    group_header("General Merchandise Merchant Messages."),
    silence(500),

    # ── Entertainment ──
    area_header("Entertainment Area."),
    silence(300),

    content(
        "Dept. 72: Three Samsung soundbars are being discontinued with no restock, so starting "
        "Feb. 21 stores will receive two JBL replacement models to keep the modular in-stock. Use "
        "the lookup tool to confirm which JBL items you'll get, place them in the former Samsung "
        "modular space, double-face as needed, and note pricing is already updated in the system.",
        "Dept 72 - Samsung/JBL Soundbars"
    ),
    silence(400),

    content(
        "Dept. 72: PC Software Display Setup. Week 50 shipment: magnetic frame plus scannable "
        "insert, set immediately; ignore Hold for Anderson. Place on Electronics cash wrap near POS; "
        "message must face customer. Insert scannable sheet for checkout purchase. Upcoming POS "
        "prompt will remind associates to suggest PC software with laptop purchases. Featured SKUs: "
        "Norton VPN and 360 tiers, McAfee Total Protection, HR Block 2025 Basic and Deluxe. "
        "Actions: Install new placemat at cash wrap. Ensure price tags are printed and placed on "
        "laptop PC software fixtures.",
        "Dept 72 - PC Software Display"
    ),
    silence(400),

    content(
        "Dept. 85: Graduation season is here. Remind customers Walmart Photo has party essentials "
        "like yard signs, banners, signature boards, and mounted prints, with more customizable "
        "options at walmart.com/photo.",
        "Dept 85 - Graduation"
    ),
    silence(700, "section break"),

    # ── Fashion ──
    area_header("Fashion Area."),
    silence(300),

    content(
        "Dept. 29: Sleepwear Preview. The week 5 update includes an assortment of licensed "
        "short-sleeved shorts sets, new Cloud Core cotton jersey items for the No Boundaries "
        "sidewall, and satin cami and short sets from No Boundaries.",
        "Dept 29 - Sleepwear Preview"
    ),
    silence(400),

    content(
        "Dept. 32: Claire's Jewelry Transition. Dept. 32 has a three phase timeline for the "
        "transition to Walmart-owned inventory for Claire's Jewelry, with start dates in weeks 4, "
        "14 and 26. RDS reps will be in stores to access backroom areas, restock and tidy Claire's "
        "fixtures, and properly dispose of any damaged Claire's product.",
        "Dept 32 - Claire's Transition"
    ),
    silence(400),

    content(
        "Dept. 34: Women's Plus Core Wall Clarification. Some stores did not set the Women's Plus "
        "Core Wall correctly, so we included specific instructions for adding a jetrail and which "
        "items go on which rows.",
        "Dept 34 - Women's Plus Core Wall"
    ),
    silence(400),

    content(
        "Depts. 24 and 33: Kids Rack Expansion. Select stores should have received one or two "
        "additional rack fixtures per department by week 3 for a broader assortment and improved "
        "story-telling.",
        "Depts 24/33 - Kids Racks"
    ),
    silence(400),

    content(
        "Fashion: T-Shirt Spinner Graphics. Stores can now print t-shirt spinner graphics from "
        "Better Way.",
        "Fashion - T-Shirt Graphics"
    ),
    silence(300),

    content(
        "Fashion: Your Part 2 Spring Guides are Here! Updated Fashion guides are now available on "
        "Better Way, including everything you need to properly set seasonal Fashion strategies, from "
        "shop layouts and volume drivers to mannequin styling and trend highlights.",
        "Fashion - Spring Guides"
    ),
    silence(700, "section break"),

    # ── Hardlines ──
    area_header("Hardlines Area."),
    silence(300),

    content(
        "Dept. 9: Water Sports modular items are delayed, with most arriving one to three weeks "
        "after the modular set, and a few, like Ozark Trail Snorkeling, potentially later. Use "
        "on-time U.S. Divers snorkeling items to fill any open shelf space while you wait for "
        "late arrivals.",
        "Dept 9 - Water Sports Delay"
    ),
    silence(400),

    content(
        "Dept. 11: Hart inventory is selling down, so flex and relabel to keep the modular full, "
        "and don't remove the Hart endcap until Hyper Tough organizers and sign arrive.",
        "Dept 11 - Hart Inventory"
    ),
    silence(400),

    content(
        "Dept. 11: Updated 5-gallon water exchange prices take effect week 4, Feb. 21 to 27. Make "
        "sure your store reflects the new pricing and update signage as needed for a smooth "
        "transition and compliance.",
        "Dept 11 - Water Exchange Pricing"
    ),
    silence(400),

    content(
        "Dept. 9: Ball Bin modulars were simplified to improve in-stocks. W&B Enterprises-supported "
        "stores replenish two core balls plus a store-specific top seller, flex into the Franklin Jr. "
        "Football spot, while other stores keep the standard three items. Week 14 removes the Direct "
        "Store Delivery shipper and sends extra core-ball inventory until the full assortment returns "
        "in the second half of the year.",
        "Dept 9 - Ball Bins"
    ),
    silence(400),

    content(
        "Dept. 11: Heaters are selling out and won't be restocked, so expect gaps until the spring "
        "reset week 5 in the South and week 9 in the North. Fill heater space with incoming Lasko "
        "and Midea fans over the next four weeks; until then, flex nearby hardware items to keep "
        "shelves shoppable.",
        "Dept 11 - Heaters to Fans"
    ),
    silence(700, "section break"),

    # ── Home ──
    area_header("Home Area."),
    silence(300),

    content(
        "Dept. 74: Get Ready for a Major Reset in Bulk Storage. Stores can expect a significant "
        "number of deletes, including all of category 160, as we prepare for a major modular reset "
        "in Bulk Storage in week 7.",
        "Dept 74 - Bulk Storage Reset"
    ),
    silence(400),

    content(
        "Dept. 74: Simplifying Picking With a Label Update. We have updated the lid label for "
        "Mainstays 13-gallon swing top trash cans so they are easier to identify for digital "
        "shoppers, resulting in fewer nil picks.",
        "Dept 74 - Label Update"
    ),
    silence(700, "section break"),

    # ── Seasonal ──
    area_header("Seasonal Area."),
    silence(300),

    content(
        "Dept. 18 and 67: Easter is earlier with a shorter selling window, so set modulars on time "
        "and flex New and Now and extra space to eggs and baskets; eggs and grass may be short on "
        "the first shipment but should fill in with a week 5 replenishment.",
        "Depts 18/67 - Easter Timing"
    ),
    silence(300),

    content(
        "Dept. 67: Coordinate Easter PFS relays with Hallmark and American Greetings, set seasonal "
        "features quickly, and follow the standard helium ring-up process; Dabney Lee endcaps are "
        "existing-inventory only, some markdowns, no additional shipments.",
        "Dept 67 - Easter PFS"
    ),
    silence(700, "section break"),

    # ═══════════════════════════════════════════════════════════════════════════
    # OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    group_header("Operations Messages."),
    silence(500),

    # ── Asset Protection ──
    area_header("Asset Protection Area."),
    silence(300),

    content(
        "Dept. 46: Select stores have Maybelline modular delays because of printing issues; set the "
        "modular as close as possible and expect Premium to install missing graphics by week 7, "
        "March 14 to 20.",
        "Dept 46 - Maybelline Delays"
    ),
    silence(400),

    content(
        "Dept. 9: Wave 2 firearm markdowns run Feb. 21 to 27. Use the lookup tool, complete only "
        "the directed price changes, and feature clearance and Rollback items in the gun case with "
        "certified coverage and ready supplies.",
        "Dept 9 - Firearm Markdowns"
    ),
    silence(400),

    content(
        "Backroom and Dept. 16: Select Kingsford Charcoal Items Will Be Delivered on HVDC Trailers. "
        "Beginning week 5, February 28 through March 6, select Kingsford Charcoal items will "
        "transition from RDC to HVDC delivery to support automation and create additional RDC "
        "capacity.",
        "Dept 16 - Kingsford HVDC"
    ),
    silence(700, "section break"),

    # ── Auto Care ──
    area_header("Auto Care Area."),
    silence(300),

    content(
        "Affirm is no longer accepted for in-store payments; customers can still manage existing "
        "Affirm purchases and returns as usual. Walmart's buy-now-pay-later option is now OnePay "
        "Later with Klarna, and stores should update signage and ensure teams know the change.",
        "Auto Care - Affirm to OnePay"
    ),
    silence(700, "section break"),

    # ── Backroom and Claims ──
    area_header("Backroom and Claims Area."),
    silence(300),

    content(
        "Backroom: Join the DSD Office Hours for Real-Time Support. Join our bi-weekly DSD Office "
        "Hours on Tuesday, March third from 2 to 3 p.m. Central on Teams to connect directly with "
        "Vendors, Merchants and Operations to resolve issues quickly. If you can't attend, sessions "
        "are held every other Tuesday.",
        "Backroom - DSD Office Hours"
    ),
    silence(700, "section break"),

    # ── Frontend ──
    area_header("Frontend Area."),
    silence(300),

    content(
        "Friendliest Front End Spring Edition starts Feb. 28. Stores compete to boost CX Scores "
        "from a week 4 baseline, with recognition for top improvement.",
        "Frontend - Spring Edition"
    ),
    silence(400),

    content(
        "Front End Operations Resolution team supports stores with Front End and Financial Services "
        "questions and can be reached Monday through Friday, 7:30 a.m. to 5 p.m. Central by phone "
        "or email.",
        "Frontend - Operations Resolution"
    ),
    silence(700, "section break"),

    # ── Pickup ──
    area_header("Pickup Area."),
    silence(300),

    content(
        "Store Fulfillment: Oversized Picking Safety Update. When a customer orders a high quantity "
        "of a single heavy item like water, mulch or soil, GIF will automatically split the pick "
        "walk to reduce strain and promote safer cart handling. If prompted, start the new walk with "
        "a new L-cart and follow all on-screen directions.",
        "Pickup - Oversized Safety"
    ),
    silence(700, "section break"),

    # ── People ──
    area_header("People Area."),
    silence(300),

    content(
        "As you get more comfortable with My Assistant and AI, start using it to improve processes "
        "by asking how tasks can be simplified or done more efficiently.",
        "People - AI Assistant"
    ),
    silence(700, "section break"),

    # ── Total Store ──
    area_header("Total Store Area."),
    silence(300),

    content(
        "Clean Floor Safety. Clean floors prevent slips, trips, and falls. Clean spills immediately, "
        "or guard the area and get help. Never leave spills unattended. Keep aisles clear, remove "
        "debris, and report wet spots, damaged flooring, or repeat hazards right away.",
        "Total Store - Floor Safety"
    ),
    silence(400),

    content(
        "Dept. 79: Spring Baby Days runs Feb. 16 to April 17, featuring extended in-store and "
        "digital features, strong omni Rollbacks and newness like Wonder Nation baby fashion. Set "
        "signage and features on time and keep item locations updated to support pickup and delivery.",
        "Dept 79 - Spring Baby Days"
    ),
    silence(700, "section break"),

    # ── Outro ──
    intro("That's your Week 4 Weekly Messages.", "Outro", rate="-5%", pitch="+1Hz"),
    silence(400),
    intro("Have a Great Week!", "Sign-off", rate="-8%", pitch="+2Hz"),
]


# ── Synthesis engine (same proven approach) ─────────────────────────────────

async def synthesize_segment(seg: Segment, output_path: Path, retries: int = 3) -> bool:
    """Synthesize a single text segment with edge-tts, with retry on transient errors."""
    import edge_tts
    for attempt in range(1, retries + 1):
        try:
            comm = edge_tts.Communicate(seg.text, VOICE, rate=seg.rate, pitch=seg.pitch, volume=seg.volume)
            await comm.save(str(output_path))
            if output_path.exists() and output_path.stat().st_size > 0:
                return True
        except Exception as e:
            if attempt < retries:
                wait = attempt * 2
                print(f"         -> Retry {attempt}/{retries} after error: {e} (waiting {wait}s)")
                await asyncio.sleep(wait)
            else:
                raise
    return False


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
    output_mp4 = output_dir / "Week 4 - Enhanced Full Content Test.mp4"

    temp_dir = Path(tempfile.mkdtemp(prefix="zorro_enhanced_full_"))

    speech_count = sum(1 for s in SEGMENTS if s.text)
    silence_count = sum(1 for s in SEGMENTS if s.silence_ms > 0)
    total_silence_ms = sum(s.silence_ms for s in SEGMENTS if s.silence_ms > 0)

    print("=" * 60)
    print("Enhanced Full Content - Segment-Based Synthesis")
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
