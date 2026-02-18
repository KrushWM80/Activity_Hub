"""
BigQuery Integration for Distribution List Selector
Loads DL data into BigQuery table for dynamic access by Code Puppy Pages
"""

import csv
import sys
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# BigQuery Configuration
PROJECT_ID = "wmt-assetprotection-prod"  # Walmart GCP project
DATASET_ID = "Store_Support_Dev"
TABLE_ID = "dl_catalog"
CREDENTIALS_FILE = "bigquery_credentials.json"  # Service account key file

def create_bigquery_client():
    """Create and return BigQuery client with service account credentials"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        print("✓ BigQuery client created successfully")
        return client
    except Exception as e:
        print(f"✗ Error creating BigQuery client: {e}")
        sys.exit(1)

def create_dataset_if_not_exists(client):
    """Create dataset if it doesn't exist"""
    dataset_id = f"{PROJECT_ID}.{DATASET_ID}"
    
    try:
        client.get_dataset(dataset_id)
        print(f"✓ Dataset {DATASET_ID} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        dataset.description = "Distribution list catalog for Walmart email tools"
        dataset = client.create_dataset(dataset)
        print(f"✓ Created dataset {DATASET_ID}")

def create_table_if_not_exists(client):
    """Create table with proper schema"""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    schema = [
        bigquery.SchemaField("email", "STRING", mode="REQUIRED", description="Distribution list email address"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED", description="Distribution list name"),
        bigquery.SchemaField("display_name", "STRING", mode="NULLABLE", description="Display name"),
        bigquery.SchemaField("description", "STRING", mode="NULLABLE", description="DL description"),
        bigquery.SchemaField("member_count", "INTEGER", mode="NULLABLE", description="Number of members"),
        bigquery.SchemaField("category", "STRING", mode="NULLABLE", description="Category (Operations, Market, etc)"),
        bigquery.SchemaField("last_updated", "TIMESTAMP", mode="REQUIRED", description="Last update timestamp"),
        bigquery.SchemaField("extraction_date", "DATE", mode="REQUIRED", description="Date of extraction"),
    ]
    
    try:
        client.get_table(table_id)
        print(f"✓ Table {TABLE_ID} already exists")
        return True
    except Exception:
        table = bigquery.Table(table_id, schema=schema)
        table.description = "Distribution list catalog with member counts and categories"
        table = client.create_table(table)
        print(f"✓ Created table {TABLE_ID}")
        return False

def load_csv_to_bigquery(client, csv_file):
    """Load CSV data into BigQuery table"""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    print(f"\nLoading data from: {csv_file}")
    print("This may take a few minutes for 134,681 records...")
    
    # Configure load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip header row
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Replace all data
        schema=[
            bigquery.SchemaField("email", "STRING"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("display_name", "STRING"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("member_count", "INTEGER"),
            bigquery.SchemaField("category", "STRING"),
        ]
    )
    
    # Add timestamp columns during load
    current_time = datetime.now().isoformat()
    
    try:
        with open(csv_file, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        
        # Wait for job to complete
        job.result()
        
        # Get table info
        table = client.get_table(table_id)
        
        print(f"\n✓ Successfully loaded {table.num_rows:,} rows into BigQuery")
        print(f"  Table: {table_id}")
        print(f"  Size: {table.num_bytes / (1024*1024):.2f} MB")
        
        # Update timestamp columns
        update_query = f"""
            UPDATE `{table_id}`
            SET 
                last_updated = CURRENT_TIMESTAMP(),
                extraction_date = CURRENT_DATE()
            WHERE TRUE
        """
        
        client.query(update_query).result()
        print("✓ Updated timestamp columns")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False

def verify_data(client):
    """Verify data was loaded correctly"""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    print("\n" + "="*80)
    print("Data Verification")
    print("="*80)
    
    # Total count
    query = f"SELECT COUNT(*) as total FROM `{table_id}`"
    result = client.query(query).result()
    total = list(result)[0].total
    print(f"Total Records: {total:,}")
    
    # Category breakdown
    query = f"""
        SELECT category, COUNT(*) as count 
        FROM `{table_id}` 
        GROUP BY category 
        ORDER BY count DESC
    """
    result = client.query(query).result()
    print("\nCategory Breakdown:")
    for row in result:
        print(f"  {row.category}: {row.count:,}")
    
    # Sample records
    query = f"SELECT email, name, member_count, category FROM `{table_id}` LIMIT 5"
    result = client.query(query).result()
    print("\nSample Records:")
    for row in result:
        print(f"  {row.email} - {row.member_count} members - {row.category}")
    
    # Last update time
    query = f"SELECT MAX(last_updated) as last_update FROM `{table_id}`"
    result = client.query(query).result()
    last_update = list(result)[0].last_update
    print(f"\nLast Updated: {last_update}")
    
    print("="*80)

def main():
    """Main execution"""
    import glob
    
    print("="*80)
    print("BigQuery Distribution List Upload")
    print("="*80)
    print()
    
    # Find latest CSV file
    csv_pattern = "all_distribution_lists*.csv"
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"✗ No CSV files found matching: {csv_pattern}")
        print("Please run extract_all_dls_optimized.py first")
        sys.exit(1)
    
    csv_file = max(csv_files, key=lambda x: x.split('_')[-1] if '_' in x else x)
    print(f"Using CSV file: {csv_file}")
    print()
    
    # Create BigQuery client
    client = create_bigquery_client()
    
    # Create dataset
    create_dataset_if_not_exists(client)
    
    # Create table
    create_table_if_not_exists(client)
    
    # Load data
    success = load_csv_to_bigquery(client, csv_file)
    
    if success:
        # Verify data
        verify_data(client)
        
        print()
        print("="*80)
        print("✓ BigQuery Setup Complete!")
        print("="*80)
        print()
        print("Next Steps:")
        print("1. Grant Code Puppy service account access to this table")
        print("2. Update your HTML/JavaScript to query BigQuery instead of CSV")
        print("3. Test the connection from Code Puppy Pages")
        print()
        print(f"Table: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")
        print("="*80)
    else:
        print()
        print("✗ BigQuery upload failed. Please check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
