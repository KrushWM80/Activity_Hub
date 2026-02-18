# LoginPage Level 2 - Quick Testing Guide

## Pre-Test Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Check http://localhost:5000/health (should return OK)
- [ ] Data files exist:
  - [ ] `/server/data/store_managers.json`
  - [ ] `/server/data/admin_users.json`
  - [ ] `/server/data/site_owners.json`
  - [ ] `/server/data/test_users.json`

---

## Test 1: Load Login Page

**Steps:**
1. Open browser: http://localhost:3000/login
2. Check browser console for errors

**Expected Results:**
- ✅ Login form loads
- ✅ Quick login buttons appear (or show "Loading user data...")
- ✅ No red errors in console
- ✅ Auto-login card visible (if enabled)

**Console Logs to Look For:**
```
[LoginPage] User in context: null
[LoginPage] Looking up user data...
```

---

## Test 2: Quick Login Buttons Load

**Steps:**
1. Wait 2-3 seconds on login page
2. Check if quick login buttons show user names

**Expected Results:**
- ✅ Buttons load with real user data
- ✅ Shows Store Manager name
- ✅ Shows Store Coach name
- ✅ Shows Admin name
- ✅ Shows Test User name
- ✅ Each shows store number or role

**Example:**
```
📍 Store Manager: John Smith (Store #2425)
👥 Store Coach: Sarah Johnson (Store #2425)
🔑 Admin: Kendall Rush (super_admin)
🧪 Test User: Test Manager (manager)
```

**If Buttons Don't Load:**
- Check backend is running: `npm start` in server folder
- Check API endpoint: http://localhost:5000/api/management/store-managers
- Check browser console for errors
- Check browser Network tab for failed requests

---

## Test 3: Auto-Fill with Manual Entry

**Steps:**
1. Clear any auto-filled data
2. Type in email field: `john.s2425.us@wal-mart.com`
3. Wait 1-2 seconds

**Expected Results:**
- ✅ Spinner appears with "Verifying user..."
- ✅ After lookup, shows blue success indicator
- ✅ First Name auto-fills: `John`
- ✅ Last Name auto-fills: `Smith`
- ✅ Job Title auto-fills: `Store Manager`
- ✅ Green box appears: "✓ User Verified - John Smith • Store #2425 • Store Manager"

**If Auto-Fill Doesn't Work:**
1. Check browser Network tab → `/api/management/store-managers/store/2425`
2. Verify API returns data
3. Check browser console for JS errors
4. Verify localStorage has a token (if API requires auth)

---

## Test 4: Auto-Fill with Admin Email

**Steps:**
1. Clear form
2. Type email: `kendall.rush@walmart.com`
3. Wait 1-2 seconds

**Expected Results:**
- ✅ Spinner appears
- ✅ System checks admin_users.json
- ✅ Finds Kendall Rush
- ✅ Auto-fills: Kendall, Rush, Business Owner - ATC Team
- ✅ Green verification box shows

**Console Logs:**
```
[LoginPage] Looking up user: kendall.rush@walmart.com
[LoginPage] Found admin user: {...}
```

---

## Test 5: Quick Login Button Click

**Steps:**
1. Click any quick login button, e.g., "Store Manager: John Smith"
2. Observe form fills
3. Observe detection message

**Expected Results:**
- ✅ Email field: `john.s2425.us@wal-mart.com`
- ✅ First Name: `John`
- ✅ Last Name: `Smith`
- ✅ Job Title: `Store Manager`
- ✅ Green "User Verified" box appears
- ✅ All within 1 second

**Console Logs:**
```
[LoginPage] Looking up user: john.s2425.us@wal-mart.com
[LoginPage] Found store user: {...}
```

---

## Test 6: Invalid Email

**Steps:**
1. Type email: `invalid@example.com`
2. Wait 1-2 seconds

**Expected Results:**
- ✅ Spinner appears with "Verifying user..."
- ✅ After lookup, orange warning box appears
- ✅ Message: "User not found in system. Please enter details manually or check email address."
- ✅ Form not auto-filled
- ✅ User can still manually enter data

**This is GOOD - shows error handling works!**

---

## Test 7: Unknown Home Office Email

**Steps:**
1. Type email: `unknown@walmart.com`
2. Wait 1-2 seconds

**Expected Results:**
- ✅ Spinner appears
- ✅ System checks admin list (not found)
- ✅ System checks site owner list (not found)
- ✅ System defaults to business owner
- ✅ Green box shows verification
- ✅ No auto-fill (no firstName/lastName in default)

**This is GOOD - defaults to business owner!**

---

## Test 8: Sign In Flow

