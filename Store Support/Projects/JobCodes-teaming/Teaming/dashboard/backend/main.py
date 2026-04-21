"""
Job Code Teaming Dashboard - Backend Server
Manages job codes and their teaming assignments with user authentication.
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
import os
import json
import sys
import pandas as pd
from datetime import datetime
from typing import Optional
import secrets
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

# BigQuery for employee lookup
try:
    from google.cloud import bigquery
    HAS_BIGQUERY = True
except ImportError:
    HAS_BIGQUERY = False

# SQLite Cache for job codes
from sqlite_cache import get_cache, init_cache

# Fix Unicode encoding for Windows console output
import io
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================
# CONFIGURATION
# ============================================================

HOST = "0.0.0.0"
PORT = 8080
DEBUG = True

# Email Configuration - Using Walmart Internal SMTP
NOTIFY_EMAIL = "ATCTEAMSUPPORT@walmart.com"

# Walmart Internal SMTP Gateway (no auth required on Walmart network/VPN)
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
FROM_EMAIL = "JobCodeTeamingDashboard@walmart.com"

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEAMING_DIR = os.path.dirname(BASE_DIR)  # C:\...\Teaming folder
JOB_CODES_DIR = os.path.join(os.path.dirname(TEAMING_DIR), "Job Codes")
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
REQUESTS_FILE = os.path.join(DATA_DIR, "update_requests.json")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")
JOB_CODES_MASTER_FILE = os.path.join(DATA_DIR, "job_codes_master.json")
JOB_CODE_REQUESTS_FILE = os.path.join(DATA_DIR, "job_code_requests.json")
REJECTION_HISTORY_FILE = os.path.join(DATA_DIR, "rejection_history.json")

# Data source files (in Teaming folder)
TEAMING_DATA_FILE = os.path.join(TEAMING_DIR, "TMS_Data_3_converted.csv")
POLARIS_DATA_FILE = os.path.join(TEAMING_DIR, "polaris_job_codes.csv")
USER_COUNTS_FILE = os.path.join(TEAMING_DIR, "polaris_user_counts.csv")

# Job Code Master Excel file
JOB_CODE_MASTER_EXCEL = os.path.join(JOB_CODES_DIR, "Job_Code_Master_Table.xlsx")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# APP SETUP
# ============================================================

app = FastAPI(
    title="Aligned",
    description="Manage job codes and teaming assignments - Store Impact through Job Codes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# ============================================================
# CACHE INITIALIZATION
# ============================================================

# Initialize cache on startup
cache = init_cache()

@app.on_event("startup")
async def startup_event():
    """Initialize cache and start sync thread on startup"""
    print("Initializing Job Code Cache...")
    
    # Try to load Polaris data - CSV is the primary fallback
    polaris_data = None
    
    # First attempt: Load from CSV
    try:
        print(f"Loading Polaris data from CSV: {POLARIS_DATA_FILE}")
        if os.path.exists(POLARIS_DATA_FILE):
            polaris_data = pd.read_csv(POLARIS_DATA_FILE)
            print(f"Successfully loaded {len(polaris_data)} job codes from CSV")
    except Exception as e:
        print(f"Error loading Polaris CSV: {e}")
    
    # Second attempt: Load user counts
    try:
        if os.path.exists(USER_COUNTS_FILE):
            user_counts_df = pd.read_csv(USER_COUNTS_FILE)
            if polaris_data is not None and 'job_code' in user_counts_df.columns:
                user_counts_df['job_code'] = user_counts_df['job_code'].str.strip()
                polaris_data = polaris_data.merge(user_counts_df, on='job_code', how='left')
                polaris_data['user_count'] = polaris_data['user_count'].fillna(0).astype(int)
                print(f"Merged user counts into Polaris data")
    except Exception as e:
        print(f"Error loading user counts: {e}")
        if polaris_data is not None and 'user_count' not in polaris_data.columns:
            polaris_data['user_count'] = 0
    
    # Sync to cache
    if polaris_data is not None:
        cache.sync_polaris_data(polaris_data)
        print(f"Cache synced with {len(polaris_data)} job codes")
    else:
        print("WARNING: No polaris data loaded")
    
    # Load and sync Job Code Master (Excel or JSON fallback) to cache
    master_records = []
    
    # First try: Load from Excel (requires openpyxl)
    try:
        print(f"Loading Job Code Master from Excel: {JOB_CODE_MASTER_EXCEL}")
        if os.path.exists(JOB_CODE_MASTER_EXCEL):
            master_df = pd.read_excel(JOB_CODE_MASTER_EXCEL)
            master_records = master_df.to_dict('records')
            print(f"âœ“ Loaded {len(master_records)} enrichment records from Excel")
    except Exception as e:
        print(f"âš ï¸ Could not load Excel (openpyxl not available or file error): {e}")
        master_records = []
    
    # Second try: Load from JSON fallback (created by convert_excel_to_json.py)
    if not master_records:
        json_fallback_path = os.path.join(BASE_DIR, "job_codes_master.json")
        try:
            print(f"Attempting JSON fallback: {json_fallback_path}")
            if os.path.exists(json_fallback_path):
                with open(json_fallback_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    master_records = json_data.get('job_codes', [])
                    print(f"âœ“ Loaded {len(master_records)} enrichment records from JSON fallback")
            else:
                print(f"â„¹ JSON fallback not found. Run: python convert_excel_to_json.py")
        except Exception as e:
            print(f"âš ï¸ Could not load JSON fallback: {e}")
    
    # Sync all loaded master records to cache
    if master_records:
        synced_count = 0
        for idx, row in enumerate(master_records):
            # Handle both SMART Job Code and job_code field names
            job_code = str(row.get('SMART Job Code') or row.get('job_code') or '').strip()
            if job_code:
                try:
                    cache.update_master_data(job_code, {
                        'workday_code': str(row.get('Workday Job Code', '') or ''),
                        'category': str(row.get('Category', '') or ''),
                        'job_family': str(row.get('Job Family', '') or ''),
                        'pg_level': str(row.get('PG Level', '') or ''),
                        'supervisor': bool(row.get('Supervisor?') == 'Yes' if row.get('Supervisor?') else False),
                        'reports_to': str(row.get('Reports to Title', '') or ''),
                        'position_mgmt': str(row.get('Position Mgmt or Job Mgmt', '') or ''),
                        'notes': str(row.get('Notes', '') or ''),
                        'created_by': 'system_startup',
                        'updated_by': 'system_startup',
                    })
                    synced_count += 1
                except Exception as e:
                    if idx < 5:  # Only log first 5 errors to avoid spam
                        print(f"Warning: Failed to sync job code {job_code}: {e}")
        print(f"âœ“ Synced {synced_count} job codes from master data to cache")
    else:
        print(f"â„¹ No master enrichment data loaded (job codes will show without details)")
    
    # Start background sync thread (will attempt BigQuery every 30 min)
    cache.start_sync_thread(sync_polaris_from_bigquery if HAS_BIGQUERY else None)
    print("Cache initialized and sync thread started")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop cache sync thread on shutdown"""
    print("Stopping cache sync thread...")
    cache.stop_sync_thread()

# ============================================================
# USER MANAGEMENT
# ============================================================

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    # Default admin user (change password immediately!)
    default_users = {
        "admin": {
            "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
            "role": "admin",
            "name": "Administrator",
            "approved": True
        }
    }
    save_users(default_users)
    return default_users

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_sessions():
    """Load active sessions"""
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    """Save sessions"""
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

def get_current_user(request: Request):
    """Get current user from session cookie"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    sessions = load_sessions()
    if session_id in sessions:
        username = sessions[session_id]["username"]
        users = load_users()
        if username in users and users[username].get("approved", False):
            return {"username": username, **users[username]}
    return None

def require_auth(request: Request):
    """Require authenticated user"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

def require_admin(request: Request):
    """Require admin user"""
    user = require_auth(request)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# ============================================================
# DATA LOADING
# ============================================================

import numpy as np
import math

def sync_polaris_from_bigquery():
    """
    Sync Polaris job code data from BigQuery
    
    Returns:
        Pandas DataFrame with columns: job_code, job_nm, user_count
        Returns None if sync fails
    """
    if not HAS_BIGQUERY:
        print("BigQuery not available, skipping sync")
        return None
    
    try:
        client = bigquery.Client()
        
        # Query polaris data - adjust this query to your actual BigQuery schema
        query = """
        SELECT DISTINCT
            UPPER(TRIM(job_code)) as job_code,
            job_nm,
            COUNT(DISTINCT worker_id) as user_count
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE job_code IS NOT NULL
        GROUP BY job_code, job_nm
        ORDER BY job_code
        """
        
        print("Querying BigQuery for Polaris data...")
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to DataFrame
        df = results.to_dataframe()
        print(f"Successfully retrieved {len(df)} job codes from BigQuery")
        
        return df
    except Exception as e:
        print(f"Error syncing from BigQuery: {e}")
        return None

def to_json_safe(val):
    """Convert numpy types and NaN to JSON-safe Python types"""
    if val is None:
        return None
    if isinstance(val, (np.integer, np.int64, np.int32)):
        return int(val)
    if isinstance(val, (np.floating, np.float64, np.float32)):
        if np.isnan(val) or math.isnan(val):
            return None
        return float(val)
    if isinstance(val, np.ndarray):
        return [to_json_safe(v) for v in val.tolist()]
    if isinstance(val, list):
        return [to_json_safe(v) for v in val]
    if pd.isna(val):
        return None
    return val

    
def compute_status(row, job_code):
    """Compute status and status_detail for a job code record based on source data availability"""
    from_polaris = row.get('_from_polaris', False)
    from_workforce = row.get('_from_workforce', False)
    from_teaming = row.get('_from_teaming', False)
    
    # Determine status category
    if from_polaris and (from_workforce or from_polaris) and from_teaming:
        # Assigned: In Polaris, has enrichment data (Workforce or Polaris), and has teaming
        status = "Assigned"
        category = "Complete"
        reason = "Job code is fully assigned with complete data"
        action = None
    elif from_polaris and not from_teaming:
        # Review: In Polaris but not in Teaming
        status = "Review"
        category = "Missing"
        reason = "Job code exists in Polaris but no team assignment found"
        action = "Assign team from Teaming"
    elif from_polaris and from_teaming and not from_workforce:
        # Review: In Polaris + Teaming but missing Workforce enrichment
        status = "Review"
        category = "Incomplete"
        reason = "Job code missing enrichment data (Workforce Table)"
        action = "Add to Workforce Table"
    elif from_teaming and not from_polaris:
        # Review: In Teaming but not in Polaris (orphan)
        status = "Review"
        category = "Orphan"
        reason = "Team assignment exists but job code not in Polaris"
        action = "Add to Polaris or remove from Teaming"
    elif from_workforce and not from_polaris:
        # Review: In Workforce but not in Polaris (orphan)
        status = "Review"
        category = "Orphan"
        reason = "Workforce enrichment data exists but job code not in Polaris"
        action = "Add to Polaris or remove from Workforce"
    else:
        # Review: No clear source or missing data
        status = "Review"
        category = "Mismatch"
        reason = f"Unexpected data configuration (P:{from_polaris}, W:{from_workforce}, T:{from_teaming})"
        action = "Investigate data sources"
    
    status_detail = {
        "category": category,
        "reason": reason,
        "action": action,
        "sources": {
            "polaris": from_polaris,
            "workforce": from_workforce,
            "teaming": from_teaming
        }
    }
    
    return status, status_detail

