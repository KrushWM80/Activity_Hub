from google.cloud import bigquery
import json

client = bigquery.Client(project="athena-gateway-prod")

# Week 7: 2026-02-15 to 2026-02-21 (cumulative through 2026-02-21)
query = """
SELECT 
    COUNT(DISTINCT assignedTo) as distinct_workers,
    COUNT(DISTINCT assignedBy) as distinct_managers,
    COUNT(DISTINCT CASE WHEN status = 'Completed' THEN 1 END) as completions,
    COUNT(*) as total_actions
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate <= '2026-02-21'
"""

print("=" * 70)
print("WEEK 7 CUMULATIVE ENGAGEMENT METRICS (through 2026-02-21)")
print("=" * 70)
print()

try:
    results = client.query(query).result()
    for row in results:
        print(f"Workers (distinct assignedTo):      {row.distinct_workers:,}")
        print(f"Managers (distinct assignedBy):     {row.distinct_managers:,}")
        print(f"Completions (status='Completed'):   {row.completions:,}")
        print(f"Total Actions:                      {row.total_actions:,}")
        print()
        print(f"Total Users (workers + managers):   {row.distinct_workers + row.distinct_managers:,}")
        print(f"Actions per User:                   {row.total_actions / (row.distinct_workers + row.distinct_managers):.1f}")
        print()
        print("-" * 70)
        print()
        
except Exception as e:
    print(f"Error: {e}")

print("Query complete.")
