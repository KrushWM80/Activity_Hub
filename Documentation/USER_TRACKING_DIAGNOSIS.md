# User Tracking Issue - Root Cause Analysis & Solution

## Executive Summary
**Problem**: Other users (like Tina.Budnaitis@walmart.com) are submitting feedback and creating fixes, but **they do NOT appear in Activity Log or Active Users list** on the admin dashboard.

**Example**: FIX-b8af1fbe was created by Tina, fix IS stored in pending_fixes.json, but **NO "Feedback Submitted" log entry exists for Tina** in activity_log.json.

**Status**: 🔴 **CRITICAL** - Users are being tracked incompletely. Admin cannot see who submitted what.

---

## Root Causes Identified

### 1. ⚠️ NO LOGIN TRACKING FOR REGULAR USERS
**Location**: `/api/auth/login` endpoint (main.py line 111-126)

**Problem**: 
- When users log in via Windows AD, the login is processed but **NO activity is logged**
- Only admin users get tracked (via `/api/auth/user` → checkAuth() function)
- Regular users bypass activity logging entirely

**Evidence**:
- Activity log shows "Accessed Main Dashboard" but only for krush@homeoffice.wal-mart.com
- Tina has only Email Report entries, NO login entries
- No "User Login" action in activity_log.json for other users

**Impact**: 
- Cannot track when users first join
- No baseline activity record exists
- Admin has NO visibility into who accessed the system

---

### 2. ⚠️ NO LOGIN TRACKING IN WINDOWS AD PATH
**Location**: `/api/auth/user` endpoint (main.py line 111-137)

**Problem**:
- When user successfully authenticates via Windows AD, system returns their info but **does NOT log the login**
- Only the admin.html frontend gets their email
- Backend has no record of their access

**Current Code Flow**:
```python
@app.get("/api/auth/user")
async def get_user_info(http_request: Request):
    # ... Windows AD authentication happens ...
    return UserInfoResponse(
        username=username,
        email=email,
        is_admin=is_admin,
        auth_method='windows_ad'
    )
    # ❌ NO log_activity() call here!
```

**Missing**: 
```python
# This is missing:
log_activity(
    action="User Login",
    user=email,
    details=f"Logged in via Windows AD",
    category="user_login"
)
```

---

### 3. ⚠️ FEEDBACK SUBMISSION ONLY LOGS IF SUBMITTED_BY IS CAPTURED
**Location**: `create_pending_fix()` function (main.py line 1613-1650)

**Problem**:
- When feedback is submitted, the code tries to get `submitted_by` from active_users.json
- **BUT**: If the user has NOT interacted with the admin tracking endpoint (`/api/admin/track-user`), they won't be in active_users.json
- Falls back to "Unknown" instead of using submitted_by from frontend

**Code Flow**:
```python
# In submit_feedback (line 1000-1008):
if not feedback.submitted_by:
    try:
        active_users_data = load_active_users()
        users = active_users_data.get("users", {})
        # ❌ If users is empty or doesn't have this user, uses last resort
        most_recent = max(users.values(), key=lambda x: x.get('timestamp', 0), default=None)
        if most_recent:
            feedback.submitted_by = most_recent.get('user_email')
    except:
        pass

if not feedback.submitted_by:
    feedback.submitted_by = "Unknown"  # ❌ FALLBACK
```

**Issue**: 
- Tina submits feedback from index.html (NOT from admin.html)
- She's never tracked by `/api/admin/track-user`
- active_users.json is empty for her
- Feedback gets "Submitted By: Tina.Budnaitis@walmart.com" (correct in pending_fixes.json)
- BUT no activity_log entry is created with her name

---

### 4. ⚠️ ACTIVITY LOG ENTRY NOT CREATED FOR NON-ADMIN FEEDBACK
**Location**: `create_pending_fix()` function - line 1645-1648

**Problem**:
- The `log_activity()` call happens but **the frontend may not pass submitted_by for regular users**
- Regular users submit via index.html which doesn't set their email in the feedback form
- Solution falls back to "Unknown" in activity log, even though pending_fixes.json has correct name

**Code Issue**:
The feedback.submitted_by is only properly set if:
1. Frontend explicitly sends it (admin.html does, but index.html might not), OR
2. User is in active_users.json (only tracked via admin endpoints)

**Result**: Activity log shows "Unknown" or missing entry entirely

---

## Why Tina's Fix Appears But She Doesn't

**FIX-b8af1fbe In pending_fixes.json**:
```json
{
  "id": "b8af1fbe",
  "submitted_by": "Tina.Budnaitis@walmart.com",  // ✅ PRESENT
  "timestamp": "2026-02-25 10:30:45"
}
```

**Activity Log for Tina**:
```
No "Feedback Submitted" entry for b8af1fbe
No "User Login" entry for Tina
Only Email Report delivery entries
```

**Why?**
1. Tina submits feedback from **index.html (projects page)**, not admin.html
2. index.html feedback form may not include email or user tracking
3. Tina is never registered in active_users.json
4. When feedback is logged to activity_log, system can't identify her
5. Log entry is either created as "Unknown" or skipped entirely

---

## Solution: 4-Point Fix

### Fix #1: Add Login Tracking to Windows AD Authentication ✅

**File**: `backend/main.py`  
**Location**: `/api/auth/user` endpoint (line 111-137)  
**Change**: Add log_activity() call after successful authentication

```python
@app.get("/api/auth/user")
async def get_user_info(http_request: Request):
    # ... existing auth logic ...
    if user_info:
        email = user_info.get('email', username + '@homeoffice.wal-mart.com')
        is_admin = email in admin_config['admins']
        
        # ✅ NEW: Log the login
        log_activity(
            action="User Login",
            user=email,
            details=f"Logged in via Windows AD",
            category="user_login"
        )
        # ✅ NEW: Track in active users
        track_user_activity(email, page="dashboard", device_info="Desktop")
        
        return UserInfoResponse(
            username=username,
            email=email,
            is_admin=is_admin,
            auth_method='windows_ad'
        )
```

