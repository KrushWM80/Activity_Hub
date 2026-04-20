@echo off
REM ==========================================
REM Dallas Team Report Backend - 24/7 Auto-Restart
REM ==========================================
REM Purpose: Keep Dallas Team Report Dashboard running continuously
REM Access:  http://localhost:5001/Dallas_Team_Report
REM Network: http://WEUS42608431466:5001/Dallas_Team_Report
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
echo  Dallas Team Report - 24/7 Auto-Restart Service
echo  Port: %Port%
echo  Log:  %LogFile%
echo ================================================================
echo.

:restart_loop
REM --- Kill any stale process holding the port before starting ---
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":%Port% " ^| findstr "LISTENING"') do (
    echo [%date% %time%] Killing stale PID %%a on port %Port%... >> "%LogFile%"
    echo [%date% %time%] Killing stale PID %%a on port %Port%...
    taskkill /F /PID %%a > nul 2>&1
)
timeout /t 2 /nobreak > nul

echo [%date% %time%] Starting Dallas Team Report on port %Port%... >> "%LogFile%"
echo [%date% %time%] Starting Dallas Team Report...

cd /d "%VETPath%"
"%PythonExe%" start_server.py >> "%LogFile%" 2>&1

echo [%date% %time%] Dallas Team Report stopped. Restarting in 5 seconds... >> "%LogFile%"
echo [%date% %time%] Restarting in 5 seconds...
timeout /t 5 /nobreak > nul
goto restart_loop
