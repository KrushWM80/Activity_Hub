"""Quick check: what TDA_Ownership values exist in BigQuery right now?"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
from google.cloud import bigquery
c = bigquery.Client(project='wmt-assetprotection-prod')

q = """
SELECT DISTINCT TDA_Ownership, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
GROUP BY TDA_Ownership
ORDER BY cnt DESC
"""
print("Current TDA_Ownership values:")
for r in c.query(q).result():
    print(f"  {str(r.TDA_Ownership):30s} => {r.cnt} rows")

print("\nTotal rows:")
q2 = "SELECT COUNT(*) as total FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`"
for r in c.query(q2).result():
    print(f"  {r.total}")
