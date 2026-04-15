@echo off
REM Safe Multi-Service Stopper - Uses PID tracking
REM Stops all Activity Hub services safely (not other platforms)

CD /D "%~dp0"

echo.
echo ========================================
echo Stopping All Activity Hub Services...
echo ========================================
echo.

REM Call PID manager to stop all services
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { . '.\pid_manager.ps1' -Action stop -Service all }"

echo.
echo ========================================
echo Verifying Status...
echo ========================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "& { . '.\pid_manager.ps1' -Action status -Service all }"

echo.
echo All Activity Hub services stopped safely.
timeout /t 2 /nobreak
