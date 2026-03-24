"""Find AMP events with meeting/call details in Cosmos message body that aren't in Meeting Planner."""
import os, re
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS",
    os.path.join(os.environ["APPDATA"], "gcloud", "application_default_credentials.json"))

from google.cloud import bigquery
client = bigquery.Client()

# Step 1: Get event_ids from AMP ALL 2 (Store Updates + Calendar Events only)
print("=" * 70)
print("Step 1: Fetching AMP events (Store Updates + Calendar Events)...")
print("=" * 70)

q_events = """
SELECT DISTINCT
    a.event_id,
    a.Activity_Title,
    a.Message_Type,
    a.Message_Status,
    a.Author_email,
    a.Store_Cnt,
    a.Start_Date,
    a.End_Date,
    a.Business_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2` a
WHERE a.Start_Date >= '2025-10-01'
  AND a.Message_Type IN ('Store Updates', 'Calendar Events')
  AND a.Message_Status IN ('Awaiting ATC Approval', 'Awaiting Comms Approval',
      'Review for Publish review', 'Review for Publish review - No Comms')
  AND a.event_id IS NOT NULL
"""
events = list(client.query(q_events).result())
print(f"Found {len(events)} AMP events since Oct 2025 (Store Updates + Calendar Events)\n")

# Deduplicate by event_id (one row per event)
event_map = {}
for e in events:
    eid = e.event_id
    if eid not in event_map:
        event_map[eid] = dict(e)
print(f"Unique events by event_id: {len(event_map)}")

# Step 2: Query Cosmos table for message bodies of these events
print("\n" + "=" * 70)
print("Step 2: Fetching message bodies from Cosmos/EDW...")
print("=" * 70)

event_ids = list(event_map.keys())
# Batch query in groups of 50
body_map = {}
batch_size = 50
for i in range(0, len(event_ids), batch_size):
    batch = event_ids[i:i+batch_size]
    id_list = ", ".join(f"'{eid}'" for eid in batch)
    q_body = f"""
    SELECT event_id, msg_txt, msg_subj_nm
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    WHERE event_id IN ({id_list})
    """
    for row in client.query(q_body).result():
        eid = row.event_id
        # Extract text from msg_txt STRUCT<array ARRAY<STRING>>
        msg_txt = row.msg_txt
        body_text = ""
        if msg_txt:
            arr = []
            if isinstance(msg_txt, dict):
                arr = msg_txt.get('array', [])
            elif hasattr(msg_txt, 'get'):
                arr = msg_txt.get('array', [])
            elif isinstance(msg_txt, (list, tuple)):
                arr = msg_txt
            else:
                arr = [str(msg_txt)]
            if arr:
                raw_html = str(arr[0])
                # Strip HTML tags
                body_text = re.sub(r'<[^>]+>', ' ', raw_html)
                body_text = re.sub(r'\s+', ' ', body_text).strip()
        body_map[eid] = {
            "body": body_text,
            "subject": str(row.msg_subj_nm or "")
        }
    print(f"  Batch {i//batch_size + 1}: fetched {len(batch)} events")

print(f"\nGot message bodies for {len(body_map)} events")

# Debug: show sample bodies
non_empty = [(eid, info) for eid, info in body_map.items() if info["body"]]
print(f"Non-empty bodies: {len(non_empty)} / {len(body_map)}")
if non_empty:
    sample_eid, sample_info = non_empty[0]
    print(f"  Sample ({sample_eid}): {sample_info['body'][:200]}...")
else:
    # Show raw type info for first entry
    print("  WARNING: All bodies empty! Checking raw msg_txt structure...")
    # Quick debug query for one event
    sample_id = event_ids[0]
    q_debug = f"""
    SELECT event_id, msg_txt
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    WHERE event_id = '{sample_id}'
    """
    for dbg in client.query(q_debug).result():
        mt = dbg.msg_txt
        print(f"  msg_txt type: {type(mt)}")
        print(f"  msg_txt repr: {repr(mt)[:500]}")
        if isinstance(mt, dict):
            print(f"  dict keys: {mt.keys()}")
        elif hasattr(mt, '__dict__'):
            print(f"  attrs: {[a for a in dir(mt) if not a.startswith('_')]}")
        print(f"  str(msg_txt)[:300]: {str(mt)[:300]}")

# Step 3: Search bodies for meeting/call indicators
print("\n" + "=" * 70)
print("Step 3: Searching message bodies for meeting/call content...")
print("=" * 70)

