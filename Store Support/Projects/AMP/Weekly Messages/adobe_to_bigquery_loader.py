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

def find_latest_csv_file(folder_path: str, logger: logging.Logger) -> str:
    """Find the most recently modified CSV file in a folder."""
    logger.info(f"Searching for CSV files in: {folder_path}")
    
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    csv_files = sorted(folder.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {folder_path}")
    
    latest_file = str(csv_files[0])
    logger.info(f"Using latest CSV file: {latest_file} (modified: {datetime.fromtimestamp(csv_files[0].stat().st_mtime)})")
    return latest_file

def parse_weekly_messages_excel(file_path: str, logger: logging.Logger) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parse Weekly Messages Area Reports FY27 Excel file using Windows COM.
    Extracts device-level page views and aggregated metrics.
    Returns two DataFrames: devices and metrics.
    """
    logger.info(f"Parsing Weekly Messages Excel file: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Weekly Messages Excel file not found: {file_path}")
    
    devices_rows = []
    metrics_rows = []
    report_date = datetime.now().date()
    extracted_date = datetime.now()
    
    try:
        import win32com.client as win32
        import subprocess
        import time
        
        logger.info("Using Windows COM to read Weekly Messages Excel...")
        
        # Kill any existing Excel processes to ensure clean start
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], 
                          stderr=subprocess.DEVNULL, timeout=5)
            time.sleep(2)
        except:
            pass
        
        # Use dynamic COM binding for flexibility
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        time.sleep(1)  # Give workbook time to fully initialize
        worksheet = workbook.Sheets(1)  # First sheet
        
        usedRange = worksheet.UsedRange
        rows = usedRange.Rows.Count
        cols = usedRange.Columns.Count
        
        logger.info(f"Sheet dimensions: {rows} rows × {cols} cols")
        
        # --- PARSE DEVICE DATA (starts at row 14 per file structure) ---
        # Column headers at row 12-13: Tablets, Desktop, Store Devices, Mobile, XCover
        # Data rows start at 14
        
        data_start_row = 14
        metrics_start_row = 30  # Approximate - will find by looking for "Unique Users" header
        
        device_headers = []
        for col in range(2, cols + 1):  # Skip first column (page names)
            cell_val = worksheet.Cells(13, col).Value
            if cell_val:
                device_headers.append((col, str(cell_val).strip()))
        
        logger.info(f"Device columns: {[h[1] for h in device_headers]}")
        
        # Read device data rows
        for row in range(data_start_row, min(data_start_row + 100, metrics_start_row)):
            page_name = worksheet.Cells(row, 1).Value
            if not page_name or pd.isna(page_name) or str(page_name).strip() == '':
                break
            
            page_name = str(page_name).strip()
            
            # Skip header rows
            if page_name.startswith('#') or 'Table' in page_name:
                break
            
            device_values = {}
            total = 0
            
            for col_idx, col_name in device_headers:
                cell_val = worksheet.Cells(row, col_idx).Value
                try:
                    val = float(cell_val) if cell_val and str(cell_val) != '' else 0
                    device_values[col_name] = int(val)
                    total += int(val)
                except (ValueError, TypeError):
                    device_values[col_name] = 0
            
            # Extract category from page name (first part before colon)
            category = 'Weekly Messages'
            if ':' in page_name:
                category = page_name.split(':')[0].strip()
            
            devices_rows.append({
                'report_date': report_date,
                'category': category,
                'page_name': page_name,
                'tablets_page_views': device_values.get('Tablets Excluding Store Device', device_values.get('Tablets', 0)),
                'desktop_page_views': device_values.get('Desktop', 0),
                'store_devices_page_views': device_values.get('Store Devices', device_values.get('Store Device', 0)),
                'mobile_phones_page_views': device_values.get('Mobile Phones Excluding Store', device_values.get('Mobile', 0)),
                'xcover_devices_page_views': device_values.get('XCover Devices', device_values.get('XCover', 0)),
                'total_page_views': total,
                'extracted_date': extracted_date
            })
        
        # --- PARSE METRICS DATA (starts around row 30) ---
        # This table has: Unique Users, Average Time on Site, Visits, etc.
        
        metrics_data_start = 31  # Row after headers
        
        for row in range(metrics_data_start, min(metrics_data_start + 100, rows + 1)):
            page_name = worksheet.Cells(row, 1).Value
            if not page_name or pd.isna(page_name) or str(page_name).strip() == '':
                break
            
            page_name = str(page_name).strip()
            
            # Skip header rows
            if page_name.startswith('#') or 'Table' in page_name or page_name == '':
                break
            
            try:
                page_views = float(worksheet.Cells(row, 2).Value or 0)
                unique_users = float(worksheet.Cells(row, 3).Value or 0)
                avg_time = float(worksheet.Cells(row, 4).Value or 0)
                visits = float(worksheet.Cells(row, 5).Value or 0)
                
                # Extract category from page name
                category = 'Weekly Messages'
                if ':' in page_name:
                    category = page_name.split(':')[0].strip()
                
                metrics_rows.append({
                    'report_date': report_date,
                    'category': category,
                    'page_name': page_name,
                    'page_views': int(page_views),
                    'unique_users': unique_users,
                    'average_time_on_site': avg_time,
                    'visits': int(visits),
                    'extracted_date': extracted_date
                })
            except (ValueError, TypeError):
                continue
        
        workbook.Close(False)
        excel.Quit()
        
        logger.info(f"Weekly Messages Excel parsed: {len(devices_rows)} device rows, {len(metrics_rows)} metric rows")
        
    except ImportError:
        logger.warning("win32com not available - cannot parse Weekly Messages Excel on non-Windows system")
        raise
    except Exception as e:
        logger.error(f"Error parsing Weekly Messages Excel: {e}", exc_info=True)
        raise
    
    devices_df = pd.DataFrame(devices_rows) if devices_rows else pd.DataFrame()
    metrics_df = pd.DataFrame(metrics_rows) if metrics_rows else pd.DataFrame()
    
    return devices_df, metrics_df

def parse_weekly_messages_csv(csv_path: str, logger: logging.Logger) -> Tuple[pd.DataFrame, pd.DataFrame]:
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
    Parse Playbook Hub FY27 Excel file using Windows COM.
    Returns DataFrame with playbook metrics.
    
    The file structure has all data in one sheet with section headers
    like "# Playbook Hub", "Valentines", "Baby Days", "Easter"
    """
    logger.info(f"Parsing Playbook Hub file: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Playbook Hub file not found: {file_path}")
    
    try:
        import win32com.client as win32
        import subprocess
        import time
        
        logger.info("Using Windows COM to read Excel file...")
        
        # Kill any existing Excel processes
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], 
                          stderr=subprocess.DEVNULL, timeout=5)
            time.sleep(2)  # Increased wait for proper COM cleanup
        except:
            pass
        
        # Use the proven working pattern from Weekly Messages parsing
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        time.sleep(1)  # Give workbook time to fully initialize
        worksheet = workbook.Sheets(1)  # Single sheet
        
        # Read all data using UsedRange with explicit COM call
        usedRange = worksheet.UsedRange
        rows = usedRange.Rows.Count
        cols = usedRange.Columns.Count
        
        logger.info(f"Playbook sheet dimensions: {rows} rows × {cols} columns")
        
        playbook_rows = []
        report_date = datetime.now().date()
        extracted_date = datetime.now()
        current_category = None
        
        # Read row by row, tracking category changes
        for row_idx in range(1, rows + 1):
            try:
                cell_val = worksheet.Cells(row_idx, 1).Value
                if not cell_val:
                    continue
                
                cell_str = str(cell_val).strip()
                
                # Check if this is a category header row
                if 'Playbook Hub' in cell_str or 'Valentines' in cell_str or 'Baby Days' in cell_str or 'Easter' in cell_str:
                    # Extract category name
                    if 'Hub' in cell_str:
                        current_category = 'Playbook Hub'
                    elif 'Valentines' in cell_str:
                        current_category = 'Valentines'
                    elif 'Baby' in cell_str:
                        current_category = 'Baby Days'
                    elif 'Easter' in cell_str:
                        current_category = 'Easter'
                    logger.debug(f"Found category at row {row_idx}: {current_category}")
                    continue
                
                # Skip metadata rows (start with # or contain keywords)
                if cell_str.startswith('#') or 'Table' in cell_str or 'Total' in cell_str or cell_str == '':
                    continue
                
                # This looks like a data row - extract values
                if current_category:
                    try:
                        page_name = cell_str
                        col2_val = worksheet.Cells(row_idx, 2).Value
                        col3_val = worksheet.Cells(row_idx, 3).Value
                        col4_val = worksheet.Cells(row_idx, 4).Value
                        
                        total_views = int(float(col2_val or 0))
                        salary_views = int(float(col3_val or 0))
                        hourly_views = int(float(col4_val or 0))
                        
                        playbook_rows.append({
                            'report_date': report_date,
                            'playbook_category': current_category,
                            'page_name': page_name,
                            'total_page_views': total_views,
                            'store_salary_associates_views': salary_views,
                            'store_hourly_associates_views': hourly_views,
                            'report_period_start': None,
                            'report_period_end': None,
                            'extracted_date': extracted_date
                        })
                    except (ValueError, TypeError):
                        # Skip rows that don't parse properly
                        pass
            except Exception as e:
                logger.debug(f"Error reading row {row_idx}: {e}")
                continue
        
        workbook.Close(False)
        excel.Quit()
        
        playbook_df = pd.DataFrame(playbook_rows)
        
        # Ensure proper data types
        if not playbook_df.empty:
            playbook_df['report_date'] = pd.to_datetime(playbook_df['report_date']).dt.date
            playbook_df['extracted_date'] = pd.to_datetime(playbook_df['extracted_date'])
            playbook_df['total_page_views'] = playbook_df['total_page_views'].astype('int64')
            playbook_df['store_salary_associates_views'] = playbook_df['store_salary_associates_views'].astype('int64')
            playbook_df['store_hourly_associates_views'] = playbook_df['store_hourly_associates_views'].astype('int64')
            
            # Remove duplicates
            playbook_df = playbook_df.drop_duplicates(
                subset=['report_date', 'playbook_category', 'page_name'], 
                keep='first'
            )
        
        logger.info(f"Playbook Hub parsed via COM: {len(playbook_df)} rows")
        return playbook_df
    
    except ImportError:
        logger.info("win32com not available, trying pandas...")
        try:
            xl_file = pd.ExcelFile(file_path, engine='openpyxl')
            logger.info(f"Excel file loaded. Sheet count: {len(xl_file.sheet_names)}")
        except ImportError:
            logger.warning("openpyxl not available, attempting with built-in engine...")
            try:
                xl_file = pd.ExcelFile(file_path)
                logger.info(f"Excel file loaded with fallback engine. Sheet count: {len(xl_file.sheet_names)}")
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
# CLOUD CSV PARSING (VB Process - New Data Sources)
# ============================================================================

