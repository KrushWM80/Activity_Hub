# Job Code Teaming Dashboard - Knowledge Base

## Project Overview

The Job Code Teaming Dashboard is a **FastAPI web application** that manages job code assignments to teams. It runs locally and is accessible to team members on the Walmart VPN.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                        │
│              HTML/CSS/JavaScript (Static)                   │
│             index.html in frontend/ folder                  │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP Requests
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                  FastAPI Backend Server                      │
│                     Port: 8080                               │
│                   main.py (1584 lines)                      │
│                                                              │
│  ├─ Authentication (HTTPBasic)                             │
│  ├─ User Management (users.json)                           │
│  ├─ Request Processing (update_requests.json)              │
│  ├─ Session Management (sessions.json)                     │
│  ├─ Job Code Data (job_codes_master.json)                  │
│  ├─ Email Notifications (SMTP)                             │
│  └─ Static File Serving                                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   └─ Reads/Writes
                   │
           ┌───────▼────────┐
           │  Data Files    │
           │   (data/)      │
           ├─ users.json    │
           ├─ sessions.json │
           ├─ update_requests.json
           ├─ job_code_requests.json
           ├─ job_codes_master.json
           ├─ email_queue.json
           ├─ email_config.json
           └─ rejection_history.json
```

---

## Network Access & URL Setup

### Why the Hostname-Based URL?

Your machine has a **permanent network hostname** that resolves on the Walmart VPN:

```
LEUS62315243171.homeoffice.Wal-Mart.com
```

This is **better than IP addresses** because:
- ✅ **Never changes** - Even if your IP address changes, the hostname stays the same
- ✅ **Team-shareable** - Colleagues on VPN can use the same URL
- ✅ **Professional** - Works reliably over long periods

### Access Methods

| User | URL | Details |
|------|-----|---------|
| You (locally) | `http://localhost:8080/static/index.html` | Dev/testing |
| You (from another machine) | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080/static/index.html` | Over VPN |
| Team members | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080/static/index.html` | Over VPN from their computers |

**Related Documentation:** See [Local Hosting Guide](../../Spark-Playground/General%20Setup/Local%20Hosting/NETWORK_SHARING.md) for detailed network setup instructions.

### Prerequisites for Team Access

1. **Server binding**: FastAPI configured to bind to `0.0.0.0` (not localhost)
   - ✅ Already configured in main.py: `HOST = "0.0.0.0"`

2. **Firewall rules**: Port 8080 must allow inbound traffic
   - PowerShell command (run as Admin):
   ```powershell
   New-NetFirewallRule -DisplayName "JobCode Dashboard 8080" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
   ```

3. **Server running**: Dashboard server must be active
   - Run: `python backend\main.py` or use `start_server.bat`

---

## Data Flow

### 1. **Initialization**
```
Startup → Load TMS Data (3).xlsx → Load polaris_job_codes.csv 
→ Merge into job_codes_master.json → Web server ready
```

### 2. **User Submits Request**
```
Browser → Select Job Code + Team → POST /update-request 
→ Stored in update_requests.json → Admin notified via email
```

### 3. **Admin Approves**
```
Admin approval → DELETE job code from "Missing" list → 
Export ready for TMS API
```

### 4. **Data Sources**
| File | Purpose | Location | Updated By |
|------|---------|----------|------------|
| `TMS Data (3).xlsx` | Current teaming assignments | Parent folder | TMS system |
| `polaris_job_codes.csv` | Job codes in use (from BigQuery) | Parent folder | BigQuery query |
| `polaris_user_counts.csv` | User counts per job code | Parent folder | BigQuery query |
| `job_codes_master.json` | Combined, ready-to-use data | data/ folder | Dashboard (on startup) |

---

## Backend Components

### Core Modules

1. **Authentication** (`main.py` - lines 1-200)
   - HTTPBasic authentication
   - Password hashing with SHA256
   - Session token management

2. **User Management** (`main.py` - lines 201-400)
   - Load/save users.json
   - Role-based access control (Admin/User)
   - User registration workflow

3. **Job Code Processing** (`main.py` - lines 400-800)
   - Load TMS data (Excel)
   - Load Polaris data (CSV)
   - Merge and deduplicate
   - Generate master job code list

4. **Request Handling** (`main.py` - lines 800-1200)
   - Process update requests
   - Admin approval/rejection
   - Export functionality
   - Email notifications

5. **Session Management** (`main.py` - lines 1200+)
   - Track active sessions
   - Timeout handling
   - User state management

---

## Data Processing Scripts

Located in parent folder (`../`):

### `job_code_comparison.py`
- **Purpose**: Compare HR data vs Teaming data
- **Input**: TMS Data (3).xlsx + HR CSV
- **Output**: Missing_JobCodes_From_Teaming.csv, Teaming_JobCodes_Not_In_HR.csv
- **Run**: `python job_code_comparison.py`

