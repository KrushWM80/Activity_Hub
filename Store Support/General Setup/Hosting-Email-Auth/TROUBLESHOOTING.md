# Troubleshooting Guide

## Common Issues & Solutions

---

## 🔴 Server Won't Start

### Issue: "Port 8080 already in use"

**Error Message:**
```
OSError: [WinError 10048] Only one usage of each socket address (protocol/port combination) is normally permitted
```

**Solutions:**

1. **Find and stop process using port 8080**
   ```powershell
   # Find process
   Get-NetTCPConnection -LocalPort 8080 | Select-Object OwningProcess
   
   # Kill process by PID (e.g., 12345)
   Stop-Process -Id 12345 -Force
   ```

2. **Wait for port to be released**
   ```powershell
   # Windows takes time to release ports
   # Wait 30 seconds and try again
   Start-Sleep -Seconds 30
   ```

3. **Use different port**
   - Edit `backend/main.py`
   - Find: `PORT = 8080`
   - Change to: `PORT = 8081`
   - Restart server

4. **Check if service is running**
   ```powershell
   # See what's using the port
   netstat -ano | findstr :8080
   tasklist | findstr <PID>
   ```

---

### Issue: "Python not found"

**Error Message:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

1. **Check if Python is installed**
   ```powershell
   python --version
   # Should show version like: Python 3.10.5
   ```

2. **Install Python**
   - Download from python.org
   - Make sure to check "Add Python to PATH" during installation
   - Restart PowerShell/CMD

3. **Use full path to Python**
   ```powershell
   C:\Users\krush\.code-puppy-venv\Scripts\python.exe backend/main.py
   ```

4. **Check virtual environment**
   ```powershell
   # If using virtual environment
   & "C:\path\to\venv\Scripts\Activate.ps1"
   python --version
   ```

---

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**

1. **Install required packages**
   ```powershell
   pip install fastapi uvicorn pandas openpyxl
   ```

2. **Install in virtual environment (if using one)**
   ```powershell
   & "C:\Users\krush\.code-puppy-venv\Scripts\Activate.ps1"
   pip install fastapi uvicorn pandas openpyxl
   ```

3. **Check which Python is running**
   ```powershell
   which python  # or
   Get-Command python
   ```

4. **Verify installation**
   ```powershell
   python -c "import fastapi; print(fastapi.__version__)"
   ```

---

## 🔴 Login Issues

### Issue: "Invalid username or password" (but credentials are correct)

**Diagnosis:**

1. **Check users.json exists**
   ```powershell
   Test-Path "C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\data\users.json"
   ```

2. **Verify file content**
   ```powershell
   Get-Content "...\data\users.json" | ConvertFrom-Json
   ```

3. **Check for typos**
   - Username: `admin` (not `Admin` - case sensitive)
   - Password: `admin123` (exactly as shown)

**Solutions:**

1. **Reset to default users**
   - Delete `data/users.json`
   - Restart server
   - Server will recreate with default admin/admin123

2. **Manually fix users.json**
   ```json
   {
     "admin": {
       "password": "admin123",
       "role": "admin",
       "email": "admin@example.com"
     }
   }
   ```

3. **Check if session is expired**
   - Try logging in again
   - Browser might have cached expired token
   - Clear localStorage: Open DevTools (F12) → Application → Storage → localStorage

---

### Issue: "Cannot login - connection refused"

**Error Message:**
```
Failed to connect to server
OR
Connection refused at localhost:8080
```

**Solutions:**

1. **Check if server is running**
   ```powershell
   # Open new PowerShell tab
   Invoke-WebRequest http://localhost:8080 -ErrorAction Ignore
   ```

2. **Check firewall**
   ```powershell
   # Allow Python through firewall
   netsh advfirewall firewall add rule name="Python" `
     dir=in action=allow program="C:\Users\krush\.code-puppy-venv\Scripts\python.exe" `
     enable=yes
   ```

3. **Try accessing dashboard directly**
   ```powershell
   # Test with curl
   curl http://localhost:8080
   
   # Or Invoke-WebRequest
   Invoke-WebRequest http://localhost:8080
   ```

---

## 🔴 Data Issues

### Issue: "data/users.json not found"

**Solutions:**

