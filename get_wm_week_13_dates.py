from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query the Calendar Dimension table for WM Week 13 dates
query = """
SELECT DISTINCT
    WM_WK as wm_week,
    MIN(CALENDAR_DATE) as week_start,
    MAX(CALENDAR_DATE) as week_end,
    COUNT(DISTINCT CALENDAR_DATE) as days_in_week
FROM `wmt-assetprotection-prod.Store_Support_Dev.CALENDAR_DIM_CUR`
WHERE FY = 2026 
  AND WM_WK = 13
GROUP BY WM_WK
ORDER BY WM_WK
"""

results = list(client.query(query).result())

if results:
    for row in results:
        print(f"WM Week {row.wm_week} (FY 2026):")
        print(f"  Start Date: {row.week_start}")
        print(f"  End Date: {row.week_end}")
        print(f"  Days in Week: {row.days_in_week}")
else:
    print("No Calendar Dimension data found for WM Week 13")
