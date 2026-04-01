"""Deep dive into TDA data to understand ownership structure"""
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# 1. Show ALL 51 projects with their TDA_Ownership
q1 = """SELECT DISTINCT Topic, TDA_Ownership, Phase, Health_Update
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
ORDER BY Topic"""
print("=== ALL 51 PROJECTS ===")
print(f"{'Topic':<65} {'TDA_Ownership':<25} {'Phase':<15} {'Health'}")
print("-" * 130)
for row in client.query(q1).result():
    print(f"  {(row.Topic or 'N/A'):<63} {(row.TDA_Ownership or 'N/A'):<25} {(row.Phase or 'N/A'):<15} {row.Health_Update or 'N/A'}")

# 2. Check what Dallas_POC column contains (this is the column we map to Executive Notes)
q2 = """SELECT DISTINCT Topic, Dallas_POC, TDA_Ownership
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Dallas_POC IS NOT NULL AND Dallas_POC != ''
ORDER BY Topic
LIMIT 20"""
print("\n\n=== DALLAS_POC COLUMN VALUES (first 20) ===")
print(f"{'Topic':<55} {'Dallas_POC (col value)':<40} {'TDA_Ownership'}")
print("-" * 130)
for row in client.query(q2).result():
    val = (row.Dallas_POC or '')[:38]
    print(f"  {(row.Topic or 'N/A'):<53} {val:<40} {row.TDA_Ownership or 'N/A'}")

# 3. Check all column names in the table
q3 = """SELECT column_name, data_type 
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Output- TDA Report'
ORDER BY ordinal_position"""
print("\n\n=== TABLE SCHEMA ===")
for row in client.query(q3).result():
    print(f"  {row.column_name:<30} {row.data_type}")

# 4. Check if there's a Dallas-related column that marks ALL projects
q4 = """SELECT 
    COUNT(DISTINCT Topic) as total_projects,
    COUNT(DISTINCT CASE WHEN Dallas_POC IS NOT NULL AND Dallas_POC != '' THEN Topic END) as has_dallas_poc_value,
    COUNT(DISTINCT CASE WHEN TDA_Ownership = 'Dallas POC' THEN Topic END) as owned_by_dallas_poc,
    COUNT(DISTINCT CASE WHEN Intake_n_Testing IS NOT NULL AND Intake_n_Testing != '' THEN Topic END) as has_intake_test,
    COUNT(DISTINCT CASE WHEN Deployment IS NOT NULL AND Deployment != '' THEN Topic END) as has_deployment
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`"""
print("\n\n=== COLUMN POPULATION COUNTS ===")
for row in client.query(q4).result():
    print(f"  Total projects: {row.total_projects}")
    print(f"  Has Dallas_POC value: {row.has_dallas_poc_value}")
    print(f"  TDA_Ownership = 'Dallas POC': {row.owned_by_dallas_poc}")
    print(f"  Has Intake_n_Testing value: {row.has_intake_test}")
    print(f"  Has Deployment value: {row.has_deployment}")

# 5. Show projects NOT owned by Dallas POC
q5 = """SELECT DISTINCT Topic, TDA_Ownership, Phase, Health_Update, Dallas_POC
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE TDA_Ownership != 'Dallas POC'
ORDER BY TDA_Ownership, Topic"""
print("\n\n=== PROJECTS NOT OWNED BY 'Dallas POC' ===")
print(f"{'Topic':<55} {'TDA_Ownership':<25} {'Phase':<15} {'Dallas_POC col'}")
print("-" * 130)
for row in client.query(q5).result():
    dp = (row.Dallas_POC or '')[:30]
    print(f"  {(row.Topic or 'N/A'):<53} {(row.TDA_Ownership or 'N/A'):<25} {(row.Phase or 'N/A'):<15} {dp}")
