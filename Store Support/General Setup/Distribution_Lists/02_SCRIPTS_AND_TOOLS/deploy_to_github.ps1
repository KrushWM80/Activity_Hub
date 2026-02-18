# GitHub Pages Deployment Script for Distribution List Selector
# This script helps deploy the DL Selector to GitHub Pages

Write-Host "================================================================================"
Write-Host "GitHub Pages Deployment Setup"
Write-Host "Distribution List Selector"
Write-Host "================================================================================"
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git detected: $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if we're already in a git repository
$isGitRepo = Test-Path ".git"

if ($isGitRepo) {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
}
else {
    Write-Host "Initializing new Git repository..." -ForegroundColor Cyan
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================================================================"
Write-Host "Step 1: Prepare Files for Deployment"
Write-Host "================================================================================"

# Check required files
$requiredFiles = @(
    "index.html",
    "all_distribution_lists.csv"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ Found: $file" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Missing: $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "ERROR: Missing required files. Cannot continue." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================================================"
Write-Host "Step 2: Create .gitignore"
Write-Host "================================================================================"

# Create .gitignore if it doesn't exist
if (!(Test-Path ".gitignore")) {
    @"
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/

# Logs
*.log
add_members_log_*.txt

# Temporary files
*.tmp
*.bak
~*

# Windows
Thumbs.db
Desktop.ini

# IDE
.vscode/
.idea/

# Exclude timestamped CSVs (keep only the clean copy)
all_distribution_lists_*.csv
ad_groups_*.csv
ad_groups_*.json
email_list_*.txt
hnmeeting2_members.csv
need_to_add_to_hnmeeting2_*.txt
already_on_hnmeeting2_*.txt

# Scripts not needed for GitHub Pages
*.ps1
*.py
test_and_add_members.ps1
add_hnmeeting2_members.ps1
dl_simple_server.py
extract_all_dls_optimized.py
schedule_dl_update.ps1

# Documentation not needed on GitHub Pages
CODE_REVIEW_AND_IMPROVEMENTS.md
DELIVERABLES.txt
FINAL_STATUS_REPORT.md
QUICK_START.txt
RESULTS_SUMMARY.txt
WORKDAY_ACCESS_GUIDE.md
WORKDAY_INTEGRATION_GUIDE.md
ADD_MEMBERS_INSTRUCTIONS.txt
SYSTEM_SPECIFICATION.md
EMAIL_TO_HR_TEMPLATE.txt
EMAIL_TO_WORKDAY_ADMIN.txt
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✓ Created .gitignore" -ForegroundColor Green
}
else {
    Write-Host "✓ .gitignore already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================================================================"
Write-Host "Step 3: Stage Files"
Write-Host "================================================================================"

git add index.html all_distribution_lists.csv DEPLOYMENT.md .gitignore
Write-Host "✓ Files staged for commit" -ForegroundColor Green

Write-Host ""
Write-Host "================================================================================"
Write-Host "Step 4: Commit Changes"
Write-Host "================================================================================"

$commitMessage = "Distribution List Selector - Initial deployment"
git commit -m $commitMessage
Write-Host "✓ Changes committed" -ForegroundColor Green

Write-Host ""
Write-Host "================================================================================"
Write-Host "Step 5: GitHub Repository Setup"
Write-Host "================================================================================"
Write-Host ""
Write-Host "Now you need to:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com/new" -ForegroundColor Cyan
Write-Host "2. Create a new repository (e.g., 'dl-selector')" -ForegroundColor Cyan
Write-Host "3. Do NOT initialize with README, .gitignore, or license" -ForegroundColor Cyan
Write-Host "4. Copy the repository URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "Enter your GitHub repository URL (or press Enter to skip):" -ForegroundColor Yellow
Write-Host "Example: https://github.com/yourusername/dl-selector.git" -ForegroundColor Gray
$repoUrl = Read-Host

if ($repoUrl) {
    Write-Host ""
    Write-Host "Setting remote origin..." -ForegroundColor Cyan
    
    try {
        # Remove existing origin if present
        git remote remove origin 2>$null
    }
    catch {
        # Ignore error if origin doesn't exist
    }
    
    git remote add origin $repoUrl
    Write-Host "✓ Remote origin set to: $repoUrl" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "================================================================================"
    Write-Host "Step 6: Push to GitHub"
    Write-Host "================================================================================"
    
    git branch -M main
    Write-Host "✓ Branch renamed to 'main'" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    Write-Host "(You may be prompted to sign in to GitHub)" -ForegroundColor Yellow
    Write-Host ""
    
    git push -u origin main
    
    Write-Host ""
    Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "================================================================================"
    Write-Host "Step 7: Enable GitHub Pages"
    Write-Host "================================================================================"
    Write-Host ""
    Write-Host "Final steps:" -ForegroundColor Yellow
    Write-Host "1. Go to your repository on GitHub" -ForegroundColor Cyan
    Write-Host "2. Click 'Settings' tab" -ForegroundColor Cyan
    Write-Host "3. Click 'Pages' in the left sidebar" -ForegroundColor Cyan
    Write-Host "4. Under 'Source', select 'Deploy from a branch'" -ForegroundColor Cyan
    Write-Host "5. Select 'main' branch and '/ (root)' folder" -ForegroundColor Cyan
    Write-Host "6. Click 'Save'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your site will be live at:" -ForegroundColor Green
    
    # Extract username and repo name from URL
    if ($repoUrl -match 'github\.com[:/]([^/]+)/([^/.]+)') {
        $username = $matches[1]
        $reponame = $matches[2]
        Write-Host "https://$username.github.io/$reponame/" -ForegroundColor Cyan
    }
}
else {
    Write-Host ""
    Write-Host "Skipped remote setup." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To push to GitHub later, run:" -ForegroundColor Cyan
    Write-Host "  git remote add origin <your-repo-url>" -ForegroundColor Gray
    Write-Host "  git branch -M main" -ForegroundColor Gray
    Write-Host "  git push -u origin main" -ForegroundColor Gray
}

Write-Host ""
Write-Host "================================================================================"
Write-Host "Deployment Complete!"
Write-Host "================================================================================"
Write-Host ""
Write-Host "Files ready for GitHub Pages:" -ForegroundColor Green
Write-Host "  ✓ index.html (Distribution List Selector)" -ForegroundColor Green
Write-Host "  ✓ all_distribution_lists.csv (134,681 lists)" -ForegroundColor Green
Write-Host "  ✓ DEPLOYMENT.md (Documentation)" -ForegroundColor Green
Write-Host ""
Write-Host "See DEPLOYMENT.md for more details and troubleshooting." -ForegroundColor Cyan
Write-Host "================================================================================"
