# Test creating one PayCycle task
$TaskName = "DC-EMAIL-PC-05"
$Date = "2026-04-03"
$Time = "06:00:00"
$TriggerDateTime = [DateTime]::Parse("$Date $Time")

Write-Host "Testing task creation for PC-05" -ForegroundColor Cyan
Write-Host "Scheduled for: $TriggerDateTime`n"

try {
    $Trigger = New-ScheduledTaskTrigger -Once -At $TriggerDateTime -ErrorAction Stop
    Write-Host "[1/4] Trigger created" -ForegroundColor Green
    
    $Action = New-ScheduledTaskAction `
        -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" `
        -Argument "daily_check_smart.py" `
        -WorkingDirectory "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails" `
        -ErrorAction Stop
    Write-Host "[2/4] Action created" -ForegroundColor Green
    
    $Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ErrorAction Stop
    Write-Host "[3/4] Settings created" -ForegroundColor Green
    
    Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action -Settings $Settings -RunLevel Highest -Force -ErrorAction Stop | Out-Null
    Write-Host "[4/4] Task registered!" -ForegroundColor Green
    Write-Host "`nSUCCESS: Task created`n" -ForegroundColor Green
    
} catch {
    Write-Host "`n[ERROR] Task creation failed!" -ForegroundColor Red
    Write-Host "Message: $($_.Exception.Message)" -ForegroundColor Yellow
}
