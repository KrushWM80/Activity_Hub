from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

q = """
SELECT DISTINCT TDA_Ownership, Phase, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Topic IS NOT NULL
GROUP BY TDA_Ownership, Phase
ORDER BY TDA_Ownership, Phase
"""
print("TDA_Ownership x Phase distribution:")
print("-" * 65)
for row in client.query(q).result():
    print(f"  {str(row.TDA_Ownership):30s} | {str(row.Phase):15s} | {row.cnt} rows")

print()
print("--- Distinct TDA_Ownership values ---")
q2 = """SELECT DISTINCT TDA_Ownership FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` ORDER BY TDA_Ownership"""
for row in client.query(q2).result():
    print(f'  "{row.TDA_Ownership}"')

print()
print("--- Pending + No Selection check ---")
q3 = """
SELECT Topic, Phase, TDA_Ownership, SUM(Facility) as stores
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Phase = 'Pending' AND (TDA_Ownership IS NULL OR TDA_Ownership = 'No Selection Provided')
GROUP BY Topic, Phase, TDA_Ownership
ORDER BY Topic
"""
for row in client.query(q3).result():
    print(f"  {row.Topic[:50]:50s} | {str(row.TDA_Ownership):25s} | {row.stores} stores")
