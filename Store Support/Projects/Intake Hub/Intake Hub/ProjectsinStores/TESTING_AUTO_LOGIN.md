# Auto-Login System - Quick Testing Guide

## Testing the New System

### Test 1: Check Server is Running

```bash
# Test 1: Verify the backend is running
curl http://127.0.0.1:8001/api/health

# Expected response: {"status": "ok"} or similar
```

### Test 2: Auto-Detection (Not Authenticated)

```bash
# Try to get user info without being logged in
curl -v http://127.0.0.1:8001/api/auth/user

# Expected response: 401 or user data with is_admin=false
```

### Test 3: Kerberos Header Detection

```bash
# Simulate Kerberos header (what domain-joined machines send)
curl -v http://127.0.0.1:8001/api/auth/user \
  -H "X-Remote-User: john.doe"

# OR
curl -v http://127.0.0.1:8001/api/auth/user \
  -H "Authorization: Negotiate YII..."

# Expected response: User detected, session may be created
```

### Test 4: Username-Only Login

```bash
# Login with just a username (no password required)
curl -X POST http://127.0.0.1:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john.doe","password":""}'

# Expected response:
# {
#   "email": "john.doe@homeoffice.wal-mart.com",
#   "username": "john.doe",
#   "is_admin": false,
#   "auth_method": "session",
#   "message": "Logged in as john.doe@homeoffice.wal-mart.com"
# }
```

### Test 5: Session Cookie Validation

```bash
# Login and save the session cookie
SESSION=$(curl -s -c /tmp/cookies.txt -X POST http://127.0.0.1:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john.doe","password":""}' | grep -o '"message":".*"')

# Use the session cookie to access dashboard
curl -b /tmp/cookies.txt http://127.0.0.1:8001/api/auth/user

# Expected response: User authenticated via session
```

### Test 6: Logout

```bash
# Clear session
curl -b /tmp/cookies.txt -X POST http://127.0.0.1:8001/api/auth/logout

# Verify no longer authenticated
curl -b /tmp/cookies.txt http://127.0.0.1:8001/api/auth/user

# Expected: Not authenticated
```

### Test 7: Login Page Auto-Detection (Browser)

1. Open browser and navigate to: `http://localhost:8001/login.html`
2. **Expected**: 
   - See spinner: "🔍 Detecting your network credentials..."
   - If on domain-joined machine: Should auto-detect and redirect
   - If not domain-joined: Spinner stops, username form appears
3. **Enter username**: Type "krush" or any valid username
4. **Click Sign In**: Should redirect to dashboard

### Test 8: Dashboard Access (Browser)

1. Navigate to: `http://localhost:8001/`
2. **If authenticated**: Should see dashboard immediately
3. **If not authenticated**: Should redirect to login page
4. **No password**: Never asked for password anywhere

## Common Test Scenarios

### Scenario A: First-Time Domain User
```
1. Delete browser cookies
2. Navigate to http://localhost:8001/
3. Expected: Auto-detect via Kerberos → Dashboard loads
4. No login form shown (unless Kerberos not available)
```

### Scenario B: First-Time Remote User
```
1. Delete browser cookies
2. Navigate to http://localhost:8001/
3. Expected: Redirect to login.html
4. Auto-detect fails (expected)
5. Username form appears
6. Enter username, click Sign In
7. Redirect to dashboard
```

### Scenario C: User Session Expires
```
1. Clear cookies manually or wait 8 hours
2. Navigate to http://localhost:8001/
3. Expected: Redirect to login.html (session gone)
4. Repeat authentication process
```

### Scenario D: Multiple Users on Same Machine
```
1. User A logs in, gets session cookie
2. User A closes browser (or we clear cookies)
3. User B logs in with different username
4. Expected: Each gets their own session
5. No cross-user data access
```

## Verification Checklist

