# Activity Hub Keep-Alive Service
# Prevents Windows from sleeping/hibernating
# Runs continuously in background
# Can be scheduled as: Activity_Hub_KeepAwake task

Write-Host "[Keep-Alive] Activity Hub Keep-Alive Service Starting..." -ForegroundColor Cyan
$LogFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\keep-alive.log"

# Ensure log exists
if (-not (Test-Path $LogFile)) {
    New-Item -Path $LogFile -ItemType File -Force | Out-Null
}

Add-Content -Path $LogFile -Value "[$(Get-Date)] Keep-Alive service started"

# Keep system awake indefinitely
$intervalSeconds = 60  # Tick every 60 seconds

Write-Host "[Keep-Alive] System will remain awake. Press CTRL+C to stop." -ForegroundColor Yellow

while ($true) {
    try {
        # Move mouse slightly (doesn't actually move visually, just signals activity)
        $pos = [System.Windows.Forms.Cursor]::Position
        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X+1), $pos.Y)
        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X), $pos.Y)
        
        # Log every 5 minutes
        if ((Get-Date).Second -eq 0) {
            Add-Content -Path $LogFile -Value "[$(Get-Date)] Keep-Alive running - preventing sleep"
        }
        
        Start-Sleep -Seconds $intervalSeconds
    }
    catch {
        Add-Content -Path $LogFile -Value "[$(Get-Date)] Error in keep-alive: $_"
        Start-Sleep -Seconds 10
    }
}
