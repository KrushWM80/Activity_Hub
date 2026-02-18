# Local Hosting Setup Guide

## Overview

The Job Code Teaming Dashboard runs as a **continuous local server** that:
- Starts automatically when you run the startup script
- Listens on `http://localhost:8080`
- Can be accessed by other computers on your network (VPN)
- Serves both frontend and backend from Python FastAPI

---

## 🚀 Quick Start (5 Minutes)

### 1. Check Requirements

```powershell
# Python must be installed
python --version

# Required packages
pip install fastapi uvicorn pandas openpyxl
```

### 2. Start the Server

**Option A: PowerShell Script**
```powershell
cd "C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard"
.\start.ps1
```

**Option B: Batch File (Simple)**
```
Double-click: start_server.bat
```

**Option C: Manual**
```powershell
cd "C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard"
python backend/main.py
```

### 3. Access Dashboard

Open browser to: **http://localhost:8080**

Login with:
- **Username**: `admin`
- **Password**: `admin123`

---

## 📐 Architecture

```
┌─────────────────────────────────────────┐
│         Your Computer                   │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │ Browser (http://localhost:8080)  │   │
│  │ - HTML/CSS/JavaScript            │   │
│  │ - Makes API calls                │   │
│  └──────────────┬───────────────────┘   │
│                 │ HTTP                  │
│  ┌──────────────▼───────────────────┐   │
│  │ FastAPI Server (Port 8080)       │   │
│  │ - Handles API requests           │   │
│  │ - Manages authentication         │   │
│  │ - Processes data                 │   │
│  └──────────────┬───────────────────┘   │
│                 │ Read/Write            │
│  ┌──────────────▼───────────────────┐   │
│  │ Data Files (JSON, CSV, Excel)    │   │
│  │ - data/users.json                │   │
│  │ - data/sessions.json             │   │
│  │ - data/update_requests.json      │   │
│  │ - TMS Data (3).xlsx              │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Data Flow

1. **Browser** sends API request (e.g., POST `/api/login`)
2. **FastAPI Server** processes request
3. **Backend** reads/writes JSON files
4. **Server** returns JSON response
5. **Browser** updates display with new data

---

## 🔧 Server Configuration

### FastAPI Main Server Code

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
import json
from datetime import datetime, timedelta

app = FastAPI()

# ============================================
# CONFIGURATION
# ============================================

PORT = 8080
HOST = "0.0.0.0"  # Allow external connections
DATA_DIR = Path(__file__).parent / "data"
FRONTEND_DIR = Path(__file__).parent / "frontend"

# ============================================
# STARTUP
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize data directory and default files"""
    DATA_DIR.mkdir(exist_ok=True)
    
    # Create default users.json if not exists
    users_file = DATA_DIR / "users.json"
    if not users_file.exists():
        default_users = {
            "admin": {
                "password": "admin123",
                "role": "admin",
                "email": "admin@example.com"
            }
        }
        with open(users_file, "w") as f:
            json.dump(default_users, f, indent=2)
    
    print(f"[OK] Dashboard ready at http://localhost:{PORT}")

# ============================================
# STATIC FILES & FRONTEND
# ============================================

# Serve static files (CSS, JS, images)
if (FRONTEND_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

# Serve main HTML on root path
@app.get("/")
async def get_root():
    return FileResponse(FRONTEND_DIR / "JobCodeTeamingDashboard.html")

@app.get("/login.html")
async def get_login():
    return FileResponse(FRONTEND_DIR / "login.html")

@app.get("/dashboard.html")
async def get_dashboard():
    return FileResponse(FRONTEND_DIR / "dashboard.html")

# ============================================
# API ROUTES
# ============================================

@app.post("/api/login")
async def login(credentials: dict):
    """User login endpoint"""
    username = credentials.get("username", "").strip()
    password = credentials.get("password", "")
    
    # Load users
    users_file = DATA_DIR / "users.json"
    with open(users_file) as f:
        users = json.load(f)
    
    # Validate credentials
    if username not in users or users[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate session token
    import secrets
    token = secrets.token_urlsafe(32)
    
    # Store session
    sessions = {}
    sessions_file = DATA_DIR / "sessions.json"
    if sessions_file.exists():
        with open(sessions_file) as f:
            sessions = json.load(f)
    
    sessions[token] = {
        "username": username,
        "role": users[username]["role"],
        "email": users[username].get("email", ""),
        "login_time": datetime.now().isoformat(),
        "expires": (datetime.now() + timedelta(hours=8)).isoformat()
    }
    
    with open(sessions_file, "w") as f:
        json.dump(sessions, f, indent=2)
    
    return {
        "success": True,
        "token": token,
        "role": users[username]["role"],
        "username": username
    }

@app.post("/api/logout")
async def logout(request: Request):
    """User logout endpoint"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    sessions_file = DATA_DIR / "sessions.json"
    if sessions_file.exists():
        with open(sessions_file) as f:
            sessions = json.load(f)
        
        if token in sessions:
            del sessions[token]
            
            with open(sessions_file, "w") as f:
                json.dump(sessions, f, indent=2)
    
    return {"success": True}

@app.get("/api/me")
async def get_current_user(request: Request):
    """Get current logged-in user info"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    
    sessions_file = DATA_DIR / "sessions.json"
    with open(sessions_file) as f:
        sessions = json.load(f)
    
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    session = sessions[token]
    
    # Check expiration
    expires = datetime.fromisoformat(session["expires"])
    if datetime.now() > expires:
        del sessions[token]
        with open(sessions_file, "w") as f:
            json.dump(sessions, f, indent=2)
        raise HTTPException(status_code=401, detail="Token expired")
    
    return session

# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    print(f"Starting Job Code Teaming Dashboard...")
    print(f"📍 Access at: http://localhost:{PORT}")
    print(f"🔑 Default login: admin / admin123")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info"
    )
```

