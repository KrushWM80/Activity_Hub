@echo off
REM Create AMP AutoFeed scheduled tasks
REM MUST be run as Administrator

setlocal enabledelayedexpansion

set PYTHON_EXE=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\platform\bundledpython\python.exe
set SCRIPT_DIR=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set ORCHESTRATOR=%SCRIPT_DIR%\amp_autofeed_orchestrator.py
set LOG_DIR=%SCRIPT_DIR%\amp_validation_logs

echo.
echo ========================================
echo Creating AMP AutoFeed Scheduled Tasks
echo ========================================
echo.

REM Create Daily Validation Task
echo [1/2] Creating Daily Validation Task (5:00 AM)...
schtasks /create /tn "AMP-AutoFeed-DailyValidation" ^
  /tr "\"!SCRIPT_DIR!\amp_run_daily.bat\"" ^
  /sc daily /st 05:00 /ru "HOMEOFFICE\Dev-krush" /f

if %ERRORLEVEL% EQU 0 (
    echo   [OK] Daily task created
) else (
    echo   [ERROR] Failed to create daily task
    goto error
)

echo.

REM Create Weekly Report Task
echo [2/2] Creating Weekly CSV Report Task (Monday 6:00 AM)...
schtasks /create /tn "AMP-AutoFeed-WeeklyReport" ^
  /tr "\"!SCRIPT_DIR!\amp_run_weekly.bat\"" ^
  /sc weekly /d MON /st 06:00 /ru "HOMEOFFICE\Dev-krush" /f

if %ERRORLEVEL% EQU 0 (
    echo   [OK] Weekly task created
) else (
    echo   [ERROR] Failed to create weekly task
    goto error
)

echo.
echo ========================================
echo Tasks Created Successfully!
echo ========================================
echo.
echo Verifying tasks:
echo.
schtasks /query /tn "AMP-AutoFeed-*" /v

goto end

:error
echo.
echo ERROR: Task creation failed. Make sure this is run as Administrator.
pause
exit /b 1

:end
echo.
echo Done!
pause
