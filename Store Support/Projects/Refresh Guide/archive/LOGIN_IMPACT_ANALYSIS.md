# Impact Analysis: New User Management System on Login Page

## Current Login Flow

### What Happens Now:
1. User enters email, firstName, lastName, jobTitle manually (or quick login buttons)
2. LoginPage.tsx calls `login(credentials)` from AuthContext
3. AuthContext calls `authService.login(credentials)` 
4. authService sends POST to `/api/auth/login`
5. Backend returns user object with roles
6. Frontend stores token and user info
7. Determines available profiles based on roles array

### Current Limitations:
- ❌ Manual entry of all fields (error-prone)
- ❌ No validation against Walmart database
- ❌ No check if user exists in admin/site owner lists
- ❌ Quick login buttons have hardcoded test data
- ❌ No way to add test users without editing code
- ❌ Email pattern `.s[####].us@wal-mart.com` not validated

---

## Impact of New User Management System

### What Will Change:

#### **1. Email Validation & Parsing (MAJOR CHANGE)**

**Before:**
```tsx
// User just types email - no validation
<TextField name="email" value={formData.email} onChange={handleChange} />
// Could be anything: "john@test.com", "invalid.email", etc.
```

**After:**
```tsx
// LoginPage will:
// 1. Extract store number from email pattern: .s[STORE].us@wal-mart.com
// 2. Query /api/management/store-managers/store/:storeNumber
// 3. Check if email matches manager or coach in that store
// 4. OR check /api/management/admin-users for admin
// 5. OR check /api/management/site-owners for site owner
// 6. OR check /api/management/test-users for test users
// 7. OR default to business owner if @walmart.com

const extractStoreNumber = (email: string) => {
  const match = email.match(/\.s(\d+)\.us@/);
  return match ? match[1] : null;
};

const lookupUserRole = async (email: string) => {
  const storeNumber = extractStoreNumber(email);
  
  if (storeNumber) {
    // Look up in store managers
    const managers = await fetch(`/api/management/store-managers/store/${storeNumber}`);
    // Check if email matches any manager or coach
  } else if (email.includes('@walmart.com')) {
    // Check admin list
    // Check site owner list
    // Default to business owner
  }
};
```

---

#### **2. Pre-population of User Data (MAJOR IMPROVEMENT)**

**Before:**
```tsx
// User has to type everything:
// Email: john.s2425.us@wal-mart.com
// First Name: john
// Last Name: smith
// Job Title: Store Manager
// All manual, error-prone
```

**After:**
```tsx
// When user enters: john.s2425.us@wal-mart.com
// System automatically fills:
// First Name: (from store_managers.json)
// Last Name: (from store_managers.json)
// Job Title: (from store_managers.json)
// Store Number: (from store_managers.json)
// Role: manager (from store_managers.json)
```

**UI Flow:**
1. User types email
2. System queries `/api/management/store-managers/store/:storeNumber`
3. System finds matching email in managers/coaches list
4. Auto-fills firstName, lastName, jobTitle, storeNumber
5. User sees "Detected: John Smith - Store Manager" (like auto-login but on demand)
6. User clicks "Sign In"

---

#### **3. Role Determination (AUTOMATIC)**

**Before:**
```tsx
// Backend had to guess role from email pattern
// Errors if user data doesn't match
```

**After:**
```tsx
// System knows exactly:
const determineRole = async (email: string) => {
  if (email.match(/\.s\d+\.us@wal-mart\.com/)) {
    const storeNumber = extractStoreNumber(email);
    
    // Check store_managers.json
    if (isManager(email)) return 'manager';
    if (isCoach(email)) return 'coach';
    if (isInTestUsers(email)) return getTestUserRole(email);
  }
  
  if (email.includes('@walmart.com')) {
    if (isInAdminList(email)) return 'admin';
    if (isInSiteOwnerList(email)) return 'site_owner';
    return 'business'; // default for home office
  }
  
  return 'denied'; // unknown user
};
```

---

#### **4. Quick Login Examples (SMART UPDATE)**

**Before:**
```tsx
const quickLogin = (role: 'business' | 'manager' | 'associate') => {
  const examples = {
    business: {
      email: 'john.doe.s00000.us@wal-mart.com', // WRONG format!
      firstName: 'John',
      lastName: 'Doe', 
      jobTitle: 'Business Owner'
    },
    // ... hard-coded test data
  };
};
```

**After:**
```tsx
// Pull from actual data:
const quickLogin = async (userType: 'store-manager' | 'store-coach' | 'admin' | 'site-owner' | 'business') => {
  let examples;
  
  if (userType === 'store-manager') {
    // Get first store manager from store_managers.json
    const managers = await fetch('/api/management/store-managers');
    examples = managers[0]; // John Smith from Store #2425
  } else if (userType === 'admin') {
    // Get first admin from admin_users.json
    const admins = await fetch('/api/management/admin-users');
    examples = admins[0]; // Kendall Rush
  } else if (userType === 'test-user') {
    // Get from test_users.json
    const testUsers = await fetch('/api/management/test-users');
    examples = testUsers[0];
  }
  
  setFormData(examples);
};
```

---

#### **5. Test User Support (NEW FEATURE)**

**Before:**
- No way to add test users without editing code
- Had to create fake emails manually

