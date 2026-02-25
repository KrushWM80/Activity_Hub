import sqlite3
from google.cloud import bigquery

# Check SQLite intake_card format
conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()

cursor.execute('SELECT intake_card FROM projects WHERE intake_card IS NOT NULL AND intake_card != "" LIMIT 5')
sqlite_intake = cursor.fetchall()
print('SQLite intake_card samples:')
for row in sqlite_intake:
    print(f'  {row[0]}')

conn.close()

# Check BigQuery Intake_Card_Nbr format from IH_Branch_Data
client = bigquery.Client(project='wmt-assetprotection-prod')
query = """
SELECT DISTINCT Cast(Intake_Card_Nbr AS STRING) as intake_card 
FROM `wmt-assetprotection-prod.Store_Support.IH_Branch_Data`
WHERE Intake_Card_Nbr IS NOT NULL
LIMIT 5
"""
result = client.query(query).result()
print('\nBigQuery IH_Branch_Data Intake_Card_Nbr samples:')
for row in result:
    print(f'  {row.intake_card}')
