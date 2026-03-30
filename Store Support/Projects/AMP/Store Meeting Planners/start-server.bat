@echo off
title Store Meeting Planner - Server
echo ================================================
echo   Store Meeting Planner - Starting Server
echo ================================================
echo.

cd /d "%~dp0backend"

REM Define Python executable path
set PYTHON_EXE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe
set PROJECT_ROOT=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub

REM Check if Python exists
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found at %PYTHON_EXE%
    pause
    exit /b 1
)

REM Set Google Cloud credentials for BigQuery
set GOOGLE_APPLICATION_CREDENTIALS=%APPDATA%\gcloud\application_default_credentials.json

REM Install requirements if needed
echo [Setup] Checking dependencies...
"%PYTHON_EXE%" -m pip install -r requirements.txt --quiet 2>nul

echo.
echo [Server] Starting on http://localhost:8090/StoreMeetingPlanner
echo [Server] Press Ctrl+C to stop.
echo.

REM Run the server
"%PYTHON_EXE%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server failed to start. Check the error above.
    pause
)

