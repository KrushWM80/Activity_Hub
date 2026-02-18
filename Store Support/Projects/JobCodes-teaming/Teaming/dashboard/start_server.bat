@echo off
echo ============================================================
echo Job Code Teaming Dashboard Server
echo ============================================================
echo.

cd /d "%~dp0"

echo Installing dependencies...
C:\Users\krush\.code-puppy-venv\Scripts\python.exe -m pip install fastapi uvicorn pandas openpyxl python-multipart --quiet

echo.
echo Starting server...
echo.
echo Dashboard URL: http://localhost:8080
echo Default Login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

C:\Users\krush\.code-puppy-venv\Scripts\python.exe backend\main.py

pause
