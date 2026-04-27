from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("=== STORE_AREA VALUES ===")
query1 = "SELECT DISTINCT Store_Area FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data` WHERE Store_Area IS NOT NULL ORDER BY Store_Area LIMIT 20"
results1 = list(client.query(query1).result())
for row in results1:
    print(f"  {row.Store_Area}")

print("\n=== BUSINESS_OWNER_AREA VALUES ===")
query2 = "SELECT DISTINCT Business_Owner_Area FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data` WHERE Business_Owner_Area IS NOT NULL ORDER BY Business_Owner_Area LIMIT 20"
results2 = list(client.query(query2).result())
for row in results2:
    print(f"  {row.Business_Owner_Area}")

print("\n=== UPDATED_BUSINESS_TYPE VALUES ===")
query3 = "SELECT DISTINCT Updated_Business_Type FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data` WHERE Updated_Business_Type IS NOT NULL ORDER BY Updated_Business_Type LIMIT 20"
results3 = list(client.query(query3).result())
for row in results3:
    print(f"  {row.Updated_Business_Type}")

print("\n=== ITB_BUSINESS VALUES ===")
query4 = "SELECT DISTINCT ITB_Business FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data` WHERE ITB_Business IS NOT NULL ORDER BY ITB_Business LIMIT 20"
results4 = list(client.query(query4).result())
for row in results4:
    print(f"  {row.ITB_Business}")
