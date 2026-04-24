@echo off
REM ==========================================
REM Friday 10:30 AM Outstanding Items Alert
REM ==========================================
REM Runs: Fridays at 10:30 AM
REM Checks BQ for messages missing Summarized text.
REM Only sends email if there are outstanding items.
REM ==========================================

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set AudioScripts=%ProjectRoot%\Store Support\Projects\AMP\Zorro\Audio\Scripts
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%AudioScripts%\daily_status_email.log

REM Use absolute path for GCP credentials
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo [%date% %time%] ====== Friday Outstanding Alert Starting ====== >> "%LogFile%"

cd /d "%AudioScripts%"

echo [%date% %time%] Running send_friday_outstanding_alert.py... >> "%LogFile%"
"%PythonExe%" send_friday_outstanding_alert.py >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] Outstanding alert completed successfully >> "%LogFile%"
) else (
    echo [%date% %time%] Outstanding alert finished with code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== Friday Outstanding Alert Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"
