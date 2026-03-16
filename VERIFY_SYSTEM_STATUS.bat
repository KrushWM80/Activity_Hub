@echo off
REM Activity Hub - System Verification Script
REM Checks if all services are working correctly

color 0F
echo.
echo =====================================================
echo  ACTIVITY HUB - System Verification
echo  %date% %time%
echo =====================================================
echo.

REM Check scheduled tasks
echo CHECKING SCHEDULED TASKS...
echo ============================
echo.

set TASKS_FOUND=0

for %%t in (JobCodes ProjectsInStores TDA Store_Dashboard StoreMeetingPlanner Zorro KeepAwake Daily_HealthCheck Continuous_Monitor) do (
    schtasks /query /tn Activity_Hub_%%t >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✓ Activity_Hub_%%t found
        set /a TASKS_FOUND+=1
    ) else (
        echo ✗ Activity_Hub_%%t MISSING
    )
)

echo.
echo Found %TASKS_FOUND% of 9 tasks
echo.

REM Check running services
echo CHECKING RUNNING SERVICES...
echo ============================
echo.

setlocal enabledelayedexpansion

set PORTS=8080 8001 5000 8081 8090 8888
set SERVICES=JobCodes ProjectsInStores TDAInsights StoreDashboard MeetingPlanner Zorro
set URLS=10.97.114.181:8080 localhost:8001 localhost:5000 localhost:8081 localhost:8090 localhost:8888

set /a idx=0
for %%p in (%PORTS%) do (
    set /a idx+=1
    netstat -ano 2>nul | findstr ":%%p.*LISTENING" >nul
    if !errorlevel! equ 0 (
        echo ✓ Port %%p LISTENING
    ) else (
        echo ✗ Port %%p NOT LISTENING
    )
)

echo.

REM Check Python processes
echo CHECKING PYTHON PROCESSES...
echo ============================
echo.

tasklist /FI "IMAGENAME eq python.exe" 2>nul | findstr python >nul
if %errorlevel% equ 0 (
    echo ✓ Python processes running
    tasklist /FI "IMAGENAME eq python.exe"
    echo.
) else (
    echo ✗ NO PYTHON PROCESSES - Services cannot be running!
    echo.
)

REM Summary
echo =====================================================
echo  SUMMARY
echo =====================================================
echo.

if %TASKS_FOUND% equ 9 (
    color 0A
    echo ✓ All scheduled tasks present
    color 0F
) else (
    color 0C
    echo ✗ Only %TASKS_FOUND%/9 tasks found - Need to run MASTER_SETUP_24_7.bat as Admin
    color 0F
)

echo.
echo SERVICE ACCESS URLS:
echo   - JobCodes:        http://10.97.114.181:8080
echo   - Projects:         http://localhost:8001
echo   - TDA Insights:     http://localhost:5000
echo   - Store Dashboard:  http://localhost:8081
echo   - Meeting Planner:  http://localhost:8090
echo   - Zorro:            http://localhost:8888
echo.

echo ACTION ITEMS:
echo   1. If tasks are missing: Run MASTER_SETUP_24_7.bat as Administrator
echo   2. If services not running: Check that Python processes are active
echo   3. If Python down: Restart computer (triggers auto-start)
echo   4. Check logs in: Activity_Hub folder for detailed diagnostics
echo.

pause
