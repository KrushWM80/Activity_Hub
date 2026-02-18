@echo off
echo ========================================
echo Projects in Stores Dashboard
echo ========================================
echo.
echo Starting backend server...
echo.

cd /d "%~dp0backend"

if not exist ".env" (
    echo WARNING: .env file not found. Using mock data.
    echo To use real data, copy .env.example to .env and configure.
    echo.
)

python main.py

pause
