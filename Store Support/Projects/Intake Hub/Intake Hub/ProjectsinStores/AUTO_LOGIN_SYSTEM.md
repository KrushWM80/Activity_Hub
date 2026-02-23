# Automatic Login System (No Password Required)

## Overview

The system has been upgraded to **eliminate passwords entirely** and automatically detect users via their Windows network credentials. Users can now click a shared link and be instantly logged in to the dashboard without entering any credentials.

## User Access Path

Users will access the dashboard via this URL:
```
http://weus42608431466.homeoffice.wal-mart.com:8001/index.html
```

This is the PRIMARY entry point. The system automatically:
1. Detects user credentials via Kerberos headers
2. Creates session if needed
3. Serves dashboard to authenticated users
4. Redirects to login for unauthenticated users

1. **User clicks link**: `http://weus42608431466.homeoffice.wal-mart.com:8001/index.html`
2. **Kerberos detection**: Browser automatically sends Windows authentication token with request
3. **System extracts username**: Backend detects authenticated user from:
   - Kerberos `Authorization` header
   - `X-Remote-User` header (if set by reverse proxy/IIS)
   - `Remote-User` header variants
4. **Session created instantly**: Backend creates session for auto-detected user
5. **Dashboard appears**: Zero-click authentication - user sees dashboard immediately

**Result**: User never sees login page, credentials are never entered, authentication is completely transparent.

### For Remote/Non-Domain Users (Fallback)

1. **User clicks link**: `http://weus42608431466.homeoffice.wal-mart.com:8001/index.html`
2. **Kerberos detection fails**: No Windows auth tokens sent
3. **Login form appears**: Simple username-only form shown (NO password field)
4. **User enters username**: Just their username (e.g., "john.doe")
5. **Auto-login created**: Username-based session created, no password verification needed
6. **Dashboard appears**: User redirected to dashboard

**Result**: Simplified login - only username required, no password.

## Technical Architecture

### Authentication Flow

```
User Request
    ↓
Check Session Cookie (for existing sessions)
    ↓ (if no session)
Check Kerberos Headers (for Windows AD users)
    ↓ (if Kerberos detected)
Extract Username, Create Session, Auto-redirect to Dashboard
    ↓ (if not detected)
Show Username-Only Login Form
    ↓ (user enters username)
Create Session, Redirect to Dashboard
```

### Key Components Modified

#### 1. **Backend Authentication** (`main.py`)

**Function: `get_current_authenticated_user(request)`**
- Checks sessions first (existing authenticated users)
- Then checks Kerberos/NTLM headers
- Falls back to Windows AD (local users)
- Returns user email if authenticated

**New Function: `extract_kerberos_username(request)`**
- Parses Kerberos authentication tokens
- Handles multiple header formats (X-Remote-User, Remote-User, etc.)
- Maps Windows usernames to Walmart email format (@homeoffice.wal-mart.com)
- Returns email for authenticated users

**Endpoint: `POST /api/auth/login`**
- **CHANGED**: Password parameter is now optional (not used)
- Accepts username only: `{ "username": "john.doe", "password": "" }`
- Creates session immediately without password validation
- Returns session cookie and user info

**Endpoint: `GET /`** (Root/Dashboard)
- Checks if user is authenticated (session or Kerberos)
- **If authenticated**: Creates session if needed, serves dashboard
- **If NOT authenticated**: Redirects to `/login.html`

**Endpoint: `GET /login.html`** (NEW)
- Serves login page
- Auto-detects user on page load via Kerberos headers
- If detected, redirects to dashboard
- If not detected, shows username-only form

#### 2. **Login Page** (`login.html`)

**Key Features**:
- **Auto-detection on load**: Immediately attempts to detect Kerberos user
- **Shows spinner while detecting**: "🔍 Detecting your network credentials..."
- **If detected**: Shows success message and redirects to dashboard
- **If not detected**: Shows fallback username-only form
- **Username field only**: NO password field anywhere
- **Enter to submit**: Press Enter to submit form or Ctrl+Enter on username
- **Clean session handling**: Browser automatically manages session cookies

#### 3. **Admin Configuration** (`admin-access.json`)

