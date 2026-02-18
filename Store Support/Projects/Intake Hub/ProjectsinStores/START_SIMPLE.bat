@echo off
cls
echo.
echo ========================================
echo  Projects in Stores Dashboard
echo  Simple Startup (All in One Window)
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Server (serves both API and Frontend)...
echo.

:: Start backend (serves everything)
start /B cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8001 2>&1"

:: Wait for server to start
timeout /t 4 /nobreak >nul

echo Opening Dashboard in browser...
start http://localhost:8001/

echo.
echo ========================================
echo  Dashboard Running!
echo ========================================
echo.
echo  Main Dashboard:  http://localhost:8001/
echo  Admin Panel:     http://localhost:8001/admin.html
echo  Email Reports:   http://localhost:8001/reports.html
echo  API Docs:        http://localhost:8001/docs
echo.
echo  Press Ctrl+C to stop the server
echo.
pause
