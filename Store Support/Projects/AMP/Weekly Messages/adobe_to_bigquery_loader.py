#!/usr/bin/env python3
"""
Adobe Analytics to BigQuery Data Loader
Parses weekly Adobe Analytics Excel exports and loads to BigQuery tables.

Usage:
    python adobe_to_bigquery_loader.py
    
Configuration:
    adobe_config.yaml (must be in same directory as this script)
"""

import os
import sys
import logging
import yaml
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, List
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError, NotFound

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(config: Dict) -> logging.Logger:
    """Initialize logging to file and console."""
    log_dir = config['logging']['log_dir']
    log_file = config['logging']['log_file']
    log_level = config['logging']['log_level']
    
    # Create log directory if needed
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / log_file
    
    # Configure logging
    logger = logging.getLogger('adobe_loader')
    logger.setLevel(getattr(logging, log_level))
    
    # File handler
    fh = logging.FileHandler(log_path)
    fh.setLevel(getattr(logging, log_level))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# ============================================================================
# CONFIGURATION LOADING
# ============================================================================

def load_config() -> Dict:
    """Load configuration from adobe_config.yaml."""
    config_path = Path(__file__).parent / 'adobe_config.yaml'
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

# ============================================================================
# BIGQUERY CLIENT
# ============================================================================

def init_bigquery_client(project_id: str, logger: logging.Logger) -> bigquery.Client:
    """Initialize BigQuery client."""
    try:
        client = bigquery.Client(project=project_id)
        logger.info(f"BigQuery client initialized for project: {project_id}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize BigQuery client: {e}", exc_info=True)
        raise

# ============================================================================
# WEEKLY MESSAGES PARSING
# ============================================================================

