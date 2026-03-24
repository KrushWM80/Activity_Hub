@echo off
REM Auto-elevate to admin and create PayCycle tasks

if not "%1" == "admin" (
    echo Requesting admin privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~0\" admin' -Verb RunAs" 
    exit /b
)

REM Now running as admin
echo.
echo Creating PayCycle tasks as Administrator...
echo.

cd /d "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"

REM Create all 22 future PayCycles using schtasks
for /f "tokens=*" %%i in ('powershell -Command "
`$tasks = @(
    @{pc=5; d='2026-04-03'},
    @{pc=6; d='2026-04-17'},
    @{pc=7; d='2026-05-01'},
    @{pc=8; d='2026-05-15'},
    @{pc=9; d='2026-05-29'},
    @{pc=10; d='2026-06-12'},
    @{pc=11; d='2026-06-26'},
    @{pc=12; d='2026-07-10'},
    @{pc=13; d='2026-07-24'},
    @{pc=14; d='2026-08-07'},
    @{pc=15; d='2026-08-21'},
    @{pc=16; d='2026-09-04'},
    @{pc=17; d='2026-09-18'},
    @{pc=18; d='2026-10-02'},
    @{pc=19; d='2026-10-16'},
    @{pc=20; d='2026-10-30'},
    @{pc=21; d='2026-11-13'},
    @{pc=22; d='2026-11-27'},
    @{pc=23; d='2026-12-11'},
    @{pc=24; d='2026-12-25'},
    @{pc=25; d='2027-01-08'},
    @{pc=26; d='2027-01-22'}
);
foreach (`$t in `$tasks) {
    `$pyExe = 'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe';
    `$cmd = 'cmd /c cd /d \"%cd%\" && \"%pyExe%\" daily_check_smart.py';
    Write-Host \"schtasks /create /tn DC-EMAIL-PC-`$(`$t.pc.ToString('00')) /tr `\"$cmd`\" /sc once /sd $(`$t.d.Replace('-','/')) /st 06:00 /rl highest /f\";
}
"') do (
    %%i
)

echo.
echo.
echo Verifying tasks...
schtasks /query /tn "DC-EMAIL-PC-*" /v | find "DC-EMAIL-PC"

echo.
echo Done!
pause
