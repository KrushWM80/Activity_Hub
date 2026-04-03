# V.E.T. Dashboard Executive Report

> **Last Updated**: April 2, 2026

## ⚠️ Known Issues & Fixes (April 2, 2026)

### BigQuery Ownership Column Renamed
The `TDA_Ownership` filter in BigQuery was renamed from `"Dallas POC"` to `"Dallas VET"`.  
`backend.py` has been updated: `BQ_OWNERSHIP_FILTER = "Dallas VET"` (147 rows).  
If data shows empty again, re-check `TDA_Ownership` values in BQ against the filter in `backend.py`.

### Server Startup (PowerShell stderr problem)
Flask writes log messages to stderr. PowerShell treats **any** stderr output as an error and kills the process.  
**Do NOT start the server from PowerShell directly.**  
Always use the bat file: `Automation/start_vet_dashboard_24_7.bat` → which calls `start_server.py` via cmd.exe.

`start_server.py` — purpose-built launcher that:
- Sets UTF-8 encoding (fixes emoji crash)
- Redirects Flask logging to stdout
- Sets GCP credentials
- Calls `backend.py`

### Email Report — 3-Tier Fallback
`send_vet_report_final.py` uses: **API (:5001) → Direct BigQuery → Sample data (last resort only)**  
`Automation/send_vet_daily_email.bat` now checks port 5001 is up before running the report,  
and starts the backend automatically if it's down.

### Do NOT use `Stop-Process -Name python`
This kills ALL Python services on the machine. To restart only VET:
```powershell
$pid = (netstat -ano | Select-String ":5001.*LISTENING" | ForEach-Object { ($_ -split "\s+")[-1] }) | Select-Object -First 1
if ($pid) { taskkill /F /PID $pid }
# Bat loop restarts within 5-7 seconds automatically
```

---

## Overview

**V.E.T. Dashboard Executive Report** is a specialized executive dashboard for TDA (Tactical Data Analytics) initiatives with a Dallas VET (formerly "Dallas POC") focus. It provides real-time visibility into project health, implementation status, and critical issues requiring immediate attention.

### Key Differentiators from TDA Insights

- **Dallas POC Filter**: Automatically filtered to show Dallas POC initiatives only
- **Executive Notes**: Displays Dallas POC information as "Executive Notes" column
- **Needs Attention Section**: Card-based view of "At Risk" initiatives for quick executive overview
- **Implementation Week**: Displays Walmart Week (WM Week) from Intake Hub data for implementation planning
- **PPT Export**: Generates professional reports with "Needs Attention" slide followed by "Initiatives" slides

## Architecture

### Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask
- **Database**: Google BigQuery
- **Services**: 
  - `backend.py` - Flask REST API for data fetching and filtering
  - `ppt_service.py` - PowerPoint report generation
  
### Data Sources

| Source | Table | Purpose |
|--------|-------|---------|
| BigQuery | `Output- TDA Report` | TDA initiatives and project metadata |
| BigQuery | `IH_Intake_Data` | Intake Hub project data with implementation weeks |

## Configuration

### Environment Variables (`.env`)

```
# BigQuery Configuration
GCP_PROJECT_ID=wmt-assetprotection-prod
BIGQUERY_DATASET=Store_Support_Dev
BIGQUERY_TABLE=Output- TDA Report

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=5000

# Google Cloud Authentication
GOOGLE_APPLICATION_CREDENTIALS=
```

### Default Filters

- **TDA Ownership**: Dallas POC (fixed filter, cannot be changed)
- **Phase**: All Selected (user-selectable)
- **Health Status**: All Selected (user-selectable)
- **Project Title**: All Selected (user-selectable)

## API Endpoints

### Data Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/data` | GET | Fetch filtered initiatives data |
| `/api/phases` | GET | Get unique project phases |
| `/api/health-statuses` | GET | Get unique health statuses |
| `/api/ownerships` | GET | Get TDA ownerships (V.E.T. = Dallas POC only) |
| `/api/needs-attention` | GET | Get At Risk initiatives for executive view |
| `/api/summary` | GET | Get summary statistics |

### Export/Report Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/export/csv` | GET | Export filtered data as CSV |
| `/api/ppt/generate` | POST | Generate PowerPoint report |

## Dashboard Sections

### 1. Filter Controls
- Phase dropdown (multi-select)
- Health Status dropdown (multi-select)
- TDA Ownership (Dallas POC - display only)
- Project Title dropdown (multi-select)
- Action buttons: Apply Filters, Reset, Refresh, Export CSV, Generate PPT

### 2. Summary Statistics
- Total Projects (Dallas POC)
- Total Stores Impacted
- On Track (count)
- At Risk (count)
- Off Track (count)
- Continuous (count)

### 3. Needs Attention Section
*Note: To be implemented in Phase 4*
- Card-based layout showing "At Risk" initiatives
- Displays: Initiative title, At Risk badge, Phase, Store count, Executive Notes, Deployment status
- Ordered by Phase and store count

