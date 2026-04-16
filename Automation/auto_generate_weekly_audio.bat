@echo off
REM ==========================================
REM Auto-Generate Weekly Audio
REM ==========================================
REM Runs: Fridays, hourly (7AM-5PM) after daily status email
REM Checks BQ: if Total == Summarized, generates audio + sends email
REM Stops checking once processed (lock file per week)
REM ==========================================

setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set AudioScripts=%ProjectRoot%\Store Support\Projects\AMP\Zorro\Audio\Scripts
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%AudioScripts%\auto_generate_weekly_audio.log

REM Use absolute path for GCP credentials
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo [%date% %time%] ====== Auto-Generate Check Starting ====== >> "%LogFile%"

cd /d "%AudioScripts%"

REM Run the auto-generate script
echo [%date% %time%] Running auto_generate_weekly_audio.py... >> "%LogFile%"
"%PythonExe%" auto_generate_weekly_audio.py >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] Auto-generate check completed successfully >> "%LogFile%"
) else (
    echo [%date% %time%] ERROR: Auto-generate failed with code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== Auto-Generate Check Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"
