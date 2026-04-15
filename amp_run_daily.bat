@echo off
REM AMP AutoFeed Daily Validation - runs at 5:00 AM
REM VB extracts emails at 4:00-4:05 AM, then this runs to validate them

setlocal enabledelayedexpansion

set PYTHON_EXE=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\platform\bundledpython\python.exe
set SCRIPT_DIR=%~dp0
set LOG_DIR=%SCRIPT_DIR%amp_validation_logs

REM Create log directory
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Log execution
echo. >> "%LOG_DIR%\daily_execution.log"
echo ====== %DATE% %TIME% ====== >> "%LOG_DIR%\daily_execution.log"

REM Run validation
echo Running AMP AutoFeed Daily Validation...
pushd "%SCRIPT_DIR%"
"%PYTHON_EXE%" amp_autofeed_validation.py >> "%LOG_DIR%\daily_execution.log" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] Daily validation completed
) else (
    echo [ERROR] Daily validation failed - see log
    echo Error code: %ERRORLEVEL% >> "%LOG_DIR%\daily_execution.log"
)

popd
endlocal
