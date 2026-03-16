"""Quick BQ data refresh check"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')
TBL = '`wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`'

t = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report')
print(f"Rows: {t.num_rows}, Modified: {t.modified}")

print(f"\n{'Topic':45s} {'Phase':12s} {'FacPhase':12s} Fac")
print("-" * 78)
q = f"SELECT Topic, Phase, Facility_Phase, Facility FROM {TBL} WHERE Topic IS NOT NULL ORDER BY Phase, Topic LIMIT 40"
for r in client.query(q):
    match = "=" if r.Phase == r.Facility_Phase else " "
    print(f"{str(r.Topic)[:45]:45s} {str(r.Phase):12s} {str(r.Facility_Phase or ''):12s} {r.Facility:>4}{match}")

q2 = f"SELECT COUNT(*) as cnt, SUM(Facility) as total FROM {TBL} WHERE Topic IS NOT NULL AND Facility > 0"
for r in client.query(q2):
    print(f"\nRows with Facility>0: {r.cnt}, Total stores: {r.total}")

q3 = f"SELECT COUNT(*) as cnt, SUM(Facility) as total FROM {TBL} WHERE Topic IS NOT NULL"
for r in client.query(q3):
    print(f"All rows: {r.cnt}, Total Facility sum: {r.total}")

# Distinct phases
q4 = f"SELECT Phase, COUNT(*) as cnt, SUM(Facility) as stores FROM {TBL} WHERE Topic IS NOT NULL GROUP BY Phase ORDER BY Phase"
print(f"\n{'Phase':15s} {'Count':>5s} {'Stores':>6s}")
for r in client.query(q4):
    print(f"{str(r.Phase):15s} {r.cnt:5d} {r.stores:6d}")
