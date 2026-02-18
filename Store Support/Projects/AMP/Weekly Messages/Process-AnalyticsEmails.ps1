# PowerShell Script to Process Adobe Analytics Weekly Email Attachments
# This script converts CSV attachments from Outlook to XLSX and saves to destination paths

# Define paths
$sourceFolder = "C:\Users\krush\Documents\VSCode\AMP\Weekly Messages\Docs"
$destinationPaths = @{
    "Weekly Messages Area Reports - Tables FY27.csv" = "C:\Users\krush\Walmart Inc\ATC Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Weekly Messages Area Reports - Tables FY27.xlsx"
    "Activity - Playbook Hub and Active Playbooks.csv" = "C:\Users\krush\Walmart Inc\ATC Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx"
}

# Create source folder if it doesn't exist
if (-not (Test-Path $sourceFolder)) {
    New-Item -ItemType Directory -Path $sourceFolder -Force | Out-Null
    Write-Host "Created source folder: $sourceFolder"
}

# Function to convert CSV to XLSX
function Convert-CsvToXlsx {
    param(
        [string]$csvPath,
        [string]$xlsxPath
    )
    
    try {
        # Create Excel COM object
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $false
        $excel.DisplayAlerts = $false
        
        # Open CSV file
        $workbook = $excel.Workbooks.Open($csvPath, 3)  # 3 = comma-delimited
        
        # Save as XLSX
        $workbook.SaveAs($xlsxPath, 51)  # 51 = XLSX format
        $workbook.Close()
        $excel.Quit()
        
        # Release COM objects
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
        [GC]::Collect()
        
        Write-Host "✓ Converted: $(Split-Path $csvPath -Leaf) → $(Split-Path $xlsxPath -Leaf)"
        return $true
    }
    catch {
        Write-Host "✗ Error converting $csvPath : $_"
        return $false
    }
}

# Main processing function
function Process-AttachedFiles {
    Write-Host "Scanning for new CSV files in: $sourceFolder"
    
    $csvFiles = Get-ChildItem -Path $sourceFolder -Filter "*.csv" -ErrorAction SilentlyContinue
    
    if ($csvFiles.Count -eq 0) {
        Write-Host "No CSV files found."
        return
    }
    
    foreach ($file in $csvFiles) {
        $fileName = $file.Name
        
        # Find matching destination
        $matchedKey = $null
        foreach ($key in $destinationPaths.Keys) {
            if ($fileName -like "*$($key.Replace('.csv', ''))*") {
                $matchedKey = $key
                break
            }
        }
        
        if ($matchedKey) {
            $destinationPath = $destinationPaths[$matchedKey]
            
            # Ensure destination folder exists
            $destFolder = Split-Path $destinationPath -Parent
            if (-not (Test-Path $destFolder)) {
                New-Item -ItemType Directory -Path $destFolder -Force | Out-Null
            }
            
            # Convert CSV to XLSX
            $success = Convert-CsvToXlsx -csvPath $file.FullName -xlsxPath $destinationPath
            
            if ($success) {
                # Move processed CSV to archive subfolder
                $archiveFolder = Join-Path $sourceFolder "Archive"
                if (-not (Test-Path $archiveFolder)) {
                    New-Item -ItemType Directory -Path $archiveFolder -Force | Out-Null
                }
                Move-Item -Path $file.FullName -Destination (Join-Path $archiveFolder $fileName) -Force
                Write-Host "Archived original CSV"
            }
        }
        else {
            Write-Host "⚠ No matching destination found for: $fileName"
        }
    }
    
    Write-Host "Processing complete!"
}

# Run the process
Process-AttachedFiles
