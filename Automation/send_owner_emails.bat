@echo off
REM ============================================================================
REM Activity Hub Project Owner Email Sender
REM Scheduled to run Mondays at 6 AM (all projects) and Wednesdays at 6 AM (not updated)
REM Uses Walmart internal SMTP (smtp-gw1.homeoffice.wal-mart.com)
REM Pattern: Same as TDA Insights and VET Dashboard
REM ============================================================================

setlocal enabledelayedexpansion

REM ---- PATHS ----
set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set ScriptPath=%ProjectRoot%\Interface
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogDir=%ScriptPath%\logs
set LogFile=%LogDir%\owner_emails.log

REM Create log directory if it doesn't exist
if not exist "%LogDir%" mkdir "%LogDir%"

REM ---- ENVIRONMENT ----
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

REM ---- LOG ENTRY ----
echo. >> "%LogFile%"
echo [%date% %time%] ====== Activity Hub Owner Email Run ====== >> "%LogFile%"

REM Determine email type from parameter
set EmailType=%1
if "%EmailType%"=="" set EmailType=monday

echo [%date% %time%] Email Type: %EmailType% >> "%LogFile%"

REM ---- CHANGE TO SCRIPT DIRECTORY ----
cd /d "%ScriptPath%"
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Failed to change directory to %ScriptPath% >> "%LogFile%"
    exit /b 1
)

echo [%date% %time%] Working directory: %cd% >> "%LogFile%"

REM ---- RUN PYTHON SCRIPT ----
echo [%date% %time%] Running send_projects_owner_emails.py %EmailType% >> "%LogFile%"

"%PythonExe%" send_projects_owner_emails.py %EmailType% >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] SUCCESS: Email run completed >> "%LogFile%"
) else (
    echo [%date% %time%] ERROR: Script failed with exit code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== Activity Hub Owner Email Run Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"

endlocal
