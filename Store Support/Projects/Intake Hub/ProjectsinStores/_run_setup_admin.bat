@echo off
REM Temporary script to run setup as Administrator
powershell.exe -Command "Start-Process powershell -ArgumentList '-NoExit -ExecutionPolicy Bypass -File \"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\ProjectsinStores\setup_24_7_auto_start.ps1\"' -Verb RunAs -WindowStyle Normal" & exit /b