**CHANGED**: Removed `fallback_password` field
- No longer needed since password authentication is gone
- Only contains authorized admin user list
- Config is simplified and cleaner

### Supported Authentication Methods

#### Priority Order:
1. **Session Cookie** (HttpOnly, 8-hour expiry)
   - If user has active session, use it
   - Session auto-renewed on each request

2. **Kerberos/NTLM Headers** (Windows AD)
   - For domain-joined machines with Windows authentication enabled
   - Headers checked: `Authorization`, `X-Remote-User`, `Remote-User`, `HTTP_REMOTE_USER`, `X-Authenticated-User`
   - Automatically detected by browser

3. **Windows AD Local User** (Same machine as server)
   - Fallback for users on same network/machine as server
   - Reads `USERNAME` environment variable
   - Mapped to Walmart email format

4. **Username-Only Login** (Fallback form)
   - For users not detected by above methods
   - No password required
   - Email created from username: `{username}@homeoffice.wal-mart.com`

## Setup Requirements

### For Windows Domain Users (Recommended)

**What IT needs to do**:
1. Ensure server is domain-joined or IIS is configured for Kerberos
2. Enable Windows Authentication in IIS (not required if using reverse proxy that handles auth)
3. Configure reverse proxy headers: Set `X-Remote-User` header to authenticated username
4. Ensure port 8001 is accessible from user network
5. Users must be on domain-joined machines or VPN to domain

**User experience**: Click link → Instant access (no login form)

### For Non-Domain Users (Current)

**No IT setup needed**:
- Users can access from anywhere
- Click link → See simple username form
- Enter username → Instant access

**User experience**: Minimal friction - only username, no passwords

### For Local Users (Same Machine)

**No setup needed**:
- Works automatically on server machine
- Reads Windows username environment variable
- No form appears

**User experience**: Click link → Instant access

## Configuration

### Username Mapping

Edit `backend/main.py` to add custom username mappings:

```python
username_map = {
    'krush': 'kendall.rush@walmart.com',
    'jsmith': 'john.smith@walmart.com',  # Add more as needed
}
```

When a username is entered, system checks this map. If found, uses mapped email. Otherwise, creates email as `{username}@homeoffice.wal-mart.com`.

### Admin Access

Edit `backend/admin-access.json`:

```json
{
  "authorized_admins": [
    "kendall.rush@homeoffice.wal-mart.com",
    "john.smith@homeoffice.wal-mart.com"
  ]
}
```

Only users in this list see admin controls.

## User Paths

### Path 1: Corporate/Domain User (Most Common)
```
User clicks URL (from domain-joined machine)
    ↓
Browser sends Kerberos token automatically
    ↓
Server detects authentication headers
    ↓
System creates session
    ↓
Dashboard loads instantly
    ↓
NO LOGIN PAGE SHOWN
    ↓
User sees: Dashboard with their data
```

### Path 2: Remote User (Any Network)
```
User clicks URL (from non-domain machine)
    ↓
Browser sends no auth headers
    ↓
Login page appears
    ↓
Auto-detection section shows: "Detecting credentials..."
    ↓
After 2-3 seconds, detection times out
    ↓
Username form appears
    ↓
User enters username (e.g., "john.doe")
    ↓
Clicks "Sign In" or presses Enter
    ↓
System creates session with detected Kerberos (if available) or username
    ↓
Dashboard loads
    ↓
User sees: Dashboard with their data
```

### Path 3: Local Server User
```
User opens URL on server machine
    ↓
Browser sends system auth
    ↓
Server detects Windows username from environment
    ↓
System creates session
    ↓
Dashboard loads instantly
    ↓
User sees: Dashboard with their data
```

## Troubleshooting

### User sees login form but has never clicked before
**Normal behavior** - System is attempting auto-detection
- If on domain-joined machine: Should auto-detect after 2-3 seconds
- If on non-domain machine: Will show username form (expected)

### User can't login with username
1. Check username is spelled correctly (no @domain)
2. Verify server is running and reachable
3. Check browser console (F12) for errors
4. Ensure username maps to valid Walmart email (mappings in main.py)

