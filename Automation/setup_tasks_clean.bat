@echo off
REM SETUP AUTO-START TASKS
REM This script creates Windows scheduled tasks for Activity Hub services
REM IMPORTANT: Must be run as Administrator!

echo.
echo ================================================
echo   Activity Hub - Auto-Start Setup
echo   Creating 7 Scheduled Tasks
echo ================================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: Administrator privileges required!
    echo.
    echo Please:
    echo 1. Right-click this batch file
    echo 2. Select "Run as administrator"
    echo 3. Click "Yes" at the prompt
    echo.
    pause
    exit /b 1
)

echo ✓ Running as Administrator
echo.

REM Task 1: Job Codes
echo Creating Task 1 of 7: Job Codes Auto-Start...
schtasks /create /tn Activity_Hub_JobCodes_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_jobcodes_server_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created

REM Task 2: Projects in Stores
echo Creating Task 2 of 7: Projects in Stores Auto-Start...
schtasks /create /tn Activity_Hub_ProjectsInStores_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_projects_in_stores_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created

REM Task 3: TDA Insights
echo Creating Task 3 of 7: TDA Insights Auto-Start...
schtasks /create /tn Activity_Hub_TDA_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created

REM Task 4: Store Dashboard
echo Creating Task 4 of 7: Store Dashboard Auto-Start...
schtasks /create /tn Activity_Hub_Store_Dashboard_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created

REM Task 5: Store Meeting Planner
echo Creating Task 5 of 7: Store Meeting Planner Auto-Start...
schtasks /create /tn Activity_Hub_StoreMeetingPlanner_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_meeting_planner_24_7.bat\"" /sc onlogon /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created

REM Task 6: Zorro
echo Creating Task 6 of 7: Zorro Auto-Start...
schtasks /create /tn Activity_Hub_Zorro_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created

REM Task 7: Daily Health Check
echo Creating Task 7 of 7: Daily Health Check at 6 AM...
schtasks /create /tn Activity_Hub_Daily_HealthCheck /tr "powershell -ExecutionPolicy Bypass -File \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1\"" /sc daily /st 06:00:00 /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created

echo.
echo ================================================
echo   All Tasks Created!
echo ================================================
echo.
echo Your Activity Hub services will now auto-start on reboot.
echo.
pause
