@echo off
REM Job Codes Teaming Dashboard Backend Server - KEEP RUNNING 24/7
REM Auto-restart on crash with logging
REM Access: http://10.97.114.181:8080/static/index.html#

setlocal enabledelayedexpansion

set JOBCODES_PATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend
set PYTHON_EXE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set LOG_FILE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\jobcodes_server.log

cd /d "%JOBCODES_PATH%"

:START
echo. >> "%LOG_FILE%"
echo [%date% %time%] ===== JOB CODES SERVER START ===== >> "%LOG_FILE%"
echo [%date% %time%] Starting Job Codes Backend Server on port 8080... >> "%LOG_FILE%"
echo [%date% %time%] Access: http://10.97.114.181:8080/static/index.html# >> "%LOG_FILE%"

REM Start server and capture any errors
"%PYTHON_EXE%" main.py 2>> "%LOG_FILE%"

echo [%date% %time%] Server stopped. Checking before restart... >> "%LOG_FILE%"

REM Wait 5 seconds before restart
timeout /t 5 /nobreak

echo [%date% %time%] Restarting server... >> "%LOG_FILE%"
goto START
