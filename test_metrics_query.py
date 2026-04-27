from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get current WM week
cal_sql = """
SELECT DISTINCT WM_WEEK_NBR, FISCAL_YEAR_NBR
FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
WHERE CALENDAR_DATE = CURRENT_DATE()
"""
cal_result = list(client.query(cal_sql).result())
if cal_result:
    current_wm_week = cal_result[0].WM_WEEK_NBR
    print(f"Current WM Week: {current_wm_week}")

# Test the exact query
sql = """
SELECT 
    p.project_id,
    CAST(p.project_update_date AS DATE) as update_date,
    p.owner,
    COALESCE(c.WM_WEEK_NBR, NULL) as update_wm_week,
    c.FISCAL_YEAR_NBR
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` p
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data` c
    ON CAST(p.project_update_date AS DATE) = c.CALENDAR_DATE
WHERE p.project_update_date IS NOT NULL
ORDER BY update_date DESC
LIMIT 30
"""

results = list(client.query(sql).result())
print(f"\nProjects with their matched WM weeks (top 30):")
week_13_count = 0
for row in results:
    if row.update_wm_week == current_wm_week:
        week_13_count += 1
        marker = " <-- WK 13"
    else:
        marker = ""
    print(f"  {row.update_date} -> WK {row.update_wm_week}, FY {row.FISCAL_YEAR_NBR}{marker}")

print(f"\nTotal in Week {current_wm_week}: {week_13_count}")
