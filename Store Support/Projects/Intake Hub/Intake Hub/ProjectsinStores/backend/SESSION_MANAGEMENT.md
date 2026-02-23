# Remote User Login System Guide

## Overview

The Intake Hub now supports **multi-user access for remote users** with a session-based authentication system. Local users (on the server machine using Windows AD) continue to work as before, while remote users can authenticate using username and password.

## System Architecture

### Authentication Methods

1. **Local Users (Windows AD)**
   - Automatic authentication when accessing from the server machine
   - No login page needed
   - `auth_method: windows_ad`

2. **Remote Users (Password-Based)**
   - Access via remote URL (e.g., `http://servername.domain.com:8001/`)
   - Must log in with username and password
   - Session stored securely in HttpOnly cookies
   - `auth_method: session`

### Session Management

- **Session Duration**: 8 hours (480 minutes)
- **Storage**: In-memory session store with secure HttpOnly cookies
- **Auto-Extension**: Sessions extend 8 hours on each API access
- **Cleanup**: Expired sessions automatically removed

## For Remote Users

### Accessing the Dashboard

1. **Open the Dashboard URL** (from your remote machine):
   ```
   http://server-hostname:8001/
   ```

2. **You'll be redirected to login page** (if not authenticated locally):
   ```
   http://server-hostname:8001/login.html
   ```

3. **Enter Your Credentials**:
   - **Username**: Your Walmart network username (samaccountname)
   - **Password**: Ask your manager for the departmental password
   - Click "Sign In"

4. **Access Dashboard**:
   - After successful login, you'll be redirected to the main dashboard
   - Your session will persist for 8 hours
   - Session auto-extends with each page access

### Testing Your Login

After logging in, verify your session:

```bash
# Using curl (or Postman):
curl -b "session_id=YOUR_SESSION_ID" http://server-hostname:8001/api/auth/user
```

Should return:
```json
{
  "email": "yourname@walmart.com",
  "username": "yourname",
  "is_admin": false,
  "auth_method": "session",
  "message": "Authenticated via session"
}
```

## For System Administrators

### Configuration

Edit `admin-access.json` to:

```json
{
  "authorized_admins": [
    "admin1@homeoffice.wal-mart.com",
    "admin2@homeoffice.wal-mart.com"
  ],
  "fallback_password": "YourDepartmentalPassword"
}
```

### Login Endpoints

#### POST `/api/auth/login`

Create a new session for a remote user.

**Request**:
```json
{
  "username": "john.doe",
  "password": "password123"
}
```

**Response** (on success):
```json
{
  "email": "john.doe@walmart.com",
  "username": "john.doe",
  "is_admin": false,
  "auth_method": "session",
  "message": "Logged in as john.doe@walmart.com"
}
```

Sets `session_id` HttpOnly cookie automatically.

**Error Responses**:
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Missing username or password

#### GET `/api/auth/user`

Check current user authentication status (works with Windows AD or session).

**Headers** (with session):
```
Cookie: session_id=YOUR_SESSION_UUID
```

**Response**:
```json
{
  "email": "john.doe@walmart.com",
  "username": "john.doe",
  "is_admin": false,
  "auth_method": "session",
  "message": "Authenticated via session"
}
```

#### POST `/api/auth/logout`

Clear the current session.

**Headers** (with session):
```
Cookie: session_id=YOUR_SESSION_UUID
```

**Response**:
```json
{
  "message": "Logged out successfully"
}
```

### Session Management

**Session Store**: In-memory dictionary
- Key: UUID (session_id)
- Value: `{email, is_admin, expires, created}`

**Session Cleanup**:
- Automatic: Expired sessions cleaned up on next access
- Manual: Can be implemented via admin endpoint (future)

### Username Mapping

Configure user identity mapping in `main.py`:

```python
username_map = {
    'krush': 'kendall.rush@walmart.com',
    # Add mappings for other users:
    # 'jsmith': 'john.smith@walmart.com',
}
```