1. **Create data directory**
   ```powershell
   New-Item -ItemType Directory -Path "data" -Force
   ```

2. **Create default users.json**
   ```json
   {
     "admin": {
       "password": "admin123",
       "role": "admin",
       "email": "admin@example.com"
     }
   }
   ```

3. **Restart server**
   - Server will auto-create if still missing

---

### Issue: "sessions.json is invalid JSON"

**Error Message:**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solutions:**

1. **Delete corrupted file**
   ```powershell
   Remove-Item "data/sessions.json" -Force
   ```

2. **Restart server**
   - Server will recreate empty sessions.json

3. **Restore from backup**
   ```powershell
   # If you have a backup
   Copy-Item "backup/sessions.json" "data/sessions.json"
   ```

---

### Issue: "Cannot write to data files (Permission Denied)"

**Error Message:**
```
PermissionError: [Errno 13] Permission denied: 'data/users.json'
```

**Solutions:**

1. **Check file permissions**
   ```powershell
   Get-Item "data/users.json" | Select-Object FullName, @{
     Name="Owner"; Expression={(Get-Acl $_.FullName).Owner}
   }
   ```

2. **Close file in other applications**
   - Excel might have the file open
   - Text editor might have lock on it
   - Close and retry

3. **Reset file permissions**
   ```powershell
   icacls "data/users.json" /reset
   ```

4. **Run PowerShell as Administrator**
   - Right-click PowerShell → Run as administrator

---

## 🟡 Performance Issues

### Issue: "Dashboard is slow"

**Solutions:**

1. **Check data file sizes**
   ```powershell
   Get-ChildItem "data/" -Recurse | Select-Object Name, Length
   ```

2. **Monitor server logs**
   - Check console output for errors
   - Look for slow API responses

3. **Archive old data**
   ```powershell
   # Move old requests to archive
   Copy-Item "data/update_requests.json" "archive/update_requests_backup.json"
   
   # Or delete if very old
   # (with backup first!)
   ```

4. **Check disk space**
   ```powershell
   Get-Volume | Select-Object DriveLetter, SizeRemaining, Size
   ```

---

### Issue: "Requests timeout"

**Solutions:**

1. **Increase FastAPI timeout**
   ```python
   # In main.py, change uvicorn settings
   uvicorn.run(
       "main:app",
       host="0.0.0.0",
       port=PORT,
       timeout_keep_alive=30,  # Increase from default
       timeout_notify=30
   )
   ```

2. **Check large file operations**
   - Exporting many requests might be slow
   - Add progress indicator in frontend

3. **Profile slow endpoints**
   ```python
   import time
   
   @app.get("/api/slow-endpoint")
   async def slow_endpoint():
       start = time.time()
       
       # ... your code ...
       
       elapsed = time.time() - start
       print(f"Took {elapsed:.2f} seconds")
   ```

---

## 🟡 Network Issues

### Issue: "Other computers can't access dashboard"

**Solutions:**

1. **Check if firewall is blocking**
   ```powershell
   # Enable port 8080 in firewall
   New-NetFirewallRule -DisplayName "Port 8080" `
     -Direction Inbound `
     -Action Allow `
     -LocalPort 8080 `
     -Protocol TCP
   ```

2. **Check your IP address**
   ```powershell
   # Get IP (not 127.x or 169.254.x)
   Get-NetIPAddress -AddressFamily IPv4 | 
     Where-Object { $_.IPAddress -notlike "127.*" }
   
   # Other users should use: http://YOUR_IP:8080
   ```

3. **Verify server is listening on 0.0.0.0**
   ```python
   # In main.py
   uvicorn.run("main:app", host="0.0.0.0", port=8080)
   ```

4. **Check VPN connection**
   - Both computers must be on same VPN
   - Test connectivity: `ping OTHER_COMPUTER_IP`

---

## 🟡 Browser Issues

### Issue: "Blank page" or "Cannot GET /"

**Solutions:**

1. **Check browser console**
   - Open DevTools: F12
   - Check Console tab for errors
   - Check Network tab to see requests

2. **Clear browser cache**
   ```
   Ctrl+Shift+Delete
   Clear all cache and cookies
   ```

3. **Try different browser**
   - Chrome, Firefox, Edge
   - See if issue is browser-specific

