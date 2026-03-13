"""Quick diagnostic: Test phase, Checkout Anywhere, Facility analysis"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')
P = 'wmt-assetprotection-prod'
D = 'Store_Support_Dev'
T = 'Output- TDA Report'

print("=== TEST PHASE TOPICS ===")
q = f"SELECT Topic, Health_Update, COUNT(*) as row_cnt, COUNT(DISTINCT Facility) as dist_fac, SUM(Facility) as sum_fac FROM `{P}.{D}.{T}` WHERE Phase = 'Test' AND Topic IS NOT NULL GROUP BY Topic, Health_Update ORDER BY Topic"
for r in client.query(q).result():
    print(f"  {str(r.Topic):<50} Health={str(r.Health_Update):<12} Rows={r.row_cnt} Distinct={r.dist_fac} Sum={r.sum_fac}")

print("\n=== CHECKOUT ANYWHERE DETAIL ===")
q2 = f"SELECT * FROM `{P}.{D}.{T}` WHERE Topic = 'Checkout Anywhere'"
for r in client.query(q2).result():
    d = dict(r)
    for k, v in d.items():
        print(f"  {k}: {v}")

print("\n=== FACILITY NULL/ZERO ANALYSIS ===")
q3 = f"SELECT COUNT(*) as total, SUM(CASE WHEN Facility IS NULL OR Facility = 0 THEN 1 ELSE 0 END) as null_or_zero, SUM(CASE WHEN Facility > 0 THEN 1 ELSE 0 END) as has_value FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL"
for r in client.query(q3).result():
    print(f"  Total rows: {r.total}, NULL/Zero: {r.null_or_zero}, Has value: {r.has_value}")

print("\n=== STORE COUNT COMPARISON: COUNT(DISTINCT) vs SUM for topics with stores ===")
q4 = f"SELECT Topic, Phase, COUNT(DISTINCT Facility) as count_distinct, SUM(Facility) as sum_facility FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL AND Facility > 0 GROUP BY Topic, Phase HAVING SUM(Facility) > 0 ORDER BY sum_facility DESC"
for r in client.query(q4).result():
    print(f"  {str(r.Topic):<50} Phase={str(r.Phase):<12} COUNT_DISTINCT={r.count_distinct:<6} SUM={r.sum_facility}")

print("\nDone!")
