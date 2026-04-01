"""Quick check of all data in the TDA table to understand filtering"""
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# 1. Total rows
q1 = "SELECT COUNT(*) as total FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`"
print("=== TOTAL ROWS IN TABLE ===")
for row in client.query(q1).result():
    print(f"Total rows: {row.total}")

# 2. Distinct topics
q2 = "SELECT COUNT(DISTINCT Topic) as topics FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`"
print("\n=== DISTINCT TOPICS (ALL) ===")
for row in client.query(q2).result():
    print(f"Total distinct topics: {row.topics}")

# 3. All TDA_Ownership values
q3 = """SELECT TDA_Ownership, COUNT(DISTINCT Topic) as projects 
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` 
GROUP BY TDA_Ownership ORDER BY projects DESC"""
print("\n=== TDA_OWNERSHIP BREAKDOWN ===")
for row in client.query(q3).result():
    print(f"  {row.TDA_Ownership}: {row.projects} projects")

# 4. Dallas POC by phase
q4 = """SELECT Phase, COUNT(DISTINCT Topic) as projects 
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` 
WHERE TDA_Ownership = 'Dallas POC'
GROUP BY Phase ORDER BY Phase"""
print("\n=== DALLAS POC BY PHASE ===")
for row in client.query(q4).result():
    print(f"  {row.Phase}: {row.projects} projects")

# 5. All Dallas/VET/POC ownership values
q5 = """SELECT DISTINCT TDA_Ownership FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` 
WHERE LOWER(TDA_Ownership) LIKE '%dallas%' OR LOWER(TDA_Ownership) LIKE '%vet%' OR LOWER(TDA_Ownership) LIKE '%poc%'"""
print("\n=== OWNERSHIP VALUES WITH DALLAS/VET/POC ===")
for row in client.query(q5).result():
    print(f'  "{row.TDA_Ownership}"')

# 6. Check Phase values for Complete or excluded
q6 = """SELECT Phase, COUNT(DISTINCT Topic) as projects 
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` 
WHERE TDA_Ownership = 'Dallas POC'
GROUP BY Phase ORDER BY Phase"""
print("\n=== ALL PHASES FOR DALLAS POC (including Complete) ===")
for row in client.query(q6).result():
    print(f"  {row.Phase}: {row.projects} projects")

# 7. List all Dallas POC topics
q7 = """SELECT DISTINCT Topic, Phase, Health_Update 
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` 
WHERE TDA_Ownership = 'Dallas POC'
ORDER BY Phase, Topic"""
print("\n=== ALL DALLAS POC PROJECTS ===")
for row in client.query(q7).result():
    print(f"  [{row.Phase}] {row.Topic} - {row.Health_Update}")
