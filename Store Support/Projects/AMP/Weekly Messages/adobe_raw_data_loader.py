#!/usr/bin/env python3
"""
Adobe Analytics Raw Data Loader
Loads exact Excel data (all rows/columns as-is) to BigQuery raw tables.
Preserves metadata and formatting exactly as shown in Excel.

This loader is separate from adobe_to_bigquery_loader.py and does NOT disturb
the existing normalized data pipeline.

Usage:
    python adobe_raw_data_loader.py
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
    log_file = "adobe_raw_loader.log"
    log_level = config['logging']['log_level']
    
    # Create log directory if needed
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / log_file
    
    # Configure logging
    logger = logging.getLogger('adobe_raw_loader')
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
# RAW DATA LOADING (WINDOWS COM)
# ============================================================================

def parse_playbook_hub_raw(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Parse Playbook Hub Excel file and extract ALL rows/columns as-is.
    Returns DataFrame with exact Excel structure: F1, F2, F3, F4
    """
    logger.info(f"Parsing Playbook Hub file for raw data: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Playbook Hub file not found: {file_path}")
    
    try:
        import win32com.client as win32
        import subprocess
        import time
        
        logger.info("Using Windows COM to read Excel file...")
        
        # Kill any existing Excel processes to ensure clean start
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], 
                          stderr=subprocess.DEVNULL, timeout=5)
            time.sleep(2)
        except:
            pass
        
        # Use dynamic COM binding (more flexible than gencache)
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        time.sleep(1)  # Give workbook time to fully initialize
        worksheet = workbook.Sheets(1)
        
        # Simple approach: read UsedRange as Value
        used_range = worksheet.UsedRange
        all_data = used_range.Value
        
        # Get dimensions
        rows_count = len(all_data) if all_data else 0
        cols_count = len(all_data[0]) if all_data and len(all_data) > 0 else 0
        
        logger.info(f"Sheet dimensions: {rows_count} rows × {cols_count} columns")
        
        # Extract all data row by row
        data_rows = []
        for row_data in all_data:
            row_dict = {}
            for col_idx in range(cols_count):
                col_name = f"F{col_idx + 1}"
                col_val = row_data[col_idx] if col_idx < len(row_data) else None
                row_dict[col_name] = str(col_val) if col_val is not None else ""
            data_rows.append(row_dict)
        
        workbook.Close(SaveChanges=False)
        excel.Quit()
        
        # Convert to DataFrame
        df = pd.DataFrame(data_rows)
        
        # Add extraction timestamp
        df['extracted_date'] = datetime.now()
        
        logger.info(f"Playbook Hub raw data extracted: {len(df)} rows × {len(df.columns)} columns")
        return df
    
    except ImportError:
        logger.error("win32com not available - cannot load raw data on non-Windows system")
        raise
    except Exception as e:
        logger.error(f"Error parsing Playbook Hub: {e}", exc_info=True)
        raise

