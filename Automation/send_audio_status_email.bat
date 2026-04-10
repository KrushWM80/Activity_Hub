@echo off
REM ==========================================
REM Audio Message Hub - Daily Status Email
REM ==========================================
REM Runs: Weekdays (Mon-Fri) at 6:00 AM Central Time
REM Sends: BQ status breakdown email to AMP partners via Outlook
REM ==========================================

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set AudioScripts=%ProjectRoot%\Store Support\Projects\AMP\Zorro\Audio\Scripts
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%AudioScripts%\daily_status_email.log

REM Use absolute path for GCP credentials
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo [%date% %time%] ====== Daily Status Email Run Starting ====== >> "%LogFile%"

cd /d "%AudioScripts%"

REM Run the daily status email script
echo [%date% %time%] Running send_daily_status_email.py... >> "%LogFile%"
"%PythonExe%" send_daily_status_email.py >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] Daily status email sent successfully >> "%LogFile%"
) else (
    echo [%date% %time%] ERROR: Daily status email failed with code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== Daily Status Email Run Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"
