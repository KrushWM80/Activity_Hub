@echo off
REM ==========================================
REM V.E.T. Dashboard - Daily Email Report
REM ==========================================
REM Runs: Daily at 6:00 AM Central Time
REM Sends: V.E.T. Executive Report email with PPT + PDF attachments via Outlook
REM Recipients: Kendall Rush, Matthew Farnworth, Tina Budnaitis
REM ==========================================

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set VETPath=%ProjectRoot%\Store Support\Projects\VET_Dashboard
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%VETPath%\daily_email.log

REM Use absolute path for GCP credentials
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo [%date% %time%] ====== VET Daily Email Run Starting ====== >> "%LogFile%"

cd /d "%VETPath%"

REM Run the VET report script
echo [%date% %time%] Running send_vet_report.py... >> "%LogFile%"
"%PythonExe%" send_vet_report.py >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] VET daily email sent successfully >> "%LogFile%"
) else (
    echo [%date% %time%] ERROR: VET daily email failed with code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== VET Daily Email Run Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"
