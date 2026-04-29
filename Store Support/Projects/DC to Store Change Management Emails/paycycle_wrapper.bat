@echo off
REM PayCycle Email Wrapper
REM This batch file is called by Task Scheduler and runs the generic Python script
REM Usage: paycycle_wrapper.bat PAYCYCLE_NUMBER

setlocal enabledelayedexpansion

set PC_NUMBER=%1
if "%PC_NUMBER%"=="" (
    echo [ERROR] PayCycle number not provided
    exit /b 1
)

set PYTHON_EXE=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set SCRIPT_PATH=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\send_paycycle_production_email_generic.py
set WORK_DIR=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails

cd /d "%WORK_DIR%"

"%PYTHON_EXE%" "%SCRIPT_PATH%" %PC_NUMBER%

exit /b %ERRORLEVEL%
