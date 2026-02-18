Add-Type -AssemblyName System.Web

$port = 8080
$url = "http://localhost:$port/"

Write-Host "Starting HTTP Server on port $port..."
Write-Host "Dashboard available at: $url"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

Write-Host "Server started! Open: $url"

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    $localPath = $request.Url.LocalPath
    if ($localPath -eq "/") { $localPath = "/index.html" }
    
    $filePath = Join-Path (Get-Location) $localPath.TrimStart('/')
    
    Write-Host "Request: $localPath"
    
    if (Test-Path $filePath) {
        $contentType = switch ([System.IO.Path]::GetExtension($filePath)) {
            ".html" { "text/html" }
            ".css"  { "text/css" }
            ".js"   { "application/javascript" }
            ".csv"  { "text/csv" }
            ".json" { "application/json" }
            ".svg"  { "image/svg+xml" }
            default { "text/plain" }
        }
        
        $response.Headers.Add("Access-Control-Allow-Origin", "*")
        $response.ContentType = $contentType
        
        $content = [System.IO.File]::ReadAllBytes($filePath)
        $response.ContentLength64 = $content.Length
        $response.OutputStream.Write($content, 0, $content.Length)
        $response.StatusCode = 200
    } else {
        $response.StatusCode = 404
        $errorMsg = "File not found: $localPath"
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($errorMsg)
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
        Write-Host "404: $localPath"
    }
    
    $response.Close()
}