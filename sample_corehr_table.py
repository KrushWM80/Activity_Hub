#!/usr/bin/env python3
"""
Query CoreHR table with LIMIT to see structure
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("=" * 80)
print("SAMPLING: wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW")
print("=" * 80)

query = """
SELECT *
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
LIMIT 5
"""

print("\nExecuting sample query...\n")

try:
    job_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=100000000  # 100MB
    )
    results = client.query(query, job_config=job_config).result(timeout=30)
    
    print(f"✅ SUCCESS - Query returned {results.total_rows} rows\n")
    
    # Get field names
    if results.schema:
        print("Available columns:")
        print("-" * 80)
        for field in results.schema:
            print(f"  {field.name:40} | {field.field_type}")
        
        print("\n" + "=" * 80)
        print("SAMPLE DATA (first 2 rows):")
        print("=" * 80)
        
        rows = list(results)
        for i, row in enumerate(rows[:2]):
            print(f"\nRow {i+1}:")
            for field in results.schema:
                value = row[field.name]
                if isinstance(value, str) and len(value) > 50:
                    value = value[:47] + "..."
                print(f"  {field.name:40} = {value}")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print(f"\nError Type: {type(e).__name__}")
