@echo off
REM ==========================================
REM TDA Insights Backend - 24/7 Auto-Restart
REM ==========================================
REM Purpose: Keep TDA Insights dashboard running continuously
REM Access: http://localhost:5000/tda-initiatives-insights
REM Network: http://WEUS42608431466:5000/tda-initiatives-insights
REM Status File: tda_insights_server.log
REM
REM Features:
REM - Auto-restart on crash
REM - Logging of all starts and errors
REM - Google Cloud BigQuery integration
REM - 5-second restart interval on failure

setlocal enabledelayedexpansion

REM Define paths with variables for maintainability
set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set TDAPath=%ProjectRoot%\Store Support\Projects\TDA Insights
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%TDAPath%\tda_insights_server.log
set Port=5000

REM Set up Google Cloud credentials for BigQuery access
REM Use absolute path (not %%APPDATA%%) because SYSTEM user has a different profile
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo.
echo ================================================================
echo TDA Insights Backend - 24/7 Operating Mode
echo ================================================================
echo Access: http://localhost:%Port%/tda-initiatives-insights
echo Network: http://WEUS42608431466:%Port%/tda-initiatives-insights
echo Log File: %LogFile%
echo Time: %date% %time%
echo ================================================================
echo.

echo [%date% %time%] Starting TDA Insights backend service... >> "%LogFile%"

REM Change to TDA directory
cd /d "%TDAPath%"

REM Start Python backend with auto-restart loop
:restart_loop
echo [%date% %time%] Launching TDA Insights (backend_simple.py)... >> "%LogFile%"
echo Launching TDA Insights on port %Port%...

"%PythonExe%" backend_simple.py 2>> "%LogFile%"

REM If process exits, log it and wait before restarting
echo [%date% %time%] Process exited with code !ERRORLEVEL! >> "%LogFile%"
echo Process crashed. Restarting in 5 seconds...
timeout /t 5 /nobreak

goto restart_loop

REM Cleanup on exit
:end
echo [%date% %time%] TDA Insights service stopped >> "%LogFile%"
endlocal
