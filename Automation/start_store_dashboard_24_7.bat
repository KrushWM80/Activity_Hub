@echo off
REM ==========================================
REM Store Activity & Communication Dashboard - 24/7 Auto-Restart
REM ==========================================
REM Purpose: Keep Store Dashboard running continuously
REM Access: http://localhost:8081/
REM Status File: store_dashboard_server.log
REM
REM Features:
REM - Auto-restart on crash
REM - Logging of all starts and errors
REM - Google Cloud BigQuery integration
REM - Audio synthesis via MP4 Pipeline (Jenny voice)
REM - 5-second restart interval on failure

setlocal enabledelayedexpansion

REM Define paths with variables for maintainability
set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set DashboardPath=%ProjectRoot%\Store Support\Projects\AMP\Store Updates Dashboard
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%DashboardPath%\store_dashboard_server.log
set Port=8081

REM Set up Google Cloud credentials for BigQuery access
set GOOGLE_APPLICATION_CREDENTIALS=%APPDATA%\gcloud\application_default_credentials.json

echo.
echo ================================================================
echo Store Activity & Communication Dashboard - 24/7 Operating Mode
echo ================================================================
echo Access: http://localhost:8081/
echo Log File: %LogFile%
echo Time: %date% %time%
echo ================================================================
echo.

echo [%date% %time%] Starting Store Dashboard backend service... >> "%LogFile%"

REM Change to Dashboard directory
cd /d "%DashboardPath%"

REM Start Python backend with auto-restart loop
:restart_loop
echo [%date% %time%] Launching Store Dashboard (amp_backend_server.py)... >> "%LogFile%"
echo Launching Store Dashboard on port %Port%...

"%PythonExe%" amp_backend_server.py 2>> "%LogFile%"

REM If process exits, log it and wait before restarting
echo [%date% %time%] Process exited with code !ERRORLEVEL! >> "%LogFile%"
echo Process crashed. Restarting in 5 seconds...
timeout /t 5 /nobreak

goto restart_loop

REM Cleanup on exit
:end
echo [%date% %time%] Store Dashboard service stopped >> "%LogFile%"
endlocal
