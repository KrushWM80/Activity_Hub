#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

print("=" * 100)
print("INTAKE HUB: Business Areas with Project Counts")
print("=" * 100)

sql = """
SELECT Business_Area, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Business_Area IS NOT NULL
AND TRIM(Business_Area) != ''
GROUP BY Business_Area
ORDER BY cnt DESC
LIMIT 50
"""

results = client.query(sql).result()
print(f"\n{'Business Area':<50} {'Count':>8}")
print("-" * 100)
for row in results:
    print(f"{row.Business_Area:<50} {row.cnt:>8}")