def load_job_code_data():
    """Load and merge job code data from Polaris and Teaming sources"""
    # Check files exist
    if not os.path.exists(POLARIS_DATA_FILE):
        raise FileNotFoundError(f"Polaris data file not found: {POLARIS_DATA_FILE}")
    
    print(f"Loading Polaris data from: {POLARIS_DATA_FILE}")
    
    # Load Polaris data
    polaris_df = pd.read_csv(POLARIS_DATA_FILE)
    polaris_df['job_code'] = polaris_df['job_code'].str.strip()
    
    # Load user counts if available
    if os.path.exists(USER_COUNTS_FILE):
        print(f"Loading user counts from: {USER_COUNTS_FILE}")
        user_counts_df = pd.read_csv(USER_COUNTS_FILE)
        user_counts_df['job_code'] = user_counts_df['job_code'].str.strip()
        polaris_df = polaris_df.merge(user_counts_df, on='job_code', how='left')
        polaris_df['user_count'] = polaris_df['user_count'].fillna(0).astype(int)
    else:
        print("User counts file not found, defaulting to 0")
        polaris_df['user_count'] = 0
    
    # Try to load teaming data (optional)
    teaming_df = None
    merged = polaris_df.copy()
    has_team_data = False  # Initialize BEFORE try block
    
    if os.path.exists(TEAMING_DATA_FILE):
        try:
            print(f"Loading Teaming data from: {TEAMING_DATA_FILE}")
            # Load CSV or Excel based on file extension
            if TEAMING_DATA_FILE.endswith('.csv'):
                teaming_df = pd.read_csv(TEAMING_DATA_FILE)
            else:
                teaming_df = pd.read_excel(TEAMING_DATA_FILE)
            
            # Check which columns are available
            available_cols = list(teaming_df.columns)
            print(f"Available Teaming columns: {available_cols}")
            
            # Create composite key from available columns (divNumber-deptNumber-jobCode)
            teaming_df['composite_job_code'] = (
                teaming_df['divNumber'].astype(str).str.strip() + '-' +
                teaming_df['deptNumber'].astype(str).str.strip() + '-' +
                teaming_df['jobCode'].astype(str).str.strip()
            )
            
            # Check if teaming has full columns needed for aggregation
            required_team_cols = ['jobCodeTitle', 'teamName', 'teamId', 'workgroupName', 'workgroupId']
            has_team_data = all(col in available_cols for col in required_team_cols)
            
            if has_team_data:
                print("Full teaming data available - aggregating by team")
                # Get unique teaming info
                teaming_summary = teaming_df.groupby('composite_job_code').agg({
                    'jobCodeTitle': 'first',
                    'teamName': lambda x: list(x.unique()),
                    'teamId': lambda x: list(x.unique()),
                    'workgroupName': lambda x: list(x.unique()),
                    'workgroupId': lambda x: list(x.unique()),
                    'divNumber': 'first',
                    'deptNumber': 'first',
                    'jobCode': 'first'
                }).reset_index()
                
                # Merge with Polaris
                merged = polaris_df.merge(
                    teaming_summary,
                    left_on='job_code',
                    right_on='composite_job_code',
                    how='left'
                )
            else:
                print(f"Partial teaming data - only {available_cols} available")
                # Just use the basic columns for division/department mapping
                teaming_summary = teaming_df[['composite_job_code', 'divNumber', 'deptNumber', 'jobCode']].drop_duplicates()
                
                # Merge with Polaris
                merged = polaris_df.merge(
                    teaming_summary,
                    left_on='job_code',
                    right_on='composite_job_code',
                    how='left'
                )
            
        except ImportError as e:
            print(f"âš ï¸  WARNING: Cannot load Excel teaming data: {e}")
            print("   Proceeding without teaming data (openpyxl not installed)")
            teaming_df = pd.DataFrame()
            merged = polaris_df.copy()  # Start fresh with just Polaris data
            has_team_data = False  # Explicitly set to False
        except Exception as e:
            print(f"âš ï¸  WARNING: Error loading teaming data: {e}")
            import traceback
            traceback.print_exc()
            teaming_df = pd.DataFrame()
            merged = polaris_df.copy()  # Start fresh with just Polaris data
            has_team_data = False  # Explicitly set to False
    else:
        print(f"Teaming data file not found at {TEAMING_DATA_FILE}, using Polaris data only")
        teaming_df = pd.DataFrame()
        has_team_data = False  # Explicitly set to False
    
    # Mark status
    merged['status'] = merged.apply(
        lambda row: 'Assigned' if 'composite_job_code' in merged.columns and pd.notna(row.get('composite_job_code')) else 'Missing',
        axis=1
    )
    
    # Add default columns for missing team data
    if not has_team_data:
        merged['jobCodeTitle'] = merged['job_nm']  # Use job name as title
        merged['job_title'] = merged['job_nm']  # Also set job_title
        # Properly initialize list columns - create independent lists for each row
        merged['teamName'] = pd.Series([[] for _ in range(len(merged))], index=merged.index)
        merged['teamId'] = pd.Series([[] for _ in range(len(merged))], index=merged.index)
        merged['workgroupName'] = pd.Series([[] for _ in range(len(merged))], index=merged.index)
        merged['workgroupId'] = pd.Series([[] for _ in range(len(merged))], index=merged.index)
    else:
        # Fill missing job titles
        merged['job_title'] = merged.apply(
            lambda row: row['jobCodeTitle'] if pd.notna(row['jobCodeTitle']) else row['job_nm'],
            axis=1
        )
        # Ensure list columns are properly initialized
        merged['teamName'] = merged['teamName'].apply(lambda x: x if isinstance(x, list) else [])
        merged['teamId'] = merged['teamId'].apply(lambda x: x if isinstance(x, list) else [])
        merged['workgroupName'] = merged['workgroupName'].apply(lambda x: x if isinstance(x, list) else [])
        merged['workgroupId'] = merged['workgroupId'].apply(lambda x: x if isinstance(x, list) else [])
    
    return merged, teaming_df

def get_team_options():
    """Get available teams from teaming data"""
    try:
        print(f"[GET /api/teams] Starting get_team_options()")
        
        if not os.path.exists(TEAMING_DATA_FILE):
            print(f"[GET /api/teams] ERROR: Teaming data file not found: {TEAMING_DATA_FILE}")
            raise FileNotFoundError(f"Teaming data file not found: {TEAMING_DATA_FILE}")
        
        print(f"[GET /api/teams] Loading file: {TEAMING_DATA_FILE}")
        
        # Load CSV or Excel based on file extension
        if TEAMING_DATA_FILE.endswith('.csv'):
            teaming_df = pd.read_csv(TEAMING_DATA_FILE)
        else:
            teaming_df = pd.read_excel(TEAMING_DATA_FILE)
        
        print(f"[GET /api/teams] Loaded {len(teaming_df)} rows with columns: {list(teaming_df.columns)}")
        
        # Check if team columns exist
        team_cols = ['teamName', 'teamId', 'workgroupName', 'workgroupId']
        available_cols = [col for col in team_cols if col in teaming_df.columns]
        
        print(f"[GET /api/teams] Available team columns: {available_cols}")
        
        if not available_cols:
            # No team data available - return empty list
            print(f"[GET /api/teams] WARNING: No team columns found in teaming data")
            return []
        
        # Only use available columns
        teams = teaming_df[available_cols].drop_duplicates()
        print(f"[GET /api/teams] Found {len(teams)} unique team combinations")
        
        # Convert to JSON-safe format
        result = []
        for idx, (_, row) in enumerate(teams.iterrows()):
            try:
                team_entry = {}
                for col in available_cols:
                    try:
                        val = row[col]
                        if col == 'teamId' or col == 'workgroupId':
                            team_entry[col] = to_json_safe(val)
                        else:
                            team_entry[col] = str(val) if pd.notna(val) else ""
                    except Exception as e:
                        print(f"[GET /api/teams] ERROR processing column {col} for row {idx}: {type(e).__name__}: {e}")
                        team_entry[col] = None
                result.append(team_entry)
            except Exception as e:
                print(f"[GET /api/teams] ERROR processing row {idx}: {type(e).__name__}: {e}")
                continue
        
        print(f"[GET /api/teams] Successfully created {len(result)} team entries")
        return result
    
    except Exception as e:
        print(f"[GET /api/teams] FATAL ERROR in get_team_options(): {type(e).__name__}: {e}")
        import traceback
        print(f"[GET /api/teams] Traceback: {traceback.format_exc()}")
        raise

# ============================================================
# UPDATE REQUESTS
# ============================================================

def load_requests():
    """Load update requests"""
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_requests(requests):
    """Save update requests"""
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(requests, f, indent=2)

def load_rejection_history():
    """Load rejection history"""
    if os.path.exists(REJECTION_HISTORY_FILE):
        with open(REJECTION_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {"job_codes": {}, "teaming": {}}

def save_rejection_history(history):
    """Save rejection history"""
    with open(REJECTION_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_rejection_to_history(job_code, request_type, reason, requested_by, rejected_by):
    """Add a rejection to the history for future reference"""
    history = load_rejection_history()
    
    if request_type == "job_code":
        if job_code not in history["job_codes"]:
            history["job_codes"][job_code] = []
        history["job_codes"][job_code].append({
            "reason": reason,
            "requested_by": requested_by,
            "rejected_by": rejected_by,
            "rejected_date": datetime.now().isoformat()
        })
    elif request_type == "teaming":
        if job_code not in history["teaming"]:
            history["teaming"][job_code] = []
        history["teaming"][job_code].append({
            "reason": reason,
            "requested_by": requested_by,
            "rejected_by": rejected_by,
            "rejected_date": datetime.now().isoformat()
        })
    
    save_rejection_history(history)

# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    """Redirect to frontend"""
    return RedirectResponse(url="/static/index.html")

@app.post("/api/check-email")
async def check_email(request: Request):
    """Check if a user exists with this email"""
    data = await request.json()
    email = data.get("email", "").lower().strip()
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    users = load_users()
    
    # Search for user by email
    for username, user in users.items():
        if user.get("email", "").lower() == email:
            return {
                "exists": True,
                "name": user.get("name", username),
                "status": "approved" if user.get("approved", False) else "pending"
            }
    
    return {"exists": False}

@app.post("/api/login-by-email")
async def login_by_email(request: Request, response: Response):
    """Passwordless login for approved users - just email"""
    data = await request.json()
    email = data.get("email", "").lower().strip()
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    users = load_users()
    
    # Find user by email
    found_username = None
    for uname, user in users.items():
        if user.get("email", "").lower() == email:
            found_username = uname
            break
    
    if not found_username:
        raise HTTPException(status_code=401, detail="User not found")
    
    user = users[found_username]
    
    if not user.get("approved", False):
        raise HTTPException(status_code=403, detail="Account pending approval")
    
    # Create session
    session_id = secrets.token_hex(32)
    sessions = load_sessions()
    sessions[session_id] = {
        "username": found_username,
        "created": datetime.now().isoformat()
    }
    save_sessions(sessions)
    
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"success": True, "user": {
        "username": found_username, 
        "role": user["role"], 
        "name": user["name"],
        "default_tab": user.get("default_tab", "none")
    }}

@app.post("/api/login")
async def login(request: Request, response: Response):
    """User login - supports both email and username (legacy, with password)"""
    data = await request.json()
    email = data.get("email", "").lower().strip()
    username = data.get("username", "").lower().strip()
    password = data.get("password", "")
    
    users = load_users()
    
    # Find user by email or username
    found_username = None
    if email:
        # Search by email
        for uname, user in users.items():
            if user.get("email", "").lower() == email:
                found_username = uname
                break
    if not found_username and username:
        # Fall back to username
        if username in users:
            found_username = username
    
    if not found_username:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users[found_username]
    if user["password_hash"] != hash_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("approved", False):
        raise HTTPException(status_code=403, detail="Account pending approval")
    
    # Create session
    session_id = secrets.token_hex(32)
    sessions = load_sessions()
    sessions[session_id] = {
        "username": found_username,
        "created": datetime.now().isoformat()
    }
    save_sessions(sessions)
    
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"success": True, "user": {
        "username": found_username, 
        "role": user["role"], 
        "name": user["name"],
        "default_tab": user.get("default_tab", "none")
    }}

