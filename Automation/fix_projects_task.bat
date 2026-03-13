@echo off
REM Fix Projects in Stores Scheduled Task - MUST RUN AS ADMIN

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

echo.
echo ================================================
echo   Fixing Projects in Stores Task
echo ================================================
echo.

echo Deleting old (incorrect) task...
schtasks /delete /tn Activity_Hub_ProjectsInStores_AutoStart /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Deleted old task

timeout /t 1 /nobreak >nul

echo Creating new (correct) task...
schtasks /create /tn Activity_Hub_ProjectsInStores_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_projects_in_stores_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
if %errorlevel% equ 0 echo   ✓ Created corrected task with proper batch file

echo.
echo ================================================
echo   Task Fixed!
echo ================================================
echo.
echo The Projects in Stores service will now:
echo - Use the PRODUCTION batch file (not DEV)
echo - Execute with full Python path (SYSTEM user compatible)
echo - Auto-restart on crash with 5-second delay
echo - Log all activity
echo.
echo Access: http://localhost:8001/
echo When system reboots, task will auto-start the service!
echo.
pause