def parse_weekly_messages_file(file_path: str, logger: logging.Logger) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parse Weekly Messages FY27 Excel file.
    Returns two DataFrames: devices and metrics.
    """
    logger.info(f"Parsing Weekly Messages file: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Weekly Messages file not found: {file_path}")
    
    # Read Excel file
    try:
        xl_file = pd.ExcelFile(file_path)
        logger.info(f"Excel file loaded. Sheet names: {xl_file.sheet_names[:5]}...")  # Log first 5
    except Exception as e:
        logger.error(f"Failed to read Excel file: {e}", exc_info=True)
        raise
    
    # Category sections to extract
    categories = [
        'Fashion', 'Home', 'Fresh', 'Frontend', 'Hardlines', 'Backroom', 'People',
        'Asset Protection', 'Entertainment', 'MM Overview', 'Consumables and OTC',
        'Food', 'Store Fulfillment', 'Seasonal'
    ]
    
    devices_rows = []
    metrics_rows = []
    report_date = datetime.now().date()  # Use today or from config
    extracted_date = datetime.now()
    
    try:
        # Read all sheets
        for sheet_name in xl_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Try to match sheet to category
            matched_category = None
            for cat in categories:
                if cat.lower() in sheet_name.lower():
                    matched_category = cat
                    break
            
            if matched_category is None:
                logger.debug(f"Skipping sheet (no category match): {sheet_name}")
                continue
            
            # Parse device-level table (first numeric table)
            try:
                device_cols = ['Tablets', 'Desktop', 'Store Devices', 'Mobile Phones', 'XCover']
                device_subset = df[[col for col in device_cols if col in df.columns]]
                
                if not device_subset.empty:
                    # Extract page names and device values
                    for idx, row in df.iterrows():
                        page_name = row.iloc[0] if len(row) > 0 else None
                        if page_name is None or pd.isna(page_name):
                            continue
                        
                        device_values = {col: row.get(col, 0) for col in device_cols}
                        total = sum([v for v in device_values.values() if isinstance(v, (int, float))])
                        
                        devices_rows.append({
                            'report_date': report_date,
                            'category': matched_category,
                            'page_name': str(page_name),
                            'tablets_page_views': device_values.get('Tablets', 0),
                            'desktop_page_views': device_values.get('Desktop', 0),
                            'store_devices_page_views': device_values.get('Store Devices', 0),
                            'mobile_phones_page_views': device_values.get('Mobile Phones', 0),
                            'xcover_devices_page_views': device_values.get('XCover', 0),
                            'total_page_views': total,
                            'extracted_date': extracted_date
                        })
            except Exception as e:
                logger.warning(f"Error parsing device data in {sheet_name}: {e}")
            
            # Parse metrics table (Unique Users, Average Time, Visits, etc.)
            try:
                metric_cols = ['Page Views', 'Unique Users', 'Average Time on Site', 'Visits']
                metric_subset = df[[col for col in metric_cols if col in df.columns]]
                
                if not metric_subset.empty:
                    for idx, row in df.iterrows():
                        page_name = row.iloc[0] if len(row) > 0 else None
                        if page_name is None or pd.isna(page_name):
                            continue
                        
                        metrics_rows.append({
                            'report_date': report_date,
                            'category': matched_category,
                            'page_name': str(page_name),
                            'page_views': row.get('Page Views', 0),
                            'unique_users': row.get('Unique Users', 0.0),
                            'average_time_on_site': row.get('Average Time on Site', 0.0),
                            'visits': row.get('Visits', 0),
                            'extracted_date': extracted_date
                        })
            except Exception as e:
                logger.warning(f"Error parsing metrics in {sheet_name}: {e}")
    
    except Exception as e:
        logger.error(f"Error during Weekly Messages parsing: {e}", exc_info=True)
        raise
    
    devices_df = pd.DataFrame(devices_rows)
    metrics_df = pd.DataFrame(metrics_rows)
    
    logger.info(f"Weekly Messages parsed: {len(devices_df)} device rows, {len(metrics_df)} metric rows")
    
    return devices_df, metrics_df

# ============================================================================
# PLAYBOOK HUB PARSING
# ============================================================================

def parse_playbook_hub_file(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Parse Playbook Hub FY27 Excel file.
    Returns DataFrame with playbook metrics.
    """
    logger.info(f"Parsing Playbook Hub file: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Playbook Hub file not found: {file_path}")
    
    try:
        xl_file = pd.ExcelFile(file_path)
        logger.info(f"Excel file loaded. Sheet count: {len(xl_file.sheet_names)}")
    except Exception as e:
        logger.error(f"Failed to read Playbook Hub file: {e}", exc_info=True)
        raise
    
    playbook_categories = ['Playbook Hub', 'Valentines', 'Baby Days', 'Easter']
    playbook_rows = []
    report_date = datetime.now().date()
    extracted_date = datetime.now()
    
    try:
        for sheet_name in xl_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Match Sheet to playbook category
            matched_category = None
            for cat in playbook_categories:
                if cat.lower() in sheet_name.lower():
                    matched_category = cat
                    break
            
            if matched_category is None:
                logger.debug(f"Skipping sheet (no playbook match): {sheet_name}")
                continue
            
            # Extract page views by user type
            try:
                for idx, row in df.iterrows():
                    page_name = row.iloc[0] if len(row) > 0 else None
                    if page_name is None or pd.isna(page_name) or str(page_name).strip() == '':
                        continue
                    
                    # Expected columns: Page Views, Store Salary Associates, Store Hourly Associates
                    playbook_rows.append({
                        'report_date': report_date,
                        'playbook_category': matched_category,
                        'page_name': str(page_name),
                        'total_page_views': row.get('Page Views', 0),
                        'store_salary_associates_views': row.get('Store Salary Associates', 0),
                        'store_hourly_associates_views': row.get('Store Hourly Associates', 0),
                        'report_period_start': None,  # Could be extracted from header
                        'report_period_end': None,
                        'extracted_date': extracted_date
                    })
            except Exception as e:
                logger.warning(f"Error parsing playbook data in {sheet_name}: {e}")
    
    except Exception as e:
        logger.error(f"Error during Playbook Hub parsing: {e}", exc_info=True)
        raise
    
    playbook_df = pd.DataFrame(playbook_rows)
    logger.info(f"Playbook Hub parsed: {len(playbook_df)} rows")
    
    return playbook_df

# ============================================================================
# BIGQUERY LOADING (MERGE/UPSERT)
# ============================================================================

