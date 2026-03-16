#!/usr/bin/env python3
"""Preview the TTS script from cached data without synthesizing"""
import json, sys
from pathlib import Path

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent))
from generate_weekly_audio import build_tts_script, AREA_GROUPS, AREA_DISPLAY_NAME

cache_file = Path(__file__).parent / "cache" / "week_4_fy2027.json"
cache = json.loads(cache_file.read_text())

print(f"Cache: {cache['event_count']} events, {cache['summarized_count']} with summaries")
print(f"Cached at: {cache['cached_at']}")
print()

# Show area breakdown
print("=== AREA BREAKDOWN ===")
for group_name in AREA_GROUPS:
    areas_in_group = AREA_GROUPS[group_name]
    group_events = [e for e in cache['events_with_summaries'] 
                    if e['store_area'] in [bq for bq, _ in areas_in_group]]
    if group_events:
        print(f"\n{group_name} ({len(group_events)} events):")
        for bq_name, display_name in areas_in_group:
            area_evts = [e for e in group_events if e['store_area'] == bq_name]
            if area_evts:
                print(f"  {display_name} Area: {len(area_evts)} events")
                for e in area_evts:
                    print(f"    - {e['title']}")

# Build and show the full script
script = build_tts_script(4, cache['events_with_summaries'])
print(f"\n{'='*70}")
print(f"FULL TTS SCRIPT ({len(script)} chars, {len(script.split())} words)")
print(f"{'='*70}\n")
print(script)
print(f"\n{'='*70}")
print(f"END OF SCRIPT")
print(f"{'='*70}")
