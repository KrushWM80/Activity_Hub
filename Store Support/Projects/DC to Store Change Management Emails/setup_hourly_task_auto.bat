@echo off
REM Setup Task Scheduler to run hourly - auto version (no prompts)

echo.
echo ============================================================
echo SETTING UP HOURLY TASK SCHEDULER
echo ============================================================
echo.

REM Delete existing task if it exists
echo Removing old task...
schtasks /Delete /TN "ManagerChangeDetection" /F 2>nul

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
    echo   - Run hourly and check for VPN
    echo   - Only process each day once
    echo   - Keep trying for up to 7 days
    echo   - Send error email only after 7 days
    echo.
    schtasks /Query /TN "ManagerChangeDetection" /V /FO LIST | findstr /i "Task Status Next"
    echo.
    echo ============================================================
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
