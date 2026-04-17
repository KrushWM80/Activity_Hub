#!/usr/bin/env python3
"""
==================================================================================
Intake Hub to AH_Projects Data Loader
==================================================================================
Purpose:
  Load project data from Intake Hub Accel Council Data table (197 columns)
  into Activity Hub AH_Projects table (48 columns) with full schema alignment

Data Flow:
  Output - Intake Accel Council Data (BigQuery, wmt-assetprotection-prod)
           ↓
  Data Mapping & Transformation (Python)
           ↓
  AH_Projects Table (wmt-assetprotection-prod.Store_Support_Dev.AH_Projects)

Configuration:
  - Source Project: wmt-assetprotection-prod
  - Source Dataset: us_walmart
  - Source Table: Output - Intake Accel Council Data
  - Target Project: wmt-assetprotection-prod
  - Target Dataset: Store_Support_Dev
  - Target Table: AH_Projects

Usage:
  # DRY RUN (preview 10 rows, no data written)
  python intake_hub_to_ah_projects_loader.py --dry-run

  # FULL LOAD (insert all data)
  python intake_hub_to_ah_projects_loader.py --execute

  # COUNT ONLY (show counts without loading)
  python intake_hub_to_ah_projects_loader.py --count-only

Author: Kendall Rush
Last Updated: April 17, 2026
==================================================================================
"""

import os
import sys
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

from google.cloud import bigquery
from google.oauth2 import service_account

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID = "wmt-assetprotection-prod"
SOURCE_DATASET = "Store_Support_Dev"
SOURCE_TABLE = "Output - Intake Accel Council Data"
TARGET_DATASET = "Store_Support_Dev"
TARGET_TABLE = "AH_Projects"

# Intake Hub Column Mappings (source_col_name -> (target_col_name, data_type, transformation))
INTAKE_HUB_MAPPINGS = {
    # IDENTIFIERS (3 fields)
    "Intake_Card_Nbr": ("project_id", "STRING", "passthrough"),
    "Project_Title": ("title", "STRING", "passthrough"),
    
    # STATUS (4 fields)
    "Project_Status": ("status", "STRING", "passthrough"),
    "Project_Phase": ("phase", "STRING", "passthrough"),
    "Health_Status": ("health", "STRING", "passthrough"),
    
    # LOCATION (12 fields)
    "Division_Cd": ("division", "STRING", "passthrough"),
    "Region_Nm": ("region", "STRING", "passthrough"),
    "Market_Nbr": ("market", "STRING", "market_normalize"),
    "Facility_Nbr": ("facility", "STRING", "facility_normalize"),
    "City_Nm": ("city", "STRING", "passthrough"),
    "State_Cd": ("state", "STRING", "passthrough"),
    "Postal_Cd": ("postal_code", "STRING", "passthrough"),
    "Store_Area_Nm": ("store_area", "STRING", "passthrough"),
    "Business_Area_Nm": ("business_area", "STRING", "passthrough"),
    
    # TIME (7 fields - 4 direct, 3 computed)
    "Project_Create_Ts": ("created_date", "TIMESTAMP", "passthrough"),
    "Project_Update_Ts": ("last_updated", "TIMESTAMP", "passthrough"),
    "Project_Completion_Target_Dt": ("projected_completion", "DATE", "passthrough"),
    "Project_Start_Target_Dt": ("projected_start_date", "DATE", "passthrough"),
    
    # OWNERSHIP (6 fields - 3 names direct, 3 IDs require lookup)
    "Owner_Nm": ("owner", "STRING", "passthrough"),
    "Director_Nm": ("director", "STRING", "passthrough"),
    "Senior_Director_Nm": ("sr_director", "STRING", "passthrough"),
    
    # CATEGORIZATION (6 fields)
    "Project_Type": ("project_type", "STRING", "passthrough"),
    "Initiative_Type": ("initiative_type", "STRING", "passthrough"),
    "Business_Type": ("business_type", "STRING", "passthrough"),
    "Facility_Type": ("facility_type", "STRING", "passthrough"),
    "Partner_Nm": ("partner", "STRING", "passthrough"),
    "Business_Organization": ("business_organization", "STRING", "passthrough"),
    
    # IMPACT (4 fields)
    "Associate_Impact_Desc": ("associate_impact", "STRING", "passthrough"),
    "Customer_Impact_Desc": ("customer_impact", "STRING", "passthrough"),
    "HO_Impact_Desc": ("ho_impact", "STRING", "passthrough"),
    "Overall_Impact_Desc": ("impact", "STRING", "passthrough"),
    
    # AMP_MEETING (5 fields)
    "AMP_Event_ID": ("amp_event_id", "STRING", "passthrough"),
    "AMP_Activity_Title": ("amp_activity_title", "STRING", "passthrough"),
    "Meeting_Type": ("meeting_type", "STRING", "passthrough"),
    "SIF_Meeting_Date": ("sif_date", "DATE", "passthrough"),
    "AIM_Meeting_Date": ("aim_date", "DATE", "passthrough"),
    
    # DESCRIPTION (3 fields)
    "Project_Summary": ("summary", "STRING", "passthrough"),
    "Project_Overview": ("overview", "STRING", "passthrough"),
    "Project_Update_Desc": ("project_update", "STRING", "passthrough"),
}

