@echo off
REM TDA Insights Dashboard - Quick Start Script
REM This script starts the backend and opens the dashboard

setlocal enabledelayedexpansion

echo.
echo ======================================
echo TDA Insights Dashboard - Starting Up
echo ======================================
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0

REM Check if we're in the right place
if not exist "%SCRIPT_DIR%backend.py" (
    echo ERROR: backend.py not found in current directory
    echo Please run this script from the TDA Insights folder
    exit /b 1
)

REM Check Python - try multiple locations
echo Checking Python installation...

REM Try venv Python first (most reliable)
set PYTHON_EXE=
if exist "%SCRIPT_DIR%..\..\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%SCRIPT_DIR%..\..\.venv\Scripts\python.exe"
    echo Found Python in venv: !PYTHON_EXE!
) else if exist "C:\Users\krush\AppData\Local\Python\bin\python.exe" (
    set "PYTHON_EXE=C:\Users\krush\AppData\Local\Python\bin\python.exe"
    echo Found Python in AppData: !PYTHON_EXE!
) else (
    for /f "delims=" %%i in ('where python 2^>nul') do set "PYTHON_EXE=%%i"
    if defined PYTHON_EXE (
        echo Found Python in PATH: !PYTHON_EXE!
    )
)

if not defined PYTHON_EXE (
    echo ERROR: Python is not installed or not found
    echo.
    echo Please try one of:
    echo 1. Install Python 3.8+ from https://www.python.org/
    echo 2. Run .\START.ps1 instead of START.bat
    echo.
    pause
    exit /b 1
)

!PYTHON_EXE! --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python version check failed
    pause
    exit /b 1
)

REM Determine which backend to use
echo Checking available backends...
if exist "%SCRIPT_DIR%backend_simple.py" (
    echo Using lightweight backend (no dependencies required)
    set BACKEND=backend_simple.py
) else (
    echo Checking dependencies for full-featured backend...
    !PYTHON_EXE! -c "import flask" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Flask not installed. Using lightweight backend...
        echo.
        echo To upgrade to full features with BigQuery and PowerPoint:
        echo   python -m pip install -r requirements.txt
        echo.
        set BACKEND=backend_simple.py
    ) else (
        echo Flask is installed. Using full-featured backend...
        set BACKEND=backend.py
    )
)

REM Start backend in a new window
echo Starting TDA Insights Backend...
start "TDA Backend" cmd /k "cd /d "%SCRIPT_DIR%" && !PYTHON_EXE! !BACKEND!"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 3 /nobreak

REM Open dashboard
echo Opening TDA Insights Dashboard...
start http://localhost:5000/dashboard.html

REM Wait a moment and show status
timeout /t 2 /nobreak

echo.
echo ======================================
echo ✅ TDA Insights Dashboard Started!
echo ======================================
echo.
echo Backend URL: http://localhost:5000
echo Dashboard: http://localhost:5000/dashboard.html
echo.
echo API Endpoints:
echo   GET http://localhost:5000/api/health          - Health check
echo   GET http://localhost:5000/api/data            - Get TDA data
echo   GET http://localhost:5000/api/phases          - Get phases
echo   GET http://localhost:5000/api/health-statuses - Get statuses
echo   POST http://localhost:5000/api/ppt/generate   - Generate PPT
echo.
echo To stop the backend: Close the backend window or press Ctrl+C
echo.
pause
