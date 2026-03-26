"""Re-query store_meeting_request_data after update, then pull AMP message bodies
for known meeting requests to discover keyword patterns."""
from google.cloud import bigquery
import os, re
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~\\AppData\\Roaming\\gcloud\\application_default_credentials.json')

client = bigquery.Client(project='wmt-assetprotection-prod')

# ============================================================
# PART 1: Fresh dump of store_meeting_request_data
# ============================================================
print("=" * 90)
print("PART 1: store_meeting_request_data (REFRESHED)")
print("=" * 90)
q1 = """
SELECT Title, Status, 
       CAST(`Start Date` AS STRING) as Start_Date,
       CAST(`End Date` AS STRING) as End_Date,
       `Meeting Type`, `Meeting Reoccurrence`, 
       `AMP Activity`, `AMP Activity URL`,
       Email, Name, `Meeting Duration`, 
       `Meeting Link`
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
ORDER BY SAFE_CAST(`Start Date` AS DATE) DESC
"""
rows = [dict(r) for r in client.query(q1).result()]
print(f"Total rows: {len(rows)}\n")

titles_for_search = []
for i, r in enumerate(rows, 1):
    title = r.get('Title', '') or ''
    status = r.get('Status', '') or ''
    start = str(r.get('Start_Date', ''))[:10]
    end = str(r.get('End_Date', ''))[:10]
    mtype = r.get('Meeting Type', '') or ''
    reoc = r.get('Meeting Reoccurrence', '') or ''
    amp = r.get('AMP Activity', False)
    amp_url = r.get('AMP Activity URL', '') or ''
    email = r.get('Email', '') or ''
    name = r.get('Name', '') or ''
    duration = r.get('Meeting Duration', '') or ''
    link = r.get('Meeting Link', '') or ''
    print(f"{i:3d}. [{status}] {title}")
    print(f"     Start: {start} | End: {end} | Dur: {duration} | Type: {mtype} | Reoc: {reoc}")
    if amp_url:
        print(f"     AMP URL: {amp_url[:80]}")
    if link:
        print(f"     Meeting Link: {link[:100]}")
    if email or name:
        print(f"     Submitter: {name} / {email}")
    print()
    if title:
        titles_for_search.append(title.strip())

print(f"Status breakdown:")
statuses = {}
for r in rows:
    s = r.get('Status', 'unknown')
    statuses[s] = statuses.get(s, 0) + 1
for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
    print(f"  {s}: {c}")
dates = [str(r.get('Start_Date', ''))[:10] for r in rows if r.get('Start_Date')]
if dates:
    print(f"Date range: {min(dates)} to {max(dates)}")
