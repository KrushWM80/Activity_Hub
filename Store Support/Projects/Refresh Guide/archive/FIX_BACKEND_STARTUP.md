# Backend Won't Start - Dependency Issues

## Problem
`npm start` returned `Exit Code: 1` - this means the server failed to start.

**Common causes:**
- Dependencies not installed
- Missing node_modules folder
- Package.json missing dependencies

## Solution

### Step 1: Install Backend Dependencies

```powershell
# Navigate to server directory
cd server

# Install all dependencies
npm install

# This may take 1-2 minutes...
# You should see output like:
# added XX packages in Xs
```

### Step 2: Try Starting Again

```powershell
npm start

# Should see:
# Walmart Refresh Guide API is running on port 5000
```

---

## If Still Failing

### Check for error messages:

When you run `npm start`, look for **red error text** showing:
- `Cannot find module 'xxx'`
- `Error: ENOENT: no such file or directory`
- Any other error message

**Copy the exact error and follow below troubleshooting:**

---

## Complete Reset (If all else fails)

```powershell
# 1. Delete node_modules and package-lock
cd server
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json -Force

# 2. Reinstall everything
npm install

# 3. Start server
npm start
```

---

## Verify Installation Worked

After `npm install` completes, check:

```powershell
# Should list packages
npm list --depth=0

# Look for packages like:
# ├── express
# ├── cors
# ├── dotenv
# └── etc...
```

If you see a list of packages ✓, dependencies are installed.

---

## Test After Starting

Once server shows "API is running on port 5000":

```powershell
# In a NEW PowerShell window, test health:
curl http://localhost:5000/health

# Should return:
# {"status":"OK","message":"Walmart Refresh Guide API is running",...}
```

---

## What to Do:

1. Open terminal in VS Code or new PowerShell
2. Navigate to `C:\Users\krush\Documents\VSCode\Refresh Guide\server`
3. Run: `npm install`
4. Wait for completion
5. Run: `npm start`
6. Report back with any error messages

---

**Once backend starts successfully, form submission will work!**
