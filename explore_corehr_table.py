#!/usr/bin/env python3
"""
Explore CoreHR UNIFIED_PROFILE_SENSITIVE_VW table structure
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("=" * 80)
print("EXPLORING: wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW")
print("=" * 80)

query = """
SELECT column_name, data_type
FROM `wmt-corehr-prod.US_HUDI.INFORMATION_SCHEMA.COLUMNS`
WHERE table_schema = 'US_HUDI' 
  AND table_name = 'UNIFIED_PROFILE_SENSITIVE_VW'
ORDER BY column_name
"""

print("\nQuery:")
print(query)
print("\nExecuting...")

try:
    results = client.query(query).result(timeout=30)
    
    print(f"\n✅ SUCCESS - Found {results.total_rows} columns\n")
    print("Columns in UNIFIED_PROFILE_SENSITIVE_VW:")
    print("-" * 80)
    
    for row in results:
        print(f"  {row['column_name']:40} | {row['data_type']}")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"\nError Type: {type(e).__name__}")
