# Health Checks & Auto-Restart - Quick Start Guide

## What's New
Your monitoring system now includes **3 additional services** with automated health checks and restart capabilities:

1. **TDA Insights** - Port 5000 - Store analytics dashboard
2. **Store Activity Dashboard** - Port 8081 - AMP communication platform  
3. **Zorro Podcast Server** - Port 8888 - Jenny voice audio generation

Plus existing services:
- **Job Codes** - Port 8080 - 24/7 operational
- **Projects in Stores** - Port 8001 - Active

---

## Service URLs

### Access From Your Computer (Localhost)
```
TDA Insights:             http://localhost:5000/dashboard.html
Store Dashboard:          http://localhost:8081/
Zorro Audio Generator:    http://localhost:8888/create-audio
Zorro Index:              http://localhost:8888/
```

### Access From Network (Use IP)
```
Job Codes:                http://10.97.114.181:8080/static/index.html#
Projects in Stores:       http://10.97.114.181:8001/
```

---

## How Health Checks Work

### Automatic Monitoring
```
Every Day at 6:00 AM  → Full health check + email report
On System Startup     → Health check + startup notification
Every 6 Hours         → Job Codes automatic restart cycle
```

### What Gets Checked
✅ Job Codes (Port 8080)  
✅ Projects in Stores (Port 8001)  
✅ TDA Insights (Port 5000)  
✅ Store Activity Dashboard (Port 8081)  
✅ Zorro (Port 8888)  

### If Service is Offline
1. Monitoring detects service not responding
2. Auto-restart function is triggered
3. Service restarts and is verified
4. Status reported in email

---

## Manual Quick Access

### Check Status Right Now
```powershell
# Open PowerShell as Administrator, then run:
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
.\MONITOR_AND_REPORT.ps1
```

This will:
- Check all 5 services
- Auto-restart any that are offline
- Send you a status email

### Start All Services Manually
```powershell
# Kill existing processes
taskkill /F /IM python.exe

# Start each service
Start-ScheduledTask -TaskName "JobCodes-Backend-Server"

# Start others (they'll run in separate windows)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat"
```

### Start Individual Service
```powershell
# TDA Insights
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat"

# Store Dashboard
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat"

# Zorro
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat"
```

---

## Checking Service Status

### See What's Running Right Now
```powershell
# Check all Activity Hub ports
netstat -ano | findstr "LISTENING" | findstr ":5000\|:8001\|:8080\|:8888"
```

You should see lines like:
```
TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING    [PID]
TCP    0.0.0.0:8001           0.0.0.0:0              LISTENING    [PID]
TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING    [PID]
TCP    0.0.0.0:8888           0.0.0.0:0              LISTENING    [PID]
```

### Get Detailed Process Info
```powershell
# Show all Python processes running
Get-Process python | Select-Object Id, ProcessName, CPU, Memory
```

---

## Email Reports

### What You'll Receive
Every morning at 6:00 AM (and on system startup), you'll get an email showing:

**Status Table:**
| Component | Status | Details |
|-----------|--------|---------|
| Job Codes | RUNNING | Port 8080 - Listening |
| Projects | RUNNING | Port 8001 - Listening |
| TDA Insights | RUNNING | Port 5000 - Listening |
| Store Dashboard | RUNNING | Port 8081 - Responding |
| Zorro | RUNNING | Port 8888 - Listening |

**Access Links:** All URLs you need to access each service

**Metrics:** Services running, tasks active, total status

---

## Documentation Files

| File | Location | Purpose |
|------|----------|---------|
| **IMPLEMENTATION_SUMMARY** | Automation/ | Overview of all changes |
| **EXTENDED_HEALTH_CHECKS_README** | Automation/ | Detailed configuration |
| **QUICK_REFERENCE_SERVICES** | Automation/ | Service inventory table |
| **SERVICE_URLs_ACCESS** | Automation/ | Complete URL reference |
| **This Guide** | Automation/ | Quick start instructions |

---

## Troubleshooting

### Service Not Starting?
1. Check log file in service directory (ends with `_server.log`)
2. Look for error messages
3. Make sure Python is installed
4. Verify Google Cloud credentials (TDA and Store Dashboard)

