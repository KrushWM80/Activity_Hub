# Continuous Running Server (HTTP Port)

A template for creating web servers that run continuously and serve dashboards, APIs, or web applications accessible via URL.

## When to Use This Method

✅ **Good For:**
- Dashboards accessed via web browser
- REST APIs for other systems
- Real-time data displays
- Interactive web applications
- Multi-user web tools
- Always-available services

❌ **Not Good For:**
- Scheduled reports/emails
- Background data sync
- Tasks that run once and exit
- Processes without web interfaces

---

## How It Works

```
┌─────────────────────┐
│  System Startup     │ ← Computer boots or user logs in
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Startup Script     │ ← Automatically launches server
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Web Server         │ ← FastAPI/Flask/Express running
│  (Port 8001)        │   ALWAYS RUNNING 24/7
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Users Access       │ ← Team opens http://server:8001
│  via Browser        │   Dashboard is always available
└─────────────────────┘
```

---

## Template Files

### 1. `backend/main.py` - FastAPI Server

```python
"""
FastAPI Backend Server Template
Serves web dashboard and API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# ============================================================
# CONFIGURATION
# ============================================================

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 8001       # Change if needed
DEBUG = True      # Set False in production

# ============================================================
# APP SETUP
# ============================================================

app = FastAPI(
    title="My Dashboard API",
    description="Backend server for web dashboard",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# STATIC FILES (Frontend)
# ============================================================

# Serve frontend files from ../frontend folder
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_PATH):
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    """Serve the main dashboard page"""
    index_path = os.path.join(FRONTEND_PATH, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to the API", "docs": "/docs"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "port": PORT}

@app.get("/api/data")
async def get_data():
    """Get main data for dashboard"""
    # Replace with your data fetching logic
    return {
        "items": [],
        "total": 0,
        "last_updated": "2026-01-16T12:00:00Z"
    }

@app.get("/api/data/{item_id}")
async def get_item(item_id: str):
    """Get specific item by ID"""
    # Replace with your data fetching logic
    return {"id": item_id, "name": "Sample Item"}

@app.post("/api/data")
async def create_item(item: dict):
    """Create new item"""
    # Replace with your create logic
    return {"success": True, "item": item}

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found"}
    )

@app.exception_handler(500)
async def server_error(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print(f"Starting server on http://{HOST}:{PORT}")
    print(f"Dashboard: http://localhost:{PORT}")
    print(f"API Docs: http://localhost:{PORT}/docs")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
```

### 2. `backend/start_server.ps1` - Server Startup Script

```powershell
# Start the Backend Server
# This script is called by startup shortcuts/tasks

$BackendPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Backend Server" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Directory: $BackendPath"
Write-Host "Time: $(Get-Date)"
Write-Host ""

# Change to backend directory
Set-Location $BackendPath

# Activate virtual environment if exists
$VenvPath = Join-Path $BackendPath ".venv\Scripts\Activate.ps1"
if (Test-Path $VenvPath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & $VenvPath
}

# Start the server
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host ""

python main.py
```

### 3. `backend/start_backend.bat` - Batch Alternative

```batch
@echo off
REM Start Backend Server - Called by startup shortcut

echo ============================================================
echo Starting Backend Server
echo ============================================================
echo.

cd /d "%~dp0"
echo Directory: %CD%
echo Time: %DATE% %TIME%
echo.

REM Activate virtual environment if exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Start the server
echo Starting FastAPI server...
echo.

python main.py
```

### 4. `create_startup_shortcut.ps1` - Auto-Start on Login

