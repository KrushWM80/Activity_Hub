from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query with correct column names
query = """
SELECT DISTINCT
    WM_WEEK_NBR as wm_week,
    MIN(CALENDAR_DATE) as week_start,
    MAX(CALENDAR_DATE) as week_end,
    COUNT(DISTINCT CALENDAR_DATE) as days_in_week,
    FISCAL_YEAR_NBR as fiscal_year
FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
WHERE FISCAL_YEAR_NBR = 2026 
  AND WM_WEEK_NBR = 13
GROUP BY WM_WEEK_NBR, FISCAL_YEAR_NBR
ORDER BY WM_WEEK_NBR
"""

results = list(client.query(query).result())

print("="*80)
print("CORRECT WM WEEK 13 DATES (from Cal_Dim_Data)")
print("="*80 + "\n")

if results:
    for row in results:
        print(f"Fiscal Year: {row.fiscal_year}")
        print(f"WM Week: {row.wm_week}")
        print(f"Week Start: {row.week_start}")
        print(f"Week End: {row.week_end}")
        print(f"Days in Week: {row.days_in_week}")
else:
    print("No data found for WM Week 13, FY 2026")
