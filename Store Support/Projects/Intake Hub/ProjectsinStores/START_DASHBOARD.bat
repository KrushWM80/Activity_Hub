@echo off
cls
echo.
echo ========================================
echo  Projects in Stores Dashboard - DEV
echo  Complete Startup Script
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend Server (serves both API and Frontend)...
echo.
start "Projects in Stores DEV Server - Keep Open" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload"

echo Waiting for server to start...
timeout /t 4 /nobreak >nul

echo [2/2] Opening Dashboard in Browser...
echo.
start http://localhost:8002/
timeout /t 1 /nobreak >nul
start http://localhost:8002/admin.html

echo.
echo ========================================
echo  DEV Dashboard Started Successfully!
echo ========================================
echo.
echo  DEV Dashboard:       http://localhost:8002/
echo  DEV Admin Panel:     http://localhost:8002/admin.html
echo  DEV Email Reports:   http://localhost:8002/reports.html
echo  DEV API Docs:        http://localhost:8002/docs
echo.
echo  PRODUCTION is at:    http://127.0.0.1:8001/
echo.
echo  Keep the server window open!
echo  Press any key to close this window...
echo.
pause >nul
