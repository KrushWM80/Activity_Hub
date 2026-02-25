@echo off
REM Start Projects in Stores Backend Server - 24/7 with auto-restart
REM This script will restart the server if it crashes

setlocal enabledelayedexpansion

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

:loop
echo [%date% %time%] Starting server...
"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\main.py"

echo [%date% %time%] Server crashed or stopped. Waiting 5 seconds before restart...
timeout /t 5 /nobreak

goto loop
