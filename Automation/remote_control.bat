@echo off
title Activity Hub Remote Control (OneDrive)
cd /d "%~dp0"

:menu
cls
echo.
echo  ============================================================
echo    ACTIVITY HUB REMOTE CONTROL (via OneDrive Sync)
echo  ============================================================
echo.
echo   Works WITHOUT WinRM/RDP - uses OneDrive sync
echo   Commands take 30-60 seconds to sync between machines
echo.
echo   SERVICES:
echo     jobcodes / projects / tda / storedashboard
echo     meetingplanner / vet / zorro / all
echo.
echo  ------------------------------------------------------------
echo   COMMANDS:
echo     1. status      - Check all service status
echo     2. start       - Start a service
echo     3. stop        - Stop a service
echo     4. restart     - Restart a service
echo     5. processes   - List python processes on desktop
echo     6. ping        - Check if desktop is reachable
echo     0. exit        - Exit
echo  ------------------------------------------------------------
echo.
set /p choice="  Enter choice (0-6): "

if "%choice%"=="0" goto :eof
if "%choice%"=="1" goto do_status
if "%choice%"=="2" goto do_start
if "%choice%"=="3" goto do_stop
if "%choice%"=="4" goto do_restart
if "%choice%"=="5" goto do_processes
if "%choice%"=="6" goto do_ping

echo.
echo   Invalid choice.
pause
goto menu

:do_status
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0remote_control.ps1" status
echo.
pause
goto menu

:do_start
echo.
set /p svc="  Which service? (or 'all'): "
powershell -ExecutionPolicy Bypass -File "%~dp0remote_control.ps1" start %svc%
echo.
pause
goto menu

:do_stop
echo.
set /p svc="  Which service? (or 'all'): "
powershell -ExecutionPolicy Bypass -File "%~dp0remote_control.ps1" stop %svc%
echo.
pause
goto menu

:do_restart
echo.
set /p svc="  Which service? (or 'all'): "
powershell -ExecutionPolicy Bypass -File "%~dp0remote_control.ps1" restart %svc%
echo.
pause
goto menu

:do_processes
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0remote_control.ps1" processes
echo.
pause
goto menu

:do_ping
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0remote_control.ps1" ping
echo.
pause
goto menu
