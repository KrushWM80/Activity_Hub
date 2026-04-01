param()

$localPath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
$remotePath = "\\10.97.114.181\c$\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"

Write-Host "Stopping backend on remote server..." -ForegroundColor Yellow

try {
    $remoteUser = "Administrator"
    $cred = Get-Credential -Message "Enter credentials for 10.97.114.181" -UserName $remoteUser -ErrorAction SilentlyContinue
    
    if ($cred) {
        Invoke-Command -ComputerName "10.97.114.181" -Credential $cred -ScriptBlock {
            Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
            Start-Sleep 2
        }
        Write-Host "Backend stopped" -ForegroundColor Green
    } else {
        Write-Host "Credentials cancelled - attempting without them" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Could not stop backend via PS Remoting" -ForegroundColor Yellow
}

Start-Sleep 2

Write-Host ""
Write-Host "Backing up and copying new main.py..." -ForegroundColor Yellow

$timeStamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = Join-Path $remotePath ("main.py.backup." + $timeStamp)
$localFile = Join-Path $localPath "main.py"
$remoteFile = Join-Path $remotePath "main.py"

Copy-Item $remoteFile $backup -ErrorAction SilentlyContinue
Copy-Item $localFile $remoteFile -Force -ErrorAction Stop
Write-Host "Updated main.py deployed" -ForegroundColor Green

Write-Host ""
Write-Host "Testing connection..." -ForegroundColor Yellow
Start-Sleep 3

try {
    $response = Invoke-WebRequest -Uri "http://10.97.114.181:8080/api/job-codes/lookup" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{job_code="30-49-855"; pay_types=@("H","S")}) -UseBasicParsing
    Write-Host "SUCCESS: Lookup endpoint is working!" -ForegroundColor Green
    Write-Host $response.Content
} catch {
    Write-Host "Testing lookup endpoint..." -ForegroundColor Yellow
    try {
        $loginResp = Invoke-WebRequest -Uri "http://10.97.114.181:8080/api/login" -Method POST -ContentType "application/json" -Body (ConvertTo-Json @{username="admin"; password="admin123"}) -UseBasicParsing -SessionVariable session
        Write-Host "Backend is responding (need to restart for changes)" -ForegroundColor Cyan
    } catch {
        Write-Host "Backend may need manual restart" -ForegroundColor Yellow
    }
}
