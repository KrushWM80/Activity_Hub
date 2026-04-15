from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

tables = {
    'Normalized - Weekly Messages Devices': 'bq_weekly_messages_devices',
    'Normalized - Weekly Messages Metrics': 'bq_weekly_messages_metrics',
    'Normalized - Playbook Hub': 'bq_playbook_hub_metrics',
    'Raw - Playbook Hub': 'bq_playbook_hub_raw',
    'Raw - Weekly Messages': 'bq_weekly_messages_raw'
}

print('=' * 80)
print('BigQuery Table Last Update Status (as of April 15, 2026)')
print('=' * 80)

for table_name, table_id in tables.items():
    query = f'''
    SELECT 
        COUNT(*) as row_count,
        MAX(extracted_date) as last_updated
    FROM `wmt-assetprotection-prod.Store_Support_Dev.{table_id}`
    '''
    try:
        result = client.query(query).result()
        for row in result:
            if row['last_updated']:
                days_old = (datetime.now() - row['last_updated'].replace(tzinfo=None)).days
                print(f'{table_name}')
                print(f'  Rows: {row["row_count"]}')
                print(f'  Last Updated: {row["last_updated"]} ({days_old} days ago)')
            else:
                print(f'{table_name}: No data')
    except Exception as e:
        print(f'{table_name}: Error - {e}')
    print()
