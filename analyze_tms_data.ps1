$ExcelFile = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"

# Use COM object to read Excel file without dependencies
$Excel = New-Object -ComObject Excel.Application
$Excel.Visible = $false

$Workbook = $Excel.Workbooks.Open($ExcelFile)
$Worksheet = $Workbook.Sheets.Item(1)

$UsedRange = $Worksheet.UsedRange
$Rows = $UsedRange.Rows.Count
$Cols = $UsedRange.Columns.Count

Write-Host "=" * 80
Write-Host "TMS DATA (3).XLSX - STRUCTURE ANALYSIS"
Write-Host "=" * 80

Write-Host "`nShape: $Rows rows × $Cols columns"

Write-Host "`nColumn Names (Row 1):"
for ($col = 1; $col -le $Cols; $col++) {
    $CellValue = $Worksheet.Cells.Item(1, $col).Value()
    Write-Host "  $col. $CellValue"
}

Write-Host "`nFirst 5 Data Rows:"
Write-Host ""
for ($row = 1; $row -le [Math]::Min(6, $Rows); $row++) {
    $RowData = @()
    for ($col = 1; $col -le [Math]::Min(10, $Cols); $col++) {
        $CellValue = $Worksheet.Cells.Item($row, $col).Value()
        $RowData += "$CellValue"
    }
    Write-Host ($RowData -join " | ")
}

$Workbook.Close($false)
$Excel.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($Excel) | Out-Null

Write-Host "`n" + ("=" * 80)
Write-Host "Analysis complete"
