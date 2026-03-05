from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')
query = """
SELECT Intake_Card_Nbr, BRANCH_NAME
FROM `wmt-assetprotection-prod.Store_Support.IH_Branch_Data`
WHERE Intake_Card_Nbr = 10010
LIMIT 1000
"""

results = client.query(query).result()
rows = list(results)

print(f'Total rows returned: {len(rows)}\n')
print('All Rows:')
print('-' * 70)
for i, row in enumerate(rows, 1):
    print(f'{i}. Intake_Card_Nbr: {row.Intake_Card_Nbr}, BRANCH_NAME: {row.BRANCH_NAME}')

print('\n' + '-' * 70)
unique_branches = sorted(set(row.BRANCH_NAME for row in rows if row.BRANCH_NAME))
print(f'\nUnique BRANCH_NAME values ({len(unique_branches)}):')
for branch in unique_branches:
    count = sum(1 for row in rows if row.BRANCH_NAME == branch)
    print(f'  - {branch} (appears {count} time{"s" if count != 1 else ""})')
