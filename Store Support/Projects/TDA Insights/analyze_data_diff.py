import os
from google.cloud import bigquery
from collections import defaultdict

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
c = bigquery.Client(project='wmt-assetprotection-prod')

# Check raw data for key projects
q = """
SELECT Topic, Facility, Phase, Health_Update, Facility_Phase, Intake_Card_Nbr
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Topic IN ('Spill Station Reform', 'Body Worn Cameras', 'Walmart Milk Plant - Georgia')
ORDER BY Topic, Facility
"""
rows = list(c.query(q).result())
print(f"Total raw rows for 3 test projects: {len(rows)}")
for r in rows:
    print(f"  {r.Topic} | Fac={r.Facility} | Phase={r.Phase} | FacPhase={r.Facility_Phase} | CardNbr={r.Intake_Card_Nbr}")

print("\n===== STORE COUNTS: GROUP BY Topic only =====")
q2 = """
SELECT Topic, COUNT(DISTINCT Facility) as store_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Topic IS NOT NULL
GROUP BY Topic
ORDER BY store_count DESC
"""
rows2 = list(c.query(q2).result())
print(f"\nTotal unique Topics: {len(rows2)}")
for r in rows2:
    print(f"  {r.Topic}: {r.store_count} stores")

print("\n===== TOPICS WITH MULTIPLE PHASE/HEALTH COMBOS =====")
q3 = """
SELECT Topic, Phase, Health_Update, COUNT(*) as cnt, COUNT(DISTINCT Facility) as fac_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Topic IS NOT NULL
GROUP BY Topic, Phase, Health_Update
ORDER BY Topic, Phase
"""
rows3 = list(c.query(q3).result())
topic_rows = defaultdict(list)
for r in rows3:
    topic_rows[r.Topic].append((r.Phase, r.Health_Update, r.cnt, r.fac_count))

multi = {t: v for t, v in topic_rows.items() if len(v) > 1}
print(f"\nTopics with multiple Phase/Health combos: {len(multi)}")
for t, combos in sorted(multi.items()):
    print(f"  {t}:")
    for phase, health, cnt, fac in combos:
        print(f"    Phase={phase}, Health={health}, raw_rows={cnt}, distinct_fac={fac}")
