@echo off
REM ==========================================
REM Store Meeting Planner Backend - 24/7 Auto-Restart
REM ==========================================
REM Purpose: Keep Store Meeting Planner backend running continuously
REM Access:  http://localhost:8090/
REM Network: http://WEUS42608431466:8090/
REM Log:     Store Support/Projects/AMP/Store Meeting Planners/backend/meeting_planner_server.log
REM
REM Features:
REM - Auto-restart on crash (5-second interval)
REM - BigQuery + AMP data integration
REM - FastAPI backend on port 8090

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set PlannerPath=%ProjectRoot%\Store Support\Projects\AMP\Store Meeting Planners\backend
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%PlannerPath%\meeting_planner_server.log
set Port=8090

set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo.
echo ================================================================
echo  Store Meeting Planner - 24/7 Auto-Restart Service
echo  Port: %Port%
echo  Log:  %LogFile%
echo ================================================================
echo.

:restart_loop
echo [%date% %time%] Starting Store Meeting Planner on port %Port%... >> "%LogFile%"
echo [%date% %time%] Starting Store Meeting Planner...

cd /d "%PlannerPath%"
"%PythonExe%" main.py >> "%LogFile%" 2>&1

echo [%date% %time%] Store Meeting Planner stopped. Restarting in 5 seconds... >> "%LogFile%"
echo [%date% %time%] Restarting in 5 seconds...
timeout /t 5 /nobreak > nul
goto restart_loop