**After:**
```tsx
// New UI section: "Test Users"
<Button onClick={() => navigate('/admin/manage-test-users')}>
  Manage Test Users (Admin Only)
</Button>

// Or quick buttons showing available test users:
{testUsers.map(user => (
  <Button onClick={() => loginAs(user.email)}>
    Test: {user.firstName} {user.lastName}
  </Button>
))}
```

---

## Step-by-Step Changes to LoginPage.tsx

### **Change 1: Add User Lookup Functions**
```tsx
// New helper functions
const extractStoreNumber = (email: string): string | null => {
  const match = email.match(/\.s(\d+)\.us@/);
  return match ? match[1] : null;
};

const lookupStoreUser = async (email: string, storeNumber: string) => {
  try {
    const response = await fetch(`/api/management/store-managers/store/${storeNumber}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    });
    const managers = await response.json();
    
    // Find manager or coach with matching email
    for (const manager of managers) {
      if (manager.email === email) {
        return { ...manager, role: 'manager' };
      }
      if (manager.coaches) {
        const coach = manager.coaches.find(c => c.email === email);
        if (coach) return { ...coach, role: 'coach', storeNumber: manager.storeNumber };
      }
    }
    return null;
  } catch (error) {
    console.error('Failed to lookup store user:', error);
    return null;
  }
};

const lookupAdminUser = async (email: string) => {
  try {
    const response = await fetch('/api/management/admin-users', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    });
    const admins = await response.json();
    return admins.find(a => a.email === email) || null;
  } catch (error) {
    console.error('Failed to lookup admin user:', error);
    return null;
  }
};

// ... similar for site owners, test users
```

---

### **Change 2: Add Email Change Handler**
```tsx
const handleEmailChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
  const email = e.target.value;
  setFormData(prev => ({ ...prev, email }));
  
  // Try to auto-fill user info
  const storeNumber = extractStoreNumber(email);
  
  if (storeNumber) {
    // Try store user first
    const storeUser = await lookupStoreUser(email, storeNumber);
    if (storeUser) {
      setFormData(prev => ({
        ...prev,
        firstName: storeUser.firstName,
        lastName: storeUser.lastName,
        jobTitle: storeUser.jobTitle,
        storeNumber
      }));
      setDetectedUser(storeUser);
      return;
    }
  }
  
  if (email.includes('@walmart.com')) {
    // Try admin
    const admin = await lookupAdminUser(email);
    if (admin) {
      setFormData(prev => ({
        ...prev,
        firstName: admin.firstName,
        lastName: admin.lastName,
        jobTitle: admin.title
      }));
      setDetectedUser(admin);
      return;
    }
    
    // Try site owner
    const siteOwner = await lookupSiteOwner(email);
    if (siteOwner) {
      setFormData(prev => ({
        ...prev,
        firstName: siteOwner.firstName,
        lastName: siteOwner.lastName,
        jobTitle: siteOwner.title
      }));
      setDetectedUser(siteOwner);
      return;
    }
  }
};
```

---

### **Change 3: Update Quick Login Buttons**
```tsx
// Instead of hardcoded data, fetch from API
const loadQuickLoginOptions = async () => {
  const storeManagers = await fetch('/api/management/store-managers').then(r => r.json());
  const admins = await fetch('/api/management/admin-users').then(r => r.json());
  const testUsers = await fetch('/api/management/test-users').then(r => r.json());
  
  setQuickLoginOptions({
    storeManager: storeManagers[0],
    admin: admins[0],
    testUser: testUsers[0]
  });
};

// In render:
<Button 
  onClick={() => quickLogin(quickLoginOptions.storeManager)}
  disabled={loading || !quickLoginOptions.storeManager}
>
  Store Manager Login ({quickLoginOptions.storeManager?.firstName})
</Button>
```

---

## Summary of Changes

| Aspect | Before | After |
|--------|--------|-------|
| **Email Entry** | Manual text input | Parsed + auto-fills from DB |
| **User Data** | Manual entry (error-prone) | Auto-populated from store_managers.json |
| **Role Assignment** | Backend guesses | Exact match from data files |
| **Test Users** | Hardcoded in code | Managed via API |
| **Validation** | Limited | Email pattern + data file check |
| **Admin Users** | Not verified | Checked against admin_users.json |
| **Site Owners** | Not verified | Checked against site_owners.json |
| **Quick Buttons** | Hardcoded fake data | Real users from API |

---

## Migration Path (No Breaking Changes)

The good news: **The new system is backward compatible!**

### Phase 1: Current State
- LoginPage works as-is
- New API endpoints available but not used

### Phase 2: Add Smart Email Parsing
- Add `handleEmailChange` function
- Auto-fill fields when user types email
- No change to `handleSubmit`

### Phase 3: Update Quick Login
- Load real data instead of hardcoded
- Show available test users

### Phase 4: Optional - Admin Management UI
- New page for managing admins/site owners/test users
- Only visible to admins

---

## Recommended Implementation

**Immediate (Low Risk):**
1. ✅ Keep current LoginPage working as-is
2. ✅ Add new API endpoints (done)
3. ⏳ Add optional email auto-fill feature
4. ⏳ Update quick login to use real data

**Later (Phase 2):**
- Create Admin Management UI
- Full integration with Walmart database

**No Breaking Changes** - users can still enter credentials manually!