def load_to_bigquery(
    client: bigquery.Client,
    df: pd.DataFrame,
    table_id: str,
    merge_keys: List[str],
    logger: logging.Logger,
    dataset_suffix: str = ""
) -> int:
    """
    Load DataFrame to BigQuery using MERGE (idempotent upsert).
    Returns count of rows inserted/updated.
    
    Args:
        dataset_suffix: Optional suffix to append to table_id for dataset identification
    """
    if df.empty:
        logger.warning(f"No data to load for {table_id}")
        return 0
    
    try:
        # Create temporary table
        temp_table_id = f"{table_id}_temp_{int(datetime.now().timestamp())}"
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        
        logger.info(f"Loading {len(df)} rows to temp table {temp_table_id}")
        load_job = client.load_table_from_dataframe(df, temp_table_id, job_config=job_config)
        load_job.result()
        logger.info(f"Temp table created: {temp_table_id}")
        
        # Build MERGE query
        merge_on_clause = " AND ".join([f"T.{key} = S.{key}" for key in merge_keys])
        update_cols = [col for col in df.columns if col not in merge_keys]
        update_set = ", ".join([f"T.{col} = S.{col}" for col in update_cols])
        insert_cols = ", ".join(df.columns)
        insert_values = ", ".join([f"S.{col}" for col in df.columns])
        
        merge_sql = f"""
        MERGE `{table_id}` T
        USING `{temp_table_id}` S
        ON {merge_on_clause}
        WHEN MATCHED THEN
          UPDATE SET {update_set}
        WHEN NOT MATCHED THEN
          INSERT ({insert_cols})
          VALUES ({insert_values})
        """
        
        logger.info(f"Executing MERGE for {table_id}")
        merge_job = client.query(merge_sql)
        merge_result = merge_job.result()
        logger.info(f"MERGE completed for {table_id}: {merge_result.total_rows} rows affected")
        
        # Delete temp table
        client.delete_table(temp_table_id)
        logger.info(f"Temp table deleted: {temp_table_id}")
        
        return len(df)
    
    except Exception as e:
        logger.error(f"Error loading to BigQuery ({table_id}): {e}", exc_info=True)
        raise

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"FATAL: Failed to load configuration: {e}")
        sys.exit(1)
    
    # Setup logging
    logger = setup_logging(config)
    logger.info("=" * 80)
    logger.info("Adobe Analytics to BigQuery Loader - START")
    logger.info("=" * 80)
    
    try:
        # Initialize BigQuery client
        client = init_bigquery_client(config['gcp']['project_id'], logger)
        
        # Parse Excel files
        logger.info("\n--- PHASE 1: PARSING EXCEL FILES ---")
        weekly_devices, weekly_metrics = parse_weekly_messages_file(
            config['source_files']['weekly_messages_path'],
            logger
        )
        playbook_hub = parse_playbook_hub_file(
            config['source_files']['playbook_hub_path'],
            logger
        )
        
        # Load to BigQuery
        logger.info("\n--- PHASE 2: LOADING TO BIGQUERY ---")
        
        # Construct full table IDs (use Store_Support_Dev as parent dataset)
        project = config['gcp']['project_id']
        dataset_weekly = config['bigquery']['datasets']['weekly_messages']
        dataset_playbook = config['bigquery']['datasets']['playbook_hub']
        
        weekly_devices_table = f"{project}.{dataset_weekly}.{config['bigquery']['tables']['weekly_devices']}"
        weekly_metrics_table = f"{project}.{dataset_weekly}.{config['bigquery']['tables']['weekly_metrics']}"
        playbook_table = f"{project}.{dataset_playbook}.{config['bigquery']['tables']['playbook']}"
        
        logger.info(f"Target tables:")
        logger.info(f"  - {weekly_devices_table}")
        logger.info(f"  - {weekly_metrics_table}")
        logger.info(f"  - {playbook_table}")
        
        # Load each table
        devices_count = load_to_bigquery(
            client, weekly_devices, weekly_devices_table,
            ['report_date', 'category', 'page_name'], logger
        )
        
        metrics_count = load_to_bigquery(
            client, weekly_metrics, weekly_metrics_table,
            ['report_date', 'category', 'page_name'], logger
        )
        
        playbook_count = load_to_bigquery(
            client, playbook_hub, playbook_table,
            ['report_date', 'playbook_category', 'page_name'], logger
        )
        
        # Summary
        logger.info("\n--- SUMMARY ---")
        logger.info(f"Weekly Messages Devices: {devices_count} rows")
        logger.info(f"Weekly Messages Metrics: {metrics_count} rows")
        logger.info(f"Playbook Hub: {playbook_count} rows")
        logger.info("=" * 80)
        logger.info("Adobe Analytics to BigQuery Loader - SUCCESS")
        logger.info("=" * 80)
        
        return 0
    
    except Exception as e:
        logger.error("=" * 80)
        logger.error("Adobe Analytics to BigQuery Loader - FAILED")
        logger.error("=" * 80)
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