@app.post("/api/logout")
async def logout(request: Request, response: Response):
    """User logout"""
    session_id = request.cookies.get("session_id")
    if session_id:
        sessions = load_sessions()
        sessions.pop(session_id, None)
        save_sessions(sessions)
    response.delete_cookie("session_id")
    return {"success": True}

def compute_source_badges(from_polaris, from_workforce, from_teaming, **kwargs):
    """
    Compute source badges indicating which data sources contain this job code.
    
    Returns list of badge strings like ['P', 'PW', 'W', 'PT', 'T'] based on source combination.
    
    Mapping:
    - P = Polaris only
    - PW = Polaris + Workforce
    - W = Workforce only
    - PT = Polaris + Teaming
    - T = Teaming only
    """
    sources = []
    
    if from_polaris:
        sources.append('P')
    if from_workforce:
        sources.append('W')
    if from_teaming:
        sources.append('T')
    
    if not sources:
        return []  # No sources
    
    # Return badges as sorted list
    return sorted(list(set(sources)))

def send_email_notification(subject: str, body: str, to_email: str = NOTIFY_EMAIL):
    """
    Send email notification using Walmart's internal SMTP gateway.
    Same method as ProjectsinStores - no auth required on Walmart network/VPN.
    Runs in background thread to not block the request.
    """
    def send():
        email_sent = False
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = FROM_EMAIL
            msg['To'] = to_email
            
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            print(f"\n{'='*60}")
            print(f"SENDING EMAIL NOTIFICATION")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"{'='*60}")
            
            # Walmart Internal SMTP Gateway (no auth required)
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=5) as server:
                server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
                print(f"[OK] Email sent to {to_email}!")
                email_sent = True
                
        except Exception as e:
            print(f"âš ï¸ Email sending failed (outside Walmart network?): {e}")
            print(f"Troubleshooting: Ensure you're on Walmart VPN or network")
            
            # Queue for manual review
            try:
                log_file = os.path.join(DATA_DIR, "email_queue.json")
                queue = []
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        queue = json.load(f)
                queue.append({
                    "to": to_email,
                    "subject": subject,
                    "body": body,
                    "timestamp": datetime.now().isoformat(),
                    "sent": False,
                    "error": str(e)
                })
                with open(log_file, 'w') as f:
                    json.dump(queue, f, indent=2)
                print(f"Email queued to {log_file} for manual review")
            except Exception as queue_error:
                print(f"Could not queue email: {queue_error}")
        
        return email_sent
    
    # Run in background to not block the request
    threading.Thread(target=send, daemon=True).start()

@app.post("/api/register")
async def register(request: Request):
    """Register new user (requires admin approval) - passwordless"""
    data = await request.json()
    username = data.get("username", "").lower()
    name = data.get("name", "")
    email = data.get("email", "").lower()
    
    if not username or not name or not email:
        raise HTTPException(status_code=400, detail="Name and email are required")
    
    users = load_users()
    
    # Check if username or email already exists
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    for uname, user in users.items():
        if user.get("email", "").lower() == email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    users[username] = {
        "password_hash": "",  # No password needed
        "role": "user",
        "name": name,
        "email": email,
        "approved": False,
        "registered": datetime.now().isoformat()
    }
    save_users(users)
    
    # Send email notification to ATCTEAMSUPPORT
    email_body = f"""
    <html>
    <body>
    <h2>New Access Request - Job Code Teaming Dashboard</h2>
    <p>A new user has requested access to the Job Code Teaming Dashboard:</p>
    <table border="1" cellpadding="10" style="border-collapse: collapse;">
        <tr><td><strong>Name:</strong></td><td>{name}</td></tr>
        <tr><td><strong>Username:</strong></td><td>{username}</td></tr>
        <tr><td><strong>Email:</strong></td><td>{email or 'Not provided'}</td></tr>
        <tr><td><strong>Requested:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
    </table>
    <p>Please log into the <a href="http://localhost:8080">Job Code Teaming Dashboard</a> to approve or reject this request.</p>
    <p>Go to <strong>Admin</strong> tab &gt; <strong>User Management</strong> to manage access.</p>
    </body>
    </html>
    """
    send_email_notification(
        subject=f"[Action Required] New Access Request: {name}",
        body=email_body
    )
    
    return {"success": True, "message": "Registration submitted. ATCTEAMSUPPORT has been notified and will review your request."}

