from google.cloud import bigquery
from datetime import datetime, timedelta

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query to check sync timing
print("="*80)
print("INTAKE HUB -> AH_PROJECTS SYNC STATUS")
print("="*80)

# Check when sync_now.py last ran (check log or query for recent updates)
# Since we don't have a sync log table, check the most recent project_update_date in AH_Projects
recent_query = """
SELECT 
    MAX(project_update_date) as most_recent_update,
    MIN(project_update_date) as oldest_update,
    COUNT(*) as total_with_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NOT NULL
"""

result = list(client.query(recent_query).result())[0]
print(f"\nMost Recent project_update_date in AH_Projects: {result.most_recent_update}")
print(f"Oldest project_update_date in AH_Projects: {result.oldest_update}")
print(f"Total projects with update_date: {result.total_with_date}")

# Now check projects with update dates BEFORE 4/25/26
print("\n" + "="*80)
print("PROJECTS WITH UPDATE DATE BEFORE 4/25/2026 (Stale Updates)")
print("="*80)

stale_query = """
SELECT 
    project_id,
    title,
    owner,
    project_update_date,
    project_update_by,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), project_update_date, DAY) as days_since_update
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NOT NULL 
AND DATE(project_update_date) < '2026-04-25'
ORDER BY project_update_date DESC
LIMIT 20
"""

stale_results = list(client.query(stale_query).result())
if stale_results:
    print(f"\nFound {len(stale_results)} projects with stale updates (before 4/25/26):\n")
    for i, row in enumerate(stale_results, 1):
        print(f"  [{i}] {row.title[:50]:50} | {row.owner[:20]:20}")
        print(f"      Update Date: {row.project_update_date.date() if row.project_update_date else 'NULL'} ({row.days_since_update} days ago)")
        print(f"      Updated By: {row.project_update_by}\n")
else:
    print("\n✓ No projects with stale updates (all are recent)")

# Check projects updated in WM Week 13 (4/21 - 4/27)
print("\n" + "="*80)
print("PROJECTS UPDATED IN WM WEEK 13 (4/21 - 4/27/2026)")
print("="*80)

wk13_query = """
SELECT 
    COUNT(*) as count,
    MIN(project_update_date) as earliest,
    MAX(project_update_date) as latest
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE DATE(project_update_date) BETWEEN '2026-04-21' AND '2026-04-27'
"""

wk13_result = list(client.query(wk13_query).result())[0]
print(f"\nProjects updated during WM13: {wk13_result.count}")
print(f"Earliest update in WK13: {wk13_result.earliest}")
print(f"Latest update in WK13: {wk13_result.latest}")

# Summary
print("\n" + "="*80)
print("SYNC STATUS SUMMARY")
print("="*80)
print(f"\nTotal Projects: 296")
print(f"  - With project_update_date: {result.total_with_date} (Updated)")
print(f"  - NULL project_update_date: {296 - result.total_with_date} (Not Updated)")
print(f"\nSync Frequency: Every 30 minutes (via sync_now.py)")
print(f"Last Known Sync: Most recent update was on {result.most_recent_update.date() if result.most_recent_update else 'Unknown'}")
print(f"\nProjects with stale updates (before 4/25): {len(stale_results)}")
print(f"Projects updated in WK13 (4/21-4/27): {wk13_result.count}")
