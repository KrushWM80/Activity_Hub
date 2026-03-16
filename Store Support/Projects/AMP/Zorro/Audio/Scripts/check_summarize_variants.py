#!/usr/bin/env python3
"""Check for 'Summarize:' vs 'Summarized:' variants in cached event bodies"""
import json, re
from pathlib import Path
from html.parser import HTMLParser

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
    def handle_data(self, data):
        self.text_parts.append(data)
    def get_text(self):
        return ' '.join(self.text_parts)

def html_to_text(html_str):
    p = HTMLTextExtractor()
    p.feed(html_str)
    return p.get_text()

cache = json.loads(Path(__file__).parent.joinpath('cache', 'week_4_fy2027.json').read_text())

# Check the events WITHOUT summaries — which patterns exist?
without = cache['events_without_summary']
with_s = cache['events_with_summaries']

print(f"Events WITH 'Summarized:' match: {len(with_s)}")
print(f"Events WITHOUT match: {len(without)}")

# We need the raw bodies — re-fetch won't work offline, but the cache only stored extracted summaries.
# Let's check if any of the "without" events have variants by looking at the raw msg_txt
# The cache doesn't store raw bodies, so let's query BQ for the 24 missing ones.

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json')
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

missing_ids = [e['event_id'] for e in without]
ids_str = ", ".join([f"'{eid}'" for eid in missing_ids])
q = f"""
SELECT event_id, msg_txt
FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
WHERE event_id IN ({ids_str})
"""
rows = list(client.query(q).result())

patterns = [
    ('Summarized:', r'Summarized:\s*(.*)'),
    ('Summarize:', r'Summarize:\s*(.*)'),
    ('Summary:', r'Summary:\s*(.*)'),
    ('Summarized', r'Summarized\s+(.*)'),  # without colon
    ('Summarize', r'Summarize\s+(.*)'),    # without colon
]

print(f"\n=== Scanning {len(rows)} message bodies for variants ===\n")
found_count = 0
for r in rows:
    msg = r.msg_txt
    if msg and isinstance(msg, dict):
        arr = msg.get('array', [])
        raw_html = arr[0] if arr else ''
    elif msg:
        raw_html = str(msg)
    else:
        continue
    
    text = html_to_text(raw_html)
    title = next((e['title'] for e in without if e['event_id'] == r.event_id), r.event_id)
    
    matched = False
    for pat_name, pat_re in patterns:
        m = re.search(pat_re, text, re.DOTALL | re.IGNORECASE)
        if m:
            preview = m.group(1).strip()[:100]
            print(f"  FOUND '{pat_name}' in: {title}")
            print(f"    Preview: {preview}...")
            found_count += 1
            matched = True
            break
    
    if not matched:
        # Show last 200 chars to see what's at the bottom
        tail = text[-200:].strip() if len(text) > 200 else text.strip()
        print(f"  NO MATCH: {title}")
        print(f"    Tail: ...{tail[-120:]}")

print(f"\n=== Found {found_count} additional matches out of {len(rows)} ===")
