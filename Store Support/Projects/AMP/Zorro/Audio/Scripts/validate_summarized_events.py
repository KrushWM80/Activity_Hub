#!/usr/bin/env python3
"""Find Week 4 'Review for Publish - No Comm' events with 'Summarized:' in msg body"""
import os, re
from html.parser import HTMLParser
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

class HTMLTextExtractor(HTMLParser):
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

# Step 0: Check what Message_Type and Status values exist for Week 4
print("=== All Message_Type values for WK 4 ===")
q0 = """
SELECT DISTINCT Message_Type, COUNT(DISTINCT event_id) as event_cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4'
GROUP BY Message_Type
ORDER BY event_cnt DESC
"""
for r in client.query(q0).result():
    print(f"  {r.Message_Type}: {r.event_cnt} events")

print("\n=== All Status values for WK 4 ===")
q0b = """
SELECT DISTINCT Status, COUNT(DISTINCT event_id) as event_cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4'
GROUP BY Status
ORDER BY event_cnt DESC
"""
for r in client.query(q0b).result():
    print(f"  {r.Status}: {r.event_cnt} events")

# Step 1: Get all Week 4 events - try Status filter for 'Review for Publish - No Comm'
print("\n=== Querying AMP ALL 2: WK 4, Status = 'Review for Publish - No Comm' ===")
q1 = """
SELECT DISTINCT event_id, Store_Area, Title, Headline, Dept, Message_Type, Status
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4'
  AND Status LIKE '%No Comm%'
ORDER BY Store_Area, Title
"""
amp_rows = list(client.query(q1).result())
event_ids = [r.event_id for r in amp_rows]
print(f"Total distinct events found: {len(event_ids)}")

# Show all events
print("\n=== All Events Found ===")
for i, r in enumerate(amp_rows, 1):
    print(f"  {i}. [{r.Store_Area}] {r.Title}")
    print(f"     Message_Type: {r.Message_Type} | Status: {r.Status}")

# Step 2: Cross-reference with raw Cosmos table for msg_txt
print(f"\n=== Querying raw Cosmos for msg_txt ({len(event_ids)} event_ids) ===")
if not event_ids:
    print("No events found — skipping Cosmos query.")
    exit()
ids_str = ", ".join([f"'{eid}'" for eid in event_ids])
q2 = f"""
SELECT event_id, msg_txt
FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
WHERE event_id IN ({ids_str})
"""
raw_rows = list(client.query(q2).result())
print(f"Matching raw rows: {len(raw_rows)}")

# Build event_id -> msg_txt map
msg_map = {}
for r in raw_rows:
    msg = r.msg_txt
    if msg:
        if isinstance(msg, dict):
            arr = msg.get('array', [])
            if arr:
                msg_map[r.event_id] = arr[0]
        else:
            msg_map[r.event_id] = str(msg)

print(f"Events with msg_txt: {len(msg_map)}")

# Step 3: Find which have "Summarized:" in message body
print("\n=== Events WITH 'Summarized:' in message body ===")
summarized_events = []
no_summarized = []

for row in amp_rows:
    eid = row.event_id
    if eid in msg_map:
        html_content = msg_map[eid]
        text = html_to_text(html_content)
        
        if 'summarized' in text.lower():
            summarized_events.append(row)
            # Extract the summarized section
            match = re.search(r'[Ss]ummarized[:\s]*(.*?)(?:\n\n|\Z)', text, re.DOTALL)
            summary_text = match.group(1).strip()[:300] if match else "FOUND but couldn't extract"
            print(f"\n  [{row.Store_Area}] {row.Title}")
            print(f"    Event ID: {eid}")
            print(f"    Summarized text: {summary_text}")
        else:
            no_summarized.append((row.Store_Area, row.Title, eid))
    else:
        no_summarized.append((row.Store_Area, row.Title, eid))

print(f"\n{'='*60}")
print(f"RESULTS:")
print(f"  Total 'Review for Publish - No Comm' events (WK 4): {len(amp_rows)}")
print(f"  Events WITH 'Summarized:' in body: {len(summarized_events)}")
print(f"  Events WITHOUT 'Summarized:': {len(no_summarized)}")
print(f"{'='*60}")

if no_summarized:
    print(f"\n=== Events WITHOUT 'Summarized:' ===")
    for area, title, eid in no_summarized:
        print(f"  [{area}] {title} ({eid})")
