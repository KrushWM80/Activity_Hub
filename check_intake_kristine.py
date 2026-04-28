#!/usr/bin/env python3
from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get schema of Intake Hub source table
table = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data')
print("=" * 80)
print("Intake Hub Source Table Schema")
print("=" * 80)
for field in table.schema:
    print(f"{field.name}: {field.field_type}")

print("\n" + "=" * 80)
print("Projects where Kristine Torres is SR_DIRECTOR")
print("=" * 80)

sql = """
SELECT 
    Intake_Card_Nbr,
    Project_Title,
    Owner,
    PROJECT_SR_DIRECTOR,
    PROJECT_DIRECTOR,
    Health_Update,
    Project_Update_Date
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE PROJECT_SR_DIRECTOR = 'Kristine Torres'
ORDER BY Project_Title
"""

results = list(client.query(sql).result())
print(f"Found {len(results)} projects where Kristine is SR_DIRECTOR\n")

for i, row in enumerate(results[:10], 1):  # Show first 10
    print(f"{i}. {row.Project_Title}")
    print(f"   Health: {row.Health_Update}, Owner: {row.Owner}")
    print(f"   Director: {row.PROJECT_DIRECTOR}")
    print()

if len(results) > 10:
    print(f"... and {len(results) - 10} more projects")
