# Minimal test to create ONE PayCycle task with explicit error handling

Write-Host "Testing PayCycle Task Creation" -ForegroundColor Cyan
Write-Host "==============================`n" -ForegroundColor Cyan

$TestTaskName = "DC-EMAIL-PC-Test"
$PytonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$WorkDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$Script = "daily_check_smart.py"

Write-Host "Parameters:"
Write-Host "  Task Name: $TestTaskName"
Write-Host "  Python: $PytonExe"
Write-Host "  Work Dir: $WorkDir"
Write-Host "  Script: $Script`n"

try {
    Write-Host "Step 1: Creating trigger for 2026-04-03 06:00..." -ForegroundColor Yellow
    $Trigger = New-ScheduledTaskTrigger -Once -At ([DateTime]::Parse("2026-04-03 06:00:00"))
    Write-Host "  ✓ Trigger created`n" -ForegroundColor Green
}
catch {
    Write-Host "  ✗ Trigger failed: $_`n" -ForegroundColor Red
    exit 1
}

try {
    Write-Host "Step 2: Creating action..." -ForegroundColor Yellow
    $Action = New-ScheduledTaskAction -Execute $PytonExe -Argument """$WorkDir\$Script""" -WorkingDirectory $WorkDir
    Write-Host "  ✓ Action created`n" -ForegroundColor Green
}
catch {
    Write-Host "  ✗ Action failed: $_`n" -ForegroundColor Red
    exit 1
}

try {
    Write-Host "Step 3: Creating principal (SYSTEM, Highest)..." -ForegroundColor Yellow
    $Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    Write-Host "  ✓ Principal created`n" -ForegroundColor Green
}
catch {
    Write-Host "  ✗ Principal failed: $_`n" -ForegroundColor Red
    exit 1
}

try {
    Write-Host "Step 4: Registering task in Task Scheduler..." -ForegroundColor Yellow
    Register-ScheduledTask -TaskName $TestTaskName -Action $Action -Trigger $Trigger -Principal $Principal -Description "Test PayCycle Task" -Force
    Write-Host "  ✓ Task registered!`n" -ForegroundColor Green
}
catch {
    Write-Host "  ✗ FAILED TO REGISTER: $_`n" -ForegroundColor Red
    Write-Host "  This is likely a permission issue or Task Scheduler error`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 5: Verifying task..." -ForegroundColor Yellow
$Task = Get-ScheduledTask -TaskName $TestTaskName -ErrorAction SilentlyContinue
if ($Task) {
    Write-Host "  ✓ Task found in Task Scheduler`n" -ForegroundColor Green
    Write-Host "Task Details:"
    Write-Host "  Name: $($Task.TaskName)"
    Write-Host "  State: $($Task.State)"
    Write-Host "  Next Run: $($Task.NextRunTime)`n"
    
    Write-Host "[SUCCESS] Test task created successfully!`n" -ForegroundColor Green
    Write-Host "Next steps: Try creating all 22 future PayCycles" -ForegroundColor Cyan
}
else {
    Write-Host "  ✗ Task NOT found after registration!`n" -ForegroundColor Red
}
