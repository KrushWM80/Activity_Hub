# Data Persistence & JSON Management

## Overview

The Job Code Teaming Dashboard stores all data (users, sessions, requests) in **JSON files** instead of a database. This guide covers:
- File structure and organization
- How data flows through the application
- Best practices for managing JSON data
- Backup and recovery strategies

---

## 📁 Data Files

```
dashboard/
├── data/
│   ├── users.json           # User accounts & roles
│   ├── sessions.json        # Active login sessions
│   └── update_requests.json # Job code assignment requests
├── ../TMS Data (3).xlsx     # Excel data source
└── ../polaris_job_codes.csv # CSV data source
```

### File Relationships

```
users.json
├─ username → password, role, email
│
└─ Referenced by:
   ├── sessions.json (who's logged in)
   └── update_requests.json (who submitted request)

sessions.json
├─ session_token → username, role, login_time, expires
│
└─ Used for:
   ├── API authentication
   └── Checking permissions

update_requests.json
├─ request_id → job_code, team_name, submitted_by, status
│
└─ Workflow:
   ├── User submits → status="pending"
   └── Admin approves → status="approved"
```

---

## 📝 File Formats

### 1. users.json

```json
{
  "admin": {
    "password": "admin123",
    "role": "admin",
    "email": "admin@example.com",
    "created_at": "2025-01-21T00:00:00Z"
  },
  "john_smith": {
    "password": "password123",
    "role": "user",
    "email": "john.smith@company.com",
    "created_at": "2025-01-21T10:30:00Z"
  },
  "manager_jane": {
    "password": "secure_password",
    "role": "admin",
    "email": "jane.manager@company.com",
    "created_at": "2025-01-15T08:00:00Z"
  }
}
```

**Fields:**
- `password` - User's password (⚠️ currently plain text)
- `role` - "admin" or "user" (determines permissions)
- `email` - For notifications
- `created_at` - Optional, for audit trail

---

### 2. sessions.json

```json
{
  "abc123xyz_session_token_here": {
    "username": "john_smith",
    "role": "user",
    "email": "john.smith@company.com",
    "login_time": "2025-01-21T10:30:00Z",
    "expires": "2025-01-21T18:30:00Z"
  },
  "def456uvw_another_token": {
    "username": "admin",
    "role": "admin",
    "email": "admin@example.com",
    "login_time": "2025-01-21T08:00:00Z",
    "expires": "2025-01-21T16:00:00Z"
  }
}
```

**Fields:**
- `username` - Who is logged in
- `role` - Their permissions (cached from users.json)
- `login_time` - When they logged in
- `expires` - When token becomes invalid

**Lifecycle:**
1. Created when user logs in
2. Checked on every API request
3. Deleted when token expires or user logs out
4. Old tokens cleaned up periodically

---

### 3. update_requests.json

```json
{
  "req_20250121_103000": {
    "id": "req_20250121_103000",
    "job_code": "1234",
    "team_name": "Team A",
    "submitted_by": "john_smith",
    "submitted_at": "2025-01-21T10:30:00Z",
    "status": "pending",
    "approved_by": null,
    "approved_at": null
  },
  "req_20250121_110500": {
    "id": "req_20250121_110500",
    "job_code": "5678",
    "team_name": "Team B",
    "submitted_by": "jane_user",
    "submitted_at": "2025-01-21T11:05:00Z",
    "status": "approved",
    "approved_by": "admin",
    "approved_at": "2025-01-21T11:15:00Z"
  }
}
```

**Fields:**
- `id` - Unique request identifier
- `job_code` - Job code being assigned
- `team_name` - Target team
- `submitted_by` - User who made request
- `submitted_at` - Timestamp of submission
- `status` - "pending" or "approved" or "rejected"
- `approved_by` - Admin who approved
- `approved_at` - When it was approved

**Workflow:**
```
User submits request
  ↓
status = "pending", approved_by = null, approved_at = null
  ↓
Admin reviews
  ↓
Admin clicks "Approve"
  ↓
status = "approved", approved_by = "admin", approved_at = "timestamp"
  ↓
Ready for export to TMS
```

---

## 💾 Python Functions for Data Management

### Load JSON

```python
import json
from pathlib import Path

def load_json(filepath):
    """Load JSON file, return empty dict if missing"""
    path = Path(filepath)
    
    if not path.exists():
        print(f"Warning: {filepath} not found, returning empty dict")
        return {}
    
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {filepath} is invalid JSON")
        return {}
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return {}
```

### Save JSON