# ============================================================================
# LOGGER SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATA TRANSFORMATIONS
# ============================================================================

def normalize_market(value):
    """Normalize market to 3-digit format with leading zeros."""
    if not value:
        return None
    try:
        market_int = int(str(value).strip())
        return f"{market_int:03d}"
    except (ValueError, TypeError):
        return None

def normalize_facility(value):
    """Convert facility number to string; handle multiple stores as comma-delimited."""
    if not value:
        return None
    return str(value).strip()

def calculate_store_count(facility_str):
    """Calculate number of stores from comma-delimited facility string."""
    if not facility_str:
        return None
    try:
        stores = [s.strip() for s in str(facility_str).split(",") if s.strip()]
        return len(stores)
    except:
        return 1

def calculate_wm_week(date_value):
    """
    Calculate Walmart week from date.
    WM Year: Feb 1 - Jan 31
    WM Weeks: 52-53 weeks per year, mostly 7-day weeks
    """
    if not date_value:
        return None
    try:
        if isinstance(date_value, str):
            date_value = datetime.fromisoformat(date_value.split(" ")[0])
        
        # Walmart fiscal year starts Feb 1
        year_start = datetime(date_value.year, 2, 1)
        if date_value < year_start:
            year_start = datetime(date_value.year - 1, 2, 1)
        
        days_diff = (date_value - year_start).days
        wm_week = (days_diff // 7) + 1
        return min(wm_week, 53)
    except:
        return None

def calculate_fiscal_year(date_value):
    """Calculate Walmart fiscal year from date (Feb 1 - Jan 31)."""
    if not date_value:
        return None
    try:
        if isinstance(date_value, str):
            date_value = datetime.fromisoformat(date_value.split(" ")[0])
        
        if date_value.month >= 2:
            return date_value.year
        else:
            return date_value.year - 1
    except:
        return None

def lookup_employee_id(name, bq_client, location_id="polaris-analytics-prod"):
    """
    Look up employee ID from Polaris schedule data using employee name.
    Returns first matching worker_id for given name.
    """
    if not name or not isinstance(name, str):
        return None
    
    try:
        # Parse name (assumes "FirstName LastName" format)
        name_parts = str(name).strip().split()
        if len(name_parts) < 2:
            return None
        
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:])
        
        query = f"""
        SELECT DISTINCT worker_id
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE first_name = '{first_name}'
          AND last_name = '{last_name}'
        LIMIT 1
        """
        
        results = bq_client.query(query).result()
        for row in results:
            return str(row.worker_id)
        return None
    except Exception as e:
        logger.warning(f"Failed to lookup employee ID for '{name}': {e}")
        return None

# ============================================================================
# DATA LOADER
# ============================================================================

