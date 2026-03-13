"""Find AMP ALL 2 events with meeting/call info in message body that aren't in Meeting Planner."""
import os
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS",
    os.path.join(os.environ["APPDATA"], "gcloud", "application_default_credentials.json"))

from google.cloud import bigquery
client = bigquery.Client()

# Step 1: Find non-Calendar-Event AMP entries with meeting keywords in body
print("=" * 70)
print("Searching AMP ALL 2 for meeting/call details in Message Body...")
print("(non-Calendar Events, after Oct 2025)")
print("=" * 70)

q = """
SELECT
    Activity_Title,
    Message_Type,
    Message_Status,
    event_id,
    Author_email,
    Store_Cnt,
    MIN(SAFE_CAST(Start_Date AS DATE)) as start_date,
    MAX(SAFE_CAST(End_Date AS DATE)) as end_date,
    ANY_VALUE(Message_Body) as message_body
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type != 'Calendar Events'
  AND Message_Status IN ('Awaiting ATC Approval', 'Awaiting Comms Approval', 'Review for Publish review')
  AND SAFE_CAST(Start_Date AS DATE) >= '2025-10-01'
  AND (
    LOWER(Message_Body) LIKE '%meeting id%'
    OR LOWER(Message_Body) LIKE '%passcode%'
    OR LOWER(Message_Body) LIKE '%zoom%'
    OR LOWER(Message_Body) LIKE '%teams meeting%'
    OR LOWER(Message_Body) LIKE '%join the call%'
    OR LOWER(Message_Body) LIKE '%attend the%call%'
    OR LOWER(Message_Body) LIKE '%office hours%'
    OR LOWER(Message_Body) LIKE '%webex%'
    OR LOWER(Message_Body) LIKE '%dial-in%'
    OR LOWER(Message_Body) LIKE '%conference call%'
    OR LOWER(Message_Body) LIKE '% at % p.m.%'
    OR LOWER(Message_Body) LIKE '% at % a.m.%'
    OR LOWER(Message_Body) LIKE '%kickoff call%'
    OR LOWER(Message_Body) LIKE '%listening session%'
    OR LOWER(Message_Body) LIKE '%brown bag%'
    OR LOWER(Message_Body) LIKE '%deployment call%'
    OR LOWER(Message_Body) LIKE '%admin call%'
    OR LOWER(Message_Body) LIKE '%installation call%'
    OR LOWER(Message_Body) LIKE '%broadcast%'
  )
GROUP BY Activity_Title, Message_Type, Message_Status, event_id, Author_email, Store_Cnt
ORDER BY start_date DESC
"""

rows = list(client.query(q).result())
print(f"\nFound {len(rows)} AMP events with meeting/call content\n")

# Step 2: Cross-reference against existing meeting requests
q_existing = """
SELECT DISTINCT LOWER(TRIM(Title)) as title_lower
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
"""
existing = set()
for r in client.query(q_existing).result():
    if r.title_lower:
        existing.add(r.title_lower)

missing = []
already_tracked = []
for r in rows:
    title = (r.Activity_Title or '').strip()
    title_lower = title.lower()
    found = False
    for et in existing:
        if title_lower in et or et in title_lower:
            found = True
            break
        if len(title_lower) > 15 and len(et) > 15 and title_lower[:30] == et[:30]:
            found = True
            break
    if found:
        already_tracked.append(r)
    else:
        missing.append(r)

print(f"Already have a meeting request: {len(already_tracked)}")
print(f"MISSING from Meeting Planner:   {len(missing)}")

print("\n" + "=" * 70)
print("EVENTS ALREADY TRACKED IN MEETING PLANNER:")
print("=" * 70)
for r in already_tracked:
    sd = str(r.start_date or '')[:10]
    print(f"  {sd} | {r.Message_Type:<20} | {(r.Activity_Title or '')[:55]}")

print("\n" + "=" * 70)
print("EVENTS MISSING FROM MEETING PLANNER (need a request):")
print("=" * 70)
for r in missing:
    sd = str(r.start_date or '')[:10]
    ed = str(r.end_date or '')[:10]
    body = (r.message_body or '')[:300].replace('\n', ' ')
    print(f"\n  Title:    {r.Activity_Title}")
    print(f"  Type:     {r.Message_Type} | Status: {r.Message_Status}")
    print(f"  Dates:    {sd} to {ed}")
    print(f"  Author:   {r.Author_email}")
    print(f"  EventID:  {r.event_id} | Stores: {r.Store_Cnt}")
    print(f"  Body:     {body}...")
