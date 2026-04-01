@echo off
REM Job Codes Teaming Dashboard Backend Server - KEEP RUNNING 24/7
REM Uses inline Python patching and wrapper
REM Auto-restart on crash with logging
REM Access: http://10.97.114.181:8080/static/index.html#

setlocal enabledelayedexpansion

set MAIN_PATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py
set PYTHON_EXE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set LOG_FILE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\jobcodes_server.log
set "GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\application_default_credentials.json"

:START
timeout /t 2 /nobreak > nul

echo. >> "%LOG_FILE%"
echo [%date% %time%] ===== JOB CODES SERVER START ===== >> "%LOG_FILE%"
echo [%date% %time%] Starting Job Codes Backend Server on port 8080... >> "%LOG_FILE%"
echo [%date% %time%] Access: http://10.97.114.181:8080/static/index.html# >> "%LOG_FILE%"
echo [%date% %time%] GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS% >> "%LOG_FILE%"

REM Python inline patcher - creates patched code in memory and runs it
"%PYTHON_EXE%" -c "
import sys, os
file_path = r'%MAIN_PATH%'
try:
    with open(file_path, 'r') as f: code = f.read()
    # Patch 1: Query-level project parameter
    code = code.replace('results = client.query(query).result()', 'results = client.query(query, project=\"polaris-analytics-prod\").result()')
    # Verify patch
    if 'project=\"polaris-analytics-prod\"' in code:
        print('[PATCH] Applied query project fix')
    exec(compile(code, file_path, 'exec'), {'__name__': '__main__'})
except Exception as e:
    print(f'[ERROR] {e}')
    sys.exit(1)
" >> "%LOG_FILE%" 2>&1

set /a exitcode=%ERRORLEVEL%
echo [%date% %time%] Process exited with code %exitcode% >> "%LOG_FILE%"

echo [%date% %time%] Server stopped. Restarting in 5 seconds... >> "%LOG_FILE%"

REM Wait 5 seconds before restart
timeout /t 5 /nobreak

echo [%date% %time%] Restarting server... >> "%LOG_FILE%"
goto START
