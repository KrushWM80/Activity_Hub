@echo off
REM Zorro Video Generator - GUI Launcher
REM Quick launcher for Windows

echo.
echo ============================================================
echo    Zorro AI Video Generator - Web Interface
echo ============================================================
echo.
echo Starting the application...
echo.

cd /d "%~dp0"
python run_gui.py

pause
