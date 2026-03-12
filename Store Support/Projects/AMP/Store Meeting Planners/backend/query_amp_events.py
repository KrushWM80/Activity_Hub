"""Temp script to list all AMP Calendar Events from BigQuery."""
import os
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS",
    os.path.join(os.environ["APPDATA"], "gcloud", "application_default_credentials.json"))

from google.cloud import bigquery
client = bigquery.Client()

q = """
SELECT
    event_id,
    Activity_Title,
    Message_Type,
    Message_Status,
    SAFE_CAST(Start_Date AS STRING) as Start_Date,
    SAFE_CAST(End_Date AS STRING) as End_Date,
    Business_Area,
    Author,
    Store_Cnt,
    WM_Week,
    WM_Year
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type = 'Calendar Event'
  AND Message_Status = 'Published'
ORDER BY Start_Date
"""

rows = list(client.query(q).result())
print(f"Total Published Calendar Events: {len(rows)}\n")
print(f"{'WK':<5} {'FY':<5} {'Start Date':<22} {'End Date':<22} {'Stores':<8} {'Title':<60} {'Author'}")
print("-" * 160)
for r in rows:
    title = (r.Activity_Title or "")[:60]
    print(f"WK{r.WM_Week or '?':<3} FY{r.WM_Year or '?':<3} {str(r.Start_Date or ''):<22} {str(r.End_Date or ''):<22} {str(r.Store_Cnt or '-'):<8} {title:<60} {r.Author or ''}")
