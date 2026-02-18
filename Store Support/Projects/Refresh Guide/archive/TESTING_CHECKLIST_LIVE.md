# Level 2 Testing - LIVE SESSION

## ✅ Both Servers Running
- ✅ **Backend:** Running on port 5000
- ✅ **Frontend:** Running on port 3000
- ✅ **Browser:** Ready at http://localhost:3000

---

## Test Sequence

### Test 1: Page Load
**Steps:**
1. Navigate to http://localhost:3000 (already done)
2. You should see the Refresh Guide app
3. Check browser console for errors

**Expected:**
- App loads without errors
- No red errors in console
- Login page displays

**Status:** [ ] PASS / [ ] FAIL

---

### Test 2: Quick Login Buttons Load
**Steps:**
1. Look at the login page
2. Scroll down to "Quick Login Examples (Real Users):"
3. You should see 2-4 buttons with real user names

**Expected:**
- See buttons like:
  - 📍 John Smith - Store #2425
  - 👥 Sarah Johnson - Store #2425
  - 🔑 Admin User
  - 🧪 Test Manager

**Status:** [ ] PASS / [ ] FAIL

**If Failed:**
- Check browser Network tab for `/api/management/store-managers` request
- Verify backend is running: http://localhost:5000/health
- Check server console for errors

---

### Test 3: Email Auto-Fill
**Steps:**
1. Type in email field: `john.s2425.us@wal-mart.com`
2. Wait 1-2 seconds for lookup
3. Watch for green checkmark box

**Expected:**
- Blue "Verifying user..." message appears temporarily
- Green success box appears showing:
  - ✓ User Verified
  - John Smith • Store #2425 • Store Manager
- FirstName field shows: `John`
- LastName field shows: `Smith`
- JobTitle field shows: `Store Manager`

**Status:** [ ] PASS / [ ] FAIL

**If Failed:**
- Check browser Network tab for API call
- Check browser console for errors
- Verify email format is correct
- Check that store_managers.json has this user

---

### Test 4: Invalid Email Handling
**Steps:**
1. Clear email field (if filled)
2. Type: `invalid@example.com`
3. Wait for lookup
4. Watch for error message

**Expected:**
- Blue "Verifying user..." appears
- Orange warning box appears:
  - "User not found in system. Please enter details manually or check email address."
- Can still type in other fields manually

**Status:** [ ] PASS / [ ] FAIL

---

### Test 5: Admin Email Auto-Fill
**Steps:**
1. Clear email field
2. Type: `kendall.rush@walmart.com`
3. Wait for lookup

**Expected:**
- Green success box with:
  - ✓ User Verified
  - Kendall Rush • super_admin
- FirstName: `Kendall`
- LastName: `Rush`
- JobTitle: `super_admin`

**Status:** [ ] PASS / [ ] FAIL

---

### Test 6: Quick Login Button Click
**Steps:**
1. Click one of the quick login buttons (e.g., "📍 John Smith")
2. Email field should auto-populate
3. Wait for auto-fill to complete
4. Watch detection status

**Expected:**
- Email field fills with user's email
- Other fields auto-fill
- Green success box appears
- Can click "Sign In" button

**Status:** [ ] PASS / [ ] FAIL

---

### Test 7: Manual Entry Still Works
**Steps:**
1. Clear all fields
2. Manually type:
   - Email: `manual@walmart.com`
   - FirstName: `John`
   - LastName: `Doe`
   - JobTitle: `Manager`
3. Click Sign In

**Expected:**
- Manual entry works without system lookup
- Can sign in with manually entered data
- Backward compatibility maintained

**Status:** [ ] PASS / [ ] FAIL

---

### Test 8: Form Submission
**Steps:**
1. Use one of the auto-filled users (John Smith or Kendall Rush)
2. Click "Sign In" button
3. Wait for redirect

**Expected:**
- Login successful
- Redirected to dashboard or survey page
- No errors in console

**Status:** [ ] PASS / [ ] FAIL

---

### Test 9: Detection Status UI
**Steps:**
1. Watch the email field closely
2. Type an email slowly: `john.s2425.us@wal-mart.com`

**Expected:**
- See transition: idle → detecting → found
- Blue spinner with "Verifying user..."
- Then green success box
- Clear visual feedback

**Status:** [ ] PASS / [ ] FAIL

---

### Test 10: Store Number Extraction
**Steps:**
1. Test different store emails:
   - `user.s1001.us@wal-mart.com` (Store #1001)
   - `user.s5000.us@wal-mart.com` (Store #5000)
   - `user.s9999.us@wal-mart.com` (Store #9999)

**Expected:**
- System correctly extracts store number
- Looks up right store's employees
- Shows correct store # in success message

**Status:** [ ] PASS / [ ] FAIL

---

## Acceptance Criteria

All 10 tests must pass:

- [x] Test 1: Page Load ✓
- [ ] Test 2: Quick Login Buttons
- [ ] Test 3: Email Auto-Fill
- [ ] Test 4: Invalid Email Handling
- [ ] Test 5: Admin Email Auto-Fill
- [ ] Test 6: Quick Login Button Click
- [ ] Test 7: Manual Entry Still Works
- [ ] Test 8: Form Submission
- [ ] Test 9: Detection Status UI
- [ ] Test 10: Store Number Extraction

**Overall Status:** ⏳ IN PROGRESS

---

## Debugging Tips

### Email Auto-Fill Not Working?
1. **Check Browser Console:**
   - Open DevTools (F12)
   - Go to Console tab
   - Look for red errors

2. **Check Network Tab:**
   - Go to Network tab
   - Type email and look for `/api/management/store-managers/store/2425` request
   - Click it and check Response
   - Should see user data

3. **Check Backend Logs:**
   - Look at server terminal
   - Should see request logs
   - Check for errors

### Quick Buttons Not Showing?
1. Check if backend returned data:
   - http://localhost:5000/api/management/store-managers
   - Should show list of users

2. Check React props:
   - Open React DevTools
   - Look at LoginPage component
   - Check `quickLoginOptions` state

### Store Number Not Extracting?
1. Check email format:
   - Must be: `firstname.s[STORE].us@wal-mart.com`
   - Must have `.s` followed by store number
   - Must end with `.us@wal-mart.com`

2. Verify regex in code:
   - `/\.s(\d+)\.us@/`
   - Should match pattern

---

## Quick Reference

### Test Users Available

**Store #2425:**
- John Smith (Manager)
- Sarah Johnson (Coach)

**Admin:**
- Kendall Rush (super_admin)

**Test Users:**
- Test Manager
- Test Coach
- Test Admin
- Test Business Owner

### API Endpoints Used

1. **Auto-Fill Lookup:**
   - GET `/api/management/store-managers/store/:storeNumber`
   - GET `/api/management/admin-users`
   - GET `/api/management/site-owners`
   - GET `/api/management/test-users`

2. **Login:**
   - POST `/api/auth/login`

---

## Next Steps After Testing

✅ All 10 Tests Pass:
1. Commit changes to GitHub
2. Create Release Notes
3. Move to Phase 2 features

⚠️ Some Tests Fail:
1. Check debugging tips above
2. Review error messages in console
3. Check API responses
4. Check browser Network tab

---

## Session Notes

**Date:** November 18, 2025  
**Started:** When both servers started successfully  
**Status:** Testing in progress  
**Testers:** (Your name here)
