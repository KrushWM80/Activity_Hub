@echo off
REM ==========================================
REM Activity Hub Remote Command Watcher - 24/7
REM ==========================================
REM Purpose: Watches for remote commands via OneDrive sync
REM  Allows laptop to control desktop services remotely
REM
REM This should run on the DESKTOP (WEUS42608431466)
REM Start manually or add as a scheduled task

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set WatcherScript=%ProjectRoot%\Automation\remote_command_watcher.ps1

echo.
echo ================================================================
echo  Activity Hub Remote Command Watcher - 24/7 Mode
echo ================================================================
echo  Desktop: %COMPUTERNAME%
echo  Watching: %ProjectRoot%\Automation\remote_commands\
echo  Polling every 30 seconds for commands
echo ================================================================
echo.

:START
echo [%date% %time%] Starting remote command watcher...
powershell -ExecutionPolicy Bypass -File "%WatcherScript%"

echo [%date% %time%] Watcher stopped. Restarting in 10 seconds...
timeout /t 10 /nobreak > nul
goto START
