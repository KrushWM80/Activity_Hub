# TDA Initiatives Insights Dashboard — Knowledge Base

**Last Updated:** March 31, 2026  
**Project:** Walmart Store Support — TDA Initiative Tracking  
**Port:** 5000  
**Host:** 0.0.0.0 (all interfaces — accessible to others on the network)  
**Data Source:** `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` (BigQuery)

> **March 31, 2026 — Naming Changes (temporary normalization in code until BQ data updates):**
> - "Total Projects" → **"Total Initiatives"** in dashboard and email reports
> - TDA Ownership: "Dallas POC" → **"Dallas VET"**
> - Phases renamed: POC/POT → **Vet**, Mkt Scale → **Test Markets**
> - New phase order: Pending → Vet → Test → Test Markets → Roll/Deploy → Complete
> - `_PHASE_MAP` and `_OWNERSHIP_MAP` dicts in backend_simple.py and send_weekly_report.py handle transition

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Frontend (Browser)                            │
│              dashboard.html — HTML5/CSS3/Vanilla JS              │
│           Walmart Living Design · html2canvas · PPT Export       │
└───────────────────────┬──────────────────────────────────────────┘
                        │ HTTP (0.0.0.0:5000)
┌───────────────────────▼──────────────────────────────────────────┐
│                   backend_simple.py                               │
│              Pure-socket HTTP server (no Flask)                   │
│         BigQuery fetch → JSON API → PPT generation               │
│            Binds: 0.0.0.0:5000 (network-accessible)             │
└───────────────────────┬──────────────────────────────────────────┘
                        │ google-cloud-bigquery