**Steps:**
1. Fill form (use auto-fill or manual)
2. Click "Sign In" button
3. Check what happens

**Expected Results:**
- ✅ Button shows loading spinner
- ✅ Backend processes login
- ✅ If successful: Redirects to dashboard (/)
- ✅ If failed: Shows error message

**Console Logs:**
```
[LoginPage] Calling login...
[LoginPage] Login succeeded
```

---

## Test 9: Manual Entry Still Works

**Steps:**
1. Clear all form fields
2. Disable quick login buttons somehow (or just don't use them)
3. Manually type:
   - Email: `test.email@wal-mart.com`
   - First Name: `John`
   - Last Name: `Doe`
   - Job Title: `Manager`
4. Click Sign In

**Expected Results:**
- ✅ Form accepts manual entry
- ✅ Login processes
- ✅ No requirement for auto-lookup
- ✅ Backward compatible - old behavior still works

---

## Test 10: Auto-Login Still Works

**Steps:**
1. Close browser completely
2. Log out of Windows
3. Log back in as a Windows user
4. Open http://localhost:3000/login
5. Check if auto-login card appears

**Expected Results:**
- ✅ Auto-login detection runs
- ✅ Shows Windows user info
- ✅ Attempts to auto-login
- ✅ Either succeeds or shows manual login form
- ✅ NEW: User data verified against system (enhanced!)

---

## Common Issues & Fixes

### Issue: "Verifying user..." spinner never stops

**Fix:**
1. Check backend is running: http://localhost:5000/health
2. Check Network tab in browser dev tools
3. Look for failed API requests
4. Verify API endpoint returns data

### Issue: Quick login buttons show "Loading user data..." forever

**Fix:**
1. Check `/api/management/store-managers` endpoint
2. Verify backend route registered
3. Check browser Network tab for 404 or 500 errors
4. Check backend logs for errors

### Issue: Auto-fill doesn't work but no errors

**Fix:**
1. Check data files have content:
   ```bash
   cat server/data/store_managers.json | head -20
   ```
2. Verify email in data file matches exactly
3. Check localStorage for token (may need for auth)
4. Try without token: `Authorization: Bearer undefined`

### Issue: Form fields don't match auto-filled data

**Fix:**
1. Check order of operations:
   - User types email
   - handleChange fires
   - lookupUserByEmail called
   - API response received
   - setFormData called
2. Wait full 2 seconds for API
3. Check API response has correct field names

### Issue: "User not found" for valid email

**Possible Causes:**
1. Email case sensitivity: Try exact match from data file
2. Email doesn't exist in data file
3. API lookup failed (network issue)
4. Email pattern doesn't match regex: `.s[####].us@wal-mart.com`

---

## Debugging Tips

### Enable Verbose Logging
Add to LoginPage.tsx temporarily:
```typescript
console.log = function(...args) {
  document.getElementById('console-log').innerText += '\n' + args.join(' ');
  window.console.log(...args);
};
```

### Check API Responses
In browser DevTools Network tab:
1. Filter by `store-managers`
2. Click request
3. Check Response tab
4. Verify data matches expected format

### Check Form State
Add to JSX temporarily:
```typescript
<pre>{JSON.stringify(formData, null, 2)}</pre>
<pre>{JSON.stringify(detectedUser, null, 2)}</pre>
```

### API Test with curl
```bash
# Test store managers endpoint
curl http://localhost:5000/api/management/store-managers/store/2425

# Should return:
# [{ email: "...", firstName: "...", ... }]
```

---

## Success Criteria

All tests pass when:

- [x] Quick login buttons load with real user data
- [x] Typing email auto-fills other fields
- [x] Detection status shows correctly (found/not-found/detecting)
- [x] Invalid emails show orange warning
- [x] Manual entry still works
- [x] Quick login button click works
- [x] Sign In button submits form
- [x] Auto-login still functions
- [x] No breaking changes to existing behavior
- [x] No console errors

---

## Acceptance Testing Checklist

- [ ] Backend runs without errors
- [ ] Frontend loads login page
- [ ] Quick login buttons appear
- [ ] Email auto-fill works
- [ ] Detection status displays
- [ ] Quick login button works
- [ ] Invalid email shows error gracefully
- [ ] Manual entry works
- [ ] Sign in flow completes
- [ ] Auto-login still works
- [ ] No console errors
- [ ] No breaking changes

---

## Next Steps After Testing

If all tests pass:
1. ✅ Commit to GitHub
2. ✅ Update README
3. ✅ Mark todo as complete
4. ✅ Plan Phase 2 features

If issues found:
1. Note which tests failed
2. Check debugging tips
3. Verify prerequisites
4. Check API endpoints
5. Review logs and network tab
