@echo off
REM DC Manager Change Detection - PayCycle Automation Startup
REM This batch file ensures PayCycle tasks are registered after system restart
REM Run this after system restart if PayCycle tasks are missing

setlocal enabledelayedexpansion

echo.
echo ================================
echo DC Manager - PayCycle Task Setup
echo ================================
echo.

REM Set paths
set PayCycleDir=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails
set SetupScript=%PayCycleDir%\setup_tasks_revised.ps1

REM Check if directory exists
if not exist "%PayCycleDir%" (
    echo [ERROR] PayCycle directory not found:
    echo %PayCycleDir%
    echo.
    pause
    exit /b 1
)

REM Check if setup script exists
if not exist "%SetupScript%" (
    echo [ERROR] Setup script not found:
    echo %SetupScript%
    echo.
    pause
    exit /b 1
)

echo [INFO] PayCycle directory found
echo [INFO] Setup script found
echo.
echo Launching PayCycle task setup with Admin privileges...
echo.

REM Launch PowerShell as Admin to run the setup script
powershell -Command "Start-Process powershell -ArgumentList '-NoExit -Command \"cd \"%PayCycleDir%\"; .\setup_tasks_revised.ps1\"' -Verb RunAs"

echo.
echo [INFO] Setup launched in administrator window
echo [INFO] Check the new PowerShell window for task creation status
echo.
pause