┌───────────────────────▼──────────────────────────────────────────┐
│                   BigQuery (GCP)                                  │
│   Project: wmt-assetprotection-prod                              │
│   Dataset: Store_Support_Dev                                     │
│   Table:   Output- TDA Report                                   │
│                                                                   │
│   Columns: Topic, Health_Update, Phase, Facility, Facility_Phase,│
│            Intake_n_Testing, Dallas_POC, Deployment,             │
│            Intake_Card_Nbr, Link, Impl_Date, TDA_Ownership       │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                 send_weekly_report.py                             │
│        Automated weekly email (Outlook COM + Edge headless)      │
│        BQ fetch → Edge screenshots → PPTX → Outlook send        │
│        Scheduled: Thursdays 11:00 AM CT                          │
└──────────────────────────────────────────────────────────────────┘
```

---

## Core Files

| File | Purpose | Lines |
|------|---------|-------|
| **backend_simple.py** | Pure-socket HTTP server, BQ data, JSON API, PPT endpoint | ~970 |
| **dashboard.html** | Interactive web dashboard, multi-select filters, html2canvas PPT export | ~2000 |
| **send_weekly_report.py** | Weekly automated email with Edge headless PPT + Outlook send | ~400 |
| **html2canvas.min.js** | Local copy of html2canvas (avoids CDN/firewall issues) | lib |
| **START.bat / START.ps1** | One-click server startup scripts | startup |
| **requirements.txt** | Python dependencies | config |
| **.env** | Environment variables (GCP project, dataset, table) | config |

### Documentation Files (Legacy — from early March builds)

| File | Status | Notes |
|------|--------|-------|
| README.md | **Outdated** | References Flask, python-pptx (neither is used now) |
| GETTING_STARTED.md | **Outdated** | References old backend.py |
| API_REFERENCE.md | **Outdated** | Documents old Flask endpoints |
| QUICKSTART.md | **Outdated** | References old startup flow |
| BIGQUERY_SETUP.md | Current | GCP auth instructions still valid |
| DESIGN_SYSTEM.md | Current | Color palette and typography still accurate |
| IMPLEMENTATION_SUMMARY.md | **Outdated** | References Flask, python-pptx |
| PPT_EXPORT_STATUS.md | **Outdated** | March 5 blocker (resolved) |
| PPT_REPAIR_ISSUES.md | **Outdated** | Regression fixed |
| PPTX_ANALYSIS.md | **Outdated** | Early debugging notes |

### Debug / Utility Scripts (Can be cleaned up)

| File | Purpose |
|------|---------|
| _refresh.py | Temp BQ data check script |
| check_data.py, check_stores.py, check_branch.py, check_pic_xml.py | Debug scripts |
| diagnose_data.py, deep_debug_pptx.py, debug_pptx.py | Debug scripts |
| investigate_data.py, investigate_phases.py | Data investigation |
| analyze_data_diff.py, quick_diag.py | Analysis scripts |
| verify_api.py, verify_changes.py | Verification scripts |
| test_pptx_gen.py, test_create_minimal.py | Test scripts |
| generate_ppt.py, ppt_service.py | Old PPT generation (replaced by dashboard html2canvas) |
| backend.py, old_backend.py | Old Flask-based backends (replaced by backend_simple.py) |
| email_preview.html | Generated email preview (output, not source) |

### Output Files

| File | Type |
|------|------|
| TDA_WK6_Report.pptx | Week 6 generated report |
| TDA_WK11_Report.pptx | Week 11 generated report |
| TDA_Weekly_Report.pptx | Generic report output |
| test_output.pptx, test_minimal.pptx, test_fixed.pptx | Test outputs |
| server.log, tda_insights_server.log | Server logs |
| Email Version.pdf | Reference PDF of email format |

---

## Backend (backend_simple.py)

### Server Details

- **Type:** Pure-socket HTTP server (no Flask, no framework)
- **Port:** 5000
- **Host:** 0.0.0.0 (all network interfaces — accessible to team via hostname or IP)
- **CORS:** `Access-Control-Allow-Origin: *`

### Startup Process

1. Load `.env` file (optional — uses defaults if missing)
2. Set `BQ_PROJECT`, `BQ_DATASET`, `BQ_TABLE` from environment
3. Attempt BigQuery import → set `BQ_AVAILABLE` flag
4. Call `get_bigquery_data()` → query BQ with aggregation
5. If BQ fails → fall back to `SAMPLE_DATA` (5 hardcoded projects)
6. Set `DATA` = BQ result or sample data
7. Start listening on port 5000

**Key:** Data is loaded once at startup and cached. Use `/api/refresh` endpoint or dashboard "Refresh Data" button to reload from BigQuery without restarting.

### BigQuery Query

```sql
SELECT 
    Topic as `Initiative - Project Title`,
    Health_Update as `Health Status`,
    Phase,
    SUM(CASE WHEN Phase = Facility_Phase THEN Facility ELSE 0 END) as `# of Stores`,
    Dallas_POC as `Dallas POC`,
    Intake_n_Testing as `Intake & Testing`,
    Deployment,
    MAX(Intake_Card_Nbr) as `Project ID`,
    COALESCE(TDA_Ownership, 'No Selection Provided') as `TDA Ownership`
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Topic IS NOT NULL
GROUP BY Topic, Health_Update, Phase, Intake_n_Testing, Dallas_POC, Deployment, TDA_Ownership
ORDER BY Topic
```

**Note (March 17, 2026):** Store count logic `CASE WHEN Phase = Facility_Phase` is confirmed correct — dashboard shows accurate counts (91 projects, 16 with stores > 0). The same query is used in `send_weekly_report.py`.

### API Endpoints

| Path | Method | Purpose |
|------|--------|---------|
| `/` or `/dashboard.html` or `/tda-initiatives-insights` | GET | Serves dashboard HTML |
| `/html2canvas.min.js` | GET | Serves local html2canvas library |
| `/api/health` | GET | Health check with BQ connection status |
| `/api/refresh` | GET | Re-fetch data from BigQuery into cache |
| `/api/data` | GET | Filtered project data (multi-select: phases, health_statuses, titles, ownerships) |
| `/api/phases` | GET | Available phase list (ordered) |
| `/api/health-statuses` | GET | Available health status values |
| `/api/ownerships` | GET | Available TDA Ownership values |
| `/api/titles` | GET | Available project title list |
| `/api/summary` | GET | Summary statistics |
| `/api/export/csv` | GET | CSV export of filtered data |
| `/api/ppt/generate` | GET | Server-side minimal PPTX generation |
| `/api/ppt/generate-from-screenshots` | POST | PPTX from client-side html2canvas screenshots |

### Fallback Sample Data

When BigQuery is unavailable, serves 5 hardcoded projects:
- Sidekick Enhancement (Test, 120 stores)
- GMD Optimization (Vet, 95 stores)
- DSD Redesign (Roll/Deploy, 250 stores)
- Fresh Department Update (Pending, 180 stores)
- Inventory System Migration (Test Markets, 15 stores)

---

## Dashboard (dashboard.html)

### Features

- Multi-select dropdown filters (Phase, Health Status, TDA Ownership, Project Title)
- Summary stat cards (Total Initiatives, Total Stores, On Track, At Risk, Off Track, Continuous)
- **Two-level grouping:** TDA Ownership → Phase (navy ownership banner + blue phase sub-banner)
- Health status badges (color-coded)
- Project titles hyperlinked to Intake Hub (`https://hoops.wal-mart.com/intake-hub/projects/{ProjectID}`)
- CSV export
- PPT export (html2canvas screenshots → backend → PPTX download)
- Connection status indicator
- Last updated timestamp

