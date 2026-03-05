from google.cloud import bigquery

client = bigquery.Client()

def print_polaris_schema():
    query = '''
    SELECT * FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    LIMIT 1
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        if rows:
            first_row = rows[0]
            print("\nAvailable columns in vw_polaris_current_schedule:")
            for col in first_row.keys():
                print(f"  - {col}")
            print("\nSample data (first row):")
            for key, value in first_row.items():
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print_polaris_schema()
