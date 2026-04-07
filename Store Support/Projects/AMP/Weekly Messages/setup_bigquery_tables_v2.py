#!/usr/bin/env python3
"""
BigQuery Table Setup for Adobe Analytics Pipeline
Creates required tables under existing Project_Metric_Lift dataset.

Usage:
    python setup_bigquery_tables.py

This script will:
1. Verify the Project_Metric_Lift dataset exists
2. Create 3 tables under Project_Metric_Lift with proper schema, partitioning, and clustering
"""

import sys
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, Conflict

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID = "wmt-assetprotection-prod"
DATASET_ID = "Project_Metric_Lift"

# Tables to create under Project_Metric_Lift
TABLES_CONFIG = [
    {
        "table_id": "bq_weekly_messages_devices",
        "description": "Weekly Messages device-level page views by category",
        "schema": [
            bigquery.SchemaField("report_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("page_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("tablets_page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("desktop_page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("store_devices_page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("mobile_phones_page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("xcover_devices_page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("total_page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("extracted_date", "TIMESTAMP", mode="REQUIRED"),
        ],
        "partition_field": "report_date",
        "clustering_fields": ["category", "page_name"]
    },
    {
        "table_id": "bq_weekly_messages_metrics",
        "description": "Weekly Messages aggregated metrics: page views, unique users, time, visits",
        "schema": [
            bigquery.SchemaField("report_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("page_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("unique_users", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("average_time_on_site", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("visits", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("extracted_date", "TIMESTAMP", mode="REQUIRED"),
        ],
        "partition_field": "report_date",
        "clustering_fields": ["category", "page_name"]
    },
    {
        "table_id": "bq_playbook_hub_metrics",
        "description": "Playbook Hub page views by user type (Salary/Hourly Associates)",
        "schema": [
            bigquery.SchemaField("report_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("playbook_category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("page_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("total_page_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("store_salary_associates_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("store_hourly_associates_views", "INT64", mode="NULLABLE"),
            bigquery.SchemaField("report_period_start", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("report_period_end", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("extracted_date", "TIMESTAMP", mode="REQUIRED"),
        ],
        "partition_field": "report_date",
        "clustering_fields": ["playbook_category"]
    }
]

# ============================================================================
# SETUP FUNCTIONS
# ============================================================================

def init_client(project_id: str) -> bigquery.Client:
    """Initialize BigQuery client."""
    try:
        client = bigquery.Client(project=project_id)
        print(f"✓ BigQuery client initialized for project: {project_id}")
        return client
    except Exception as e:
        print(f"✗ Failed to initialize BigQuery client: {e}")
        sys.exit(1)

def verify_dataset(client: bigquery.Client, dataset_id: str) -> bool:
    """Verify dataset exists."""
    dataset_ref = f"{PROJECT_ID}.{dataset_id}"
    
    try:
        dataset = client.get_dataset(dataset_ref)
        print(f"  ✓ Dataset verified: {dataset_ref}")
        return True
    except NotFound:
        print(f"  ✗ Dataset not found: {dataset_ref}")
        print(f"     Please create this dataset manually in BigQuery console")
        return False

def create_table(client: bigquery.Client, table_config: dict) -> bool:
    """Create a table if it doesn't exist."""
    table_id = table_config["table_id"]
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"
    
    try:
        # Check if table exists
        client.get_table(table_ref)
        print(f"  ℹ Table already exists: {table_ref}")
        return True
    except NotFound:
        # Create table
        try:
            table = bigquery.Table(table_ref, schema=table_config["schema"])
            table.description = table_config.get("description", "")
            
            # Set partitioning
            if "partition_field" in table_config:
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.DAY,
                    field=table_config["partition_field"]
                )
            
            # Set clustering
            if "clustering_fields" in table_config:
                table.clustering_fields = table_config["clustering_fields"]
            
            table = client.create_table(table)
            print(f"  ✓ Table created: {table_ref}")
            
            # Verify schema
            schema_info = ", ".join([f"{field.name} ({field.field_type})" for field in table.schema[:3]])
            print(f"      Schema: {schema_info}... ({len(table.schema)} fields)")
            
            if table_config.get("partition_field"):
                print(f"      Partition: {table_config['partition_field']}")
            if table_config.get("clustering_fields"):
                print(f"      Clustering: {', '.join(table_config['clustering_fields'])}")
            
            return True
        except Exception as e:
            print(f"  ✗ Failed to create table {table_ref}: {e}")
            return False

def verify_table_exists(client: bigquery.Client, table_id: str) -> bool:
    """Verify table exists and return row count."""
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"
    try:
        table = client.get_table(table_ref)
        print(f"  ✓ Verified: {table_ref} ({table.num_rows} rows, {len(table.schema)} columns)")
        return True
    except NotFound:
        print(f"  ✗ Table not found: {table_ref}")
        return False

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main setup function."""
    print("\n" + "=" * 100)
    print(" BigQuery Adobe Analytics Pipeline - Table Setup")
    print("=" * 100)
    print(f" Project: {PROJECT_ID}")
    print(f" Dataset: {DATASET_ID}")
    print(f" Tables: {len(TABLES_CONFIG)}\n")
    
    # Initialize BigQuery client
    print("[PHASE 1] Initializing BigQuery client...")
    client = init_client(PROJECT_ID)
    
    # Verify dataset exists
    print("\n[PHASE 2] Verifying dataset...")
    if not verify_dataset(client, DATASET_ID):
        print("\n✗ Dataset verification failed. Exiting.")
        sys.exit(1)
    
    # Create tables
    print("\n[PHASE 3] Creating tables...")
    all_tables_ok = True
    
    for config in TABLES_CONFIG:
        if not create_table(client, config):
            all_tables_ok = False
    
    if not all_tables_ok:
        print("\n✗ Some tables failed to create. Exiting.")
        sys.exit(1)
    
    # Verify all tables
    print("\n[PHASE 4] Verifying tables...")
    all_verified = True
    
    for config in TABLES_CONFIG:
        if not verify_table_exists(client, config["table_id"]):
            all_verified = False
    
    # Summary
    print("\n" + "=" * 100)
    if all_verified:
        print(" ✓ BigQuery Setup Complete!")
        print("=" * 100)
        print(f"\n Tables ready for data load:")
        for config in TABLES_CONFIG:
            print(f"  • {PROJECT_ID}.{DATASET_ID}.{config['table_id']}")
        print("\n All tables configured with:")
        print(f"  • DATE partitioning (by report_date)")
        print(f"  • Query clustering (optimized for common filters)")
        print(f"  • REQUIRED timestamp (extracted_date tracks load time)")
        print("\n" + "=" * 100)
        return 0
    else:
        print(" ✗ Setup incomplete. Please address errors above.")
        print("=" * 100)
        return 1

if __name__ == "__main__":
    sys.exit(main())
