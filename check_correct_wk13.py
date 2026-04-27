from google.cloud import bigquery
from datetime import date

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check projects with update dates in the correct WM Week 13: 4/25/26 to 5/1/26
query = """
SELECT 
    CAST(project_update_date AS DATE) as update_date,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE CAST(project_update_date AS DATE) BETWEEN DATE('2026-04-25') AND DATE('2026-05-01')
GROUP BY update_date
ORDER BY update_date
"""

results = list(client.query(query).result())
print("Projects with update dates in WM Week 13 (4/25/26 - 5/1/26):")
total_in_wk13 = 0
for row in results:
    print(f"  {row.update_date}: {row.count} projects")
    total_in_wk13 += row.count

print(f"\nTotal projects updated in WM Week 13: {total_in_wk13}")
print(f"Percent of 296 total: {(total_in_wk13 / 296 * 100):.1f}%")