### Startup Script (PowerShell)

```powershell
# start.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Job Code Teaming Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Python path
$pythonPath = "C:\Users\krush\.code-puppy-venv\Scripts\python.exe"

# Check Python
if (-not (Test-Path $pythonPath)) {
    Write-Host "ERROR: Python not found" -ForegroundColor Red
    exit 1
}

# Get network info
$ipv4 = Get-NetIPAddress -AddressFamily IPv4 | 
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } | 
    Select-Object -First 1

Write-Host ""
Write-Host "🌍 Network Information:" -ForegroundColor Green
Write-Host "  Local:     http://localhost:8080"
if ($ipv4) {
    Write-Host "  Network:   http://$($ipv4.IPAddress):8080"
}
Write-Host ""
Write-Host "🔑 Default Credentials:" -ForegroundColor Yellow
Write-Host "  Username: admin"
Write-Host "  Password: admin123"
Write-Host ""

# Start server
Set-Location $PSScriptRoot
& $pythonPath backend/main.py

Read-Host "Press Enter to exit"
```

---

## 🌐 Network Access (VPN/Sharing)

### Allow Other Computers to Access

By default, the server listens on `0.0.0.0:8080` which means:
- ✅ You can access locally: `http://localhost:8080`
- ✅ Other VPN users can access: `http://YOUR_IP:8080` (where YOUR_IP is your computer's IP)

### Get Your IP Address

```powershell
# Get IPv4 address (not 127.x or 169.254.x)
Get-NetIPAddress -AddressFamily IPv4 | 
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" }
```

### Windows Firewall Configuration

If others can't connect, check firewall:

```powershell
# Allow Python through firewall
New-NetFirewallRule -DisplayName "Python FastAPI" `
    -Direction Inbound `
    -Action Allow `
    -Program "C:\Users\krush\.code-puppy-venv\Scripts\python.exe"

# Or allow port 8080
New-NetFirewallRule -DisplayName "Port 8080" `
    -Direction Inbound `
    -Action Allow `
    -LocalPort 8080 `
    -Protocol TCP
```

---

## 🔍 Monitoring & Logs

### View Server Logs

```powershell
# PowerShell keeps terminal open showing:
# - Startup messages
# - API requests
# - Errors

# Example output:
# INFO:     Uvicorn running on http://0.0.0.0:8080
# INFO:     Application startup complete
# INFO:     POST /api/login - 200 OK
# INFO:     GET /api/job-codes - 200 OK
```

### Check if Server is Running

```powershell
# Test with Invoke-WebRequest
Invoke-WebRequest http://localhost:8080 -ErrorAction Ignore

# Or use curl
curl http://localhost:8080
```

---

## 🛑 Stop the Server

```powershell
# Press Ctrl+C in the terminal where server is running

# Or kill the process
Stop-Process -Name python -Force
```

---

## 🐛 Common Issues

### "Port 8080 already in use"

```powershell
# Find process using port 8080
Get-NetTCPConnection -LocalPort 8080

# Kill the process
Stop-Process -Id <PID> -Force

# Or use different port (edit main.py: PORT = 8081)
```

### "Python not found"

```powershell
# Install Python or update virtual environment path
# Check: C:\Users\krush\.code-puppy-venv\Scripts\python.exe exists

# Or run with system Python:
python backend/main.py
```

### "Module not found" (uvicorn, fastapi, etc.)

```powershell
# Install required packages
pip install fastapi uvicorn pandas openpyxl

# Or in virtual environment
C:\Users\krush\.code-puppy-venv\Scripts\pip.exe install fastapi uvicorn pandas openpyxl
```

---

## 📊 Performance Tips

1. **Keep it running** - No startup overhead once server boots
2. **Monitor disk space** - JSON files grow over time, archive old data
3. **Backup data** - Copy `data/` folder regularly
4. **Use VPN** - More secure than exposing to public internet

---

## 🎓 Key Learnings

✅ **FastAPI is lightweight** - Perfect for dashboards and small tools  
✅ **Port 8080 is common** - Easy to remember and configure  
✅ **JSON storage is simple** - No database needed for small projects  
✅ **Static + Dynamic** - Serve HTML frontend + API backend from same server  
✅ **Network access is easy** - Just open firewall and use IP address  

---

## 📚 Related Files

- Source: `C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard`
- Backend: `backend/main.py`
- Frontend: `frontend/JobCodeTeamingDashboard.html`
- Startup: `start.ps1`, `start_server.bat`
- See also: [../Local Hosting/](../../Local%20Hosting/) for other hosting methods
