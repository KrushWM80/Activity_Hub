@echo off
echo Starting Projects in Stores Dashboard...
echo.
cd /d "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
if errorlevel 1 (
    echo ERROR: Could not change to backend directory
    pause
    exit /b 1
)
echo Current directory: %CD%
echo.
echo Starting server on http://0.0.0.0:8001
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8001
if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start
    pause
)
