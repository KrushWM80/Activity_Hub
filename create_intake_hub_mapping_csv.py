#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
import csv

client = bigquery.Client()

# Define the mapping from all 60 Intake Hub areas to the 12 target areas
BUSINESS_AREA_MAPPING = {
    # Compliance & Safety Group
    'Compliance': 'Compliance',
    'Compliance/Legal': 'Compliance',
    'Safety': 'Safety',
    'Safety  & Asset Protection': 'Safety',
    'Asset Protection': 'Compliance',
    
    # People & Training Group
    'People': 'People',
    'US People': 'People',
    'Workforce Management': 'People',
    'Academy/Training': 'People',
    
    # Realty Group
    'Realty': 'Realty',
    
    # Supply Chain & Logistics Group
    'Supply Chain': 'Supply Chain',
    'Supply Chain Maintenance': 'Supply Chain',
    'Logistics': 'Supply Chain',
    'Transportation Operations': 'Supply Chain',
    'Flow': 'Supply Chain',
    
    # Fulfillment Group
    'Store Fulfillment': 'Store Fulfillment',
    'Fulfillment Operations': 'Store Fulfillment',
    'Fulfillment Operations Support': 'Store Fulfillment',
    
    # Operations Strategy & Support Group (Large catchall for most ops)
    'Operations Strategy & Support': 'Operations Strategy & Support',
    'Ops Support': 'Operations Strategy & Support',
    'Ops A&S Backroom/Claims': 'Operations Strategy & Support',
    'Ops A&S Digital': 'Operations Strategy & Support',
    'Ops A&S Front End': 'Operations Strategy & Support',
    'Ops A&S GM Salesfloor': 'Operations Strategy & Support',
    'Ops A&S Grocery Salesfloor': 'Operations Strategy & Support',
    'Ops A&S WMT Services': 'Operations Strategy & Support',
    'Ops Backroom & Claims': 'Operations Strategy & Support',
    'Ops Business Community': 'Operations Strategy & Support',
    'Ops Digital': 'Operations Strategy & Support',
    'Ops Food & Consumables': 'Operations Strategy & Support',
    'Ops Fresh': 'Operations Strategy & Support',
    'Ops Front End': 'Operations Strategy & Support',
    'Ops Hardlines & ACC': 'Operations Strategy & Support',
    'Ops Homelines': 'Operations Strategy & Support',
    'Ops Seasonal & Entertainment': 'Operations Strategy & Support',
    'Ops WMT Services': 'Operations Strategy & Support',
    'Ops Apparel': 'Operations Strategy & Support',
    'Store Ops': 'Operations Strategy & Support',
    'Ambient Operations Support': 'Operations Strategy & Support',
    'Grocery Operations Support': 'Operations Strategy & Support',
    'Maintenance': 'Operations Strategy & Support',
    'Retail Services': 'Operations Strategy & Support',
    
    # E2E Strategy Group
    'E2E Strategy': 'E2E Strategy',
    'Transformation Strategy': 'Transformation Strategy',
    'Engineering': 'Transformation Strategy',
    'Product': 'Transformation Strategy',
    'Product and Technology': 'Transformation Strategy',
    'Strategic Program Management': 'Transformation Strategy',
    
    # Marketing & Merchandising Group
    'Marketing': 'Marketing',
    'Merchandising': 'Merchandising',
    'Merchant': 'Merchandising',
    
    # Health & Wellness Group
    'Health & Wellness': 'Health & Wellness',
    
    # Other/Misc (map to closest)
    'Enterprise Returns': 'Operations Strategy & Support',
    'LMDS': 'Supply Chain',
    'GBS': 'Operations Strategy & Support',
    'Supplies': 'Operations Strategy & Support',
    'Foundation': 'People',
    'Utilities': 'Operations Strategy & Support',
    'Pharmacy': 'Health & Wellness',
}

# Query Intake Hub projects
sql = """
SELECT 
    PROJECT_ID,
    Title,
    Business_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Title IS NOT NULL
AND TRIM(Title) != ''
AND PROJECT_ID IS NOT NULL
ORDER BY PROJECT_ID
"""

print("Fetching projects from Intake Hub...")
results = client.query(sql).result()

projects_data = []
for row in results:
    project_id = row.PROJECT_ID
    title = row.Title
    current_ba = row.Business_Area if row.Business_Area else 'Unknown'
    
    # Map to new business area
    updated_ba = BUSINESS_AREA_MAPPING.get(current_ba, 'Operations Strategy & Support')
    
    # Build Intake Hub URL (assuming project link structure)
    # Standard format: https://hoops.wal-mart.com/intake-hub/projects/{PROJECT_ID}
    intake_url = f"https://hoops.wal-mart.com/intake-hub/projects/{project_id}"
    
    projects_data.append({
        'Project_ID': project_id,
        'Project_Title': title,
        'Current_IH_Business_Area': current_ba,
        'Updated_Business_Area': updated_ba,
        'Intake_Hub_URL': intake_url
    })

print(f"Total projects found: {len(projects_data)}")

# Write to CSV
output_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Intake_Hub_Business_Area_Mapping.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Project_ID', 'Project_Title', 'Current_IH_Business_Area', 'Updated_Business_Area', 'Intake_Hub_URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(projects_data)

print(f"\n✓ CSV file created: {output_path}")
print(f"\nSummary by Updated Business Area:")
print("-" * 80)

# Summary by updated area
summary = {}
for project in projects_data:
    area = project['Updated_Business_Area']
    summary[area] = summary.get(area, 0) + 1

for area in sorted(summary.keys()):
    print(f"  {area:<40} {summary[area]:>6} projects")

print(f"\nTotal: {len(projects_data)} projects")
