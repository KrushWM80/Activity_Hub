from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

query = """
SELECT 
  'bq_weekly_messages_devices' as table_name, COUNT(*) as row_count FROM `wmt-assetprotection-prod.Store_Support_Dev.bq_weekly_messages_devices`
UNION ALL
SELECT 'bq_weekly_messages_metrics', COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.bq_weekly_messages_metrics`
UNION ALL  
SELECT 'bq_playbook_hub_metrics', COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.bq_playbook_hub_metrics`
"""

result = client.query(query).result()
for row in result:
    print(f"{row['table_name']}: {row['row_count']} rows")