```powershell
# Create Startup Shortcut for Backend Server
# No Admin required - runs when YOU log in
# Run this script once to set up auto-start

# CUSTOMIZE THESE VALUES
$ProjectName = "My Dashboard"
$BackendPath = "C:\Users\krush\Documents\VSCode\YourProject\backend"
$StartScript = "start_backend.bat"
$ServerPort = 8001

# Get startup folder path
$StartupFolder = [System.Environment]::GetFolderPath('Startup')
$BatchFile = Join-Path $BackendPath $StartScript
$ShortcutPath = Join-Path $StartupFolder "$ProjectName Backend.lnk"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CREATING STARTUP SHORTCUT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project: $ProjectName"
Write-Host "Backend: $BackendPath"
Write-Host "Script:  $StartScript"
Write-Host "Port:    $ServerPort"
Write-Host ""

# Verify batch file exists
if (-not (Test-Path $BatchFile)) {
    Write-Host "ERROR: Batch file not found at $BatchFile" -ForegroundColor Red
    exit 1
}

# Create shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatchFile
$Shortcut.WorkingDirectory = $BackendPath
$Shortcut.Description = "Auto-start $ProjectName Backend Server"
$Shortcut.WindowStyle = 1  # Normal window
$Shortcut.Save()

Write-Host "============================================================" -ForegroundColor Green
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Shortcut created at:"
Write-Host "  $ShortcutPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "The server will now start automatically when you log in."
Write-Host "Access the dashboard at: http://localhost:$ServerPort" -ForegroundColor Green
Write-Host ""
Write-Host "To remove: Delete the shortcut from your Startup folder" -ForegroundColor Gray
Write-Host "  $StartupFolder" -ForegroundColor Gray
```

### 5. `setup_auto_startup.ps1` - Auto-Start on Boot (Admin Required)

```powershell
# Setup Auto-Startup for Backend Server (Admin Required)
# Runs even when NO ONE is logged in
# Run as Administrator

# CUSTOMIZE THESE VALUES
$TaskName = "MyDashboard-Backend"
$ProjectName = "My Dashboard"
$BackendPath = "C:\Users\krush\Documents\VSCode\YourProject\backend"
$StartScript = "start_server.ps1"
$ServerPort = 8001

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SETTING UP AUTO-STARTUP (ADMIN)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project:     $ProjectName"
Write-Host "Task Name:   $TaskName"
Write-Host "Backend:     $BackendPath"
Write-Host "Script:      $StartScript"
Write-Host "Port:        $ServerPort"
Write-Host ""

# Check for admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

$ScriptPath = Join-Path $BackendPath $StartScript

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$TaskName' already exists (Status: $($existingTask.State))" -ForegroundColor Yellow
    $confirm = Read-Host "Replace existing task? (Y/N)"
    if ($confirm -ne 'Y') {
        Write-Host "Cancelled." -ForegroundColor Gray
        exit 0
    }
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

try {
    # Create trigger for system startup
    $trigger = New-ScheduledTaskTrigger -AtStartup
    
    # Create action to run PowerShell script
    $action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`"" `
        -WorkingDirectory $BackendPath
    
    # Create principal (run with highest privileges)
    $principal = New-ScheduledTaskPrincipal `
        -UserId "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType S4U `
        -RunLevel Highest
    
    # Create settings
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RestartCount 3 `
        -RestartInterval (New-TimeSpan -Minutes 1)
    
    # Register the scheduled task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Trigger $trigger `
        -Action $action `
        -Principal $principal `
        -Settings $settings `
        -Description "Auto-starts $ProjectName backend server on system startup" `
        -Force
    
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name:      $TaskName"
    Write-Host "  Trigger:   At System Startup"
    Write-Host "  Script:    $ScriptPath"
    Write-Host "  Port:      $ServerPort"
    Write-Host ""
    Write-Host "The backend server will:" -ForegroundColor Yellow
    Write-Host "  - Start automatically when computer boots"
    Write-Host "  - Run even if no one is logged in"
    Write-Host "  - Auto-restart if it crashes (up to 3 times)"
    Write-Host ""
    Write-Host "Access: http://localhost:$ServerPort" -ForegroundColor Green
    Write-Host ""
    Write-Host "To remove: Unregister-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
}
catch {
    Write-Host ""
    Write-Host "ERROR: $_" -ForegroundColor Red
}
```

### 6. `frontend/index.html` - Basic Dashboard

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            background: #0071ce;
            color: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
        }
        header h1 { font-size: 24px; }
        main {
            background: white;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4caf50;
        }
        .data-section {
            margin-top: 20px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }
        .loading {
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 My Dashboard</h1>
        </header>
        <main>
            <div class="status">
                <div class="status-dot"></div>
                <span>Server Running</span>
            </div>
            
            <div class="data-section">
                <h2>Data</h2>
                <div id="data-container" class="loading">Loading...</div>
            </div>
        </main>
    </div>
    
    <script>
        async function loadData() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                
                document.getElementById('data-container').innerHTML = `
                    <p><strong>Total Items:</strong> ${data.total}</p>
                    <p><strong>Last Updated:</strong> ${data.last_updated}</p>
                `;
            } catch (error) {
                document.getElementById('data-container').innerHTML = 
                    '<p style="color: red;">Error loading data</p>';
            }
        }
        
        loadData();
    </script>
</body>
</html>
```

