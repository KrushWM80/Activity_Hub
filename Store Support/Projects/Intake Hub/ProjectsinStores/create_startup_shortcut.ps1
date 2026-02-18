# Create Startup Shortcut for Projects in Stores Backend
# No Admin required - just run this script

$StartupFolder = [System.Environment]::GetFolderPath('Startup')
$BatchFile = "C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend\start_backend.bat"
$ShortcutPath = Join-Path $StartupFolder "Projects in Stores Backend.lnk"

Write-Host "Creating startup shortcut..." -ForegroundColor Cyan
Write-Host ""

# Create shortcut object
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Configure shortcut
$Shortcut.TargetPath = $BatchFile
$Shortcut.WorkingDirectory = "C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
$Shortcut.Description = "Auto-start Projects in Stores Backend Server"
$Shortcut.WindowStyle = 1  # Normal window

# Save shortcut
$Shortcut.Save()

Write-Host "Shortcut created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Details:" -ForegroundColor Cyan
Write-Host "  Name: Projects in Stores Backend.lnk"
Write-Host "  Location: $StartupFolder"
Write-Host "  Target: $BatchFile"
Write-Host ""
Write-Host "The backend will now start automatically when you log in." -ForegroundColor Yellow
Write-Host "Access the dashboard at: http://10.97.105.88:8001" -ForegroundColor Green
Write-Host ""
Write-Host "To remove: Delete the shortcut from your Startup folder" -ForegroundColor Gray
