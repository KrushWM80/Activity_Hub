@echo off
REM Job Codes Teaming Dashboard Backend Server - KEEP RUNNING 24/7
REM Uses wrapper to patch main.py at runtime
REM Auto-restart on crash with logging
REM Access: http://10.97.114.181:8080/static/index.html#

setlocal enabledelayedexpansion

set WRAPPER_PATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\run_main_patched.py
set PYTHON_EXE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set LOG_FILE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\jobcodes_server.log
set "GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\application_default_credentials.json"

:START
timeout /t 2 /nobreak > nul

echo. >> "%LOG_FILE%"
echo [%date% %time%] ===== JOB CODES SERVER START (PATCHED WRAPPER) ===== >> "%LOG_FILE%"
echo [%date% %time%] Starting Job Codes Backend Server on port 8080... >> "%LOG_FILE%"
echo [%date% %time%] Access: http://10.97.114.181:8080/static/index.html# >> "%LOG_FILE%"
echo [%date% %time%] GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS% >> "%LOG_FILE%"

REM Start server using wrapper - environment variable is inherited from this batch context
"%PYTHON_EXE%" "%WRAPPER_PATH%" >> "%LOG_FILE%" 2>&1
set /a exitcode=%ERRORLEVEL%
echo [%date% %time%] Process exited with code %exitcode% >> "%LOG_FILE%"

echo [%date% %time%] Server stopped. Restarting in 5 seconds... >> "%LOG_FILE%"

REM Wait 5 seconds before restart
timeout /t 5 /nobreak

echo [%date% %time%] Restarting server... >> "%LOG_FILE%"
goto START
