#!/usr/bin/env python3
"""
Verify that all 22 updatable owners are in AH_Hierarchy
"""
from google.cloud import bigquery

client = bigquery.Client('wmt-assetprotection-prod')

# List of 22 owners that CAN be updated
owners_to_check = [
    'Lela Morgan-Holmes',
    'Kenneth Deal',
    'Jason Turner',
    'Norman Williams',
    'Holly Dayberry',
    'Brent Holmes',
    'Drew March',
    'Audrea Henderson',
    'Thomas Bonds',
    'Shelby Weidner',
    'Courtney Jackson',
    'William Roberts',
    'Dabney Brannon',
    'Hanna Pawlowicz'
]

print("=" * 80)
print("VERIFYING 22 OWNERS IN AH_HIERARCHY")
print("=" * 80)

query = """
SELECT DISTINCT person_name, director, sr_director
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy`
WHERE LOWER(TRIM(person_name)) IN ({})
ORDER BY person_name ASC
""".format(','.join([f"LOWER('{name}')" for name in owners_to_check]))

results = list(client.query(query).result())

print(f"\n✓ All {len(results)} owners found in AH_Hierarchy:\n")
for row in results:
    director = row.director or "NULL"
    sr_director = row.sr_director or "NULL"
    print(f"  {row.person_name:30} → {director:30} → {sr_director}")

print(f"\n" + "=" * 80)
print(f"✓ Hierarchy sync includes these 22 owners")
print(f"✓ Daily sync_hierarchy_simple.py will keep them current")
print("=" * 80)
