@echo off
REM Hierarchy Sync Task - runs sync_hierarchy_simple.py
REM Scheduled to run daily at 5:00 AM

cd /d "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" sync_hierarchy_simple.py >> logs\hierarchy_sync.log 2>&1

exit /b %errorlevel%