def parse_weekly_messages_cloud_csv(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Parse Weekly Messages Cloud CSV file (from VB process).
    Extracts device-level page views and aggregates metrics.
    
    Structure:
    - Lines 1-11: Comments/headers
    - Line 12-13: Column names (device types)
    - Line 14+: Data rows (complete URLs and metrics)
    """
    logger.info(f"Parsing Weekly Messages Cloud CSV: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Weekly Messages Cloud CSV not found: {file_path}")
    
    try:
        # Read CSV, skip header comments
        df = pd.read_csv(file_path, skiprows=13)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Extract data - FIRST TABLE ONLY
        rows = []
        report_date = datetime.now().date()
        extracted_date = datetime.now()
        data_started = False
        table_ended = False
        
        for idx, row in df.iterrows():
            page_name = str(row.iloc[0]).strip()
            
            # Skip empty rows
            if not page_name or page_name == 'NaN':
                continue
            
            # Detect table boundaries (comment rows), stop reading if we already have data
            if page_name.startswith('#') or 'Complete URL' in page_name or 'Page Views' in page_name:
                if data_started:
                    # We've hit the end of the first table, stop reading
                    table_ended = True
                    break
                else:
                    # Still in header section
                    continue
            
            # Extract device metrics
            try:
                tablets = int(float(row.iloc[1] or 0))
                desktop = int(float(row.iloc[2] or 0))
                store_devices = int(float(row.iloc[3] or 0))
                mobile = int(float(row.iloc[4] or 0))
                xcover = int(float(row.iloc[5] or 0))
                total = tablets + desktop + store_devices + mobile + xcover
                
                # Extract category from page name
                category = 'Weekly Messages - Cloud'
                if 'fashion' in page_name.lower():
                    category = 'Fashion'
                elif 'home' in page_name.lower():
                    category = 'Home'
                
                rows.append({
                    'report_date': report_date,
                    'category': category,
                    'page_name': page_name,
                    'tablets_page_views': tablets,
                    'desktop_page_views': desktop,
                    'store_devices_page_views': store_devices,
                    'mobile_phones_page_views': mobile,
                    'xcover_devices_page_views': xcover,
                    'total_page_views': total,
                    'extracted_date': extracted_date
                })
                data_started = True
            except (ValueError, TypeError):
                continue
        
        result_df = pd.DataFrame(rows)
        logger.info(f"Weekly Messages Cloud CSV parsed: {len(result_df)} rows")
        return result_df
        
    except Exception as e:
        logger.error(f"Error parsing Weekly Messages Cloud CSV: {e}", exc_info=True)
        raise

def parse_playbook_cloud_csv(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Parse Playbook Hub Cloud CSV file (from VB process).
    Handles multiple category sections with their own tables.
    """
    logger.info(f"Parsing Playbook Cloud CSV: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Playbook Cloud CSV not found: {file_path}")
    
    try:
        # Read entire CSV first
        df = pd.read_csv(file_path, header=None)
        
        rows = []
        report_date = datetime.now().date()
        extracted_date = datetime.now()
        
        current_category = None
        i = 0
        
        while i < len(df):
            cell_val = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ""
            
            # Check for category headers
            if '# Playbook Hub' in cell_val or '# Freeform table' in cell_val:
                i += 1
                continue
            elif '# Valentines' in cell_val:
                current_category = 'Valentines'
                i += 1
                continue
            elif '# Baby' in cell_val:
                current_category = 'Baby Days'
                i += 1
                continue
            elif '# Easter' in cell_val:
                current_category = 'Easter'
                i += 1
                continue
            elif cell_val.startswith('#') or 'Report suite' in cell_val or 'Date:' in cell_val:
                i += 1
                continue
            
            # Check for data rows (has numeric values)
            if current_category and len(cell_val) > 0 and not cell_val.startswith('#'):
                try:
                    col2 = int(float(pd.to_numeric(df.iloc[i, 1] or 0)))
                    col3 = int(float(pd.to_numeric(df.iloc[i, 2] or 0)))
                    col4 = int(float(pd.to_numeric(df.iloc[i, 3] or 0)))
                    
                    rows.append({
                        'report_date': report_date,
                        'playbook_category': current_category or 'Unknown',
                        'page_name': cell_val,
                        'total_page_views': col2,
                        'store_salary_associates_views': col3,
                        'store_hourly_associates_views': col4,
                        'extracted_date': extracted_date
                    })
                except (ValueError, TypeError):
                    pass
            
            i += 1
        
        result_df = pd.DataFrame(rows)
        logger.info(f"Playbook Cloud CSV parsed: {len(result_df)} rows")
        return result_df
        
    except Exception as e:
        logger.error(f"Error parsing Playbook Cloud CSV: {e}", exc_info=True)
        raise

def parse_weekly_messages_audio_normalized(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Parse Weekly Messages Audio CSV and convert to normalized columns.
    Converts raw F1-F5 format to: page_name, page_views, unique_users, visits, avg_time_on_site
    """
    logger.info(f"Parsing Weekly Messages Audio CSV to normalized format: {file_path}")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        import win32com.client as win32
        import subprocess
        import time
        
        logger.info("Using Windows COM to read Audio CSV file...")
        
        # Kill any existing Excel processes
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], 
                          stderr=subprocess.DEVNULL, timeout=5)
            time.sleep(2)
        except:
            pass
        
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        time.sleep(1)
        worksheet = workbook.Sheets(1)
        
        used_range = worksheet.UsedRange
        all_data = used_range.Value
        
        rows_count = len(all_data) if all_data else 0
        logger.info(f"Audio CSV dimensions: {rows_count} rows")
        
        rows = []
        report_date = datetime.now().date()
        extracted_date = datetime.now()
        
        # Skip header rows (those starting with #) and find where data starts
        data_start_idx = None
        for idx, row_data in enumerate(all_data):
            if row_data and len(row_data) > 0:
                first_cell = str(row_data[0]).strip()
                # Look for first data row (doesn't start with # and isn't empty)
                if not first_cell.startswith('#') and first_cell and 'Page Name' not in first_cell:
                    data_start_idx = idx
                    break
        
        if data_start_idx is None:
            logger.warning("No data rows found in Audio CSV")
            workbook.Close(SaveChanges=False)
            excel.Quit()
            return pd.DataFrame()
        
        # Extract data rows starting from data_start_idx
        for row_data in all_data[data_start_idx:]:
            if not row_data or len(row_data) < 5:
                continue
            
            # Extract columns from data row
            page_name = str(row_data[0]).strip() if row_data[0] else ""
            
            # Skip empty/header rows and only keep Audio pages (weekly_messages_audiowk*)
            if not page_name or page_name.startswith('#') or 'Page Name' in page_name:
                continue
            
            # Only extract rows for weekly_messages_audiowk (Audio-specific pages)
            if 'weekly_messages_audiowk' not in page_name.lower():
                continue
            
            try:
                page_views = int(float(row_data[1] or 0))
                unique_users = float(row_data[2] or 0)
                visits = int(float(row_data[3] or 0))
                avg_time_on_site = float(row_data[4] or 0)
                
                rows.append({
                    'report_date': report_date,
                    'page_name': str(page_name),
                    'page_views': int(page_views),
                    'unique_users': float(unique_users),
                    'visits': int(visits),
                    'avg_time_on_site': float(avg_time_on_site),
                    'extracted_date': extracted_date
                })
            except (ValueError, TypeError, IndexError):
                continue
        
        workbook.Close(SaveChanges=False)
        excel.Quit()
        
        result_df = pd.DataFrame(rows)
        
        # Ensure correct data types
        result_df['report_date'] = pd.to_datetime(result_df['report_date']).dt.date
        result_df['page_name'] = result_df['page_name'].astype(str)
        result_df['page_views'] = result_df['page_views'].astype('int64')
        result_df['unique_users'] = result_df['unique_users'].astype('float64')
        result_df['visits'] = result_df['visits'].astype('int64')
        result_df['avg_time_on_site'] = result_df['avg_time_on_site'].astype('float64')
        
        logger.info(f"Weekly Messages Audio normalized: {len(result_df)} rows × {len(result_df.columns)} columns")
        return result_df
        
    except Exception as e:
        logger.error(f"Error parsing Audio CSV: {e}", exc_info=True)
        raise

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
        # Create temporary table with explicit schema
        temp_table_id = f"{table_id}_temp_{int(datetime.now().timestamp())}"
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        
        # Build schema explicitly to avoid type inference issues
        schema = []
        for col in df.columns:
            if col == 'extracted_date':
                schema.append(bigquery.SchemaField(col, "TIMESTAMP"))
            elif col in {'report_date', 'report_period_start', 'report_period_end'}:
                schema.append(bigquery.SchemaField(col, "DATE"))
            elif col in {'page_views', 'visits', 'total_page_views', 'store_salary_associates_views', 'store_hourly_associates_views', 'tablets_page_views', 'desktop_page_views', 'store_devices_page_views', 'mobile_phones_page_views', 'xcover_devices_page_views'}:
                schema.append(bigquery.SchemaField(col, "INT64"))
            elif col in {'unique_users', 'average_time_on_site', 'avg_time_on_site'}:
                schema.append(bigquery.SchemaField(col, "FLOAT64"))
            else:
                schema.append(bigquery.SchemaField(col, "STRING"))
        
        job_config.schema = schema
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
        
        # Parse data from source files
        logger.info("\n--- PHASE 1: PARSING SOURCE FILES ---")
        
        # Weekly Messages: Parse Excel file (new source)
        weekly_devices = pd.DataFrame()
        weekly_metrics = pd.DataFrame()
        
        try:
            weekly_messages_excel = config['source_files']['weekly_messages_excel_path']
            weekly_devices, weekly_metrics = parse_weekly_messages_excel(weekly_messages_excel, logger)
        except FileNotFoundError as e:
            logger.warning(f"Weekly Messages Excel file not available: {e}")
            logger.info("Continuing - will load when available")
        except Exception as e:
            logger.warning(f"Error parsing Weekly Messages Excel: {e}")
        
        # Playbook Hub: Parse Excel file
        playbook_hub = pd.DataFrame()
        try:
            playbook_hub = parse_playbook_hub_file(
                config['source_files']['playbook_hub_path'],
                logger
            )
        except FileNotFoundError as e:
            logger.warning(f"Playbook Hub file not available: {e}")
        
        # Cloud CSV: Parse Weekly Messages Cloud
        weekly_messages_cloud = pd.DataFrame()
        try:
            weekly_messages_cloud_csv = config['source_files']['weekly_messages_cloud_csv']
            weekly_messages_cloud = parse_weekly_messages_cloud_csv(weekly_messages_cloud_csv, logger)
        except FileNotFoundError as e:
            logger.warning(f"Weekly Messages Cloud CSV not available: {e}")
        except Exception as e:
            logger.warning(f"Error parsing Weekly Messages Cloud CSV: {e}")
        
        # Cloud CSV: Parse Playbook Cloud
        playbook_cloud = pd.DataFrame()
        try:
            playbook_cloud_csv = config['source_files']['playbook_hub_cloud_csv']
            playbook_cloud = parse_playbook_cloud_csv(playbook_cloud_csv, logger)
        except FileNotFoundError as e:
            logger.warning(f"Playbook Cloud CSV not available: {e}")
        except Exception as e:
            logger.warning(f"Error parsing Playbook Cloud CSV: {e}")
        
        # Audio CSV: Parse Weekly Messages Audio (normalized)
        weekly_messages_audio = pd.DataFrame()
        try:
            weekly_messages_audio_csv = config['source_files']['weekly_messages_audio_csv_path']
            weekly_messages_audio = parse_weekly_messages_audio_normalized(weekly_messages_audio_csv, logger)
        except FileNotFoundError as e:
            logger.warning(f"Weekly Messages Audio CSV not available: {e}")
        except Exception as e:
            logger.warning(f"Error parsing Weekly Messages Audio CSV: {e}")
        
        # Load to BigQuery
        logger.info("\n--- PHASE 2: LOADING TO BIGQUERY ---")
        project = config['gcp']['project_id']
        dataset_id = config['bigquery']['dataset_id']
        
        weekly_devices_table = f"{project}.{dataset_id}.{config['bigquery']['tables']['weekly_devices']}"
        weekly_metrics_table = f"{project}.{dataset_id}.{config['bigquery']['tables']['weekly_metrics']}"
        playbook_table = f"{project}.{dataset_id}.{config['bigquery']['tables']['playbook']}"
        
        logger.info(f"Target tables:")
        logger.info(f"  - {weekly_devices_table}")
        logger.info(f"  - {weekly_metrics_table}")
        logger.info(f"  - {playbook_table}")
        
        # Audio table
        audio_table = f"{project}.{dataset_id}.{config['bigquery']['tables']['audio']}"
        logger.info(f"  - {audio_table}")
        
        # Cloud CSV target tables
        weekly_cloud_table = f"{project}.{dataset_id}.{config['bigquery']['tables']['weekly_cloud']}"
        playbook_cloud_table = f"{project}.{dataset_id}.{config['bigquery']['tables']['playbook_cloud']}"
        
        logger.info(f"Cloud data target tables:")
        logger.info(f"  - {weekly_cloud_table}")
        logger.info(f"  - {playbook_cloud_table}")
        
        # Load each table if data is available
        devices_count = 0
        metrics_count = 0
        playbook_count = 0
        audio_count = 0
        weekly_cloud_count = 0
        playbook_cloud_count = 0
        
        if not weekly_devices.empty:
            devices_count = load_to_bigquery(
                client, weekly_devices, weekly_devices_table,
                ['report_date', 'category', 'page_name'], logger
            )
        else:
            logger.info(f"Weekly Messages Devices: No data to load (Excel not available yet)")
        
        if not weekly_metrics.empty:
            metrics_count = load_to_bigquery(
                client, weekly_metrics, weekly_metrics_table,
                ['report_date', 'category', 'page_name'], logger
            )
        else:
            logger.info(f"Weekly Messages Metrics: No data to load (Excel not available yet)")
        
        if not playbook_hub.empty:
            playbook_count = load_to_bigquery(
                client, playbook_hub, playbook_table,
                ['report_date', 'playbook_category', 'page_name'], logger
            )
        else:
            logger.info(f"Playbook Hub: No data to load")
        
        if not weekly_messages_audio.empty:
            audio_count = load_to_bigquery(
                client, weekly_messages_audio, audio_table,
                ['report_date', 'page_name'], logger
            )
        else:
            logger.info(f"Weekly Messages Audio: No data to load")
        
        # Load Cloud CSV data
        if not weekly_messages_cloud.empty:
            weekly_cloud_count = load_to_bigquery(
                client, weekly_messages_cloud, weekly_cloud_table,
                ['report_date', 'category', 'page_name'], logger
            )
        else:
            logger.info(f"Weekly Messages Cloud: No data to load")
        
        if not playbook_cloud.empty:
            playbook_cloud_count = load_to_bigquery(
                client, playbook_cloud, playbook_cloud_table,
                ['report_date', 'playbook_category', 'page_name'], logger
            )
        else:
            logger.info(f"Playbook Cloud: No data to load")
        
        # Summary
        logger.info("\n--- SUMMARY ---")
        logger.info(f"LEGACY DATA (Excel):")
        logger.info(f"  Weekly Messages Devices: {devices_count} rows")
        logger.info(f"  Weekly Messages Metrics: {metrics_count} rows")
        logger.info(f"  Playbook Hub: {playbook_count} rows")
        logger.info(f"  Weekly Messages Audio: {audio_count} rows")
        logger.info(f"CLOUD DATA (CSV):")
        logger.info(f"  Weekly Messages Cloud: {weekly_cloud_count} rows")
        logger.info(f"  Playbook Cloud: {playbook_cloud_count} rows")
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
