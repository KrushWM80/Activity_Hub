@echo off
REM Create the TDA Weekly Email scheduled task
REM Must be run as Administrator

schtasks /create /tn "Activity_Hub_TDA_Weekly_Email" /tr "cmd /c \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\send_tda_weekly_email.bat\"" /sc weekly /d THU /st 11:00 /ru "%USERNAME%" /rl HIGHEST /f

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Weekly email task created!
    echo   Task: Activity_Hub_TDA_Weekly_Email
    echo   Schedule: Every Thursday at 11:00 AM
    echo   Script: send_tda_weekly_email.bat
    echo.
) else (
    echo.
    echo FAILED: Could not create task. Run as Administrator.
    echo.
)
pause
