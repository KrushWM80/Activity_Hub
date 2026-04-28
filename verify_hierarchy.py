#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client('wmt-assetprotection-prod')

# Check sample of hierarchy data with relationships
query = """
SELECT person_name, director, sr_director 
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy` 
WHERE director IS NOT NULL 
LIMIT 15
"""

results = list(client.query(query).result())
print(f"\nHierarchy Sample ({len(results)} with directors):\n")
for row in results:
    print(f"{row.person_name:30} -> {row.director:30} -> {row.sr_director or 'NULL'}")

# Check distribution
query2 = """
SELECT 
    COUNTIF(director IS NOT NULL) as with_director,
    COUNTIF(sr_director IS NOT NULL) as with_sr_director,
    COUNTIF(director IS NOT NULL AND sr_director IS NOT NULL) as complete_chain
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy`
"""

summary = list(client.query(query2).result())[0]
print(f"\nHierarchy Distribution:")
print(f"  With director: {summary.with_director}")
print(f"  With sr_director: {summary.with_sr_director}")
print(f"  With both: {summary.complete_chain}")
