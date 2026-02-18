"""Check stores with Project_Type = 'None'"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Get all 28 stores with Project_Type = 'None'
query = """
SELECT Facility, FY, Project_Type, Initiative_Type
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty' 
  AND Status = 'Active' 
  AND (Project_Type = 'None' OR Project_Type IS NULL)
  AND Initiative_Type IS NOT NULL
ORDER BY Facility
"""

print("All Active Realty projects with Project_Type='None'/NULL:\n")
print("Store#\t\tFY\tProject_Type\tInitiative_Type")
print("-" * 70)

count = 0
for row in client.query(query).result():
    count += 1
    store = int(row.Facility) if row.Facility else 'NULL'
    print(f"{store}\t\t{row.FY}\t{row.Project_Type}\t\t{row.Initiative_Type}")

print("-" * 70)
print(f"Total: {count}")
