from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get ALL fields for project 18049
sql = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

print("Complete record for Project ID 18049:\n")
results = list(client.query(sql).result())

if results:
    row = results[0]
    fields = row.keys()
    
    for field in fields:
        value = getattr(row, field, 'N/A')
        if value is None:
            value = "NULL/MISSING"
        print(f"{field}: {value}")
else:
    print("Project not found")
