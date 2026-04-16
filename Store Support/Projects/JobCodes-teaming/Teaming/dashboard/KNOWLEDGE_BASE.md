# Job Code Teaming Dashboard - Knowledge Base

## âš ï¸ Automation & Recovery (April 2, 2026)

### Scheduled Tasks

| Task Name | Schedule | Purpose |
|-----------|----------|--------|
| `Activity_Hub_JobCodes_AutoStart` | On logon | Starts `start_jobcodes_server_24_7.bat` â†’ `main.py` on port 8080 |

### Bat Files (`Automation/`)
- `start_jobcodes_server_24_7.bat` â€” Port-kill block + restart loop. Primary crash recovery (5-7 sec downtime)
- Log: `Automation/jobcodes_server.log`

### Recovery Layers
1. **Bat restart loop** â€” primary (5-7 sec recovery on crash)
2. **Continuous monitor** (`continuous_monitor.ps1`) â€” checks all 7 services every 5 min; only launches new bat if bat process is not already running

### Known Issue (ongoing)
Job Codes exits with code 1 immediately on startup â€” crash loop. The bat keeps retrying every 5 seconds. Check `Automation/jobcodes_server.log` for the Python traceback.

### âš ï¸ NEVER use `Stop-Process -Name python`
This kills ALL Python processes on the machine â€” all 7 services go down.

**Safe way to restart only Job Codes (port 8080):**
```powershell
$p = (netstat -ano | Select-String ":8080.*LISTENING" | ForEach-Object { ($_ -split "\s+")[-1] }) | Select-Object -First 1
if ($p) { taskkill /F /PID $p }
# Bat loop restarts automatically within 5-7 seconds
```

### Adding/Changing This Service
If the port, entry point, or bat file changes, update ALL of:
1. `Automation/start_jobcodes_server_24_7.bat`
2. `Automation/register_tasks_cmd.bat`
3. `continuous_monitor.ps1` services array
4. `MONITOR_AND_REPORT.ps1` services list
5. `Documentation/KNOWLEDGE_HUB.md` Active Services table
6. This file

---

## Project Overview

The Job Code Teaming Dashboard is a **FastAPI web application** that manages job code assignments to teams. It runs locally and is accessible to team members on the Walmart VPN.

---

## Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Frontend (Browser)                        â”‚
â”‚              HTML/CSS/JavaScript (Static)                   â”‚
â”‚             index.html in frontend/ folder                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                   â”‚ HTTP Requests
                   â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                  FastAPI Backend Server                      â”‚
â”‚                     Port: 8080                               â”‚
â”‚                   main.py (1700+ lines)                     â”‚
â”‚                                                              â”‚
â”‚  â”œâ”€ Authentication (HTTPBasic)                             â”‚
â”‚  â”œâ”€ User Management (users.json)                           â”‚
â”‚  â”œâ”€ Request Processing (update_requests.json)              â”‚
â”‚  â”œâ”€ Session Management (sessions.json)                     â”‚
â”‚  â”œâ”€ Job Code Cache (SQLite)  â† NEW                        â”‚
â”‚  â”œâ”€ Job Code Master DB (SQLite)  â† NEW                    â”‚
â”‚  â”œâ”€ BigQuery Sync (Background Thread)  â† NEW              â”‚
â”‚  â”œâ”€ Email Notifications (SMTP)                             â”‚
â”‚  â””â”€ Static File Serving                                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                   â”‚
                   â”œâ”€ Reads/Writes JSON files (users, sessions, requests)
                   â”‚
                   â”œâ”€ SQLite Cache (jobcodes_cache.db)
                   â”‚   â”œâ”€ polaris_job_codes table
                   â”‚   â”œâ”€ job_code_master table
                   â”‚   â””â”€ sync_history table
                   â”‚
                   â””â”€ BigQuery (auto-sync every 30 min)
                       â””â”€ polaris-analytics-prod.us_walmart
