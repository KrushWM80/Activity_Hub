#!/usr/bin/env python
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("=" * 80)
print("SEARCHING FOR PROJECT 17902 / INTAKE_CARD 17902")
print("=" * 80)

search_query = """
SELECT 
  Intake_Card,
  PROJECT_ID,
  PROJECT_TITLE,
  Owner,
  PROJECT_OWNER,
  PROJECT_OWNERID,
  CREATED_USERID,
  Director,
  Sr_Director,
  VP
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE 
  Intake_Card = 17902
  OR PROJECT_ID = 17902
LIMIT 10
"""

try:
    search_results = client.query(search_query).result()
    total = search_results.total_rows
    print(f"\nFound {total} rows with PROJECT ID or INTAKE_CARD = 17902\n")
    
    for idx, row in enumerate(search_results, 1):
        print(f"--- RESULT {idx} ---")
        print(f"Intake_Card: {row.Intake_Card}")
        print(f"PROJECT_ID: {row.PROJECT_ID}")
        print(f"PROJECT_TITLE: {row.PROJECT_TITLE}")
        print(f"Owner (col): {row.Owner}")
        print(f"PROJECT_OWNER: {row.PROJECT_OWNER}")
        print(f"PROJECT_OWNERID: {row.PROJECT_OWNERID}")
        print(f"CREATED_USERID: {row.CREATED_USERID}")
        print(f"Director: {row.Director}")
        print(f"Sr_Director: {row.Sr_Director}")
        print(f"VP: {row.VP}")
        print()
        
    if total == 0:
        print("No rows found. Searching for 'Huff'...\n")
        
        huff_query = """
        SELECT 
          Intake_Card,
          PROJECT_ID,
          PROJECT_TITLE,
          Owner,
          PROJECT_OWNER,
          PROJECT_OWNERID
        FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
        WHERE 
          Owner LIKE '%Huff%'
          OR PROJECT_OWNER LIKE '%Huff%'
        LIMIT 5
        """
        
        huff_results = client.query(huff_query).result()
        print(f"Found {huff_results.total_rows} rows with 'Huff':\n")
        for idx, row in enumerate(huff_results, 1):
            print(f"--- RESULT {idx} ---")
            print(f"Intake_Card: {row.Intake_Card}")
            print(f"PROJECT_ID: {row.PROJECT_ID}")
            print(f"PROJECT_TITLE: {row.PROJECT_TITLE}")
            print(f"Owner: {row.Owner}")
            print(f"PROJECT_OWNER: {row.PROJECT_OWNER}")
            print()
                
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()


