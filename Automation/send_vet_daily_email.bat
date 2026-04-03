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

REM --- Ensure VET backend (port 5001) is running before generating report ---
echo [%date% %time%] Checking VET backend on port 5001... >> "%LogFile%"
netstat -ano | findstr ":5001 " | findstr "LISTENING" > nul 2>&1
if %errorlevel% neq 0 (
    echo [%date% %time%] Backend not running - starting it now... >> "%LogFile%"
    start /b "" cmd /c "%ProjectRoot%\Automation\start_vet_dashboard_24_7.bat" > nul 2>&1
    REM Wait up to 30 seconds for port 5001 to come up
    set /a attempts=0
    :wait_vet
    timeout /t 3 /nobreak > nul
    netstat -ano | findstr ":5001 " | findstr "LISTENING" > nul 2>&1
    if %errorlevel% equ 0 goto vet_ready
    set /a attempts+=1
    if !attempts! lss 10 goto wait_vet
    echo [%date% %time%] WARNING: Backend did not start in 30s - report may use fallback data >> "%LogFile%"
    goto run_report
    :vet_ready
    echo [%date% %time%] Backend confirmed running on port 5001 >> "%LogFile%"
) else (
    echo [%date% %time%] Backend already running on port 5001 >> "%LogFile%"
)

:run_report
cd /d "%VETPath%"

REM Run the VET report script
echo [%date% %time%] Running send_vet_report_final.py... >> "%LogFile%"
"%PythonExe%" send_vet_report_final.py >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] VET daily email sent successfully >> "%LogFile%"
) else (
    echo [%date% %time%] ERROR: VET daily email failed with code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== VET Daily Email Run Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"
