param()

$remotePath = "\\10.97.114.181\c$\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
$localMainPy = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py"
$remoteMainPy = Join-Path $remotePath "main.py"
$maxRetries = 5
$retryWait = 5

Write-Host "Deployment Script - Direct File Copy" -ForegroundColor Cyan
Write-Host ""

# Backup
Write-Host "Backing up remote main.py..." -ForegroundColor Yellow
$backup = Join-Path $remotePath ("main.py.backup." + (Get-Date -Format "yyyyMMdd-HHmmss"))
Copy-Item $remoteMainPy $backup -ErrorAction SilentlyContinue -Force
Write-Host "Backup created" -ForegroundColor Green

# Copy with retries
Write-Host ""
Write-Host "Copying updated main.py (with $maxRetries retries)..." -ForegroundColor Yellow

$success = $false
for ($i = 1; $i -le $maxRetries; $i++) {
    try {
        Write-Host "Attempt $i/$maxRetries..." -ForegroundColor Cyan
        Copy-Item $localMainPy $remoteMainPy -Force -ErrorAction Stop
        Write-Host "SUCCESS: File copied" -ForegroundColor Green
        $success = $true
        break
    } catch {
        if ($i -lt $maxRetries) {
            Write-Host "  File locked, waiting ${retryWait}s..." -ForegroundColor Yellow
            Start-Sleep -Seconds $retryWait
        } else {
            Write-Host "ERROR: Could not copy after $maxRetries attempts" -ForegroundColor Red
            Write-Host "The backend process may still be running. Try manually:" -ForegroundColor Yellow
            Write-Host "  1. RDP to 10.97.114.181" -ForegroundColor Yellow
            Write-Host "  2. Stop python.exe from Task Manager" -ForegroundColor Yellow
            Write-Host "  3. Run this script again" -ForegroundColor Yellow
            exit 1
        }
    }
}

if ($success) {
    Write-Host ""
    Write-Host "Waiting for backend to auto-restart..." -ForegroundColor Yellow
    Start-Sleep 5
    
    Write-Host ""
    Write-Host "Testing lookup endpoint..." -ForegroundColor Yellow
    try {
        $loginResp = Invoke-WebRequest -Uri "http://10.97.114.181:8080/api/login" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{username="admin"; password="admin123"}) -UseBasicParsing -SessionVariable session -ErrorAction Stop
        Write-Host "Backend is responding" -ForegroundColor Green
        
        $lookupBody = ConvertTo-Json @{job_code="30-49-855"; pay_types=@("H","S")}
        $lookupResp = Invoke-WebRequest -Uri "http://10.97.114.181:8080/api/job-codes/lookup" -Method POST -ContentType "application/json" -Body $lookupBody -WebSession $session -UseBasicParsing
        
        $result = $lookupResp.Content | ConvertFrom-Json
        Write-Host ""
        Write-Host "DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Job Code 30-49-855 Lookup Results:" -ForegroundColor Cyan
        Write-Host "Employee Count: $($result.employee_count)" -ForegroundColor White
        
        if ($result.employee_count -gt 0) {
            Write-Host ""
            Write-Host "Employees (Pay Types H and S):" -ForegroundColor Cyan
            foreach ($worker in ($result.workers | Select-Object -First 10)) {
                Write-Host "  - $($worker.worker_id) | $($worker.first_name) $($worker.last_name) | Pay: $($worker.pay_type) | Location: $($worker.location_nm)"
            }
        }
    } catch {
        Write-Host ""
        Write-Host "Backend may not be responding yet" -ForegroundColor Yellow
        Write-Host "Updated code is deployed. If backend is not running:" -ForegroundColor Yellow
        Write-Host "  1. RDP to 10.97.114.181" -ForegroundColor Yellow
        Write-Host "  2. Run: python main.py (from dashboard\backend folder)" -ForegroundColor Yellow
        Write-Host "  3. Try the lookup endpoint after restart" -ForegroundColor Yellow
    }
}