```

---

## Network Access & URL Setup

### Why the Hostname-Based URL?

Your machine has a **permanent network hostname** that resolves on the Walmart VPN:

```
LEUS62315243171.homeoffice.Wal-Mart.com
```

This is **better than IP addresses** because:
- âœ… **Never changes** - Even if your IP address changes, the hostname stays the same
- âœ… **Team-shareable** - Colleagues on VPN can use the same URL
- âœ… **Professional** - Works reliably over long periods

### Access Methods

| User | URL | Details |
|------|-----|---------|
| You (locally) | `http://localhost:8080/static/index.html` | Dev/testing |
| You (from another machine) | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080/static/index.html` | Over VPN |
| Team members | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080/static/index.html` | Over VPN from their computers |

**Related Documentation:** See [Local Hosting Guide](../../Spark-Playground/General%20Setup/Local%20Hosting/NETWORK_SHARING.md) for detailed network setup instructions.

### Prerequisites for Team Access

1. **Server binding**: FastAPI configured to bind to `0.0.0.0` (not localhost)
   - âœ… Already configured in main.py: `HOST = "0.0.0.0"`

2. **Firewall rules**: Port 8080 must allow inbound traffic
   - PowerShell command (run as Admin):
   ```powershell
   New-NetFirewallRule -DisplayName "JobCode Dashboard 8080" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
   ```

3. **Server running**: Dashboard server must be active
   - Run: `python backend\main.py` or use `start_server.bat`

---

## Data Architecture (Updated - April 7, 2026)

### 3-Tier Data System

**Tier 1: Polaris Cache (SQLite)**
- Table: `polaris_job_codes` (source of truth from BigQuery)
- Auto-syncs every 30 minutes from BigQuery
- Fallback snapshots if sync fails
- Replaces: `polaris_job_codes.csv` (static file)

**Tier 2: Job Code Master (SQLite)**
- Table: `job_code_master` (platform-managed enrichment)
- User-entered data via dashboard (Job Codes Tab)
- Columns: workday_code, category, job_family, pg_level, supervisor, notes, etc.
- Replaces: `Job_Code_Master_Table.xlsx` (Excel file)

**Tier 3: Job Code Complete (Runtime Merge)**
- Endpoint: `GET /api/job-codes`
- Merges: Polaris (base) + Master (enrichment) + Teaming (assignments)
- Frontend displays unified view

### Sync Architecture

```
BigQuery (Polaris Source)
       â†“ (every 30 min)
SQLite Cache (polaris_job_codes table)
       â†“
Backend /api/job-codes endpoint
       â†“
Frontend displays merged data
```

## Data Flow

### 1. **Startup Initialization**
```
Server starts
  â”œâ”€ Initialize SQLite cache (create tables if not exist)
  â”œâ”€ Perform initial BigQuery sync (if HAS_BIGQUERY)
  â””â”€ Start background sync thread (30-min interval)
```

### 2. **User Views Job Codes**
```
GET /api/job-codes
  â”œâ”€ Query: polaris_job_codes table (Polaris base data)
  â”œâ”€ Join: job_code_master table (User enrichment data)
  â”œâ”€ Join: TMS Data (Teaming assignments) if available
  â””â”€ Return merged result to frontend
```

### 3. **User Updates Job Code Metadata**
```
POST /api/job-codes-master/{job_code}
  â”œâ”€ Admin user update data
  â”œâ”€ INSERT/UPDATE job_code_master table
  â””â”€ Return updated record with timestamp
```

### 4. **Background Sync Process**
```
Every 30 minutes (background thread)
  â”œâ”€ Query BigQuery for latest Polaris data
  â”œâ”€ Validate minimum record count (>100)
  â”œâ”€ REPLACE polaris_job_codes table
  â”œâ”€ Log sync in sync_history table
  â”œâ”€ Save snapshot JSON as fallback
  â””â”€ Alert admin if sync fails
```

### 5. **Data Sources Summary**
| Source | Purpose | Method | Updated |
|--------|---------|--------|---------|
| BigQuery | Job codes, user counts | Auto-sync | Every 30 min |
| SQLite Cache | Fast local queries | Auto-indexed | Real-time |
| Job Code Master | Enrichment (category, family, etc.) | Dashboard UI | On-demand |
| Teaming Excel | Team assignments | Manual upload | When updated |
| **ELM** | **WM Stores, Facilities & Banner Codes** | **Auto-sync** | **Daily** |

---

