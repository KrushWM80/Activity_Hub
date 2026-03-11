@echo off
title Store Meeting Planner - Server
echo ================================================
echo   Store Meeting Planner - Starting Server
echo ================================================
echo.

cd /d "%~dp0backend"

REM Check if Python is available
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found in PATH. Please install Python 3.10+.
    pause
    exit /b 1
)

REM Install requirements if needed
echo [Setup] Checking dependencies...
pip install -r requirements.txt --quiet 2>nul

echo.
echo [Server] Starting on http://localhost:8090
echo [Server] Press Ctrl+C to stop.
echo.

python main.py
pause
