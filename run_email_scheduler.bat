@echo off
REM Activity Hub Email Scheduler - Daily Runner
REM Logs to logs\email_scheduler.log

cd /d "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface"
"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\run_scheduled_emails.py" >> "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\logs\email_scheduler.log" 2>&1
