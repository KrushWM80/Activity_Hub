from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check if maybe Tour Guides exists with Kendall Rush but has a blank business_organization
sql = """
SELECT 
    project_id,
    title,
    owner,
    COALESCE(business_organization, '(NULL)') as business_organization,
    project_update_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE 1=1
  AND (business_organization IS NULL OR TRIM(business_organization) = '')
  AND owner = 'Kendall Rush'
ORDER BY title
"""

print("Checking for Kendall Rush projects with BLANK/NULL business_organization:")
results = list(client.query(sql).result())
if results:
    print(f"Found {len(results)} projects with blank business_organization:\n")
    for row in results:
        print(f"  - {row['title']} (ID: {row['project_id']})")
else:
    print("No projects found with blank business_organization for Kendall Rush")

# Also list ALL Kendall Rush projects regardless of business_organization
print("\n\nALL Kendall Rush projects (no filters):")
sql_all = """
SELECT 
    project_id,
    title,
    owner,
    COALESCE(business_organization, '(NULL)') as business_organization,
    project_update_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE owner = 'Kendall Rush'
ORDER BY title
"""

results_all = list(client.query(sql_all).result())
print(f"Total: {len(results_all)} projects\n")
for row in results_all:
    org_display = row['business_organization']
    print(f"  - {row['title']}")
    print(f"    Org: {org_display}, Updated: {row['project_update_date']}")
