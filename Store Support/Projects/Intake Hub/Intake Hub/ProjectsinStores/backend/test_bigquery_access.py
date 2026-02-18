#!/usr/bin/env python3
"""
Test script to verify BigQuery access to wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data

Run this after setting up authentication:
  Option 1: gcloud auth application-default login
  Option 2: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

Then: python test_bigquery_access.py
"""

import os
import sys
from datetime import datetime

def test_bigquery_access():
    """Test connection and permissions to BigQuery table."""
    
    print("\n" + "="*70)
    print("BigQuery Access Test")
    print("="*70)
    
    # Check authentication method
    print("\n📋 Checking Authentication Setup...")
    creds_env = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_env:
        print(f"✅ GOOGLE_APPLICATION_CREDENTIALS: {creds_env}")
        if not os.path.exists(creds_env):
            print(f"   ❌ File not found: {creds_env}")
            return False
    else:
        print("⚠️  GOOGLE_APPLICATION_CREDENTIALS not set (will use gcloud CLI if available)")
    
    # Import BigQuery client
    print("\n📦 Importing google-cloud-bigquery...")
    try:
        from google.cloud import bigquery
        print("✅ Successfully imported google.cloud.bigquery")
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        print("   Install with: pip install google-cloud-bigquery")
        return False
    
    # Initialize client
    print("\n🔗 Initializing BigQuery Client...")
    try:
        client = bigquery.Client(project="wmt-assetprotection-prod")
        print("✅ BigQuery client initialized")
        print(f"   Project: {client.project}")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        print("   Check: gcloud auth application-default login")
        return False
    
    # Get dataset
    print("\n📂 Accessing Dataset...")
    dataset_id = "Store_Support_Dev"
    try:
        dataset = client.get_dataset(dataset_id)
        print(f"✅ Dataset found: {dataset.project}.{dataset.dataset_id}")
        print(f"   Description: {dataset.description}")
        print(f"   Created: {dataset.created}")
    except Exception as e:
        print(f"❌ Failed to access dataset '{dataset_id}': {e}")
        print("   Check: Do you have permissions to Store_Support_Dev?")
        return False
    
    # Get table
    print("\n📋 Accessing Table...")
    table_id = "IH_Intake_Data"
    try:
        table = client.get_table(f"{dataset_id}.{table_id}")
        print(f"✅ Table found: {table.project}.{table.dataset_id}.{table.table_id}")
        print(f"   Rows: {table.num_rows:,}")
        print(f"   Bytes: {table.num_bytes:,}")
        print(f"   Created: {table.created}")
        print(f"   Modified: {table.modified}")
    except Exception as e:
        print(f"❌ Failed to access table '{table_id}': {e}")
        return False
    
    # List columns
    print("\n📊 Table Schema (First 10 Columns)...")
    try:
        schema = table.schema
        print(f"✅ Total columns: {len(schema)}")
        print("\n   Column Name              | Type       | Mode")
        print("   " + "-"*60)
        for field in schema[:10]:
            print(f"   {field.name:25} | {field.field_type:10} | {field.mode}")
        if len(schema) > 10:
            print(f"   ... and {len(schema) - 10} more columns")
    except Exception as e:
        print(f"❌ Failed to read schema: {e}")
        return False
    
    # Run test query
    print("\n🔍 Running Test Query...")
    query = f"""
    SELECT 
      COUNT(*) as total_rows,
      COUNT(DISTINCT Project_Title) as unique_projects,
      COUNT(DISTINCT Facility) as unique_stores,
      MAX(Last_Updated) as latest_update
    FROM `{dataset_id}.{table_id}`
    WHERE Status = 'Active'
    """
    
    try:
        query_job = client.query(query, project="wmt-assetprotection-prod")
        results = query_job.result()
        
        print("✅ Query executed successfully!")
        print("\n   Result:")
        for row in results:
            print(f"      Total Active Rows:        {row['total_rows']:,}")
            print(f"      Unique Projects:          {row['unique_projects']:,}")
            print(f"      Unique Stores:            {row['unique_stores']:,}")
            print(f"      Latest Update:            {row['latest_update']}")
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False
    
    # Summary
    print("\n" + "="*70)
    print("✅ All Tests Passed! You have full BigQuery access.")
    print("="*70)
    print("\nYou can now:")
    print("  1. Run the backend: python backend/main.py")
    print("  2. API will query BigQuery and cache results in SQLite")
    print("  3. Open http://localhost:8002 in browser")
    print("\n")
    
    return True

if __name__ == "__main__":
    success = test_bigquery_access()
    sys.exit(0 if success else 1)
