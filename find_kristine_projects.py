#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query for projects with Kristine Torres as SR_DIRECTOR or in any director field
sql = """
SELECT DISTINCT 
  Intake_Card_Nbr,
  Project_Title,
  Business_Owner_Area,
  PROJECT_DIRECTOR,
  PROJECT_SR_DIRECTOR
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE PROJECT_SR_DIRECTOR = 'Kristine Torres' 
  OR PROJECT_DIRECTOR = 'Kristine Torres'
  OR Project_Title LIKE '%Kristine%'
ORDER BY Project_Title
"""

print("Projects with Kristine Torres as director/contact:")
print("="*80)
results = list(client.query(sql).result())
for row in results:
    print(f"ID: {row['Intake_Card_Nbr']} | Title: {row['Project_Title']}")
    print(f"  Director: {row['PROJECT_DIRECTOR']} | SR Director: {row['PROJECT_SR_DIRECTOR']}")
    print()

print(f"\nTotal: {len(results)} projects")