Mapped users are checked during admin verification using both canonical and homeoffice email variants.

### Multi-User Tracking

Both local and remote users are tracked in `/api/admin/active-users`:

```json
{
  "active_users": [
    {
      "email": "kendall.rush@walmart.com",
      "last_seen": "2024-02-05T14:23:45.123456",
      "page": "Email Reports",
      "auth_method": "windows_ad"
    },
    {
      "email": "testuser@walmart.com",
      "last_seen": "2024-02-05T14:22:10.654321",
      "page": "Main Dashboard",
      "auth_method": "session"
    }
  ]
}
```

### Verify System Status

```bash
# Check auth endpoints
curl http://hostname:8001/api/auth/user

# Check active users
curl http://hostname:8001/api/admin/active-users

# Test login (would create session)
curl -X POST http://hostname:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Admin2026"}'
```

## Security Considerations

### Cookie Security

- **HttpOnly**: JavaScript cannot access session cookies (XSS protection)
- **SameSite=Lax**: CSRF protection with same-site cookie policy
- **Secure Flag**: Set to false by default (HTTP). Set to true for HTTPS production.

### Password Management

- **Fallback Password**: Shared departmental password for remote users
- **No Storage**: Passwords not stored; compared against config
- **Single Config**: One password per environment (consider changing regularly)

### Session Limits

- **No Database**: Sessions kept in-memory (resets on server restart)
- **Expiry**: 8 hours without activity (auto-extends on use)
- **Size Limit**: Few hundred concurrent sessions manageable in-memory

## Troubleshooting

### Issue: "Invalid credentials" error

**Solution**: 
- Verify username is correct (lowercase, no domain)
- Confirm password matches `admin-access.json`
- Check fallback_password hasn't been changed

### Issue: Session expires after restart

**Solution**: 
- Expected behavior - all sessions cleared on server restart
- Users will need to log in again
- Consider implementing persistent session storage (future enhancement)

### Issue: User not appearing in active users

**Solution**:
- Ensure user has made at least one API request after login
- Check that middleware is enabled (it is by default)
- Session might have expired - check 8-hour limit

### Issue: Reports not visible after login

**Solution**:
- User must have reports assigned to their email (e.g., `testuser@walmart.com`)
- Admin can create reports for users
- Reports cannot be transferred between users
- Check /api/reports/configs to verify report ownership

## Implementation Details

### Request Flow (Remote User)

```
1. User navigates to http://hostname:8001/
         ↓
2. Frontend detects not authenticated (no Windows AD)
         ↓
3. Redirects to /login.html
         ↓
4. User enters username and password
         ↓
5. POST /api/auth/login with credentials
         ↓
6. Backend validates password, creates session, sets cookie
         ↓
7. Frontend stores session info, redirects to /index.html
         ↓
8. Subsequent requests include session_id cookie
         ↓
9. Backend uses cookie to identify user
```

### Session Flow

```python
# On login:
session_id = create_session(user_email, is_admin=True)
# Returns UUID, stores in _SESSIONS dict
# Front end receives in cookie

# On subsequent requests:
current_user = get_session_user(session_id)  # Extends expiry
# Returns email or None if expired

# On logout:
clear_session(session_id)  # Removes from _SESSIONS
```

## Future Enhancements

- [ ] Persistent session storage (database or Redis)
- [ ] Multi-factor authentication (MFA)
- [ ] LDAP/Active Directory remote authentication
- [ ] Session timeout configurable per-role
- [ ] Session audit trail in activity log
- [ ] Email verification for new users
- [ ] Password policy enforcement

## Testing

Run the test script to verify the system:

```bash
python test_login.py
```

Expected output:
- ✅ Local user auth via Windows AD
- ✅ Remote user login with password
- ✅ Session cookie created
- ✅ Session cookie works for subsequent requests
- ✅ Logout clears session

---

**Last Updated**: February 2024  
**System Version**: 2.0 (Session-based Multi-user)  
**Status**: ✅ Fully Operational
