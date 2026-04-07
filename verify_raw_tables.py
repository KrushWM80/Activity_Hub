from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query both raw tables
queries = {
    'Playbook Hub Raw': 'SELECT COUNT(*) as row_count FROM `wmt-assetprotection-prod.Store_Support_Dev.bq_playbook_hub_raw`',
    'Weekly Messages Raw': 'SELECT COUNT(*) as row_count FROM `wmt-assetprotection-prod.Store_Support_Dev.bq_weekly_messages_raw`'
}

print("=" * 80)
print("RAW DATA TABLE VERIFICATION")
print("=" * 80)

for table_name, query in queries.items():
    result = client.query(query).result()
    for row in result:
        print(f"{table_name}: {row['row_count']} rows ✓")
    
    # Get sample data
    sample_query = f"SELECT * EXCEPT(extracted_date) FROM `wmt-assetprotection-prod.Store_Support_Dev.bq_{table_name.lower().replace(' ', '_')}_raw` LIMIT 3"
    try:
        sample_result = client.query(f"SELECT * EXCEPT(extracted_date) FROM `wmt-assetprotection-prod.Store_Support_Dev.bq_{'playbook_hub_raw' if 'Playbook' in table_name else 'weekly_messages_raw'}` LIMIT 3").result()
        print(f"\nSample rows from {table_name}:")
        for row in sample_result:
            print(f"  {dict(row)}")
    except:
        pass

print("\n" + "=" * 80)