@app.get("/api/me")
async def get_me(request: Request):
    """Get current user info"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"username": user["username"], "role": user["role"], "name": user["name"]}

@app.get("/api/job-codes")
async def get_job_codes(request: Request):
    """Get all job codes with enrichment data from cache and master table"""
    user = require_auth(request)
    
    try:
        print("[GET /api/job-codes] Starting endpoint")
        # Get merged data from cache (Polaris + Master)
        job_codes = cache.get_job_codes()
        print(f"[GET /api/job-codes] Got {len(job_codes) if job_codes else 0} job codes from cache")
        
        if not job_codes:
            return {"job_codes": [], "total": 0}
        
        # Merge with Teaming data if available (optional)
        teaming_map = {}
        try:
            print("[GET /api/job-codes] Loading Teaming data...")
            merged_df, _ = load_job_code_data()
            print(f"[GET /api/job-codes] Loaded teaming data: {len(merged_df) if merged_df is not None else 0} rows")
            
            if merged_df is not None and len(merged_df) > 0:
                print(f"[GET /api/job-codes] Processing {len(merged_df)} teaming rows")
                for idx, (_, row) in enumerate(merged_df.iterrows()):
                    try:
                        # Use bracket notation for pandas Series, not .get()
                        jc = str(row['job_code']).strip() if pd.notna(row['job_code']) else ""
                        
                        if jc:
                            # Extract team data safely - handle lists/arrays from aggregation
                            if 'teamName' in row.index:
                                teams = row['teamName']
                                # Check if it's a list or numpy array
                                if isinstance(teams, (list, np.ndarray)):
                                    teams = list(teams) if isinstance(teams, np.ndarray) else teams
                                elif not pd.isna(teams):
                                    teams = [teams]
                                else:
                                    teams = []
                            else:
                                teams = []
                            
                            if 'teamId' in row.index:
                                team_ids = row['teamId']
                                if isinstance(team_ids, (list, np.ndarray)):
                                    team_ids = list(team_ids) if isinstance(team_ids, np.ndarray) else team_ids
                                elif not pd.isna(team_ids):
                                    team_ids = [team_ids]
                                else:
                                    team_ids = []
                            else:
                                team_ids = []
                            
                            if 'workgroupName' in row.index:
                                workgroups = row['workgroupName']
                                if isinstance(workgroups, (list, np.ndarray)):
                                    workgroups = list(workgroups) if isinstance(workgroups, np.ndarray) else workgroups
                                elif not pd.isna(workgroups):
                                    workgroups = [workgroups]
                                else:
                                    workgroups = []
                            else:
                                workgroups = []
                            
                            teaming_map[jc] = {
                                "teams": [to_json_safe(t) for t in teams],
                                "team_ids": [to_json_safe(t) for t in team_ids],
                                "workgroups": [to_json_safe(w) for w in workgroups],
                                "division": to_json_safe(row['divNumber']) if 'divNumber' in row.index else None,
                                "department": to_json_safe(row['deptNumber']) if 'deptNumber' in row.index else None,
                            }
                    except Exception as row_error:
                        print(f"[GET /api/job-codes] Warning: Error processing row {idx}: {row_error}")
                        import traceback
                        traceback.print_exc()
                        continue
                print(f"[GET /api/job-codes] Built teaming map for {len(teaming_map)} job codes")
        except Exception as e:
            print(f"[GET /api/job-codes] Warning: Could not load Teaming data: {e}")
            import traceback
            traceback.print_exc()
            teaming_map = {}
        
        # Build result
        print(f"[GET /api/job-codes] Building result from {len(job_codes)} job codes")
        result = []
        for idx, jc in enumerate(job_codes):
            try:
                job_code_str = jc.get("job_code", "")
                teaming_info = teaming_map.get(job_code_str, {})
                
                # Determine source tracking flags
                # A job code is from Polaris if it exists in the cache (filtered from Polaris CSV)
                from_polaris = bool(True)  # All items in job_codes come from cache which loads Polaris
                
                # A job code has workforce enrichment if it has any of these fields
                from_workforce = bool(
                    jc.get("workday_code") or
                    jc.get("category") or
                    jc.get("job_family") or
                    jc.get("pg_level")
                )
                
                # A job code has team assignment if it's in teaming_map or has team data
                from_teaming = bool(teaming_info and (
                    teaming_info.get("teams") or
                    teaming_info.get("team_ids") or
                    teaming_info.get("workgroups")
                ))
                
                # Compute badges
                source_badges = compute_source_badges(from_polaris, from_workforce, from_teaming)
                
                # Compute status using the compute_status function
                status_data = {
                    '_from_polaris': from_polaris,
                    '_from_workforce': from_workforce,
                    '_from_teaming': from_teaming
                }
                computed_status, status_detail = compute_status(status_data, job_code_str)
                
                result.append({
                    "job_code": job_code_str,
                    "job_title": jc.get("job_nm", ""),
                    "job_name": jc.get("job_nm", ""),
                    "status": computed_status,
                    "status_detail": status_detail,
                    "source_badges": source_badges,
                    "teams": teaming_info.get("teams", []),
                    "team_ids": teaming_info.get("team_ids", []),
                    "workgroups": teaming_info.get("workgroups", []),
                    "division": teaming_info.get("division"),
                    "department": teaming_info.get("department"),
                    "user_count": to_json_safe(jc.get("user_count", 0)),
                    # Master table fields
                    "workday_code": jc.get("workday_code", ""),
                    "category": jc.get("category", ""),
                    "job_family": jc.get("job_family", ""),
                    "pg_level": jc.get("pg_level", ""),
                    "supervisor": jc.get("supervisor", False),
                    "notes": jc.get("notes", ""),
                })
            except Exception as e:
                print(f"[GET /api/job-codes] Error processing job code {idx}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"[GET /api/job-codes] SUCCESS: Returning {len(result)} job codes")
        return {"job_codes": result, "total": len(result)}
        
    except Exception as e:
        print(f"[GET /api/job-codes] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving job codes: {str(e)}")

@app.get("/api/teams")
async def get_teams(request: Request):
    """Get available teams"""
    try:
        print("[GET /api/teams] Endpoint called")
        user = require_auth(request)
        print(f"[GET /api/teams] Auth passed for user: {user.get('username')}")
        teams = get_team_options()
        print(f"[GET /api/teams] Returning {len(teams)} teams")
        return {"teams": teams}
    except HTTPException as e:
        print(f"[GET /api/teams] HTTPException: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        print(f"[GET /api/teams] UNHANDLED EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving teams: {str(e)}")

@app.post("/api/job-codes/lookup")
async def lookup_job_code_employees(request: Request):
    """
    Lookup employees by job code and pay type using Polaris BigQuery data.
    
    Body:
    {
        "job_code": "30-49-855",
        "pay_types": ["H", "S"]  # or comma-separated string "H,S"
    }
    """
    user = require_auth(request)
    
    if not HAS_BIGQUERY:
        raise HTTPException(status_code=503, detail="BigQuery not available. Missing google-cloud-bigquery library.")
    
    try:
        data = await request.json()
        job_code = data.get("job_code", "").strip()
        pay_types = data.get("pay_types", ["H", "S"])
        
        # Handle both list and comma-separated string
        if isinstance(pay_types, str):
            pay_types = [pt.strip() for pt in pay_types.split(",")]
        
        if not job_code:
            raise HTTPException(status_code=400, detail="job_code is required")
        
        # Query Polaris for employees with this job code and pay type
        # Load credentials explicitly for any user context
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
        
        credentials_path = r"C:\ProgramData\gcloud\application_default_credentials.json"
        try:
            # Try service account first
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        except:
            # Fall back to user credentials (authorized_user)
            from google.auth import load_credentials_from_file
            credentials, project = load_credentials_from_file(credentials_path)
            client = bigquery.Client(credentials=credentials, project=project)
        
        # Build pay type filter
        pay_type_list = "', '".join(pay_types)
        query = f"""
        SELECT DISTINCT
            CAST(worker_id AS STRING) as worker_id,
            first_name,
            last_name,
            job_code,
            job_nm,
            worker_payment_type,
            CAST(location_id AS STRING) as location_id,
            location_nm,
            hire_date,
            empl_type_code
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE job_code = '{job_code}'
          AND worker_payment_type IN ('{pay_type_list}')
        ORDER BY location_id, worker_id
        LIMIT 500
        """
        
        print(f"[LOOKUP] Querying for job_code='{job_code}', pay_types={pay_types}")
        results = client.query(query, project="polaris-analytics-prod").result()
        rows = [dict(row) for row in results]
        
        # Convert to list of dictionaries
        workers = []
        for row in rows:
            workers.append({
                "worker_id": str(row.get("worker_id", "")),
                "first_name": str(row.get("first_name", "")),
                "last_name": str(row.get("last_name", "")),
                "job_code": str(row.get("job_code", "")),
                "job_nm": str(row.get("job_nm", "")),
                "pay_type": str(row.get("worker_payment_type", "")),
                "location_id": str(row.get("location_id", "")),
                "location_nm": str(row.get("location_nm", "")),
            })
        
        return {
            "job_code": job_code,
            "pay_types": pay_types,
            "employee_count": len(workers),
            "workers": workers,
            "query_timestamp": datetime.now().isoformat()
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        print(f"[ERROR] Job code lookup error: {e}")
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

@app.get("/api/missing-job-codes-report")
async def missing_job_codes_report(request: Request):
    """
    Generate CSV report of Missing job codes with sample impacted users.
    Returns: Job Code, Role/Title, Impacted Count, Sample Employee, Employee Name
    """
    user = require_auth(request)
    
    try:
        print("[MISSING REPORT] Starting missing job codes report generation")
        
        # Get all job codes with their status
        job_codes = cache.get_job_codes()
        print(f"[MISSING REPORT] Loaded {len(job_codes) if job_codes else 0} total job codes")
        
        if not job_codes:
            raise HTTPException(status_code=404, detail="No job codes available")
        
        # Load teaming data to get status
        merged_df, _ = load_job_code_data()
        print(f"[MISSING REPORT] Loaded teaming data: {len(merged_df) if merged_df is not None else 0} rows")
        
        # Build status map
        status_map = {}
        if merged_df is not None and len(merged_df) > 0:
            for _, row in merged_df.iterrows():
                job_code_str = str(row['job_code']).strip() if pd.notna(row['job_code']) else ""
                status = 'Assigned' if pd.notna(row.get('composite_job_code')) else 'Missing'
                status_map[job_code_str] = status
        
        # Filter for Missing status job codes
        missing_codes = []
        for jc in job_codes:
            job_code_str = jc.get("job_code", "")
            status = status_map.get(job_code_str, "Unknown")
            if status == "Missing":
                missing_codes.append({
                    "job_code": job_code_str,
                    "job_title": jc.get("job_nm", ""),
                    "user_count": jc.get("user_count", 0),
                })
        
        print(f"[MISSING REPORT] Found {len(missing_codes)} missing job codes")
        
        # Build CSV data
        csv_rows = []
        csv_rows.append({
            "Job Code": "Job Code",
            "Role": "Role/Title",
            "Impacted Count": "Impacted User Count",
            "Sample Employee ID": "Sample Employee",
            "Sample Employee Name": "Employee Name"
        })
        
        # Try to get sample employees if BigQuery is available
        for idx, missing_code in enumerate(missing_codes):
            job_code = missing_code["job_code"]
            job_title = missing_code["job_title"]
            user_count = missing_code["user_count"]
            
            sample_employee = "-"
            sample_employee_name = "-"
            
            # Try to lookup one employee if BigQuery is available
            if HAS_BIGQUERY:
                try:
                    from google.oauth2 import service_account
                    credentials_path = r"C:\ProgramData\gcloud\application_default_credentials.json"
                    try:
                        credentials = service_account.Credentials.from_service_account_file(credentials_path)
                        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
                    except:
                        from google.auth import load_credentials_from_file
                        credentials, project = load_credentials_from_file(credentials_path)
                        client = bigquery.Client(credentials=credentials, project=project)
                    
                    # Query for one employee
                    query = f"""
                    SELECT DISTINCT
                        CAST(worker_id AS STRING) as worker_id,
                        first_name,
                        last_name
                    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
                    WHERE job_code = '{job_code}'
                    LIMIT 1
                    """
                    
                    results = client.query(query, project="polaris-analytics-prod").result()
                    rows = list(results)
                    
                    if rows:
                        row = rows[0]
                        sample_employee = str(row.worker_id)
                        sample_employee_name = f"{row.first_name} {row.last_name}".strip()
                        print(f"[MISSING REPORT] Found sample employee for {job_code}: {sample_employee} - {sample_employee_name}")
                except Exception as e:
                    print(f"[MISSING REPORT] Could not lookup employee for {job_code}: {e}")
            
            csv_rows.append({
                "Job Code": job_code,
                "Role": job_title,
                "Impacted Count": str(user_count),
                "Sample Employee ID": sample_employee,
                "Sample Employee Name": sample_employee_name
            })
        
        print(f"[MISSING REPORT] Generated {len(csv_rows)} rows (including header)")
        
        # Return as JSON - frontend can convert to CSV
        return {
            "report_type": "Missing Job Codes",
            "generated_at": datetime.now().isoformat(),
            "total_missing": len(missing_codes),
            "data": csv_rows
        }
        
    except HTTPException as e:
        print(f"[MISSING REPORT] HTTPException: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        print(f"[MISSING REPORT] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.post("/api/comprehensive-teaming-request")
async def comprehensive_teaming_request(request: Request):
    """Submit a comprehensive teaming request matching MyWalmart template format"""
    user = require_auth(request)
    data = await request.json()
    
    job_code = data.get("job_code")
    if not job_code:
        raise HTTPException(status_code=400, detail="Job code is required")
    
    # Get current values from teaming data
    previous_values = None
    try:
        merged, teaming_df = load_job_code_data()
        job_data = merged[merged['job_code'] == job_code]
        if not job_data.empty:
            row = job_data.iloc[0]
            if pd.notna(row.get('teamName')):
                # Has existing assignment
                previous_values = {
                    "team_name": row.get('teamName', [None])[0] if isinstance(row.get('teamName'), list) else row.get('teamName'),
                    "team_id": row.get('teamId', [None])[0] if isinstance(row.get('teamId'), list) else row.get('teamId'),
                    "workgroup_name": row.get('workgroupName', [None])[0] if isinstance(row.get('workgroupName'), list) else row.get('workgroupName'),
                    "workgroup_id": row.get('workgroupId', [None])[0] if isinstance(row.get('workgroupId'), list) else row.get('workgroupId')
                }
    except Exception as e:
        print(f"Error getting previous values: {e}")
    
    requests_list = load_requests()
    
    # Create comprehensive teaming request
    new_request = {
        "id": len(requests_list) + 1,
        "type": "comprehensive_teaming",
        "status": "pending",
        "requested_by": user['username'],
        "requested_by_name": user['name'],
        "requested_at": datetime.now().isoformat(),
        "previous_values": previous_values,
        
        # Core job code info
        "job_code": job_code,
        "job_title": data.get("job_title", ""),
        "dept_number": data.get("dept_number", ""),
        "div_number": data.get("div_number", ""),
        "base_division_code": data.get("base_division_code", ""),
        
        # Team assignment
        "team_name": data.get("team_name", ""),
        "team_id": data.get("team_id", ""),
        "workgroup_name": data.get("workgroup_name", ""),
        "workgroup_id": data.get("workgroup_id", ""),
        
        # Banner codes and merch depts (arrays)
        "banner_codes": data.get("banner_codes", []),
        "merch_dept_numbers": data.get("merch_dept_numbers", []),
        
        # Role and access
        "role": data.get("role", ""),
        "access_level": data.get("access_level", ""),
        
        # Team Lead info
        "tl_job_code": data.get("tl_job_code", ""),
        "tl_job_title": data.get("tl_job_title", ""),
        "tl_dept_number": data.get("tl_dept_number", ""),
        "tl_div_number": data.get("tl_div_number", ""),
        
        # Store Leader info
        "sl_job_code": data.get("sl_job_code", ""),
        "sl_dept_number": data.get("sl_dept_number", ""),
        "sl_div_number": data.get("sl_div_number", ""),
        "sl_job_title": data.get("sl_job_title", ""),
        
        # Auto-generated action
        "action": data.get("action", ""),
        "notes": data.get("notes", "")
    }
    
    requests_list.append(new_request)
    save_requests(requests_list)
    
    # Send email notification
    subject = f"Comprehensive Teaming Request - {job_code}"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
    <h2>New Comprehensive Teaming Request</h2>
    <table border="1" cellpadding="5" style="border-collapse: collapse;">
        <tr><td><strong>Job Code:</strong></td><td>{job_code}</td></tr>
        <tr><td><strong>Job Title:</strong></td><td>{data.get('job_title', '')}</td></tr>
        <tr><td><strong>Requested by:</strong></td><td>{user['name']} ({user['username']})</td></tr>
        <tr><td><strong>Team:</strong></td><td>{data.get('team_name', '')}</td></tr>
        <tr><td><strong>Workgroup:</strong></td><td>{data.get('workgroup_name', '')}</td></tr>
        <tr><td><strong>Role:</strong></td><td>{data.get('role', '')}</td></tr>
        <tr><td><strong>Action:</strong></td><td>{data.get('action', '')}</td></tr>
        <tr><td><strong>Banner Codes:</strong></td><td>{', '.join(data.get('banner_codes', []))}</td></tr>
        <tr><td><strong>Merch Depts:</strong></td><td>{', '.join(data.get('merch_dept_numbers', []))}</td></tr>
        <tr><td><strong>Time:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
    </table>
    <p>Please review and approve in the dashboard admin panel.</p>
    </body>
    </html>
    """
    
    send_email_notification(subject, body)
    
    return {"success": True, "request_id": new_request["id"], "message": "Comprehensive teaming request submitted successfully"}

