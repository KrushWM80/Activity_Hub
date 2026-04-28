@echo off
REM Pricing Operations Callouts - Weekly Email Task
REM Scheduled to run Friday 4:00 PM CT
REM Sends callouts email with Tableau screenshot

setlocal enabledelayedexpansion

REM Set working directory
cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Pricing\Callouts"

REM Set Python environment
set PYTHONPATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

REM Get Python executable from venv
set PYTHON_EXE="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"

REM Log file
set LOG_FILE=logs\task_scheduler.log
echo. >> %LOG_FILE%
echo ================================================================================ >> %LOG_FILE%
echo [%date% %time%] Pricing Callouts Email Task Started >> %LOG_FILE%
echo ================================================================================ >> %LOG_FILE%

REM Check if Python executable exists
if not exist %PYTHON_EXE% (
    echo [%date% %time%] ERROR: Python not found at %PYTHON_EXE% >> %LOG_FILE%
    exit /b 1
)

REM Check if Google credentials exist
if not exist "%GOOGLE_APPLICATION_CREDENTIALS%" (
    echo [%date% %time%] ERROR: Google credentials not found >> %LOG_FILE%
    exit /b 1
)

REM Run email sender
echo [%date% %time%] Executing email sender... >> %LOG_FILE%
%PYTHON_EXE% send_pricing_callouts_email.py >> %LOG_FILE% 2>&1

if %ERRORLEVEL% equ 0 (
    echo [%date% %time%] SUCCESS: Email task completed >> %LOG_FILE%
) else (
    echo [%date% %time%] ERROR: Email task failed with exit code %ERRORLEVEL% >> %LOG_FILE%
)

echo [%date% %time%] Task ended >> %LOG_FILE%
echo. >> %LOG_FILE%

endlocal
exit /b %ERRORLEVEL%
