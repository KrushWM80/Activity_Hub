@echo off
REM Daily Snapshot Generator Wrapper
REM Runs daily_check_smart.py to generate manager snapshots
REM Called by Task Scheduler every day at 5:00 AM

setlocal enabledelayedexpansion

set PYTHON_EXE=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set SCRIPT_PATH=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\daily_check_smart.py
set WORK_DIR=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails

cd /d "%WORK_DIR%"

"%PYTHON_EXE%" "%SCRIPT_PATH%"

exit /b %ERRORLEVEL%
