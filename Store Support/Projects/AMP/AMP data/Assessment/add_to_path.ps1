# Add Git and Google Cloud SDK to PATH - PowerShell Script
# Date: October 28, 2025
# Purpose: Add installed software to system PATH

Write-Host "🔧 Adding Git and Google Cloud SDK to PATH..." -ForegroundColor Green
Write-Host "================================================"

# Define the paths to add
$gitPath = "$env:USERPROFILE\AppData\Local\Programs\Git\bin"
$gcloudPath = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"

Write-Host "📂 Paths to add:"
Write-Host "   Git: $gitPath"
Write-Host "   Google Cloud SDK: $gcloudPath"
Write-Host ""

# Check if paths exist
$gitExists = Test-Path $gitPath
$gcloudExists = Test-Path $gcloudPath

Write-Host "🔍 Verification:"
Write-Host "   Git path exists: $gitExists" -ForegroundColor $(if($gitExists){'Green'}else{'Red'})
Write-Host "   Google Cloud SDK path exists: $gcloudExists" -ForegroundColor $(if($gcloudExists){'Green'}else{'Red'})
Write-Host ""

if ($gitExists -and $gcloudExists) {
    Write-Host "✅ Both paths found! Adding to PATH..." -ForegroundColor Green
    
    # Get current PATH
    $currentPath = $env:PATH
    
    # Add to current session PATH
    $env:PATH = "$gitPath;$gcloudPath;$currentPath"
    
    Write-Host "✅ Added to current PowerShell session PATH" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🧪 Testing commands in current session:"
    
    # Test Git
    try {
        $gitVersion = git --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Git: $gitVersion" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Git: Failed to execute" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ Git: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test Google Cloud SDK
    try {
        $gcloudVersion = gcloud version --format="value(Google Cloud SDK)" 2>&1 | Select-Object -First 1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Google Cloud SDK: $gcloudVersion" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Google Cloud SDK: Failed to execute" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ Google Cloud SDK: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test BigQuery CLI
    try {
        $bqVersion = bq version 2>&1 | Select-Object -First 1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ BigQuery CLI: $bqVersion" -ForegroundColor Green
        } else {
            Write-Host "   ❌ BigQuery CLI: Failed to execute" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ BigQuery CLI: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "🎯 PERMANENT PATH SETUP OPTIONS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1 - Add to User PATH (Recommended):"
    Write-Host "   1. Press Win+R, type 'sysdm.cpl', press Enter"
    Write-Host "   2. Click 'Environment Variables'"
    Write-Host "   3. In 'User variables', select 'Path' and click 'Edit'"
    Write-Host "   4. Click 'New' and add: $gitPath"
    Write-Host "   5. Click 'New' and add: $gcloudPath"
    Write-Host "   6. Click OK on all dialogs"
    Write-Host "   7. Restart VS Code"
    Write-Host ""
    
    Write-Host "Option 2 - PowerShell Profile (This session only):"
    Write-Host "   The paths are already added to this PowerShell session."
    Write-Host "   You can use git and gcloud commands now in this terminal."
    Write-Host ""
    
    Write-Host "Option 3 - Create Permanent PowerShell Profile:"
    Write-Host "   Run this command to add to your PowerShell profile:"
    Write-Host "   Add-Content `$PROFILE '`$env:PATH += `";$gitPath;$gcloudPath`"'"
    Write-Host ""
    
    Write-Host "🚀 YOU CAN NOW USE THESE COMMANDS:" -ForegroundColor Green
    Write-Host "   git --version"
    Write-Host "   gcloud version"
    Write-Host "   bq version"
    Write-Host "   gcloud auth login"
    Write-Host "   gcloud config set project wmt-assetprotection-prod"
    
} else {
    Write-Host "❌ One or more paths not found. Please verify installation." -ForegroundColor Red
    if (-not $gitExists) {
        Write-Host "   Git not found at: $gitPath" -ForegroundColor Red
    }
    if (-not $gcloudExists) {
        Write-Host "   Google Cloud SDK not found at: $gcloudPath" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✨ PATH setup complete for this session!" -ForegroundColor Green