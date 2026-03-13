@echo off
REM ==========================================
REM SET UP AUTO-START SCHEDULED TASKS
REM ==========================================
REM Purpose: Create permanent Windows scheduled tasks
REM to auto-start all services on system reboot
REM and run daily health checks
REM
REM Required: Run as Administrator
REM
REM Services Auto-Start (6 total):
REM - Job Codes Dashboard (port 8080) - On system startup
REM - Projects in Stores (port 8001) - On system startup
REM - TDA Insights (port 5000) - On system startup
REM - Store Dashboard (port 8081) - On system startup
REM - Store Meeting Planner (port 8090) - On system startup
REM - Zorro (port 8888) - On system startup
REM - Health Check (email) - Daily at 6:00 AM
REM ==========================================

setlocal enabledelayedexpansion

REM Check if running as Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: This script must run as Administrator
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

echo.
echo ================================================
echo CREATING AUTO-START SCHEDULED TASKS
echo ================================================
echo.

REM Task 1: Job Codes Auto-Start on Reboot
echo Creating Task 1: Job Codes Auto-Start on Reboot...
schtasks /create /tn Activity_Hub_JobCodes_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_jobcodes_server_24_7.bat\"" /sc onstart /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo   ✓ Task created: Activity_Hub_JobCodes_AutoStart
) else (
    echo   ✗ Failed to create Job Codes task (error code: %errorlevel%)
)

REM Task 2: Projects in Stores Auto-Start on Reboot
echo Creating Task 2: Projects in Stores Auto-Start on Reboot...
schtasks /create /tn Activity_Hub_ProjectsInStores_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\ProjectsinStores\START_BACKEND.bat\"" /sc onstart /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo   ✓ Task created: Activity_Hub_ProjectsInStores_AutoStart
) else (
    echo   ✗ Failed to create Projects in Stores task (error code: %errorlevel%)
)

REM Task 3: TDA Insights Auto-Start on Reboot
echo Creating Task 3: TDA Insights Auto-Start on Reboot...
schtasks /create /tn Activity_Hub_TDA_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat\"" /sc onstart /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo   ✓ Task created: Activity_Hub_TDA_AutoStart
) else (
    echo   ✗ Failed to create TDA task (error code: %errorlevel%)
)

REM Task 4: Store Dashboard Auto-Start on Reboot
echo Creating Task 4: Store Dashboard Auto-Start on Reboot...
schtasks /create /tn Activity_Hub_Store_Dashboard_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat\"" /sc onstart /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo   ✓ Task created: Activity_Hub_Store_Dashboard_AutoStart
) else (
    echo   ✗ Failed to create Store Dashboard task (error code: %errorlevel%)
)

REM Task 5: Store Meeting Planner Auto-Start on Reboot
echo Creating Task 5: Store Meeting Planner Auto-Start on Reboot...
schtasks /create /tn Activity_Hub_StoreMeetingPlanner_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Store Meeting Planners\start-server.bat\"" /sc onstart /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo   ✓ Task created: Activity_Hub_StoreMeetingPlanner_AutoStart
) else (
    echo   ✗ Failed to create Store Meeting Planner task (error code: %errorlevel%)
)

REM Task 6: Zorro Auto-Start on Reboot
echo Creating Task 6: Zorro Auto-Start on Reboot...
schtasks /create /tn Activity_Hub_Zorro_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat\"" /sc onstart /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo   ✓ Task created: Activity_Hub_Zorro_AutoStart
) else (
    echo   ✗ Failed to create Zorro task (error code: %errorlevel%)
)

REM Task 7: Daily Health Check at 6 AM EST
echo Creating Task 7: Daily Health Check at 6:00 AM...
schtasks /create /tn Activity_Hub_Daily_HealthCheck /tr "powershell -ExecutionPolicy Bypass -File \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1\"" /sc daily /st 06:00:00 /ru SYSTEM /f
if %errorlevel% equ 0 (
    echo   ✓ Task created: Activity_Hub_Daily_HealthCheck
) else (
    echo   ✗ Failed to create Health Check task (error code: %errorlevel%)
)

echo.
echo ================================================
echo TASK SETUP COMPLETE
echo ================================================
echo.
echo The following scheduled tasks have been created:
echo.
echo 1. Activity_Hub_JobCodes_AutoStart
echo    - Starts: On system reboot
echo    - Service: Job Codes Dashboard (port 8080)
echo    - Access: http://10.97.114.181:8080/
echo.
echo 2. Activity_Hub_ProjectsInStores_AutoStart
echo    - Starts: On system reboot
echo    - Service: Projects in Stores (port 8001)
echo    - Access: http://localhost:8001/
echo.
echo 3. Activity_Hub_TDA_AutoStart
echo    - Starts: On system reboot
echo    - Service: TDA Insights (port 5000)
echo    - Access: http://localhost:5000/
echo.
echo 4. Activity_Hub_Store_Dashboard_AutoStart
echo    - Starts: On system reboot
echo    - Service: Store Dashboard (port 8081)
echo    - Access: http://localhost:8081/
echo.
echo 5. Activity_Hub_StoreMeetingPlanner_AutoStart
echo    - Starts: On system reboot
echo    - Service: Store Meeting Planner (port 8090)
echo    - Access: http://localhost:8090/
echo.
echo 6. Activity_Hub_Zorro_AutoStart
echo    - Starts: On system reboot
echo    - Service: Zorro Podcast Server (port 8888)
echo    - Access: http://localhost:8888/
echo.
echo 7. Activity_Hub_Daily_HealthCheck
echo    - Starts: Daily at 6:00 AM EST
echo    - Action: Runs MONITOR_AND_REPORT.ps1 for health check and email
echo.
echo All services will automatically start on computer reboot.
echo Daily health check will run automatically at 6 AM.
echo.
echo To verify tasks were created successfully, run:
echo   schtasks /query /tn Activity_Hub* /v
echo.
echo To manually run a task immediately, use:
echo   schtasks /run /tn Activity_Hub_JobCodes_AutoStart
echo.
pause
