@echo off
echo.
echo ========================================
echo  Projects in Stores Dashboard - DEV
echo  Backend Server Startup
echo ========================================
echo.

cd /d "%~dp0backend"

echo Starting DEV server on http://localhost:8002
echo.
echo Keep this window open while testing!
echo Press CTRL+C to stop the server.
echo.
echo DEV URLs:
echo   Main Dashboard:   http://localhost:8002/
echo   Admin Panel:      http://localhost:8002/admin.html
echo   API Docs:         http://localhost:8002/docs
echo.
echo PRODUCTION is at:  http://127.0.0.1:8001/
echo.

set ENVIRONMENT=dev
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload

pause
