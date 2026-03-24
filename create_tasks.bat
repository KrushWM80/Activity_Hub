@echo off
REM DC PayCycle Task Creator using schtasks.exe
REM This should work since schtasks handles permissions better

setlocal enabledelayedexpansion

set "BasePath=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
set "PyExe=c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
set "Script=daily_check_smart.py"

echo Creating 22 PayCycle tasks...
echo.

set created=0
set failed=0

REM PC-05: 2026-04-03
schtasks /create /tn "DC-EMAIL-PC-05" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 04/03/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-05 & set /a created+=1) || (echo [FAIL] PC-05 & set /a failed+=1)

REM PC-06: 2026-04-17
schtasks /create /tn "DC-EMAIL-PC-06" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 04/17/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-06 & set /a created+=1) || (echo [FAIL] PC-06 & set /a failed+=1)

REM PC-07: 2026-05-01
schtasks /create /tn "DC-EMAIL-PC-07" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 05/01/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-07 & set /a created+=1) || (echo [FAIL] PC-07 & set /a failed+=1)

REM PC-08: 2026-05-15
schtasks /create /tn "DC-EMAIL-PC-08" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 05/15/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-08 & set /a created+=1) || (echo [FAIL] PC-08 & set /a failed+=1)

REM PC-09: 2026-05-29
schtasks /create /tn "DC-EMAIL-PC-09" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 05/29/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-09 & set /a created+=1) || (echo [FAIL] PC-09 & set /a failed+=1)

REM PC-10: 2026-06-12
schtasks /create /tn "DC-EMAIL-PC-10" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 06/12/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-10 & set /a created+=1) || (echo [FAIL] PC-10 & set /a failed+=1)

REM PC-11: 2026-06-26
schtasks /create /tn "DC-EMAIL-PC-11" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 06/26/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-11 & set /a created+=1) || (echo [FAIL] PC-11 & set /a failed+=1)

REM PC-12: 2026-07-10
schtasks /create /tn "DC-EMAIL-PC-12" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 07/10/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-12 & set /a created+=1) || (echo [FAIL] PC-12 & set /a failed+=1)

REM PC-13: 2026-07-24
schtasks /create /tn "DC-EMAIL-PC-13" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 07/24/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-13 & set /a created+=1) || (echo [FAIL] PC-13 & set /a failed+=1)

REM PC-14: 2026-08-07
schtasks /create /tn "DC-EMAIL-PC-14" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 08/07/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-14 & set /a created+=1) || (echo [FAIL] PC-14 & set /a failed+=1)

REM PC-15: 2026-08-21
schtasks /create /tn "DC-EMAIL-PC-15" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 08/21/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-15 & set /a created+=1) || (echo [FAIL] PC-15 & set /a failed+=1)

REM PC-16: 2026-09-04
schtasks /create /tn "DC-EMAIL-PC-16" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 09/04/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-16 & set /a created+=1) || (echo [FAIL] PC-16 & set /a failed+=1)

REM PC-17: 2026-09-18
schtasks /create /tn "DC-EMAIL-PC-17" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 09/18/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-17 & set /a created+=1) || (echo [FAIL] PC-17 & set /a failed+=1)

REM PC-18: 2026-10-02
schtasks /create /tn "DC-EMAIL-PC-18" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 10/02/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-18 & set /a created+=1) || (echo [FAIL] PC-18 & set /a failed+=1)

REM PC-19: 2026-10-16
schtasks /create /tn "DC-EMAIL-PC-19" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 10/16/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-19 & set /a created+=1) || (echo [FAIL] PC-19 & set /a failed+=1)

REM PC-20: 2026-10-30
schtasks /create /tn "DC-EMAIL-PC-20" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 10/30/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-20 & set /a created+=1) || (echo [FAIL] PC-20 & set /a failed+=1)

REM PC-21: 2026-11-13
schtasks /create /tn "DC-EMAIL-PC-21" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 11/13/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-21 & set /a created+=1) || (echo [FAIL] PC-21 & set /a failed+=1)

REM PC-22: 2026-11-27
schtasks /create /tn "DC-EMAIL-PC-22" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 11/27/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-22 & set /a created+=1) || (echo [FAIL] PC-22 & set /a failed+=1)

REM PC-23: 2026-12-11
schtasks /create /tn "DC-EMAIL-PC-23" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 12/11/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-23 & set /a created+=1) || (echo [FAIL] PC-23 & set /a failed+=1)

REM PC-24: 2026-12-25
schtasks /create /tn "DC-EMAIL-PC-24" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 12/25/2026 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-24 & set /a created+=1) || (echo [FAIL] PC-24 & set /a failed+=1)

REM PC-25: 2027-01-08
schtasks /create /tn "DC-EMAIL-PC-25" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 01/08/2027 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-25 & set /a created+=1) || (echo [FAIL] PC-25 & set /a failed+=1)

REM PC-26: 2027-01-22
schtasks /create /tn "DC-EMAIL-PC-26" /tr "cmd /c cd /d \"%BasePath%\" && \"%PyExe%\" %Script%" /sc once /sd 01/22/2027 /st 06:00 /rl highest /f >nul 2>&1 && (echo [OK] PC-26 & set /a created+=1) || (echo [FAIL] PC-26 & set /a failed+=1)

echo.
echo Results: Created=%created%, Failed=%failed%
echo.

schtasks /query /tn "DC-EMAIL-PC-*" 2>nul | find /c "DC-EMAIL-PC" >nul && (
    for /f "tokens=1" %%A in ('schtasks /query /tn "DC-EMAIL-PC-*" 2^>nul ^| find /c "DC-EMAIL-PC"') do echo Total in scheduler: %%A
)
