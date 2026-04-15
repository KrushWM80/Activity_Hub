@echo off
REM Quick Service Status Check
REM Shows which services are running

CD /D "%~dp0"

echo.
echo ========================================
echo Activity Hub Services - Status Report
echo ========================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "& { . '.\pid_manager.ps1' -Action status -Service all }"

echo.