---

### Fix #2: Add Login Tracking to Fallback Password Auth ✅

**File**: `backend/main.py`  
**Location**: `/api/auth/login` endpoint (line 139-167)  
**Change**: Add tracking after successful password authentication

```python
@app.post("/api/auth/login")
async def fallback_login(request: LoginRequest):
    # ... existing validation ...
    
    return_response = AuthResponse(
        email=email,
        username=username,
        is_admin=True,
        auth_method='fallback_password',
        message='Authenticated via fallback password'
    )
    
    # ✅ NEW: Log successful login
    log_activity(
        action="User Login",
        user=email,
        details=f"Logged in via fallback password",
        category="user_login"
    )
    # ✅ NEW: Track in active users
    track_user_activity(email, page="dashboard", device_info="Desktop")
    
    return return_response
```

---

### Fix #3: Ensure Frontend Passes User Info in Feedback ✅

**File**: `frontend/index.html` (or wherever feedback form is)  
**Change**: When submitting feedback, include user email

**Current**:
```javascript
const feedbackData = {
    category: ...,
    rating: ...,
    comments: ...,
    timestamp: new Date().toISOString()
    // ❌ NO user info
}
```

**New**:
```javascript
// Get current user from localStorage or sessionStorage
const currentUser = sessionStorage.getItem('adminUser') || 
                    localStorage.getItem('currentUser') || 
                    'Unknown';

const feedbackData = {
    category: ...,
    rating: ...,
    comments: ...,
    timestamp: new Date().toISOString(),
    submitted_by: currentUser  // ✅ ADD THIS
}
```

---

### Fix #4: Improve Activity Log Entry Creation ✅

**File**: `backend/main.py`  
**Location**: `create_pending_fix()` function (line 1645-1648)  
**Change**: Ensure submitted_by is always captured correctly

```python
def create_pending_fix(feedback: FeedbackRequest, discovery_result: dict):
    # ... existing code ...
    
    # ✅ IMPROVED: More robust user identification
    submitted_by = feedback.submitted_by or "Unknown"
    if submitted_by == "Unknown" and feedback.user_context:
        # Try to get email from user_context
        if isinstance(feedback.user_context, dict):
            submitted_by = feedback.user_context.get('user_email') or submitted_by
    
    # ... rest of fix creation ...
    
    # Log the feedback submission with guaranteed user identification
    log_activity(
        action="Feedback Submitted",
        user=submitted_by,  # ✅ Use captured submitted_by
        details=f"Submitted feedback: {feedback.category} (Rating: {feedback.rating}/5) - FIX-{fix_id}",
        category="feedback_submission"
    )
```

---

## Implementation Checklist

- [ ] **Fix #1**: Add Windows AD login tracking (backend/main.py line 111-137)
- [ ] **Fix #2**: Add fallback password login tracking (backend/main.py line 139-167)
- [ ] **Fix #3**: Update frontend feedback form to include user email
- [ ] **Fix #4**: Improve activity log entry creation (backend/main.py line 1645-1648)
- [ ] **Test**: Submit feedback as non-admin user, verify appears in Activity Log
- [ ] **Verify**: Login appears in Activity Log for each user
- [ ] **Verify**: Active Users list shows all logged-in users

---

## Expected Results After Fix

| Before | After |
|--------|-------|
| Tina creates FIX-b8af1fbe | ✅ |
| Tina appears in Activity Log | ❌ | ✅ |
| Tina appears in Active Users | ❌ | ✅ |
| Login event logged for Tina | ❌ | ✅ |
| Admin can see when Tina accessed system | ❌ | ✅ |

---

## Impact on Admin Dashboard

**Activity Log Tab**:
- Will now show login events for all users
- Will show feedback submissions with correct submitter name
- Can track user engagement over time

**Active Users Widget**:
- Will show all currently logged-in users
- Grouped by email + device type
- Real-time updates as users access pages

**Fix Submissions**:
- Linked to Activity Log entries
- Can trace who submitted what feedback
- Complete audit trail

---

## Quick Deploy Steps

1. **Stop server**:
   ```powershell
   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
   ```

2. **Apply fixes** to main.py:
   - Add login tracking to /api/auth/user
   - Add login tracking to /api/auth/login
   - Update create_pending_fix() for better user capture

3. **Restart server**:
   ```powershell
   cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"
   & "C:\Users\krush\AppData\Local\Python\bin\python.exe" main.py
   ```

4. **Test** as regular user:
   - Log in to admin.html
   - Check Activity Log shows your login
   - Submit feedback
   - Check Activity Log shows your feedback submission

---

## Files Affected

- ✏️ `backend/main.py` - Add 4 critical tracking points
- ✏️ `frontend/index.html` (or feedback form) - Include user in submission
- 📖 `activity_log.json` - Will now have complete entries
- 📖 `active_users.json` - Will now have all users
- 📖 `pending_fixes.json` - Unchanged (already correct)

---

## Questions This Solves

✅ **Why doesn't Tina appear in Activity Log if her fix exists?**
- Fixes created when user not properly identified in active_users.json

✅ **Why aren't login events showing?**
- Authentication endpoints don't call log_activity()

✅ **Why don't I see other users in Active Users list?**
- Only admin tracking endpoint triggers user tracking

✅ **How do we audit who did what?**
- Complete activity log with login + action tracking

---

## Priority
🔴 **CRITICAL** - Deploy immediately after testing
- Affects audit trail compliance
- Impacts admin accountability
- Blocks user activity tracking

