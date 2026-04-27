from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get the most recent last_updated timestamp from AH_Projects
query = """
SELECT 
    MAX(last_updated) as latest_sync_time,
    MAX(created_date) as latest_created_date,
    COUNT(*) as total_projects,
    COUNT(DISTINCT owner) as unique_owners
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
"""

results = list(client.query(query).result())
row = results[0] if results else None

print("=" * 80)
print("AH_Projects Sync Status")
print("=" * 80)

if row:
    latest_sync = row.latest_sync_time
    latest_created = row.latest_created_date
    
    print(f"\nLatest Sync/Update Time: {latest_sync}")
    if latest_sync:
        now = datetime.utcnow()
        time_diff = now - latest_sync.replace(tzinfo=None)
        hours_ago = time_diff.total_seconds() / 3600
        print(f"Time Elapsed: {hours_ago:.1f} hours ago ({time_diff})")
    
    print(f"\nLatest Project Created: {latest_created}")
    print(f"\nTotal Projects: {row.total_projects}")
    print(f"Unique Owners: {row.unique_owners}")
else:
    print("No data found")

print("\n" + "=" * 80)
print("Recent Updates Distribution")
print("=" * 80)

# Get distribution of updates by date
dist_query = """
SELECT 
    CAST(last_updated AS DATE) as update_date,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE last_updated IS NOT NULL
GROUP BY update_date
ORDER BY update_date DESC
LIMIT 10
"""

dist_results = list(client.query(dist_query).result())
print("\nLast 10 update dates:")
for row in dist_results:
    print(f"  {row.update_date}: {row.count} projects")
