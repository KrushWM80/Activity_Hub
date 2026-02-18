#!/usr/bin/env python3
"""
Check available WM_Week and FY values in BigQuery AMP table
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query to find available weeks and years
query = """
SELECT DISTINCT
  wm_week,
  fy,
  COUNT(*) as record_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE wm_week IS NOT NULL AND fy IS NOT NULL
GROUP BY wm_week, fy
ORDER BY fy DESC, CAST(wm_week AS INT64) DESC
LIMIT 20
"""

print("Checking available Week/FY combinations in BigQuery...\n")

try:
    results = client.query(query).result()
    
    print("Available Data:")
    print("-" * 50)
    for row in results:
        print(f"  Week: {row['wm_week']:<5} | FY: {row['fy']:<6} | Records: {row['record_count']}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
