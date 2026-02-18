from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

query = """
SELECT DISTINCT Title 
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` 
WHERE LOWER(Title) LIKE '%gmd%' 
  AND Status = 'Active' 
ORDER BY Title
"""

results = client.query(query).result()
titles = [row.Title for row in results]

print(f'\nFound {len(titles)} GMD projects:\n')
for i, title in enumerate(titles, 1):
    print(f'{i}. {title}')
