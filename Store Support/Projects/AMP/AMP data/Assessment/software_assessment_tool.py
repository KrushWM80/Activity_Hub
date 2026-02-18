#!/usr/bin/env python3
"""
Software Environment Assessment Tool
Checks what software is installed vs what's needed for the AMP BigQuery Trigger System

This tool will help identify what software you have and what needs to be installed
for the complete BigQuery trigger deployment.
"""

import subprocess
import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SoftwareAssessment:
    def __init__(self):
        self.required_software = {
            "essential": {
                "Google Cloud CLI (gcloud)": {
                    "check_command": ["gcloud", "version"],
                    "install_url": "https://cloud.google.com/sdk/docs/install",
                    "description": "Essential for BigQuery operations and Cloud Function deployment",
                    "windows_installer": "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
                },
                "Git": {
                    "check_command": ["git", "--version"],
                    "install_url": "https://git-scm.com/download/windows",
                    "description": "Version control and includes Git Bash terminal",
                    "windows_installer": "https://github.com/git-for-windows/git/releases/latest"
                },
                "Python 3.8+": {
                    "check_command": ["python", "--version"],
                    "install_url": "https://www.python.org/downloads/",
                    "description": "Already available in your environment",
                    "status": "✅ Already Available"
                }
            },
            "recommended": {
                "BigQuery CLI (bq)": {
                    "check_command": ["bq", "version"],
                    "install_url": "Included with Google Cloud CLI",
                    "description": "Command-line tool for BigQuery operations",
                    "note": "Installed automatically with Google Cloud CLI"
                },
                "Terraform": {
                    "check_command": ["terraform", "version"],
                    "install_url": "https://www.terraform.io/downloads.html",
                    "description": "Infrastructure as Code for advanced deployments",
                    "windows_installer": "https://releases.hashicorp.com/terraform/"
                },
                "curl": {
                    "check_command": ["curl", "--version"],
                    "install_url": "Usually pre-installed on Windows 10+",
                    "description": "For testing HTTP endpoints and API calls"
                }
            },
            "optional": {
                "Visual Studio Code": {
                    "check_command": ["code", "--version"],
                    "install_url": "https://code.visualstudio.com/download",
                    "description": "Code editor with Google Cloud extensions",
                    "status": "✅ Already Available (in use)"
                },
                "Docker": {
                    "check_command": ["docker", "--version"],
                    "install_url": "https://www.docker.com/products/docker-desktop",
                    "description": "For containerized deployments (optional)"
                }
            }
        }
        
        self.assessment_results = {}
    
    def check_software_installed(self, command: List[str]) -> Tuple[bool, str]:
        """Check if software is installed by running a command"""
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False, "Command not found or timed out"
    
    def check_python_packages(self) -> Dict[str, bool]:
        """Check if required Python packages are installed"""
        required_packages = {
            "google-cloud-bigquery": "Google BigQuery client library",
            "google-cloud-functions-framework": "Cloud Functions development",
            "google-auth": "Google authentication",
            "pandas": "Data manipulation (useful for testing)",
            "requests": "HTTP requests library"
        }
        
        package_status = {}
        for package, description in required_packages.items():
            try:
                __import__(package.replace('-', '_'))
                package_status[package] = True
            except ImportError:
                package_status[package] = False
        
        return package_status
    
    def check_environment_variables(self) -> Dict[str, Optional[str]]:
        """Check important environment variables"""
        important_vars = {
            "GOOGLE_APPLICATION_CREDENTIALS": "Google Cloud service account key",
            "GOOGLE_CLOUD_PROJECT": "Default Google Cloud project",
            "PATH": "System PATH (should include gcloud)",
            "USERPROFILE": "User profile directory",
            "COMPUTERNAME": "Computer name"
        }
        
        env_status = {}
        for var, description in important_vars.items():
            env_status[var] = {
                "value": os.environ.get(var),
                "description": description,
                "set": var in os.environ
            }
        
        return env_status
    
    def assess_all_software(self) -> Dict:
        """Run complete software assessment"""
        print("🔍 Running Software Environment Assessment...")
        print("=" * 60)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {
                "platform": sys.platform,
                "python_version": sys.version,
                "python_executable": sys.executable
            },
            "software_status": {},
            "python_packages": self.check_python_packages(),
            "environment_variables": self.check_environment_variables(),
            "recommendations": []
        }
        
        # Check all software categories
        for category, software_list in self.required_software.items():
            print(f"\n📂 {category.upper()} SOFTWARE:")
            print("-" * 40)
            
            results["software_status"][category] = {}
            
            for software_name, software_info in software_list.items():
                if "status" in software_info:
                    # Pre-determined status
                    status = True
                    version = software_info["status"]
                    print(f"   {software_name}: {version}")
                else:
                    # Check dynamically
                    status, version = self.check_software_installed(software_info["check_command"])
                    status_icon = "✅" if status else "❌"
                    print(f"   {software_name}: {status_icon} {version[:50] if len(version) > 50 else version}")
                
                results["software_status"][category][software_name] = {
                    "installed": status,
                    "version": version,
                    "install_url": software_info["install_url"],
                    "description": software_info["description"]
                }
                
                # Add recommendations for missing essential software
                if not status and category == "essential":
                    results["recommendations"].append({
                        "priority": "HIGH",
                        "software": software_name,
                        "action": f"Install {software_name}",
                        "url": software_info["install_url"]
                    })
        
        # Check Python packages
        print(f"\n🐍 PYTHON PACKAGES:")
        print("-" * 40)
        for package, installed in results["python_packages"].items():
            status_icon = "✅" if installed else "❌"
            print(f"   {package}: {status_icon}")
            
            if not installed:
                results["recommendations"].append({
                    "priority": "MEDIUM",
                    "software": package,
                    "action": f"pip install {package}",
                    "command": f"pip install {package}"
                })
        
        # Check environment variables
        print(f"\n🌍 ENVIRONMENT VARIABLES:")
        print("-" * 40)
        for var, info in results["environment_variables"].items():
            status_icon = "✅" if info["set"] else "❌"
            value_display = "***SET***" if info["set"] else "NOT SET"
            if var == "PATH" and info["set"]:
                value_display = "***SET*** (PATH is configured)"
            print(f"   {var}: {status_icon} {value_display}")
        
        return results
    
    def generate_installation_guide(self, results: Dict) -> str:
        """Generate detailed installation guide"""
        
        guide = f"""# AMP BigQuery Trigger System - Installation Guide

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**System:** {results['system_info']['platform']}

## 🚨 Required Actions

### Essential Software Missing:
"""
        
        essential_missing = []
        for software, info in results["software_status"]["essential"].items():
            if not info["installed"]:
                essential_missing.append((software, info))
        
        if essential_missing:
            for software, info in essential_missing:
                guide += f"""
#### {software}
- **Status**: ❌ Not Installed
- **Description**: {info['description']}
- **Install From**: {info['install_url']}
- **Action Required**: Download and install before proceeding
"""
        else:
            guide += "\n✅ All essential software is installed!\n"
        
        # Python packages
        missing_packages = [pkg for pkg, installed in results["python_packages"].items() if not installed]
        if missing_packages:
            guide += f"""
### Python Packages Missing:
```bash
pip install {' '.join(missing_packages)}
```
"""
        
        # Environment setup
        guide += """
## 🔧 Environment Setup Steps

### 1. Google Cloud CLI Setup
```bash
# After installing gcloud, authenticate
gcloud auth login

# Set your project
gcloud config set project wmt-assetprotection-prod

# Enable required APIs
gcloud services enable bigquery.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable pubsub.googleapis.com
```

### 2. BigQuery Authentication
```bash
# Create and download service account key
gcloud iam service-accounts create bigquery-data-sync --display-name="BigQuery Data Sync"

# Grant necessary permissions
gcloud projects add-iam-policy-binding wmt-assetprotection-prod \
    --member="serviceAccount:bigquery-data-sync@wmt-assetprotection-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding wmt-assetprotection-prod \
    --member="serviceAccount:bigquery-data-sync@wmt-assetprotection-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

# Download key
gcloud iam service-accounts keys create key.json \
    --iam-account=bigquery-data-sync@wmt-assetprotection-prod.iam.gserviceaccount.com

# Set environment variable
set GOOGLE_APPLICATION_CREDENTIALS=key.json
```

### 3. Test Your Setup
```bash
# Test BigQuery access
bq ls wmt-assetprotection-prod:Store_Support

# Test Cloud Functions access  
gcloud functions list --project=wmt-assetprotection-prod
```

## 📥 Download Links

### Essential Downloads:
"""
        
        # Add download links for missing software
        for software, info in results["software_status"]["essential"].items():
            if not info["installed"]:
                guide += f"- **{software}**: {info['install_url']}\n"
        
        guide += """
### Recommended Downloads:
- **Git for Windows**: https://git-scm.com/download/windows (includes Git Bash)
- **Google Cloud CLI**: https://cloud.google.com/sdk/docs/install-sdk

## 🚀 Deployment Checklist

After installing missing software:

1. ✅ Run BigQuery SQL to create tables and procedures
2. ✅ Set up Google Cloud authentication  
3. ✅ Deploy Cloud Functions using the deployment script
4. ✅ Test the trigger system
5. ✅ Set up monitoring

## 🆘 Troubleshooting

### Common Issues:
- **"gcloud not found"**: Add Google Cloud CLI to your PATH
- **Authentication errors**: Run `gcloud auth login` 
- **Permission denied**: Check service account permissions
- **BigQuery access denied**: Verify project and dataset permissions

### Get Help:
- Google Cloud Documentation: https://cloud.google.com/docs
- BigQuery Documentation: https://cloud.google.com/bigquery/docs
"""
        
        return guide
    
    def generate_quick_install_script(self, results: Dict) -> str:
        """Generate PowerShell script for quick installation"""
        
        script = """# AMP BigQuery Trigger System - Quick Install Script (PowerShell)
# Run this script as Administrator to install missing software

Write-Host "🚀 AMP BigQuery Trigger System - Quick Install" -ForegroundColor Green
Write-Host "=" * 50

# Function to check if software is installed
function Test-SoftwareInstalled {
    param([string]$Command)
    try {
        & $Command --version 2>$null
        return $true
    } catch {
        return $false
    }
}

# Install Chocolatey if not present (package manager for Windows)
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing Chocolatey package manager..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install Git (includes Git Bash)
if (!(Test-SoftwareInstalled "git")) {
    Write-Host "📥 Installing Git for Windows..." -ForegroundColor Yellow
    choco install git -y
} else {
    Write-Host "✅ Git already installed" -ForegroundColor Green
}

# Install Google Cloud CLI
if (!(Test-SoftwareInstalled "gcloud")) {
    Write-Host "☁️ Installing Google Cloud CLI..." -ForegroundColor Yellow
    choco install gcloudsdk -y
} else {
    Write-Host "✅ Google Cloud CLI already installed" -ForegroundColor Green
}

# Install curl (usually pre-installed on Windows 10+)
if (!(Test-SoftwareInstalled "curl")) {
    Write-Host "🌐 Installing curl..." -ForegroundColor Yellow
    choco install curl -y
} else {
    Write-Host "✅ curl already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Installation Complete!" -ForegroundColor Green
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Restart your terminal/PowerShell" -ForegroundColor White
Write-Host "2. Run: gcloud auth login" -ForegroundColor White
Write-Host "3. Run: gcloud config set project wmt-assetprotection-prod" -ForegroundColor White
Write-Host "4. Execute the BigQuery SQL scripts" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
"""
        
        return script

