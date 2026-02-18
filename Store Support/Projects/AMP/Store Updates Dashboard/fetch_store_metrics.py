#!/usr/bin/env python3
"""
Store Metrics Aggregation from BigQuery
Fetches store-level event counts and calculates Store High/Low/Avg
"""

from google.cloud import bigquery
import json

# Initialize BigQuery client
client = bigquery.Client(project='wmt-assetprotection-prod')

# Query to get store-level metrics
query = """
WITH store_event_summary AS (
  SELECT
    store,
    wm_week,
    fy,
    COUNT(DISTINCT event_id) as event_count
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
  WHERE CAST(fy AS INT64) = 2027 
    AND CAST(wm_week AS INT64) = 2
    AND store IS NOT NULL
  GROUP BY store, wm_week, fy
)
SELECT
  wm_week,
  fy,
  MAX(event_count) as store_high,
  MIN(event_count) as store_low,
  ROUND(AVG(event_count), 2) as store_avg,
  COUNT(DISTINCT store) as total_unique_stores,
  SUM(event_count) as total_store_event_touchpoints
FROM store_event_summary
GROUP BY wm_week, fy
"""

print("Querying BigQuery for store-level metrics...")
print("Table: wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2")
print("Filter: WM Week 2, FY 2027\n")

try:
    query_job = client.query(query)
    results = query_job.result()
    
    # Extract the first (and only) row
    row = next(results, None)
    
    if row is None:
        print("❌ No results returned from query")
        print("This may indicate no data for WM Week 2, FY 2027")
        exit(1)
    
    metrics = {
        'wm_week': int(row['wm_week']) if row['wm_week'] else 2,
        'fy': int(row['fy']) if row['fy'] else 2027,
        'store_high': int(row['store_high']) if row['store_high'] else 0,
        'store_low': int(row['store_low']) if row['store_low'] else 0,
        'store_avg': float(row['store_avg']) if row['store_avg'] else 0.0,
        'total_unique_stores': int(row['total_unique_stores']) if row['total_unique_stores'] else 0,
        'total_store_event_touchpoints': int(row['total_store_event_touchpoints']) if row['total_store_event_touchpoints'] else 0
    }
    
    print("=" * 70)
    print("STORE-LEVEL METRICS (WM Week 2, FY 2027)")
    print("=" * 70)
    print(f"Store High (max events per store):     {metrics['store_high']}")
    print(f"Store Low (min events per store):      {metrics['store_low']}")
    print(f"Store Avg (avg events per store):      {metrics['store_avg']}")
    print(f"Total Unique Stores:                   {metrics['total_unique_stores']}")
    print(f"Total Store-Event Touchpoints:         {metrics['total_store_event_touchpoints']}")
    print("=" * 70)
    
    # Save to JSON for dashboard integration
    output_file = r'c:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard\store_metrics.json'
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n✓ Metrics saved to: store_metrics.json")
    print(f"\nUpdate the dashboard with:")
    print(f"  Store High: {metrics['store_high']}")
    print(f"  Store Low:  {metrics['store_low']}")
    print(f"  Store Avg:  {metrics['store_avg']}")
    
except StopIteration:
    print("❌ No results returned from query")
    print("This may indicate no data for WM Week 2, FY 2027")
    exit(1)
except Exception as e:
    print(f"❌ Error executing query: {str(e)}")
    import traceback
    traceback.print_exc()
    print("\nPlease ensure:")
    print("  1. BigQuery credentials are configured (gcloud auth application-default login)")
    print("  2. You have access to wmt-assetprotection-prod project")
    print("  3. The table 'Output - AMP ALL 2' exists in Store_Support_Dev dataset")
    exit(1)
