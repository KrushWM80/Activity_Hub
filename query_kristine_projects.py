#!/usr/bin/env python3
from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query 1: How many projects where Kristine is sr_director or project_director
sql1 = """
SELECT 
    COUNT(*) as total_count,
    COUNTIF(sr_director = 'Kristine Torres') as sr_director_count,
    COUNTIF(project_director = 'Kristine Torres') as project_director_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE sr_director = 'Kristine Torres' OR project_director = 'Kristine Torres'
"""

print("=" * 80)
print("QUERY 1: Kristine's Project Count in AH_Projects")
print("=" * 80)
results1 = list(client.query(sql1).result())
for row in results1:
    print(f"Total Projects: {row.total_count}")
    print(f"  - As Sr Director: {row.sr_director_count}")
    print(f"  - As Project Director: {row.project_director_count}")

# Query 2: Get list of Kristine's projects with all details
sql2 = """
SELECT 
    project_id,
    title,
    owner,
    health,
    status,
    project_director,
    sr_director,
    project_update,
    project_update_date,
    business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE sr_director = 'Kristine Torres' OR project_director = 'Kristine Torres'
ORDER BY title
"""

print("\n" + "=" * 80)
print("QUERY 2: Kristine's Projects from AH_Projects")
print("=" * 80)
results2 = list(client.query(sql2).result())
print(f"Found {len(results2)} projects:\n")

for i, row in enumerate(results2, 1):
    print(f"{i}. {row.title}")
    print(f"   Health: {row.health}, Owner: {row.owner}, Status: {row.status}")
    print(f"   Sr Director: {row.sr_director}, Project Director: {row.project_director}")
    print()

# Query 3: Check the 3 not-updated projects for Kendall - what are their health values?
print("\n" + "=" * 80)
print("QUERY 3: Kendall's 3 Not-Updated Projects (health check)")
print("=" * 80)

sql3 = """
WITH current_week AS (
    SELECT DISTINCT WM_WEEK_NBR, FISCAL_YEAR_NBR
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
    WHERE CALENDAR_DATE = CURRENT_DATE()
    LIMIT 1
)
SELECT 
    ap.project_id,
    ap.title,
    ap.owner,
    ap.health,
    ap.status,
    ap.project_update_date,
    c.WM_WEEK_NBR,
    c.FISCAL_YEAR_NBR
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` ap
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data` c
  ON CAST(ap.project_update_date AS DATE) = c.CALENDAR_DATE
WHERE ap.owner = 'Kendall Rush'
ORDER BY ap.project_update_date, ap.title
"""

results3 = list(client.query(sql3).result())
print(f"All Kendall's projects:\n")
for row in results3:
    week_status = "NOT THIS WEEK" if row.WM_WEEK_NBR != 13 else "THIS WEEK"
    print(f"- {row.title}")
    print(f"  Health: {row.health}, Update Date: {row.project_update_date}")
    print(f"  Status: {week_status} (WM Week {row.WM_WEEK_NBR})")
    print()
