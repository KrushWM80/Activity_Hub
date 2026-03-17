@echo off
REM Fix missing Projects in Stores scheduled task
REM Must run as Administrator

net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: Must run as Administrator!
    pause
    exit /b 1
)

echo Creating Activity_Hub_ProjectsInStores_AutoStart task...
schtasks /create /tn Activity_Hub_ProjectsInStores_AutoStart /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_projects_in_stores_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1

if %errorlevel% equ 0 (
    echo ✓ Task created successfully!
    echo.
    echo You must restart the computer for the task to run.
    echo OR manually run this batch file:
    echo   C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_projects_in_stores_24_7.bat
) else (
    echo ✗ Task creation failed
)

pause
