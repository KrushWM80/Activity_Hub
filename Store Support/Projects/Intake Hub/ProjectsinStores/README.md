# Projects in Stores Dashboard

A comprehensive dashboard for tracking Operational Projects and store coverage with AI-powered analytics.

## Overview

This dashboard provides:
- **Real-time BigQuery Data:** 196 active projects across 4,576 stores
- **Hierarchical Navigation:** Division → Region → Market → Store drill-down
- **Sparky AI Chat:** Natural language search for projects and data analysis
- **Live Filtering:** Search by project title, division, region, market, phase
- **CSV Export:** Export data at any hierarchy level
- **Minimize/Maximize Chat:** Collapsible AI assistant

## Data Source

**Database:** `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
- **Project Source:** Operations (196 active projects)
- **Coverage:** 4,576+ stores across all divisions
- **Updates:** Real-time via BigQuery connection

## Features

### 📧 Email Reporting & Notifications
**NEW: Automated scheduled email reports**
- Create custom report configurations with filters and content types
- Schedule daily, weekly, bi-weekly, or monthly delivery
- Choose from 13 content types (Overview, Counts, New, Upcoming, Notes, Activity Feeds)
- Professional HTML emails with optional PDF attachments
- Filter by Partner, Business Organization, Store Area, Owner, Phase, and more
- Manage multiple reports with pause/resume capability
- Test reports before scheduling

**Quick Start:** See [EMAIL_REPORTING_QUICKSTART.md](EMAIL_REPORTING_QUICKSTART.md)  
**Full Guide:** See [EMAIL_REPORTING_GUIDE.md](EMAIL_REPORTING_GUIDE.md)

### Sparky AI Assistant
🤖 **Intelligent project search and data analysis:**
- Search projects by name (e.g., "Sidekick", "GMD", "DSD")
- Shows all matching projects when multiple found
- Auto-filters when single project found
- Provides breakdowns by division, phase, store count
- Minimize/maximize with − and + buttons

### Hierarchical Navigation
📊 **Multi-level drill-down:**
- **Division Level:** EAST, WEST, NORTH, SOUTHEAST, SOUTHWEST, NHM
- **Region Level:** Regional breakdowns with project counts
- **Market Level:** Market-specific projects
- **Store Level:** Individual store project assignments
- **Breadcrumbs:** Easy navigation back up the hierarchy
- **Multi-buttons:** Up to 3 buttons per level for quick access

### Filters
🔍 **Dynamic filtering:**
- Project Title (search box)
- Source (Operations/Realty)
- Division, Region, Market
- Phase (Roll/Deploy, Test, Mkt Scale, POC/POT, Complete, Pending)
- Real-time count updates when filtering

### Export
📥 **CSV export at any level:**
- Export full dataset or filtered results
- Includes all project and store details
- Timestamped filenames

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Backend:** Python 3.10+ with FastAPI
- **Database:** Google BigQuery
- **AI:** Mock intelligent responses (OpenAI integration ready)
- **Authentication:** gcloud application-default credentials

## Project Structure

```
ProjectsinStores/
├── frontend/          # React dashboard
├── backend/           # FastAPI services
├── shared/            # Shared types and utilities
├── config/            # Configuration files
└── docs/              # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Database credentials for wmt-assetprotection-prod (optional - includes mock data)
- OpenAI API key (optional - for AI assistant)

### Installation & Run

```powershell
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start the backend (IMPORTANT: Use run_server.py for Windows!)
# Option A: Using batch file (recommended - opens in new window)
.\start_server.bat

# Option B: Using PowerShell (opens new window)
Start-Process powershell -ArgumentList "-Command", "python run_server.py"

# Option C: Direct (may have signal issues in VS Code terminal)
python run_server.py

# 3. Open frontend
# Option A: Open http://localhost:8001 in browser (backend serves frontend)
# Option B: Open frontend/simple.html directly in browser
```

**Note for Windows Users:** If the server crashes when you make HTTP requests, use Option A or B above to run the server in a separate window. This avoids signal interference from the VS Code integrated terminal.

**That's it!** The dashboard works immediately with mock data.

### Configure Real Data (Optional)

```powershell
# Option 1: Use gcloud CLI (Easiest!)
gcloud auth application-default login
gcloud config set project wmt-assetprotection-prod

# Option 2: Use service account
cd backend
cp .env.example .env
notepad .env  # Add your credentials
```

See [BIGQUERY_SETUP.md](BIGQUERY_SETUP.md) for detailed BigQuery connection instructions.

## 📁 Project Structure

```
ProjectsinStores/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── database.py          # BigQuery integration
│   ├── ai_agent.py          # OpenAI integration
│   ├── models.py            # Data models
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Configuration template
│   └── test_api.py          # API test script
├── frontend/
│   └── index.html           # Single-page dashboard
├── QUICKSTART.md            # Quick start guide
├── DEPLOYMENT.md            # Deployment instructions
└── README.md                # This file
```

## 🔗 API Endpoints

### Project Data
- `GET /api/health` - Health check
- `GET /api/projects` - Get filtered projects
- `GET /api/summary` - Get summary statistics
- `GET /api/filters` - Get filter options
- `GET /api/store-counts` - Get store counts by dimension
- `POST /api/ai/query` - Query AI assistant

### Email Reports
- `GET /api/reports/configs` - List report configurations
- `GET /api/reports/configs/{id}` - Get specific configuration
- `POST /api/reports/configs` - Create report configuration
- `PUT /api/reports/configs/{id}` - Update configuration
- `DELETE /api/reports/configs/{id}` - Delete configuration
- `POST /api/reports/configs/{id}/toggle` - Enable/disable report
- `POST /api/reports/generate` - Generate report immediately
- `GET /api/reports/logs` - View execution logs
- `GET /api/reports/options` - Get configuration options

## 🎨 Dashboard Features

✅ Real-time project tracking  
✅ Interactive filters (Division, Region, Market, Phase, etc.)  
✅ Bar charts and pie charts  
✅ AI-powered natural language queries  
✅ **Automated email reports with scheduling**  
✅ **Custom report configurations**  
✅ **Professional HTML + PDF reports**  
✅ Detailed project table  
✅ Summary statistics  
✅ Responsive design  
✅ Works with mock data out-of-the-box  

## 🚢 Deploy to Code Puppy Pages

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions including:
- Code Puppy Pages integration
- Production configuration
- Security best practices
- Troubleshooting guide

## 🧪 Testing

Test the API endpoints:
```powershell
cd backend
python test_api.py
```
23, 2026 - Added Email Reporting & Notifications System
## Last Updated

January 6, 2026
