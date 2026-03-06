@echo off
REM PayCycle 3 Remote Diagnostics Script
REM Purpose: Check if PayCycle 3 executed on remote machine WEUS42608431466
REM Date: March 6, 2026

echo.
echo ========================================
echo PayCycle 3 Execution Diagnostics
echo Remote Machine: WEUS42608431466
echo Time: %date% %time%
echo ========================================
echo.

REM Try to access remote machine
echo [1/5] Checking network connectivity...
ping -n 1 WEUS42608431466 >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot reach WEUS42608431466 on network
    goto error
) else (
    echo SUCCESS: WEUS42608431466 is reachable
)

echo.
echo [2/5] Attempting to access remote email output folder...
echo Path: \\WEUS42608431466\c$\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\DC to Store Change Management Emails\emails_sent\

REM If you have admin access, this might work:
dir "\\WEUS42608431466\c$\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\DC to Store Change Management Emails\emails_sent\" /B /O:-D 2>nul

if errorlevel 1 (
    echo UNABLE TO ACCESS (may require admin credentials)
    echo Try mapping the drive with valid credentials first
) else (
    echo SUCCESS: Listed remote files
)

echo.
echo [3/5] Checking if task exists remotely...
echo (Requires PowerShell admin access)
echo Command: Get-ScheduledTask -TaskName "*PC-03*" -ComputerName WEUS42608431466

echo.
echo [4/5] Network path test...
dir "\\WEUS42608431466.homeoffice.wal-mart.com\c$\" /B 2>nul
if errorlevel 1 (
    echo Network share not accessible - check permissions and VPN
)

echo.
echo [5/5] Summary
echo ============
echo Reachability: OK (ping successful)
echo Network Share: Check above for details
echo Recommendation: Log into WEUS42608431466 directly to verify task execution
echo.

goto end

:error
echo ERROR DETECTED
echo Unable to continue diagnostics
echo Verify machine name and network connectivity

:end
echo.
echo ========================================
echo Diagnostic Completed
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Log into WEUS42608431466 directly
echo 2. Open Task Scheduler
echo 3. Search for "DC-EMAIL-PC-03"
echo 4. Check task history for 6:00 AM execution
echo 5. Look for files in emails_sent folder
echo.
pause