- [ ] Server starts without errors
- [ ] `/api/health` returns OK
- [ ] Login with username succeeds (no password required)
- [ ] Session cookie set correctly (HttpOnly)
- [ ] Dashboard accessible with session cookie
- [ ] Redirect to login.html when not authenticated
- [ ] Auto-logout after 8 hours of inactivity
- [ ] User activity logged correctly
- [ ] Admin users can see admin controls
- [ ] Regular users cannot see admin controls
- [ ] Kerberos header detected (if headers sent)
- [ ] Username auto-lowercased in form
- [ ] Enter key submits form
- [ ] Error messages display properly
- [ ] Success messages display properly

## Expected Log Output

When running `python main.py`, you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)

# When user logs in via username
INFO:     User Login [Auto-detect: john.doe@homeoffice.wal-mart.com]

# When user accesses dashboard
INFO:     Main Dashboard [john.doe@homeoffice.wal-mart.com]

# When user logs out
INFO:     User Logout [john.doe@homeoffice.wal-mart.com]
```

## Browser Developer Tools Checks

### Check 1: Session Cookie
1. Open DevTools (F12)
2. Go to **Application/Storage → Cookies**
3. Expected: `session_id` cookie present, HttpOnly flag set
4. Duration: ~8 hours

### Check 2: Network Requests
1. Open DevTools (F12)
2. Go to **Network** tab
3. Refresh page
4. Check `/api/auth/user` request
5. Expected: 
   - Request includes `Cookie: session_id=...`
   - Response has user data if authenticated
   - Response has `is_admin: false` or `true`

### Check 3: Console Errors
1. Open DevTools (F12)
2. Go to **Console** tab
3. Expected: No red errors about authentication
4. Info messages show auto-detect progress

## Troubleshooting Tests

### If Login Fails

```bash
# Check what's happening
curl -v -X POST http://127.0.0.1:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":""}'

# Should return 200 with session info, not 401
```

### If Kerberos Not Detected

```bash
# Check if headers are being received
curl -v http://127.0.0.1:8001/api/auth/user \
  -H "X-Remote-User: test.user"

# Check server logs for "Kerberos detected" message
```

### If Session Not Persisting

```bash
# Verify cookies are sent with requests
curl -v -c /tmp/cookies.txt -X POST http://127.0.0.1:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":""}'

# Check /tmp/cookies.txt has session_id
cat /tmp/cookies.txt

# Verify cookie is sent on next request
curl -v -b /tmp/cookies.txt http://127.0.0.1:8001/api/auth/user
```

## Performance Expectations

- Auto-detect on page load: 2-3 seconds
- Login submit: 0.5-1 second
- Dashboard load: 0.5-2 seconds (depends on data)
- Session check on each request: <100ms

## Success Indicators

✅ All above tests pass
✅ No SQL/Python errors in server logs
✅ Login page shows spinner briefly
✅ No password field visible anywhere
✅ Dashboard appears instantly without password entry
✅ Session persists across page refreshes
✅ Logout clears session
✅ Kerberos headers detected (if applicable)

## Common Mistakes to Avoid

❌ Don't manually add password to URL
❌ Don't try to send password in headers
❌ Don't expect Kerberos on non-domain machines
❌ Don't keep old password fields in forms
❌ Don't forget HttpOnly flag on cookies
❌ Don't hardcode usernames in code

## Questions to Verify Understanding

1. Q: Does the login form ask for password?
   A: NO - password field removed entirely

2. Q: What happens when domain-joined user clicks link?
   A: Auto-detection via Kerberos headers, instant access, no form

3. Q: What happens when remote user clicks link?
   A: Kerberos detection fails, username form appears, user enters username only

4. Q: Is session still secure without password?
   A: YES - Kerberos tokens provide security, HttpOnly cookies prevent theft

5. Q: How long is session valid?
   A: 8 hours of inactivity, auto-renewed on each request

6. Q: Can user change their password?
   A: N/A - They don't have one! They use Windows credentials (system admin manages)

7. Q: What if username entered is wrong?
   A: User is logged in anyway (no validation), but may lack permissions

8. Q: Can multiple users share account?
   A: No - Each Windows user gets unique session, activity logged separately