def parse_weekly_messages_raw(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Parse Weekly Messages Excel file and extract ALL rows/columns as-is.
    Returns DataFrame with exact Excel structure: F1, F2, F3, F4, F5, F6
    """
    logger.info(f"Parsing Weekly Messages file for raw data: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Weekly Messages file not found: {file_path}")
    
    try:
        import win32com.client as win32
        import subprocess
        import time
        
        logger.info("Using Windows COM to read Excel file...")
        
        # Kill any existing Excel processes to ensure clean start
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], 
                          stderr=subprocess.DEVNULL, timeout=5)
            time.sleep(2)
        except:
            pass
        
        # Use dynamic COM binding (more flexible than gencache)
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        time.sleep(1)  # Give workbook time to fully initialize
        worksheet = workbook.Sheets(1)
        
        # Simple approach: read UsedRange as Value
        used_range = worksheet.UsedRange
        all_data = used_range.Value
        
        # Get dimensions
        rows_count = len(all_data) if all_data else 0
        cols_count = len(all_data[0]) if all_data and len(all_data) > 0 else 0
        
        logger.info(f"Sheet dimensions: {rows_count} rows × {cols_count} columns")
        
        # Extract all data row by row
        data_rows = []
        for row_data in all_data:
            row_dict = {}
            for col_idx in range(cols_count):
                col_name = f"F{col_idx + 1}"
                col_val = row_data[col_idx] if col_idx < len(row_data) else None
                row_dict[col_name] = str(col_val) if col_val is not None else ""
            data_rows.append(row_dict)
        
        workbook.Close(SaveChanges=False)
        excel.Quit()
        
        # Convert to DataFrame
        df = pd.DataFrame(data_rows)
        
        # Add extraction timestamp
        df['extracted_date'] = datetime.now()
        
        logger.info(f"Weekly Messages raw data extracted: {len(df)} rows × {len(df.columns)} columns")
        return df
    
    except ImportError:
        logger.error("win32com not available - cannot load raw data on non-Windows system")
        raise
    except Exception as e:
        logger.error(f"Error parsing Weekly Messages: {e}", exc_info=True)
        raise

# ============================================================================
# WEEKLY MESSAGES AUDIO CSV PARSING
# ============================================================================

def parse_weekly_messages_audio_raw(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Parse Weekly Messages Audio CSV file and extract ALL rows/columns as-is.
    Returns DataFrame with exact CSV structure: F1, F2, F3, F4, F5
    Uses COM to read CSV like Excel does (handles mixed content).
    """
    logger.info(f"Parsing Weekly Messages Audio CSV file: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Weekly Messages Audio CSV file not found: {file_path}")
    
    try:
        import win32com.client as win32
        import subprocess
        import time
        
        logger.info("Using Windows COM to read CSV file...")
        
        # Kill any existing Excel processes to ensure clean start
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], 
                          stderr=subprocess.DEVNULL, timeout=5)
            time.sleep(2)
        except:
            pass
        
        # Use dynamic COM binding (more flexible than gencache)
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        time.sleep(1)  # Give workbook time to fully initialize
        worksheet = workbook.Sheets(1)
        
        # Simple approach: read UsedRange as Value
        used_range = worksheet.UsedRange
        all_data = used_range.Value
        
        rows_count = len(all_data) if all_data else 0
        cols_count = len(all_data[0]) if all_data and len(all_data) > 0 else 0
        
        logger.info(f"CSV dimensions: {rows_count} rows × {cols_count} columns")
        
        # Extract all data row by row (up to 5 columns for Audio CSV)
        data_rows = []
        for row_data in all_data:
            row_dict = {}
            # Cap at 5 columns for audio data
            for col_idx in range(min(cols_count, 5)):
                col_name = f"F{col_idx + 1}"
                col_val = row_data[col_idx] if col_idx < len(row_data) else None
                row_dict[col_name] = str(col_val) if col_val is not None else ""
            data_rows.append(row_dict)
        
        workbook.Close(SaveChanges=False)
        excel.Quit()
        
        # Convert to DataFrame
        df = pd.DataFrame(data_rows)
        
        # Ensure exactly 5 columns (F1-F5)
        for col_num in range(1, 6):
            col_name = f"F{col_num}"
            if col_name not in df.columns:
                df[col_name] = ""
        
        # Persist only F1-F5 columns
        df = df[['F1', 'F2', 'F3', 'F4', 'F5']]
        
        # Add extraction timestamp
        df['extracted_date'] = datetime.now()
        
        logger.info(f"Weekly Messages Audio raw data extracted: {len(df)} rows × {len(df.columns)} columns")
        return df
    
    except Exception as e:
        logger.error(f"Error parsing Weekly Messages Audio CSV: {e}", exc_info=True)
        raise

# ============================================================================
# CLOUD CSV RAW PARSING (VB Process - New Data Sources)
# ============================================================================

