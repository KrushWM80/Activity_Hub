# Quick Setup - Run in Administrator PowerShell
# Copy and paste these commands into an ADMIN PowerShell window

Write-Host "Setting up Projects in Stores (Port 8001)..." -ForegroundColor Cyan
$action = New-ScheduledTaskAction -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_server_24_7.bat" -WorkingDirectory "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
$trigger = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Seconds 30)
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "ActivityHubServer" -Action $action -Trigger $trigger -Principal $principal -Force
Write-Host "[OK] ActivityHubServer created and started" -ForegroundColor Green
Start-ScheduledTask -TaskName "ActivityHubServer"
Start-Sleep -Seconds 5

Write-Host "`nSetting up DC Manager PayCycle tasks..." -ForegroundColor Cyan
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
.\setup_tasks_revised.ps1
Write-Host "[OK] DC Manager tasks created" -ForegroundColor Green
$PayCycleTasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
Write-Host "   Found: $($PayCycleTasks.Count)/26 tasks" -ForegroundColor Green

Write-Host "`nSetting up Job Codes continuous sync..." -ForegroundColor Cyan
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
$action = New-ScheduledTaskAction -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" -Argument 'job_code_comparison.py' -WorkingDirectory "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming"
$trigger = New-ScheduledTaskTrigger -Daily -At "02:00 AM"
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "JobCodes-Continuous-Sync" -Action $action -Trigger $trigger -Principal $principal -Force
Write-Host "[OK] Job Codes sync task created" -ForegroundColor Green

Write-Host "`n================================================" -ForegroundColor Green
Write-Host "RESTORATION COMPLETE" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Green
Write-Host "Services ready:" -ForegroundColor Cyan
Write-Host "  1. Projects in Stores (port 8001) - RUNNING" -ForegroundColor Green
Write-Host "  2. DC Manager PayCycle (26 tasks) - READY" -ForegroundColor Green
Write-Host "  3. Job Codes Continuous Sync - READY`n" -ForegroundColor Green