```python
def save_json(filepath, data, pretty=True):
    """Save data to JSON file with optional formatting"""
    path = Path(filepath)
    
    # Create directory if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(path, 'w') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f)
        
        print(f"✓ Saved {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error saving {filepath}: {e}")
        return False
```

### Update with Lock (Thread-Safe)

```python
import fcntl
import json
from pathlib import Path

def update_json_safe(filepath, update_func):
    """
    Safely update JSON file
    - Locks file to prevent concurrent writes
    - update_func receives current data, returns modified data
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(path, 'a+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            
            try:
                # Read current data
                f.seek(0)
                content = f.read()
                data = json.loads(content) if content else {}
                
                # Update
                updated_data = update_func(data)
                
                # Write back
                f.seek(0)
                f.truncate()
                json.dump(updated_data, f, indent=2)
                
                return True
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

# Usage
def approve_request_safe(request_id, admin_username):
    """Safely approve a request"""
    def updater(requests):
        if request_id in requests:
            requests[request_id]["status"] = "approved"
            requests[request_id]["approved_by"] = admin_username
            requests[request_id]["approved_at"] = datetime.now().isoformat()
        return requests
    
    return update_json_safe("data/update_requests.json", updater)
```

### Bulk Operations

```python
def get_all_pending_requests():
    """Get all requests with status 'pending'"""
    requests = load_json("data/update_requests.json")
    return {
        req_id: req for req_id, req in requests.items()
        if req.get("status") == "pending"
    }

def get_user_requests(username):
    """Get all requests submitted by a user"""
    requests = load_json("data/update_requests.json")
    return {
        req_id: req for req_id, req in requests.items()
        if req.get("submitted_by") == username
    }

def count_approvals_by_admin(admin_username):
    """Count how many requests an admin has approved"""
    requests = load_json("data/update_requests.json")
    return sum(
        1 for req in requests.values()
        if req.get("approved_by") == admin_username
    )
```

---

## 🔄 Data Flow Example: Complete Request Workflow

```python
from datetime import datetime

# 1. USER SUBMITS REQUEST
# Frontend sends: POST /api/requests with job_code, team_name
@app.post("/api/requests")
async def submit_request(data: dict, session: dict):
    """User submits a request"""
    
    # Create request
    request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    new_request = {
        "id": request_id,
        "job_code": data["job_code"],
        "team_name": data["team_name"],
        "submitted_by": session["username"],  # From current session
        "submitted_at": datetime.now().isoformat(),
        "status": "pending",
        "approved_by": None,
        "approved_at": None
    }
    
    # Save to update_requests.json
    requests_data = load_json("data/update_requests.json")
    requests_data[request_id] = new_request
    save_json("data/update_requests.json", requests_data)
    
    return {"success": True, "request_id": request_id}

# 2. ADMIN VIEWS PENDING REQUESTS
# Frontend sends: GET /api/requests?status=pending
@app.get("/api/requests")
async def list_requests(status: str = None, session: dict = None):
    """Get requests (filter by status)"""
    
    requests_data = load_json("data/update_requests.json")
    
    if status:
        requests_data = {
            req_id: req for req_id, req in requests_data.items()
            if req["status"] == status
        }
    
    return requests_data

# 3. ADMIN APPROVES REQUEST
# Frontend sends: POST /api/requests/{request_id}/approve
@app.post("/api/requests/{request_id}/approve")
async def approve_request(request_id: str, session: dict):
    """Admin approves a request"""
    
    # Check permission
    if session["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can approve")
    
    # Load and update
    requests_data = load_json("data/update_requests.json")
    
    if request_id not in requests_data:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request = requests_data[request_id]
    request["status"] = "approved"
    request["approved_by"] = session["username"]
    request["approved_at"] = datetime.now().isoformat()
    
    # Save updated request
    save_json("data/update_requests.json", requests_data)
    
    # Optional: Send email to user (see EMAIL_NOTIFICATIONS.md)
    
    return {
        "success": True,
        "message": f"Request {request_id} approved",
        "request": request
    }

# 4. ADMIN EXPORTS FOR TMS
# Frontend sends: GET /api/export/approved
@app.get("/api/export/approved")
async def export_approved_requests(session: dict):
    """Export approved requests for TMS update"""
    
    if session["role"] != "admin":
        raise HTTPException(status_code=403)
    
    requests_data = load_json("data/update_requests.json")
    
    approved = [
        req for req in requests_data.values()
        if req["status"] == "approved"
    ]
    
    # Format for TMS API
    export_data = [
        {
            "jobCode": req["job_code"],
            "teamName": req["team_name"],
            "approvedBy": req["approved_by"],
            "approvedAt": req["approved_at"]
        }
        for req in approved
    ]
    
    # Return as JSON download
    return JSONResponse(
        content=export_data,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=tms_updates.json"}
    )
```

