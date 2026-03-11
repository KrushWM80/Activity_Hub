#!/usr/bin/env python3
"""Find events with 'Summarized:' text in message body"""
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

# Step 1: Get all Week 4 event_ids from AMP ALL 2
print("=== Getting ALL Week 4 Store Updates event_ids ===")
q1 = """
SELECT DISTINCT event_id, Store_Area, Title, Headline, Dept
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4'
  AND Status LIKE '%Published%'
  AND Message_Type LIKE '%Store Updates%'
ORDER BY Store_Area, Title
"""
amp_rows = list(client.query(q1).result())
event_ids = [r.event_id for r in amp_rows]
print(f"Found {len(event_ids)} distinct events")

# Step 2: Batch query raw table for msg_txt of these events
print("\n=== Querying raw Cosmos for msg_txt ===")
ids_str = ", ".join([f"'{eid}'" for eid in event_ids])
q2 = f"""
SELECT event_id, msg_txt
FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
WHERE event_id IN ({ids_str})
"""
raw_rows = list(client.query(q2).result())
print(f"Found {len(raw_rows)} matching raw rows")

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

# Step 3: Search for "Summarized" in message text
print("\n=== Events with 'Summarized' in message body ===")
summarized_count = 0
no_summarized = []

for row in amp_rows:
    eid = row.event_id
    if eid in msg_map:
        html_content = msg_map[eid]
        text = html_to_text(html_content)
        
        # Case-insensitive search
        if 'summarized' in text.lower():
            summarized_count += 1
            # Extract the summarized section
            match = re.search(r'[Ss]ummarized[:\s]*(.*?)(?:\n\n|$)', text, re.DOTALL)
            summary_text = match.group(1)[:200] if match else "FOUND but couldn't extract"
            print(f"\n  [{row.Store_Area}] {row.Title}")
            print(f"    Event: {eid}")
            print(f"    Summary: {summary_text}")
        else:
            no_summarized.append((row.Store_Area, row.Title, eid))
    else:
        no_summarized.append((row.Store_Area, row.Title, eid))

print(f"\n=== TOTALS ===")
print(f"With 'Summarized:': {summarized_count}")
print(f"Without: {len(no_summarized)}")

# Show the first 5 msg_txt samples even without "Summarized" to understand content
print("\n=== Sample message body text (first 3 without Summarized) ===")
for area, title, eid in no_summarized[:3]:
    if eid in msg_map:
        text = html_to_text(msg_map[eid])
        print(f"\n  [{area}] {title}")
        print(f"    Text preview: {text[:300]}")
