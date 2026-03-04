"""
Search for Area/Topic metadata in BigQuery
"""
from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

# List all tables in the store_refresh dataset
query = """
SELECT table_name, table_type
FROM `athena-gateway-prod.store_refresh.INFORMATION_SCHEMA.TABLES`
ORDER BY table_name
"""

print("📋 All tables in store_refresh dataset:")
results = client.query(query).result()

for row in results:
    table_name = row['table_name']
    table_type = row['table_type']
    print(f"  - {table_name} ({table_type})")

# Also check other datasets
print("\n📦 Available datasets in athena-gateway-prod project:")
datasets_query = """
SELECT schema_name
FROM `athena-gateway-prod.INFORMATION_SCHEMA.SCHEMATA`
ORDER BY schema_name
"""

ds_results = client.query(datasets_query).result()
for row in ds_results:
    print(f"  - {row['schema_name']}")

# Try to inspect backup table mentioned in docs
print("\n🔍 Checking for backup/reference tables...")
try:
    tables_in_dev = client.list_tables('wmt-assetprotection-prod.Store_Support_Dev')
    print("\n📋 Tables in wmt-assetprotection-prod.Store_Support_Dev:")
    for table in tables_in_dev:
        print(f"  - {table.table_id}")
        
        # Try to get schema for each
        try:
            full_table_id = f"{table.project}.{table.dataset_id}.{table.table_id}"
            t = client.get_table(full_table_id)
            print(f"    Columns: {', '.join([f.name for f in t.schema])}")
        except Exception as e:
            print(f"    (cannot access schema)")
except Exception as e:
    print(f"  Error accessing backup project: {e}")

print("\n✓ Discovery complete")
