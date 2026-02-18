from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# Query to find projects owned by Jorden
query = """
SELECT DISTINCT 
    COALESCE(Owner, PROJECT_OWNER, '') as owner,
    COALESCE(PROJECT_TITLE, Title, 'Untitled') as title
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Owner IS NOT NULL AND Owner != '' AND LOWER(Owner) LIKE '%jorden%'
LIMIT 10
"""

result = client.query(query)
print('Projects owned by Jorden:')
for row in result:
    print(f'  Owner: "{row.owner}" | Title: {row.title}')
