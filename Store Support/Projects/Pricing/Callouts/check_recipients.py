from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')
query = """SELECT id, email, added_date, is_active FROM `wmt-assetprotection-prod.Store_Support_Dev.Pricing_Callout_Email_Recipients` ORDER BY added_date DESC LIMIT 10"""
results = client.query(query).result()

print("Email Recipients in Database:")
print("=" * 80)
for row in results:
    print(f"ID: {row.id}")
    print(f"Email: {row.email}")
    print(f"Date: {row.added_date}")
    print(f"Active: {row.is_active}")
    print("-" * 80)

# Count totals
query_count = """SELECT COUNT(*) as total, SUM(CASE WHEN is_active = TRUE THEN 1 ELSE 0 END) as active FROM `wmt-assetprotection-prod.Store_Support_Dev.Pricing_Callout_Email_Recipients`"""
results_count = client.query(query_count).result()
for row in results_count:
    print(f"\nTotal Recipients: {row.total}")
    print(f"Active Recipients: {row.active}")
