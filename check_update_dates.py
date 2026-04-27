from google.cloud import bigquery
from datetime import datetime, timedelta

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get today's date and calculate current Walmart week
today = datetime.now()
fiscal_year_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
days_since_fy = (today - fiscal_year_start).days
current_wm_week = (days_since_fy // 7) + 1

print(f"Today: {today.date()}")
print(f"Current WM Week: {current_wm_week}")
print(f"FY Start: {fiscal_year_start.date()}\n")

# Check total projects
count_query = """
SELECT COUNT(*) as total FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
"""
total = list(client.query(count_query).result())[0].total
print(f"Total Projects: {total}\n")

# Check projects with no update date
no_update = """
SELECT COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NULL
"""
no_update_count = list(client.query(no_update).result())[0].count
print(f"Projects with NO update date: {no_update_count}")

# Check projects with recent update (this week)
# Get a sample of projects with their update dates
sample_query = """
SELECT 
    project_id,
    title,
    owner,
    project_update_date,
    last_updated,
    CASE 
        WHEN project_update_date IS NULL THEN 'No update date'
        ELSE 'Has update date'
    END as status
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
ORDER BY project_update_date DESC
LIMIT 20
"""

results = list(client.query(sample_query).result())
print(f"\nSample of projects (top 20 by update_date):\n")
for row in results:
    print(f"  {row.title[:40]:40} | {row.owner[:20]:20} | Update: {row.project_update_date} | Status: {row.status}")

# Find projects with NO update at all
no_update_projects = """
SELECT 
    project_id,
    title,
    owner,
    project_update_date,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NULL OR TRIM(project_update_date) = ''
ORDER BY project_id
"""

no_update_results = list(client.query(no_update_projects).result())
print(f"\n\nProjects with NO update_date ({len(no_update_results)} total):\n")
for row in no_update_results[:5]:  # Show first 5
    print(f"  {row.title[:50]:50} | Owner: {row.owner}")
if len(no_update_results) > 5:
    print(f"  ... and {len(no_update_results) - 5} more")
