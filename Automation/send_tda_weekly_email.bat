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

REM --- Ensure TDA backend (port 5000) is running before generating report ---
echo [%date% %time%] Checking TDA backend on port 5000... >> "%LogFile%"
netstat -ano | findstr ":5000 " | findstr "LISTENING" > nul 2>&1
if %errorlevel% neq 0 (
    echo [%date% %time%] Backend not running - starting it now... >> "%LogFile%"
    start /b "" cmd /c "%ProjectRoot%\Automation\start_tda_insights_24_7.bat" > nul 2>&1
    REM Wait up to 30 seconds for port 5000 to come up
    set /a attempts=0
    :wait_tda
    timeout /t 3 /nobreak > nul
    netstat -ano | findstr ":5000 " | findstr "LISTENING" > nul 2>&1
    if %errorlevel% equ 0 goto tda_ready
    set /a attempts+=1
    if !attempts! lss 10 goto wait_tda
    echo [%date% %time%] WARNING: Backend did not start in 30s - report may use fallback data >> "%LogFile%"
    goto run_report
    :tda_ready
    echo [%date% %time%] Backend confirmed running on port 5000 >> "%LogFile%"
) else (
    echo [%date% %time%] Backend already running on port 5000 >> "%LogFile%"
)

:run_report
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
