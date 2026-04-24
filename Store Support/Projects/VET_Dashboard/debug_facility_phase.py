"""Debug: check what Facility_Phase values exist in BQ"""
from google.cloud import bigquery
import os, json

creds = os.path.join(os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json')
if os.path.exists(creds):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds

client = bigquery.Client(project='wmt-assetprotection-prod')

# 1) Check distinct Facility_Phase values
print("=== Distinct Phase / Facility_Phase combos ===")
q1 = """
SELECT DISTINCT Phase, Facility_Phase, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE TDA_Ownership = 'Dallas VET'
GROUP BY Phase, Facility_Phase
ORDER BY Phase, Facility_Phase
"""
for row in client.query(q1).result():
    print(f"  Phase={row.Phase!r:20s}  Facility_Phase={row.Facility_Phase!r:20s}  count={row.cnt}")

# 2) Check a sample row from our actual query
print("\n=== Sample rows from actual query ===")
q2 = """
SELECT
    tda.Topic,
    tda.Phase,
    tda.Facility_Phase,
    tda.Impl_Date,
    tda.Facility
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` tda
WHERE tda.TDA_Ownership = 'Dallas VET'
LIMIT 10
"""
for row in client.query(q2).result():
    print(f"  Topic={row.Topic!r:40s}  Phase={row.Phase!r:15s}  FacPhase={row.Facility_Phase!r:15s}  Impl={row.Impl_Date}  Facility={row.Facility}")
