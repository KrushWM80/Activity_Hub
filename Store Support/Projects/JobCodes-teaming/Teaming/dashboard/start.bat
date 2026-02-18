@echo off
echo ========================================
echo   Job Code Teaming Dashboard
echo ========================================
echo.

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "start.ps1"

pause
