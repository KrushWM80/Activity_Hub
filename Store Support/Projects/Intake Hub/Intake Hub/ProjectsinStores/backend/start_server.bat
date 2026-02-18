@echo off
REM ==============================================
REM Projects in Stores Dashboard - Server Launcher
REM This launches the server in a separate window
REM to avoid signal interference from PowerShell
REM ==============================================
cd /d "%~dp0"

echo.
echo ========================================
echo  Projects in Stores Dashboard Server
echo ========================================
echo.
echo Server URL: http://localhost:8001
echo.

REM Start the server in a NEW console window
start "Projects Dashboard API" cmd /k "cd /d "%~dp0" && python run_server.py"

echo Server started in a new window!
echo Look for the window titled "Projects Dashboard API"
echo.
pause