4. **Check if frontend files exist**
   ```powershell
   Test-Path "frontend/JobCodeTeamingDashboard.html"
   Test-Path "frontend/login.html"
   Test-Path "frontend/dashboard.html"
   ```

---

### Issue: "Token expired - need to login again"

**This is normal behavior** - Sessions expire after 8 hours.

**Solutions:**

1. **Increase session timeout**
   ```python
   # In backend/main.py
   expires = (datetime.now() + timedelta(hours=8)).isoformat()
   # Change to: timedelta(hours=24)
   ```

2. **Implement session refresh**
   ```javascript
   // JavaScript to auto-refresh token before expiration
   setInterval(() => {
       fetch("/api/refresh-token", {
           method: "POST",
           headers: { "Authorization": `Bearer ${getSessionToken()}` }
       });
   }, 6 * 60 * 60 * 1000);  // Every 6 hours
   ```

3. **Clear old sessions periodically**
   ```python
   # Backend cleanup task
   @app.on_event("startup")
   async def cleanup_expired_sessions():
       """Remove expired sessions on startup"""
       sessions = load_json("data/sessions.json")
       
       now = datetime.now()
       expired = [
           token for token, session in sessions.items()
           if datetime.fromisoformat(session["expires"]) < now
       ]
       
       for token in expired:
           del sessions[token]
       
       save_json("data/sessions.json", sessions)
   ```

---

## 🟡 Export Issues

### Issue: "Export button doesn't download file"

**Solutions:**

1. **Check browser download settings**
   - Browser might be blocking download
   - Check downloads folder

2. **Verify export endpoint returns data**
   ```python
   # Debug: Print what's being exported
   @app.get("/api/export/approved")
   async def export_approved_requests(session: dict):
       requests = load_json("data/update_requests.json")
       approved = [r for r in requests.values() if r["status"] == "approved"]
       
       print(f"Exporting {len(approved)} requests")  # Debug
       
       return JSONResponse(content=approved)
   ```

3. **Test export with curl**
   ```powershell
   # Test export endpoint
   $token = "YOUR_SESSION_TOKEN"
   $headers = @{"Authorization" = "Bearer $token"}
   
   Invoke-WebRequest -Uri "http://localhost:8080/api/export/approved" `
     -Headers $headers `
     -OutFile "export.json"
   ```

---

## 📋 Debugging Checklist

```
□ Server is running? 
  → Check PowerShell terminal shows "Uvicorn running..."

□ Can access localhost:8080?
  → Try: Invoke-WebRequest http://localhost:8080

□ Can login?
  → Check: data/users.json exists with admin user

□ Can see dashboard after login?
  → Check: frontend HTML files exist

□ Can submit requests?
  → Check: data/update_requests.json is writable

□ Can admin approve requests?
  → Check: user has "admin" role in users.json

□ Can export data?
  → Check: approved requests exist in update_requests.json

□ Other users can't access?
  → Check: Firewall allows port 8080
  → Check: Server uses host="0.0.0.0"
  → Check: Get your IP with: Get-NetIPAddress
```

---

## 📞 Advanced Debugging

### Enable verbose logging

```python
# In main.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Then use:
logger.debug(f"Attempting login for user: {username}")
logger.error(f"Failed to load users.json: {e}")
```

### Check system logs

```powershell
# Windows Event Viewer
eventvwr.msc

# Or check Python errors
# (captured in terminal where server is running)
```

### Monitor file changes

```powershell
# Watch for file modifications
Get-ChildItem "data/" -Recurse | 
  Where-Object { $_.LastWriteTime -gt (Get-Date).AddSeconds(-5) }
```

---

## 🎓 Prevention Tips

✅ **Backup regularly** - Automate daily backups of data folder  
✅ **Monitor disk space** - Keep 500MB+ free for logs  
✅ **Keep Python updated** - Patch security vulnerabilities  
✅ **Test after changes** - Always verify before deploying  
✅ **Review logs** - Check for warnings and errors  

---

## 📚 Related Files

- Backend: `backend/main.py`
- Frontend: `frontend/JobCodeTeamingDashboard.html`
- Data: `data/` directory
- Logs: Terminal output where server is running
