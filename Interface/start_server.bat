@echo off
REM Activity Hub Server Startup with BigQuery Credentials
REM This script sets up Google Cloud credentials and starts Flask

cd /d "%~dp0"
setlocal enabledelayedexpansion

set GOOGLE_APPLICATION_CREDENTIALS=%APPDATA%\gcloud\application_default_credentials.json
set PYTHONDONTWRITEBYTECODE=1

echo.
echo ========================================
echo Starting Activity Hub Server
echo ========================================
echo Credentials: !GOOGLE_APPLICATION_CREDENTIALS!
echo.

"..\.venv\Scripts\python.exe" activity_hub_server.py

pause