@app.post("/api/request-update")
async def request_update(request: Request):
    """Submit a request to update job code teaming"""
    user = require_auth(request)
    data = await request.json()
    
    job_code = data.get("job_code")
    team_name = data.get("team_name")
    team_id = data.get("team_id")
    workgroup_name = data.get("workgroup_name")
    workgroup_id = data.get("workgroup_id")
    notes = data.get("notes", "")
    
    if not job_code or not team_name:
        raise HTTPException(status_code=400, detail="Job code and team are required")
    
    # Get current values from teaming data
    previous_values = None
    try:
        merged, teaming_df = load_job_code_data()
        job_data = merged[merged['job_code'] == job_code]
        if not job_data.empty:
            row = job_data.iloc[0]
            if pd.notna(row.get('teamName')):
                # Has existing assignment
                previous_values = {
                    "team_name": row.get('teamName', [None])[0] if isinstance(row.get('teamName'), list) else row.get('teamName'),
                    "team_id": row.get('teamId', [None])[0] if isinstance(row.get('teamId'), list) else row.get('teamId'),
                    "workgroup_name": row.get('workgroupName', [None])[0] if isinstance(row.get('workgroupName'), list) else row.get('workgroupName'),
                    "workgroup_id": row.get('workgroupId', [None])[0] if isinstance(row.get('workgroupId'), list) else row.get('workgroupId')
                }
    except Exception as e:
        print(f"Error getting previous values: {e}")
    
    requests_list = load_requests()
    
    new_request = {
        "id": len(requests_list) + 1,
        "job_code": job_code,
        "team_name": team_name,
        "team_id": team_id,
        "workgroup_name": workgroup_name,
        "workgroup_id": workgroup_id,
        "notes": notes,
        "previous_values": previous_values,  # Track what's being replaced
        "requested_by": user["username"],
        "requested_by_name": user["name"],
        "requested_at": datetime.now().isoformat(),
        "status": "pending"
    }
    
    requests_list.append(new_request)
    save_requests(requests_list)
    
    return {"success": True, "request_id": new_request["id"]}

@app.get("/api/comprehensive-requests/export")
async def export_comprehensive_requests(request: Request):
    """Export approved comprehensive teaming requests in MyWalmart Excel template format"""
    user = require_auth(request)
    if user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    requests_list = load_requests()
    approved_comprehensive = [r for r in requests_list 
                             if r.get('type') == 'comprehensive_teaming' 
                             and r.get('status') == 'approved']
    
    if not approved_comprehensive:
        raise HTTPException(status_code=404, detail="No approved comprehensive teaming requests found")
    
    # Build export data - create one row per banner code per request
    export_data = []
    current_date = datetime.now().strftime('%m/%d/%Y')
    
    for req in approved_comprehensive:
        banner_codes = req.get('banner_codes', [''])
        if not banner_codes:
            banner_codes = ['']  # Ensure at least one row
            
        for banner_code in banner_codes:
            row = {
                'Status': 'Pending Request',  # Default status for new requests
                'Requester': req.get('requested_by_name', ''),
                'Requested Date': current_date,
                'Stage Date': '',
                'Prod Date Due': '',
                'Action': req.get('action', ''),
                'teamName': req.get('team_name', ''),
                'teamId': req.get('team_id', ''),
                'baseDivisionCode': req.get('base_division_code', ''),
                'bannerCode': banner_code,
                'workgroupId': req.get('workgroup_id', ''),
                'workgroupName': req.get('workgroup_name', ''),
                'jobCode': req.get('job_code', ''),
                'deptNumber': req.get('dept_number', ''),
                'divNumber': req.get('div_number', ''),
                'jobCodeTitle': req.get('job_title', ''),
                'accessLevel': req.get('access_level', ''),
                'role': req.get('role', ''),
                'merchDeptNumbers': ','.join(req.get('merch_dept_numbers', [])),
                'tlJobCode': req.get('tl_job_code', ''),
                'tlJobTitle': req.get('tl_job_title', ''),
                'tlDeptNumber': req.get('tl_dept_number', ''),
                'tlDivNumber': req.get('tl_div_number', ''),
                'slJobCode': req.get('sl_job_code', ''),
                'slDeptNumber': req.get('sl_dept_number', ''),
                'slDivNumber': req.get('sl_div_number', ''),
                'slJobTitle': req.get('sl_job_title', '')
            }
            export_data.append(row)
    
    return {
        "success": True, 
        "data": export_data,
        "count": len(export_data),
        "original_requests": len(approved_comprehensive),
        "message": f"Exported {len(export_data)} rows from {len(approved_comprehensive)} approved requests"
    }

@app.get("/api/requests")
async def get_requests(request: Request, status: Optional[str] = None):
    """Get update requests"""
    try:
        print("[GET /api/requests] Endpoint called")
        user = require_auth(request)
        print(f"[GET /api/requests] Auth passed for user: {user.get('username')}")
        requests_list = load_requests()
        
        # Non-admins can only see their own requests
        if user["role"] != "admin":
            requests_list = [r for r in requests_list if r["requested_by"] == user["username"]]
        
        if status:
            requests_list = [r for r in requests_list if r["status"] == status]
        
        print(f"[GET /api/requests] Returning {len(requests_list)} requests")
        return {"requests": requests_list}
    except HTTPException as e:
        print(f"[GET /api/requests] HTTPException: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        print(f"[GET /api/requests] UNHANDLED EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving requests: {str(e)}")

@app.put("/api/requests/{request_id}")
async def update_request(request_id: int, request: Request):
    """Update request - admin can edit any field with audit log, owner can edit details if pending"""
    user = require_auth(request)
    data = await request.json()
    
    requests_list = load_requests()
    for req in requests_list:
        if req["id"] == request_id:
            is_admin = user.get("role") == "admin"
            is_owner = req["requested_by"] == user["username"]
            
            # Initialize audit log if not present
            if "audit_log" not in req:
                req["audit_log"] = []
            
            # Initialize admin comments if not present
            if "admin_comments" not in req:
                req["admin_comments"] = ""
            
            # Admin can edit any field with audit logging
            if is_admin and data.get("admin_override"):
                admin_changes = []
                
                # Track which fields were changed
                editable_fields = [
                    "team_name", "team_id", "workgroup_name", "workgroup_id",
                    "role", "banner_codes", "merch_dept_numbers", "access_level",
                    "tl_job_code", "tl_job_title", "tl_dept_number", "tl_div_number",
                    "sl_job_code", "sl_dept_number", "sl_div_number", "sl_job_title",
                    "notes", "admin_comments"
                ]
                
                for field in editable_fields:
                    if field in data and data[field] != req.get(field):
                        admin_changes.append(f"{field}: {req.get(field)} → {data[field]}")
                        req[field] = data[field]
                
                # Add audit log entry
                change_reason = data.get("change_reason", "Manual admin adjustment")
                audit_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "user": user["name"],
                    "action": f"Admin edited request: {change_reason}" if change_reason else "Admin edited request",
                    "changes": admin_changes,
                    "comments": data.get("admin_comments", "")
                }
                req["audit_log"].append(audit_entry)
                req["admin_comments"] = data.get("admin_comments", req.get("admin_comments", ""))
                req["last_edited_by"] = user["username"]
                req["last_edited_at"] = datetime.now().isoformat()
            
            # Admin can also change status
            if is_admin and "status" in data and data["status"] != req.get("status"):
                old_status = req.get("status", "pending")
                req["status"] = data["status"]
                req["admin_notes"] = data.get("admin_notes", req.get("admin_notes", ""))
                req["processed_by"] = user["username"]
                req["processed_at"] = datetime.now().isoformat()
                
                # Add status change to audit log
                status_audit = {
                    "timestamp": datetime.now().isoformat(),
                    "user": user["name"],
                    "action": f"Status changed: {old_status} → {data['status']}",
                    "reason": data.get("admin_notes", "")
                }
                req["audit_log"].append(status_audit)
                
                # Add to rejection history if rejected
                if data["status"] == "rejected":
                    rejection_reason = data.get("admin_notes", "No reason provided")
                    add_rejection_to_history(
                        job_code=req["job_code"],
                        request_type="teaming",
                        reason=rejection_reason,
                        requested_by=req.get('requested_by_name', req.get('requested_by', 'Unknown')),
                        rejected_by=user['name']
                    )
            
            # Owner can edit team/notes if still pending (no admin override)
            if is_owner and req["status"] == "pending" and not data.get("admin_override"):
                owner_changes = []
                if "team_name" in data and data["team_name"] != req.get("team_name"):
                    owner_changes.append(f"team_name: {req.get('team_name')} → {data['team_name']}")
                    req["team_name"] = data["team_name"]
                if "team_id" in data and data["team_id"] != req.get("team_id"):
                    owner_changes.append(f"team_id: {req.get('team_id')} → {data['team_id']}")
                    req["team_id"] = data["team_id"]
                if "workgroup_name" in data and data["workgroup_name"] != req.get("workgroup_name"):
                    owner_changes.append(f"workgroup_name: {req.get('workgroup_name')} → {data['workgroup_name']}")
                    req["workgroup_name"] = data["workgroup_name"]
                if "workgroup_id" in data and data["workgroup_id"] != req.get("workgroup_id"):
                    owner_changes.append(f"workgroup_id: {req.get('workgroup_id')} → {data['workgroup_id']}")
                    req["workgroup_id"] = data["workgroup_id"]
                if "notes" in data and data["notes"] != req.get("notes"):
                    owner_changes.append(f"notes updated")
                    req["notes"] = data["notes"]
                
                # Add audit entry for owner changes
                if owner_changes:
                    audit_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "user": user["name"],
                        "action": "Request updated by owner",
                        "changes": owner_changes
                    }
                    req["audit_log"].append(audit_entry)
                
                req["updated_at"] = datetime.now().isoformat()
            
            if not is_admin and not is_owner:
                raise HTTPException(status_code=403, detail="Not authorized to edit this request")
            
            break
    else:
        raise HTTPException(status_code=404, detail="Request not found")
    
    save_requests(requests_list)
    return {"success": True}

@app.delete("/api/requests/{request_id}")
async def delete_request(request_id: int, request: Request):
    """Delete request - owner can delete if pending, admin can delete any"""
    user = require_auth(request)
    
    requests_list = load_requests()
    for i, req in enumerate(requests_list):
        if req["id"] == request_id:
            is_admin = user.get("role") == "admin"
            is_owner = req["requested_by"] == user["username"]
            
            if is_admin or (is_owner and req["status"] == "pending"):
                requests_list.pop(i)
                save_requests(requests_list)
                return {"success": True}
            else:
                raise HTTPException(status_code=403, detail="Not authorized to delete this request")
    
    raise HTTPException(status_code=404, detail="Request not found")

