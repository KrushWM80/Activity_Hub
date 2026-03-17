# Read TMS Data (3).xlsx structure and export details
$FilePath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"

$Excel = New-Object -ComObject Excel.Application
$Excel.Visible = $false

try {
    $Workbook = $Excel.Workbooks.Open($FilePath)
    $Worksheet = $Workbook.Sheets.Item(1)
    
    $UsedRange = $Worksheet.UsedRange
    $Rows = $UsedRange.Rows.Count
    $Cols = $UsedRange.Columns.Count
    
    Write-Host "=============================================================================="
    Write-Host "TMS DATA (3).XLSX - COMPLETE STRUCTURE ANALYSIS"
    Write-Host "=============================================================================="
    Write-Host ""
    Write-Host "File: $FilePath"
    Write-Host "Dimensions: $Rows rows x $Cols columns"
    Write-Host ""
    
    # Get all column headers
    Write-Host "COLUMN HEADERS:"
    Write-Host "=============================================================================="
    $ColumnHeaders = @()
    for ($col = 1; $col -le $Cols; $col++) {
        $ColumnName = $Worksheet.Cells.Item(1, $col).Value
        $ColumnHeaders += $ColumnName
        Write-Host "$col`t$ColumnName"
    }
    Write-Host ""
    
    # Get first 10 data rows
    Write-Host "FIRST 10 DATA ROWS (showing all columns):"
    Write-Host "=============================================================================="
    for ($row = 2; $row -le [Math]::Min($Rows, 11); $row++) {
        $RowOutput = "Row $row`t"
        for ($col = 1; $col -le $Cols; $col++) {
            $CellValue = $Worksheet.Cells.Item($row, $col).Value
            $DisplayValue = if ($null -eq $CellValue) { "[empty]" } else { $CellValue }
            if ($col -lt $Cols) {
                $RowOutput += "$DisplayValue`t"
            } else {
                $RowOutput += "$DisplayValue"
            }
        }
        Write-Host $RowOutput
    }
    
    Write-Host ""
    Write-Host "=============================================================================="
    Write-Host "SUMMARY:"
    Write-Host "  Total Columns: $Cols"
    Write-Host "  Total Rows: $Rows"
    Write-Host "  Column List: $($ColumnHeaders -join ', ')"
    Write-Host "=============================================================================="
    
    $Workbook.Close($false)
}
catch {
    Write-Host "ERROR: $_"
}
finally {
    $Excel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Excel) | Out-Null
}
