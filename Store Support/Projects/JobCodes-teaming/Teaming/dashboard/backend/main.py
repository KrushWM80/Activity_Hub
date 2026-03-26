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
TEAMING_DATA_FILE = os.path.join(TEAMING_DIR, "TMS Data (3).xlsx")
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
    title="Job Code Teaming Dashboard",
    description="Manage job codes and teaming assignments",
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
    has_team_data = False
    
    if os.path.exists(TEAMING_DATA_FILE):
        try:
            print(f"Loading Teaming data from: {TEAMING_DATA_FILE}")
            teaming_df = pd.read_excel(TEAMING_DATA_FILE)
            
            # Check which columns are available
            available_cols = list(teaming_df.columns)
            print(f"Available Teaming columns: {available_cols}")
            
            # Create composite key from available columns
            teaming_df['composite_job_code'] = (
                teaming_df['divNumber'].fillna(0).astype(int).astype(str) + '-' +
                teaming_df['deptNumber'].fillna(0).astype(int).astype(str) + '-' +
                teaming_df['jobCode'].fillna(0).astype(int).astype(str)
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
            print(f"⚠️  WARNING: Cannot load Excel teaming data: {e}")
            print("   Proceeding without teaming data (openpyxl not installed)")
            teaming_df = pd.DataFrame()  # Empty dataframe
        except Exception as e:
            print(f"⚠️  WARNING: Error loading teaming data: {e}")
            teaming_df = pd.DataFrame()  # Empty dataframe
    else:
        print(f"Teaming data file not found at {TEAMING_DATA_FILE}, using Polaris data only")
        teaming_df = pd.DataFrame()  # Empty dataframe
    
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
    if not os.path.exists(TEAMING_DATA_FILE):
        raise FileNotFoundError(f"Teaming data file not found: {TEAMING_DATA_FILE}")
    teaming_df = pd.read_excel(TEAMING_DATA_FILE)
    
    # Check if team columns exist
    team_cols = ['teamName', 'teamId', 'workgroupName', 'workgroupId']
    available_cols = [col for col in team_cols if col in teaming_df.columns]
    
    if not available_cols:
        # No team data available - return empty list
        print(f"No team columns found in teaming data. Available: {list(teaming_df.columns)}")
        return []
    
    # Only use available columns
    teams = teaming_df[available_cols].drop_duplicates()
    
    # Convert to JSON-safe format
    result = []
    for _, row in teams.iterrows():
        team_entry = {}
        for col in available_cols:
            if col == 'teamId' or col == 'workgroupId':
                team_entry[col] = to_json_safe(row[col])
            else:
                team_entry[col] = str(row[col]) if pd.notna(row[col]) else ""
        result.append(team_entry)
    
    return result

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
            print(f"⚠️ Email sending failed (outside Walmart network?): {e}")
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
    """Get all job codes with teaming status"""
    user = require_auth(request)
    
    merged_df, _ = load_job_code_data()
    
    result = []
    for _, row in merged_df.iterrows():
        teams = row["teamName"] if isinstance(row["teamName"], list) else []
        team_ids = row["teamId"] if isinstance(row["teamId"], list) else []
        workgroups = row["workgroupName"] if isinstance(row["workgroupName"], list) else []
        
        result.append({
            "job_code": str(row["job_code"]) if pd.notna(row["job_code"]) else "",
            "job_name": str(row["job_nm"]) if pd.notna(row["job_nm"]) else "",
            "job_title": str(row["job_title"]) if pd.notna(row["job_title"]) else "",
            "status": str(row["status"]) if pd.notna(row["status"]) else "Unknown",
            "teams": [str(t) for t in teams if pd.notna(t)],
            "team_ids": [to_json_safe(t) for t in team_ids if pd.notna(t)],
            "workgroups": [str(w) for w in workgroups if pd.notna(w)],
            "division": to_json_safe(row.get("divNumber")),
            "department": to_json_safe(row.get("deptNumber")),
            "user_count": to_json_safe(row.get("user_count", 0)),
        })
    
    return {"job_codes": result, "total": len(result)}

@app.get("/api/teams")
async def get_teams(request: Request):
    """Get available teams"""
    user = require_auth(request)
    teams = get_team_options()
    return {"teams": teams}

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
        client = bigquery.Client()
        
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
        results = client.query(query).result()
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
    user = require_auth(request)
    requests_list = load_requests()
    
    # Non-admins can only see their own requests
    if user["role"] != "admin":
        requests_list = [r for r in requests_list if r["requested_by"] == user["username"]]
    
    if status:
        requests_list = [r for r in requests_list if r["status"] == status]
    
    return {"requests": requests_list}

@app.put("/api/requests/{request_id}")
async def update_request(request_id: int, request: Request):
    """Update request - admin can change status, owner can edit details"""
    user = require_auth(request)
    data = await request.json()
    
    requests_list = load_requests()
    for req in requests_list:
        if req["id"] == request_id:
            is_admin = user.get("role") == "admin"
            is_owner = req["requested_by"] == user["username"]
            
            # Admin can change status
            if is_admin and "status" in data:
                req["status"] = data["status"]
                req["admin_notes"] = data.get("admin_notes", req.get("admin_notes", ""))
                req["processed_by"] = user["username"]
                req["processed_at"] = datetime.now().isoformat()
                
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
            
            # Owner can edit team/notes if still pending
            if is_owner and req["status"] == "pending":
                if "team_name" in data:
                    req["team_name"] = data["team_name"]
                if "team_id" in data:
                    req["team_id"] = data["team_id"]
                if "workgroup_name" in data:
                    req["workgroup_name"] = data["workgroup_name"]
                if "workgroup_id" in data:
                    req["workgroup_id"] = data["workgroup_id"]
                if "notes" in data:
                    req["notes"] = data["notes"]
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
async def export_requests(request: Request, status: Optional[str] = "approved"):
    """Export approved requests for TMS update"""
    user = require_admin(request)
    requests_list = load_requests()
    
    if status:
        requests_list = [r for r in requests_list if r["status"] == status]
    
    # Format for TMS API or manual update
    export_data = []
    for req in requests_list:
        # Parse job code into components
        parts = req["job_code"].split("-")
        if len(parts) == 3:
            export_data.append({
                "jobCode": parts[2],
                "deptNumber": parts[1],
                "divNumber": parts[0],
                "teamName": req["team_name"],
                "teamId": req["team_id"],
                "workgroupName": req["workgroup_name"],
                "workgroupId": req["workgroup_id"],
                "full_job_code": req["job_code"],
                "requested_by": req["requested_by_name"],
                "requested_at": req["requested_at"]
            })
    
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
        <h2 style="color: #0071ce;">✅ Email Test Successful!</h2>
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
        print(f"⚠️ WARNING: Polaris data file not found at {POLARIS_DATA_FILE}")
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
            teaming_df = pd.read_excel(TEAMING_DATA_FILE)
            # Group by jobCode and aggregate team/workgroup info
            for _, row in teaming_df.iterrows():
                job_code = str(row.get('jobCode', '')).strip()
                if job_code and pd.notna(job_code):
                    # Use first team/workgroup assignment if multiple exist
                    if job_code not in teaming_data:
                        teaming_data[job_code] = {
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
    
    print(f"✓ Loaded {len(job_codes)} job codes from Polaris with user counts")
    
    return data

def save_job_codes_master(job_codes):
    """Save job codes to JSON cache"""
    with open(JOB_CODES_MASTER_FILE, 'w') as f:
        json.dump(job_codes, f, indent=2)

def sync_job_codes_from_excel():
    """Load job codes from Excel master table and sync to JSON"""
    if not os.path.exists(JOB_CODE_MASTER_EXCEL):
        print(f"⚠️ WARNING: Job Code Master Excel not found at {JOB_CODE_MASTER_EXCEL}")
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
    print(f"✓ Loaded {len(job_codes)} job codes from Excel")
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
    """Get all job codes from Polaris (source of truth) with user counts"""
    user = get_current_user(request)
    # Always load fresh from Polaris
    data = load_job_codes_master()
    return data

@app.post("/api/job-codes-master/{job_code}/notes")
async def update_job_code_notes(job_code: str, request: Request):
    """Update notes for a specific job code (admin only)"""
    user = require_admin(request)
    data = await request.json()
    notes = data.get('notes', '')
    
    # Load Excel to update notes
    if not os.path.exists(JOB_CODE_MASTER_EXCEL):
        raise HTTPException(status_code=404, detail="Excel file not found")
    
    df = pd.read_excel(JOB_CODE_MASTER_EXCEL)
    
    # Find and update the job code
    mask = df['SMART Job Code'].astype(str).str.strip() == job_code.strip()
    if mask.any():
        df.loc[mask, 'Notes'] = notes
    else:
        # Add new row if not exists
        new_row = {'SMART Job Code': job_code, 'Notes': notes}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Save back to Excel
    df.to_excel(JOB_CODE_MASTER_EXCEL, index=False)
    
    return {"success": True, "message": "Notes updated successfully"}

@app.post("/api/job-codes-master/sync")
async def sync_job_codes_master(request: Request):
    """Sync job codes from Excel (admin only)"""
    user = require_admin(request)
    data = sync_job_codes_from_excel()
    return {"success": True, "data": data}

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
        <h2 style="color: green;">✓ Job Code Request Approved</h2>
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
        <h2 style="color: red;">✗ Job Code Request Rejected</h2>
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
# STATIC FILES
# ============================================================

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

print(f"\n[STATIC FILES] Frontend path: {FRONTEND_PATH}")
print(f"[STATIC FILES] Path exists: {os.path.exists(FRONTEND_PATH)}")
if os.path.exists(FRONTEND_PATH):
    print(f"[STATIC FILES] Files in frontend: {os.listdir(FRONTEND_PATH)}")

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    favicon_path = os.path.join(FRONTEND_PATH, "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/x-icon")
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
# MAIN
# ============================================================

def check_pending_requests():
    """Check for pending access requests on startup"""
    users = load_users()
    pending = [u for u, data in users.items() if not data.get('approved', False) and u != 'admin']
    if pending:
        print(f"\n🔔 PENDING ACCESS REQUESTS: {len(pending)}")
        for username in pending:
            user_data = users[username]
            print(f"   • {user_data.get('name', username)} ({username}) - registered {user_data.get('registered', 'unknown')}")
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
        print(f"  ⚠️ WARNING: Teaming data file not found!")
    if not os.path.exists(POLARIS_DATA_FILE):
        print(f"  ⚠️ WARNING: Polaris data file not found!")

if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         JOB CODE TEAMING DASHBOARD                           ║
╠══════════════════════════════════════════════════════════════╣
║  Server running at: http://localhost:{PORT}                   ║
║  Default login: admin / admin123                             ║
║  (Change password immediately!)                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verify data files exist
    verify_data_files()
    
    # Check for pending access requests
    check_pending_requests()
    
    uvicorn.run(app, host=HOST, port=PORT)