## ELM Datasource - WM Stores & Facilities (Updated - April 16, 2026)

### Overview
**ELM (Enterprise Location Management)** is the authoritative source for all Walmart store and facility information, including complete banner code definitions.

### Key Tables

| Table | Project | Dataset | Purpose |
|-------|---------|---------|---------|
| `division_view` | `wmt-loc-cat-prod` | `catalog_location_views` | Store details, banners, locations, status |
| `businessunit_view` | `wmt-loc-cat-prod` | `catalog_location_views` | Business unit hierarchy and organization |

### Division Structure

**Division 1: WM US Stores**
- Format: Standard Walmart Supercenters, Neighborhood Markets, etc.
- Banner codes: WAL, NHM, SAM, and others
- Used for: Store-level targeting and job codes

**Division 10: Health & Wellness (H&W)**
- Format: Pharmacy operations, health facilities
- Banner codes: RX and H&W specific codes
- Used for: Pharmacy and health-focused job codes

### Query Template - Division 1 (WM US Stores)

```sql
SELECT
  CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,
  physical_city AS CITY_NAME,
  LEFT(physical_zip_code,5) AS POSTAL_CODE,
  region_code AS REGION_NBR,
  martket_code AS MARKET_AREA_NBR,
  division_nbr,
  division_name,
  format_code,
  CASE division_name
    WHEN 'WAL-MART STORES INC.' THEN 'Store'
    WHEN 'PHARMACY' THEN 'H&W'
    ELSE division_name
  END AS Alignment,
  CASE subdivision_code
    WHEN 'A' THEN 'SOUTHEAST BU'
    WHEN 'B' THEN 'SOUTHWEST BU'
    WHEN 'C' THEN 'FORMAT DEVELOPMENT'
    WHEN 'D' THEN 'STORE NO 8'
    WHEN 'E' THEN 'NORTH BU'
    WHEN 'F' THEN 'EAST BU'
    WHEN 'G' THEN 'RETAIL SUBDIVISION G'
    WHEN 'M' THEN 'WEST BU'
    WHEN 'O' THEN 'NHM BU'
    WHEN 'X' THEN 'US Retail SD X'
    WHEN 'I' THEN 'PR BU'
    WHEN 'Z' THEN 'RX Facilities'
    ELSE subdivision_code
  END AS SUBDIV_NAME,
  banner_code AS BANNER_CODE,
  banner_desc AS BANNER_DESC,
  bu_status_code AS OPEN_STATUS_CODE,
  bu_status_desc AS OPEN_STATUS_DESC,
  physical_county AS COUNTY_NAME,
  physical_country_code AS COUNTRY_CODE,
  physical_state_code AS STATE_PROV_CODE,
  LATITUDE AS LATITUDE_DGR,
  longitude AS LONGITUDE_DGR
FROM
  `wmt-loc-cat-prod.catalog_location_views.division_view`
WHERE
  physical_country_code = 'US'
  AND base_division_desc = "WAL-MART STORES INC."
  AND division_nbr = 1
  AND bu_status_desc != 'CLOSED'
  AND Date(new_bu_start_date) <= date_add(current_date(), INTERVAL 90 DAY)
```

### Query Template - Division 10 (Health & Wellness)

Same structure as Division 1, but with `division_nbr = 10`

### Output Tables

**Division 1 Data:**
- BigQuery: `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Div 1 Data`
- Frequency: Daily (queries run each morning)

**Division 10 Data:**
- BigQuery: `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Div 10 Data`
- Frequency: Daily (queries run each morning)

### Banner Codes Reference

Extracted from ELM `division_view.banner_code` and `banner_desc` - **Division 1 & 10 only**:

**Division 1 - WM US Stores (Primary Retail):**

| Code | Description | Type |
|------|-------------|------|
| A1 | WM Supercenter | Store |
| B2 | Walmart Express | Store |
| B4 | Neighborhood Market | Store |
| C7 | Wal-Mart | Store |
| D7 | Sam's Club | Store |
| H8 | walmart.com | eCommerce |
| H9 | samsclub.com | eCommerce |
| O3 | WM On Campus/RX Facilities | Special |
| S3 | WALMART NEIGHBORHOOD MARKET | Store |
| Z1 | STAND ALONE PICKUP | Special |

