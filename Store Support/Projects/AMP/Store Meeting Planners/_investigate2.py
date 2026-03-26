"""Check what the calendar query actually filters on and what's missing"""
from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~\\AppData\\Roaming\\gcloud\\application_default_credentials.json')

client = bigquery.Client(project='wmt-assetprotection-prod')

# What statuses exist for Calendar Events?
print("CALENDAR EVENT STATUSES (all time):")
q = """
SELECT Message_Status, COUNT(DISTINCT Activity_Title) as titles, MIN(CAST(Start_Date AS STRING)) as earliest, MAX(CAST(Start_Date AS STRING)) as latest
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type = 'Calendar Events'
GROUP BY Message_Status
ORDER BY titles DESC
"""
for r in client.query(q).result():
    print(f"  {r.Message_Status}: {r.titles} titles ({r.earliest} to {r.latest})")

# What about Published status?
print("\nCALENDAR EVENTS with status 'Published':")
q2 = """
SELECT Activity_Title, Message_Status, CAST(Start_Date AS STRING) as s, CAST(End_Date AS STRING) as e, Store_Cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type = 'Calendar Events' AND Message_Status = 'Published'
  AND Start_Date >= '2026-01-01'
GROUP BY Activity_Title, Message_Status, Start_Date, End_Date, Store_Cnt
ORDER BY Start_Date
LIMIT 20
"""
rows = list(client.query(q2).result())
print(f"  Found {len(rows)}")
for r in rows:
    print(f"  [{r.Message_Status}] {r.Activity_Title} | {r.s} - {r.e} | Stores: {r.Store_Cnt}")

# Current query filters
print("\nWHAT OUR QUERY CURRENTLY RETURNS (using 3 status filters):")
q3 = """
SELECT Activity_Title, Message_Status, CAST(Start_Date AS STRING) as s, CAST(End_Date AS STRING) as e
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type = 'Calendar Events'
  AND Message_Status IN ('Awaiting ATC Approval', 'Awaiting Comms Approval', 'Review for Publish review')
  AND Start_Date <= '2026-03-31' AND End_Date >= '2026-03-01'
GROUP BY Activity_Title, Message_Status, Start_Date, End_Date
ORDER BY Start_Date
"""
rows3 = list(client.query(q3).result())
print(f"  Returns {len(rows3)} events for March 2026")
for r in rows3:
    print(f"  [{r.Message_Status}] {r.Activity_Title} | {r.s} - {r.e}")

# If we include more statuses
print("\nIF WE INCLUDE Published + Expired + all statuses:")
q4 = """
SELECT Activity_Title, Message_Status, CAST(Start_Date AS STRING) as s, CAST(End_Date AS STRING) as e, Store_Cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type = 'Calendar Events'
  AND Start_Date <= '2026-03-31' AND End_Date >= '2026-03-01'
GROUP BY Activity_Title, Message_Status, Start_Date, End_Date, Store_Cnt
ORDER BY Start_Date
"""
rows4 = list(client.query(q4).result())
print(f"  Returns {len(rows4)} events for March 2026")
for r in rows4:
    print(f"  [{r.Message_Status}] {r.Activity_Title} | {r.s} - {r.e} | Stores: {r.Store_Cnt}")

# Check Store Updates with Published status around now
print("\nSTORE UPDATES (Published) around now:")
q5 = """
SELECT Activity_Title, Message_Status, CAST(Start_Date AS STRING) as s, CAST(End_Date AS STRING) as e, Store_Cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type = 'Store Updates'
  AND Message_Status = 'Published'
  AND Start_Date >= '2026-03-15' AND Start_Date <= '2026-04-15'
GROUP BY Activity_Title, Message_Status, Start_Date, End_Date, Store_Cnt
ORDER BY Start_Date
LIMIT 20
"""
rows5 = list(client.query(q5).result())
print(f"  Found {len(rows5)}")
for r in rows5:
    print(f"  {r.Activity_Title} | {r.s} - {r.e} | Stores: {r.Store_Cnt}")

# Meeting requests
print("\nMEETING REQUESTS (all):")
q6 = """
SELECT Title, Status, CAST(`Start Date` AS STRING) as s, `Meeting Reoccurrence` as reoc
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
ORDER BY SAFE_CAST(`Start Date` AS DATE) DESC
LIMIT 15
"""
for r in client.query(q6).result():
    print(f"  [{r.Status}] {r.Title} | {r.s} | Reoc: {r.reoc}")
