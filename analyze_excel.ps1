# Use COM to read Excel file
$ExcelFile = "Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"

$Excel = New-Object -ComObject Excel.Application
$Excel.Visible = $false
$Workbook = $Excel.Workbooks.Open((Get-Item $ExcelFile).FullName)

Write-Host "=== SHEET NAMES ===" 
$SheetNames = @()
foreach ($Sheet in $Workbook.Sheets) {
    $SheetNames += $Sheet.Name
    Write-Host $Sheet.Name
}
Write-Host ""

# Analyze each sheet
foreach ($SheetName in $SheetNames) {
    $Worksheet = $Workbook.Sheets($SheetName)
    
    Write-Host "=== SHEET: $SheetName ===" 
    
    # Get used range
    $UsedRange = $Worksheet.UsedRange
    $Rows = $UsedRange.Rows.Count
    $Cols = $UsedRange.Columns.Count
    
    Write-Host "Dimensions: $Rows rows, $Cols columns"
    Write-Host ""
    
    # Get column headers (first row)
    Write-Host "COLUMN NAMES (exactly as they appear):"
    $ColumnNames = @()
    for ($i = 1; $i -le $Cols; $i++) {
        $CellValue = $Worksheet.Cells.Item(1, $i).Value2
        $ColumnNames += $CellValue
        Write-Host "  Column $i : $CellValue"
    }
    Write-Host ""
    
    # Get first 5 rows of data (rows 2-6, since row 1 is header)
    Write-Host "FIRST 5 DATA ROWS (excluding header):"
    Write-Host ""
    
    for ($row = 2; $row -le 6; $row++) {
        Write-Host "Row $($row-1):"
        for ($col = 1; $col -le $Cols; $col++) {
            $ColumnName = $ColumnNames[$col-1]
            $CellValue = $Worksheet.Cells.Item($row, $col).Value2
            if ($CellValue -ne $null) {
                Write-Host "  $ColumnName : $CellValue"
            } else {
                Write-Host "  $ColumnName : (empty)"
            }
        }
        Write-Host ""
    }
    
    Write-Host "============================================================"
}

$Workbook.Close($false)
$Excel.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($Excel) | Out-Null
