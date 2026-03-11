@echo off
REM Daily Status Email Setup - Requires Administrator
REM This file will request administrator elevation and run the PowerShell setup

powershell -Command "Start-Process powershell -ArgumentList '-NoExit -ExecutionPolicy Bypass -File \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\SETUP_DAILY_STATUS_EMAILS.ps1\"' -Verb RunAs"

pause
