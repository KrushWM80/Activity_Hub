@echo off
REM Start Activity Hub Server - 24/7 with auto-restart
REM Port: 8088
REM URL: http://weus42608431466:8088/activity-hub/

setlocal enabledelayedexpansion

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

:loop
echo [%date% %time%] Starting Activity Hub server on port 8088...
"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" "Interface\activity_hub_server.py"

echo [%date% %time%] Activity Hub server crashed or stopped. Waiting 5 seconds before restart...
timeout /t 5 /nobreak

goto loop
