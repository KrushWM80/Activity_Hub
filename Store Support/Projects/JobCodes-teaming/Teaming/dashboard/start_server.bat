@echo off
echo ============================================================
echo Job Code Teaming Dashboard Server
echo ============================================================
echo.

cd /d "%~dp0"

REM Use the venv in Activity_Hub (parent project directory)
set PYTHON_EXE=..\..\..\..\..\.venv\Scripts\python.exe

REM Check if venv exists, otherwise try to use system python
if not exist "%PYTHON_EXE%" (
    echo Warning: Virtual environment not found at expected path
    echo Attempting to use system Python...
    set PYTHON_EXE=python.exe
)

echo Installing dependencies...
"%PYTHON_EXE%" -m pip install fastapi uvicorn pandas openpyxl python-multipart --quiet

echo.
echo Starting server...
echo.
echo Dashboard URL: http://localhost:8080
echo Default Login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

"%PYTHON_EXE%" backend\main.py

pause
