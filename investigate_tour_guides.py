from google.cloud import bigquery
from Interface.send_projects_owner_emails import query_owner_projects

owner = 'Kendall Rush'

# First check what the query returns
print(f"Projects for {owner} via query function:")
projects = query_owner_projects(owner, include_only_not_updated=False)
print(f"Total projects: {len(projects)}")
for p in projects:
    print(f"  - {p['title']} (ID: {p['project_id']}, Updated: {p['updated']})")

# Now check raw BigQuery for "Tour Guides" specifically
print("\n\nSearching BigQuery for 'Tour Guides' or 'tour' project:")
client = bigquery.Client(project='wmt-assetprotection-prod')
sql = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    health,
    project_update,
    project_update_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE LOWER(title) LIKE '%tour%' OR LOWER(title) LIKE '%guide%'
"""
results = list(client.query(sql).result())
if results:
    print(f"Found {len(results)} projects matching 'tour' or 'guide':")
    for row in results:
        print(f"\n  Title: {row['title']}")
        print(f"  ID: {row['project_id']}")
        print(f"  Owner: {row['owner']}")
        print(f"  Updated: {row['project_update_date']}")
else:
    print("No 'Tour Guides' or 'tour'/'guide' projects found in database")

# Check all Kendall Rush projects directly from BigQuery
print(f"\n\nDirect BigQuery query for {owner}:")
sql_direct = """
SELECT 
    project_id,
    title,
    owner,
    project_update_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE owner = @owner_name
ORDER BY title
"""
from google.cloud import bigquery as bq
job_config = bq.QueryJobConfig(query_parameters=[
    bq.ScalarQueryParameter("owner_name", "STRING", owner),
])
results_direct = list(client.query(sql_direct, job_config=job_config).result())
print(f"Found {len(results_direct)} projects total:")
for row in results_direct:
    print(f"  - {row['title']}")

