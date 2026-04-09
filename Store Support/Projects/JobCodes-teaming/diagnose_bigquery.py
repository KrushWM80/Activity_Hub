"""
Diagnostic script to test BigQuery connection and query execution
"""

from google.cloud import bigquery
import sys
import traceback

print("=" * 80)
print("BIGQUERY DIAGNOSTIC")
print("=" * 80)

try:
    print("\n1. Initializing BigQuery client...")
    client = bigquery.Client()
    print("   ✓ Client initialized")
except Exception as e:
    print(f"   ✗ Failed to initialize client: {e}")
    sys.exit(1)

try:
    print("\n2. Getting project and datasets...")
    project = client.project
    print(f"   ✓ Project: {project}")
    
    datasets = list(client.list_datasets(max_results=5))
    print(f"   ✓ Found {len(datasets)} datasets (showing first 5):")
    for ds in datasets:
        print(f"      - {ds.project}.{ds.dataset_id}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    traceback.print_exc()

try:
    print("\n3. Checking Polaris dataset...")
    dataset = client.get_dataset("polaris-analytics-prod.us_walmart")
    print(f"   ✓ Found dataset: {dataset.project}.{dataset.dataset_id}")
    
    tables = list(client.list_tables(dataset, max_results=10))
    print(f"   ✓ Found {len(tables)} tables in dataset:")
    for table in tables[:5]:
        print(f"      - {table.table_id}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    traceback.print_exc()

try:
    print("\n4. Testing simple COUNT query on Polaris...")
    query = """
    SELECT COUNT(*) as row_count
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    LIMIT 1
    """
    print(f"   Query: {query.strip()}")
    print("   Executing...")
    
    job = client.query(query, job_config=bigquery.QueryJobConfig(
        maximum_bytes_billed=10_000_000
    ))
    result = job.result(timeout=30)  # 30 second timeout
    
    for row in result:
        print(f"   ✓ Query successful! Row count: {row.row_count}")
except Exception as e:
    print(f"   ✗ Query failed: {e}")
    traceback.print_exc()

try:
    print("\n5. Testing WHERE clause with 30-second timeout...")
    query = """
    SELECT DISTINCT win_nbr
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE win_nbr = 219251625
    LIMIT 10
    """
    print("   Executing...")
    
    job = client.query(query, job_config=bigquery.QueryJobConfig(
        maximum_bytes_billed=100_000_000
    ))
    result = job.result(timeout=30)  # 30 second timeout
    
    rows = list(result)
    if rows:
        print(f"   ✓ Found {len(rows)} records:")
        for row in rows:
            print(f"      WIN: {row.win_nbr}")
    else:
        print(f"   ⚠ No records found (but query succeeded)")
except Exception as e:
    print(f"   ✗ Query failed (might be timeout or data issue): {e}")
    traceback.print_exc()

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
