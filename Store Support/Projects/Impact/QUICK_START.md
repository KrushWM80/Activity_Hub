# Impact Platform Dashboard - Quick Start Guide

## Updated Changes (April 14, 2026)

### 1. **Activity Hub Integration** ✅
- Projects tab now loads the dashboard through the FastAPI backend on port 8002
- Dashboard will display when clicking "Projects" in Activity Hub navigation

### 2. **UI/UX Updates** ✅
- Activity Hub header with navigation tabs (For You, Projects, Reporting, etc.)
- Projects tab highlighted when active
- Links section matches For You page styling
- Quick Stats section removed
- Responsive layout with right sidebar

### 3. **Health Status Labels** ✅ 
Updated to match standard terminology:
- Green → "On Track"
- Yellow → "At Risk"
- Red → "Off Track"
- Continuous support

### 4. **Dashboard Features**
- 4 metric boxes: Active Projects, Unique Owners, Updated This Week, Percent Updated
- Project filtering by Business Area, Health Status, Project Status
- Add Project modal form
- Generate PPT report button
- Project table with actions
- Links sidebar (Confluence, GitHub, Jira, Help Desk)

### 5. **Backend Changes** ✅
- FastAPI now serves dashboard static files (HTML, CSS, JS)
- API routes remain on /api/impact/* paths
- Static files mount ensures frontend loads correctly in iframe
- All API endpoints fully functional

## How to Run

### Step 1: Start the Backend Service
```powershell
cd "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Impact\backend"
$pythonExe = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
& $pythonExe impact_backend.py
```

### Step 2: Access the Dashboard
**Option A (Iframe in Activity Hub):**
- Navigate to http://weus42608431466:8088/activity-hub/for-you
- Click the "Projects" tab
- Dashboard will load in iframe

**Option B (Direct Access):**
- http://localhost:8002/ (local machine)
- http://weus42608431466:8002/ (remote network)

## API Endpoints

All available at `http://localhost:8002/api/impact/`:

- `GET /projects` - Get all projects with optional filters
- `GET /projects/{id}` - Get specific project
- `POST /projects` - Create new project
- `PUT /projects/{id}` - Update project
- `GET /metrics` - Get dashboard metrics
- `POST /generate-ppt` - Generate PPT report
- `GET /download/report/{id}.{pptx|pdf}` - Download generated report

## Test Data

The dashboard displays 4 test projects from BigQuery:
1. Store Network Expansion (Green/On Track)
2. Infrastructure Modernization (Yellow/At Risk)
3. Supply Chain Optimization (Red/Off Track)   
4. Workforce Development Program (Green/On Track)

## Pending Features

### Data Integration (Phase 2)
- [ ] Integrate Intake Hub projects via Data Bridge API
- [ ] Pull project data from IH_Intake_Data table
- [ ] Sync updates automatically

### PPT Generation
- Generate PPT working in theory, needs testing with actual generation

### Additional Enhancements
- [ ] "My Projects" tab/section
- [ ] Project editing/deletion
- [ ] Advanced filtering and search
- [ ] Email notifications (scheduled jobs ready)
- [ ] Export to PDF

## Important Notes

- Dashboard integration with Activity Hub: Clicking Projects tab loads dashboard in iframe
- All project data currently from AH_Projects manually-entered test data
- BigQuery credentials must be configured (`application_default_credentials.json`)
- Backend must be running for dashboard to function
- Links sidebar customizable via admin panel (future feature)

## Troubleshooting

**Dashboard not loading in Projects tab:** 
- Ensure backend is running on port 8002
- Check firewall/network access to  weus42608431466:8002

**Projects not showing:**
- Verify BigQuery table AH_Projects has data
- Check BigQuery credentials are valid
- Run `/api/impact/metrics` to test data connectivity

**Generate PPT not working:**
- Ensure python-pptx is installed
- Verify temp directory is writable
- Check network connectivity for file downloads
