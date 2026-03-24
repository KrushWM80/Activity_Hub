@echo off
cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
set PORT=8001
set ENVIRONMENT=prod
set GOOGLE_APPLICATION_CREDENTIALS=%APPDATA%\gcloud\application_default_credentials.json
:loop
echo [%date% %time%] Starting Projects in Stores server on port 8001...
"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\main.py"
echo [%date% %time%] Server crashed or stopped. Waiting 5 seconds before restart...
timeout /t 5 /nobreak
goto loop
