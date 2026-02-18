#!/usr/bin/env python3
"""
Query BigQuery for store-level (Facility) activity counts
Groups by Facility (Store), Week, FY and counts distinct Activity_IDs
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='wmt-assetprotection-prod')

query = """
SELECT DISTINCT Facility, Week, FY, Count(Activity_ID) as activity_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2` 
WHERE CAST(FY AS STRING) = '2027'
  AND CAST(Week AS STRING) = '2'
  AND Facility IS NOT NULL
GROUP BY Facility, Week, FY
ORDER BY activity_count DESC
"""

print("Querying BigQuery for store-level activity counts...")
print("Query: Count distinct Activity_IDs per Facility (Store)")
print("Filter: Week 2, FY 2027\n")

try:
    results = client.query(query).result()
    
    activity_counts = []
    row_count = 0
    
    print("Processing results...")
    for row in results:
        activity_counts.append(int(row['activity_count']))
        row_count += 1
        if row_count <= 5:
            print(f"  Facility: {row['Facility']}, Activity Count: {row['activity_count']}")
    
    if not activity_counts:
        print("❌ No results returned")
        exit(1)
    
    # Calculate metrics
    store_high = max(activity_counts)
    store_low = min(activity_counts)
    store_avg = sum(activity_counts) / len(activity_counts)
    total_stores = len(activity_counts)
    total_activity_touchpoints = sum(activity_counts)
    
    print(f"  ... and {row_count - 5} more stores\n")
    
    metrics = {
        'wm_week': 2,
        'fy': 2027,
        'store_high': store_high,
        'store_low': store_low,
        'store_avg': round(store_avg, 2),
        'total_unique_stores': total_stores,
        'total_activity_touchpoints': total_activity_touchpoints
    }
    
    print("=" * 70)
    print("STORE-LEVEL ACTIVITY METRICS (WM Week 2, FY 2027)")
    print("=" * 70)
    print(f"Store High (max activities per store): {metrics['store_high']}")
    print(f"Store Low (min activities per store):  {metrics['store_low']}")
    print(f"Store Avg (avg activities per store):  {metrics['store_avg']}")
    print(f"Total Unique Stores:                   {metrics['total_unique_stores']}")
    print(f"Total Activity-Store Touchpoints:      {metrics['total_activity_touchpoints']}")
    print("=" * 70)
    
    # Save to JSON
    output_file = r'c:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard\store_metrics.json'
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n✓ Metrics saved to store_metrics.json")
    print(f"\nUpdate the dashboard with:")
    print(f"  Store High: {metrics['store_high']}")
    print(f"  Store Low:  {metrics['store_low']}")
    print(f"  Store Avg:  {metrics['store_avg']}")
    
except Exception as e:
    print(f"❌ Error executing query: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
