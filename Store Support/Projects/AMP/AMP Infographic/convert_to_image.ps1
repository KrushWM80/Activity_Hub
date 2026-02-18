# Convert HTML to Image for WorkVivo
# Using Microsoft Edge browser automation

$htmlFile = "$PSScriptRoot\workvivo_social_post.html"
$outputFile = "$PSScriptRoot\workvivo_winter_health.png"

Write-Host "🖼️  Converting HTML to PNG image..." -ForegroundColor Cyan

# Method 1: Using Edge DevTools Protocol
Write-Host "📄 Opening in Edge browser..." -ForegroundColor Yellow
Write-Host ""
Write-Host "INSTRUCTIONS:" -ForegroundColor Green
Write-Host "1. The HTML file will open in Edge"
Write-Host "2. Press F12 to open Developer Tools"
Write-Host "3. Press Ctrl+Shift+P to open Command Palette"
Write-Host "4. Type 'screenshot' and select 'Capture node screenshot'"
Write-Host "5. Click on the white post area"
Write-Host "6. Save as: workvivo_winter_health.png"
Write-Host ""
Write-Host "OR use the simpler method:"
Write-Host "1. Right-click on the post image"
Write-Host "2. Select 'Save image as...'"
Write-Host "3. Save as: workvivo_winter_health.png"
Write-Host ""

Start-Process msedge.exe -ArgumentList $htmlFile

Write-Host "✅ Browser opened!" -ForegroundColor Green
Write-Host "📱 Save the image and upload to WorkVivo!" -ForegroundColor Cyan