### 4. Initiatives Table
- Grouped by Phase (secondary grouping by TDA Ownership)
- Columns:
  - Initiative Title (linked to HOOPS Intake Hub)
  - Health Status (color-coded badge)
  - Phase (blue tag)
  - # of Stores (count)
  - Executive Notes (Dallas POC full text)
  - WM Week (Implementation week from Intake Hub, earliest if multiple stores)
  - Deployment Status

### 5. Pagination & Export
- 8 rows per page (optimized for PowerPoint slide dimensions)
- CSV export includes all columns and data
- PPT generation with title pages and detailed tables

## Column Mapping

| Display Name | BigQuery Field | Source |
|------------|------------|--------|
| Initiative Title | `Initiative - Project Title` | TDA Report |
| Health Status | `Health Status` | TDA Report |
| Phase | `Phase` | TDA Report |
| # of Stores | `# of Stores` | TDA Report |
| Executive Notes | `Dallas POC` | TDA Report |
| WM Week | `WM_Week` | IH_Intake_Data (MIN aggregation) |
| Deployment | `Deployment` | TDA Report |

## BigQuery Query Logic

The backend executes a query that:

1. Selects TDA initiatives where `TDA_Ownership = 'Dallas POC'`
2. LEFT JOINs with Intake Hub data on `Intake_Card_Nbr`
3. Aggregates the earliest `WM_Week` for each initiative (MIN function)
4. Returns data ordered by Phase then Initiative Title

### Sample Query

```sql
SELECT 
    tda.`Initiative - Project Title`,
    tda.`Health Status`,
    tda.Phase,
    tda.`# of Stores`,
    tda.`Dallas POC` AS `Executive Notes`,
    tda.`TDA Ownership`,
    tda.Intake_Card_Nbr AS `Project ID`,
    tda.`Intake & Testing`,
    tda.Deployment,
    COALESCE(MIN(intake.WM_Week), 'TBD') AS `WM Week`
FROM 
    `wmt-assetprotection-prod.Store_Support_Dev.`Output- TDA Report`` tda
LEFT JOIN 
    `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` intake
    ON CAST(tda.Intake_Card_Nbr AS STRING) = CAST(intake.Intake_Card AS STRING)
WHERE 
    tda.`TDA Ownership` = 'Dallas POC'
GROUP BY
    [all non-aggregated columns]
ORDER BY 
    tda.Phase ASC,
    tda.`Initiative - Project Title` ASC
```

## Starting the Dashboard

### Backend Setup

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up Google Cloud authentication
# Option A: Default Application Credentials
gcloud auth application-default login

# Option B: Service Account (set in .env)
# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# 3. Start the backend server
python backend.py

# Server will run on http://127.0.0.1:5000
```

### Frontend Access

- URL: `http://127.0.0.1:5000/`
- Dashboard will auto-load filters and display Dallas POC initiatives

## Performance Considerations

### Caching

- All data is cached for 5 minutes to reduce BigQuery costs
- Use "Refresh Data" button to force immediate cache refresh
- Cache automatically expires and refreshes after 5 minutes

### Pagination

- 8 rows per page (matches PowerPoint slide dimensions of 1280x720px)
- Grouped rendering by Phase for better organization
- Dynamic pagination based on filtered results

## Troubleshooting

### Dashboard Won't Load

1. Check backend is running: `http://127.0.0.1:5000/api/health`
2. Check BigQuery connectivity: Review backend logs for connection errors
3. Verify `.env` configuration and Google Cloud credentials

### No Data Displayed

1. Verify BigQuery tables contain Dallas POC initiatives
2. Check filter selections (at least one Phase and Health Status must be selected)
3. Review backend logs: `tail -f tda_insights_server.log`

### Intake Hub Data Missing

- WM Week column shows "TBD" if no Intake Hub record matches the Project ID
- Verify Project IDs exist in both tables: 
  - `Intake_Card_Nbr` in Output- TDA Report
  - `Intake_Card` in IH_Intake_Data

## Files

```
VET_Dashboard/
├── vet_dashboard.html    - Frontend UI (HTML/CSS/JS)
├── backend.py            - Flask backend API
├── ppt_service.py        - PPT generation service
├── requirements.txt      - Python dependencies
├── .env                  - Environment configuration
└── README.md             - This file
```

## Dependencies

See [requirements.txt](requirements.txt) for full list. Key packages:

- `flask` - Web framework
- `flask-cors` - CORS support
- `google-cloud-bigquery` - BigQuery client
- `python-pptx` - PowerPoint generation
- `python-dotenv` - Environment configuration

## License

Internal Walmart Tool

---

**Last Updated**: March 20, 2026  
**Version**: 1.0.0-Phase 2 (Backend Implementation Complete)
