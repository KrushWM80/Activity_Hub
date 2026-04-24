from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get Kendall Rush ALL projects including those recently updated
sql = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    health,
    project_update,
    project_update_date,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE owner = 'Kendall Rush'
ORDER BY last_updated DESC
"""

print("ALL Kendall Rush projects (sorted by last_updated):\n")
results = list(client.query(sql).result())
print(f"Total: {len(results)}\n")

for row in results:
    update_date = row.project_update_date.strftime('%Y-%m-%d %H:%M') if row.project_update_date else 'None'
    last_mod = row.last_updated.strftime('%Y-%m-%d %H:%M') if row.last_updated else 'None'
    print(f"Title: {row.title}")
    print(f"  ID: {row.project_id}")
    print(f"  Org: {row.business_organization}")
    print(f"  Last Updated Timestamp: {last_mod}")
    print(f"  Project Update Date: {update_date}")
    print(f"  Project Note: {row.project_update[:60] if row.project_update else 'None'}...")
    print()