### `polaris_comparison.py`
- **Purpose**: Compare Polaris (BigQuery) vs Teaming data
- **Input**: polaris_job_codes.csv + TMS Data (3).xlsx
- **Output**: Missing_From_Teaming_POLARIS.csv, Teaming_Not_In_Polaris.csv
- **Run**: `python polaris_comparison.py`

### `get_user_ids.py`, `get_user_details_bigquery.py`, `get_worker_names_stores.py`
- **Purpose**: Extract data from BigQuery and HR systems
- **Used to collect**: Job codes, user counts, department details

---

## User Roles & Permissions

### Admin
```
✅ View all job codes (entire list)
✅ View all user requests (all submissions)
✅ Approve/reject user registrations
✅ Approve/reject teaming update requests
✅ Export approved requests (for TMS upload)
✅ Change user roles
✅ View analytics/reports
```

### User
```
✅ View all job codes
✅ Submit teaming update requests
✅ View own request history
❌ Approve requests
❌ Change user roles
❌ Export data
```

---

## Workflow Example

### Scenario: User Requests a Job Code to be Assigned a Team

1. **User Login**
   - Username: `jsmith`
   - Password: (their password)

2. **View Job Codes**
   - Dashboard loads: `GET /job-codes`
   - Shows all job codes with "Assigned" or "Missing" status

3. **Find Missing Job Code**
   - Example: Job Code `1-993-1026` (Status: Missing)
   - User selects it + chooses Team: "GM - Guest Services"

4. **Submit Request**
   - `POST /update-request` with:
     ```json
     {
       "jobCode": "1-993-1026",
       "teamId": "GM-001",
       "teamName": "GM - Guest Services",
       "reason": "Store #4012 needs this team assignment"
     }
     ```

5. **Backend Processes**
   - Stores in `update_requests.json`
   - Sends email to `ATCTEAMSUPPORT@walmart.com`

6. **Admin Review**
   - Admin logs in, sees request in "Approval Queue"
   - Reviews and clicks "Approve"
   - Request moves to "Approved" status

7. **Export for TMS**
   - Admin clicks "Export Approved Requests"
   - Gets CSV with fields ready for TMS API:
     - jobCode, deptNumber, divNumber, teamName, teamId, workgroupName, workgroupId

---

## Configuration

### Network
```python
HOST = "0.0.0.0"  # Listen on all interfaces (enables team access)
PORT = 8080
```

### Email
```python
NOTIFY_EMAIL = "ATCTEAMSUPPORT@walmart.com"
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"  # Walmart internal
SMTP_PORT = 25
FROM_EMAIL = "JobCodeTeamingDashboard@walmart.com"
```

### File Paths
```python
BASE_DIR = dashboard folder
TEAMING_DIR = parent folder (../Teaming/)
DATA_DIR = dashboard/data/
JOB_CODES_DIR = ../../Job Codes/
```

---

## Troubleshooting

### URL Access Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Can't reach from team machine | Firewall rule missing | Add firewall rule (see above) |
| "Connection refused" | Server not running | `python backend\main.py` |
| Hostname doesn't resolve | Not on VPN | Connect to Walmart VPN first |
| 404 on /static/index.html | Frontend files moved | Check frontend/ folder exists |

### Data Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| No job codes loading | TMS Data file missing | Place `TMS Data (3).xlsx` in parent folder |
| "Job codes out of sync" | Polaris CSV outdated | Re-run `get_user_ids.py` or BigQuery query |
| Can't approve requests | users.json permissions | Check file is readable/writable |

---

## Security Considerations

⚠️ **Default Credentials**
- Default admin: `admin` / `admin123`
- **MUST change on first login**

🔐 **Password Storage**
- Stored as SHA256 hash
- Never stored in plaintext

🛡️ **Network Access**
- Only works on Walmart VPN
- HTTPBasic (username/password)
- No additional encryption added (rely on VPN security)

---

## Related References

- [Network Sharing Guide](../../Spark-Playground/General%20Setup/Local%20Hosting/NETWORK_SHARING.md) - How to share dashboards with team
- [Local Hosting Guide](../../Spark-Playground/General%20Setup/Local%20Hosting/README.md) - When to use continuous server vs scheduled tasks
- Main Dashboard README (README.md) - Quick start guide

---

## Key Takeaways

✅ **Hostname-based URLs** are stable and team-shareable on VPN
✅ **FastAPI backend** handles all business logic
✅ **JSON data files** store users, requests, and session data
✅ **Email notifications** keep admins updated on new requests
✅ **Multiple data sources** (TMS, Polaris, HR) are merged and reconciled
✅ **Firewall rule required** for team access from other machines
