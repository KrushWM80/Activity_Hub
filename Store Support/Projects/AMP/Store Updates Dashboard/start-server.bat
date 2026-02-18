@echo off
echo Starting Store Updates Dashboard Server...
echo.
echo Server will run on http://localhost:8080
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
python -m http.server 8080
pause