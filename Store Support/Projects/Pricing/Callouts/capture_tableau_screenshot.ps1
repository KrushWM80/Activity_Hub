# PowerShell script to capture Tableau dashboard screenshot
# This script uses Edge browser to navigate to the Tableau dashboard and take a screenshot

param(
    [string]$DestinationPath = "tableau_screenshot.png"
)

$TableauUrl = "https://tableau-prep-prod.homeoffice.wal-mart.com/#/views/PricingForecast/PricingForecast?:iid=1"
$EdgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

Write-Host "Capturing Tableau dashboard screenshot..."
Write-Host "Dashboard URL: $TableauUrl"
Write-Host "Destination: $DestinationPath"

# Launch Edge and capture screenshot
# Using user data dir to maintain authentication
$UserDataDir = "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data\Default"

& $EdgePath `
    --headless `
    --disable-gpu `
    --no-sandbox `
    --user-data-dir=$UserDataDir `
    --screenshot=$DestinationPath `
    --window-size=1280,1600 `
    --virtual-time-budget=15000 `
    $TableauUrl

if (Test-Path $DestinationPath) {
    $FileSize = (Get-Item $DestinationPath).Length
    Write-Host "Screenshot saved successfully!"
    Write-Host "File size: $FileSize bytes"
    Write-Host "Location: $(Convert-Path $DestinationPath)"
}
else {
    Write-Host "ERROR: Screenshot was not created. Tableau may require interactive login."
    Write-Host "Please try manually:"
    Write-Host "1. Open the Tableau dashboard in your browser"
    Write-Host "2. Take a screenshot (Shift+Windows+S on Windows 10/11)"
    Write-Host "3. Save as 'tableau_screenshot_manual.png' in the Callouts folder"
}
