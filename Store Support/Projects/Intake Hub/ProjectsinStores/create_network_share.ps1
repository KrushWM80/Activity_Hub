# Create Network Share for Projects in Stores Dashboard
# Run as Administrator

$ShareName = "ProjectsInStores"
$LocalPath = "C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores"
$Description = "Projects in Stores Dashboard - VPN Access"

Write-Host "Creating network share for Projects in Stores Dashboard..." -ForegroundColor Cyan
Write-Host ""

# Check if share already exists
$existingShare = Get-SmbShare -Name $ShareName -ErrorAction SilentlyContinue

if ($existingShare) {
    Write-Host "Share '$ShareName' already exists at: $($existingShare.Path)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Access Path: \\$env:COMPUTERNAME\$ShareName\code_puppy_standalone.html" -ForegroundColor Green
    exit
}

# Create the share
try {
    New-SmbShare -Name $ShareName -Path $LocalPath -Description $Description -FullAccess "Everyone"
    Write-Host "Share created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Share Details:" -ForegroundColor Cyan
    Write-Host "  Name: $ShareName"
    Write-Host "  Path: $LocalPath"
    Write-Host "  Description: $Description"
    Write-Host ""
    Write-Host "Users can access via:" -ForegroundColor Yellow
    Write-Host "  \\$env:COMPUTERNAME\$ShareName" -ForegroundColor Green
    Write-Host "  or"
    Write-Host "  \\10.97.105.88\$ShareName\code_puppy_standalone.html" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: Users need VPN connection to access this share" -ForegroundColor Yellow
} 
catch {
    Write-Host "Error creating share: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure you're running as Administrator!" -ForegroundColor Yellow
}