def parse_weekly_messages_cloud_raw(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """Parse Weekly Messages Cloud CSV and extract all rows/columns as-is."""
    logger.info(f"Parsing Weekly Messages Cloud CSV for raw data: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path, skiprows=13, header=None)
        rows = []
        extracted_date = datetime.now()
        
        for _, row_data in df.iterrows():
            row_dict = {}
            for col_idx in range(min(6, len(row_data))):
                row_dict[f"F{col_idx + 1}"] = str(row_data[col_idx]) if pd.notna(row_data[col_idx]) else ""
            row_dict['extracted_date'] = extracted_date
            rows.append(row_dict)
        
        result_df = pd.DataFrame(rows)
        logger.info(f"Weekly Messages Cloud raw: {len(result_df)} rows × {len(result_df.columns)} columns")
        return result_df
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise

def parse_playbook_cloud_raw(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """Parse Playbook Cloud CSV and extract all data rows as-is (raw format)."""
    logger.info(f"Parsing Playbook Cloud CSV for raw data: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        # Read entire CSV without headers - multi-section format
        df = pd.read_csv(file_path, header=None, on_bad_lines='skip')
        rows = []
        extracted_date = datetime.now()
        
        # Extract all data rows (skip header/metadata rows)
        for idx, row_data in df.iterrows():
            cell_val = str(row_data.iloc[0]).strip() if pd.notna(row_data.iloc[0]) else ""
            
            # Skip header and metadata rows
            if (cell_val.startswith('#') or 
                'Report suite' in cell_val or 
                'Date:' in cell_val or
                cell_val == ''):
                continue
            
            # Extract data row as-is
            row_dict = {}
            for col_idx in range(min(4, len(row_data))):
                value = row_data.iloc[col_idx]
                row_dict[f"F{col_idx + 1}"] = str(value) if pd.notna(value) else ""
            row_dict['extracted_date'] = extracted_date
            rows.append(row_dict)
        
        result_df = pd.DataFrame(rows)
        logger.info(f"Playbook Cloud raw: {len(result_df)} rows × {len(result_df.columns)} columns")
        return result_df
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise

# ============================================================================
# BIGQUERY LOADING
# ============================================================================

def load_raw_to_bigquery(
    client: bigquery.Client,
    df: pd.DataFrame,
    table_id: str,
    logger: logging.Logger
) -> int:
    """
    Load raw DataFrame to BigQuery table using TRUNCATE+INSERT.
    This replaces the entire table with fresh data each time.
    """
    if df.empty:
        logger.warning(f"No data to load for {table_id}")
        return 0
    
    try:
        logger.info(f"Loading {len(df)} rows to {table_id}")
        
        # Use WRITE_TRUNCATE to replace entire table
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        
        # Build schema: all STRING columns + extracted_date TIMESTAMP
        schema = []
        for col in df.columns:
            if col == 'extracted_date':
                schema.append(bigquery.SchemaField(col, "TIMESTAMP"))
            else:
                schema.append(bigquery.SchemaField(col, "STRING"))
        
        job_config.schema = schema
        
        # Load data
        load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        load_job.result()
        
        logger.info(f"Successfully loaded {len(df)} rows to {table_id}")
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
    logger.info("Adobe Analytics Raw Data Loader - START")
    logger.info("=" * 80)
    
    try:
        # Initialize BigQuery client
        client = init_bigquery_client(config['gcp']['project_id'], logger)
        
        logger.info("\n--- PHASE 1: PARSING SOURCE FILES ---")
        
        # Parse raw data from Excel files
        playbook_raw = pd.DataFrame()
        weekly_raw = pd.DataFrame()
        audio_raw = pd.DataFrame()
        
        try:
            playbook_raw = parse_playbook_hub_raw(
                config['source_files']['playbook_hub_path'],
                logger
            )
        except FileNotFoundError as e:
            logger.warning(f"Playbook Hub file not available: {e}")
        
        try:
            weekly_raw = parse_weekly_messages_raw(
                config['source_files']['weekly_messages_excel_path'],
                logger
            )
        except FileNotFoundError as e:
            logger.warning(f"Weekly Messages file not available: {e}")
        
        try:
            audio_raw = parse_weekly_messages_audio_raw(
                config['source_files']['weekly_messages_audio_csv_path'],
                logger
            )
        except FileNotFoundError as e:
            logger.warning(f"Weekly Messages Audio CSV file not available: {e}")
        
        # Cloud CSV Raw Data
        weekly_cloud_raw = pd.DataFrame()
        playbook_cloud_raw = pd.DataFrame()
        
        try:
            weekly_cloud_raw = parse_weekly_messages_cloud_raw(
                config['source_files']['weekly_messages_cloud_csv'],
                logger
            )
        except Exception as e:
            logger.warning(f"Weekly Messages Cloud CSV not available: {e}")
        
        try:
            playbook_cloud_raw = parse_playbook_cloud_raw(
                config['source_files']['playbook_hub_cloud_csv'],
                logger
            )
        except Exception as e:
            logger.warning(f"Playbook Cloud CSV not available: {e}")
        
        logger.info("\n--- PHASE 2: LOADING TO BIGQUERY ---")
        
        project = config['gcp']['project_id']
        dataset_id = config['bigquery']['dataset_id']
        
        playbook_raw_table = f"{project}.{dataset_id}.bq_playbook_hub_raw"
        weekly_raw_table = f"{project}.{dataset_id}.bq_weekly_messages_raw"
        audio_raw_table = f"{project}.{dataset_id}.bq_weekly_messages_audio_raw"
        weekly_cloud_raw_table = f"{project}.{dataset_id}.bq_weekly_messages_cloud_raw"
        playbook_cloud_raw_table = f"{project}.{dataset_id}.bq_playbook_cloud_raw"
        
        logger.info(f"Target tables:")
        logger.info(f"  LEGACY: {playbook_raw_table}, {weekly_raw_table}, {audio_raw_table}")
        logger.info(f"  CLOUD:  {weekly_cloud_raw_table}, {playbook_cloud_raw_table}")
        
        # Load each table if data is available
        playbook_count = 0
        weekly_count = 0
        audio_count = 0
        weekly_cloud_count = 0
        playbook_cloud_count = 0
        
        if not playbook_raw.empty:
            playbook_count = load_raw_to_bigquery(
                client, playbook_raw, playbook_raw_table, logger
            )
        else:
            logger.info(f"Playbook Hub Raw: No data to load")
        
        if not weekly_raw.empty:
            weekly_count = load_raw_to_bigquery(
                client, weekly_raw, weekly_raw_table, logger
            )
        else:
            logger.info(f"Weekly Messages Raw: No data to load")
        
        if not audio_raw.empty:
            audio_count = load_raw_to_bigquery(
                client, audio_raw, audio_raw_table, logger
            )
        else:
            logger.info(f"Weekly Messages Audio Raw: No data to load")
        
        # Load Cloud CSV data
        if not weekly_cloud_raw.empty:
            weekly_cloud_count = load_raw_to_bigquery(
                client, weekly_cloud_raw, weekly_cloud_raw_table, logger
            )
        else:
            logger.info(f"Weekly Messages Cloud Raw: No data to load")
        
        if not playbook_cloud_raw.empty:
            playbook_cloud_count = load_raw_to_bigquery(
                client, playbook_cloud_raw, playbook_cloud_raw_table, logger
            )
        else:
            logger.info(f"Playbook Cloud Raw: No data to load")
        
        # Summary
        logger.info("\n--- SUMMARY ---")
        logger.info(f"LEGACY DATA (Excel):")
        logger.info(f"  Playbook Hub Raw: {playbook_count} rows")
        logger.info(f"  Weekly Messages Raw: {weekly_count} rows")
        logger.info(f"  Weekly Messages Audio Raw: {audio_count} rows")
        logger.info(f"CLOUD DATA (CSV):")
        logger.info(f"  Weekly Messages Cloud Raw: {weekly_cloud_count} rows")
        logger.info(f"  Playbook Cloud Raw: {playbook_cloud_count} rows")
        logger.info("=" * 80)
        logger.info("Adobe Analytics Raw Data Loader - SUCCESS")
        logger.info("=" * 80)
        
        return 0
    
    except Exception as e:
        logger.error("=" * 80)
        logger.error("Adobe Analytics Raw Data Loader - FAILED")
        logger.error("=" * 80)
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