---

## 🛡️ Data Integrity & Backup

### Backup Strategy

```powershell
# PowerShell backup script
# Save as: backup-dashboard-data.ps1

$backupDir = "C:\Backups\Dashboard"
$dataDir = "C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\data"

# Create backup directory if needed
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Create timestamped backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = Join-Path $backupDir "backup_$timestamp"

# Copy all data files
Copy-Item -Path $dataDir -Destination $backupPath -Recurse -Force

Write-Host "✓ Backup created: $backupPath" -ForegroundColor Green

# Optional: Keep only last 10 backups
$backups = Get-ChildItem $backupDir | Sort-Object CreationTime -Descending
if ($backups.Count -gt 10) {
    $backups | Select-Object -Last ($backups.Count - 10) | Remove-Item -Recurse -Force
    Write-Host "✓ Old backups cleaned up" -ForegroundColor Green
}
```

### Schedule Automatic Backups

```powershell
# Create scheduled task in Windows Task Scheduler

$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "C:\path\to\backup-dashboard-data.ps1"

$trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM

Register-ScheduledTask -Action $action -Trigger $trigger `
    -TaskName "Dashboard Daily Backup" `
    -Description "Backup Job Code Dashboard data daily"
```

### Verify Data Integrity

```python
def validate_json_structure():
    """Check that all JSON files have correct structure"""
    
    # Check users.json
    users = load_json("data/users.json")
    for username, user_data in users.items():
        assert "password" in user_data, f"Missing password for {username}"
        assert "role" in user_data, f"Missing role for {username}"
        assert user_data["role"] in ["admin", "user"], f"Invalid role for {username}"
    
    # Check sessions.json
    sessions = load_json("data/sessions.json")
    for token, session_data in sessions.items():
        assert "username" in session_data, f"Missing username in session {token}"
        assert "role" in session_data, f"Missing role in session {token}"
        assert "expires" in session_data, f"Missing expires in session {token}"
    
    # Check update_requests.json
    requests = load_json("data/update_requests.json")
    for request_id, request_data in requests.items():
        assert "id" in request_data, f"Missing id in request {request_id}"
        assert "status" in request_data, f"Missing status in request {request_id}"
        assert request_data["status"] in ["pending", "approved", "rejected"]
    
    print("✓ All data structures valid")
```

---

## ⚠️ Common Issues & Solutions

### File Locked/Cannot Write

```python
# Problem: "File is being used by another process"

# Solution: Use file locking
import time

def save_json_with_retry(filepath, data, max_retries=3):
    """Try multiple times if file is locked"""
    for attempt in range(max_retries):
        try:
            save_json(filepath, data)
            return True
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(0.1 * (attempt + 1))  # Wait longer each time
            else:
                raise
    return False
```

### Corrupted JSON File

```python
def recover_from_backup(filepath, backup_dir):
    """Restore file from most recent backup"""
    
    import shutil
    from datetime import datetime
    
    # Find most recent backup
    backups = sorted(
        Path(backup_dir).glob("*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if not backups:
        print("No backups found!")
        return False
    
    latest_backup = backups[0] / Path(filepath).name
    
    if not latest_backup.exists():
        print(f"Backup not found: {latest_backup}")
        return False
    
    # Copy from backup
    shutil.copy(latest_backup, filepath)
    print(f"✓ Restored from {latest_backup}")
    return True
```

### Session Expired While Working

```python
# Frontend JavaScript to handle expired session

async function makeAPICall(endpoint, method = "GET") {
    const token = localStorage.getItem("sessionToken");
    
    const response = await fetch(endpoint, {
        method,
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    
    if (response.status === 401) {
        // Token expired
        localStorage.removeItem("sessionToken");
        
        // Warn user
        alert("Your session has expired. Please log in again.");
        window.location.href = "/login.html";
        
        return null;
    }
    
    return response.json();
}
```

---

## 🎓 Key Learnings

✅ **JSON is simple** - No database setup, just files  
✅ **File locking matters** - Prevent corruption from concurrent writes  
✅ **Backup regularly** - Automate daily backups  
✅ **Validate on load** - Catch corrupted data early  
✅ **Sessions should expire** - Don't let old sessions linger  
✅ **Keep data normalized** - Avoid duplicate information  

---

## 📚 Related Files

- Source: `C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\data`
- Backend: `backend/main.py`
- See also: [USER_AUTHENTICATION.md](./USER_AUTHENTICATION.md) - Session structure
- See also: [WORKFLOW_PATTERNS.md](./WORKFLOW_PATTERNS.md) - Request data flow
