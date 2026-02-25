@echo off
REM =========================================================
REM ONE-CLICK PROJECTS IN STORES RESTART
REM Restarts all services in correct order
REM =========================================================

echo.
echo =========================================================
echo  PROJECTS IN STORES - COMPLETE RESTART
echo =========================================================
echo.

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

REM Step 1: Kill existing processes
echo [1/4] Stopping existing processes...
powershell.exe -NoProfile -Command "Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"
echo     ✓ Port 8001 cleared
echo.

REM Step 2: Start Keep-Awake (optional - runs in background)
echo [2/4] Starting Keep-Awake service...
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Minimized -Command "Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File C:\Users\krush\Documents\keep-awake.ps1' -WindowStyle Minimized"
echo     ✓ Keep-Awake started (minimized)
echo.

REM Step 3: Wait briefly for services to initialize
echo [3/4] Initializing services (waiting 2 seconds)...
timeout /t 2 /nobreak
echo     ✓ Ready
echo.

REM Step 4: Start Projects in Stores Backend
echo [4/4] Starting Projects in Stores backend on port 8001...
echo.
echo =========================================================
echo  STARTING SERVER (Ctrl+C to stop)
echo =========================================================
echo.

cd /d "Store Support\Projects\Intake Hub\ProjectsinStores\backend"
"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" main.py

REM If we get here, server was stopped
echo.
echo =========================================================
echo  SERVER STOPPED
echo =========================================================
echo Don't close this window - it will close automatically.
timeout /t 5 /nobreak
