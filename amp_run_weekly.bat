@echo off
REM Wrapper for weekly AMP AutoFeed CSV report
cd /d "%~dp0"
"C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\platform\bundledpython\python.exe" amp_autofeed_orchestrator.py csv-report --days 90 --log-dir amp_validation_logs
