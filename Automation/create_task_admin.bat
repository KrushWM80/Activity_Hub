@echo off
REM Setup 24/7 Auto-Start Task - Run as Administrator!
REM This batch file will be called by the scheduled task

setlocal enabledelayedexpansion

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: This script must run as Administrator!
    echo Please right-click Command Prompt and select "Run as Administrator"
    echo Then run: "%~f0"
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Creating Scheduled Task: Projects in Stores Server 24/7
echo ============================================================
echo.

REM Remove existing task first
echo Removing existing task if present...
schtasks /delete /tn "Projects in Stores Server 24/7" /f >nul 2>&1

REM Create the new task
echo Creating task at system startup...
schtasks /create /tn "Projects in Stores Server 24/7" /tr "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server.bat" /sc onstart /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo SUCCESS: Task created successfully!
    echo ============================================================
    echo.
    echo Task Details:
    echo   Name: Projects in Stores Server 24/7
    echo   Trigger: At system startup
    echo   Action: Start backend server
    echo   Privileges: Highest
    echo.
    echo The server will now start automatically when Windows boots.
    echo.
    pause
) else (
    echo.
    echo ============================================================
    echo ERROR: Failed to create task (Error: %errorlevel%)
    echo ============================================================
    echo.
    pause
    exit /b 1
)
