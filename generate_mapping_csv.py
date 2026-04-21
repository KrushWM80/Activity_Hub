#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
import csv
from datetime import datetime

client = bigquery.Client()

# Define the business area mapping
# Current Projects areas → New Intake Hub areas
mapping = {
    'Automotive': 'Operations Strategy & Support',
    'Ecommerce & Digital': 'E2E Strategy',
    'General Merchandise': 'Merchandising',
    'Grocery & Fresh': 'Operations Strategy & Support',
    'Risk & Compliance': 'Compliance',
    'Store Operations': 'Operations Strategy & Support',
    'Supply Chain': 'Supply Chain'
}

print("Business Area Mapping:")
print("=" * 80)
for old, new in mapping.items():
    print(f"  {old:30} → {new}")
print("=" * 80)

# Query all projects
sql = """
SELECT 
    project_id,
    title,
    business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE title IS NOT NULL AND TRIM(title) != ''
ORDER BY business_organization, title
"""

results = client.query(sql).result()

# Generate CSV
csv_filename = "Projects_BusinessArea_Mapping.csv"
csv_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

with open(os.path.join(csv_path, csv_filename), 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Project_ID', 'Project_Title', 'Current_Business_Area', 'Updated_Business_Area']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    count = 0
    for row in results:
        current_area = row.business_organization or 'N/A'
        updated_area = mapping.get(current_area, current_area)
        
        writer.writerow({
            'Project_ID': row.project_id,
            'Project_Title': row.title,
            'Current_Business_Area': current_area,
            'Updated_Business_Area': updated_area
        })
        count += 1

print(f"\n✓ CSV Generated: {csv_filename}")
print(f"  Location: {csv_path}")
print(f"  Total Projects: {count}")
print(f"\nMapping Summary:")

# Show counts by area
mapping_counts = {}
results = client.query(sql).result()
for row in results:
    current = row.business_organization or 'N/A'
    updated = mapping.get(current, current)
    if updated not in mapping_counts:
        mapping_counts[updated] = 0
    mapping_counts[updated] += 1

print("\nProjects by Updated Business Area:")
print("-" * 60)
print(f"{'Updated Business Area':<45} {'Count':>8}")
print("-" * 60)
for area in sorted(mapping_counts.keys()):
    print(f"{area:<45} {mapping_counts[area]:>8}")
print("-" * 60)
print(f"{'TOTAL':<45} {sum(mapping_counts.values()):>8}")
