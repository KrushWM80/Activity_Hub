@echo off
REM This batch file elevates to admin and runs the PowerShell script to create the scheduled task
REM Right-click and select "Run as Administrator"

echo.
echo Checking for Administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERROR: This script requires Administrator privileges!
    echo.
    echo Please right-click this .bat file and select "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo Running task creation script with Administrator privileges...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\CreateScheduledTask_Admin.ps1"

pause
