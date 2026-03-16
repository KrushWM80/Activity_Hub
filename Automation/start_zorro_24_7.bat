@echo off
REM ==========================================
REM Zorro Activity Hub - 24/7 Auto-Restart
REM ==========================================
REM Purpose: Keep Zorro podcast server running continuously
REM Access: http://localhost:8888/
REM Status File: zorro_server.log
REM
REM Features:
REM - Auto-restart on crash
REM - Logging of all starts and errors
REM - Jenny Neural voice MP4 audio generation
REM - Podcast server with metadata support
REM - 5-second restart interval on failure

setlocal enabledelayedexpansion

REM Define paths with variables for maintainability
set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set ZorroPath=%ProjectRoot%\Store Support\Projects\AMP\Zorro
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%ZorroPath%\zorro_server.log
set Port=8888

echo.
echo ================================================================
echo Zorro Activity Hub Podcast Server - 24/7 Operating Mode
echo ================================================================
echo Access: http://localhost:%Port%/
echo Audio Generator: http://localhost:%Port%/create-audio
echo Log File: %LogFile%
echo Time: %date% %time%
echo ================================================================
echo.

echo [%date% %time%] Starting Zorro podcast server service... >> "%LogFile%"

REM Change to Zorro directory
cd /d "%ZorroPath%"

REM Start Python backend with auto-restart loop
:restart_loop
echo [%date% %time%] Launching Zorro Server (audio_server.py)... >> "%LogFile%"
echo Launching Zorro on port %Port%...

"%PythonExe%" audio_server.py 2>> "%LogFile%"

REM If process exits, log it and wait before restarting
echo [%date% %time%] Process exited with code !ERRORLEVEL! >> "%LogFile%"
echo Process crashed. Restarting in 5 seconds...
timeout /t 5 /nobreak

goto restart_loop

REM Cleanup on exit
:end
echo [%date% %time%] Zorro server stopped >> "%LogFile%"
endlocal
