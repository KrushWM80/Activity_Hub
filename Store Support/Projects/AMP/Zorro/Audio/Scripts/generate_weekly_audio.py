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
from dataclasses import dataclass, field
from typing import Optional, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# BigQuery credentials — resolve ADC path robustly for any launch context
# (scheduled tasks, batch files, VS Code terminals, etc.)
def _resolve_adc_path():
    """Find the Application Default Credentials JSON, trying multiple locations."""
    candidates = []
    # 1. Already set by user/environment
    env_val = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
    if env_val and os.path.isfile(env_val):
        return env_val
    # 2. Standard APPDATA location
    appdata = os.environ.get('APPDATA', '')
    if appdata:
        candidates.append(os.path.join(appdata, 'gcloud', 'application_default_credentials.json'))
    # 3. Explicit user profile fallback (covers scheduled tasks where APPDATA is missing)
    userprofile = os.environ.get('USERPROFILE', '')
    if userprofile:
        candidates.append(os.path.join(userprofile, 'AppData', 'Roaming', 'gcloud',
                                       'application_default_credentials.json'))
    # 4. Hardcoded known path as last resort
    candidates.append(r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json')
    for path in candidates:
        if os.path.isfile(path):
            return path
    return candidates[0] if candidates else ''

_adc_path = _resolve_adc_path()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _adc_path
logger.info(f"ADC credentials: {_adc_path} (exists: {os.path.isfile(_adc_path)})")

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

# AMP message URL pattern
AMP_MSG_URL = "https://amp2-cms.prod.walmart.com/message/{event_id}/{week}/{fy}"

# ── Segment-based prosody (V2 Enhanced) ─────────────────────────────────────

@dataclass
class Segment:
    """A segment of audio to synthesize or a silence gap."""
    text: Optional[str] = None
    silence_ms: int = 0
    rate: str = "+0%"
    pitch: str = "+0Hz"
    volume: str = "+0%"
    label: str = ""
    tier: str = ""  # prosody tier name for script annotations

# Silence helpers (5 levels)
def _silence(ms, label=""):
    return Segment(silence_ms=ms, label=label)

def _micro():       return _silence(200, "micro")
def _pause():       return _silence(400, "pause")
def _header_pause(): return _silence(300, "header pause")
def _area_break():  return _silence(600, "area break")
def _section_break(label=""): return _silence(800, label or "section break")

# Speech helpers (6 prosody tiers)
def _group_hdr(text):
    return Segment(text=text, rate="-10%", pitch="+1Hz", label=f"GROUP: {text}", tier="group_header")

def _area_hdr(text):
    return Segment(text=text, rate="-5%", pitch="+1Hz", label=f"AREA: {text}", tier="area_header")

def _headline(text, label=""):
    return Segment(text=text, rate="-4%", pitch="+1Hz", label=f"HL: {label or text}", tier="headline")

def _body(text, label=""):
    return Segment(text=text, rate="+0%", label=label or text[:40], tier="body")

def _warm(text, label="", rate="-5%", pitch="+2Hz"):
    return Segment(text=text, rate=rate, pitch=pitch, label=label or text[:40], tier="intro_outro")

# Tier annotation labels for the script file
TIER_ANNOTATIONS = {
    "group_header": "[SLOW, LIFTED]",
    "area_header":  "[MODERATE, LIFTED]",
    "headline":     "[SLIGHTLY SLOW, LIFTED]",
    "body":         "[NORMAL PACE]",
    "intro_outro":  "[WARM, PERSONAL]",
}


class HTMLTextExtractor(HTMLParser):
    """Extract plain text from HTML, preserving paragraph breaks for block elements."""
    BLOCK_TAGS = {'p', 'div', 'br', 'li', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'}

    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.BLOCK_TAGS:
            self.text_parts.append('\n')

    def handle_endtag(self, tag):
        if tag.lower() in self.BLOCK_TAGS:
            self.text_parts.append('\n')

    def handle_data(self, data):
        self.text_parts.append(data)

    def get_text(self):
        return ''.join(self.text_parts)


def html_to_text(html_str):
    parser = HTMLTextExtractor()
    parser.feed(html_str)
    return parser.get_text()


def extract_summarized_text(raw_text):
    """Extract text after summary marker from message body.
    
    Handles all known variants (authors frequently misspell):
      - 'Summarized: text'   (correct spelling)
      - 'Summarize: text'    (no d)
      - 'Summarized : text'  (space before colon)
      - 'Summarized  text'   (no colon at all)
      - 'Summerized: text'   (common misspelling — mm + e)
      - 'Summarzied: text'   (transposed letters)
      - 'Sumarized: text'    (single m)
      - Other creative misspellings of "Summarize/d"
    """
    # Pattern 1: Flexible match for common misspellings of Summarize/d + optional colon
    # Covers: Summarized, Summarize, Summerized, Summarzied, Sumarized, etc.
    match = re.search(r'Sum+[aeiou]r+[a-z]*z[a-z]*e?d?\s*:\s*(.*)', raw_text, re.DOTALL | re.IGNORECASE)
    if not match:
        # Pattern 2: Same flexible prefix but no colon, just whitespace then content
        match = re.search(r'Sum+[aeiou]r+[a-z]*z[a-z]*e?d?\s+(.*)', raw_text, re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    text = match.group(1).strip()
    # Clean up CSS artifacts
    text = re.sub(r'::marker\s*\{[^}]*\}', '', text)
    # Normalize line endings
    text = text.replace('\r\n', '\n')
    # Ensure paragraph breaks before sub-topic headers (Dept. XX:)
    text = re.sub(r'\n+\s*(Dept\.)', r'\n\n\1', text)
    # Normalize remaining runs of 2+ newlines to exactly 2
    text = re.sub(r'\n{2,}', '\n\n', text)
    # Within each paragraph, collapse whitespace to single spaces
    paragraphs = [re.sub(r'[ \t]+', ' ', p).strip() for p in text.split('\n\n')]
    paragraphs = [p for p in paragraphs if p]  # remove empties
    # Within each paragraph, preserve single newlines (title + body on separate lines)
    paragraphs = [re.sub(r'\n', '\n\n', p) if '\n' in p else p for p in paragraphs]
    text = '\n\n'.join(paragraphs)
    # Truncate at reasonable length for TTS
    if len(text) > 2000:
        # Try to cut at a sentence boundary
        cut = text[:2000].rfind('. ')
        if cut > 400:
            text = text[:cut + 1]
        else:
            text = text[:2000] + '...'
    return text


def fetch_week_events(client, week, fy):
    """Query AMP ALL 2 for Merchant Messages in Review for Publish - No Comms status."""
    query = """
    SELECT DISTINCT event_id, Store_Area, Title, Headline, Dept, Message_Type, Status
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = @fy AND WM_Week = @week
      AND Message_Type = 'Merchant Message'
      AND Status = 'Review for Publish review - No Comms'
      AND Business_Area != 'AMP PR Merchandise'
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
                # Preserve paragraph breaks as separate lines for natural TTS pacing
                for sub in evt['summary_text'].split('\n\n'):
                    sub = sub.strip()
                    if sub:
                        lines.append(sub)
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


def build_tts_segments(week, events_with_summaries) -> List[Segment]:
    """Build prosody-tagged segments from area-grouped summarized events.
    
    Returns a list of Segment objects with per-segment rate/pitch/silence for
    segment-based synthesis (V2 Enhanced prosody).
    """
    # Group events (same logic as build_tts_script)
    grouped = {}
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

    segments = []

    # Intro
    segments.append(_warm(f"Hello! Your Week {week} Weekly Messages are Here!", "Greeting"))
    segments.append(_pause())
    segments.append(Segment(
        text="Please visit the Landing Page to access full content.",
        rate="-3%", label="Intro instruction", tier="intro_outro"
    ))
    segments.append(_section_break("intro break"))

    first_group = True
    for group_name in AREA_GROUPS:
        area_events = grouped[group_name]
        if not any(area_events.values()):
            continue

        if not first_group:
            segments.append(_section_break(f"→ {group_name}"))
        first_group = False

        segments.append(_group_hdr(f"{group_name}."))
        segments.append(_pause())

        first_area = True
        for bq_name, display_name in AREA_GROUPS[group_name]:
            events = area_events.get(bq_name, [])
            if not events:
                continue

            if not first_area:
                segments.append(_area_break())
            first_area = False

            segments.append(_area_hdr(f"{display_name} Area."))
            segments.append(_header_pause())

            for i, evt in enumerate(events):
                title = evt.get('title', '')
                summary = evt['summary_text']

                # Split multi-topic summaries (separated by double newlines) into separate segments
                sub_topics = [s.strip() for s in summary.split('\n\n') if s.strip()]
                for j, sub in enumerate(sub_topics):
                    segments.append(_body(sub, title or sub[:40]))
                    if j < len(sub_topics) - 1:
                        segments.append(_pause())  # pause between sub-topics

                if i < len(events) - 1:
                    segments.append(_pause())

    # Ungrouped
    if ungrouped:
        segments.append(_section_break("additional"))
        segments.append(_group_hdr("Additional Messages."))
        segments.append(_pause())
        for evt in ungrouped:
            display = AREA_DISPLAY_NAME.get(evt['store_area'], evt['store_area'])
            segments.append(_body(evt['summary_text'], display))
            segments.append(_pause())

    # Outro
    segments.append(_section_break("outro"))
    segments.append(_warm(f"That's your Week {week} Weekly Messages.", "Outro", rate="-5%", pitch="+1Hz"))
    segments.append(_pause())
    segments.append(_warm("Have a Great Week!", "Sign-off", rate="-8%", pitch="+2Hz"))

    return segments


def build_annotated_script(segments: List[Segment]) -> str:
    """Build a human-readable script with inflection/prosody annotations.
    
    Example output:
        [WARM, PERSONAL] Hello! Your Week 9 Weekly Messages are Here!
        --- 400ms pause ---
        [SLOW, LIFTED] Food & Consumables Merchant Messages.
    """
    lines = []
    for seg in segments:
        if seg.silence_ms > 0:
            lines.append(f"  --- {seg.silence_ms}ms {seg.label or 'silence'} ---")
            lines.append("")
        elif seg.text:
            annotation = TIER_ANNOTATIONS.get(seg.tier, "")
            if annotation:
                lines.append(f"{annotation} {seg.text}")
            else:
                lines.append(seg.text)
            lines.append("")
    return "\n".join(lines).strip()


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
    # Pre-flight: verify credentials exist before attempting BQ connection
    cred_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
    if not cred_file or not os.path.isfile(cred_file):
        return {
            'error': (
                f"BQ credentials file not found at: {cred_file or '(not set)'}. "
                f"Run 'gcloud auth application-default login' on Eagle WiFi to fix."
            )
        }

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

    # Full status breakdown for all Merchant Messages (excl. AMP PR Merchandise)
    logger.info("Fetching full status breakdown (excl. AMP PR Merchandise)...")
    from google.cloud.bigquery import ScalarQueryParameter, QueryJobConfig as _QJC
    status_query = """
    SELECT Status, COUNT(DISTINCT event_id) as cnt
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = @fy AND WM_Week = @week
      AND Message_Type = 'Merchant Message'
      AND Business_Area != 'AMP PR Merchandise'
    GROUP BY Status
    ORDER BY cnt DESC
    """
    status_config = _QJC(query_parameters=[
        ScalarQueryParameter("fy", "INT64", fy),
        ScalarQueryParameter("week", "STRING", str(week)),
    ])
    status_breakdown = []
    total_all = 0
    total_excl_denied = 0
    try:
        for row in client.query(status_query, job_config=status_config).result():
            status_breakdown.append({'status': row.Status, 'count': row.cnt})
            total_all += row.cnt
            if 'Denied' not in (row.Status or ''):
                total_excl_denied += row.cnt
    except Exception as e:
        logger.warning(f"Could not fetch status breakdown: {e}")

    logger.info(f"Status breakdown: {len(status_breakdown)} statuses, total (excl. Denied): {total_excl_denied}")

    cache_data = {
        'week': week,
        'fy': fy,
        'cached_at': datetime.now().isoformat(),
        'event_count': len(events),
        'review_no_comm_count': review_no_comm,
        'status_breakdown': status_breakdown,
        'total_excl_denied': total_excl_denied,
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
    Phase 2: Build segment-based TTS script from cached data and synthesize MP4.
    Uses V2 Enhanced prosody (per-segment rate/pitch) for natural speech.
    Requires OFF VPN (edge-tts needs speech.platform.bing.com).
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

    # Build V2 Enhanced segments for annotated script display
    logger.info("Building V2 Enhanced segments for annotated script...")
    segments = build_tts_segments(week, events_with_summaries)
    annotated_script = build_annotated_script(segments)
    # Plain script for actual TTS synthesis (proven single-pass method)
    plain_script = build_tts_script(week, events_with_summaries)

    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "output" / "Audio"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"Weekly Messages Audio Template - Summarized - Week {week} - Jenny Neural - Vimeo.mp4"

    # Save both standard and annotated scripts
    script_file = output_dir / f"Week {week} - Weekly Messages Audio Script.txt"
    with open(script_file, 'w', encoding='utf-8') as sf:
        sf.write(plain_script)
    logger.info(f"Saved standard TTS script to {script_file.name}")

    inflection_file = output_dir / f"Week {week} - Weekly Messages Audio Script (Inflection).txt"
    with open(inflection_file, 'w', encoding='utf-8') as sf:
        sf.write(annotated_script)
    logger.info(f"Saved inflection script to {inflection_file.name}")

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from windows_media_synthesizer import WindowsMediaSynthesizer

    synth = WindowsMediaSynthesizer()

    # Single-pass synthesis: one edge-tts call with entire script (fast & reliable)
    logger.info("Synthesizing with Jenny Neural voice (single-pass)...")
    success = synth.synthesize_to_mp4(plain_script, str(output_file), voice=voice, rate=rate)

    if success and output_file.exists():
        size_kb = output_file.stat().st_size / 1024

        # Get audio duration via ffprobe
        duration = 0
        try:
            import subprocess as _sp
            ffprobe = str(synth.ffmpeg_path).replace("ffmpeg.exe", "ffprobe.exe")
            pr = _sp.run(
                [ffprobe, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(output_file)],
                capture_output=True, text=True, timeout=10
            )
            if pr.returncode == 0:
                duration = float(pr.stdout.strip())
        except Exception:
            pass

        logger.info(f"Success! {output_file.name} ({size_kb:.1f} KB, {duration:.1f}s)")

        result = {
            'success': True,
            'output_file': str(output_file),
            'script_file': str(script_file),
            'event_count': cache_data['event_count'],
            'review_no_comm_count': cache_data.get('review_no_comm_count', 0),
            'summarized_count': cache_data['summarized_count'],
            'script_length': len(annotated_script),
            'events_without_summary': cache_data.get('events_without_summary', []),
            'duration_seconds': duration,
            'week': week,
            'fy': fy,
        }

        # Generate email report
        _generate_email_report(result, output_dir, week, fy, annotated_script, cache_data)

        return result
    else:
        return {
            'success': False,
            'error': 'Audio synthesis failed. Are you off VPN? Jenny Neural requires speech.platform.bing.com access.',
            'event_count': cache_data['event_count'],
            'review_no_comm_count': cache_data.get('review_no_comm_count', 0),
            'summarized_count': cache_data['summarized_count'],
            'script_length': len(annotated_script),
        }


def _generate_email_report(result, output_dir, week, fy, annotated_script, cache_data):
    """Generate an HTML email report after successful audio synthesis.
    
    Includes: MP4 file info, script, CMS URL, audio length, event counts,
    and events missing summaries with their AMP message URLs.
    """
    output_dir = Path(output_dir)
    mp4_name = Path(result.get('output_file', '')).name if result.get('output_file') else 'N/A'
    script_name = f"Week {week} - Weekly Messages Audio Script.txt"
    inflection_name = f"Week {week} - Weekly Messages Audio Script (Inflection).txt"
    mp4_size = 'N/A'
    if result.get('output_file') and Path(result['output_file']).exists():
        mp4_size = f"{Path(result['output_file']).stat().st_size / 1024:.1f} KB"

    duration_s = result.get('duration_seconds', 0)
    if duration_s:
        mins = int(duration_s // 60)
        secs = int(duration_s % 60)
        duration_str = f"{mins}m {secs}s" if mins else f"{secs}s"
    else:
        duration_str = "N/A"

    year = fy - 1  # Walmart FY2027 covers calendar year 2026
    cms_url = f"https://enablement.walmart.com/content/store-communications/home/merchandise/weekly-messages/{year}/week-{week}/weekly_messages_audiowk{week}.html"

    event_count = cache_data.get('event_count', result.get('event_count', 0))
    summarized_count = cache_data.get('summarized_count', result.get('summarized_count', 0))
    events_without = cache_data.get('events_without_summary', result.get('events_without_summary', []))

    # Build missing summary rows
    missing_rows = ""
    for evt in events_without:
        eid = evt.get('event_id', '')
        title = evt.get('title', 'Unknown')
        area = evt.get('area', 'Unknown')
        msg_url = AMP_MSG_URL.format(event_id=eid, week=week, fy=fy)
        missing_rows += f"""
            <tr>
                <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">{area}</td>
                <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">{title}</td>
                <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">
                    <a href="{msg_url}" style="color:#2563EB;">{msg_url}</a>
                </td>
            </tr>"""

    missing_section = ""
    if events_without:
        missing_section = f"""
        <div style="margin-top:24px;">
            <h3 style="color:#DC2626;font-size:15px;margin-bottom:8px;">
                Events Without Summary ({len(events_without)})
            </h3>
            <p style="font-size:13px;color:#6B7280;margin-bottom:8px;">
                These events did not have a "Summarized:" marker in their message body 
                and were excluded from the audio.
            </p>
            <table style="width:100%;border-collapse:collapse;font-size:13px;">
                <thead>
                    <tr style="background:#FEE2E2;">
                        <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #FECACA;">Area</th>
                        <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #FECACA;">Title</th>
                        <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #FECACA;">Message URL</th>
                    </tr>
                </thead>
                <tbody>{missing_rows}
                </tbody>
            </table>
        </div>"""

    # Escape script for HTML
    import html as html_mod
    escaped_script = html_mod.escape(annotated_script)

    generated_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    email_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Messages Audio Report - Week {week} FY{fy}</title>
</head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#F3F4F6;">
    <div style="max-width:700px;margin:20px auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
        
        <!-- Header -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td align="center" style="padding:28px 32px;border-bottom:4px solid #1D4ED8;background-color:#EFF6FF;">
                    <h1 style="font-size:22px;font-weight:700;margin:0;color:#1E3A8A;">Weekly Messages Audio Report</h1>
                    <p style="font-size:14px;margin:6px 0 0;color:#4B5563;">Week {week} &#8226; FY{fy} &#8226; {generated_at}</p>
                </td>
            </tr>
        </table>

        <!-- Summary Stats -->
        <div style="padding:24px 32px;">
            <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">
                <div style="flex:1;min-width:140px;background:#EFF6FF;border-radius:8px;padding:14px;text-align:center;">
                    <div style="font-size:24px;font-weight:700;color:#1D4ED8;">{event_count}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">Weekly Messages</div>
                </div>
                <div style="flex:1;min-width:140px;background:#ECFDF5;border-radius:8px;padding:14px;text-align:center;">
                    <div style="font-size:24px;font-weight:700;color:#059669;">{summarized_count}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">With Summaries</div>
                </div>
                <div style="flex:1;min-width:140px;background:{('#FEF2F2' if events_without else '#F0FDF4')};border-radius:8px;padding:14px;text-align:center;">
                    <div style="font-size:24px;font-weight:700;color:{('#DC2626' if events_without else '#16A34A')};">{len(events_without)}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">Missing Summary</div>
                </div>
                <div style="flex:1;min-width:140px;background:#F5F3FF;border-radius:8px;padding:14px;text-align:center;">
                    <div style="font-size:24px;font-weight:700;color:#7C3AED;">{duration_str}</div>
                    <div style="font-size:12px;color:#6B7280;margin-top:2px;">Audio Length</div>
                </div>
            </div>

            <!-- File Details -->
            <h3 style="font-size:15px;color:#111827;margin-bottom:10px;">Deliverables</h3>
            <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:16px;">
                <tr style="background:#F9FAFB;">
                    <td style="padding:8px 12px;font-weight:600;width:120px;border-bottom:1px solid #E5E7EB;">MP4 File</td>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">{mp4_name} ({mp4_size})</td>
                </tr>
                <tr>
                    <td style="padding:8px 12px;font-weight:600;border-bottom:1px solid #E5E7EB;">Standard Script</td>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">📄 {script_name}</td>
                </tr>
                <tr style="background:#F9FAFB;">
                    <td style="padding:8px 12px;font-weight:600;border-bottom:1px solid #E5E7EB;">Inflection Script</td>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">🎭 {inflection_name}</td>
                </tr>
                <tr>
                    <td style="padding:8px 12px;font-weight:600;border-bottom:1px solid #E5E7EB;">CMS URL</td>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">
                        <a href="{cms_url}" style="color:#2563EB;word-break:break-all;">{cms_url}</a>
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 12px;font-weight:600;border-bottom:1px solid #E5E7EB;">Voice</td>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">Jenny Neural (en-US) &bull; V2 Enhanced Prosody</td>
                </tr>
                <tr style="background:#F9FAFB;">
                    <td style="padding:8px 12px;font-weight:600;border-bottom:1px solid #E5E7EB;">Codec</td>
                    <td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;">AAC @ 256kbps + libx264 thumbnail</td>
                </tr>
            </table>

            {missing_section}

            <!-- Script Preview -->
            <div style="margin-top:24px;">
                <h3 style="font-size:15px;color:#111827;margin-bottom:8px;">TTS Script (Enhanced with Inflection Markings)</h3>
                <pre style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;padding:16px;font-size:12px;line-height:1.6;max-height:400px;overflow-y:auto;white-space:pre-wrap;word-wrap:break-word;">{escaped_script}</pre>
            </div>
        </div>

        <!-- Footer -->
        <div style="background:#F9FAFB;padding:16px 32px;text-align:center;border-top:1px solid #E5E7EB;">
            <p style="font-size:12px;color:#9CA3AF;margin:0;">
                🎙️ Narrated by Jenny Neural Voice &bull; Powered by Zorro Activity Hub &bull; Generated {generated_at}
            </p>
        </div>
    </div>
</body>
</html>"""

    # Save email report
    email_file = output_dir / f"Week {week} - Weekly Messages Audio Report.html"
    with open(email_file, 'w', encoding='utf-8') as ef:
        ef.write(email_html)
    logger.info(f"Email report saved to {email_file.name}")

    # Also store the email path in the result
    result['email_report'] = str(email_file)
    return email_file


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
            result['status_breakdown'] = cache_data.get('status_breakdown', [])
            result['total_excl_denied'] = cache_data.get('total_excl_denied', 0)
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

    # Build V2 Enhanced segments with prosody
    logger.info("Step 4: Building V2 Enhanced segments with prosody...")
    segments = build_tts_segments(week, events_with_summaries)
    annotated_script = build_annotated_script(segments)
    plain_script = build_tts_script(week, events_with_summaries)
    result['script_length'] = len(annotated_script)
    speech_segs = [s for s in segments if s.text]
    logger.info(f"Segments: {len(speech_segs)} speech, script: {len(annotated_script)} chars")

    # Synthesize audio
    logger.info("Step 5: Synthesizing with Jenny Neural voice (single-pass)...")
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "output" / "Audio"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"Weekly Messages Audio Template - Summarized - Week {week} - Jenny Neural - Vimeo.mp4"

    # Save both standard and annotated scripts
    script_file = output_dir / f"Week {week} - Weekly Messages Audio Script.txt"
    with open(script_file, 'w', encoding='utf-8') as sf:
        sf.write(plain_script)
    logger.info(f"Saved standard TTS script to {script_file.name}")

    inflection_file = output_dir / f"Week {week} - Weekly Messages Audio Script (Inflection).txt"
    with open(inflection_file, 'w', encoding='utf-8') as sf:
        sf.write(annotated_script)
    logger.info(f"Saved inflection script to {inflection_file.name}")

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from windows_media_synthesizer import WindowsMediaSynthesizer

    synth = WindowsMediaSynthesizer()
    success = synth.synthesize_to_mp4(plain_script, str(output_file), voice=voice, rate=rate)

    if success and output_file.exists():
        size_kb = output_file.stat().st_size / 1024

        # Get audio duration via ffprobe
        duration = 0
        try:
            import subprocess as _sp
            ffprobe = str(synth.ffmpeg_path).replace("ffmpeg.exe", "ffprobe.exe")
            pr = _sp.run(
                [ffprobe, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(output_file)],
                capture_output=True, text=True, timeout=10
            )
            if pr.returncode == 0:
                duration = float(pr.stdout.strip())
        except Exception:
            pass

        result['success'] = True
        result['output_file'] = str(output_file)
        result['script_file'] = str(script_file)
        result['phase_completed'] = 'full' if bq_available else 'synthesize_from_cache'
        result['duration_seconds'] = duration
        result['week'] = week
        result['fy'] = fy
        logger.info(f"Success! {output_file.name} ({size_kb:.1f} KB, {duration:.1f}s)")

        # Generate email report
        _generate_email_report(result, output_dir, week, fy, annotated_script, cache_data)
    else:
        result['error'] = "Audio synthesis failed. Are you off VPN? Jenny Neural requires speech.platform.bing.com access."
        logger.error(result['error'])

    return result


def send_audio_report_email(week, fy, to_recipients=None):
    """Send the Weekly Messages Audio Report via Outlook COM (pywin32).
    
    Attaches the MP4 file and TTS script. Uses the existing HTML report as the
    email body. Requires Outlook to be running on the local machine.
    
    Args:
        week: Walmart week number
        fy: Fiscal year
        to_recipients: List of email addresses (default: kendall.rush@walmart.com)
    
    Returns:
        dict with success, error, and message fields
    """
    if to_recipients is None:
        to_recipients = ['kendall.rush@walmart.com']

    output_dir = Path(__file__).parent.parent.parent / "output" / "Audio"

    # Locate the report, MP4, and script files
    report_file = output_dir / f"Week {week} - Weekly Messages Audio Report.html"
    mp4_file = output_dir / f"Weekly Messages Audio Template - Summarized - Week {week} - Jenny Neural - Vimeo.mp4"
    script_file = output_dir / f"Week {week} - Weekly Messages Audio Script.txt"
    inflection_file = output_dir / f"Week {week} - Weekly Messages Audio Script (Inflection).txt"

    if not report_file.exists():
        return {'success': False, 'error': f'Report not found: {report_file.name}. Run synthesis first.'}

    # Read the HTML report as email body
    html_body = report_file.read_text(encoding='utf-8')

    # Collect valid attachments
    attachments = []
    for f in [mp4_file, script_file, inflection_file]:
        if f.exists():
            attachments.append(str(f.absolute()))
        else:
            logger.warning(f"Attachment not found, skipping: {f.name}")

    # CMS URL for reference
    year = fy - 1  # Walmart FY2027 covers calendar year 2026
    cms_url = f"https://enablement.walmart.com/content/store-communications/home/merchandise/weekly-messages/{year}/week-{week}/weekly_messages_audiowk{week}.html"

    try:
        import pythoncom
        import time
        pythoncom.CoInitialize()
        import win32com.client

        # Retry loop — Outlook may reject COM calls if busy (RPC_E_CALL_REJECTED)
        max_retries = 4
        for attempt in range(max_retries):
            try:
                outlook = win32com.client.Dispatch('Outlook.Application')
                mail = outlook.CreateItem(0)  # olMailItem
                mail.To = '; '.join(to_recipients)
                mail.Subject = f"Weekly Messages Audio Report - Week {week} FY{fy}"
                mail.HTMLBody = html_body

                for att in attachments:
                    mail.Attachments.Add(att)
                    logger.info(f"Attached: {Path(att).name}")

                mail.Send()
                logger.info(f"Email sent to {', '.join(to_recipients)}")
                return {
                    'success': True,
                    'message': f'Email sent to {", ".join(to_recipients)}',
                    'attachments': [Path(a).name for a in attachments],
                }
            except pythoncom.com_error as ce:
                # -2147418111 (0x80010001) = RPC_E_CALL_REJECTED (Outlook busy)
                if ce.args[0] == -2147418111 and attempt < max_retries - 1:
                    wait = 2 * (attempt + 1)
                    logger.warning(f"Outlook busy, retrying in {wait}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait)
                else:
                    raise
    except ImportError:
        return {'success': False, 'error': 'pywin32 not installed. Run: pip install pywin32'}
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass


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
