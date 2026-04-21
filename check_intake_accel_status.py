#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

# Check Status values
sql = r"""
SELECT DISTINCT Status
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Status IS NOT NULL
ORDER BY Status
"""

print("Distinct Status values:")
results = client.query(sql).result()
for row in results:
    print(f"  '{row.Status}'")

# Check ARCHIVED values
print("\nDistinct ARCHIVED values:")
sql2 = r"""
SELECT DISTINCT ARCHIVED
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
"""

results2 = client.query(sql2).result()
for row in results2:
    print(f"  {row.ARCHIVED}")

# Count by Status and ARCHIVED
print("\nProject counts by Status and ARCHIVED:")
sql3 = r"""
SELECT DISTINCT Intake_Card_Nbr, Status, ARCHIVED
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
ORDER BY Status, ARCHIVED
LIMIT 30
"""

results3 = client.query(sql3).result()
count = 0
for row in results3:
    print(f"  Project {row.Intake_Card_Nbr}: Status='{row.Status}', ARCHIVED={row.ARCHIVED}")
    count += 1
