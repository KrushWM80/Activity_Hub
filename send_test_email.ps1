# Send test email to kendall.rush@walmart.com

try {
    Write-Host "Testing SMTP connectivity to smtp-gw1.homeoffice.wal-mart.com:25..."
    
    $smtp = New-Object Net.Mail.SmtpClient
    $smtp.Host = "smtp-gw1.homeoffice.wal-mart.com"
    $smtp.Port = 25
    $smtp.Timeout = 5000
    
    $email = New-Object System.Net.Mail.MailMessage
    $email.From = "activity-hub@walmart.com"
    $email.To.Add("kendall.rush@walmart.com")
    $email.Subject = "Test Email - Impact Platform Projects Dashboard"
    
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; color: #333; }
        h2 { color: #0071CE; }
    </style>
</head>
<body>
    <h2>Impact Platform - Test Email</h2>
    <p>Hi Kendall,</p>
    <p>This is a test email from the Activity Hub Projects Dashboard.</p>
    <h3>Test Information:</h3>
    <ul>
        <li><strong>Sent At:</strong> $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')</li>
        <li><strong>From:</strong> activity-hub@walmart.com</li>
        <li><strong>To:</strong> kendall.rush@walmart.com</li>
        <li><strong>Server:</strong> smtp-gw1.homeoffice.wal-mart.com:25</li>
    </ul>
    <p>✅ If you received this email successfully, the email system is working correctly!</p>
    <hr/>
    <p style="font-size: 12px; color: #666;">
        Activity Hub Projects Dashboard | 
        <a href="http://weus42608431466:8088/activity-hub/projects">View Dashboard</a>
    </p>
</body>
</html>
"@
    
    $email.Body = $html
    $email.IsBodyHtml = $true
    
    Write-Host "Sending email to kendall.rush@walmart.com..."
    $smtp.Send($email)
    Write-Host "✅ SUCCESS: Email sent to kendall.rush@walmart.com!"
    Write-Host "   Sent At: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    
    $email.Dispose()
    $smtp.Dispose()
    
} catch {
    Write-Host "❌ ERROR: $_"
    exit 1
}
