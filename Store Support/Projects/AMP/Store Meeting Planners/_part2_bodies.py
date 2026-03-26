"""Part 2: Match known meeting request titles to AMP events, pull Cosmos bodies,
and extract keyword patterns that indicate a store meeting."""
from google.cloud import bigquery
import os, re, json
from collections import Counter
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~\\AppData\\Roaming\\gcloud\\application_default_credentials.json')

client = bigquery.Client(project='wmt-assetprotection-prod')

# Step 1: Get unique AMP URLs from meeting request data
print("=" * 90)
print("STEP 1: Get AMP Activity URLs from meeting request data")
print("=" * 90)
q0 = """
SELECT DISTINCT `AMP Activity URL` as url, Title
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
WHERE `AMP Activity URL` IS NOT NULL AND `AMP Activity URL` != ''
"""
url_rows = [dict(r) for r in client.query(q0).result()]
print(f"Found {len(url_rows)} rows with AMP URLs\n")

# Extract event_ids from URLs (format: .../message/{uuid}/... or .../preview/{uuid}/...)
url_event_ids = set()
url_title_map = {}
for r in url_rows:
    url = r.get('url', '')
    title = r.get('Title', '')
    # Extract UUID from URL
    m = re.search(r'/(message|preview)/([a-f0-9-]{36})/', url)
    if m:
        eid = m.group(2)
        url_event_ids.add(eid)
        url_title_map[eid] = title
        
print(f"Extracted {len(url_event_ids)} unique event_ids from URLs\n")

# Step 2: Also get all unique titles (for title-based matching)
q_titles = """
SELECT DISTINCT LOWER(TRIM(Title)) as title
FROM `wmt-assetprotection-prod.Store_Support_Dev.store_meeting_request_data`
WHERE Title IS NOT NULL AND Title != ''
"""
known_titles = set()
for r in client.query(q_titles).result():
    t = r.get('title', '')
    if t:
        known_titles.add(t)
print(f"Unique known meeting titles: {len(known_titles)}\n")
for t in sorted(known_titles):
    print(f"  - {t}")

# Step 3: Match titles in AMP ALL 2 to get event_ids
print("\n" + "=" * 90)
print("STEP 2: Find matching events in AMP ALL 2")
print("=" * 90)

# Use title matching + URL matching combined
# First try URL-based matching (most reliable)
amp_events = {}
if url_event_ids:
    # Not all URLs use event_id as the UUID — the URL UUID is the message_id
    # Try matching via Activity_Title instead
    pass

# Title-based matching in AMP ALL 2
# Build OR conditions for each unique title keyword (first 3+ words)
title_keywords = set()
for t in known_titles:
    # Get meaningful words (3+ chars)
    words = [w for w in t.split() if len(w) >= 4]
    if len(words) >= 2:
        # Use first 2-3 significant words
        title_keywords.add(' '.join(words[:3]).lower())

print(f"\nSearching AMP ALL 2 for {len(title_keywords)} title patterns...\n")

# Query AMP ALL 2 for events matching known titles
all_amp_event_ids = set()
for tk in title_keywords:
    escaped = tk.replace("'", "\\'")
    q = f"""
    SELECT DISTINCT event_id, Activity_Title, Message_Type, Message_Status
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE LOWER(Activity_Title) LIKE '%{escaped}%'
      AND event_id IS NOT NULL
    LIMIT 5
    """
    try:
        for r in client.query(q).result():
            eid = r.event_id
            if eid not in amp_events:
                amp_events[eid] = {
                    'event_id': eid,
                    'title': r.Activity_Title,
                    'type': r.Message_Type,
                    'status': r.Message_Status,
                }
                all_amp_event_ids.add(eid)
    except:
        pass

print(f"Found {len(amp_events)} matched AMP events\n")
for eid, m in sorted(amp_events.items(), key=lambda x: x[1]['title']):
    print(f"  [{m['type']}] [{m['status'][:20]}] {m['title']} (eid={eid})")

# Step 4: Pull message bodies from Cosmos
print("\n" + "=" * 90)
print("STEP 3: Pull Cosmos message bodies for matched events")
print("=" * 90)

event_ids = list(all_amp_event_ids)
print(f"Pulling bodies for {len(event_ids)} event_ids...")

bodies = {}
for i in range(0, len(event_ids), 50):
    batch = event_ids[i:i+50]
    id_list = ", ".join(f"'{eid}'" for eid in batch)
    q3 = f"""
    SELECT event_id, msg_txt
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    WHERE event_id IN ({id_list})
    """
    for r in client.query(q3).result():
        eid = r.event_id
        msg_txt = r.msg_txt
        body = ""
        if msg_txt and isinstance(msg_txt, dict):
            arr = msg_txt.get("array", [])
            if arr:
                raw_html = str(arr[0])
                body = re.sub(r'<[^>]+>', ' ', raw_html)
                body = re.sub(r'\s+', ' ', body).strip()
        if body:
            bodies[eid] = body

print(f"Retrieved {len(bodies)} message bodies\n")

# Step 5: Print bodies grouped by type
print("=" * 90)
print("STEP 4: Message body samples (first 400 chars each)")
print("=" * 90)
for eid, body in sorted(bodies.items(), key=lambda x: amp_events.get(x[0], {}).get('title', '')):
    meta = amp_events.get(eid, {})
    print(f"\n--- [{meta.get('type','')}] {meta.get('title','Unknown')} ---")
    print(f"BODY: {body[:400]}")

