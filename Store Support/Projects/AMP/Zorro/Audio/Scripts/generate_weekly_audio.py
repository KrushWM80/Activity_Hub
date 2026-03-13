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

# Area groupings for the TTS script template
AREA_GROUPS = {
    "Food & Consumables Merchant Messages": [
        "Consumables", "Food", "Fresh"
    ],
    "General Merchandise Merchant Messages": [
        "Entertainment", "Fashion", "Hardlines", "Home", "Seasonal"
    ],
    "Operations Messages": [
        "Asset Protection", "Auto Care", "Backroom and Claims",
        "Frontend", "Digital", "People", "Total Store"
    ],
}

# Reverse lookup: Store_Area → group name
AREA_TO_GROUP = {}
for group, areas in AREA_GROUPS.items():
    for area in areas:
        AREA_TO_GROUP[area] = group


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
    """Extract text after 'Summarized:' marker from message body."""
    match = re.search(r'Summarized:\s*(.*)', raw_text, re.DOTALL | re.IGNORECASE)
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
    """Query AMP ALL 2 for the week's events with No Comms status."""
    query = """
    SELECT DISTINCT event_id, Store_Area, Title, Headline, Dept, Message_Type, Status
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = @fy AND WM_Week = @week
      AND Status LIKE '%No Comm%'
    ORDER BY Store_Area, Title
    """
    from google.cloud.bigquery import ScalarQueryParameter, QueryJobConfig
    job_config = QueryJobConfig(query_parameters=[
        ScalarQueryParameter("fy", "INT64", fy),
        ScalarQueryParameter("week", "STRING", str(week)),
    ])
    rows = list(client.query(query, job_config=job_config).result())
    logger.info(f"Found {len(rows)} events for FY{fy} Week {week}")
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
    """Build the TTS-friendly script from area-grouped summarized events."""
    # Group events by area group
    grouped = {}
    for group_name in AREA_GROUPS:
        grouped[group_name] = []

    ungrouped = []
    for event in events_with_summaries:
        area = event['store_area']
        group = AREA_TO_GROUP.get(area)
        if group:
            grouped[group].append(event)
        else:
            ungrouped.append(event)

    # Build script
    lines = []
    lines.append(f"Hello! Your Week {week} Weekly Messages are Here!")
    lines.append("")
    lines.append("Please Visit the Landing Page to access full content.")

    for group_name, events in grouped.items():
        if not events:
            continue
        lines.append("")
        lines.append(f"{group_name}:")
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
            lines.append(f"{evt['store_area']}: {evt['summary_text']}")
            lines.append("")

    lines.append(f"That's your Week {week} Weekly Messages, Have a Great Week!")

    return "\n".join(lines)


