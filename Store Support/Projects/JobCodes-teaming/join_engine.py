"""
Data Join Engine: Merge Polaris + Excel + TMS into Enriched Job Code Master
Purpose: Create complete job code dataset with all enrichment fields

Architecture:
  Polaris (271 SMART codes) [Authority]
    ↓ LEFT JOIN on job_code
  Excel Master (864 records, 50 enrichment columns)
    ↓ LEFT JOIN on job_code
  TMS Data (492 records, team/organizational structure)
    
Config: Keep all Polaris codes; NULL for unmatched enrichment
"""

import pandas as pd
import sqlite3
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class JobCodeJoinEngine:
    """Orchestrates joining Polaris + Excel + TMS data"""
    
    def __init__(self, workspace_dir):
        self.workspace = Path(workspace_dir)
        self.polaris_csv = self.workspace / "polaris_jobcodes.csv"  # From CSV provided
        self.excel_master = self.workspace / "Job_Code_Master_Table.xlsx"
        self.tms_data = self.workspace / "TMS Data (3).xlsx"
        self.output_db = self.workspace / "jobcodes_cache.db"
        
    def load_polaris_data(self):
        """Load Polaris job codes from CSV (or BigQuery extract)"""
        logger.info("Loading Polaris job codes...")
        
        try:
            # Try loading from CSV first (user-provided or BigQuery export)
            if self.polaris_csv.exists():
                df = pd.read_csv(self.polaris_csv)
                logger.info(f"✓ Loaded {len(df)} Polaris records from CSV")
                return df
            else:
                logger.warning(f"Polaris CSV not found at {self.polaris_csv}")
                return None
        except Exception as e:
            logger.error(f"Error loading Polaris data: {e}")
            return None
    
    def load_excel_enrichment(self):
        """Load Excel master data enrichment (Job_Code_Master_Table.xlsx)"""
        logger.info("Loading Excel enrichment data...")
        
        try:
            # Try openpyxl first (now installed)
            try:
                df = pd.read_excel(self.excel_master, sheet_name='Table', engine='openpyxl')
                logger.info(f"✓ Loaded {len(df)} records from Excel (openpyxl)")
                return df
            except:
                # Fallback to convert_excel_to_json if openpyxl fails
                logger.info("Falling back to JSON import from convert_excel_to_json...")
                json_file = self.workspace / "job_codes_master.json"
                if json_file.exists():
                    with open(json_file) as f:
                        data = json.load(f)
                    df = pd.DataFrame(data)
                    logger.info(f"✓ Loaded {len(df)} records from JSON export")
                    return df
                else:
                    raise FileNotFoundError(f"Excel file not found: {self.excel_master}")
        
        except Exception as e:
            logger.error(f"Error loading Excel enrichment: {e}")
            return None
    
    def load_tms_data(self):
        """Load TMS organizational structure data"""
        logger.info("Loading TMS data...")
        
        try:
            df = pd.read_excel(self.tms_data, sheet_name='Sheet1', engine='openpyxl')
            logger.info(f"✓ Loaded {len(df)} TMS records")
            
            # Ensure job_code column exists and is consistently named
            if 'jobCode' in df.columns:
                df['job_code'] = df['jobCode']
            
            return df
        
        except Exception as e:
            logger.error(f"Error loading TMS data: {e}")
            return None
    
    def normalize_job_codes(self, df, code_column='job_code'):
        """Normalize job code format for matching (remove whitespace, consistent case)"""
        if code_column in df.columns:
            df[code_column] = df[code_column].str.strip().str.upper()
        return df
    
    def join_datasets(self, polaris_df, excel_df, tms_df):
        """
        Execute LEFT JOINs to merge datasets
        
        Strategy: Polaris is authority (keep all)
        Returns: Enriched dataset with all columns from all sources
        """
        
        logger.info("Starting data joins...")
        
        # Step 1: Normalize job codes across all frames
        polaris_df = self.normalize_job_codes(polaris_df, 'job_code')
        excel_df = self.normalize_job_codes(excel_df, 'job_code')
        tms_df = self.normalize_job_codes(tms_df, 'job_code')
        
        logger.info(f"Polaris: {len(polaris_df)} codes")
        logger.info(f"Excel: {len(excel_df)} enrichment records")
        logger.info(f"TMS: {len(tms_df)} organizational records")
        
        # Step 2: Left join Polaris + Excel on job_code
        logger.info("Joining Polaris ← Excel enrichment...")
        
        # Select key enrichment columns from Excel (avoid duplication)
        excel_cols = ['job_code', 'category', 'job_family', 'pg_level', 
                      'description', 'workday_job_code']  # Adjust to actual Excel columns
        excel_subset = excel_df[[col for col in excel_cols if col in excel_df.columns]]
        
        merged = polaris_df.merge(
            excel_subset,
            on='job_code',
            how='left',
            indicator=False,
            suffixes=('', '_excel')
        )
        
        matched_count = merged['category'].notna().sum()
        logger.info(f"  ✓ Matched {matched_count}/{len(polaris_df)} Polaris codes to Excel enrichment")
        
        # Step 3: Left join result + TMS on job_code
        logger.info("Joining enriched result ← TMS organizational data...")
        
        # Select key TMS columns
        tms_cols = ['job_code', 'teamName', 'teamId', 'baseDivisionCode', 
                   'bannerCode', 'role', 'workgroupId', 'workgroupName']
        tms_subset = tms_df[[col for col in tms_cols if col in tms_df.columns]]
        
        final = merged.merge(
            tms_subset,
            on='job_code',
            how='left',
            indicator=False,
            suffixes=('', '_tms')
        )
        
        matched_tms = final['teamName'].notna().sum()
        logger.info(f"  ✓ Matched {matched_tms}/{len(final)} codes to TMS organizational data")
        
        logger.info(f"\nFinal enriched dataset: {len(final)} records, {len(final.columns)} columns")
        
        return final
    
    def save_to_database(self, df, table_name='enriched_job_codes'):
        """Save merged dataset to SQLite database"""
        logger.info(f"Saving to database: {self.output_db}")
        
        try:
            conn = sqlite3.connect(self.output_db)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            logger.info(f"✓ Saved {len(df)} records to {table_name} table")
            return True
        
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return False
    
    def save_to_csv(self, df, output_name='enriched_job_codes.csv'):
        """Save merged dataset to CSV"""
        logger.info(f"Saving to CSV: {output_name}")
        
        try:
            output_path = self.workspace / output_name
            df.to_csv(output_path, index=False)
            logger.info(f"✓ Saved {len(df)} records to {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return None
    
    def execute_full_pipeline(self):
        """Execute complete join pipeline"""
        logger.info("="*80)
        logger.info("JOB CODE ENRICHMENT PIPELINE")
        logger.info("="*80)
        
        # Load all datasets
        polaris = self.load_polaris_data()
        excel = self.load_excel_enrichment()
        tms = self.load_tms_data()
        
        if polaris is None:
            logger.error("Cannot proceed without Polaris data")
            return None
        
        # Execute joins
        enriched = self.join_datasets(
            polaris,
            excel if excel is not None else pd.DataFrame(),
            tms if tms is not None else pd.DataFrame()
        )
        
        # Save outputs
        self.save_to_database(enriched)
        csv_path = self.save_to_csv(enriched)
        
        logger.info("="*80)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*80)
        logger.info(f"\nEnrichment Summary:")
        logger.info(f"  Total codes: {len(enriched)}")
        logger.info(f"  With Excel enrichment: {enriched['category'].notna().sum() if 'category' in enriched.columns else 'N/A'}")
        logger.info(f"  With TMS data: {enriched['teamName'].notna().sum() if 'teamName' in enriched.columns else 'N/A'}")
        
        return enriched


def main():
    """Main execution"""
    workspace = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming"
    
    engine = JobCodeJoinEngine(workspace)
    enriched_data = engine.execute_full_pipeline()
    
    if enriched_data is not None:
        print("\n" + "="*80)
        print("SAMPLE OF ENRICHED DATA:")
        print("="*80)
        print(enriched_data.head(10).to_string())


if __name__ == "__main__":
    main()
