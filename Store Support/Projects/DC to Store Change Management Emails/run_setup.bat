@echo off
REM Run PayCycle task setup as admin

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"

REM Run PowerShell as admin to execute setup
powershell -NoProfile -Command "Start-Process powershell -ArgumentList '-NoProfile -Command \"cd ''C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails''; .\\setup_tasks_FUTURE_PAYCYCLES.ps1\"' -Verb RunAs"

pause

