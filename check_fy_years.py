from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check what WM weeks exist for 2026
query = """
SELECT DISTINCT 
    FISCAL_YEAR_NBR, 
    WM_WEEK_NBR,
    MIN(CALENDAR_DATE) as week_start,
    MAX(CALENDAR_DATE) as week_end
FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
WHERE FISCAL_YEAR_NBR IN (2025, 2026)
GROUP BY FISCAL_YEAR_NBR, WM_WEEK_NBR
ORDER BY FISCAL_YEAR_NBR, WM_WEEK_NBR
LIMIT 30
"""

results = list(client.query(query).result())
print("WM Weeks in Cal_Dim_Data:")
for row in results:
    if row.week_start:
        print(f"  FY {row.FISCAL_YEAR_NBR}, WK {row.WM_WEEK_NBR}: {row.week_start} to {row.week_end}")

# Now find what WM week 2026-04-22 belongs to
query2 = """
SELECT DISTINCT 
    CALENDAR_DATE,
    FISCAL_YEAR_NBR,
    WM_WEEK_NBR
FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
WHERE CALENDAR_DATE IN ('2026-04-22', '2026-04-26', '2026-04-27', '2026-05-02')
ORDER BY CALENDAR_DATE
"""

results2 = list(client.query(query2).result())
print("\nSpecific 2026 dates and their WM weeks:")
for row in results2:
    print(f"  {row.CALENDAR_DATE} -> FY {row.FISCAL_YEAR_NBR}, WK {row.WM_WEEK_NBR}")

# Check project update dates to see what they are
query3 = """
SELECT DISTINCT CAST(project_update_date AS DATE) as update_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NOT NULL
ORDER BY update_date DESC
LIMIT 20
"""

results3 = list(client.query(query3).result())
print("\nMost recent project update dates (top 20):")
for row in results3:
    print(f"  {row.update_date}")
