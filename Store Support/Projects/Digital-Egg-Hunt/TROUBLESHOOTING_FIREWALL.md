# Digital Egg Hunt - Firewall/Network Troubleshooting

## Current Status (April 2, 2026)
**Active Configuration**: Port 80 (Standard HTTP)
- **QR Codes Point To**: `http://10.97.114.181/Digital_Egg_Hunt?egg=[ID]`
- **Web Server**: Running on port 80
- **Status**: ✅ WORKING

---

## Problem
"Safari (or browser) can't open the leaderboard page"
This is typically caused by **corporate network firewall blocking non-standard ports** on mobile devices.

---

## Solution Hierarchy (Try in Order)

### ✅ OPTION 1: Port 80 (CURRENT - ACTIVE)
**Why it works**: Port 80 is the standard HTTP port, rarely blocked by firewalls

**Server**: Port 80  
**QR Code URLs**: `http://10.97.114.181/Digital_Egg_Hunt?egg=[ID]`  
**How to switch**: Already implemented! Just need to test on phone.

**To activate**:
```powershell
# Server is already running on port 80
# QR codes are already updated
# Just test on phone!
```

---

### 🔄 OPTION 2: Port 8080 (Fallback #1)
**Why it works**: Common alternate HTTP port, often whitelisted for development

**If Option 1 fails, do this:**

1. Update web_server.py:
```python
PORT = 8080  # Change from 80
```

2. Update generate_eggs.py:
```python
app_url="http://10.97.114.181:8080/Digital_Egg_Hunt"  # Change from 80
```

3. Regenerate eggs:
```powershell
cd "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
& ".\.venv\Scripts\python.exe" "Store Support\Projects\Digital-Egg-Hunt\generate_eggs.py"
```

4. Restart web server:
```powershell
Stop-Job -Name "DEH-WebServer-80"
Start-Job -ScriptBlock { param($exe, $script) & $exe $script } -ArgumentList $pythonExe, $webScript -Name "DEH-WebServer-8080"
```

---

### 🔄 OPTION 3: Serve from Backend (Fallback #2)
**Why it works**: Backend on port 8003 may have different firewall rules

**If Options 1 & 2 fail, do this:**

1. Move frontend to backend:
   - Add static file serving to backend `main.py`
   - Move `index.html` to `backend/static/index.html`

2. Update QR codes:
```python
app_url="http://10.97.114.181:8003/static/Digital_Egg_Hunt"
```

3. This is more complex - contact for detailed instructions

---

## Test Checklist

### ✅ Internal (from laptop)
- [ ] `http://localhost/Digital_Egg_Hunt` → Works
- [ ] `http://10.97.114.181/Digital_Egg_Hunt` → Works
- [ ] `http://10.97.114.181/Digital_Egg_Hunt?egg=T1` → Works

### ✅ WiFi Phone Test (from employee WiFi)
- [ ] Scan QR code on printed test egg
- [ ] Browser opens and shows leaderboard
- [ ] Can register name
- [ ] Egg auto-scans after registration
- [ ] Leaderboard shows in real-time

### ✅ Mobile Data Test (4G/5G)
- [ ] Same as WiFi test
- [ ] Verifies external network accessibility

---

## Current System Info

**Web Server**:
- File: `Store Support\Projects\Digital-Egg-Hunt\web_server.py`
- Current Port: **80**
- Status: ✅ Running

**Egg Generator**:
- File: `Store Support\Projects\Digital-Egg-Hunt\generate_eggs.py`
- Current URL: **http://10.97.114.181/Digital_Egg_Hunt?egg=[ID]**

**Egg Files**:
- Test: `Digital_Egg_Hunt_Test.html` (T1-T10)
- Production 2": `Digital_Egg_Hunt_Production_2in.html` (EGG-001-030)
- Production 4": `Digital_Egg_Hunt_Production_4in.html` (EGG-031-055)
- Production 6": `Digital_Egg_Hunt_Production_6in.html` (EGG-056-070)
- Production 8": `Digital_Egg_Hunt_Production_8in.html` (EGG-071-080)

---

## Admin Notes

If port 80 requires admin privileges:
```powershell
# Run PowerShell as Administrator first, then:
# ... your commands here
```

If you get "Address already in use" error:
```powershell
# Find what's using port 80
netstat -ano | Select-String ":80 "

# Kill the process (if safe)
taskkill /PID <PID> /F
```

---

## Backend Status (Always Working)
- Port: **8003**
- URL: `http://10.97.114.181:8003/`
- Never had firewall issues (non-standard port acceptable for API)