class IntakeHubLoader:
    def __init__(self, project_id=PROJECT_ID):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        logger.info(f"Initialized BigQuery client for project: {project_id}")

    def build_transform_query(self, limit_rows=None):
        """Build transformation query that maps Intake Hub → AH_Projects schema."""
        
        limit_clause = f"LIMIT {limit_rows}" if limit_rows else ""
        
        # Quote table names properly for BigQuery (handle spaces in names)
        source_table_ref = f"`{self.project_id}.{SOURCE_DATASET}.{SOURCE_TABLE}`"
        target_table_ref = f"`{self.project_id}.{TARGET_DATASET}.{TARGET_TABLE}`"
        
        query = f"""
        SELECT
          -- IDENTIFIERS
          CAST(Intake_Card_Nbr AS STRING) as project_id,
          CAST(Intake_Card_Nbr AS STRING) as intake_card,
          CAST(Project_Title AS STRING) as title,
          
          -- STATUS
          CAST(Project_Status AS STRING) as status,
          CAST(Project_Phase AS STRING) as phase,
          COALESCE(CAST(Health_Status AS STRING), 'Unknown') as health,
          'Intake Hub' as project_source,
          
          -- LOCATION
          CAST(Division_Cd AS STRING) as division,
          CAST(Region_Nm AS STRING) as region,
          FORMAT('%03d', CAST(Market_Nbr AS INT64)) as market,
          CAST(Facility_Nbr AS STRING) as facility,
          1 as store_count,  -- TODO: Update once multi-facility data available
          CAST(City_Nm AS STRING) as city,
          CAST(State_Cd AS STRING) as state,
          CAST(Postal_Cd AS STRING) as postal_code,
          NULL as latitude,
          NULL as longitude,
          CAST(Store_Area_Nm AS STRING) as store_area,
          CAST(Business_Area_Nm AS STRING) as business_area,
          
          -- TIME
          CAST(Project_Create_Ts AS TIMESTAMP) as created_date,
          CAST(Project_Update_Ts AS TIMESTAMP) as last_updated,
          CAST(Project_Completion_Target_Dt AS DATE) as projected_completion,
          -- WM_WEEK and FISCAL_YEAR: Calculate from created_date
          MOD(CAST(FLOOR(DATE_DIFF(CAST(Project_Create_Ts AS DATE), DATE('2026-02-01'), DAY) / 7) + 1 AS INT64), 53) as wm_week,
          IF(
            EXTRACT(MONTH FROM CAST(Project_Create_Ts AS DATE)) >= 2,
            EXTRACT(YEAR FROM CAST(Project_Create_Ts AS DATE)),
            EXTRACT(YEAR FROM CAST(Project_Create_Ts AS DATE)) - 1
          ) as fiscal_year,
          NULL as implementation_week,
          CAST(Project_Start_Target_Dt AS DATE) as projected_start_date,
          
          -- OWNERSHIP (names only - IDs require separate lookup)
          CAST(Owner_Nm AS STRING) as owner,
          NULL as owner_id,  -- TODO: Populate via Polaris lookup
          CAST(Director_Nm AS STRING) as director,
          NULL as director_id,  -- TODO: Populate via Polaris lookup
          CAST(Senior_Director_Nm AS STRING) as sr_director,
          NULL as sr_director_id,  -- TODO: Populate via Polaris lookup
          
          -- CATEGORIZATION
          CAST(Project_Type AS STRING) as project_type,
          CAST(Initiative_Type AS STRING) as initiative_type,
          CAST(Business_Type AS STRING) as business_type,
          CAST(Facility_Type AS STRING) as facility_type,
          CAST(Partner_Nm AS STRING) as partner,
          CAST(Business_Organization AS STRING) as business_organization,
          
          -- IMPACT
          CAST(Associate_Impact_Desc AS STRING) as associate_impact,
          CAST(Customer_Impact_Desc AS STRING) as customer_impact,
          CAST(HO_Impact_Desc AS STRING) as ho_impact,
          CAST(Overall_Impact_Desc AS STRING) as impact,
          
          -- AMP_MEETING
          CAST(AMP_Event_ID AS STRING) as amp_event_id,
          CAST(AMP_Activity_Title AS STRING) as amp_activity_title,
          CAST(Meeting_Type AS STRING) as meeting_type,
          CAST(SIF_Meeting_Date AS DATE) as sif_date,
          CAST(AIM_Meeting_Date AS DATE) as aim_date,
          
          -- DESCRIPTION
          CAST(Project_Summary AS STRING) as summary,
          CAST(Project_Overview AS STRING) as overview,
          CAST(Project_Update_Desc AS STRING) as project_update
          
        FROM {source_table_ref}
        WHERE Intake_Card_Nbr IS NOT NULL
        {limit_clause}
        """
        
        return query

    def dry_run(self, limit_rows=10):
        """Run transformation query in dry-run mode (read-only, show preview)."""
        logger.info(f"Starting DRY RUN with limit {limit_rows} rows...")
        
        query = self.build_transform_query(limit_rows=limit_rows)
        logger.info(f"Running transformation query...")
        
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
        job = self.bq_client.query(query, job_config=job_config)
        
        # Dry run doesn't execute, just estimates
        logger.info(f"Query would scan {job.total_bytes_processed / (1024**3):.2f} GB")
        logger.info(f"Query would process {job.total_bytes_billed / (1024**3):.2f} GB (billable)")
        
        # Run actual query for preview
        logger.info(f"Executing query for row preview...")
        query_job = self.bq_client.query(query)
        results = query_job.result(max_results=limit_rows)
        
        logger.info(f"\nSample Output ({limit_rows} rows):")
        logger.info("=" * 120)
        
        rows_list = list(results)
        if rows_list:
            # Show column names
            columns = list(rows_list[0].keys())
            logger.info(f"Columns: {columns}")
            logger.info("")
            
            # Show first few rows
            for i, row in enumerate(rows_list[:3], 1):
                logger.info(f"Row {i}: {dict(row)}")
            
            if len(rows_list) > 3:
                logger.info(f"... and {len(rows_list) - 3} more rows")
        else:
            logger.warning("No rows returned from query")
        
        logger.info("=" * 120)
        logger.info("DRY RUN COMPLETE - No data written to target table")

    def count_source(self):
        """Get row count from source Intake Hub table."""
        logger.info("Checking source Intake Hub table...")
        
        source_table_ref = f"`{self.project_id}.{SOURCE_DATASET}.{SOURCE_TABLE}`"
        
        count_query = f"""
        SELECT COUNT(*) as row_count
        FROM {source_table_ref}
        WHERE Intake_Card_Nbr IS NOT NULL
        """
        
        results = self.bq_client.query(count_query).result()
        for row in results:
            count = row.row_count
            logger.info(f"Source table has {count:,} valid rows (with Intake_Card_Nbr)")
            return count

    def execute_load(self):
        """Execute full data load from Intake Hub → AH_Projects."""
        logger.info("="*100)
        logger.info("STARTING FULL DATA LOAD: Intake Hub → AH_Projects")
        logger.info("="*100)
        
        # Check source
        source_count = self.count_source()
        
        # Build transformation query
        query = self.build_transform_query()
        
        # Insert data
        logger.info(f"\nInserting transformed data into {TARGET_DATASET}.{TARGET_TABLE}...")
        
        job_config = bigquery.QueryJobConfig(
            destination=f"{self.project_id}.{TARGET_DATASET}.{TARGET_TABLE}",
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        
        query_job = self.bq_client.query(query, job_config=job_config)
        query_job.result()
        
        logger.info(f"✓ Data load complete!")
        logger.info(f"  Rows written: {query_job.output_rows}")
        logger.info(f"  Total bytes processed: {query_job.total_bytes_processed / (1024**3):.2f} GB")
        
        # Verify load
        verify_query = f"""
        SELECT 
          COUNT(*) as total_rows,
          COUNT(DISTINCT project_id) as unique_projects,
          MIN(created_date) as earliest_date,
          MAX(created_date) as latest_date
        FROM `{self.project_id}.{TARGET_DATASET}.{TARGET_TABLE}`
        """
        
        logger.info("\nVerifying loaded data...")
        results = self.bq_client.query(verify_query).result()
        for row in results:
            logger.info(f"  Total rows: {row.total_rows:,}")
            logger.info(f"  Unique projects: {row.unique_projects:,}")
            logger.info(f"  Date range: {row.earliest_date} to {row.latest_date}")
        
        logger.info("="*100)

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Load Intake Hub data into AH_Projects table"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (read-only, show preview)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute full data load"
    )
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Show source row count without loading"
    )
    
    args = parser.parse_args()
    
    try:
        loader = IntakeHubLoader()
        
        if args.dry_run:
            loader.dry_run(limit_rows=10)
        elif args.count_only:
            loader.count_source()
        elif args.execute:
            confirm = input("\n⚠️  WARNING: This will load data into AH_Projects table.\nContinue? (yes/no): ")
            if confirm.lower() == "yes":
                loader.execute_load()
            else:
                logger.info("Load cancelled by user")
        else:
            parser.print_help()
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
