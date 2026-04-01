param()

$localPath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
$remotePath = "\\10.97.114.181\c$\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"

Write-Host "Step 1: Checking remote access..." -ForegroundColor Yellow
if (Test-Path $remotePath) {
    Write-Host "OK: Remote path accessible" -ForegroundColor Green
} else {
    Write-Host "ERROR: Cannot access remote path" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Backing up remote main.py..." -ForegroundColor Yellow
$timeStamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = Join-Path $remotePath ("main.py.backup." + $timeStamp)
Copy-Item (Join-Path $remotePath "main.py") $backup -ErrorAction SilentlyContinue
Write-Host "OK: Backup created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Copying updated main.py..." -ForegroundColor Yellow
$localFile = Join-Path $localPath "main.py"
$remoteFile = Join-Path $remotePath "main.py"
Copy-Item $localFile $remoteFile -Force
Write-Host "OK: Deployed main.py with lookup endpoint" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Testing backend..." -ForegroundColor Yellow
Start-Sleep 2
try {
    $response = Invoke-WebRequest -Uri "http://10.97.114.181:8080/api/login" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{username="admin"; password="admin123"}) -UseBasicParsing
    Write-Host "OK: Backend is responding" -ForegroundColor Green
} catch {
    Write-Host "WARN: Backend may need restart" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "DEPLOYMENT COMPLETE" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lookup endpoint available at:" -ForegroundColor Cyan
Write-Host "  http://10.97.114.181:8080/api/job-codes/lookup" -ForegroundColor White
