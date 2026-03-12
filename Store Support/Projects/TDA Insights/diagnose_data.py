#!/usr/bin/env python3
"""
Diagnostic script to investigate data discrepancies between our dashboard and the other dashboard.
"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

from google.cloud import bigquery

PROJECT = 'wmt-assetprotection-prod'
DATASET = 'Store_Support_Dev'
TABLE = 'Output- TDA Report'

client = bigquery.Client(project=PROJECT)

print("=" * 90)
print("DIAGNOSTIC REPORT: TDA Insights Data Investigation")
print("=" * 90)

# 1. Raw row count
print("\n--- 1. RAW TABLE INFO ---")
q1 = f"SELECT COUNT(*) as total_rows FROM `{PROJECT}.{DATASET}.{TABLE}`"
for row in client.query(q1).result():
    print(f"Total raw rows in table: {row.total_rows}")

# 2. All distinct Phases and their counts
print("\n--- 2. ALL PHASES (including Complete) ---")
q2 = f"""
SELECT Phase, COUNT(DISTINCT Topic) as num_topics, COUNT(*) as num_rows, COUNT(DISTINCT Facility) as distinct_facilities
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic IS NOT NULL
GROUP BY Phase
ORDER BY Phase
"""
phase_data = {}
for row in client.query(q2).result():
    phase = row.Phase or '(NULL)'
    print(f"  Phase: {phase:25s} | Topics: {row.num_topics:3d} | Rows: {row.num_rows:4d} | Distinct Facilities: {row.distinct_facilities}")
    phase_data[phase] = {'topics': row.num_topics, 'rows': row.num_rows, 'facilities': row.distinct_facilities}

# 3. All distinct Health Statuses
print("\n--- 3. ALL HEALTH STATUSES ---")
q3 = f"""
SELECT Health_Update, COUNT(DISTINCT Topic) as num_topics
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic IS NOT NULL
GROUP BY Health_Update
ORDER BY Health_Update
"""
for row in client.query(q3).result():
    print(f"  Health: {(row.Health_Update or '(NULL)'):25s} | Topics: {row.num_topics}")

# 4. Phase x Health Status cross-tab (excluding Complete)
print("\n--- 4. PHASE x HEALTH STATUS CROSS-TAB (excluding Complete) ---")
q4 = f"""
SELECT Phase, Health_Update, COUNT(DISTINCT Topic) as num_topics
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic IS NOT NULL AND Phase != 'Complete'
GROUP BY Phase, Health_Update
ORDER BY Phase, Health_Update
"""
for row in client.query(q4).result():
    print(f"  {(row.Phase or '(NULL)'):25s} | {(row.Health_Update or '(NULL)'):15s} | Topics: {row.num_topics}")

# 5. What our dashboard query actually returns 
print("\n--- 5. OUR DASHBOARD QUERY OUTPUT (grouped, excluding Complete) ---")
q5 = f"""
SELECT 
    Topic as title,
    Health_Update as health,
    Phase,
    COUNT(DISTINCT Facility) as store_count,
    Dallas_POC,
    Intake_n_Testing,
    Deployment
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic IS NOT NULL
GROUP BY Topic, Health_Update, Phase, Intake_n_Testing, Dallas_POC, Deployment
HAVING Phase != 'Complete'
ORDER BY Phase, Topic
"""
dashboard_rows = list(client.query(q5).result())
print(f"Total grouped rows (our dashboard sees): {len(dashboard_rows)}")

# Group by phase for counting
from collections import defaultdict
phase_projects = defaultdict(list)
for row in dashboard_rows:
    phase_projects[row.Phase].append({
        'title': row.title,
        'health': row.health,
        'stores': row.store_count,
        'display_stores': 0 if row.store_count == 1 else row.store_count
    })

for phase in sorted(phase_projects.keys()):
    projects = phase_projects[phase]
    print(f"\n  Phase: {phase} ({len(projects)} rows)")
    # Count by health
    health_counts = defaultdict(int)
    for p in projects:
        health_counts[p['health']] += 1
    for h, c in sorted(health_counts.items()):
        print(f"    {h}: {c}")
    # List all projects
    for p in sorted(projects, key=lambda x: x['title']):
        print(f"    - {p['title']:50s} | Health: {p['health']:15s} | Raw Stores: {p['stores']:5d} | Display: {p['display_stores']}")

# 6. Check for duplicate Topics (same topic, different grouped rows)
print("\n--- 6. TOPICS WITH MULTIPLE GROUPED ROWS (may appear duplicated) ---")
topic_counts = defaultdict(int)
for row in dashboard_rows:
    topic_counts[row.title] += 1
duplicates = {t: c for t, c in topic_counts.items() if c > 1}
if duplicates:
    for t, c in sorted(duplicates.items()):
        print(f"  '{t}' appears {c} times (different POC/Testing/Deployment values)")
        for row in dashboard_rows:
            if row.title == t:
                print(f"    Phase={row.Phase}, Health={row.health}, Stores={row.store_count}, POC={row.Dallas_POC[:40] if row.Dallas_POC else 'N/A'}")
else:
    print("  No duplicates found - each Topic has exactly one grouped row")

# 7. Unique topics per phase (deduplicated)
print("\n--- 7. UNIQUE TOPICS PER PHASE (deduplicated) ---")
phase_unique_topics = defaultdict(set)
for row in dashboard_rows:
    phase_unique_topics[row.Phase].add(row.title)
for phase in sorted(phase_unique_topics.keys()):
    topics = sorted(phase_unique_topics[phase])
    print(f"\n  {phase}: {len(topics)} unique topics")
    for t in topics:
        print(f"    - {t}")

# 8. Specific checks from user's report
print("\n--- 8. SPECIFIC CHECKS ---")

# Pending
print("\n  [Pending]")
pending = [r for r in dashboard_rows if r.Phase == 'Pending']
print(f"  We show: {len(pending)} rows")
pending_topics = set(r.title for r in pending)
print(f"  Unique topics: {len(pending_topics)}")

# Check Checkout Anywhere
print(f"\n  Looking for 'Checkout Anywhere' across ALL phases:")
q_ca = f"""
SELECT Topic, Phase, Health_Update, COUNT(DISTINCT Facility) as stores
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE LOWER(Topic) LIKE '%checkout%'
GROUP BY Topic, Phase, Health_Update
"""
for row in client.query(q_ca).result():
    print(f"    Topic='{row.Topic}', Phase={row.Phase}, Health={row.Health_Update}, Stores={row.stores}")

# POC/POT  
print("\n  [POC/POT]")
poc_pot = [r for r in dashboard_rows if r.Phase in ('POC', 'POT', 'POC/POT')]
print(f"  We show: {len(poc_pot)} rows")
poc_topics = set(r.title for r in poc_pot)
print(f"  Unique topics: {len(poc_topics)}")

# Check 3rd Party Cut Fruit
print(f"\n  Looking for '3rd Party Cut Fruit' or 'Cut Fruit' across ALL phases:")
q_cf = f"""
SELECT Topic, Phase, Health_Update, COUNT(DISTINCT Facility) as stores
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE LOWER(Topic) LIKE '%fruit%' OR LOWER(Topic) LIKE '%3rd%' OR LOWER(Topic) LIKE '%third%'
GROUP BY Topic, Phase, Health_Update
"""
for row in client.query(q_cf).result():
    print(f"    Topic='{row.Topic}', Phase={row.Phase}, Health={row.Health_Update}, Stores={row.stores}")

# Roll/Deploy
print("\n  [Roll/Deploy]")
roll_deploy = [r for r in dashboard_rows if r.Phase in ('Roll/Deploy', 'Roll / Deploy', 'Deploy', 'Rollout')]
print(f"  We show: {len(roll_deploy)} rows")
# Also check what phase names look like deploy/roll
print("  Checking all phase values containing 'roll' or 'deploy':")
q_rd = f"""
SELECT DISTINCT Phase FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE LOWER(Phase) LIKE '%roll%' OR LOWER(Phase) LIKE '%deploy%'
"""
for row in client.query(q_rd).result():
    print(f"    Phase value: '{row.Phase}'")

# Body Worn Cameras detail
print(f"\n  Looking for 'Body Worn Cameras' / 'Body Wear' detail:")
q_bwc = f"""
SELECT Topic, Phase, Health_Update, Facility, COUNT(*) as row_count
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE LOWER(Topic) LIKE '%body%worn%' OR LOWER(Topic) LIKE '%body%wear%' OR LOWER(Topic) LIKE '%body%cam%'
GROUP BY Topic, Phase, Health_Update, Facility
ORDER BY Facility
"""
bwc_rows = list(client.query(q_bwc).result())
print(f"  Found {len(bwc_rows)} facility rows for Body Worn Cameras")
for row in bwc_rows:
    print(f"    Topic='{row.Topic}', Phase={row.Phase}, Facility={row.Facility}, Health={row.Health_Update}")

# Test phase
print("\n  [Test]")
test = [r for r in dashboard_rows if r.Phase == 'Test']
print(f"  We show: {len(test)} rows")
test_topics = set(r.title for r in test)
print(f"  Unique topics: {len(test_topics)}")
# Check BagMo, Phone Number Capture, Workforce Modernization
for keyword in ['BagMo', 'Phone Number', 'Workforce']:
    print(f"\n  Looking for '{keyword}' across ALL phases:")
    q_k = f"""
    SELECT Topic, Phase, Health_Update, COUNT(DISTINCT Facility) as stores
    FROM `{PROJECT}.{DATASET}.{TABLE}`
    WHERE LOWER(Topic) LIKE '%{keyword.lower()}%'
    GROUP BY Topic, Phase, Health_Update
    """
    for row in client.query(q_k).result():
        print(f"    Topic='{row.Topic}', Phase={row.Phase}, Health={row.Health_Update}, Stores={row.stores}")

# 9. Check: Are there any "Continuous" or "Off Track" values?
print("\n--- 9. CHECKING FOR 'Continuous' AND 'Off Track' VALUES ---")
q9a = f"""
SELECT DISTINCT Phase FROM `{PROJECT}.{DATASET}.{TABLE}` ORDER BY Phase
"""
print("  All Phase values:")
for row in client.query(q9a).result():
    print(f"    '{row.Phase}'")

q9b = f"""
SELECT DISTINCT Health_Update FROM `{PROJECT}.{DATASET}.{TABLE}` ORDER BY Health_Update
"""
print("  All Health_Update values:")
for row in client.query(q9b).result():
    print(f"    '{row.Health_Update}'")

# 10. Store count distribution
print("\n--- 10. STORE COUNT ANALYSIS ---")
q10 = f"""
SELECT 
    Topic,
    Phase,
    COUNT(DISTINCT Facility) as raw_store_count,
    CASE WHEN COUNT(DISTINCT Facility) = 1 THEN 0 ELSE COUNT(DISTINCT Facility) END as display_count
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic IS NOT NULL AND Phase != 'Complete'
GROUP BY Topic, Phase
ORDER BY raw_store_count DESC
"""
print("  Top 20 by store count:")
for i, row in enumerate(client.query(q10).result()):
    if i < 20:
        print(f"    {row.Topic:50s} | Phase: {row.Phase:15s} | Raw: {row.raw_store_count:5d} | Display: {row.display_count}")

print("\n" + "=" * 90)
print("END DIAGNOSTIC REPORT")
print("=" * 90)