### Multi-Select Filter Logic

- Custom dropdown with checkbox list (not native `<select>`)
- "All Selected" toggle at top
- Individual checkbox per option
- Display label updates (e.g., "3 of 5 selected")
- Click outside to close

### Summary Card Calculations

```
Total Initiatives = data.length
Total Stores    = SUM(# of Stores)
On Track        = count where Health Status contains "on track"
At Risk         = count where Health Status contains "at risk"
Off Track       = count where Health Status contains "off track"
Continuous      = count where Health Status contains "continuous"
```

### Table Pagination

- **Phase order:** Pending → Vet → Test → Test Markets → Roll/Deploy
- **Complete phase excluded** from display
- **Two-level grouping:** TDA Ownership (navy `#1E3A8A` banner, 15px padding) → Phase (blue `#3B82F6` sub-banner, 7px padding)
- "No Selection Provided" ownership displays as "TDA Ownership - Currently No TDA Ownership"
- Previous/Next buttons with "Page X of Y" indicator
- Content-aware pagination using DOM measurement

### PPT Generation Flow (Client-Side)

1. Organize data by phase in `phaseOrder`
2. For each phase → call `packRowsIntoPages()` to split into pages
3. Render each page as HTML table with inline styles into a 1280px hidden wrapper
4. Capture with `html2canvas(wrapper, {scale: 1.5, backgroundColor: 'white'})`
5. POST all screenshots as base64 PNG to `/api/ppt/generate-from-screenshots`
6. Backend wraps screenshots into PPTX slides (zipfile + raw XML)
7. Download PPTX blob

### Height-Based Pagination Constants

```
SLIDE_HEIGHT      = 720px
TITLE_HEIGHT      = 60px
TABLE_HEADER_HEIGHT = 50px
PADDING_MARGINS   = 30px
AVAILABLE_HEIGHT  = 580px (720 - 60 - 50 - 30)
AVERAGE_ROW_HEIGHT = 70px
ITEMS_PER_PAGE    = 8 (580 / 70)
```

Actual pagination uses DOM measurement: create hidden container, add rows, measure `offsetHeight`, pack until cumulative height exceeds `AVAILABLE_HEIGHT`.

---

## Weekly Email Report (send_weekly_report.py)

### Purpose

Generates and sends a weekly TDA Insights email with attached PPTX report via Outlook.

### Configuration

```python
RECIPIENTS     = ["Kendall.rush@walmart.com"]
PHASE_ORDER    = ['Pending', 'Vet', 'Test', 'Test Markets', 'Roll/Deploy']
EXCLUDED_PHASES = {'Complete'}
EDGE_PATH      = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PPT_FILENAME   = "TDA_WK{wm_week}_Report.pptx"
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `_walmart_week()` | Walmart fiscal week number (FY starts Saturday nearest Feb 1) |
| `fetch_data()` | Query BigQuery for latest data (same aggregation as backend) |
| `build_email_html(data)` | Generate Outlook-compatible HTML email body |
| `_build_phase_html(phase, rows)` | Build phase table HTML (matches dashboard styling) |
| `_measure_row_heights(phase, rows)` | Edge `--dump-dom` with JS injection to measure row heights |
| `_paginate_by_height(rows, heights)` | Split rows into pages (AVAILABLE_HEIGHT=800) |
| `_capture_html_screenshot(html, png, width=1280)` | Edge headless screenshot → Pillow auto-crop → JPEG |
| `generate_report_pptx(data)` | Title slide + screenshot slides assembled as PPTX |
| `send_outlook_email()` | Win32com Outlook with PPT attachment |
| `main()` | Entry point (supports `--preview` flag) |

### Email Generation Flow

```
1. fetch_data() → Query BigQuery
2. generate_report_pptx(data) → For each phase:
   a. _measure_row_heights() → Edge --dump-dom with JS injection
   b. _paginate_by_height() → Split rows into pages
   c. _build_phase_html() → HTML matching dashboard tables
   d. _capture_html_screenshot() → Edge headless → PNG → Pillow crop → JPEG
   e. Add screenshot as PPTX slide
