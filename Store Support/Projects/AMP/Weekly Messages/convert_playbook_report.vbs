Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

sourceFolder = "C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\AMP\Weekly Messages\Docs"
destinationPath = "C:\Users\krush\Walmart Inc\ATC Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx"

' Find the most recent CSV file
Set objFolder = objFSO.GetFolder(sourceFolder)
Set objFiles = objFolder.Files

Dim latestFile, latestTime
latestTime = 0

For Each objFile In objFiles
    If InStr(objFile.Name, "Activity - Playbook Hub and Active Playbooks") > 0 And InStr(objFile.Name, ".csv") > 0 Then
        fileTime = objFile.DateLastModified
        If fileTime > latestTime Then
            latestTime = fileTime
            Set latestFile = objFile
        End If
    End If
Next

If latestFile Is Nothing Then
    WScript.Echo "✗ No Playbook Hub CSV file found"
    WScript.Quit 1
End If

csvPath = latestFile.Path
WScript.Echo "Found source file: " & csvPath
WScript.Echo "Converting to: " & destinationPath

' Create directory if needed
destFolder = objFSO.GetParentFolderName(destinationPath)
If Not objFSO.FolderExists(destFolder) Then
    objFSO.CreateFolder destFolder
End If

' Convert CSV to XLSX using Excel COM object
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False
objExcel.DisplayAlerts = False

On Error Resume Next
Set objWorkbook = objExcel.Workbooks.Open(csvPath, 3)
If Err.Number <> 0 Then
    WScript.Echo "✗ Error opening CSV: " & Err.Description
    objExcel.Quit
    WScript.Quit 1
End If

objWorkbook.SaveAs destinationPath, 51
objWorkbook.Close
objExcel.Quit
Set objExcel = Nothing

WScript.Echo "✓ Successfully converted and saved to: " & destinationPath
WScript.Echo "✓ Playbook Hub report processed successfully at " & Now()
WScript.Quit 0
