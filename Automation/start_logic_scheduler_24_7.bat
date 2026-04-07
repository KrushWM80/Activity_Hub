@echo off
REM Start Logic Scheduler Service - 24/7 with auto-restart
REM Port: 5011
REM Health: http://localhost:5011/health

setlocal enabledelayedexpansion

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

:loop
echo [%date% %time%] Starting Logic Scheduler Service on port 5011...
"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" "Interface\Admin\Logic\Scheduler\main.py"

echo [%date% %time%] Logic Scheduler Service crashed or stopped. Waiting 5 seconds before restart...
timeout /t 5 /nobreak

goto loop
