@echo off
REM Check Activity Hub Status & Run Health Check
REM Right-click this file and select "Run as administrator"

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

echo.
echo ================================================
echo   Activity Hub - Status Check & Health Report
echo ================================================
echo.

REM Show scheduled tasks status
echo === SCHEDULED TASKS STATUS ===
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-ScheduledTask | Where-Object {$_.TaskName -like 'Activity_Hub*'} | Select-Object TaskName, State | Format-Table"

echo.
echo === RUNNING HEALTH CHECK ===
echo.
echo This will check all services and send email report...
echo.

REM Run health check
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1"

echo.
echo ================================================
echo   Health check complete!
echo ================================================
echo.
pause
