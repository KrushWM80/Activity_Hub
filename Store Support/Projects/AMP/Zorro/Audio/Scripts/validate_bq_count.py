"""Quick BQ validation: count Week 10 FY2027 Merchant Messages by Status and Business Area."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

# Resolve ADC
for p in [
    os.path.join(os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'),
    os.path.expanduser('~/.config/gcloud/application_default_credentials.json'),
]:
    if os.path.isfile(p):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = p
        break

from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# Check which column has "AMP PR Merchandise"
print("=== Checking for AMP PR Merchandise in Week 10 FY2027 ===")
q_check = """
SELECT Business_Area, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '10' AND Message_Type = 'Merchant Message'
GROUP BY Business_Area
ORDER BY cnt DESC
"""
for row in client.query(q_check).result():
    print(f"  {row.Business_Area}: {row.cnt}")

print("\n=== Week 10 - No Comms only, by Business_Area ===")
q2 = """
SELECT Business_Area, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '10' AND Message_Type = 'Merchant Message'
  AND Status = 'Review for Publish review - No Comms'
GROUP BY Business_Area
ORDER BY cnt DESC
"""
for row in client.query(q2).result():
    print(f"  {row.Business_Area}: {row.cnt}")

print("\n=== Week 4 - No Comms only, by Business_Area ===")
q3 = """
SELECT Business_Area, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4' AND Message_Type = 'Merchant Message'
  AND Status = 'Review for Publish review - No Comms'
GROUP BY Business_Area
ORDER BY cnt DESC
"""
for row in client.query(q3).result():
    print(f"  {row.Business_Area}: {row.cnt}")
total = 0
for row in client.query(query).result():
    print(f"  {row.Status}: {row.cnt}")
    total += row.cnt
print(f"  TOTAL: {total}")

# Also check total distinct events regardless of status
query2 = """
SELECT COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '4' AND Message_Type = 'Merchant Message'
"""
for row in client.query(query2).result():
    print(f"\n  All statuses combined: {row.cnt} distinct events")