### 7. `requirements.txt` - Dependencies

```text
# FastAPI Web Framework
fastapi>=0.104.0
uvicorn>=0.24.0

# Optional: Database connections
# sqlalchemy>=2.0.0
# asyncpg>=0.29.0

# Optional: BigQuery
# google-cloud-bigquery>=3.13.0

# Optional: Environment variables
python-dotenv>=1.0.0

# Add your project-specific dependencies below:
```

---

## Project Structure

```
your-server-project/
├── backend/
│   ├── main.py                     # FastAPI server
│   ├── start_server.ps1            # PowerShell startup
│   ├── start_backend.bat           # Batch startup
│   ├── requirements.txt            # Python dependencies
│   └── .venv/                      # Virtual environment
├── frontend/
│   ├── index.html                  # Dashboard page
│   ├── styles.css                  # Stylesheet
│   └── app.js                      # Client JavaScript
├── create_startup_shortcut.ps1     # Auto-start on login
├── setup_auto_startup.ps1          # Auto-start on boot (admin)
└── README.md                       # Project documentation
```

---

## Setup Instructions

### Step 1: Create Your Project
1. Copy this template to your project folder
2. Customize `backend/main.py` with your API endpoints
3. Create your frontend in `frontend/` folder

### Step 2: Create Virtual Environment
```cmd
cd your-project\backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Test Manually
```cmd
cd backend
python main.py
```
Open browser to: http://localhost:8001

### Step 4: Set Up Auto-Start

**Option A: Start when YOU log in (no admin needed)**
```powershell
.\create_startup_shortcut.ps1
```

**Option B: Start when computer boots (admin required)**
```powershell
# Run as Administrator
.\setup_auto_startup.ps1
```

### Step 5: Access from Other Computers

To let others access your dashboard:
1. Find your IP: `ipconfig` → Look for IPv4 Address
2. Share the URL: `http://YOUR-IP:8001`
3. Ensure firewall allows port 8001

For VPN access:
- Your VPN IP might be different (e.g., 10.97.105.88)
- Share the VPN URL: `http://10.97.105.88:8001`

---

## Auto-Start Options Comparison

| Option | Admin Required | Runs When | Best For |
|--------|---------------|-----------|----------|
| Startup Shortcut | No | You log in | Personal machine |
| Scheduled Task (Boot) | Yes | Computer boots | Shared server |

---

## Best Practices

### 1. Use Health Check Endpoint
```python
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "uptime": get_uptime()}
```

### 2. Log Server Activity
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Server started on port 8001")
```

### 3. Handle Graceful Shutdown
```python
import signal
import sys

def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
```

### 4. Add API Documentation
FastAPI automatically provides:
- Interactive docs: `http://localhost:8001/docs`
- OpenAPI spec: `http://localhost:8001/openapi.json`

---

## Troubleshooting

### Server Won't Start
1. Check if port is already in use: `netstat -ano | findstr :8001`
2. Verify Python path and dependencies
3. Check for syntax errors in main.py

### Can't Access from Other Computers
1. Check Windows Firewall allows port 8001
2. Verify you're using correct IP address
3. Ensure both computers on same network/VPN

### Server Stops When Logged Out
Use the admin scheduled task option (`setup_auto_startup.ps1`) instead of startup shortcut.

---

## Real-World Example

See the working implementation at:
`C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores`

This project:
- FastAPI backend on port 8001
- Interactive dashboard with search, filters
- BigQuery connection for live data
- AI chat integration
- VPN-accessible at http://10.97.105.88:8001
- Auto-starts on boot via scheduled task
