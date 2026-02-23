# User Mapping Configuration Guide

## Problem
Users may have multiple email formats:
- **Windows Username**: `krush`
- **Microsoft Email**: `krush@homeoffice.wal-mart.com`
- **Canonical Email**: `kendall.rush@walmart.com`

This can cause inconsistencies where reports, admin access, and user identification don't match.

## Solution: User Mapping

### 1. Username to Email Mapping
**File**: `main.py` → `get_windows_username()` function

Maps Windows usernames to their canonical Walmart email address.

```python
username_map = {
    'krush': 'kendall.rush@walmart.com',
    'jsmith': 'john.smith@walmart.com',
    'lwalker': 'lucy.walker@walmart.com',
}
```

### 2. Admin Access Configuration
**File**: `admin-access.json`

Stores authorized admin users. When checking admin status, the system checks both:
- The mapped canonical email
- The homeoffice email variant (for backward compatibility)

### 3. Report Configuration
**Files**: `report_configs/*.json`

Each report's `user_id` should match the **canonical email** returned by authentication:
```json
{
  "user_id": "kendall.rush@walmart.com",
  "report_name": "Kendall's Daily"
}
```

---

## Adding a New User

### Step 1: Add to Username Map (main.py)
```python
username_map = {
    'krush': 'kendall.rush@walmart.com',
    'newuser': 'first.last@walmart.com',  # ADD THIS LINE
}
```

### Step 2: Add to Admin List (optional)
If they need admin access, add to `admin-access.json`:
```json
{
  "authorized_admins": [
    "krush@homeoffice.wal-mart.com",
    "first.last@walmart.com"  // NEW USER - add canonical email
  ]
}
```

### Step 3: Create/Update Reports
When creating reports for this user, set `user_id` to their canonical email:
```json
{
  "user_id": "first.last@walmart.com",
  "report_name": "Their Report"
}
```

---

## Testing

### Verify User Mapping
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8001/api/auth/user" -UseBasicParsing
$response.Content | ConvertFrom-Json
```

Expected output should show:
- `email`: New user's canonical email (e.g., `kendall.rush@walmart.com`)
- `is_admin`: `true` or `false` based on admin-access.json

### Verify Reports Show Up
```powershell
$url = "http://localhost:8001/api/reports/configs?user_id=first.last@walmart.com"
Invoke-WebRequest -Uri $url -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

Should return all reports with matching `user_id`.

---

## User Identity Resolution

The system resolves user identity in this order:

1. **Get Windows Username** → `krush`
2. **Map to Canonical Email** → `kendall.rush@walmart.com`
3. **Use for All Operations** → Reports, admin checks, activity logs
4. **Maintain Backward Compatibility** → Check homeoffice variant for admin access

---

## Current Mappings

| Windows Username | Canonical Email | Purpose |
|---|---|---|
| krush | kendall.rush@walmart.com | Primary user |

---

## Need to Add More Users?

1. Get their Windows username (ask them to run: `echo %USERNAME%`)
2. Get their Walmart email (from Azure AD or their email)
3. Add to this guide and `main.py` mapping
4. Update `admin-access.json` if they need admin access
5. Restart server: `python main.py`
6. Test authentication endpoint