# Step 6: Keyword frequency analysis
print("\n\n" + "=" * 90)
print("STEP 5: KEYWORD FREQUENCY ANALYSIS")
print("=" * 90)
print(f"Analyzing {len(bodies)} message bodies from known meeting requests...\n")

keyword_patterns = [
    ('call', r'\bcall\b'),
    ('meeting', r'\bmeeting\b'),
    ('office hours', r'\boffice\s+hours\b'),
    ('join', r'\bjoin\b'),
    ('join us', r'\bjoin\s+us\b'),
    ('dial', r'\bdial\b'),
    ('dial-in', r'\bdial[\s-]*in\b'),
    ('zoom', r'\bzoom\b'),
    ('teams', r'\bteams\b'),
    ('webex', r'\bwebex\b'),
    ('passcode', r'\bpasscode\b'),
    ('password', r'\bpassword\b'),
    ('meeting id', r'\bmeeting\s*id\b'),
    ('session', r'\bsession\b'),
    ('kickoff', r'\bkick[\s-]*off\b'),
    ('launch', r'\blaunch\b'),
    ('training', r'\btraining\b'),
    ('broadcast', r'\bbroadcast\b'),
    ('listening', r'\blistening\b'),
    ('conference', r'\bconference\b'),
    ('bridge', r'\bbridge\b'),
    ('pin', r'\bpin\b'),
    ('register', r'\bregister\b'),
    ('sign up', r'\bsign\s+up\b'),
    ('rsvp', r'\brsvp\b'),
    ('attend', r'\battend\b'),
    ('calendar invite', r'\bcalendar\s+invite\b'),
    ('outlook', r'\boutlook\b'),
    ('link below', r'\blink\s+below\b'),
    ('click here', r'\bclick\s+here\b'),
    ('virtual', r'\bvirtual\b'),
    ('live', r'\blive\b'),
    ('webinar', r'\bwebinar\b'),
    ('town hall', r'\btown[\s-]*hall\b'),
    ('brown bag', r'\bbrown\s+bag\b'),
    ('open forum', r'\bopen\s+forum\b'),
    ('q&a', r'\bq\s*[&+]\s*a\b'),
    ('walk-through', r'\bwalk[\s-]*through\b'),
    ('walkthrough', r'\bwalkthrough\b'),
    ('demo', r'\bdemo\b'),
    ('install', r'\binstall'),
    ('deployment', r'\bdeployment\b'),
    ('pilot', r'\bpilot\b'),
    ('rollout', r'\broll[\s-]*out\b'),
    ('admin call', r'\badmin\s+call\b'),
    ('update call', r'\bupdate\s+call\b'),
    ('weekly call', r'\bweekly\s+call\b'),
    ('phone', r'\bphone\b'),
    ('invite', r'\binvite\b'),
    ('agenda', r'\bagenda\b'),
    ('pre-launch', r'\bpre[\s-]*launch\b'),
    ('evaluation', r'\bevaluation\b'),
    ('support call', r'\bsupport\s+call\b'),
    ('office hour', r'\boffice\s+hour\b'),
    ('questions', r'\bquestions?\b'),
    ('troubleshoot', r'\btroubleshoot'),
    ('real-time', r'\breal[\s-]*time\b'),
    ('feedback', r'\bfeedback\b'),
    ('how to', r'\bhow\s+to\b'),
    ('learn more', r'\blearn\s+more\b'),
    ('reach out', r'\breach\s+out\b'),
    ('contact', r'\bcontact\b'),
    ('email', r'\bemail\b'),
    ('coach', r'\bcoach\b'),
    ('champion', r'\bchampion\b'),
    ('coordinator', r'\bcoordinator\b'),
    ('host', r'\bhost\b'),
    ('hosting', r'\bhosting\b'),
    ('schedule', r'\bschedule\b'),
    ('scheduled', r'\bscheduled\b'),
]

hits = {}
for label, pattern in keyword_patterns:
    count = 0
    examples = []
    for eid, body in bodies.items():
        if re.search(pattern, body, re.I):
            count += 1
            title = amp_events.get(eid, {}).get('title', '')
            examples.append(title)
    if count > 0:
        hits[label] = (count, examples)

# Sort by frequency
total = len(bodies) or 1
print(f"{'KEYWORD':<20} {'HITS':>5} {'%':>5}  EXAMPLE TITLES")
print("-" * 90)
for label, (count, examples) in sorted(hits.items(), key=lambda x: -x[1][0]):
    pct = count / total * 100
    ex = examples[0][:50] if examples else ''
    print(f"  {label:<18} {count:>5} {pct:>4.0f}%  {ex}")

# Step 7: URL patterns
print(f"\n\nURL/Link patterns in bodies:")
url_pats = [
    ('zoom link', r'zoom\.(us|com)/[jw]/\d+'),
    ('teams link', r'teams\.microsoft\.com'),
    ('webex link', r'webex\.\w+\.com'),
    ('phone number', r'\b\d{3}[\s.-]\d{3,4}[\s.-]\d{4}\b'),
    ('meeting id digits', r'meeting\s*id\s*[:\s]\s*\d{3,}'),
    ('any URL', r'https?://\S+'),
    ('walmart URL', r'walmart\.com\S*'),
]
for label, pattern in url_pats:
    matches = []
    for eid, body in bodies.items():
        found = re.findall(pattern, body, re.I)
        if found:
            title = amp_events.get(eid, {}).get('title', '')
            matches.append(title)
    if matches:
        print(f"  '{label}': {len(matches)} bodies ({len(matches)/total*100:.0f}%)")
        for t in matches[:3]:
            print(f"    -> {t}")
