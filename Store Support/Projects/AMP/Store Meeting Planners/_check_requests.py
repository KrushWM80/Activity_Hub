"""Investigate store_meeting_request_data table thoroughly"""
from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~\\AppData\\Roaming\\gcloud\\application_default_credentials.json')

client = bigquery.Client(project='wmt-assetprotection-prod')

# 1. Schema
print("=" * 80)
print("SCHEMA: store_meeting_request_data")
print("=" * 80)
table = client.get_table('Store_Support_Dev.store_meeting_request_data')
for i, f in enumerate(table.schema, 1):
    print(f"  {i:2d}. {f.name} ({f.field_type})")
print(f"\nTotal rows: {table.num_rows}")

# 2. ALL rows
print("\n" + "=" * 80)
print("ALL ROWS (ordered by Start Date DESC)")
print("=" * 80)
q = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
ORDER BY SAFE_CAST(`Start Date` AS DATE) DESC
"""
rows = [dict(r) for r in client.query(q).result()]
print(f"Total: {len(rows)} rows\n")
for i, r in enumerate(rows, 1):
    print(f"--- Row {i} ---")
    for k, v in r.items():
        if v is not None and str(v).strip():
            print(f"  {k}: {v}")
    print()
