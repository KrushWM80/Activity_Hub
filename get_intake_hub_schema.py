#!/usr/bin/env python3
"""
Get column names from Intake Hub Data
"""

from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client(project='wmt-assetprotection-prod')

def get_intake_hub_schema():
    """Get all column names from Intake Hub table"""
    
    print("=" * 80)
    print("INTAKE HUB TABLE SCHEMA")
    print("=" * 80)
    
    query = """
    SELECT column_name, data_type
    FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'Output - Intake Accel Council Data'
    ORDER BY column_name
    """
    
    try:
        results = list(client.query(query).result())
        
        print(f"\nFound {len(results)} columns:\n")
        
        # Print all columns
        for i, row in enumerate(results, 1):
            col_name = row['column_name']
            col_type = row['data_type']
            print(f"{i:3d}. {col_name:50s} | {col_type}")
        
        # Look for email/contact related columns
        print("\n" + "=" * 80)
        print("CONTACT-RELATED COLUMNS")
        print("=" * 80)
        
        contact_keywords = ['email', 'phone', 'contact', 'owner', 'manager', 'lead', 'name']
        
        for row in results:
            col_name = row['column_name'].lower()
            if any(keyword in col_name for keyword in contact_keywords):
                print(f"  {row['column_name']:50s} | {row['data_type']}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    get_intake_hub_schema()