@app.get("/api/export-requests")
async def export_requests(request: Request, status: Optional[str] = None):
    """Export requests - all by default, or filtered by status"""
    user = require_admin(request)
    requests_list = load_requests()
    
    print(f"[EXPORT] Total requests loaded: {len(requests_list)}")
    print(f"[EXPORT] Status filter: {status}")
    
    # Load optimized worker data for sample worker info
    worker_data = {}
    try:
        optimized_worker_file = os.path.join(TEAMING_DIR, "Worker_Names_Stores_Missing_JobCodes_Optimized.json")
        if os.path.exists(optimized_worker_file):
            with open(optimized_worker_file, 'r', encoding='utf-8') as f:
                workers = json.load(f)
                for w in workers:
                    job_code = w.get('job_code')
                    sample = w.get('sample_worker', {})
                    worker_data[job_code] = {
                        'name': f"{sample.get('first_name', '')} {sample.get('last_name', '')}".strip(),
                        'store': sample.get('store_number', '')
                    }
        print(f"[EXPORT] Loaded worker data for {len(worker_data)} job codes")
    except Exception as e:
        print(f"[EXPORT] Warning: Could not load worker data: {e}")
    
    # If status is not provided, return all. If provided (including "approved"), filter by that status
    # For backward compatibility, if status is explicitly "approved", show only approved
    if status:
        requests_list = [r for r in requests_list if r["status"] == status]
    
    print(f"[EXPORT] After status filter: {len(requests_list)}")
    
    # Format for TMS API or manual update
    export_data = []
    for req in requests_list:
        # Parse job code into components - handle various formats
        parts = req["job_code"].split("-") if req["job_code"] else []
        
        print(f"[EXPORT] Processing job code: {req['job_code']}, parts: {parts}")
        
        job_parts = {
            "jobCode": parts[2] if len(parts) >= 3 else "",
            "deptNumber": parts[1] if len(parts) >= 3 else "",
            "divNumber": parts[0] if len(parts) >= 3 else ""
        }
        
        # Calculate impact count (banner codes + merch depts)
        banner_count = len(req.get("banner_codes", [])) if isinstance(req.get("banner_codes"), list) else 0
        merch_count = len(req.get("merch_dept_numbers", [])) if isinstance(req.get("merch_dept_numbers"), list) else 0
        impact_count = max(banner_count + merch_count, 1)  # At least 1 for the main job code
        
        # Get sample worker info
        sample_worker_info = worker_data.get(req["job_code"], {})
        sample_worker_name = sample_worker_info.get('name', '')
        sample_worker_store = sample_worker_info.get('store', '')
        
        export_data.append({
            "jobCode": job_parts["jobCode"],
            "deptNumber": job_parts["deptNumber"],
            "divNumber": job_parts["divNumber"],
            "teamName": req["team_name"],
            "teamId": int(req.get("team_id", 0)) if req.get("team_id") else "",
            "workgroupName": req["workgroup_name"],
            "workgroupId": int(req.get("workgroup_id", 0)) if req.get("workgroup_id") else "",
            "full_job_code": req["job_code"],
            "status": req.get("status", "pending"),
            "impact_count": impact_count,
            "requested_by": req["requested_by_name"],
            "requested_at": req["requested_at"],
            "sample_worker": sample_worker_name,
            "sample_worker_store": sample_worker_store
        })
    
    print(f"[EXPORT] Final export_data count: {len(export_data)}")
    return {"export_data": export_data, "count": len(export_data)}

# Admin endpoints
@app.get("/api/admin/users")
async def get_users(request: Request):
    """Get all users (admin only)"""
    user = require_admin(request)
    users = load_users()
    # Remove password hashes
    safe_users = {k: {kk: vv for kk, vv in v.items() if kk != "password_hash"} for k, v in users.items()}
    return {"users": safe_users}

@app.put("/api/admin/users/{username}")
async def update_user(username: str, request: Request):
    """Update user (admin only)"""
    admin = require_admin(request)
    data = await request.json()
    
    users = load_users()
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "approved" in data:
        users[username]["approved"] = data["approved"]
    if "role" in data:
        users[username]["role"] = data["role"]
    if "default_tab" in data:
        users[username]["default_tab"] = data["default_tab"]
    
    save_users(users)
    return {"success": True}

@app.delete("/api/admin/users/{username}")
async def delete_user(username: str, request: Request):
    """Delete user (admin only)"""
    admin = require_admin(request)
    
    if username == admin["username"]:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
    
    return {"success": True}

@app.get("/api/admin/email-queue")
async def get_email_queue(request: Request):
    """Get queued/failed emails (admin only)"""
    user = require_admin(request)
    log_file = os.path.join(DATA_DIR, "email_queue.json")
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return {"emails": json.load(f)}
    return {"emails": []}

@app.delete("/api/admin/email-queue")
async def clear_email_queue(request: Request):
    """Clear email queue (admin only)"""
    user = require_admin(request)
    log_file = os.path.join(DATA_DIR, "email_queue.json")
    if os.path.exists(log_file):
        os.remove(log_file)
    return {"success": True}

