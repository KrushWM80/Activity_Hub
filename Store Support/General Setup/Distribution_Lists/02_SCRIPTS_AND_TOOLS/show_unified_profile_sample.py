from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')
q = "SELECT * FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` LIMIT 1"
row = list(client.query(q).result())[0]

print("\nAll fields in Unified Profile:")
print("="*80)
for k, v in row.items():
    if v:
        print(f"{k:40} = {v}")
