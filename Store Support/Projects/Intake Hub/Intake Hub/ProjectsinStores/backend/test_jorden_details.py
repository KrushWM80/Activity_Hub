from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# Query to find Jorden Huff's projects with all details
query = """
SELECT 
    COALESCE(Owner, PROJECT_OWNER, '') as owner,
    COALESCE(PROJECT_TITLE, Title, 'Untitled') as title,
    Project_Source,
    Facility,
    Status,
    Division
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Owner IS NOT NULL AND Owner != '' AND LOWER(Owner) LIKE '%jorden%'
LIMIT 20
"""

result = client.query(query)
print('Projects owned by Jorden with full details:')
for row in result:
    print(f'  Owner: "{row.owner}"')
    print(f'    Title: {row.title}')
    print(f'    Project_Source: {row.Project_Source}')
    print(f'    Facility: {row.Facility}')
    print(f'    Status: {row.Status}')
    print(f'    Division: {row.Division}')
    print()
