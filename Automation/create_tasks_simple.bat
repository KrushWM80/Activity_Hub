@echo off
REM Direct schtasks commands to set up auto-start
REM Run this batch file as Administrator

cd /d "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

echo Creating scheduled task: Activity_Hub_TDA_AutoStart
schtasks /create /tn "Activity_Hub_TDA_AutoStart" /tr "\"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

echo Creating scheduled task: Activity_Hub_Store_Dashboard_AutoStart
schtasks /create /tn "Activity_Hub_Store_Dashboard_AutoStart" /tr "\"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

echo Creating scheduled task: Activity_Hub_Zorro_AutoStart
schtasks /create /tn "Activity_Hub_Zorro_AutoStart" /tr "\"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat\"" /sc onstart /ru SYSTEM /rl HIGHEST /f

echo Creating scheduled task: Activity_Hub_Daily_HealthCheck
schtasks /create /tn "Activity_Hub_Daily_HealthCheck" /tr "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1\"" /sc daily /st 06:00:00 /ru SYSTEM /rl HIGHEST /f

echo.
echo Verifying tasks created:
schtasks /query /tn "Activity_Hub*" /fo list

echo.
echo Setup complete!
pause
