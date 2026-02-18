# Simple PowerShell HTTP Server
$port = 8080
$url = "http://localhost:$port/"

Write-Host "Starting HTTP Server on port $port..."
Write-Host "Dashboard will be available at: $url"
Write-Host "Press Ctrl+C to stop the server"

# Create HTTP listener
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

Write-Host "Server started successfully!"
Write-Host "Open your browser to: $url"

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        # Get the requested file path
        $localPath = $request.Url.LocalPath
        if ($localPath -eq "/") { $localPath = "/index.html" }
        
        $filePath = Join-Path (Get-Location) $localPath.TrimStart('/')
        
        Write-Host "Request: $($request.HttpMethod) $localPath"
        
        if (Test-Path $filePath -PathType Leaf) {
            # Determine content type
            $contentType = switch ([System.IO.Path]::GetExtension($filePath).ToLower()) {
                ".html" { "text/html; charset=utf-8" }
                ".css"  { "text/css; charset=utf-8" }
                ".js"   { "application/javascript; charset=utf-8" }
                ".csv"  { "text/csv; charset=utf-8" }
                ".json" { "application/json; charset=utf-8" }
                default { "application/octet-stream" }
            }
            
            # Set CORS headers
            $response.Headers.Add("Access-Control-Allow-Origin", "*")
            $response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            $response.Headers.Add("Access-Control-Allow-Headers", "Content-Type")
            
            # Read and serve the file
            $content = Get-Content $filePath -Raw -Encoding UTF8
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($content)
            
            $response.ContentType = $contentType
            $response.ContentLength64 = $buffer.Length
            $response.StatusCode = 200
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        } else {
            # File not found
            $response.StatusCode = 404
            $errorMessage = "File not found: $localPath"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($errorMessage)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        }
        
        $response.Close()
    }
} finally {
    $listener.Stop()
    Write-Host "Server stopped."
}