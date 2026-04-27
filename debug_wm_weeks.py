from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check current WM week from Cal_Dim_Data
query = """
SELECT DISTINCT WM_WEEK_NBR, CALENDAR_DATE
FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
WHERE CALENDAR_DATE = CURRENT_DATE()
"""

results = list(client.query(query).result())
print("Current WM Week from Cal_Dim_Data:")
for row in results:
    print(f"  CURRENT_DATE: WM_WEEK_NBR={row.WM_WEEK_NBR}, CALENDAR_DATE={row.CALENDAR_DATE}")

# Check project update dates and their WM weeks
query2 = """
SELECT 
    CAST(p.project_update_date AS DATE) as update_date,
    c.WM_WEEK_NBR,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` p
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data` c
    ON CAST(p.project_update_date AS DATE) = c.CALENDAR_DATE
WHERE p.project_update_date IS NOT NULL
GROUP BY update_date, WM_WEEK_NBR
ORDER BY update_date DESC
LIMIT 15
"""

results2 = list(client.query(query2).result())
print("\nProject update dates and their WM weeks (top 15):")
for row in results2:
    print(f"  Date: {row.update_date}, WM Week: {row.WM_WEEK_NBR}, Count: {row.count}")
