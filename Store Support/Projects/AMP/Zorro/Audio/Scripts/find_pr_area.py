"""Find where AMP PR Merchandise appears in AMP ALL 2."""
import os
for p in [os.path.join(os.environ.get('APPDATA',''),'gcloud','application_default_credentials.json')]:
    if os.path.isfile(p): os.environ['GOOGLE_APPLICATION_CREDENTIALS']=p; break

from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# Check Business_Area and Store_Area for anything with "PR"
for col in ['Business_Area', 'Store_Area']:
    q = f"""SELECT DISTINCT {col} FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE {col} LIKE '%PR%' OR {col} LIKE '%Puerto%' LIMIT 20"""
    print(f"=== {col} containing PR ===")
    for row in client.query(q).result():
        print(f"  {getattr(row, col)}")

# Also check all distinct Business_Area values
print("\n=== All distinct Business_Area values ===")
q2 = """SELECT DISTINCT Business_Area FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2` ORDER BY Business_Area"""
for row in client.query(q2).result():
    print(f"  {row.Business_Area}")