3. build_email_html(data) → Professional HTML email with:
   - Spark logo (base64 encoded from General Setup/Design/Spark Blank.png)
   - Title: 26px "TDA Initiatives Insights"
   - Summary context paragraph
   - Phase tables (Title, Health Status, # Stores) — 14px fonts, 10px padding
   - Footer with timestamp
4. send_outlook_email() → win32com Outlook.Application COM
   - Subject: "TDA Initiative Insights - Weekly Report"
   - Attach PPTX
   - Send to RECIPIENTS list
```

### Edge Headless Screenshot Details

```
Edge flags:
  --headless --disable-gpu --no-sandbox --hide-scrollbars
  --force-device-scale-factor=1.5
  --window-size=1280,900
  --screenshot=<output.png>
  --virtual-time-budget=5000

Post-processing (Pillow):
  1. Open PNG
  2. Auto-crop to content bounding box (getbbox)
  3. Crop to bbox[2] width × bbox[3]+4 height
  4. Convert to JPEG quality=78
```

### Walmart Fiscal Week Calculation

```
FY starts Saturday nearest Feb 1
FY2027 starts January 31, 2026 (Saturday)
March 16, 2026 = WM WK 7
PPT filename: TDA_WK7_Report.pptx
```

---

## Data Model

### BigQuery Table Schema

| Column | Type | Description |
|--------|------|-------------|
| Topic | STRING | Initiative / Project title |
| Health_Update | STRING | On Track, At Risk, Off Track, Continuous |
| Phase | STRING | Current project phase |
| Facility | INTEGER | Store count for this Facility_Phase |
| Facility_Phase | STRING | Phase that the store count applies to |
| Intake_n_Testing | STRING | Intake and testing status notes |
| Dallas_POC | STRING | Point of contact (displayed as "Dallas VET") |
| Deployment | STRING | Deployment status notes |
| Intake_Card_Nbr | INTEGER | Project ID for Intake Hub linkage |
| Link | STRING | URL |
| Impl_Date | DATE | Implementation date |
| TDA_Ownership | STRING | TDA ownership group (e.g., "Intake & Test", NULL → "No Selection Provided") |

### Phase Model

```
Phase lifecycle (project-level):
    Pending → Vet → Test → Test Markets → Roll/Deploy → Complete

Facility_Phase (store-level):
  Indicates what phase the stores are actually in for a given row.
  One Topic can have multiple rows with different Facility_Phase values.
    E.g., "Practice Card" may have rows for Test Markets (220), Roll/Deploy (2), Complete (31)
```

### Data Relationships (March 16 observations)

- Table has **169 rows** (multiple rows per Topic)
- Each row represents stores in a specific Facility_Phase for a Topic
- A single Topic at Phase=Vet may have Facility_Phase=Test (stores being tested)
- Distinct Facility_Phase values: Complete, Test Markets, No List, Pending, Roll/Deploy, Test
- Phase values: Complete, Vet, Pending, Roll/Deploy, Test, Test Markets

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend Server | Pure-socket HTTP (Python, no framework) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Database | Google BigQuery |
| PPT (Dashboard) | html2canvas + zipfile XML |
| PPT (Email) | Edge headless screenshots + zipfile XML |
| Email | win32com (Outlook COM) |
| Image Processing | Pillow (PIL) |
| Design System | Walmart Living Design |
| Python Version | 3.14.3 |
| Auth | Google Application Default Credentials |

### Python Dependencies (requirements.txt)

```
google-cloud-bigquery
google-auth
python-dotenv
Pillow
pywin32
```

### External Tools

- **Edge:** `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` (headless screenshots)
- **Spark Logo:** `Store Support/General Setup/Design/Spark Blank.png` (7446 bytes, base64 in email)

---

## Environment Variables (.env)

```
GCP_PROJECT_ID=wmt-assetprotection-prod
BIGQUERY_DATASET=Store_Support_Dev
BIGQUERY_TABLE=Output_TDA Report
```

Also requires `GOOGLE_APPLICATION_CREDENTIALS` pointing to gcloud ADC JSON, or run `gcloud auth application-default login`.

---

## Network Access

| User | URL |
|------|-----|
| Local (you) | `http://localhost:5000/tda-initiatives-insights` |
| Team (network) | `http://WEUS42608431466:5000/tda-initiatives-insights` |
| Team (IP) | `http://10.97.114.181:5000/tda-initiatives-insights` |

**Server binds to `0.0.0.0:5000`** — accessible from any machine on the same network.

**Firewall rule** (created March 17, 2026):
```powershell
New-NetFirewallRule -DisplayName 'TDA Insights Dashboard' -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow -Profile Domain,Private
```

All three URL paths serve the dashboard: `/`, `/dashboard.html`, `/tda-initiatives-insights`

**API_BASE** in dashboard.html uses `window.location.origin` — works regardless of hostname/IP used to access.

---

## Startup

### Manual

```powershell
cd "Store Support\Projects\TDA Insights"
$env:GOOGLE_APPLICATION_CREDENTIALS = "$env:APPDATA\gcloud\application_default_credentials.json"
python backend_simple.py
# Open: http://localhost:5000/tda-initiatives-insights
```

### Via MASTER_SETUP (Automatic)

The `MASTER_SETUP_24_7.bat` at the workspace root starts all services including TDA on port 5000.

### START.bat

```batch
@echo off
cd /d "%~dp0"
pip install -r requirements.txt
python backend_simple.py
```

---

## Automation & Recovery

### Scheduled Tasks

| Task Name | Schedule | Purpose |
|-----------|----------|--------|
| `Activity_Hub_TDA_AutoStart` | On logon | Starts `start_tda_insights_24_7.bat` → `backend_simple.py` on port 5000 |
| `Activity_Hub_TDA_Daily_Email` | Daily 6:00 AM | Runs `send_tda_weekly_email.bat` |
| `Activity_Hub_TDA_Weekly_Email` | Thursdays 11:00 AM | Runs `send_tda_weekly_email.bat` → BQ → PPT → Outlook |
| `Activity_Hub_TDA_Watchdog` | Every 5 minutes | Checks port 5000 → auto-restarts `backend_simple.py` if down. Logs to `watchdog.log` |

### Bat Files (`Automation/`)
- `start_tda_insights_24_7.bat` — Port-kill block + restart loop. Primary crash recovery (5-7 sec downtime)
- `send_tda_weekly_email.bat` — Checks port 5000 is UP before running report; starts backend if down, waits 30s
- `create_weekly_email_task.ps1` — Admin script to recreate the scheduled task

### Recovery Layers
1. **Bat restart loop** — primary (5-7 sec recovery on crash)
2. **TDA Watchdog task** — backup, fires every 5 min if bat loop itself dies
3. **Continuous monitor** (`continuous_monitor.ps1`) — checks all 7 services every 5 min; only launches new bat if bat process is not already running
4. **Email fallback** — `send_tda_weekly_email.bat` starts backend automatically if port 5000 is down at email time

### ⚠️ NEVER use `Stop-Process -Name python`
This kills ALL Python processes on the machine — all 7 services go down.

**Safe way to restart only TDA (port 5000):**
```powershell
$p = (netstat -ano | Select-String ":5000.*LISTENING" | ForEach-Object { ($_ -split "\s+")[-1] }) | Select-Object -First 1
if ($p) { taskkill /F /PID $p }
# Bat loop restarts automatically within 5-7 seconds
```

### Adding/Changing This Service
If the port, entry point, or bat file changes, update ALL of:
1. `Automation/start_tda_insights_24_7.bat`
2. `Automation/register_tasks_cmd.bat`
3. `continuous_monitor.ps1` services array
4. `MONITOR_AND_REPORT.ps1` services list
5. `Documentation/KNOWLEDGE_HUB.md` Active Services table
6. This file

---

## Known Issues & Pending Work (March 17, 2026)

1. **Store counts confirmed correct** — Dashboard shows accurate data. Email needs test send to verify.
2. **PPT right margin** — Edge headless reserves 24 CSS px scrollbar gutter. Auto-crop to `bbox[2]` mostly resolves but thin white strip may appear.
3. **Outdated documentation** — README, GETTING_STARTED, API_REFERENCE, IMPLEMENTATION_SUMMARY, QUICKSTART all reference Flask/python-pptx from the March 3 initial build. Should be updated or removed.
4. **Debug scripts** — ~15 debug/test/investigation scripts can be cleaned up.
5. **TDA Ownership grouping** — Implemented March 17. Two-level layout: Ownership banner (navy) → Phase sub-banner (blue). Ownership values from BQ: "Intake & Test", "No Selection Provided" (includes NULLs). Special section for Pending + No Selection Provided always appears first.
6. **Network sharing** — Server now binds to `0.0.0.0`. Firewall rule "TDA Insights Dashboard" allows inbound TCP 5000. Friendly URL: `/tda-initiatives-insights`.
