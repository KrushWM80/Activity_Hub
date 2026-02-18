# Disable automatic startup for Job Codes Dashboard Server

$taskName = "JobCodesDashboardServer"

Write-Host "Disabling auto-start for Job Codes Dashboard..." -ForegroundColor Yellow

$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($task) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Auto-start disabled successfully!" -ForegroundColor Green
    Write-Host "The server will no longer start automatically at login." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can re-enable it anytime by running: .\setup_auto_start.ps1" -ForegroundColor Yellow
}
else {
    Write-Host "Auto-start task not found. It may already be disabled." -ForegroundColor Yellow
}
