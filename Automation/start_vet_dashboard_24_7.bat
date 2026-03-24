@echo off
REM ==========================================
REM V.E.T. Dashboard Backend - 24/7 Auto-Restart
REM ==========================================
REM Purpose: Keep V.E.T. (Vendor/Executive/Tracking) Dashboard running continuously
REM Access:  http://localhost:5001/vet_dashboard.html
REM Network: http://WEUS42608431466:5001/vet_dashboard.html
REM Log:     Store Support/Projects/VET_Dashboard/vet_dashboard_server.log
REM
REM Features:
REM - Auto-restart on crash (5-second interval)
REM - BigQuery integration (TDA Report data)
REM - Flask backend on port 5001

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set VETPath=%ProjectRoot%\Store Support\Projects\VET_Dashboard
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%VETPath%\vet_dashboard_server.log
set Port=5001

set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo.
echo ================================================================
echo  V.E.T. Dashboard - 24/7 Auto-Restart Service
echo  Port: %Port%
echo  Log:  %LogFile%
echo ================================================================
echo.

:restart_loop
echo [%date% %time%] Starting V.E.T. Dashboard on port %Port%... >> "%LogFile%"
echo [%date% %time%] Starting V.E.T. Dashboard...

cd /d "%VETPath%"
"%PythonExe%" backend.py >> "%LogFile%" 2>&1

echo [%date% %time%] V.E.T. Dashboard stopped. Restarting in 5 seconds... >> "%LogFile%"
echo [%date% %time%] Restarting in 5 seconds...
timeout /t 5 /nobreak > nul
goto restart_loop
