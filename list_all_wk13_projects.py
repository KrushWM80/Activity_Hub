from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query all projects with update dates in WM Week 13, FY 2027
query = """
SELECT 
    p.project_id,
    p.title,
    p.owner,
    CAST(p.project_update_date AS DATE) as update_date,
    c.WM_WEEK_NBR,
    c.FISCAL_YEAR_NBR
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` p
INNER JOIN `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data` c
    ON CAST(p.project_update_date AS DATE) = c.CALENDAR_DATE
WHERE c.WM_WEEK_NBR = 13
    AND c.FISCAL_YEAR_NBR = 2027
    AND p.project_update_date IS NOT NULL
ORDER BY p.project_id
"""

results = list(client.query(query).result())

print("=" * 100)
print("ALL Projects with project_update_date in WM Week 13, FY 2027")
print("=" * 100)
print(f"\nTotal: {len(results)} projects\n")

for i, row in enumerate(results, 1):
    print(f"{i}. Project ID: {row.project_id}")
    print(f"   Title: {row.title}")
    print(f"   Owner: {row.owner}")
    print(f"   Update Date: {row.update_date}")
    print(f"   WM Week: {row.WM_WEEK_NBR}, FY: {row.FISCAL_YEAR_NBR}")
    print()

print("=" * 100)
print(f"TOTAL COUNT: {len(results)} project(s) updated in WM Week 13, FY 2027")
print("=" * 100)
