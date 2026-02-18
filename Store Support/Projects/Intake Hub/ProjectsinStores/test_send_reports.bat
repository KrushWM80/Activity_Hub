@echo off
REM Test script to send both email reports

echo.
echo Testing Email Reports...
echo.

REM Report 1: Kendall's Daily
echo [1] Sending "Kendall's Daily" report...
powershell -Command "try { $body = @{ 'config_id' = '4b80e040-b338-4489-b8ff-6b3f8f5ee4be'; 'override_email' = 'kendall.rush@walmart.com' } | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:8001/api/reports/generate' -Method Post -ContentType 'application/json' -Body $body -UseBasicParsing; Write-Host '✅ Response Status:' $response.StatusCode; $result = $response.Content | ConvertFrom-Json; Write-Host '   Message:' $result.message; Write-Host '   Sent to:' ($result.sent_to -join ', ') } catch { Write-Host '❌ Error:' $_.Exception.Message }"

echo.
echo [2] Sending "New Projects & Daily Recap" report...
powershell -Command "try { $body = @{ 'config_id' = '6058279f-4f63-411d-adce-3c826b95687e'; 'override_email' = 'kendall.rush@walmart.com' } | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:8001/api/reports/generate' -Method Post -ContentType 'application/json' -Body $body -UseBasicParsing; Write-Host '✅ Response Status:' $response.StatusCode; $result = $response.Content | ConvertFrom-Json; Write-Host '   Message:' $result.message; Write-Host '   Sent to:' ($result.sent_to -join ', ') } catch { Write-Host '❌ Error:' $_.Exception.Message }"

echo.
echo Done! Check your email for the reports.
echo.
pause
