#!/usr/bin/env python3
"""
Calculate Store High/Low/Avg from BigQuery result JSON
For each STORE: count distinct EVENT_IDs
Then find max/min/avg of those counts per store
"""

import json
from collections import defaultdict

# Load the BigQuery result JSON
with open(r'c:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard\bigquery_result.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the JSON array
import re
match = re.search(r'\[\s*\n\s*\{', content)
if not match:
    print("❌ Could not find JSON array in bigquery_result.json")
    exit(1)

idx = match.start()
end_idx = content.rfind(']') + 1
json_text = content[idx:end_idx]

try:
    data = json.loads(json_text)
except json.JSONDecodeError as e:
    print(f"❌ JSON parsing error: {e}")
    exit(1)

# Filter for Week 2
week2_data = [r for r in data if str(r.get('WM_Week', '')) == '2']

if not week2_data:
    print("❌ No Week 2 data found in bigquery_result.json")
    exit(1)

# For each row in the data, we need to map: which stores got this event?
# Since the data is event-level, we need store-level detail
# GROUP BY: store, COUNT DISTINCT: event_id

# Dictionary to track: for each store, which event_ids did it receive
store_event_mapping = defaultdict(set)  # store -> set of event_ids

# Note: The current JSON has aggregate data (Store_Cnt per event)
# But doesn't have individual store records
# We need to get store-level detail from the AMP data source

print("⚠️  Current data structure is event-level, not store-level")
print("We need store-level details from the AMP DataSource.\n")

# For now, let's use the Store Count data we have and note the limitation
print("=" * 70)
print("CURRENT DATA LIMITATION")
print("=" * 70)
print("The BigQuery JSON has EVENT-level aggregation:")
print("  - event_id with Store_Cnt (how many stores got each event)")
print("\nWe need STORE-level aggregation:")
print("  - Each store mapped to which event_ids they received")
print("  - Then count distinct event_ids PER STORE")
print("\nThis requires detail-level data from one of:")
print("  - AMP_ALL 2 table with individual store records")
print("  - Store dimension table with event mapping")
print("=" * 70)

# Create placeholder metrics
metrics = {
    'wm_week': 2,
    'fy': 2027,
    'store_high': 0,
    'store_low': 0,
    'store_avg': 0.0,
    'total_unique_events': len(week2_data),
    'note': 'PENDING: Need store-level detail data to calculate Event Count per Store'
}

print(f"\n⚠️  Store High/Low/Avg metrics require store-level data")
print(f"Please provide the store-to-event mapping data.")
print(f"\nTotal events in Week 2: {len(week2_data)}")

