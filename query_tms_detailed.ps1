# Query TMS Data (3).xlsx columns using PowerShell COM

$ExcelFile = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"

Write-Host "=" * 80
Write-Host "TMS DATA (3).XLSX - COLUMN ANALYSIS"
Write-Host "=" * 80

# Create Excel COM object
$Excel = New-Object -ComObject Excel.Application
$Excel.Visible = $false

try {
    # Open workbook
    $Workbook = $Excel.Workbooks.Open($ExcelFile)
    $Worksheet = $Workbook.Sheets.Item(1)
    
    $UsedRange = $Worksheet.UsedRange
    $Rows = $UsedRange.Rows.Count
    $Cols = $UsedRange.Columns.Count
    
    Write-Host "`n✓ File loaded: TMS Data (3).xlsx"
    Write-Host "`nDimensions: $Rows rows × $Cols columns"
    
    Write-Host "`n" + ("=" * 80)
    Write-Host "`n📋 ALL COLUMN HEADERS (Row 1):"
    Write-Host ("-" * 80)
    
    $ColumnNames = @()
    for ($col = 1; $col -le $Cols; $col++) {
        $CellValue = $Worksheet.Cells.Item(1, $col).Value()
        $ColumnNames += $CellValue
        Write-Host "  Column $($col.ToString().PadLeft(2)): $CellValue"
    }
    
    Write-Host "`n" + ("=" * 80)
    Write-Host "`n📊 FIRST 5 DATA ROWS (Preview):"
    Write-Host ("-" * 80)
    
    for ($row = 2; $row -le [Math]::Min(6, $Rows); $row++) {
        $RowData = @()
        for ($col = 1; $col -le [Math]::Min(5, $Cols); $col++) {
            $CellValue = $Worksheet.Cells.Item($row, $col).Value()
            $DisplayValue = if ($null -eq $CellValue) { "None" } else { $CellValue.ToString().Substring(0, [Math]::Min(12, $CellValue.ToString().Length)) }
            $RowData += $DisplayValue
        }
        Write-Host "  Row $row`: $($RowData -join ' | ')"
    }
    
    Write-Host "`n" + ("=" * 80)
    Write-Host "TOTAL COLUMNS: $Cols"
    Write-Host "TOTAL ROWS: $Rows"
    Write-Host "`nCOLUMN NAMES:"
    Write-Host ("-" * 80)
    for ($i = 0; $i -lt $ColumnNames.Count; $i++) {
        Write-Host ("{0,2}. {1}" -f ($i+1), $ColumnNames[$i])
    }
    Write-Host "=" * 80
    
    $Workbook.Close($false)
}
catch {
    Write-Host "Error: $_"
}
finally {
    $Excel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Excel) | Out-Null
    Remove-Variable Excel -ErrorAction SilentlyContinue
}
