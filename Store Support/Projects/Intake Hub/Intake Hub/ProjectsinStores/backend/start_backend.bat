@echo off
REM Auto-start Projects in Stores Backend Server
cd /d "C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "start_server.ps1"
pause
