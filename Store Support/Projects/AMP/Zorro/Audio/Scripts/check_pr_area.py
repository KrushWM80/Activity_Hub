"""Check AMP PR Merchandise event and all Business_Area values for Week 10."""
import os
for p in [os.path.join(os.environ.get('APPDATA',''),'gcloud','application_default_credentials.json')]:
    if os.path.isfile(p): os.environ['GOOGLE_APPLICATION_CREDENTIALS']=p; break

from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# 1. Check the specific event from the URL
print("=== Specific Event: 211d20a3-7fd9-4df7-bdf6-cfc80c55d813 ===")
q1 = """
SELECT event_id, Business_Area, Store_Area, Title, Message_Type, Status, WM_Week, FY
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE event_id = '211d20a3-7fd9-4df7-bdf6-cfc80c55d813'
"""
for row in client.query(q1).result():
    print(f"  Business_Area: {row.Business_Area}")
    print(f"  Store_Area: {row.Store_Area}")
    print(f"  Message_Type: {row.Message_Type}")
    print(f"  Status: {row.Status}")
    print(f"  Title: {row.Title}")
    print(f"  WM_Week: {row.WM_Week}, FY: {row.FY}")

# 2. Find ALL distinct Business_Area for Week 10 (no Message_Type filter)
print("\n=== Week 10 FY2027 - ALL Business_Area (no Message_Type filter) ===")
q2 = """
SELECT Business_Area, Message_Type, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '10'
GROUP BY Business_Area, Message_Type
ORDER BY Business_Area, Message_Type
"""
for row in client.query(q2).result():
    marker = " <<<" if "PR" in (row.Business_Area or "") else ""
    print(f"  {row.Business_Area} | {row.Message_Type}: {row.cnt}{marker}")

# 3. Full status breakdown for Week 10 - ALL Message_Types
print("\n=== Week 10 FY2027 - ALL statuses, ALL Message_Types (Merchant Message only) ===")
q3 = """
SELECT Status, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '10' AND Message_Type = 'Merchant Message'
GROUP BY Status
ORDER BY cnt DESC
"""
total = 0
for row in client.query(q3).result():
    print(f"  {row.Status}: {row.cnt}")
    total += row.cnt
print(f"  TOTAL: {total}")

# 4. Count AMP PR Merchandise specifically for Week 10
print("\n=== AMP PR Merchandise in Week 10 Merchant Messages ===")
q4 = """
SELECT Status, COUNT(DISTINCT event_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND WM_Week = '10' AND Message_Type = 'Merchant Message'
  AND Business_Area LIKE '%PR%'
GROUP BY Status
"""
pr_total = 0
for row in client.query(q4).result():
    print(f"  {row.Status}: {row.cnt}")
    pr_total += row.cnt
if pr_total == 0:
    print("  (none found)")
else:
    print(f"  TOTAL PR: {pr_total}")
