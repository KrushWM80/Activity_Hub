@echo off
REM Weekly Report Generator - Windows Batch Launcher
REM Purpose: Easy one-click access to weekly report system
REM Usage: Double-click this file each Friday morning

echo.
echo ========================================
echo   Weekly Report Generator
echo   Running: %date%
echo ========================================
echo.

cd /d "c:\Users\krush\Documents\VSCode\WEEKLY_REPORT_SYSTEM"

REM Verify system is ready
if not exist "WEEKLY_CAPTURE_LOG.md" (
    echo.
    echo ERROR: WEEKLY_CAPTURE_LOG.md not found!
    echo Please run setup first.
    echo.
    pause
    exit /b 1
)

REM Show menu
:menu
echo.
echo Select an option:
echo.
echo 1 = View WEEKLY_CAPTURE_LOG (Add work items)
echo 2 = Run PRE_REPORT_CHECKLIST (Verify completeness)
echo 3 = GENERATE WEEKLY REPORT (Create report)
echo 4 = View last week's report
echo 5 = Open reports folder
echo 6 = Exit
echo.

set /p choice="Enter choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo Opening WEEKLY_CAPTURE_LOG.md...
    start notepad "WEEKLY_CAPTURE_LOG.md"
    timeout /t 2
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Opening PRE_REPORT_CHECKLIST.md...
    start notepad "PRE_REPORT_CHECKLIST.md"
    timeout /t 2
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Generating report...
    powershell -NoExit -Command ".\GENERATE_WEEKLY_REPORT.ps1"
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo Opening reports folder...
    start explorer "reports"
    timeout /t 2
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo Opening reports folder...
    start explorer "reports"
    timeout /t 2
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo Goodbye!
    exit /b 0
)

echo Invalid choice. Please try again.
goto menu
