#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

# Get schema of IH_Intake_Data
print("Schema of IH_Intake_Data table:")
print("=" * 80)

dataset_id = "Store_Support_Dev"
table_id = "IH_Intake_Data"

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
table = client.get_table(table_ref)

for field in table.schema:
    print(f"  {field.name:40} {field.field_type}")
