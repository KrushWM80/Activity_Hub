from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~\\AppData\\Roaming\\gcloud\\application_default_credentials.json')
client = bigquery.Client(project='wmt-assetprotection-prod')
q = """SELECT Title, Status, CAST(`Start Date` AS STRING) as sd, CAST(`End Date` AS STRING) as ed, 
       `Meeting Reoccurrence` as reoc, `Meeting Type` as mtype, Email, Name,
       CAST(`Submission Start time` AS STRING) as submitted,
       `Created By` as created_by
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
ORDER BY SAFE_CAST(`Start Date` AS DATE) DESC"""
rows = list(client.query(q).result())
print(f"TOTAL ROWS: {len(rows)}")
print()

# Status summary
from collections import Counter
statuses = Counter(r.Status for r in rows)
print("STATUS SUMMARY:")
for s, c in statuses.most_common():
    print(f"  {s}: {c}")
print()

# Date range summary
dates = [str(r.sd)[:10] for r in rows if r.sd]
print(f"DATE RANGE: {min(dates)} to {max(dates)}")
print()

for i, r in enumerate(rows, 1):
    ed = str(r.ed)[:10] if r.ed else "N/A"
    sd = str(r.sd)[:10] if r.sd else "N/A"
    cb = r.created_by or ""
    print(f"{i:2d}. [{r.Status:8s}] {r.Title}")
    print(f"    Date: {sd} to {ed} | Type: {r.mtype} | Reoc: {r.reoc} | By: {r.Name} | Creator: {cb}")
    print()
