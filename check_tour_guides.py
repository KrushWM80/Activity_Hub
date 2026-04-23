from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Search for Tour Guides without the business_organization filter
sql = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    health,
    project_update_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE LOWER(title) LIKE '%tour%'
   OR LOWER(title) LIKE '%guide%'
   OR LOWER(title) LIKE '%kendall%'
ORDER BY title
"""

print("Searching without business_organization filter...")
results = list(client.query(sql).result())
print(f"Found {len(results)} projects:\n")

for row in results:
    org = row['business_organization'] if row['business_organization'] else "(BLANK/NULL)"
    print(f"Title: {row['title']}")
    print(f"  Owner: {row['owner']}")
    print(f"  Business Org: {org}")
    print()

# Also check the full WHERE clause that the API uses
print("\n\nApplying API WHERE clause (business_organization != ''):")
sql_with_filter = """
SELECT 
    project_id,
    title,
    owner,
    business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE 1=1
AND TRIM(business_organization) != ''
AND owner = 'Kendall Rush'
ORDER BY title
"""
results2 = list(client.query(sql_with_filter).result())
print(f"Found {len(results2)} Kendall Rush projects with non-empty business_organization:\n")
for row in results2:
    print(f"  - {row['title']}")