**Division 10 - Health & Wellness:**

| Code | Description | Type |
|------|-------------|------|
| N7 | Pharmacy | H&W |
| O3 | WM On Campus/RX Facilities | Special |

**Note**: O3 (WM On Campus/RX Facilities) appears in both divisions and represents specialty facilities

### Usage in Dashboard

**Banner Code Dropdown:**
- Source: Query result from `Store Cur Div 1 Data` and `Store Cur Div 10 Data` tables
- Display format: `{BANNER_CODE} - {BANNER_DESC}`
- Examples:
  - `WAL - Walmart Supercenter`
  - `NHM - Neighborhood Market`
  - `RX - Pharmacy`
  - `O3 - Aligned`

---

## Backend Components

### Core Modules

1. **Authentication** (`main.py` - lines 1-200)
   - HTTPBasic authentication
   - Password hashing with SHA256
   - Session token management

2. **Cache Management** (`sqlite_cache.py` - NEW)
   - SQLite database for Polaris job codes
   - Job code master table for enrichment data
   - Background sync from BigQuery (30-min interval)
   - Snapshot fallback for resilience
   - Fast queries via local database

3. **User Management** (`main.py` - lines 201-400)
   - Load/save users.json
   - Role-based access control (Admin/User)
   - User registration workflow

4. **Job Code Processing** (`main.py` - lines 400-800)
   - Query Polaris cache (SQLite)
   - Merge with master table data
   - Merge with Teaming assignments
   - Generate complete job code view

5. **Request Handling** (`main.py` - lines 800-1200)
   - Process update requests
   - Admin approval/rejection
   - Export functionality
   - Email notifications

6. **Session Management** (`main.py` - lines 1200+)
   - Track active sessions
   - Timeout handling
   - User state management

### Key Endpoints

**Job Code Queries:**
- `GET /api/job-codes` - All job codes with enrichment
- `GET /api/job-codes/{job_code}` - Single job code detail
- `GET /api/job-codes-master` - Master data only

**Master Data Management:**
- `POST /api/job-codes-master/{job_code}` - Update master data
- `POST /api/job-codes-master/{job_code}/notes` - Update notes

**Cache Administration:**
- `GET /api/cache-status` - Sync status and health
- `POST /api/cache/sync-now` - Manual BigQuery sync trigger

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
- **Input**: polaris_job_codes.csv + TMS Data (3).xlsx (for reference only now - uses cache)
- **Output**: Missing_From_Teaming_POLARIS.csv, Teaming_Not_In_Polaris.csv
- **Run**: `python polaris_comparison.py`

### `get_user_ids.py`, `get_user_details_bigquery.py`, `get_worker_names_stores.py`
- **Purpose**: Extract data from BigQuery and HR systems
- **Used to collect**: Job codes, user counts, department details
- **Note**: Cache auto-syncs now, manual extraction less necessary

---

## User Roles & Permissions

### Admin
```
âœ… View all job codes (entire list)
âœ… Update job code master data (enrichment fields)
âœ… View all user requests (all submissions)
âœ… Approve/reject user registrations
âœ… Approve/reject teaming update requests
âœ… Export approved requests (for TMS upload)
âœ… Change user roles
âœ… View analytics/reports
âœ… Trigger manual cache sync
âœ… View cache sync status
```

### User
```
âœ… View all job codes
âœ… Submit teaming update requests
âœ… View own request history
âŒ Approve requests
âŒ Change user roles
âŒ Export data
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

âš ï¸ **Default Credentials**
- Default admin: `admin` / `admin123`
- **MUST change on first login**

ðŸ” **Password Storage**
- Stored as SHA256 hash
- Never stored in plaintext

ðŸ›¡ï¸ **Network Access**
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

âœ… **Hostname-based URLs** are stable and team-shareable on VPN
âœ… **FastAPI backend** handles all business logic
âœ… **JSON data files** store users, requests, and session data
âœ… **Email notifications** keep admins updated on new requests
âœ… **Multiple data sources** (TMS, Polaris, HR) are merged and reconciled
âœ… **Firewall rule required** for team access from other machines