@app.post("/api/admin/test-email")
async def test_email(request: Request):
    """Send a test email (admin only)"""
    user = require_admin(request)
    data = await request.json()
    to_email = data.get("to_email", NOTIFY_EMAIL)
    
    send_email_notification(
        subject="[Test] Job Code Teaming Dashboard - Email Test",
        body=f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #0071ce;">âœ… Email Test Successful!</h2>
        <p>This is a test email from the Job Code Teaming Dashboard.</p>
        <table border="1" cellpadding="10" style="border-collapse: collapse;">
            <tr><td><strong>Sent by:</strong></td><td>{user['name']} ({user['username']})</td></tr>
            <tr><td><strong>Time:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
            <tr><td><strong>SMTP Server:</strong></td><td>{SMTP_SERVER}:{SMTP_PORT}</td></tr>
        </table>
        <p>If you received this email, the email notification system is working correctly.</p>
        </body>
        </html>
        """,
        to_email=to_email
    )
    
    return {"success": True, "message": f"Test email sent to {to_email}. Check server console for status."}

# ============================================================
# JOB CODE MASTER MANAGEMENT
# ============================================================

def load_job_codes_master():
    """
    Load job codes using Polaris as source of truth, merge with Teaming data, then Excel.
    Priority: Polaris (active job codes) -> TMS Data (team/workgroup) -> Excel (notes & gaps)
    """
    # Load Polaris data as source of truth for active job codes
    if not os.path.exists(POLARIS_DATA_FILE):
        print(f"âš ï¸ WARNING: Polaris data file not found at {POLARIS_DATA_FILE}")
        return {"job_codes": [], "last_synced": None, "source": "none"}
    
    print(f"Loading Job Codes from Polaris: {POLARIS_DATA_FILE}")
    polaris_df = pd.read_csv(POLARIS_DATA_FILE)
    polaris_df['job_code'] = polaris_df['job_code'].astype(str).str.strip()
    
    # Handle duplicates by keeping first occurrence and combining job titles
    polaris_grouped = polaris_df.groupby('job_code').agg({
        'job_nm': lambda x: ' / '.join(sorted(set(x)))  # Combine unique job names
    }).reset_index()
    
    print(f"Loaded {len(polaris_grouped)} unique job codes from Polaris (removed duplicates)")
    
    # Load user counts
    user_counts_dict = {}
    if os.path.exists(USER_COUNTS_FILE):
        print(f"Loading user counts from: {USER_COUNTS_FILE}")
        user_counts_df = pd.read_csv(USER_COUNTS_FILE)
        user_counts_df['job_code'] = user_counts_df['job_code'].astype(str).str.strip()
        user_counts_df['user_count'] = user_counts_df['user_count'].fillna(0).astype(int)
        user_counts_dict = dict(zip(user_counts_df['job_code'], user_counts_df['user_count']))
        print(f"Loaded {len(user_counts_dict)} user counts")
    else:
        print("User counts file not found")
    
    # Load TMS Data (Teaming) for team/workgroup assignments
    teaming_data = {}
    if os.path.exists(TEAMING_DATA_FILE):
        print(f"Loading team/workgroup data from Teaming: {TEAMING_DATA_FILE}")
        try:
            # Load CSV or Excel based on file extension
            if TEAMING_DATA_FILE.endswith('.csv'):
                teaming_df = pd.read_csv(TEAMING_DATA_FILE)
            else:
                teaming_df = pd.read_excel(TEAMING_DATA_FILE)
            # Combine divNumber-deptNumber-jobCode to match Polaris format
            for _, row in teaming_df.iterrows():
                div_num = str(row.get('divNumber', '')).strip()
                dept_num = str(row.get('deptNumber', '')).strip()
                job_code = str(row.get('jobCode', '')).strip()
                
                if div_num and dept_num and job_code and pd.notna(row.get('divNumber')) and pd.notna(row.get('deptNumber')) and pd.notna(row.get('jobCode')):
                    # Combine into hierarchical format: divNumber-deptNumber-jobCode
                    combined_code = f"{div_num}-{dept_num}-{job_code}"
                    # Use first team/workgroup assignment if multiple exist
                    if combined_code not in teaming_data:
                        teaming_data[combined_code] = {
                            'Team': str(row.get('teamName', '')) if pd.notna(row.get('teamName')) else '',
                            'Workgroup': str(row.get('workgroupName', '')) if pd.notna(row.get('workgroupName')) else '',
                            'Dept Number': str(row.get('deptNumber', '')) if pd.notna(row.get('deptNumber')) else '',
                            'Div Number': str(row.get('divNumber', '')) if pd.notna(row.get('divNumber')) else ''
                        }
            print(f"Loaded team/workgroup data for {len(teaming_data)} job codes from Teaming")
        except Exception as e:
            print(f"Error loading Teaming data: {e}")
    
    # Load Excel for Notes and any remaining fields
    excel_data = {}
    if os.path.exists(JOB_CODE_MASTER_EXCEL):
        print(f"Loading notes and additional fields from Excel: {JOB_CODE_MASTER_EXCEL}")
        try:
            excel_df = pd.read_excel(JOB_CODE_MASTER_EXCEL)
            # Create a dictionary keyed by SMART Job Code
            for _, row in excel_df.iterrows():
                smart_code = row.get('SMART Job Code')
                if pd.notna(smart_code):
                    excel_data[str(smart_code).strip()] = {
                        'Workday Job Code': str(row.get('Workday Job Code', '')) if pd.notna(row.get('Workday Job Code')) else '',
                        'Category': str(row.get('Category', '')) if pd.notna(row.get('Category')) else '',
                        'Workgroup': str(row.get('Workgroup', '')) if pd.notna(row.get('Workgroup')) else '',
                        'Team': str(row.get('Team', '')) if pd.notna(row.get('Team')) else '',
                        'Job Family': str(row.get('Job Family', '')) if pd.notna(row.get('Job Family')) else '',
                        'PG Level': str(row.get('PG Level', '')) if pd.notna(row.get('PG Level')) else '',
                        'Supervisor?': str(row.get('Supervisor?', '')) if pd.notna(row.get('Supervisor?')) else '',
                        'Reports to Title': str(row.get('Reports to Title', '')) if pd.notna(row.get('Reports to Title')) else '',
                        'Position Mgmt or Job Mgmt': str(row.get('Position Mgmt or Job Mgmt', '')) if pd.notna(row.get('Position Mgmt or Job Mgmt')) else '',
                        'Notes': str(row.get('Notes', '')) if pd.notna(row.get('Notes')) else '',
                    }
            print(f"Loaded additional data for {len(excel_data)} job codes from Excel")
        except Exception as e:
            print(f"Error loading Excel data: {e}")
    
    # Merge all data sources: Polaris -> Teaming -> Excel (Notes)
    job_codes = []
    for _, row in polaris_grouped.iterrows():
        job_code = str(row['job_code']).strip()
        user_count = user_counts_dict.get(job_code, 0)
        teaming_info = teaming_data.get(job_code, {})
        excel_info = excel_data.get(job_code, {})
        
        jc_data = {
            'SMART Job Code': job_code,
            'Job Title': str(row.get('job_nm', '')),
            'Workday Job Code': excel_info.get('Workday Job Code', ''),
            'Category': excel_info.get('Category', ''),
            # Use Teaming data first, fall back to Excel
            'Workgroup': teaming_info.get('Workgroup') or excel_info.get('Workgroup', ''),
            'Team': teaming_info.get('Team') or excel_info.get('Team', ''),
            'Job Family': excel_info.get('Job Family', ''),
            'PG Level': excel_info.get('PG Level', ''),
            'Supervisor?': excel_info.get('Supervisor?', ''),
            'Reports to Title': excel_info.get('Reports to Title', ''),
            'Position Mgmt or Job Mgmt': excel_info.get('Position Mgmt or Job Mgmt', ''),
            'user_count': int(user_count),
            'Notes': excel_info.get('Notes', '')
        }
        
        job_codes.append(jc_data)
    
    data = {
        "job_codes": job_codes,
        "last_synced": datetime.now().isoformat(),
        "total_count": len(job_codes),
        "source": "polaris_with_excel_notes"
    }
    
    print(f"âœ“ Loaded {len(job_codes)} job codes from Polaris with user counts")
    
    return data

def save_job_codes_master(job_codes):
    """Save job codes to JSON cache"""
    with open(JOB_CODES_MASTER_FILE, 'w') as f:
        json.dump(job_codes, f, indent=2)

def sync_job_codes_from_excel():
    """Load job codes from Excel master table and sync to JSON"""
    if not os.path.exists(JOB_CODE_MASTER_EXCEL):
        print(f"âš ï¸ WARNING: Job Code Master Excel not found at {JOB_CODE_MASTER_EXCEL}")
        return {"job_codes": [], "last_synced": None}
    
    print(f"Loading Job Code Master from: {JOB_CODE_MASTER_EXCEL}")
    df = pd.read_excel(JOB_CODE_MASTER_EXCEL)
    
    # Convert DataFrame to list of dicts, handling NaN values
    job_codes = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None}).to_dict('records')
    
    # Clean up the data - convert nan to None
    for jc in job_codes:
        for key, value in jc.items():
            if pd.isna(value):
                jc[key] = None
    
    data = {
        "job_codes": job_codes,
        "last_synced": datetime.now().isoformat(),
        "total_count": len(job_codes)
    }
    
    save_job_codes_master(data)
    print(f"âœ“ Loaded {len(job_codes)} job codes from Excel")
    return data

def load_job_code_requests():
    """Load job code change requests"""
    if os.path.exists(JOB_CODE_REQUESTS_FILE):
        with open(JOB_CODE_REQUESTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_job_code_requests(requests):
    """Save job code change requests"""
    with open(JOB_CODE_REQUESTS_FILE, 'w') as f:
        json.dump(requests, f, indent=2)

@app.get("/api/job-codes-master")
async def get_job_codes_master(request: Request):
    """Get all job codes from cache with master enrichment data - mapped to frontend field names"""
    user = get_current_user(request)
    raw_job_codes = cache.get_job_codes()
    
    # Transform field names to match frontend expectations
    job_codes = []
    for jc in raw_job_codes:
        transformed = {
            'SMART Job Code': jc.get('job_code'),  # Map job_code -> SMART Job Code
            'Job Title': jc.get('job_nm'),          # Map job_nm -> Job Title
            'Workday Code': jc.get('workday_code', ''),
            'Category': jc.get('category', ''),
            'Job Family': jc.get('job_family', ''),
            'Workgroup': '',  # Not in current schema, placeholder
            'Team': '',       # Not in current schema, placeholder
            'PG Level': jc.get('pg_level', ''),
            'Supervisor?': 'Yes' if jc.get('supervisor') else 'No',
            'Reports to Title': jc.get('reports_to', ''),
            'Position Mgmt or Job Mgmt': jc.get('position_mgmt', ''),
            'Notes': jc.get('notes', ''),
            'user_count': jc.get('user_count', 0),
            'created_by': jc.get('created_by', ''),
            'updated_at': jc.get('updated_at'),
        }
        job_codes.append(transformed)
    
    return {"job_codes": job_codes, "total": len(job_codes)}

@app.get("/api/job-codes/{job_code}")
async def get_job_code_detail(job_code: str, request: Request):
    """Get detailed information for a specific job code"""
    user = require_auth(request)
    job_code_data = cache.get_job_code(job_code)
    
    if not job_code_data:
        raise HTTPException(status_code=404, detail=f"Job code {job_code} not found")
    
    return job_code_data

@app.post("/api/job-codes-master/{job_code}")
async def update_job_code_master(job_code: str, request: Request):
    """Update job code master data (user-entered enrichment)"""
    user = require_admin(request)
    
    data = await request.json()
    data['updated_by'] = user.get('username', 'unknown')
    
    if not cache.update_master_data(job_code, data):
        raise HTTPException(status_code=400, detail=f"Failed to update job code {job_code}")
    
    # Return updated record
    updated = cache.get_job_code(job_code)
    return {"success": True, "job_code": updated}

@app.post("/api/job-codes-master/{job_code}/notes")
async def update_job_code_notes(job_code: str, request: Request):
    """Update notes for a specific job code"""
    user = require_admin(request)
    
    data = await request.json()
    notes = data.get('notes', '')
    
    if not cache.update_master_data(job_code, {'notes': notes, 'updated_by': user.get('username', 'unknown')}):
        raise HTTPException(status_code=400, detail=f"Failed to update notes for {job_code}")
    
    return {"success": True, "message": "Notes updated successfully"}

@app.get("/api/cache-status")
async def get_cache_status(request: Request):
    """Get cache synchronization status (admin only)"""
    user = require_admin(request)
    status = cache.get_sync_status()
    return status

@app.post("/api/cache/sync-now")
async def trigger_cache_sync(request: Request):
    """Manually trigger cache sync from BigQuery (admin only)"""
    user = require_admin(request)
    
    try:
        if HAS_BIGQUERY:
            polaris_data = sync_polaris_from_bigquery()
            if polaris_data is not None and cache.sync_polaris_data(polaris_data):
                return {"success": True, "message": "Cache synced successfully"}
            else:
                raise HTTPException(status_code=500, detail="Sync failed")
        else:
            raise HTTPException(status_code=503, detail="BigQuery not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync error: {str(e)}")

@app.post("/api/job-codes-master/sync")
async def sync_job_codes_master(request: Request):
    """Trigger cache sync (admin only) - legacy endpoint for compatibility"""
    return await trigger_cache_sync(request)

@app.post("/api/job-codes-master/request")
async def request_job_code_change(request: Request):
    """Submit a request to create or update a job code"""
    user = get_current_user(request)
    data = await request.json()
    
    requests = load_job_code_requests()
    
    # Get previous values if it's an update
    previous_values = None
    if data.get("type") == "update":
        job_code_data = load_job_codes_master()
        job_codes = job_code_data.get('job_codes', [])
        for jc in job_codes:
            if jc.get('SMART Job Code') == data.get('job_code'):
                previous_values = {
                    'SMART Job Code': jc.get('SMART Job Code'),
                    'Workday Job Code': jc.get('Workday Job Code'),
                    'Job Title': jc.get('Job Title'),
                    'Category': jc.get('Category'),
                    'Workgroup': jc.get('Workgroup'),
                    'Team': jc.get('Team'),
                    'Job Family': jc.get('Job Family'),
                    'PG Level': jc.get('PG Level'),
                    'Supervisor?': jc.get('Supervisor?'),
                    'Reports to Title': jc.get('Reports to Title'),
                    'Position Mgmt or Job Mgmt': jc.get('Position Mgmt or Job Mgmt')
                }
                break
    
    new_request = {
        "id": len(requests) + 1,
        "type": data.get("type", "update"),  # "create" or "update"
        "job_code": data.get("job_code"),
        "changes": data.get("changes", {}),
        "previous_values": previous_values,  # Track what's being replaced
        "reason": data.get("reason", ""),
        "requested_by": user['username'],
        "requested_by_name": user['name'],
        "status": "pending",
        "submitted": datetime.now().isoformat()
    }
    
    requests.append(new_request)
    save_job_code_requests(requests)
    
    # Send email notification to admin
    if new_request['type'] == 'create':
        subject = f"New Job Code Creation Request - {new_request.get('job_code', 'New Code')}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
        <h2>New Job Code Creation Request</h2>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr><td><strong>Requested by:</strong></td><td>{user['name']} ({user['username']})</td></tr>
            <tr><td><strong>Job Code:</strong></td><td>{new_request.get('job_code', 'TBD')}</td></tr>
            <tr><td><strong>Reason:</strong></td><td>{new_request.get('reason', 'N/A')}</td></tr>
            <tr><td><strong>Time:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
        </table>
        <p>Please review and approve in the dashboard admin panel.</p>
        </body>
        </html>
        """
    else:
        subject = f"Job Code Update Request - {new_request['job_code']}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
        <h2>Job Code Update Request</h2>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr><td><strong>Job Code:</strong></td><td>{new_request['job_code']}</td></tr>
            <tr><td><strong>Requested by:</strong></td><td>{user['name']} ({user['username']})</td></tr>
            <tr><td><strong>Reason:</strong></td><td>{new_request.get('reason', 'N/A')}</td></tr>
            <tr><td><strong>Time:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
        </table>
        <p>Please review and approve in the dashboard admin panel.</p>
        </body>
        </html>
        """
    
    send_email_notification(subject, body)
    
    return {"success": True, "request_id": new_request['id']}

@app.get("/api/job-codes-master/requests")
async def get_job_code_requests(request: Request):
    """Get all job code change requests"""
    user = get_current_user(request)
    requests = load_job_code_requests()
    
    # Filter by status if provided
    status = request.query_params.get('status')
    if status:
        requests = [r for r in requests if r['status'] == status]
    
    # Non-admins only see their own requests
    if user['role'] != 'admin':
        requests = [r for r in requests if r['requested_by'] == user['username']]
    
    return {"requests": requests}

@app.post("/api/job-codes-master/requests/{request_id}/approve")
async def approve_job_code_request(request_id: int, request: Request):
    """Approve a job code change request (admin only)"""
    user = require_admin(request)
    requests = load_job_code_requests()
    
    # Find the request
    req = next((r for r in requests if r['id'] == request_id), None)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if req['status'] != 'pending':
        raise HTTPException(status_code=400, detail="Request already processed")
    
    # Update request status
    req['status'] = 'approved'
    req['approved_by'] = user['username']
    req['approved_by_name'] = user['name']
    req['approved_date'] = datetime.now().isoformat()
    
    # Apply the changes to job codes master
    master_data = load_job_codes_master()
    job_codes = master_data.get('job_codes', [])
    
    if req['type'] == 'create':
        # Add new job code
        job_codes.append(req['changes'])
    else:
        # Update existing job code
        for jc in job_codes:
            if jc.get('SMART Job Code') == req['job_code']:
                jc.update(req['changes'])
                break
    
    master_data['job_codes'] = job_codes
    master_data['last_modified'] = datetime.now().isoformat()
    save_job_codes_master(master_data)
    
    save_job_code_requests(requests)
    
    # Send email to requester
    requester_email = req['requested_by']
    send_email_notification(
        subject=f"Job Code Request Approved - {req.get('job_code', 'New Code')}",
        body=f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
        <h2 style="color: green;">âœ“ Job Code Request Approved</h2>
        <p>Your job code request has been approved by {user['name']}.</p>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr><td><strong>Job Code:</strong></td><td>{req.get('job_code', 'New Code')}</td></tr>
            <tr><td><strong>Type:</strong></td><td>{req['type'].title()}</td></tr>
            <tr><td><strong>Approved by:</strong></td><td>{user['name']}</td></tr>
            <tr><td><strong>Approved date:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
        </table>
        </body>
        </html>
        """,
        to_email=requester_email
    )
    
    return {"success": True}

