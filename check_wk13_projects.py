from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get all dates in WM Week 13
query = """
SELECT DISTINCT CALENDAR_DATE
FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
WHERE WM_WEEK_NBR = 13 AND FISCAL_YEAR_NBR = 2026
ORDER BY CALENDAR_DATE
"""

results = list(client.query(query).result())
print("All dates in WM Week 13:")
dates_in_wk13 = []
for row in results:
    print(f"  {row.CALENDAR_DATE}")
    dates_in_wk13.append(row.CALENDAR_DATE)

# Now count projects with update dates in WM Week 13
query2 = """
SELECT 
    CAST(p.project_update_date AS DATE) as update_date,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` p
WHERE CAST(p.project_update_date AS DATE) IN (
    SELECT DISTINCT CALENDAR_DATE
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
    WHERE WM_WEEK_NBR = 13 AND FISCAL_YEAR_NBR = 2026
)
GROUP BY update_date
ORDER BY update_date DESC
"""

results2 = list(client.query(query2).result())
print(f"\nProjects with updates in WM Week 13:")
total_in_wk13 = 0
for row in results2:
    print(f"  Date: {row.update_date}, Count: {row.count}")
    total_in_wk13 += row.count

print(f"\nTotal projects updated in WM Week 13: {total_in_wk13}")
