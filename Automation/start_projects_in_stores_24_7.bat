@echo off
cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
set PORT=8001
set ENVIRONMENT=prod
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json
:loop
REM --- Kill any stale process holding the port before starting ---
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8001 " ^| findstr "LISTENING"') do (
    echo [%date% %time%] Killing stale PID %%a on port 8001...
    taskkill /F /PID %%a > nul 2>&1
)
timeout /t 2 /nobreak > nul

echo [%date% %time%] Starting Projects in Stores server on port 8001...
"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\main.py"
echo [%date% %time%] Server crashed or stopped. Waiting 5 seconds before restart...
timeout /t 5 /nobreak
goto loop
