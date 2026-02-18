# Restart Backend Server - Step by Step

## Current Status
Backend is running but not responding correctly to root path. This is normal - the API doesn't have a GET / route.

## What You Need to Do

### Step 1: Find the Backend Terminal

You should have **3 terminals open:**
1. **Frontend** - showing `webpack compiled successfully` (port 3000)
2. **Backend** - showing `API is running on port 5000` ← This one!
3. **PowerShell** - regular command prompt

Find the one showing **port 5000** or **Walmart Refresh Guide API**.

---

### Step 2: Stop the Backend Server

**In the backend terminal, press:**
```
Ctrl+C
```

You should see the server stop and prompt return.

---

### Step 3: Verify It Stopped

The backend terminal should now show a command prompt (like `C:\...>`), not server logs.

If you still see "listening" or server output, try **Ctrl+C again**.

---

### Step 4: Restart the Backend Server

**In the same backend terminal, type:**
```powershell
cd server
npm start
```

Then press **Enter**.

---

### Step 5: Wait for Success Message

You should see output like:
```
> walmart-refresh-guide-server@1.0.0 start
> node src/index.js

Walmart Refresh Guide API is running on port 5000
```

When you see this message ✓, the backend is ready.

---

### Step 6: Test the Health Endpoint

**In a NEW terminal (or PowerShell), type:**
```powershell
curl http://localhost:5000/health
```

Or open browser and go to:
```
http://localhost:5000/health
```

**Expected response:**
```json
{
  "status": "OK",
  "message": "Walmart Refresh Guide API is running",
  "timestamp": "2025-11-17T..."
}
```

If you see this ✓, backend is working!

---

## Troubleshooting

### If npm start fails:

**Error: "Cannot find module"**
```powershell
# Install dependencies:
npm install
npm start
```

**Error: "Port 5000 already in use"**
```powershell
# Kill the process using port 5000:
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force

# Then try:
npm start
```

**Error: "node not found"**
```powershell
# Check if Node is installed:
node --version

# If not, install from nodejs.org
```

---

## After Backend Restarts Successfully

1. ✅ Backend terminal shows: "API is running on port 5000"
2. ✅ Browser shows health check response
3. ✅ Go back to app and try "Update Item" again
4. ✅ Should save successfully!

---

## Terminal Layout Reference

```
┌─────────────────────────────────────────┐
│ FRONTEND (Port 3000)                    │
│ webpack compiled successfully           │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│ BACKEND (Port 5000) ← RESTART THIS      │
│ Walmart Refresh Guide API is running    │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│ POWERSHELL (Commands)                   │
│ C:\Users\krush\Documents\VSCode\...     │
└─────────────────────────────────────────┘
```

---

**Once restarted, test by visiting:**
- http://localhost:5000/health → Should work ✓
- Then try form submission in app → Should save ✓
