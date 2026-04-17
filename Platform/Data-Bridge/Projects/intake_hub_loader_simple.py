#!/usr/bin/env python3
"""
Simplified Intake Hub to AH_Projects Data Loader
Loads data from 'Output - Intake Accel Council Data' (197 columns) 
into AH_Projects (48 columns) with essential field mapping

Usage:
  python intake_hub_loader_simple.py --dry-run    # Preview 10 rows
  python intake_hub_loader_simple.py --count-only # Show row count
  python intake_hub_loader_simple.py --execute    # Load all data
"""

import sys
import argparse
import logging
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT = "wmt-assetprotection-prod"
SOURCE = "`wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`"
TARGET = "`wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`"

class IntakeHubLoader:
    def __init__(self):
        self.bq_client = bigquery.Client(project=PROJECT)
        logger.info(f"BigQuery client initialized for {PROJECT}")

    def get_count(self):
        """Get row count from source table."""
        query = f"SELECT COUNT(*) as cnt FROM {SOURCE} WHERE Intake_Card_Nbr IS NOT NULL"
        result = list(self.bq_client.query(query).result())[0]
        count = result.cnt
        logger.info(f"Source has {count:,} rows")
        return count

    def build_query(self):
        """Build the transformation query mapping Intake Hub → AH_Projects."""
        query = f"""
        SELECT
          -- IDENTIFIERS (3)
          CAST(Intake_Card_Nbr AS STRING) as project_id,
          CAST(Intake_Card_Nbr AS STRING) as intake_card,
          CAST(Project_Title AS STRING) as title,
          
          -- STATUS (4)
          CAST(Status AS STRING) as status,
          CAST(Phase AS STRING) as phase,
          CAST(Health_Update AS STRING) as health,
          'Intake Hub' as project_source,
          
          -- LOCATION (basic - expansion needed)
          NULL as division,
          NULL as region,
          NULL as market,
          NULL as facility,
          NULL as store_count,
          NULL as city,
          NULL as state,
          NULL as postal_code,
          NULL as latitude,
          NULL as longitude,
          CAST(Store_Area AS STRING) as store_area,
          NULL as business_area,
          
          -- TIME (6 direct, 1 computed)
          CAST(CREATED_TS AS TIMESTAMP) as created_date,
          CAST(Last_Updated AS TIMESTAMP) as last_updated,
          CAST(PROJECT_END_DATE AS DATE) as projected_completion,
          NULL as wm_week,
          NULL as fiscal_year,
          NULL as implementation_week,
          CAST(PROJECT_START_DATE AS DATE) as projected_start_date,
          
          -- OWNERSHIP (6)
          CAST(Owner AS STRING) as owner,
          NULL as owner_id,
          CAST(PROJECT_DIRECTOR AS STRING) as director,
          CAST(PROJECT_DIRECTOR_ID AS STRING) as director_id,
          CAST(PROJECT_SR_DIRECTOR AS STRING) as sr_director,
          CAST(PROJECT_SR_DIRECTOR_ID AS STRING) as sr_director_id,
          
          -- CATEGORIZATION (6 - NULL for now, can be populated later)
          NULL as project_type,
          NULL as initiative_type,
          NULL as business_type,
          NULL as facility_type,
          NULL as partner,
          NULL as business_organization,
          
          -- IMPACT (4)
          CAST(ASSOCIATE_IMPACT_DESC AS STRING) as associate_impact,
          CAST(CUSTOMER_IMPACT_DESC AS STRING) as customer_impact,
          NULL as ho_impact,
          NULL as impact,
          
          -- AMP_MEETING (5 - NULL for now)
          NULL as amp_event_id,
          NULL as amp_activity_title,
          CAST(Meeting_Type AS STRING) as meeting_type,
          CAST(SIF_Date AS DATE) as sif_date,
          CAST(AIM_Date AS DATE) as aim_date,
          
          -- DESCRIPTION (3)
          CAST(PRESENTATION_SUMMARY AS STRING) as summary,
          CAST(OVERVIEW AS STRING) as overview,
          CAST(Project_Update AS STRING) as project_update
          
        FROM {SOURCE}
        WHERE Intake_Card_Nbr IS NOT NULL
        """
        return query

    def dry_run(self, limit=10):
        """Run transformation query; show first N rows."""
        logger.info(f"DRY RUN: Executing transformation query with limit {limit}")
        
        query = self.build_query() + f" LIMIT {limit}"
        
        try:
            results = list(self.bq_client.query(query).result(max_results=limit))
            logger.info(f"\nSample Output ({len(results)} rows):\n")
            
            if results:
                for i, row in enumerate(results[:3], 1):
                    logger.info(f"Row {i}:")
                    for k, v in dict(row).items():
                        val_str = str(v)[:50] if v else "NULL"
                        logger.info(f"  {k}: {val_str}")
                    logger.info("")
            
            logger.info(f"DRY RUN COMPLETE - No data written")
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False

    def execute(self):
        """Execute full data load."""
        logger.info("="*80)
        logger.info("EXECUTING FULL DATA LOAD")
        logger.info("="*80)
        
        confirm = input("\nThis will INSERT all Intake Hub data into AH_Projects.\nContinue? (yes/no): ")
        if confirm.lower() != "yes":
            logger.info("Cancelled")
            return
        
        query = self.build_query()
        
        try:
            logger.info("Appending data to AH_Projects...")
            config = bigquery.QueryJobConfig(
                destination=TARGET,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
            )
            
            job = self.bq_client.query(query, job_config=config)
            job.result()
            
            logger.info(f"✓ Load complete! Rows written: {job.output_rows:,}")
            logger.info(f"  Query bytes processed: {job.total_bytes_processed/(1024**3):.2f} GB")
            
            # Verify
            verify_query = f"SELECT COUNT(*) as total FROM {TARGET}"
            total = list(self.bq_client.query(verify_query).result())[0].total
            logger.info(f"✓ AH_Projects now contains {total:,} rows")
            
        except Exception as e:
            logger.error(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Load Intake Hub data to AH_Projects")
    parser.add_argument('--dry-run', action='store_true', help='Preview 10 rows')
    parser.add_argument('--count-only', action='store_true', help='Show source count')
    parser.add_argument('--execute', action='store_true', help='Execute full load')
    
    args = parser.parse_args()
    loader = IntakeHubLoader()
    
    try:
        if args.dry_run:
            loader.dry_run(limit=10)
        elif args.count_only:
            loader.get_count()
        elif args.execute:
            loader.execute()
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
