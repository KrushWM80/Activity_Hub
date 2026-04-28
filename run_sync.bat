@echo off
REM AH_Projects Sync Runner
REM Called by Windows Task Scheduler every 30 minutes

cd /d "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" sync_now.py
