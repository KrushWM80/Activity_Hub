from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query using Cal_Dim_Data with correct WK 13, FY 2027
query = """
SELECT 
    CAST(p.project_update_date AS DATE) as update_date,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` p
INNER JOIN `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data` c
    ON CAST(p.project_update_date AS DATE) = c.CALENDAR_DATE
    AND c.WM_WEEK_NBR = 13
    AND c.FISCAL_YEAR_NBR = 2027
WHERE p.project_update_date IS NOT NULL
GROUP BY update_date
ORDER BY update_date
"""

results = list(client.query(query).result())

print("Projects with updates in WM Week 13 (FY 2027) using Cal_Dim_Data:")
print("=" * 70)

total_in_wk13 = 0
for row in results:
    print(f"  {row.update_date}: {row.count} projects")
    total_in_wk13 += row.count

print("=" * 70)
print(f"Total projects updated in WM Week 13, FY 2027: {total_in_wk13}")
print(f"Percent of 296 total: {(total_in_wk13 / 296 * 100):.1f}%")
