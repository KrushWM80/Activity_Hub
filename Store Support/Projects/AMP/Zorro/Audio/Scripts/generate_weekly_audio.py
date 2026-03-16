#!/usr/bin/env python3
"""
Weekly Message Audio Pipeline
Automated: BigQuery → Extract Summarized text → Build TTS Script → Jenny Neural MP4

Usage:
    # As standalone script:
    python generate_weekly_audio.py --week 4 --fy 2027
    
    # As importable module:
    from generate_weekly_audio import generate_weekly_message_audio
    result = generate_weekly_message_audio(week=4, fy=2027)
"""
import os
import re
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# BigQuery credentials
os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS',
    os.path.join(os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'))

# Area groupings for the TTS script template (ordered)
# Each area entry: (BQ Store_Area value, display name for TTS)
AREA_GROUPS = {
    "Food & Consumables Merchant Messages": [
        ("Consumables", "Beauty and Consumables"),
        ("Food", "Food"),
        ("Fresh", "Fresh"),
    ],
    "General Merchandise Merchant Messages": [
        ("Entertainment", "Entertainment"),
        ("Fashion", "Fashion"),
        ("Hardlines", "Hardlines"),
        ("Home", "Home"),
        ("Seasonal", "Seasonal"),
    ],
    "Operations Messages": [
        ("Asset Protection", "Asset Protection"),
        ("Auto Care", "Auto Care"),
        ("Backroom and Claims", "Backroom and Claims"),
        ("Frontend", "Frontend"),
        ("Digital", "Pickup"),
        ("People", "People"),
        ("Total Store", "Total Store"),
    ],
}

# Reverse lookup: BQ Store_Area → (group name, display name)
AREA_TO_GROUP = {}
AREA_DISPLAY_NAME = {}
for group, areas in AREA_GROUPS.items():
    for bq_name, display_name in areas:
        AREA_TO_GROUP[bq_name] = group
        AREA_DISPLAY_NAME[bq_name] = display_name

# Cache directory for BQ data (survives VPN state changes)
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class HTMLTextExtractor(HTMLParser):
    """Extract plain text from HTML, skipping tags."""
    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data):
        self.text_parts.append(data)

    def get_text(self):
        return ' '.join(self.text_parts)


def html_to_text(html_str):
    parser = HTMLTextExtractor()
    parser.feed(html_str)
    return parser.get_text()


