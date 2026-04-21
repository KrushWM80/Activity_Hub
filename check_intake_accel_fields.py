#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

# Check what fields we can use to identify projects
sql = r"""
SELECT DISTINCT Intake_Card_Nbr, Link
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr IS NOT NULL
LIMIT 10
"""

try:
    results = client.query(sql).result()
    print("Sample Intake Card Numbers and Links:")
    for row in results:
        print(f"  Card: {row.Intake_Card_Nbr}, Link: {row.Link}")
except Exception as e:
    print(f"Error: {e}")

# Check Business_Owner_Area values
print("\n\nDistinct Business_Owner_Area values:")
sql2 = r"""
SELECT DISTINCT Business_Owner_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Business_Owner_Area IS NOT NULL
ORDER BY Business_Owner_Area
"""

try:
    results2 = client.query(sql2).result()
    for row in results2:
        print(f"  {row.Business_Owner_Area}")
except Exception as e:
    print(f"Error: {e}")
