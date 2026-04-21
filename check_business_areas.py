#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client()

# Get all distinct business_organization values
sql = """
SELECT DISTINCT business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
ORDER BY business_organization
"""

results = client.query(sql).result()
areas = [row.business_organization for row in results]

print('=== ALL Business Organizations in BigQuery ===')
for area in areas:
    print(f'  {repr(area)}')
print(f'\nTotal: {len(areas)} distinct areas')

# Now get count by business area
sql2 = """
SELECT business_organization, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
GROUP BY business_organization
ORDER BY cnt DESC
"""

results2 = client.query(sql2).result()
print('\n=== Projects by Business Organization ===')
for row in results2:
    print(f'  {repr(row.business_organization)}: {row.cnt} projects')

# Check what we're currently excluding
excluded = ['Automotive', 'Unknown', 'N/A', '']
print(f'\n=== Current Exclusions ===')
for exc in excluded:
    if exc == '':
        print(f'  Empty string')
    else:
        print(f'  {repr(exc)}')

print(f'\n=== John Stien project counts by business area ===')
sql3 = """
SELECT business_organization, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE owner = 'John Stien'
GROUP BY business_organization
ORDER BY cnt DESC
"""
results3 = client.query(sql3).result()
for row in results3:
    print(f'  {repr(row.business_organization)}: {row.cnt} projects')

total_stien = sum(r.cnt for r in client.query(sql3).result())
print(f'\nTotal John Stien projects: {total_stien}')

# Check what we're showing (excluding the invalid areas)
print(f'\n=== What We Show (Current Filter) ===')
sql4 = """
SELECT DISTINCT business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE business_organization NOT IN ('Automotive', 'Unknown', 'N/A')
AND TRIM(business_organization) != ''
ORDER BY business_organization
"""
results4 = client.query(sql4).result()
shown_areas = [row.business_organization for row in results4]
for area in shown_areas:
    print(f'  {repr(area)}')

print(f'\nTotal shown: {len(shown_areas)} areas')
