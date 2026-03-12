from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# Check distinct Intake_Card vs total records
query = """
SELECT 
  COUNT(*) as total_records,
  COUNT(DISTINCT Intake_Card) as distinct_intake_cards,
  COUNT(DISTINCT Facility) as distinct_facilities,
  COUNT(DISTINCT Project_Source) as distinct_sources,
  COUNT(DISTINCT CASE WHEN Project_Source = 'Realty' THEN Intake_Card END) as realty_cards,
  COUNT(DISTINCT CASE WHEN Project_Source IN ('Operations', 'Intake Hub') THEN Intake_Card END) as ops_hub_cards,
  COUNT(DISTINCT CASE WHEN Project_Source = 'Realty' THEN Facility END) as realty_facilities,
  COUNT(DISTINCT CASE WHEN Project_Source IN ('Operations', 'Intake Hub') THEN Facility END) as ops_hub_facilities
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""

result = list(client.query(query).result())[0]
print(f"Total Active Records: {result['total_records']}")
print(f"Distinct Intake_Card: {result['distinct_intake_cards']}")
print(f"Distinct Facility: {result['distinct_facilities']}")
print(f"Total Project Sources: {result['distinct_sources']}")
print(f"\nBreakdown:")
print(f"  Realty Intake_Cards: {result['realty_cards']}")
print(f"  Operations/Hub Intake_Cards: {result['ops_hub_cards']}")
print(f"  Realty Facilities: {result['realty_facilities']}")
print(f"  Operations/Hub Facilities: {result['ops_hub_facilities']}")

# Check Project_Source values
print("\n\nProject Sources:")
source_query = """
SELECT Project_Source, COUNT(*) as count, COUNT(DISTINCT Intake_Card) as distinct_cards
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
GROUP BY Project_Source
ORDER BY count DESC
"""
results = client.query(source_query).result()
for row in results:
    print(f"  {row['Project_Source']}: {row['count']} records, {row['distinct_cards']} distinct cards")
