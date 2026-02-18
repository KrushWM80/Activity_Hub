# QUICK CHECKLIST - Restart Backend & Test

## ✓ Checklist

### Terminal Setup
- [ ] Find the backend terminal (should show "listening on port 5000" or similar)
- [ ] Confirm frontend terminal shows "webpack compiled successfully"
- [ ] Have a 3rd PowerShell ready for testing

### Stop Backend
- [ ] In backend terminal, press **Ctrl+C**
- [ ] Wait for command prompt to return
- [ ] Confirm server logs stop

### Start Backend
- [ ] Type: `cd server`
- [ ] Type: `npm start`
- [ ] Wait for message: **"Walmart Refresh Guide API is running on port 5000"**
- [ ] Once you see it ✓, backend is ready!

### Verify Health Check
- [ ] Open browser OR new PowerShell
- [ ] Go to: `http://localhost:5000/health`
- [ ] Should see JSON response with "status": "OK"
- [ ] If yes ✓, API is working!

### Test Form Submission
- [ ] Go to app at `http://localhost:3000`
- [ ] Login as Store Manager
- [ ] Click "View All Items"
- [ ] Click "Continue Survey"
- [ ] Fill in form with changes
- [ ] Click "Update Item"
- [ ] **Expected**: "Survey response saved successfully!" alert
- [ ] **Expected**: Redirected to View All Items page

### Verify Data Saved
- [ ] Open file: `server/data/survey_responses.json`
- [ ] Check that it has a new entry with your changes
- [ ] Should show: owner, status, deadline, notes you entered

---

## If Anything Fails

1. **Backend won't start:**
   ```powershell
   npm install
   npm start
   ```

2. **Port 5000 in use:**
   ```powershell
   Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
   npm start
   ```

3. **Health check fails:**
   - Confirm backend terminal shows "API is running"
   - Try closing browser and reopening
   - Check for typos in URL

4. **Form submission still fails:**
   - Check browser console (F12) for exact error
   - Check backend terminal for error messages
   - Share the error details

---

## Success Criteria

✅ Backend shows "API is running on port 5000"  
✅ Health check URL returns OK status  
✅ Form submission shows success message  
✅ Data appears in survey_responses.json file  

Once all 4 are done → **Full end-to-end testing complete!**
