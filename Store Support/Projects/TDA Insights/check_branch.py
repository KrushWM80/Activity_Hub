"""Check Branch_name column in BQ table"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')
P = 'wmt-assetprotection-prod'
D = 'Store_Support_Dev'
T = 'Output- TDA Report'

print("=== ALL COLUMNS IN TABLE ===")
q1 = f"SELECT column_name, data_type FROM `{P}.{D}.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'Output- TDA Report' ORDER BY ordinal_position"
cols = []
for r in client.query(q1).result():
    cols.append(r.column_name)
    print(f"  {r.column_name}: {r.data_type}")

has_branch = any('branch' in c.lower() for c in cols)
print(f"\nBranch_name column exists: {has_branch}")

if has_branch:
    branch_col = [c for c in cols if 'branch' in c.lower()][0]
    print(f"\n=== DISTINCT {branch_col} VALUES ===")
    q2 = f"SELECT DISTINCT `{branch_col}` as val FROM `{P}.{D}.{T}` ORDER BY val"
    for r in client.query(q2).result():
        print(f"  '{r.val}'")
    
    print(f"\n=== {branch_col} VALUE COUNTS ===")
    q3 = f"SELECT `{branch_col}` as val, COUNT(*) as cnt FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL GROUP BY val ORDER BY cnt DESC"
    for r in client.query(q3).result():
        print(f"  {str(r.val):<25} count={r.cnt}")
    
    print(f"\n=== Filter check: Implement, Validation, Intake & Test ===")
    q4 = f"SELECT `{branch_col}` as val, COUNT(DISTINCT Topic) as topics FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL AND `{branch_col}` IN ('Implement', 'Validation', 'Intake & Test') GROUP BY val"
    total = 0
    for r in client.query(q4).result():
        print(f"  {r.val}: {r.topics} topics")
        total += r.topics
    print(f"  Total with filter: {total}")
    
    q5 = f"SELECT COUNT(DISTINCT Topic) as total FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL"
    for r in client.query(q5).result():
        print(f"  Total without filter: {r.total}")
else:
    print("\n  Branch_name NOT found. Checking all tables in dataset for branch columns...")
    q_all = f"SELECT table_name, column_name FROM `{P}.{D}.INFORMATION_SCHEMA.COLUMNS` WHERE LOWER(column_name) LIKE '%branch%' ORDER BY table_name"
    found = False
    for r in client.query(q_all).result():
        print(f"  Table: {r.table_name}, Column: {r.column_name}")
        found = True
    if not found:
        print("  No branch columns found in any table in this dataset")

print("\nDone!")
