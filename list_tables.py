from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# List all tables in the dataset
print("Listing all tables in Store_Support_Dev dataset:\n")

dataset_id = 'Store_Support_Dev'
dataset_ref = client.dataset(dataset_id, project='wmt-assetprotection-prod')
tables = client.list_tables(dataset_ref)

print("Available tables:")
for table in tables:
    print(f"  - {table.table_id}")
