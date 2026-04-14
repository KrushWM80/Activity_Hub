@echo off
REM AMP AutoFeed Validation - Setup via Batch (No Execution Policy Issues)
REM Run this as Administrator

setlocal enabledelayedexpansion

echo AMP AutoFeed Validation - One-Click Setup
echo ==========================================
echo.

REM Check if running as admin
net session >nul 2>&1
if NOT %errorLevel% == 0 (
    echo ERROR: This script must be run as Administrator
    echo.
    echo To run as admin:
    echo 1. Right-click this file: create_tasks.bat
    echo 2. Click "Run as administrator"
    pause
    exit /b 1
)

echo Step 1: Checking Python installation...
py --version >nul 2>&1
if %errorLevel% == 0 (
    for /f "tokens=2" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python !PYTHON_VERSION! found
    set PYTHON_CMD=py
) else (
    echo [ERROR] Python not found or not in PATH
    echo.
    echo Please install Python first:
    echo - Download from python.org
    echo - OR use Windows Store app "Python 3.11"
    echo - Make sure to check "Add Python to PATH" during install
    pause
    exit /b 1
)

setlocal
set SCRIPT_PATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py
set LOG_DIR=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_validation_logs

echo.
echo Step 2: Creating scheduled tasks...
echo.

REM Create daily validation task
echo Task 1: Creating daily validation (7:00 AM)...
schtasks /create /tn "AMP-AutoFeed-DailyValidation" /tr "%PYTHON_CMD% \"%SCRIPT_PATH%\" daily --log-dir \"%LOG_DIR%\"" /sc daily /st 07:00 /ru SYSTEM /f >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Daily task created
) else (
    echo [WARN] Could not create daily task (may already exist)
)

echo.

REM Create weekly report task
echo Task 2: Creating weekly CSV report (Monday 6:00 AM)...
schtasks /create /tn "AMP-AutoFeed-WeeklyReport" /tr "%PYTHON_CMD% \"%SCRIPT_PATH%\" csv-report --days 90 --log-dir \"%LOG_DIR%\"" /sc weekly /d MON /st 06:00 /ru SYSTEM /f >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Weekly task created
) else (
    echo [WARN] Could not create weekly task (may already exist)
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.

echo Next Steps:
echo ============
echo 1. Verify Outlook folder structure exists:
echo    Inbox ^> ATC ^> Reports ^> AMP ^> [Quick Base API Response Data + Auto Feed]
echo.
echo 2. (IMPORTANT) Install Python packages via corporate network:
echo    py -m pip install beautifulsoup4 pywin32 --proxy [CORPORATE_PROXY]
echo.
echo    If you have internet access from a personal device or VPN:
echo    - Install packages there, OR
echo    - Download .whl files and install locally with:
echo      py -m pip install --no-index --find-links=C:\path\to\wheels beautifulsoup4 pywin32
echo.
echo 3. Test the system:
echo    cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
echo    py amp_autofeed_orchestrator.py daily
echo.
echo 4. Verify scheduled tasks were created:
echo    schtasks /query /tn "AMP-AutoFeed-*"
echo.
echo Logs Location:
echo %LOG_DIR%
echo.

pause
