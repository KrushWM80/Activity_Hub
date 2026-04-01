# Fix BigQuery client initialization
param([string]$ComputerName = "10.97.114.181")

$scriptBlock = {
    # Kill Python processes
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
    
    # Replace client initialization
    $filePath = 'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py'
    
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw
        $original = 'client = bigquery.Client(project="polaris-analytics-prod")'
        $replacement = 'client = bigquery.Client()'
        
        if ($content.Contains($original)) {
            $newContent = $content.Replace($original, $replacement)
            Set-Content -Path $filePath -Value $newContent -Force
            return "Fixed: Replaced bigquery.Client call"
        } else {
            return "Already uses correct pattern or line not found"
        }
    } else {
        return "File not found: $filePath"
    }
}

try {
    Write-Host "Connecting to $ComputerName..."
    $session = New-PSSession -ComputerName $ComputerName -ErrorAction Stop
    Write-Host "Executing fix on remote..."
    $result = Invoke-Command -Session $session -ScriptBlock $scriptBlock
    Write-Host "Result: $result"
    Remove-PSSession $session
    Write-Host "Session closed"
} catch {
    Write-Host "Error: $_"
    exit 1
}
