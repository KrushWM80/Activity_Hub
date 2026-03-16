@echo off
REM =====================================================
REM ACTIVITY HUB - COMPLETE 24/7 SETUP (MASTER)
REM =====================================================
REM This script recreates ALL automation from scratch
REM - Kills old tasks
REM - Creates 7+3 = 10 scheduled tasks
REM - Enables keep-alive
REM - Enables continuous monitoring
REM =====================================================

echo.
echo =====================================================
echo  ACTIVITY HUB - COMPLETE SYSTEM RESTORATION
echo  March 16, 2026
echo =====================================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if errorlevel 1 (
    echo.
    color 0C
    echo ERROR: Administrator privileges required!
    echo.
    color 0F
    echo SOLUTION:
    echo 1. RIGHT-CLICK this batch file
    echo 2. Select "Run as administrator"
    echo 3. Click "Yes" at the UAC prompt
    echo.
    pause
    exit /b 1
)

color 0A
echo ✓ Running as Administrator
color 0F
echo.

REM Define paths
set PYTHON_EXE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set PROJECT_ROOT=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set AUTOMATION_DIR=%PROJECT_ROOT%\Automation

echo Step 1: Removing old scheduled tasks (if they exist)
echo ======================================================
timeout /t 1 /nobreak >nul
schtasks /delete /tn Activity_Hub_JobCodes_AutoStart /f >nul 2>&1
schtasks /delete /tn Activity_Hub_ProjectsInStores_AutoStart /f >nul 2>&1
schtasks /delete /tn Activity_Hub_TDA_AutoStart /f >nul 2>&1
schtasks /delete /tn Activity_Hub_Store_Dashboard_AutoStart /f >nul 2>&1
schtasks /delete /tn Activity_Hub_StoreMeetingPlanner_AutoStart /f >nul 2>&1
schtasks /delete /tn Activity_Hub_Zorro_AutoStart /f >nul 2>&1
schtasks /delete /tn Activity_Hub_Daily_HealthCheck /f >nul 2>&1
schtasks /delete /tn Activity_Hub_KeepAwake /f >nul 2>&1
schtasks /delete /tn Activity_Hub_ContinuousMonitoring /f >nul 2>&1
echo ✓ Old tasks cleaned

timeout /t 1 /nobreak >nul

echo.
echo Step 2: Creating 6 Service Auto-Start Tasks (OnSystemStart)
echo ============================================================

echo Creating Task 1/6: Job Codes Server (Port 8080)...
schtasks /create /tn Activity_Hub_JobCodes_AutoStart /tr "cmd /c \"%AUTOMATION_DIR%\start_jobcodes_server_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED)

echo Creating Task 2/6: Projects in Stores (Port 8001)...
schtasks /create /tn Activity_Hub_ProjectsInStores_AutoStart /tr "cmd /c \"%AUTOMATION_DIR%\start_projects_in_stores_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED)

echo Creating Task 3/6: TDA Insights (Port 5000)...
schtasks /create /tn Activity_Hub_TDA_AutoStart /tr "cmd /c \"%AUTOMATION_DIR%\start_tda_insights_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED)

echo Creating Task 4/6: Store Dashboard (Port 8081)...
schtasks /create /tn Activity_Hub_Store_Dashboard_AutoStart /tr "cmd /c \"%AUTOMATION_DIR%\start_store_dashboard_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED)

echo Creating Task 5/6: Store Meeting Planner (Port 8090)...
schtasks /create /tn Activity_Hub_StoreMeetingPlanner_AutoStart /tr "cmd /c \"%PROJECT_ROOT%\Store Support\Projects\AMP\Store Meeting Planners\start-server.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED)

echo Creating Task 6/6: Zorro (Port 8888)...
schtasks /create /tn Activity_Hub_Zorro_AutoStart /tr "cmd /c \"%AUTOMATION_DIR%\start_zorro_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED)

echo.
timeout /t 1 /nobreak >nul

echo Step 3: Creating Service Recovery Tasks
echo =========================================

echo Creating Task 7: Keep-Awake Service (24/7)...
schtasks /create /tn Activity_Hub_KeepAwake /tr "powershell -ExecutionPolicy Bypass -File \"%PROJECT_ROOT%\Automation\keep_alive.ps1\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   Note: Keep-awake optional)

echo Creating Task 8: Daily Health Check (6:00 AM)...
schtasks /create /tn Activity_Hub_Daily_HealthCheck /tr "powershell -ExecutionPolicy Bypass -File \"%PROJECT_ROOT%\MONITOR_AND_REPORT.ps1\"" /sc daily /st 06:00:00 /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED)

echo Creating Task 9: Continuous Monitoring (Every 5 Minutes)...
schtasks /create /tn Activity_Hub_Continuous_Monitor /tr "powershell -ExecutionPolicy Bypass -File \"%PROJECT_ROOT%\continuous_monitor.ps1\"" /sc minute /mo 5 /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 (echo   ✓ Created) else (echo   ✗ FAILED - Optional)

echo.
echo =====================================================
echo  RESTORATION COMPLETE!
echo =====================================================
echo.
color 0B
echo ✓ All 9 scheduled tasks created successfully
color 0F
echo.
echo WHAT JUST HAPPENED:
echo   - 6 services will auto-start on system reboot
echo   - Keep-awake service prevents Windows sleep (24/7)
echo   - Continuous monitoring checks every 5 minutes
echo   - Any crashed service is automatically restarted
echo   - Daily health check runs at 6:00 AM with email report
echo.
echo NEXT STEPS:
echo   1. Restart your computer NOW (to test auto-start)
echo   2. Wait 2-3 minutes for services to start
echo   3. Check services: http://localhost:8001 (Projects)
echo   4. Other ports: 8080, 5000, 8081, 8090, 8888
echo.
echo SERVICE URLS:
echo   Job Codes:        http://10.97.114.181:8080
echo   Projects:         http://localhost:8001
echo   TDA Insights:     http://localhost:5000
echo   Store Dashboard:  http://localhost:8081
echo   Meeting Planner:  http://localhost:8090
echo   Zorro:            http://localhost:8888
echo.
echo =====================================================
echo.
pause