def generate_weekly_message_audio(week=None, fy=None, voice="Jenny", rate=0.95, output_dir=None):
    """
    Full pipeline: BigQuery → Summarized text extraction → TTS script → Jenny Neural MP4.
    
    Returns dict with keys: success, output_file, event_count, summarized_count, script_length, error
    """
    result = {
        'success': False,
        'output_file': None,
        'event_count': 0,
        'summarized_count': 0,
        'script_length': 0,
        'error': None,
        'events_without_summary': [],
    }

    try:
        from google.cloud import bigquery
        client = bigquery.Client(project='wmt-assetprotection-prod')
    except Exception as e:
        result['error'] = f"BigQuery connection failed: {e}"
        logger.error(result['error'])
        return result

    # Auto-detect current week if not specified
    if week is None or fy is None:
        try:
            detect_q = """
            SELECT DISTINCT WM_Week, FY
            FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
            WHERE Date = CURRENT_DATE()
            LIMIT 1
            """
            rows = list(client.query(detect_q).result())
            if rows:
                if week is None:
                    week = int(rows[0].WM_Week)
                if fy is None:
                    fy = int(rows[0].FY)
            else:
                result['error'] = "Could not auto-detect current Walmart week"
                return result
        except Exception as e:
            result['error'] = f"Week detection failed: {e}"
            return result

    logger.info(f"=== Weekly Message Audio Pipeline: FY{fy} Week {week} ===")

    # Step 1: Fetch events from AMP ALL 2
    logger.info("Step 1: Fetching events from AMP ALL 2...")
    events = fetch_week_events(client, week, fy)
    result['event_count'] = len(events)
    if not events:
        result['error'] = f"No events found for FY{fy} Week {week}"
        return result

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
            events_without.append({'event_id': eid, 'title': row.Title, 'area': row.Store_Area})
            continue

        raw_text = html_to_text(msg_map[eid])
        summary = extract_summarized_text(raw_text)

        if summary:
            events_with_summaries.append({
                'event_id': eid,
                'store_area': row.Store_Area,
                'title': row.Title,
                'summary_text': summary,
            })
        else:
            events_without.append({'event_id': eid, 'title': row.Title, 'area': row.Store_Area})

    result['summarized_count'] = len(events_with_summaries)
    result['events_without_summary'] = events_without
    logger.info(f"Found {len(events_with_summaries)} events with Summarized text, {len(events_without)} without")

    if not events_with_summaries:
        result['error'] = "No events have 'Summarized:' text in their message body"
        return result

    # Step 4: Build TTS script
    logger.info("Step 4: Building TTS script...")
    script = build_tts_script(week, events_with_summaries)
    result['script_length'] = len(script)
    logger.info(f"Script: {len(script)} characters, {len(script.split())} words")

    # Step 5: Synthesize audio
    logger.info("Step 5: Synthesizing with Jenny Neural voice...")
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "output" / "Audio"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"Weekly Messages Audio Template - Summarized - Week {week} - Jenny Neural - Vimeo.mp4"

    # Import synthesizer
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from windows_media_synthesizer import WindowsMediaSynthesizer

    synth = WindowsMediaSynthesizer()
    success = synth.synthesize_to_mp4(script, str(output_file), voice=voice, rate=rate)

    if success and output_file.exists():
        size_kb = output_file.stat().st_size / 1024
        result['success'] = True
        result['output_file'] = str(output_file)
        logger.info(f"Success! {output_file.name} ({size_kb:.1f} KB)")
    else:
        result['error'] = "Audio synthesis failed. Are you off VPN? Jenny Neural requires speech.platform.bing.com access."
        logger.error(result['error'])

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Weekly Message Audio from BigQuery")
    parser.add_argument("--week", type=int, default=None, help="Walmart week number (auto-detect if omitted)")
    parser.add_argument("--fy", type=int, default=None, help="Fiscal year (auto-detect if omitted)")
    parser.add_argument("--voice", default="Jenny", help="Voice: Jenny, David, Zira (default: Jenny)")
    parser.add_argument("--rate", type=float, default=0.95, help="Speech rate (default: 0.95)")
    args = parser.parse_args()

    result = generate_weekly_message_audio(week=args.week, fy=args.fy, voice=args.voice, rate=args.rate)

    print(f"\n{'='*60}")
    print(f"PIPELINE RESULTS")
    print(f"{'='*60}")
    print(f"  Success:            {result['success']}")
    print(f"  Events found:       {result['event_count']}")
    print(f"  With Summarized:    {result['summarized_count']}")
    print(f"  Script length:      {result['script_length']} chars")
    if result['output_file']:
        print(f"  Output:             {Path(result['output_file']).name}")
        print(f"  Size:               {Path(result['output_file']).stat().st_size / 1024:.1f} KB")
    if result['error']:
        print(f"  Error:              {result['error']}")
    if result['events_without_summary']:
        print(f"\n  Events without Summarized text ({len(result['events_without_summary'])}):")
        for e in result['events_without_summary']:
            print(f"    [{e['area']}] {e['title']}")
    print(f"{'='*60}")
