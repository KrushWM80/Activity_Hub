@echo off
set BASE=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation
set USER=HOMEOFFICE\krush

schtasks /create /tn "Activity_Hub_JobCodes_AutoStart" /tr "cmd /c \"%BASE%\start_jobcodes_server_24_7.bat\"" /sc onlogon /ru "%USER%" /f
schtasks /create /tn "Activity_Hub_ProjectsInStores_AutoStart" /tr "cmd /c \"%BASE%\start_projects_in_stores_24_7.bat\"" /sc onlogon /ru "%USER%" /f
schtasks /create /tn "Activity_Hub_TDA_AutoStart" /tr "cmd /c \"%BASE%\start_tda_insights_24_7.bat\"" /sc onlogon /ru "%USER%" /f
schtasks /create /tn "Activity_Hub_Store_Dashboard_AutoStart" /tr "cmd /c \"%BASE%\start_store_dashboard_24_7.bat\"" /sc onlogon /ru "%USER%" /f
schtasks /create /tn "Activity_Hub_StoreMeetingPlanner_AutoStart" /tr "cmd /c \"%BASE%\start_meeting_planner_24_7.bat\"" /sc onlogon /ru "%USER%" /f
schtasks /create /tn "Activity_Hub_VETDashboard_AutoStart" /tr "cmd /c \"%BASE%\start_vet_dashboard_24_7.bat\"" /sc onlogon /ru "%USER%" /f
schtasks /create /tn "Activity_Hub_Zorro_AutoStart" /tr "cmd /c \"%BASE%\start_zorro_24_7.bat\"" /sc onlogon /ru "%USER%" /f
schtasks /create /tn "Activity_Hub_Daily_HealthCheck" /tr "powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1\"" /sc daily /st 06:00:00 /f

echo.
schtasks /query /fo TABLE 2>&1 | findstr "Activity_Hub"
