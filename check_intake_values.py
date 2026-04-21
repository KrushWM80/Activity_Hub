#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

# First check if there are any records
sql = """
SELECT COUNT(*) as cnt, COUNT(DISTINCT Business_Area) as distinct_ba
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
"""

results = client.query(sql).result()
for row in results:
    print(f"Total records: {row.cnt}")
    print(f"Distinct Business_Area values: {row.distinct_ba}")

# Check first 50 Business_Area values
print("\nSample Business_Area values:")
sql2 = """
SELECT DISTINCT Business_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
LIMIT 50
"""

results2 = client.query(sql2).result()
for row in results2:
    print(f"  {repr(row.Business_Area)}")
