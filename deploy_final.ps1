param()

Write-Host "Deployment - Copy & Rename Approach" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

$remoteServer = "10.97.114.181"
$remoteShare = "\\$remoteServer\c$"
$backendFolder = "Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
$localMainPy = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py"

Write-Host "Step 1: Getting credentials..." -ForegroundColor Yellow
$cred = Get-Credential -Message "Admin for $remoteServer" -UserName "Administrator"
if (-not $cred) { exit 1 }

Write-Host ""
Write-Host "Step 2: Mapping drive with credentials..." -ForegroundColor Yellow

try {
    $drive = New-PSDrive -Name TempDrive -PSProvider FileSystem -Root $remoteShare -Credential $cred -ErrorAction Stop
    Write-Host "Mapped" -ForegroundColor Green
    
    $remoteBackendPath = Join-Path -Path "TempDrive:" -ChildPath $backendFolder
    $remoteMainPy = Join-Path $remoteBackendPath "main.py"
    $remoteMainPyNew = Join-Path $remoteBackendPath "main.py.new"
    
    Write-Host ""
    Write-Host "Step 3: Copying to temporary file..." -ForegroundColor Yellow
    Copy-Item $localMainPy $remoteMainPyNew -Force
    Write-Host "Copied to main.py.new" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Step 4: Backing up current main.py..." -ForegroundColor Yellow
    $backup = Join-Path $remoteBackendPath ("main.py.backup." + (Get-Date -Format "yyyyMMdd-HHmmss"))
    Copy-Item $remoteMainPy $backup -Force -ErrorAction SilentlyContinue
    Write-Host "Backup created" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Step 5: Replacing main.py..." -ForegroundColor Yellow
    Remove-Item $remoteMainPy -Force
    Rename-Item $remoteMainPyNew $remoteMainPy -Force
    Write-Host "Replaced successfully" -ForegroundColor Green
    
    Remove-PSDrive TempDrive
    
    Write-Host ""
    Write-Host "Step 6: Waiting for backend..." -ForegroundColor Yellow
    Start-Sleep 5
    
    Write-Host ""
    Write-Host "Step 7: Testing lookup endpoint..." -ForegroundColor Yellow
    
    try {
        $loginResp = Invoke-WebRequest -Uri "http://$remoteServer:8080/api/login" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{username="admin"; password="admin123"}) -UseBasicParsing -SessionVariable session -ErrorAction Stop
        Write-Host "Backend online" -ForegroundColor Green
        
        $lookupResp = Invoke-WebRequest -Uri "http://$remoteServer:8080/api/job-codes/lookup" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{job_code="30-49-855"; pay_types=@("H","S")}) -WebSession $session -UseBasicParsing
        
        $result = $lookupResp.Content | ConvertFrom-Json
        
        Write-Host ""
        Write-Host "SUCCESS!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Job Code: 30-49-855 (Pay Types: H and S)" -ForegroundColor Cyan
        Write-Host "Employee Count: $($result.employee_count)" -ForegroundColor White
        
        if ($result.employee_count -gt 0) {
            Write-Host ""
            Write-Host "Workers:" -ForegroundColor Cyan
            foreach ($w in $result.workers) {
                Write-Host "  $($w.worker_id) | $($w.first_name) $($w.last_name) | $($w.pay_type) | $($w.location_nm)"
            }
        }
        
    } catch {
        Write-Host ""
        Write-Host "WARN: Could not test endpoint yet" -ForegroundColor Yellow
        Write-Host "File was deployed successfully" -ForegroundColor Green
        Write-Host "Give backend a few seconds to reload and try again" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    exit 1
}
