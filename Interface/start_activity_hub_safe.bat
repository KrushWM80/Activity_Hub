@echo off
REM Safe Activity Hub Server Starter - Uses PID tracking
REM Do not use this if you have the old blanket kill scripts running

CD /D "%~dp0"
cd Interface

REM Set credentials if needed
set GOOGLE_APPLICATION_CREDENTIALS=%APPDATA%\gcloud\application_default_credentials.json

REM Call PID manager to start
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { . '..\pid_manager.ps1' -Action start -Service activity-hub }"

REM Keep window open
timeout /t 3 /nobreak
