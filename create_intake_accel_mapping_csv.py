#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
import csv

client = bigquery.Client()

# Query from correct table: Output - Intake Accel Council Data
sql = r"""
SELECT DISTINCT
    Intake_Card_Nbr as Project_ID,
    Project_Title,
    Business_Owner_Area,
    Link
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Title IS NOT NULL
AND TRIM(Project_Title) != ''
AND Intake_Card_Nbr IS NOT NULL
AND Business_Owner_Area IS NOT NULL
AND TRIM(Business_Owner_Area) != ''
AND ARCHIVED = False
ORDER BY Intake_Card_Nbr
"""

print("Fetching ACTIVE projects from 'Output - Intake Accel Council Data'...")
results = client.query(sql).result()

projects_data = []
for row in results:
    project_id = row.Project_ID
    title = row.Project_Title
    business_area = row.Business_Owner_Area if row.Business_Owner_Area else 'Unknown'
    link = row.Link if row.Link else f'https://hoops.wal-mart.com/intake-hub/projects/{project_id}'
    
    projects_data.append({
        'Project_ID': project_id,
        'Project_Title': title,
        'Current_IH_Business_Area': business_area,
        'Updated_Business_Area': business_area,  # Already correct in source table
        'Intake_Hub_URL': link
    })

print(f"Total ACTIVE projects found: {len(projects_data)}")

# Write to CSV
output_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Intake_Hub_Business_Area_Mapping.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Project_ID', 'Project_Title', 'Current_IH_Business_Area', 'Updated_Business_Area', 'Intake_Hub_URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(projects_data)

print(f"✓ CSV file created: {output_path}")
print(f"\nSummary by Business Area:")
print("-" * 80)

# Summary by area
summary = {}
for project in projects_data:
    area = project['Updated_Business_Area']
    summary[area] = summary.get(area, 0) + 1

for area in sorted(summary.keys()):
    print(f"  {area:<50} {summary[area]:>6} projects")

print(f"\nTotal: {len(projects_data)} active projects")
print(f"\nData Source: wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data")
