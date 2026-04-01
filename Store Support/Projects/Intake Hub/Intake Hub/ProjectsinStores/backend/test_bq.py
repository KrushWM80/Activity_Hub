"""Test BigQuery connectivity"""
from google.cloud import bigquery

print("Testing BigQuery connection...\n")

client = bigquery.Client(project="wmt-assetprotection-prod")

# Simple test query
query = "SELECT COUNT(*) as cnt FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` WHERE Project_Source = 'Realty'"

print(f"Running: {query}\n")

try:
    result = client.query(query, timeout=30).result(timeout=30)
    row = list(result)[0]
    print(f"✓ BigQuery is working!")
    print(f"  Realty records in source: {row.cnt}\n")
except Exception as e:
    print(f"❌ BigQuery query failed:")
    print(f"  {type(e).__name__}: {e}")
