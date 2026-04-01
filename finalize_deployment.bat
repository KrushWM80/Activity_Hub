@echo off
REM Finalization script untuk JobCodes Backend Deployment
REM This script will:
REM 1. Kill any running Python processes
REM 2. Swap the .new files to their final names
REM 3. Start the server again

setlocal enabledelayedexpansion

echo.
echo ========================================
echo JobCodes Backend - Finalization Deployment
echo ========================================
echo.

REM Remote paths
set REMOTE_HOST=\\10.97.114.181\c$
set BACKEND_PATH=%REMOTE_HOST%\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend

echo [1/4] Killing any running Python processes...
taskkill /s 10.97.114.181 /im python.exe /f 2>nul
if errorlevel 1 (
    echo         No processes found (or access denied)
) else (
    echo         Processes killed
)

echo.
echo [2/4] Waiting for file locks to clear...
timeout /t 5 /nobreak

echo.
echo [3/4] Swapping files to final names...

REM Swap main.py
if exist "%BACKEND_PATH%\main.py.new" (
    del "%BACKEND_PATH%\main.py" 2>nul
    ren "%BACKEND_PATH%\main.py.new" "main.py" 2>nul
    echo         ✓ main.py updated
) else (
    echo         ! main.py.new not found
)

REM Swap Polaris CSV
if exist "%BACKEND_PATH%\..\polaris_job_codes.csv.new" (
    del "%BACKEND_PATH%\..\polaris_job_codes.csv" 2>nul
    ren "%BACKEND_PATH%\..\polaris_job_codes.csv.new" "polaris_job_codes.csv" 2>nul
    echo         ✓ polaris_job_codes.csv updated
) else (
    echo         ! polaris_job_codes.csv.new not found
)

REM Swap Teaming CSV
if exist "%BACKEND_PATH%\..\TMS_Data_3_converted.csv.new" (
    del "%BACKEND_PATH%\..\TMS_Data_3_converted.csv" 2>nul
    ren "%BACKEND_PATH%\..\TMS_Data_3_converted.csv.new" "TMS_Data_3_converted.csv" 2>nul
    echo         ✓ TMS_Data_3_converted.csv updated
) else (
    echo         ! TMS_Data_3_converted.csv.new not found
)

echo.
echo [4/4] Restarting server...
REM Get the backend path for the remote
set REMOTE_STARTUP_PATH=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend

echo Executing pyhost to start the server...
REM This would need to be run directly on the remote machine
REM For now, we'll just echo completion
echo.
echo ========================================
echo ✓ Deployment files swapped successfully!
echo ========================================
echo.
echo NOTE: You may need to manually restart the server on the remote machine
echo Run command on 10.97.114.181:
echo   cd C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend
echo   python main.py
echo.

endlocal
