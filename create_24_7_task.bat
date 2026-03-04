@echo off
REM Create Windows Task Scheduler job for 24/7 server operation
REM This script MUST be run as Administrator

echo Checking for Administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERROR: This script requires Administrator privileges!
    echo.
    echo Please right-click this .bat file and select "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo Creating scheduled task: "Projects in Stores Server 24/7"
echo.

set SCRIPTPATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat

REM Delete existing task if present
echo Removing old task if it exists...
schtasks /Delete /TN "Projects in Stores Server 24/7" /F /S localhost 2>nul

REM Create new task
echo Creating new task...
schtasks /Create ^
  /TN "Projects in Stores Server 24/7" ^
  /TR "cmd.exe /c \"%SCRIPTPATH%\"" ^
  /SC ONSTART ^
  /RL HIGHEST ^
  /F

if %errorLevel% equ 0 (
    echo.
    echo ✅ SUCCESS: Task created successfully!
    echo.
    echo Verifying task...
    schtasks /Query /TN "Projects in Stores Server 24/7" /V /FO List
) else (
    echo.
    echo ❌ ERROR: Failed to create task (Error Code: %errorLevel%)
)

echo.
pause
