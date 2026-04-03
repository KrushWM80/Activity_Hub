# TDA Backend Watchdog - Checks port 5000 and restarts if down
# Runs via scheduled task every 5 minutes

$logFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights\watchdog.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    $tcp = New-Object System.Net.Sockets.TcpClient
    $tcp.Connect("localhost", 5000)
    $tcp.Close()
    # Port is open - backend running
} catch {
    # Port closed - restart backend
    "$timestamp [WATCHDOG] Port 5000 down - restarting backend..." | Out-File -Append $logFile

    $python = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
    $script = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights\backend_simple.py"
    $workDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights"
    $creds = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"

    # Use cmd /c with SET so env var is inherited by the python child process
    $cmdArgs = "/c `"set GOOGLE_APPLICATION_CREDENTIALS=$creds && cd /d `"$workDir`" && `"$python`" `"$script`"`""
    Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs -WindowStyle Hidden
    Start-Sleep -Seconds 15

    # Verify it came back
    try {
        $tcp2 = New-Object System.Net.Sockets.TcpClient
        $tcp2.Connect("localhost", 5000)
        $tcp2.Close()
        "$timestamp [WATCHDOG] Backend restarted successfully" | Out-File -Append $logFile
    } catch {
        "$timestamp [WATCHDOG] ERROR: Backend failed to restart" | Out-File -Append $logFile
    }
}
