#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

print("=" * 100)
print("BUSINESS ORGANIZATIONS COMPARISON: Intake Hub vs Projects")
print("=" * 100)

# Get Intake Hub business organizations
print("\n1. INTAKE HUB - Business Organizations (IH_Intake_Data)")
print("-" * 100)
sql_intake = """
SELECT DISTINCT Business_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Business_Area IS NOT NULL
AND TRIM(Business_Area) != ''
ORDER BY Business_Area
"""

try:
    results = client.query(sql_intake).result()
    intake_orgs = sorted([row.Business_Area for row in results])
    
    print(f"Intake Hub has {len(intake_orgs)} distinct Business Areas:")
    for org in intake_orgs:
        print(f"  • {org}")
    print(f"\nTotal Intake Hub organizations: {len(intake_orgs)}")
except Exception as e:
    print(f"Error querying Intake Hub: {e}")
    intake_orgs = []

# Get Projects business organizations
print("\n2. PROJECTS - Business Organizations (AH_Projects)")
print("-" * 100)
sql_projects = """
SELECT DISTINCT business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE business_organization IS NOT NULL
AND TRIM(business_organization) != ''
ORDER BY business_organization
"""

results = client.query(sql_projects).result()
projects_orgs = sorted([row.business_organization for row in results])

for org in projects_orgs:
    print(f"  • {org}")
print(f"\nTotal Projects organizations: {len(projects_orgs)}")

# Comparison
print("\n3. COMPARISON ANALYSIS")
print("-" * 100)

intake_set = set(intake_orgs)
projects_set = set(projects_orgs)

only_in_intake = intake_set - projects_set
only_in_projects = projects_set - intake_set
in_both = intake_set & projects_set

print(f"\n✓ In BOTH (aligned): {len(in_both)}")
for org in sorted(in_both):
    print(f"    {org}")

if only_in_intake:
    print(f"\n⚠ ONLY in Intake Hub ({len(only_in_intake)}):")
    for org in sorted(only_in_intake):
        print(f"    {org}")

if only_in_projects:
    print(f"\n⚠ ONLY in Projects ({len(only_in_projects)}):")
    for org in sorted(only_in_projects):
        print(f"    {org}")

# Get project counts by org for projects
print("\n4. PROJECT COUNTS BY BUSINESS ORGANIZATION")
print("-" * 100)
sql_counts = """
SELECT business_organization, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE business_organization IS NOT NULL
AND TRIM(business_organization) != ''
GROUP BY business_organization
ORDER BY cnt DESC
"""

results = client.query(sql_counts).result()
print("Business Organization                      Projects    Status")
print("-" * 100)
for row in results:
    status = "IN INTAKE HUB" if row.business_organization in intake_set else "NOT IN INTAKE HUB"
    print(f"{row.business_organization:40} {row.cnt:5}       {status}")

print("\n" + "=" * 100)
