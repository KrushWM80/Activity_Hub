@echo off
REM Safe Multi-Service Starter - Uses PID tracking
REM Starts all Activity Hub services without blanket killing

setlocal enabledelayedexpansion

CD /D "%~dp0"

echo.
echo ========================================
echo Starting All Activity Hub Services...
echo ========================================
echo.

REM Call PID manager to start all services
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { . '.\pid_manager.ps1' -Action start -Service all }"

echo.
echo ========================================
echo Starting Service Status Check...
echo ========================================
echo.

timeout /t 3

powershell -NoProfile -ExecutionPolicy Bypass -Command "& { . '.\pid_manager.ps1' -Action status -Service all }"

echo.
echo All services started. Check ports:
echo   - Activity Hub:      http://localhost:8088
echo   - Job Codes:         http://localhost:8080
echo   - Projects in Stores: http://localhost:8001
echo   - AMP Dashboard:     http://localhost:8081
echo   - V.E.T. Dashboard:  http://localhost:5001
echo.
