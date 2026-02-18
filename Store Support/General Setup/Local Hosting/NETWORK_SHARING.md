# Network Sharing Guide

How to share your locally-hosted dashboards with your team on the Walmart VPN/network.

---

## 🎯 Quick Reference

| URL Type | Example | Stable? | Use For |
|----------|---------|---------|---------|
| **Hostname (BEST)** | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080` | ✅ Never changes | Share with team |
| IP Address | `http://10.97.105.88:8080` | ❌ Changes often | Testing only |
| Localhost | `http://localhost:8080` | N/A | Personal dev only |

---

## 🖥️ Your Machine's Hostname

Your laptop has a permanent hostname that resolves to your current IP:

```
LEUS62315243171.homeoffice.Wal-Mart.com
```

To find your hostname, run in PowerShell:
```powershell
[System.Net.Dns]::GetHostEntry($env:COMPUTERNAME).HostName
```

---

## 🚀 Hosting Multiple Services

Use **one hostname + different ports** for multiple dashboards:

| Service | Port | URL |
|---------|------|-----|
| Job Code Teaming | 8080 | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080` |
| Projects in Stores | 8000 | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8000` |
| Another Dashboard | 8081 | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8081` |
| API Service | 8082 | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8082` |

### Recommended Port Ranges
- `8000-8099` - Web dashboards & APIs
- `3000-3099` - Node.js applications
- `5000-5099` - Flask/Python apps

---

## 🔥 Firewall Setup

For each port you want to share, add a firewall rule:

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "My Dashboard 8080" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Projects API 8000" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### Check Existing Rules
```powershell
Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*Dashboard*" -or $_.DisplayName -like "*API*" }
```

### Remove a Rule
```powershell
Remove-NetFirewallRule -DisplayName "My Dashboard 8080"
```

---

## 📋 Server Configuration

Your server must bind to `0.0.0.0` (all interfaces), not just `localhost`:

### FastAPI/Uvicorn
```python
uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Flask
```python
app.run(host="0.0.0.0", port=8080)
```

### Node.js/Express
```javascript
app.listen(8080, '0.0.0.0', () => console.log('Server running'));
```

### Python HTTP Server
```powershell
python -m http.server 8080 --bind 0.0.0.0
```

---

## 🔗 Creating Friendly URLs

### Option 1: SharePoint Redirect (Quick)
Create a simple HTML file that redirects to your hostname:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=http://LEUS62315243171.homeoffice.Wal-Mart.com:8080">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to dashboard...</p>
    <p><a href="http://LEUS62315243171.homeoffice.Wal-Mart.com:8080">Click here</a> if not redirected.</p>
</body>
</html>
```

Upload to SharePoint → Share that link with team.

### Option 2: DNS Alias (Best, requires IT)
Submit IT ticket requesting:
> "Please create DNS CNAME: `jobcode-dashboard.homeoffice.wal-mart.com` pointing to `LEUS62315243171.homeoffice.Wal-Mart.com`"

### Option 3: HOSTS File (Small teams)
Each team member adds to `C:\Windows\System32\drivers\etc\hosts`:
```
10.97.105.88  jobcodedashboard
```
Then access: `http://jobcodedashboard:8080`

---

## ⚠️ IP Address Stability

**Why IP addresses change:**

| Event | IP Changes? |
|-------|-------------|
| Disconnect/reconnect VPN | ✅ Yes |
| Restart computer | ✅ Yes |
| DHCP lease expires (8-24 hrs) | ⚠️ Possibly |
| Switch Wi-Fi/Ethernet | ✅ Yes |
| Different location | ✅ Yes |

**Solution:** Always use the hostname, not IP!

---

## 📝 Startup Script Template

Add this to your dashboard's `start.ps1`:

```powershell
# Get hostname for sharing
$fqdn = [System.Net.Dns]::GetHostEntry($env:COMPUTERNAME).HostName
$port = 8080  # Change per service

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Dashboard Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Share this URL with your team:" -ForegroundColor Green
Write-Host ""
Write-Host "  http://${fqdn}:${port}" -ForegroundColor Yellow
Write-Host ""
Write-Host "(This URL never changes!)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start your server here
python backend/main.py
```

---

## 🧪 Testing Connectivity

### From your machine:
```powershell
# Test localhost
curl http://localhost:8080

# Test hostname
curl http://LEUS62315243171.homeoffice.Wal-Mart.com:8080
```

### From teammate's machine:
```powershell
# Test if they can reach you
Test-NetConnection -ComputerName LEUS62315243171.homeoffice.Wal-Mart.com -Port 8080

# Try the URL
curl http://LEUS62315243171.homeoffice.Wal-Mart.com:8080
```

---

## 📊 Current Services

Track your running services here:

| Service | Port | Status | URL |
|---------|------|--------|-----|
| Job Code Teaming Dashboard | 8080 | Active | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080` |
| Projects in Stores | 8000 | Active | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8000` |

---

## 📚 Related Docs

- [Continuous Server Setup](./Continous%20Running%20Server%20-%20HTTP%20Port/)
- [Scheduled Automation](./Scheduled%20Automation%20System/)
- [Decision Guide](./DECISION_GUIDE.md)
