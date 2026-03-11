@echo off
REM Restore All Activity Hub Services - Admin Launcher
REM This batch file launches the PowerShell restoration script with Administrator privileges

echo.
echo ============================================================
echo  ACTIVITY HUB - SERVICE RESTORATION
echo  (Requires Administrator Privileges)
echo ============================================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This script requires Administrator privileges.
    echo.
    echo How to run this:
    echo   1. Right-click this batch file
    echo   2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [INFO] Running with Administrator privileges
echo.
echo Launching restoration script...
echo.

REM Get the directory of this batch file
cd /d "%~dp0"

REM Run the PowerShell restoration script
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\RESTORE_ALL_SERVICES_ADMIN.ps1"

if %errorLevel% equ 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] All services have been restored!
    echo ============================================================
    echo.
) else (
    echo.
    echo ============================================================
    echo [ERROR] Restoration encountered issues. See details above.
    echo ============================================================
    echo.
)

pause
