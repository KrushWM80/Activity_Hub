#!/usr/bin/env python3
"""
TEMPORARY INTAKE HUB DATA LOADER
Purpose: Load projects from Intake Hub BigQuery table into AH_Projects
Until Data Bridge schema verification is complete

Source: wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data
Target: wmt-assetprotection-prod.Store_Support_Dev.AH_Projects

Column Mapping (temporary - may change after schema verification):
- impact_id: Unique project identifier from source
- title: Project name/title
- business_area: Category (HR, Store Ops, Supply Chain, Technology)
- owner_name: Project owner
- health_status: On Track / At Risk / Off Track
- project_status: Active / Inactive
- latest_update: Recent project news/update text
"""

from google.cloud import bigquery
from datetime import datetime
import json

def load_intake_hub_data(dry_run=False):
    """Load and transform Intake Hub data into AH_Projects format"""
    
    client = bigquery.Client()
    
    # Query source Intake Hub table
    query = """
    SELECT 
        SAFE.INT64(REGEXP_EXTRACT(CONCAT('proj-', ROW_NUMBER() OVER ()), r'proj-(\d+)')) as impact_id,
        `Title` as title,
        `Business Area` as business_area,
        `Owner Name` as owner_name,
        `Owner ID` as owner_id,
        `Health Status` as health_status,
        `Project Status` as project_status,
        `Latest Update` as latest_update,
        `Updated This Week` as current_wm_week_update,
        CURRENT_TIMESTAMP() as created_at,
        CURRENT_TIMESTAMP() as updated_at
    FROM `wmt-assetprotection-prod.Store_Support_Dev.`Output - Intake Accel Council Data``
    WHERE COALESCE(`Project Status`, '') != 'Inactive'
    LIMIT 100
    """
    
    print("🔄 Querying Intake Hub source data...")
    results = client.query(query).result()
    projects = list(results)
    
    print(f"✅ Found {len(projects)} source projects")
    
    if dry_run:
        print("\n📋 DRY RUN - Sample data (first 2 records):")
        for i, proj in enumerate(projects[:2]):
            print(json.dumps(dict(proj), indent=2, default=str))
        return {"records": len(projects), "mode": "dry_run"}
    
    # Insert into target table
    if projects:
        errors = client.insert_rows_json(
            'wmt-assetprotection-prod.Store_Support_Dev.AH_Projects',
            [dict(row) for row in projects]
        )
        
        if errors:
            print(f"❌ Insert errors: {errors}")
            return {"status": "error", "errors": errors}
        else:
            print(f"✅ Successfully inserted {len(projects)} projects")
            return {"status": "success", "records_inserted": len(projects)}
    
    return {"status": "no_data"}

def get_mapping_info():
    """Display current column mapping for verification"""
    mapping = {
        "impact_id": "Unique project ID (generated)",
        "title": "Project name/title",
        "business_area": "HR / Store Operations / Supply Chain / Technology",
        "owner_name": "Project owner name",
        "owner_id": "Project owner ID",
        "health_status": "On Track / At Risk / Off Track",
        "project_status": "Active / Inactive",
        "latest_update": "Recent project update text",
        "current_wm_week_update": "Boolean: True if updated this week",
        "created_at": "Timestamp created",
        "updated_at": "Timestamp last modified"
    }
    
    print("\n📊 TEMPORARY COLUMN MAPPING:")
    print("=" * 60)
    for field, description in mapping.items():
        print(f"  {field:30} → {description}")
    print("=" * 60)
    print("\n⚠️  VERIFY in Admin → Data Bridge → Field Configuration before going live")

if __name__ == "__main__":
    print("🚀 INTAKE HUB TEMPORARY DATA LOADER")
    print("=" * 60)
    
    # Show mapping first
    get_mapping_info()
    
    # Run dry run to show what would be loaded
    print("\n📋 Running DRY RUN (no data inserted)...")
    result = load_intake_hub_data(dry_run=True)
    print(f"Result: {result}")
    
    # Uncomment to actually insert:
    # print("\n💾 Running ACTUAL INSERT...")
    # result = load_intake_hub_data(dry_run=False)
    # print(f"Result: {result}")