### Users getting "Invalid credentials"
- No longer possible - passwords aren't validated
- If users see errors, it's likely server connection issue

### Kerberos detection failing despite being domain-joined
1. Check IIS is configured for Windows Authentication
2. Verify reverse proxy is setting X-Remote-User header
3. Check server logs for header information
4. Ensure URL uses server hostname, not IP address
5. Try clearing browser cache and cookies

### Session expiring too quickly
- Default is 8 hours of inactivity
- Session auto-renews on each page access
- If page stays open, session continues indefinitely

## Security Considerations

### What's Changed
- ✅ **No passwords stored**: No password validation or storage
- ✅ **Kerberos tokens used**: Industry-standard Windows authentication
- ✅ **HttpOnly cookies**: Session cookies cannot be accessed by JavaScript
- ✅ **No hardcoded credentials**: System reads from environment/headers

### What's Maintained
- ✅ Session expiry (8 hours)
- ✅ Secure cookie attributes (HttpOnly, SameSite=Lax)
- ✅ User activity logging
- ✅ Admin access controls
- ✅ User tracking and audit trail

### Assumptions
- **For Kerberos to work**: 
  - Server must be domain-joined OR
  - Reverse proxy must handle Kerberos and set headers
- **For username-only**:
  - System trusts that username correctly identifies user
  - Appropriate for internal networks only

## API Reference

### `/api/auth/user` (GET)
Returns currently authenticated user info or not-authenticated response.

**Request**:
```
GET /api/auth/user
Cookie: session_id=...
```

**Response (Authenticated)**:
```json
{
  "email": "kendall.rush@homeoffice.wal-mart.com",
  "username": "krush",
  "is_admin": true,
  "auth_method": "session",
  "message": "Authenticated via session"
}
```

**Response (Not Authenticated)**:
```json
{
  "email": null,
  "username": null,
  "is_admin": false,
  "auth_method": "none",
  "message": "Not authenticated"
}
```

### `/api/auth/login` (POST)
Creates session from username (password optional, not validated).

**Request**:
```json
POST /api/auth/login
Content-Type: application/json

{
  "username": "john.doe",
  "password": ""
}
```

**Response**:
```json
{
  "email": "john.doe@homeoffice.wal-mart.com",
  "username": "john.doe",
  "is_admin": false,
  "auth_method": "session",
  "message": "Logged in as john.doe@homeoffice.wal-mart.com"
}
```

**Headers Set**:
- `Set-Cookie: session_id=<uuid>; HttpOnly; Path=/; SameSite=Lax; Max-Age=28800`

### `/api/auth/logout` (POST)
Clears user session and removes session cookie.

**Request**:
```
POST /api/auth/logout
Cookie: session_id=...
```

**Response**:
```json
{
  "message": "Logged out successfully"
}
```

## Migration Notes

### From Password-Based System

If migrating from old password-based login:

1. **Database**: No password database needed anymore
2. **Admin config**: Remove `fallback_password` field (already done)
3. **Frontend**: Old login.html updated with auto-detection
4. **Backend**: All password validation removed from `/api/auth/login`
5. **Cookies**: Same session cookies work (upgrade is backward compatible)

### Backward Compatibility

- Old session cookies still work
- Old password in URL parameters ignored
- Old HTML forms still function (password field ignored)
- No breaking changes for existing integrations

## Roadmap

### Future Enhancements (Optional)
1. **LDAP integration**: Direct directory lookups
2. **Multi-factor auth**: Optional 2FA for sensitive operations
3. **SSO integration**: Direct Microsoft/Azure AD
4. **Session management UI**: Per-device sessions control
5. **Biometric auth**: For mobile/remote access

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review server logs: Check FastAPI output for auth errors
3. Browser console: Check browser F12 console for JavaScript errors
4. Network tab: Verify auth headers being sent in requests

## Summary

✅ **Zero-password authentication** - Users never type passwords
✅ **Automatic for domain users** - Instant login for corporate machines
✅ **Fallback for remote** - Simple username form for non-domain users
✅ **No configuration needed** - Works out of the box
✅ **Secure by default** - Uses Kerberos + HttpOnly cookies
✅ **User-friendly** - Click link → View dashboard