def extract_summarized_text(raw_text):
    """Extract text after summary marker from message body.
    
    Handles all known variants:
      - 'Summarized: text'   (colon right after)
      - 'Summarize: text'    (no d, colon right after)
      - 'Summarized : text'  (space before colon — from HTML newline converted to space)
      - 'Summarized  text'   (no colon at all, just content after whitespace)
    """
    # Pattern 1: Summarize or Summarized, optional whitespace, then colon
    match = re.search(r'Summarize[d]?\s*:\s*(.*)', raw_text, re.DOTALL | re.IGNORECASE)
    if not match:
        # Pattern 2: Summarized followed by whitespace then content (no colon)
        match = re.search(r'Summarized\s+(.*)', raw_text, re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    text = match.group(1).strip()
    # Clean up CSS artifacts and extra whitespace
    text = re.sub(r'::marker\s*\{[^}]*\}', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Truncate at reasonable length for TTS
    if len(text) > 600:
        # Try to cut at a sentence boundary
        cut = text[:600].rfind('. ')
        if cut > 200:
            text = text[:cut + 1]
        else:
            text = text[:600] + '...'
    return text


def fetch_week_events(client, week, fy):
    """Query AMP ALL 2 for Merchant Messages in Review for Publish - No Comms status."""
    query = """
    SELECT DISTINCT event_id, Store_Area, Title, Headline, Dept, Message_Type, Status
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = @fy AND WM_Week = @week
      AND Message_Type = 'Merchant Message'
      AND Status = 'Review for Publish review - No Comms'
    ORDER BY Store_Area, Title
    """
    from google.cloud.bigquery import ScalarQueryParameter, QueryJobConfig
    job_config = QueryJobConfig(query_parameters=[
        ScalarQueryParameter("fy", "INT64", fy),
        ScalarQueryParameter("week", "STRING", str(week)),
    ])
    rows = list(client.query(query, job_config=job_config).result())
    logger.info(f"Found {len(rows)} Weekly Messages events for FY{fy} Week {week}")
    return rows


def fetch_message_bodies(client, event_ids):
    """Batch query Cosmos raw table for msg_txt HTML bodies."""
    if not event_ids:
        return {}
    ids_str = ", ".join([f"'{eid}'" for eid in event_ids])
    query = f"""
    SELECT event_id, msg_txt
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    WHERE event_id IN ({ids_str})
    """
    rows = list(client.query(query).result())
    msg_map = {}
    for r in rows:
        msg = r.msg_txt
        if msg:
            if isinstance(msg, dict):
                arr = msg.get('array', [])
                if arr:
                    msg_map[r.event_id] = arr[0]
            else:
                msg_map[r.event_id] = str(msg)
    logger.info(f"Retrieved message bodies for {len(msg_map)}/{len(event_ids)} events")
    return msg_map


def build_tts_script(week, events_with_summaries):
    """Build the TTS-friendly script from area-grouped summarized events.
    
    Groups by team (Food & Consumables, General Merchandise, Operations)
    then sub-groups by individual area within each team.
    """
    # Group events by area group, then sub-group by area
    grouped = {}  # group_name -> {bq_area -> [events]}
    for group_name in AREA_GROUPS:
        grouped[group_name] = {}
        for bq_name, _ in AREA_GROUPS[group_name]:
            grouped[group_name][bq_name] = []

    ungrouped = []
    for event in events_with_summaries:
        area = event['store_area']
        group = AREA_TO_GROUP.get(area)
        if group:
            if area not in grouped[group]:
                grouped[group][area] = []
            grouped[group][area].append(event)
        else:
            ungrouped.append(event)

    # Build script
    lines = []
    lines.append(f"Hello! Your Week {week} Weekly Messages are Here!")
    lines.append("")
    lines.append("Please Visit the Landing Page to access full content.")

    for group_name in AREA_GROUPS:
        # Check if this group has any events
        area_events = grouped[group_name]
        if not any(area_events.values()):
            continue
        lines.append("")
        lines.append(f"{group_name}:")

        # Sub-group by area in defined order
        for bq_name, display_name in AREA_GROUPS[group_name]:
            events = area_events.get(bq_name, [])
            if not events:
                continue
            lines.append("")
            lines.append(f"{display_name} Area:")
            lines.append("")
            for evt in events:
                lines.append(evt['summary_text'])
                lines.append("")

    # Include any ungrouped areas
    if ungrouped:
        lines.append("")
        lines.append("Additional Messages:")
        lines.append("")
        for evt in ungrouped:
            display = AREA_DISPLAY_NAME.get(evt['store_area'], evt['store_area'])
            lines.append(f"{display}: {evt['summary_text']}")
            lines.append("")

    lines.append(f"That's your Week {week} Weekly Messages, Have a Great Week!")

    return "\n".join(lines)


def save_cache(week, fy, data):
    """Save BQ data to local JSON cache for offline synthesis."""
    cache_file = CACHE_DIR / f"week_{week}_fy{fy}.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    logger.info(f"Cached data to {cache_file.name}")
    return cache_file


def load_cache(week, fy):
    """Load cached BQ data if available."""
    cache_file = CACHE_DIR / f"week_{week}_fy{fy}.json"
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded cache from {cache_file.name} ({data.get('cached_at', 'unknown')}")
        return data
    return None


def fetch_and_cache_bq_data(week, fy):
    """
    Phase 1: Fetch BQ data and cache locally. Requires VPN.
    Returns dict with event data, summaries, and counts.
    """
    from google.cloud import bigquery
    client = bigquery.Client(project='wmt-assetprotection-prod')

    logger.info(f"=== Phase 1: BQ Data Fetch — FY{fy} Week {week} ===")

    # Step 1: Fetch Weekly Messages events with No Comms status
    logger.info("Step 1: Fetching Weekly Messages from AMP ALL 2...")
    events = fetch_week_events(client, week, fy)
    if not events:
        return {'error': f"No Weekly Messages with No Comm status found for FY{fy} Week {week}"}

    # Step 2: Fetch message bodies from Cosmos
    logger.info("Step 2: Fetching message bodies from Cosmos...")
    event_ids = [r.event_id for r in events]
    msg_map = fetch_message_bodies(client, event_ids)

    # Step 3: Extract Summarized text
    logger.info("Step 3: Extracting Summarized text...")
    events_with_summaries = []
    events_without = []

    for row in events:
        eid = row.event_id
        if eid not in msg_map:
            events_without.append({'event_id': eid, 'title': row.Title, 'area': row.Store_Area, 'status': row.Status})
            continue

        raw_text = html_to_text(msg_map[eid])
        summary = extract_summarized_text(raw_text)

        if summary:
            events_with_summaries.append({
                'event_id': eid,
                'store_area': row.Store_Area,
                'title': row.Title,
                'status': row.Status,
                'summary_text': summary,
            })
        else:
            events_without.append({'event_id': eid, 'title': row.Title, 'area': row.Store_Area, 'status': row.Status})

    # Count by status
    review_no_comm = sum(1 for r in events if 'Review for Publish' in (r.Status or ''))

    cache_data = {
        'week': week,
        'fy': fy,
        'cached_at': datetime.now().isoformat(),
        'event_count': len(events),
        'review_no_comm_count': review_no_comm,
        'summarized_count': len(events_with_summaries),
        'events_with_summaries': events_with_summaries,
        'events_without_summary': events_without,
    }

    # Save to local cache
    save_cache(week, fy, cache_data)

    logger.info(f"Weekly Messages (Review for Publish - No Comm): {review_no_comm}")
    logger.info(f"Total No Comm events: {len(events)}")
    logger.info(f"With Summarized text: {len(events_with_summaries)}")
    logger.info(f"Without Summarized text: {len(events_without)}")

    return cache_data


def synthesize_from_cache(week, fy, voice="Jenny", rate=0.95, output_dir=None):
    """
    Phase 2: Build TTS script from cached data and synthesize MP4. Requires OFF VPN.
    """
    cache_data = load_cache(week, fy)
    if not cache_data:
        return {'success': False, 'error': f'No cached data for FY{fy} Week {week}. Run Phase 1 (fetch data) on VPN first.'}

    events_with_summaries = cache_data['events_with_summaries']
    if not events_with_summaries:
        return {
            'success': False,
            'error': "No events have 'Summarized:' text in their message body",
            'event_count': cache_data['event_count'],
            'review_no_comm_count': cache_data.get('review_no_comm_count', 0),
            'summarized_count': 0,
        }

    # Build TTS script
    logger.info("Building TTS script from cached data...")
    script = build_tts_script(week, events_with_summaries)
    logger.info(f"Script: {len(script)} characters, {len(script.split())} words")

    # Synthesize audio
    logger.info("Synthesizing with Jenny Neural voice...")
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "output" / "Audio"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"Weekly Messages Audio Template - Summarized - Week {week} - Jenny Neural - Vimeo.mp4"

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from windows_media_synthesizer import WindowsMediaSynthesizer

    synth = WindowsMediaSynthesizer()
    success = synth.synthesize_to_mp4(script, str(output_file), voice=voice, rate=rate)

    if success and output_file.exists():
        size_kb = output_file.stat().st_size / 1024
        logger.info(f"Success! {output_file.name} ({size_kb:.1f} KB)")
        return {
            'success': True,
            'output_file': str(output_file),
            'event_count': cache_data['event_count'],
            'review_no_comm_count': cache_data.get('review_no_comm_count', 0),
            'summarized_count': cache_data['summarized_count'],
            'script_length': len(script),
            'events_without_summary': cache_data.get('events_without_summary', []),
        }
    else:
        return {
            'success': False,
            'error': 'Audio synthesis failed. Are you off VPN? Jenny Neural requires speech.platform.bing.com access.',
            'event_count': cache_data['event_count'],
            'review_no_comm_count': cache_data.get('review_no_comm_count', 0),
            'summarized_count': cache_data['summarized_count'],
            'script_length': len(script),
        }


def generate_weekly_message_audio(week=None, fy=None, voice="Jenny", rate=0.95, output_dir=None, phase=None):
    """
    Full pipeline with two-phase VPN support:
      phase='fetch'     → BQ data pull + cache (requires VPN)
      phase='synthesize' → TTS from cache (requires OFF VPN)
      phase=None         → try full pipeline; on BQ failure, fall back to cache
    
    Returns dict with: success, output_file, event_count, review_no_comm_count,
                        summarized_count, script_length, error
    """
    result = {
        'success': False,
        'output_file': None,
        'event_count': 0,
        'review_no_comm_count': 0,
        'summarized_count': 0,
        'script_length': 0,
        'error': None,
        'events_without_summary': [],
        'phase_completed': None,
    }

    # Phase 1 only: fetch and cache
    if phase == 'fetch':
        if week is None or fy is None:
            result['error'] = 'week and fy are required for fetch phase'
            return result
        try:
            cache_data = fetch_and_cache_bq_data(week, fy)
            if 'error' in cache_data:
                result['error'] = cache_data['error']
                return result
            result['success'] = True
            result['event_count'] = cache_data['event_count']
            result['review_no_comm_count'] = cache_data['review_no_comm_count']
            result['summarized_count'] = cache_data['summarized_count']
            result['events_without_summary'] = cache_data.get('events_without_summary', [])
            result['phase_completed'] = 'fetch'
            return result
        except Exception as e:
            result['error'] = f'BQ fetch failed: {e}'
            return result

    # Phase 2 only: synthesize from cache
    if phase == 'synthesize':
        if week is None or fy is None:
            result['error'] = 'week and fy are required for synthesize phase'
            return result
        return synthesize_from_cache(week, fy, voice=voice, rate=rate, output_dir=output_dir)

    # Auto mode: try full pipeline, fall back to cache on BQ failure
    if week is None or fy is None:
        result['error'] = 'week and fy are required (auto-detect not available in two-phase mode)'
        return result

    bq_available = False
    try:
        cache_data = fetch_and_cache_bq_data(week, fy)
        if 'error' in cache_data:
            result['error'] = cache_data['error']
            return result
        bq_available = True
    except Exception as e:
        logger.warning(f"BQ unavailable ({e}), checking for cached data...")
        cache_data = load_cache(week, fy)
        if cache_data:
            logger.info("Using cached BQ data for synthesis")
        else:
            result['error'] = f'BQ unavailable and no cached data. Connect to VPN and run fetch phase first. ({e})'
            return result

    result['event_count'] = cache_data['event_count']
    result['review_no_comm_count'] = cache_data.get('review_no_comm_count', 0)
    result['summarized_count'] = cache_data['summarized_count']
    result['events_without_summary'] = cache_data.get('events_without_summary', [])

    events_with_summaries = cache_data['events_with_summaries']
    if not events_with_summaries:
        result['error'] = "No events have 'Summarized:' text in their message body"
        return result

    # Build TTS script
    logger.info("Step 4: Building TTS script...")
    script = build_tts_script(week, events_with_summaries)
    result['script_length'] = len(script)
    logger.info(f"Script: {len(script)} characters, {len(script.split())} words")

    # Synthesize audio
    logger.info("Step 5: Synthesizing with Jenny Neural voice...")
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "output" / "Audio"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"Weekly Messages Audio Template - Summarized - Week {week} - Jenny Neural - Vimeo.mp4"

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from windows_media_synthesizer import WindowsMediaSynthesizer

    synth = WindowsMediaSynthesizer()
    success = synth.synthesize_to_mp4(script, str(output_file), voice=voice, rate=rate)

    if success and output_file.exists():
        size_kb = output_file.stat().st_size / 1024
        result['success'] = True
        result['output_file'] = str(output_file)
        result['phase_completed'] = 'full' if bq_available else 'synthesize_from_cache'
        logger.info(f"Success! {output_file.name} ({size_kb:.1f} KB)")
    else:
        result['error'] = "Audio synthesis failed. Are you off VPN? Jenny Neural requires speech.platform.bing.com access."
        logger.error(result['error'])

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Weekly Message Audio from BigQuery")
    parser.add_argument("--week", type=int, default=None, help="Walmart week number")
    parser.add_argument("--fy", type=int, default=None, help="Fiscal year")
    parser.add_argument("--voice", default="Jenny", help="Voice: Jenny, David, Zira (default: Jenny)")
    parser.add_argument("--rate", type=float, default=0.95, help="Speech rate (default: 0.95)")
    parser.add_argument("--phase", choices=["fetch", "synthesize"], default=None,
                        help="fetch=BQ data pull (VPN ON), synthesize=TTS from cache (VPN OFF), omit=auto")
    args = parser.parse_args()

    result = generate_weekly_message_audio(
        week=args.week, fy=args.fy, voice=args.voice, rate=args.rate, phase=args.phase
    )

    print(f"\n{'='*60}")
    print(f"PIPELINE RESULTS")
    print(f"{'='*60}")
    print(f"  Phase:                       {result.get('phase_completed', 'N/A')}")
    print(f"  Success:                     {result['success']}")
    print(f"  Weekly Messages (No Comm):   {result.get('event_count', 0)}")
    print(f"  Review for Publish - No Comm:{result.get('review_no_comm_count', 0)}")
    print(f"  With Summarized text:        {result.get('summarized_count', 0)}")
    print(f"  Script length:               {result.get('script_length', 0)} chars")
    if result.get('output_file'):
        print(f"  Output:                      {Path(result['output_file']).name}")
        print(f"  Size:                        {Path(result['output_file']).stat().st_size / 1024:.1f} KB")
    if result.get('error'):
        print(f"  Error:                       {result['error']}")
    if result.get('events_without_summary'):
        print(f"\n  Events without Summarized text ({len(result['events_without_summary'])}):")
        for e in result['events_without_summary']:
            print(f"    [{e.get('area', '?')}] {e.get('title', '?')}")
    print(f"{'='*60}")