@app.post("/api/job-codes-master/requests/{request_id}/reject")
async def reject_job_code_request(request_id: int, request: Request):
    """Reject a job code change request (admin only)"""
    user = require_admin(request)
    data = await request.json()
    reason = data.get('reason', 'No reason provided')
    
    requests = load_job_code_requests()
    
    # Find the request
    req = next((r for r in requests if r['id'] == request_id), None)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if req['status'] != 'pending':
        raise HTTPException(status_code=400, detail="Request already processed")
    
    # Update request status
    req['status'] = 'rejected'
    req['rejected_by'] = user['username']
    req['rejected_by_name'] = user['name']
    req['rejected_date'] = datetime.now().isoformat()
    req['rejection_reason'] = reason
    
    # Add to rejection history for future reference
    add_rejection_to_history(
        job_code=req.get('job_code', 'Unknown'),
        request_type="job_code",
        reason=reason,
        requested_by=req.get('requested_by_name', req.get('requested_by', 'Unknown')),
        rejected_by=user['name']
    )
    
    save_job_code_requests(requests)
    
    # Send email to requester
    requester_email = req['requested_by']
    send_email_notification(
        subject=f"Job Code Request Rejected - {req.get('job_code', 'Request')}",
        body=f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
        <h2 style="color: red;">âœ— Job Code Request Rejected</h2>
        <p>Your job code request has been rejected by {user['name']}.</p>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr><td><strong>Job Code:</strong></td><td>{req.get('job_code', 'Request')}</td></tr>
            <tr><td><strong>Type:</strong></td><td>{req['type'].title()}</td></tr>
            <tr><td><strong>Rejected by:</strong></td><td>{user['name']}</td></tr>
            <tr><td><strong>Reason:</strong></td><td>{reason}</td></tr>
            <tr><td><strong>Rejected date:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
        </table>
        </body>
        </html>
        """,
        to_email=requester_email
    )
    
    return {"success": True}

@app.get("/api/rejection-history")
async def get_rejection_history(request: Request):
    """Get rejection history for all job codes"""
    user = get_current_user(request)
    history = load_rejection_history()
    return history

@app.get("/api/rejection-history/{job_code}")
async def get_rejection_history_for_job_code(job_code: str, request: Request):
    """Get rejection history for a specific job code"""
    user = get_current_user(request)
    history = load_rejection_history()
    
    return {
        "job_code": job_code,
        "job_code_rejections": history.get("job_codes", {}).get(job_code, []),
        "teaming_rejections": history.get("teaming", {}).get(job_code, [])
    }

# ============================================================
# BANNER CODES - ELM Datasource Integration
# ============================================================

@app.get("/api/banner-codes")
async def get_banner_codes():
    """
    Get banner codes from ELM datasource
    
    Returns:
        List of dicts with banner codes and descriptions
        Format suitable for dropdown population
    """
    try:
        from banner_codes_manager import get_banner_codes_api
        return get_banner_codes_api()
    except ImportError:
        # Fallback to default banner codes if manager not available
        default_banners = [
            {"code": "WAL", "desc": "Walmart Supercenter"},
            {"code": "NHM", "desc": "Neighborhood Market"},
            {"code": "SAM", "desc": "Sam's Club"},
            {"code": "HTO", "desc": "Home Town"},
            {"code": "DVT", "desc": "Discount"},
            {"code": "O3", "desc": "Aligned"},
            {"code": "RX", "desc": "Pharmacy"},
        ]
        
        dropdown_options = [f"{b['code']} - {b['desc']}" for b in default_banners]
        
        return {
            'status': 'ok',
            'banner_codes': default_banners,
            'dropdown_options': dropdown_options,
            'total': len(default_banners),
            'source': 'default'
        }

# ============================================================
# /aligned ROUTE - Main Entry Point for Aligned App
# ============================================================

@app.get("/aligned")
async def serve_aligned():
    """Serve Aligned app from /aligned path"""
    return RedirectResponse(url="/static/index.html")

# ============================================================
# STATIC FILES
# ============================================================

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

print(f"\n[STATIC FILES] Frontend path: {FRONTEND_PATH}")
print(f"[STATIC FILES] Path exists: {os.path.exists(FRONTEND_PATH)}")
if os.path.exists(FRONTEND_PATH):
    print(f"[STATIC FILES] Files in frontend: {os.listdir(FRONTEND_PATH)}")

@app.get("/Spark_Blank.png")
async def spark_blank():
    """Serve Spark favicon PNG"""
    path = os.path.join(FRONTEND_PATH, "Spark_Blank.png")
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png", headers={"Cache-Control": "public, max-age=86400"})
    from fastapi.responses import Response
    return Response(status_code=204)

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    favicon_path = os.path.join(FRONTEND_PATH, "Spark_Blank.png")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/png", headers={"Cache-Control": "public, max-age=86400"})
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"), media_type="text/html")

@app.get("/static/{full_path:path}")
async def serve_static(full_path: str):
    """Serve static files from frontend directory"""
    file_path = os.path.join(FRONTEND_PATH, full_path)
    
    # Prevent directory traversal
    file_path = os.path.normpath(file_path)
    if not file_path.startswith(os.path.normpath(FRONTEND_PATH)):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # If file exists, serve it
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # For SPA routing, serve index.html
    index_path = os.path.join(FRONTEND_PATH, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    
    raise HTTPException(status_code=404, detail="File not found")

# ============================================================
# FEEDBACK ENDPOINTS
# ============================================================

FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.json")

def load_feedback():
    """Load feedback from file"""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_feedback(feedback_list):
    """Save feedback to file"""
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(feedback_list, f, indent=2, ensure_ascii=False)

@app.post("/api/submit-feedback")
async def submit_feedback(request: Request):
    """Submit feedback from Job Codes Dashboard"""
    try:
        data = await request.json()
        
        feedback_entry = {
            "id": int(datetime.now().timestamp() * 1000),
            "timestamp": datetime.now().isoformat(),
            "category": data.get("category"),
            "rating": data.get("rating"),
            "comments": data.get("comments"),
            "page": data.get("page", "job-codes-dashboard"),
            "user": data.get("user", "Unknown")
        }
        
        # Load existing feedback
        feedback_list = load_feedback()
        feedback_list.append(feedback_entry)
        save_feedback(feedback_list)
        
        # Send email notification
        send_feedback_notification(feedback_entry)
        
        return {"success": True, "message": "Feedback submitted successfully"}
    except Exception as e:
        print(f"âŒ Error submitting feedback: {str(e)}")
        return {"success": False, "error": str(e)}

@app.get("/api/feedback")
async def get_feedback(request: Request):
    """Get all feedback (admin endpoint)"""
    try:
        # Check if user is authenticated
        user = get_current_user(request)
        if not user:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        feedback_list = load_feedback()
        return {"feedback": feedback_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def send_feedback_notification(feedback_entry):
    """Send email notification when feedback is submitted"""
    try:
        recipients = ["ATCteamsupport@walmart.com", "Kendall.rush@walmart.com"]
        
        subject = f"New Feedback: {feedback_entry['category']} - {feedback_entry['user']}"
        
        body = f"""
Job Codes Dashboard - New Feedback Submission

Category: {feedback_entry['category']}
Rating: {feedback_entry['rating']}/5
Page: {feedback_entry['page']}
User: {feedback_entry['user']}
Time: {feedback_entry['timestamp']}

Comments:
{feedback_entry['comments'] or 'No additional comments'}

---
This is an automated notification from the Job Codes Teaming Dashboard.
        """
        
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Send via Walmart SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.sendmail(FROM_EMAIL, recipients, msg.as_string())
        
        print(f"âœ… Feedback notification sent to {', '.join(recipients)}")
    except Exception as e:
        print(f"âš ï¸ Failed to send feedback notification: {str(e)}")

# ============================================================
# MAIN
# ============================================================

def check_pending_requests():
    """Check for pending access requests on startup"""
    users = load_users()
    pending = [u for u, data in users.items() if not data.get('approved', False) and u != 'admin']
    if pending:
        print(f"\nðŸ”” PENDING ACCESS REQUESTS: {len(pending)}")
        for username in pending:
            user_data = users[username]
            print(f"   â€¢ {user_data.get('name', username)} ({username}) - registered {user_data.get('registered', 'unknown')}")
        print(f"   Go to Admin tab to approve/deny these requests.\n")
    return pending

def verify_data_files():
    """Verify data files exist on startup"""
    print(f"\nVerifying data files:")
    print(f"  Teaming data: {TEAMING_DATA_FILE}")
    print(f"    Exists: {os.path.exists(TEAMING_DATA_FILE)}")
    print(f"  Polaris data: {POLARIS_DATA_FILE}")
    print(f"    Exists: {os.path.exists(POLARIS_DATA_FILE)}")
    
    if not os.path.exists(TEAMING_DATA_FILE):
        print(f"  âš ï¸ WARNING: Teaming data file not found!")
    if not os.path.exists(POLARIS_DATA_FILE):
        print(f"  âš ï¸ WARNING: Polaris data file not found!")





@app.get("/Worker_Names_Stores_Missing_JobCodes_Optimized.json")
async def get_worker_data_optimized():
    """Serve optimized worker data (count + sample) for faster tooltip loading"""
    import json as json_lib
    worker_data_dir = TEAMING_DIR
    json_file = os.path.join(worker_data_dir, "Worker_Names_Stores_Missing_JobCodes_Optimized.json")
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json_lib.load(f)
        except Exception as e:
            print(f"Error reading optimized worker JSON: {e}")
    return []

@app.get("/Worker_Names_Stores_Missing_JobCodes.json")
async def get_worker_data():
    """Serve worker data for employee tooltips"""
    import json as json_lib
    worker_data_dir = TEAMING_DIR
    json_file = os.path.join(worker_data_dir, "Worker_Names_Stores_Missing_JobCodes.json")
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json_lib.load(f)
        except Exception as e:
            print(f"Error reading worker JSON: {e}")
    csv_file = os.path.join(worker_data_dir, "Worker_Names_Stores_Missing_JobCodes.csv")
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading worker CSV: {e}")
    return []

if __name__ == "__main__":
    print(f"""
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘         JOB CODE TEAMING DASHBOARD                           â•‘
â• â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•£
â•‘  Server running at: http://localhost:{PORT}                   â•‘
â•‘  Default login: admin / admin123                             â•‘
â•‘  (Change password immediately!)                              â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    """)
    
    # Verify data files exist
    verify_data_files()
    
    # Check for pending access requests
    check_pending_requests()
    
    uvicorn.run(app, host=HOST, port=PORT)


