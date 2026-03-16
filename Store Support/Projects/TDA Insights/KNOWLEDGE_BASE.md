# TDA Initiatives Insights Dashboard — Knowledge Base

**Last Updated:** March 16, 2026  
**Project:** Walmart Store Support — TDA Initiative Tracking  
**Port:** 5000  
**Data Source:** `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` (BigQuery)

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Frontend (Browser)                            │
│              dashboard.html — HTML5/CSS3/Vanilla JS              │
│           Walmart Living Design · html2canvas · PPT Export       │
└───────────────────────┬──────────────────────────────────────────┘
                        │ HTTP (localhost:5000)
┌───────────────────────▼──────────────────────────────────────────┐
│                   backend_simple.py                               │
│              Pure-socket HTTP server (no Flask)                   │
│         BigQuery fetch → JSON API → PPT generation               │
│            Binds: 127.0.0.1:5000                                 │
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
│            Intake_Card_Nbr, Link, Impl_Date                     │
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
- **Host:** 127.0.0.1 (localhost only)
- **CORS:** `Access-Control-Allow-Origin: *`

### Startup Process

1. Load `.env` file (optional — uses defaults if missing)
2. Set `BQ_PROJECT`, `BQ_DATASET`, `BQ_TABLE` from environment
3. Attempt BigQuery import → set `BQ_AVAILABLE` flag
4. Call `get_bigquery_data()` → query BQ with aggregation
5. If BQ fails → fall back to `SAMPLE_DATA` (5 hardcoded projects)
6. Set `DATA` = BQ result or sample data
7. Start listening on port 5000

**Key:** Data is loaded once at startup and cached. Server restart required for fresh data.

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
    MAX(Intake_Card_Nbr) as `Project ID`
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Topic IS NOT NULL
GROUP BY Topic, Health_Update, Phase, Intake_n_Testing, Dallas_POC, Deployment
ORDER BY Topic
```

**Note (March 16, 2026):** The `CASE WHEN Phase = Facility_Phase` store count logic needs review. BQ data now has 169 rows where most POC/POT rows have `Facility_Phase=Test` (not `POC/POT`), causing store count mismatches.

### API Endpoints

| Path | Method | Purpose |
|------|--------|---------|
| `/` or `/dashboard.html` | GET | Serves dashboard HTML |
| `/html2canvas.min.js` | GET | Serves local html2canvas library |
| `/api/health` | GET | Health check with BQ connection status |
| `/api/data` | GET | Filtered project data (multi-select: phases, health_statuses, titles) |
| `/api/phases` | GET | Available phase list (ordered) |
| `/api/health-statuses` | GET | Available health status values |
| `/api/titles` | GET | Available project title list |
| `/api/summary` | GET | Summary statistics |
| `/api/export/csv` | GET | CSV export of filtered data |
| `/api/ppt/generate` | GET | Server-side minimal PPTX generation |
| `/api/ppt/generate-from-screenshots` | POST | PPTX from client-side html2canvas screenshots |

### Fallback Sample Data

When BigQuery is unavailable, serves 5 hardcoded projects:
- Sidekick Enhancement (Test, 120 stores)
- GMD Optimization (POC/POT, 95 stores)
- DSD Redesign (Roll/Deploy, 250 stores)
- Fresh Department Update (Pending, 180 stores)
- Inventory System Migration (Mkt Scale, 15 stores)

---

## Dashboard (dashboard.html)

### Features

- Multi-select dropdown filters (Phase, Health Status, Project Title)
- Summary stat cards (Total Projects, Total Stores, On Track, At Risk, Off Track, Continuous)
- Phase-organized table with pagination
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
Total Projects  = data.length
Total Stores    = SUM(# of Stores)
On Track        = count where Health Status contains "on track"
At Risk         = count where Health Status contains "at risk"
Off Track       = count where Health Status contains "off track"
Continuous      = count where Health Status contains "continuous"
```

### Table Pagination

- **Phase order:** Pending → POC/POT → Test → Mkt Scale → Roll/Deploy
- **Complete phase excluded** from display
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
PHASE_ORDER    = ['Pending', 'POC/POT', 'Test', 'Mkt Scale', 'Roll/Deploy']
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
| Dallas_POC | STRING | Point of contact |
| Deployment | STRING | Deployment status notes |
| Intake_Card_Nbr | INTEGER | Project ID for Intake Hub linkage |
| Link | STRING | URL |
| Impl_Date | DATE | Implementation date |

### Phase Model

```
Phase lifecycle (project-level):
  Pending → POC/POT → Test → Mkt Scale → Roll/Deploy → Complete

Facility_Phase (store-level):
  Indicates what phase the stores are actually in for a given row.
  One Topic can have multiple rows with different Facility_Phase values.
  E.g., "Practice Card" may have rows for Mkt Scale (220), Roll/Deploy (2), Complete (31)
```

### Data Relationships (March 16 observations)

- Table has **169 rows** (multiple rows per Topic)
- Each row represents stores in a specific Facility_Phase for a Topic
- A single Topic at Phase=POC/POT may have Facility_Phase=Test (stores being tested)
- Distinct Facility_Phase values: Complete, Mkt Scale, No List, Pending, Roll/Deploy, Test
- Phase values: Complete, POC/POT, Pending, Roll/Deploy, Test, Mkt Scale

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
| Local (you) | `http://localhost:5000/dashboard.html` |
| Team (VPN) | `http://LEUS62315243171.homeoffice.Wal-Mart.com:5000/dashboard.html` |

**Note:** Backend binds to `127.0.0.1`. To share on VPN, change to `0.0.0.0` and add firewall rule:
```powershell
New-NetFirewallRule -DisplayName "TDA Dashboard 5000" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

---

## Startup

### Manual

```powershell
cd "Store Support\Projects\TDA Insights"
$env:GOOGLE_APPLICATION_CREDENTIALS = "$env:APPDATA\gcloud\application_default_credentials.json"
python backend_simple.py
# Open: http://localhost:5000/dashboard.html
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

## Known Issues & Pending Work (March 16, 2026)

1. **Store Count Logic** — `SUM(CASE WHEN Phase = Facility_Phase THEN Facility ELSE 0 END)` zeros out most POC/POT rows since their Facility_Phase is "Test". Needs review.
2. **Backend serves sample data if BQ fails at startup** — Server must be restarted with valid GCP credentials to get real data. No runtime refresh endpoint.
3. **PPT right margin** — Edge headless reserves 24 CSS px scrollbar gutter. Auto-crop to `bbox[2]` mostly resolves but thin white strip may appear.
4. **Windows Task Scheduler** — Weekly email on Thursdays 11 AM CT not yet scheduled.
5. **Outdated documentation** — README, GETTING_STARTED, API_REFERENCE, IMPLEMENTATION_SUMMARY, QUICKSTART all reference Flask/python-pptx from the March 3 initial build. Should be updated or removed.
6. **Debug scripts** — ~15 debug/test/investigation scripts can be cleaned up.
