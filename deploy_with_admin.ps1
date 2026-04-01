param()

$remoteServer = "10.97.114.181"
$localPath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
$remotePath = "\\10.97.114.181\c$\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT TO 10.97.114.181:8080" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get admin credentials
Write-Host "Step 1: Getting credentials..." -ForegroundColor Yellow
$cred = Get-Credential -Message "Enter admin credentials for 10.97.114.181" -UserName "Administrator"

if (-not $cred) {
    Write-Host "Credentials cancelled" -ForegroundColor Red
    exit 1
}

# Stop backend process
Write-Host ""
Write-Host "Step 2: Stopping backend process..." -ForegroundColor Yellow
try {
    Invoke-Command -ComputerName $remoteServer -Credential $cred -ScriptBlock {
        Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*JobCodes*" -or $_.Commandline -like "*main.py*"} | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep 2
        Write-Host "Backend process stopped"
    }
    Write-Host "OK: Backend stopped" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Could not stop backend: $_" -ForegroundColor Red
    exit 1
}

Start-Sleep 2

# Backup and copy new main.py
Write-Host ""
Write-Host "Step 3: Backing up and deploying new main.py..." -ForegroundColor Yellow

$timeStamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = Join-Path $remotePath ("main.py.backup." + $timeStamp)

try {
    Copy-Item (Join-Path $remotePath "main.py") $backup -ErrorAction SilentlyContinue
    Copy-Item (Join-Path $localPath "main.py") (Join-Path $remotePath "main.py") -Force
    Write-Host "OK: Deployed updated main.py with lookup endpoint" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Could not copy file: $_" -ForegroundColor Red
    exit 1
}

# Restart backend
Write-Host ""
Write-Host "Step 4: Restarting backend..." -ForegroundColor Yellow
try {
    Invoke-Command -ComputerName $remoteServer -Credential $cred -ScriptBlock {
        $backendPath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
        $pythonExe = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
        
        Set-Location $backendPath
        $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
        
        Start-Process -FilePath $pythonExe -ArgumentList "main.py" -NoNewWindow
        Start-Sleep 3
        Write-Host "Backend restarted"
    }
    Write-Host "OK: Backend started" -ForegroundColor Green
} catch {
    Write-Host "Warning: Could not auto-start backend: $_" -ForegroundColor Yellow
    Write-Host "You may need to manually start it" -ForegroundColor Yellow
}

# Test endpoint
Write-Host ""
Write-Host "Step 5: Testing lookup endpoint..." -ForegroundColor Yellow
Start-Sleep 3

try {
    $loginResp = Invoke-WebRequest -Uri "http://10.97.114.181:8080/api/login" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{username="admin"; password="admin123"}) -UseBasicParsing -SessionVariable session -ErrorAction Stop
    Write-Host "OK: Backend is responding" -ForegroundColor Green
    
    $lookupBody = @{
        job_code = "30-49-855"
        pay_types = @("H", "S")
    } | ConvertTo-Json
    
    $lookupResp = Invoke-WebRequest -Uri "http://10.97.114.181:8080/api/job-codes/lookup" -Method POST -ContentType "application/json" -Body $lookupBody -WebSession $session -UseBasicParsing -ErrorAction Stop
    
    $result = $lookupResp.Content | ConvertFrom-Json
    Write-Host ""
    Write-Host "SUCCESS: Lookup endpoint working!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Results for job code 30-49-855 (Pay types H and S):" -ForegroundColor Cyan
    Write-Host "Employee Count: $($result.employee_count)" -ForegroundColor White
    
    if ($result.employee_count -gt 0) {
        Write-Host ""
        Write-Host "Employees:" -ForegroundColor Cyan
        $result.workers | Select-Object -First 10 | ForEach-Object {
            Write-Host "  ID: $($_.worker_id) | $($_.first_name) $($_.last_name) | Pay: $($_.pay_type) | Location: $($_.location_nm)"
        }
    }
} catch {
    Write-Host "ERROR testing endpoint: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check if backend is running and accessible" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
