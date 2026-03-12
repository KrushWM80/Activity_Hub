#!/usr/bin/env python3
from google.cloud import bigquery
import os

# Set up BigQuery client
creds_path = os.path.join(os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query the actual BQ table
query = """
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT project_id) as unique_projects
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
"""

print("=== QUERYING BIGQUERY ===")
print("Table: wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data\n")

try:
    results = client.query(query).result()
    for row in results:
        print(f"Total Records: {row.total_records:,}")
        print(f"Unique Projects: {row.unique_projects:,}")
    
    # Get actual column names
    print("\n=== SCHEMA ===")
    schema_query = """
    SELECT column_name, data_type
    FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data.__TABLES_SUMMARY__`
    JOIN information_schema.columns 
    ON table_name = '__TABLES_SUMMARY__'
    LIMIT 25
    """
    
    print("Getting first 10 rows with all columns:")
    sample_query = """
    SELECT *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
    LIMIT 10
    """
    
    sample_results = client.query(sample_query).result()
    cols = [field.name for field in sample_results.schema]
    print(f"Columns: {cols}")
    for row in sample_results:
        print(row)
    
    # Check partner field if it exists
    print("\n=== CHECKING AVAILABLE COLUMNS ===")
    try:
        col_query = """
        SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` LIMIT 0
        """
        col_results = client.query(col_query).result()
        cols = [field.name for field in col_results.schema]
        print(f"Columns in BQ table: {cols}")
    except Exception as e:
        print(f"Error getting columns: {e}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
