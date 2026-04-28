#!/usr/bin/env python3
from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get schema of AH_Projects
table = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.AH_Projects')
print("=" * 80)
print("AH_Projects Table Schema")
print("=" * 80)
for field in table.schema:
    print(f"{field.name}: {field.field_type}")

print("\n" + "=" * 80)
print("Sample row from AH_Projects")
print("=" * 80)

sql = "SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` LIMIT 1"
results = list(client.query(sql).result())
for row in results:
    print(row)
