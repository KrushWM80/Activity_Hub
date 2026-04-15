@echo off
REM Safe Activity Hub Server Stopper - Uses PID tracking
REM Safely stops ONLY the Activity Hub server, not other services

CD /D "%~dp0"

REM Call PID manager to stop
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { . '..\pid_manager.ps1' -Action stop -Service activity-hub }"

echo.
echo Activity Hub stopped safely.
timeout /t 2 /nobreak