# HIGH-CONFIDENCE patterns: actual meeting join details (Meeting ID + Passcode, links)
high_confidence_patterns = [
    r'meeting\s*id\s*[:\s]\s*\d{3,}',           # "Meeting ID: 12345678"
    r'passcode\s*[:\s]\s*\S+',                    # "Passcode: abc123"
    r'zoom\.(us|com)/[jw]/\d+',                   # Zoom join link
    r'teams\.microsoft\.com/.+/meetup-join',       # Teams join link
    r'webex\.\w+\.com/\S+',                        # WebEx link
    r'(?:dial|call)[\s-]in\s*(?:number|info)',     # "Dial-in number/info"
    r'\d{3}[\s.-]\d{3,4}[\s.-]\d{4}.*(?:pin|code|access)', # Phone + PIN
]
# MEDIUM-CONFIDENCE patterns: meeting language (needs 2+ to flag)
medium_patterns = [
    r'join\s+(?:the\s+)?(?:call|meeting|session)',
    r'attend\s+(?:the\s+)?(?:call|meeting|session)',
    r'conference\s*(?:call|bridge|line)',
    r'(?:kickoff|deployment|admin|installation)\s*call',
    r'listening\s+session',
]
high_compiled = [re.compile(p, re.IGNORECASE) for p in high_confidence_patterns]
med_compiled = [re.compile(p, re.IGNORECASE) for p in medium_patterns]

meetings_found = []
for eid, info in body_map.items():
    body = info["body"]
    if not body:
        continue
    # Check high-confidence patterns (any 1 match = flag)
    high_matches = []
    for i, pat in enumerate(high_compiled):
        if pat.search(body):
            high_matches.append(high_confidence_patterns[i])
    # Check medium-confidence patterns (need 2+ matches to flag)
    med_matches = []
    for i, pat in enumerate(med_compiled):
        if pat.search(body):
            med_matches.append(medium_patterns[i])
    # Flag if any high-confidence OR 2+ medium-confidence
    if high_matches or len(med_matches) >= 2:
        confidence = "HIGH" if high_matches else "MEDIUM"
        all_matches = high_matches + med_matches
        event_meta = event_map.get(eid, {})
        meetings_found.append({
            "event_id": eid,
            "title": event_meta.get("Activity_Title", ""),
            "type": event_meta.get("Message_Type", ""),
            "status": event_meta.get("Message_Status", ""),
            "author": event_meta.get("Author_email", ""),
            "start": str(event_meta.get("Start_Date", ""))[:10],
            "end": str(event_meta.get("End_Date", ""))[:10],
            "area": event_meta.get("Business_Area", ""),
            "stores": event_meta.get("Store_Cnt", 0),
            "patterns": all_matches,
            "confidence": confidence,
            "body_snippet": body[:400]
        })

print(f"Events with meeting/call content: {len(meetings_found)}")

# Step 4: Cross-reference against existing meeting requests
print("\n" + "=" * 70)
print("Step 4: Cross-referencing against existing Meeting Planner requests...")
print("=" * 70)

q_existing = """
SELECT DISTINCT LOWER(TRIM(Title)) as title_lower
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
"""
existing_titles = set()
for r in client.query(q_existing).result():
    if r.title_lower:
        existing_titles.add(r.title_lower)
print(f"Existing meeting request titles: {len(existing_titles)}")

missing = []
already_tracked = []
for m in meetings_found:
    title_lower = m["title"].strip().lower()
    found = False
    for et in existing_titles:
        if title_lower in et or et in title_lower:
            found = True
            break
        if len(title_lower) > 15 and len(et) > 15 and title_lower[:30] == et[:30]:
            found = True
            break
    if found:
        already_tracked.append(m)
    else:
        missing.append(m)

print(f"\nAlready tracked in Meeting Planner: {len(already_tracked)}")
print(f"MISSING from Meeting Planner:      {len(missing)}")

if already_tracked:
    print("\n--- Already Tracked ---")
    for m in already_tracked:
        print(f"  {m['start']} | {m['type']:<20} | {m['title'][:55]}")

print("\n" + "=" * 70)
print("EVENTS WITH MEETING CONTENT NOT IN MEETING PLANNER:")
print("=" * 70)
for m in missing:
    print(f"\n  [{m.get('confidence','?')}] {m['title']}")
    print(f"  Type:     {m['type']} | Status: {m['status']}")
    print(f"  Dates:    {m['start']} to {m['end']}")
    print(f"  Author:   {m['author']}")
    print(f"  Area:     {m['area']} | Stores: {m['stores']}")
    print(f"  Patterns: {', '.join(m['patterns'])}")
    print(f"  Body:     {m['body_snippet'][:250]}...")
