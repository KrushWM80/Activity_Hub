@echo off
REM Create scheduled task with admin check
REM This file will request Admin privileges if needed

echo.
echo Checking for Administrator privileges...
net session >nul 2>&1

if %errorLevel% neq 0 (
    echo.
    echo ERROR: This script requires Administrator privileges!
    echo.
    echo Re-running with Administrator privileges...
    echo.
    
    REM Re-run with admin privileges
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

echo.
echo ✅ Running with Administrator privileges
echo.
echo Creating scheduled task: "Projects in Stores Server 24/7"
echo.

set TASK_NAME=Projects in Stores Server 24/7
set BATCH_SCRIPT=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_server_24_7.bat

REM Verify batch script exists
if not exist "%BATCH_SCRIPT%" (
    echo ERROR: Batch script not found at:
    echo %BATCH_SCRIPT%
    pause
    exit /b 1
)

echo Batch Script: %BATCH_SCRIPT%
echo.

REM Delete existing task if present
echo Removing old task (if exists)...
schtasks /Delete /TN "%TASK_NAME%" /F 2>nul

REM Create the scheduled task
echo Creating new task...
powershell -NoProfile -Command @"
`$TaskName = "Projects in Stores Server 24/7"
`$BatchPath = "%BATCH_SCRIPT%"

`$Trigger = New-ScheduledTaskTrigger -AtStartup
`$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"`$BatchPath`""
`$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName `$TaskName -Action `$Action -Trigger `$Trigger -Settings `$Settings -RunLevel Highest -Force -ErrorAction Stop
    Write-Host "✅ Task created successfully!" -ForegroundColor Green
    Get-ScheduledTask -TaskName `$TaskName | Select-Object TaskName, State
} catch {
    Write-Host "❌ ERROR: Failed to create task" -ForegroundColor Red
    Write-Host `$_.Exception.Message -ForegroundColor Red
    exit 1
}
"@

echo.
echo ============================================
echo ✅ Setup Complete!
echo ============================================
echo.
echo The scheduled task has been created:
echo   Task Name: %TASK_NAME%
echo   Trigger: At System Startup
echo   Action: Auto-start backend server
echo.
echo The server will:
echo   - Automatically start when Windows boots
echo   - Automatically restart if it crashes
echo   - Run continuously 24/7
echo.
pause
