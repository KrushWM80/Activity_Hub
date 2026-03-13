from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

print("=== TESTING CORRECT PROJECT COUNT LOGIC ===\n")

# Test what the correct query should return
query = """
SELECT 
  COUNT(DISTINCT CASE 
    WHEN Project_Source IN ('Operations', 'Intake Hub') AND Intake_Card IS NOT NULL 
      THEN CAST(Intake_Card AS STRING)
    WHEN Project_Source = 'Realty' 
      THEN Title  -- Count Realty by TITLE, not Facility
    ELSE NULL
  END) as total_projects,
  COUNT(DISTINCT CASE WHEN Project_Source IN ('Operations', 'Intake Hub') THEN Intake_Card END) as ops_hub_projects,
  COUNT(DISTINCT CASE WHEN Project_Source = 'Realty' THEN Title END) as realty_projects,
  COUNT(DISTINCT Facility) as total_stores,
  COUNT(DISTINCT CASE WHEN Project_Source IN ('Operations', 'Intake Hub') THEN Facility END) as ops_hub_stores,
  COUNT(DISTINCT CASE WHEN Project_Source = 'Realty' THEN Facility END) as realty_stores
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""

result = list(client.query(query).result())[0]

print("CORRECTED COUNTS:")
print(f"  Total Projects: {result['total_projects']}")
print(f"  ├─ Operations/Hub: {result['ops_hub_projects']}")
print(f"  └─ Realty: {result['realty_projects']}")
print(f"\nTotal Stores: {result['total_stores']}")
print(f"  ├─ Operations/Hub: {result['ops_hub_stores']}")
print(f"  └─ Realty: {result['realty_stores']}")

print("\n\nSample Realty Project Titles:")
title_query = """
SELECT DISTINCT Title, COUNT(*) as store_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active' AND Project_Source = 'Realty'
GROUP BY Title
ORDER BY store_count DESC
LIMIT 10
"""
results = list(client.query(title_query).result())
for i, row in enumerate(results, 1):
    print(f"  {i}. {row['Title']} ({row['store_count']} stores)")
