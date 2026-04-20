from google.cloud import bigquery

bq_client = bigquery.Client(project='wmt-assetprotection-prod')

# Check distinct values in key fields
fields_to_check = ['store_area', 'impact', 'ho_impact']

for field in fields_to_check:
    sql = f"""
    SELECT DISTINCT {field} as value, COUNT(*) as count
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    WHERE {field} IS NOT NULL
    GROUP BY {field}
    ORDER BY count DESC
    LIMIT 20
    """
    
    print(f"\n=== Distinct values in '{field}' ===\n")
    try:
        results = list(bq_client.query(sql).result())
        if results:
            for row in results:
                print(f"  {row.value}: {row.count}")
        else:
            print("  (no values)")
    except Exception as e:
        print(f"  Error: {e}")
