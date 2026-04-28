@echo off
REM Daily Batch Update - Sync projects with hierarchy data
REM Scheduled: Daily at 5:00 AM (after hierarchy sync runs at same time)

setlocal enabledelayedexpansion
cd /d "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

REM Log file
set "LOG_FILE=logs\batch_update_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log"

echo. >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"
echo Batch Update Started: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

REM Run the batch update script
".venv\Scripts\python.exe" batch_update_daily.py >> "%LOG_FILE%" 2>&1

echo Batch Update Completed: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

exit /b 0
