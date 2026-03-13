from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

print("=== CURRENT BQ TABLE STATUS ===\n")

# Total Active records
query = """
SELECT COUNT(*) as total
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""
result = list(client.query(query).result())[0]
print(f"Total Active Records: {result['total']:,}")

# Breakdown by Project_Source
print("\nBy Project_Source:")
query2 = """
SELECT Project_Source, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
GROUP BY Project_Source
ORDER BY count DESC
"""
results = list(client.query(query2).result())
for row in results:
    print(f"  {row['Project_Source']}: {row['count']:,} records")

# Distinct Intake_Card and Facility counts
print("\nDistinct Identifiers:")
query3 = """
SELECT 
  COUNT(DISTINCT Intake_Card) as distinct_intake_cards,
  COUNT(DISTINCT Facility) as distinct_facilities,
  COUNT(DISTINCT CASE WHEN Project_Source = 'Realty' THEN Intake_Card END) as realty_intake_cards,
  COUNT(DISTINCT CASE WHEN Project_Source IN ('Operations', 'Intake Hub') THEN Intake_Card END) as ops_hub_intake_cards
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""
result = list(client.query(query3).result())[0]
print(f"  Distinct Intake_Card (Projects): {result['distinct_intake_cards']:,}")
print(f"  Distinct Facility (Stores): {result['distinct_facilities']:,}")
print(f"  Realty Intake_Cards: {result['realty_intake_cards']:,}")
print(f"  Operations/Hub Intake_Cards: {result['ops_hub_intake_cards']:,}")

# Check last updated timestamp
print("\nData Freshness:")
query4 = """
SELECT 
  MAX(Last_Updated) as last_updated_legacy,
  MAX(UPDATE_TS) as last_updated_new
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""
result = list(client.query(query4).result())[0]
print(f"  Last_Updated (legacy field): {result['last_updated_legacy']}")
print(f"  UPDATE_TS (new field): {result['last_updated_new']}")
