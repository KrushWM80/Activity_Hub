@echo off
REM Setup Task Scheduler to run hourly with 7-day VPN retry window

echo.
echo ============================================================
echo SETTING UP HOURLY TASK SCHEDULER
echo ============================================================
echo.
echo This will create a Task Scheduler task that:
echo   - Runs EVERY HOUR
echo   - Checks VPN connectivity
echo   - Retries for up to 7 days if VPN unavailable
echo   - Only processes each day once (when VPN becomes available)
echo.
echo Press CTRL+C to cancel, or
pause

REM Delete existing task if it exists
schtasks /Delete /TN "ManagerChangeDetection" /F 2>nul

echo.
echo Creating new hourly task...
echo.

REM Create task that runs every hour
schtasks /Create ^
    /TN "ManagerChangeDetection" ^
    /TR "cmd /c cd /d C:\Users\jhendr6\puppy\elm && python daily_check_smart.py >> daily_run_log_%%date:~10,4%%%%date:~4,2%%%%date:~7,2%%.txt 2>&1" ^
    /SC HOURLY ^
    /ST 02:00 ^
    /RU "%USERNAME%" ^
    /RL HIGHEST ^
    /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS!
    echo ============================================================
    echo.
    echo Task created: ManagerChangeDetection
    echo Schedule: Every hour starting at 2:00 AM
    echo Script: daily_check_smart.py
    echo.
    echo The task will:
    echo   1. Check if today's snapshot already exists
    echo   2. If yes: Skip (already ran successfully)
    echo   3. If no: Check VPN connectivity
    echo   4. If VPN available: Run daily check
    echo   5. If VPN unavailable: Exit and retry next hour
    echo   6. After 7 days of no VPN: Send error email
    echo.
    echo Next run: Check Task Scheduler for exact time
    echo.
) else (
    echo.
    echo ============================================================
    echo FAILED!
    echo ============================================================
    echo.
    echo Could not create task. Error code: %ERRORLEVEL%
    echo Try running this script as Administrator.
    echo.
)

pause
