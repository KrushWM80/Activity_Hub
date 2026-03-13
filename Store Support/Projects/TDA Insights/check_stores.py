"""Quick store count check"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
from google.cloud import bigquery
c = bigquery.Client(project='wmt-assetprotection-prod')
q = "SELECT SUM(Facility) as s, COUNT(*) as n, SUM(CASE WHEN Facility>0 THEN 1 ELSE 0 END) as has_val FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` WHERE Topic IS NOT NULL"
for r in c.query(q).result():
    print(f"Total rows: {r.n}, SUM all facilities: {r.s}, Rows with value>0: {r.has_val}")