def main():
    """Run complete software assessment"""
    
    assessor = SoftwareAssessment()
    results = assessor.assess_all_software()
    
    # Generate reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Save detailed results as JSON
    results_filename = f"software_assessment_{timestamp}.json"
    with open(results_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # 2. Generate installation guide
    guide = assessor.generate_installation_guide(results)
    guide_filename = f"installation_guide_{timestamp}.md"
    with open(guide_filename, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    # 3. Generate quick install script
    install_script = assessor.generate_quick_install_script(results)
    script_filename = f"quick_install_{timestamp}.ps1"
    with open(script_filename, 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    # Print summary
    print(f"\n📊 ASSESSMENT SUMMARY:")
    print("=" * 60)
    
    total_essential = len(results["software_status"]["essential"])
    installed_essential = sum(1 for info in results["software_status"]["essential"].values() if info["installed"])
    
    total_packages = len(results["python_packages"])
    installed_packages = sum(1 for installed in results["python_packages"].values() if installed)
    
    print(f"Essential Software: {installed_essential}/{total_essential} installed")
    print(f"Python Packages: {installed_packages}/{total_packages} installed")
    print(f"Recommendations: {len(results['recommendations'])} actions needed")
    
    print(f"\n📁 Files Generated:")
    print(f"   • {results_filename} - Detailed assessment results")
    print(f"   • {guide_filename} - Installation guide")
    print(f"   • {script_filename} - Quick install script (PowerShell)")
    
    if results["recommendations"]:
        print(f"\n🚨 HIGH PRIORITY ACTIONS:")
        for rec in results["recommendations"]:
            if rec["priority"] == "HIGH":
                print(f"   • {rec['action']}")
                if "url" in rec:
                    print(f"     URL: {rec['url']}")
    
    print(f"\n💡 Next Steps:")
    print("1. Review the installation guide")
    print("2. Install missing essential software") 
    print("3. Run the quick install script as Administrator (optional)")
    print("4. Set up Google Cloud authentication")
    print("5. Deploy the BigQuery trigger system")
    
    return results

if __name__ == "__main__":
    main()