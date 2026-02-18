# PowerShell Script to Convert Weekly Messages Report CSV to XLSX
# Converts the latest CSV file from Docs folder and replaces the XLSX in the destination

$sourceFolder = "C:\Users\krush\Documents\VSCode\AMP\Weekly Messages\Docs"
$destinationPath = "C:\Users\krush\Walmart Inc\ATC Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Weekly Messages Area Reports - Tables FY27.xlsx"

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
        
        Write-Host "✓ Successfully converted and saved to: $xlsxPath"
        return $true
    }
    catch {
        Write-Host "✗ Error converting CSV to XLSX: $_"
        return $false
    }
}

# Main execution
try {
    # Find the most recent Weekly Messages CSV file
    $csvFile = Get-ChildItem -Path $sourceFolder -Filter "*Weekly Messages Area Reports*.csv" -ErrorAction SilentlyContinue | Sort-Object CreationTime -Descending | Select-Object -First 1
    
    if (-not $csvFile) {
        Write-Host "✗ No Weekly Messages CSV file found in: $sourceFolder"
        exit 1
    }
    
    Write-Host "Found source file: $($csvFile.FullName)"
    Write-Host "Converting to: $destinationPath"
    
    # Ensure destination folder exists
    $destFolder = Split-Path $destinationPath -Parent
    if (-not (Test-Path $destFolder)) {
        New-Item -ItemType Directory -Path $destFolder -Force | Out-Null
        Write-Host "Created destination folder"
    }
    
    # Convert CSV to XLSX
    $success = Convert-CsvToXlsx -csvPath $csvFile.FullName -xlsxPath $destinationPath
    
    if ($success) {
        Write-Host "✓ Weekly Messages report processed successfully at $(Get-Date)"
        exit 0
    }
    else {
        Write-Host "✗ Failed to convert file"
        exit 1
    }
}
catch {
    Write-Host "✗ Error: $_"
    exit 1
}
