"""
Check Polaris table schema
"""
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get schema
table = client.get_table('polaris-analytics-prod.us_walmart.vw_polaris_current_schedule')

print("Polaris Current Schedule - Available Columns:")
print("="*80)
for schema_field in table.schema:
    print(f"  - {schema_field.name:30} ({schema_field.field_type})")

# Get sample row
print("\n\nSample row with store/location fields:")
print("="*80)
q = """
SELECT * 
FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
LIMIT 1
"""
row = list(client.query(q).result())[0]

for k, v in row.items():
    if v and ('location' in k.lower() or 'store' in k.lower() or 'win' in k.lower() or 'email' in k.lower() or 'user' in k.lower()):
        print(f"  {k:30} = {v}")
