@echo off
REM ==========================================
REM TDA Insights - Weekly Email Report
REM ==========================================
REM Runs: Thursdays at 11:00 AM Central Time
REM Sends: TDA Initiative Insights email with PPT attachment via Outlook
REM ==========================================

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set TDAPath=%ProjectRoot%\Store Support\Projects\TDA Insights
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%TDAPath%\weekly_email.log

REM Use absolute path for GCP credentials
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo [%date% %time%] ====== Weekly Email Run Starting ====== >> "%LogFile%"

cd /d "%TDAPath%"

REM Run the weekly report script
echo [%date% %time%] Running send_weekly_report.py... >> "%LogFile%"
"%PythonExe%" send_weekly_report.py >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] Weekly email sent successfully >> "%LogFile%"
) else (
    echo [%date% %time%] ERROR: Weekly email failed with code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== Weekly Email Run Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"
