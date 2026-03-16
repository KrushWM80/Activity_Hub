#!/usr/bin/env python3
"""Quick diagnostic: show Message_Type and Status values for WK 4 No Comm events"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json')

from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

print("=== Message_Type + Status for WK 4, Status LIKE '%No Comm%' ===")
q = """
SELECT DISTINCT Message_Type, Status, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4' AND Status LIKE '%No Comm%'
GROUP BY Message_Type, Status
ORDER BY cnt DESC
"""
for r in client.query(q).result():
    print(f"  Message_Type=[{r.Message_Type}] | Status=[{r.Status}] | Count={r.cnt}")

print("\n=== All Message_Type values for WK 4 (any status) ===")
q2 = """
SELECT DISTINCT Message_Type, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4'
GROUP BY Message_Type
ORDER BY cnt DESC
"""
for r in client.query(q2).result():
    print(f"  [{r.Message_Type}]: {r.cnt} events")