### Can't Access (Localhost)
```powershell
# Check if port is listening
netstat -ano | findstr ":5000"  # For TDA
netstat -ano | findstr ":8080"  # For Store Dashboard
netstat -ano | findstr ":8888"  # For Zorro

# If nothing shows, service isn't running - start it manually
```

### Can't Access (Network - IP)
1. Verify IP is correct: `ipconfig | findstr IPv4`
2. Ping the computer: `ping 10.97.114.181`
3. Check Windows Firewall allows port access
4. Verify service is running on that computer

### Port Already in Use
```powershell
# Find what's using the port
netstat -ano | findstr ":5000"

# Kill process if needed
taskkill /F /PID [PID_NUMBER]

# Restart service
```

---

## Key Points to Remember

📌 **Unique Port Assignments**
- TDA Insights uses port 5000
- Store Dashboard uses port 8081
- Job Codes also uses port 8080 (network IP-based access)
- Zorro uses port 8888
- All services can run simultaneously

📌 **Job Codes uses IP address (not hostname)**
- Reliable access: `10.97.114.181:8080`
- Hostname DNS points to wrong IP - don't use it

📌 **Daily emails show all service statuses**
- Recipients: ATCTeamsupport@walmart.com, kendall.rush@walmart.com
- Includes access URLs and metrics
- Alerts if services are offline

📌 **Auto-restart is fully automated**
- You don't need to do anything
- Monitoring runs daily at 6 AM
- Services restart automatically if offline

---

## Common Tasks

### I want to run the Store Dashboard
```powershell
# Start Store Dashboard (can run alongside TDA)
& "Automation\start_store_dashboard_24_7.bat"

# Access at: http://localhost:8080/
```

### I want to run both TDA and Store Dashboard
```powershell
# Start TDA Insights
& "Automation\start_tda_insights_24_7.bat"

# Start Store Dashboard (in separate cmd/PowerShell window)
& "Automation\start_store_dashboard_24_7.bat"

# Access both:
# TDA:              http://localhost:5000/dashboard.html
# Store Dashboard:  http://localhost:8081/
```

### I want to check status without waiting for email
```powershell
# Run monitoring anytime
PS> .\MONITOR_AND_REPORT.ps1
```

### I want to see detailed logs
```powershell
# Each service logs to its own file
# TDA Logs
Get-Content "Store Support\Projects\TDA Insights\tda_insights_server.log" -Tail 20

# Zorro Logs  
Get-Content "Store Support\Projects\AMP\Zorro\zorro_server.log" -Tail 20

# Job Codes Logs
Get-Content "Automation\jobcodes_server.log" -Tail 20
```

---

## What Changed

✅ **Monitoring Script Enhanced**
- Now checks TDA, Store Dashboard, and Zorro
- Can auto-restart all three services
- Reports status of all 5 services in emails

✅ **New Batch Files Created**
- Auto-restart wrappers for each service
- Logging to track start/stop events
- 5-second restart interval if service crashes

✅ **Documentation Added**
- Complete guides and references
- Quick access tables
- Troubleshooting procedures

✅ **Email Reports Enhanced**
- Now include all 5 services
- Show running count (X/5)
- Include access URLs for all services

---

## Next Steps

### Immediate (Today)
1. ✅ Review this guide
2. ✅ Visit each service URL to verify access
3. ✅ Run `MONITOR_AND_REPORT.ps1` manually to test

### This Week
1. ✅ Monitor daily emails for service status
2. ✅ Verify auto-restart works if a service goes down
3. ✅ Check logs if any issues occur

### Ongoing
1. ✅ Monitor receives daily reports
2. ✅ Services auto-restart if offline
3. ✅ Email alerts if problems detected

---

## Support

### Questions or Issues?
- Check the documentation files for detailed info
- Review log files for error messages
- Run MONITOR_AND_REPORT.ps1 to test monitoring system

### Emergency Contact
Email: ATCTeamsupport@walmart.com or kendall.rush@walmart.com

---

**Status:** ✅ Ready to Use  
**Last Updated:** March 12, 2026  
**System:** WEUS42608431466  

**Start exploring your services now!** 🚀
