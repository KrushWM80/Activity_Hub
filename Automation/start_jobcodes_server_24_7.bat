@echo off
REM Job Codes Teaming Dashboard Backend Server - KEEP RUNNING 24/7
REM Auto-restart on crash with logging
REM Access: http://10.97.114.181:8080/static/index.html#

setlocal enabledelayedexpansion

set MAIN_PATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py
set PYTHON_EXE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set LOG_FILE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\jobcodes_server.log
set "GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\application_default_credentials.json"

:START
timeout /t 2 /nobreak > nul

REM Kill any stale process on port 8080 before starting
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080.*LISTENING" 2^>nul') do (
    echo [%date% %time%] Killing stale PID %%a on port 8080 >> "%LOG_FILE%"
    taskkill /F /PID %%a > nul 2>&1
)

echo. >> "%LOG_FILE%"
echo [%date% %time%] ===== JOB CODES SERVER START ===== >> "%LOG_FILE%"
echo [%date% %time%] Starting Job Codes Backend Server on port 8080... >> "%LOG_FILE%"
echo [%date% %time%] Access: http://10.97.114.181:8080/static/index.html# >> "%LOG_FILE%"
echo [%date% %time%] GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS% >> "%LOG_FILE%"

"%PYTHON_EXE%" "%MAIN_PATH%" >> "%LOG_FILE%" 2>&1

set /a exitcode=%ERRORLEVEL%
echo [%date% %time%] Process exited with code %exitcode% >> "%LOG_FILE%"

echo [%date% %time%] Server stopped. Restarting in 5 seconds... >> "%LOG_FILE%"

REM Wait 5 seconds before restart
timeout /t 5 /nobreak

echo [%date% %time%] Restarting server... >> "%LOG_FILE%"
goto START
