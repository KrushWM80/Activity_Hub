#!/usr/bin/env python3
"""Query BigQuery for Weekly Message data to understand schema for audio pipeline"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

query = """
SELECT DISTINCT
  event_id,
  Title,
  Store_Area,
  Business_Area,
  Dept,
  Headline,
  week_at_glance_summary,
  Does_Have_Week_at_a_Glance,
  Week_at_a_Glance,
  WM_Week,
  FY,
  Status,
  Message_Type
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027
  AND WM_Week = '4'
  AND Status LIKE '%Published%'
  AND Message_Type LIKE '%Store Updates%'
ORDER BY Store_Area, Title
"""

rows = list(client.query(query).result())
print(f"Total distinct events for Week 4: {len(rows)}")
print()

for i, r in enumerate(rows[:60], 1):
    summary = (r.week_at_glance_summary or '')[:150]
    headline = (r.Headline or '')[:100]
    waag = (r.Week_at_a_Glance or '')[:100]
    print(f"{i}. [{r.Store_Area}] {r.Title[:80]}")
    print(f"   Dept: {r.Dept} | Has_WaaG: {r.Does_Have_Week_at_a_Glance}")
    print(f"   Headline: {headline}")
    print(f"   WaaG_Summary: {summary}")
    print(f"   WaaG: {waag}")
    print()
