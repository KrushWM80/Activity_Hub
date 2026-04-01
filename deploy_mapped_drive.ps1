param()

Write-Host "Remote Backend Deployment" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

$remoteServer = "10.97.114.181"
$remoteShare = "\\$remoteServer\c$"
$backendFolder = "Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
$localMainPy = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py"

Write-Host "Step 1: Getting credentials..." -ForegroundColor Yellow
$cred = Get-Credential -Message "Admin for $remoteServer" -UserName "Administrator"
if (-not $cred) { exit 1 }

Write-Host ""
Write-Host "Step 2: Mapping network drive..." -ForegroundColor Yellow

try {
    # Map the UNC path with credentials
    $drive = New-PSDrive -Name TempDrive -PSProvider FileSystem -Root $remoteShare -Credential $cred -ErrorAction Stop
    Write-Host "Mapped successfully" -ForegroundColor Green
    
    $remoteBackendPath = Join-Path -Path "TempDrive:" -ChildPath $backendFolder
    
    Write-Host ""
    Write-Host "Step 3: Backing up old main.py..." -ForegroundColor Yellow
    $backup = Join-Path $remoteBackendPath ("main.py.backup." + (Get-Date -Format "yyyyMMdd-HHmmss"))
    Copy-Item (Join-Path $remoteBackendPath "main.py") $backup -Force -ErrorAction SilentlyContinue
    Write-Host "Backup created" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Step 4: Copying updated main.py..." -ForegroundColor Yellow
    Copy-Item $localMainPy (Join-Path $remoteBackendPath "main.py") -Force -ErrorAction Stop
    Write-Host "Deployed!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Step 5: Testing endpoint..." -ForegroundColor Yellow
    Start-Sleep 3
    
    try {
        $loginResp = Invoke-WebRequest -Uri "http://$remoteServer:8080/api/login" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{username="admin"; password="admin123"}) -UseBasicParsing -SessionVariable session -ErrorAction Stop
        Write-Host "Backend is responding" -ForegroundColor Green
        
        $lookupResp = Invoke-WebRequest -Uri "http://$remoteServer:8080/api/job-codes/lookup" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{job_code="30-49-855"; pay_types=@("H","S")}) -WebSession $session -UseBasicParsing
        
        $result = $lookupResp.Content | ConvertFrom-Json
        
        Write-Host ""
        Write-Host "SUCCESS - DEPLOYMENT COMPLETE" -ForegroundColor Green
        Write-Host "==============================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Job Code 30-49-855 Lookup Results:" -ForegroundColor Cyan
        Write-Host "Employee Count: $($result.employee_count)" -ForegroundColor White
        
        if ($result.employee_count -gt 0) {
            Write-Host ""
            Write-Host "Employees (H and S pay types):" -ForegroundColor Cyan
            foreach ($w in ($result.workers | Select-Object -First 20)) {
                Write-Host "  ID: $($w.worker_id) | $($w.first_name) $($w.last_name) | Pay: $($w.pay_type) | Location: $($w.location_nm)"
            }
        }
        
    } catch {
        Write-Host "Backend may need manual restart (file was updated)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To restart: RDP to $remoteServer and restart Python/backend" -ForegroundColor Yellow
    }
    
    Remove-PSDrive TempDrive
    
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    exit 1
}
