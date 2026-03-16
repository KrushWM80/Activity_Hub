#!/usr/bin/env python3
"""Check the one remaining unmatched event"""
import os, json, re
from html.parser import HTMLParser
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json')
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

cache = json.loads(open(os.path.join(os.path.dirname(__file__), 'cache', 'week_4_fy2027.json')).read())
missing = cache['events_without_summary']
print(f"Missing events: {len(missing)}")
for e in missing:
    print(f"  [{e.get('area','?')}] {e.get('title','?')} - {e['event_id']}")

# Query ALL missing
eids = [e['event_id'] for e in missing]
ids_str = ", ".join([f"'{eid}'" for eid in eids])
q = f"SELECT event_id, msg_txt FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` WHERE event_id IN ({ids_str})"
rows = list(client.query(q).result())
msg = rows[0].msg_txt
if isinstance(msg, dict):
    raw = msg.get('array', [''])[0]
else:
    raw = str(msg)

class HTE(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, d):
        self.parts.append(d)
    def get_text(self):
        return ' '.join(self.parts)

p = HTE()
p.feed(raw)
text = p.get_text()

# Show every occurrence of 'summar' in the text
print(f"Event: {missing[0]['title']}")
print(f"Text length: {len(text)} chars")
print()

for m in re.finditer(r'(?i)summar\w*', text):
    start = max(0, m.start()-30)
    end = min(len(text), m.end()+80)
    print(f"Found '{m.group()}' at pos {m.start()}:")
    print(f"  ...{text[start:end]}...")
    print()

# Show last 300 chars
print("=== Last 300 chars ===")
print(text[-300:])
