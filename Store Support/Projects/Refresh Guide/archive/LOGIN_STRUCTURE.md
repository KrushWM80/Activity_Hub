# Login Structure & User Classification

## Email-Based Role Determination

The system determines user roles based on email domain pattern and store assignment.

---

## **User Role Classification Rules**

### **1. Store Manager & Store Associate (Store-Specific)**
**Email Pattern:** `.s[STORE_NUMBER].us@wal-mart.com`

**Examples:**
- `john.s2425.us@wal-mart.com` → Store #2425 Manager/Associate
- `sarah.s2425.us@wal-mart.com` → Store #2425 Manager/Associate
- `coach.s5000.us@wal-mart.com` → Store #5000 Manager/Associate

**How it works:**
1. Extract store number from email: `.s**2425**.us@wal-mart.com`
2. Look up Store Dashboard Table to find which role this person has at that store
3. Assign role: **manager** or **associate** based on Store Dashboard

**Access:**
- Can see store-specific surveys and items
- Can submit survey responses
- Field editing based on role (Manager can edit Owner/Deadline; Associate can edit Status/Notes)

---

### **2. Business Owner (Home Office - Default)**
**Email Pattern:** `@walmart.com` (Home Office email)

**Examples:**
- `mike.business@walmart.com`
- `kendall.rush@walmart.com`
- `john.doe@walmart.com`

**Requirements:**
- Must have `@walmart.com` email domain
- NOT on the Admin List
- NOT on the Site Owner List
- Automatically assigned **business** role

**Access:**
- Business Owner Dashboard (view all stores, limited reporting)
- Can create refresh requests (if enabled)
- Cannot edit store-level data

---

### **3. Admin (Home Office)**
**Email Pattern:** `@walmart.com` + On Admin List

**How it works:**
1. Check email domain: Must be `@walmart.com`
2. Check against **Admin List** table/document
3. If found: Assign role **admin**

**Access:**
- Full system access
- User management
- System configuration
- All store data and reporting

---

### **4. Site Owner (Home Office)**
**Email Pattern:** `@walmart.com` + On Site Owner List

**How it works:**
1. Check email domain: Must be `@walmart.com`
2. Check against **Site Owner List** table/document
3. If found: Assign role **site_owner**

**Access:**
- Site Owner Dashboard
- Regional store management
- Site-level reporting and analytics
- User management for assigned sites

---

## **Login Flow**

```
User enters email
        ↓
Extract email domain
        ↓
    ┌───┴────────────────────────┐
    │                            │
Is email .s[####].us@wal-mart.com?
    │ YES                        │ NO
    │                            │
    ↓                            ↓
Extract Store #           Is email @walmart.com?
    │                            │
    ↓                            ├─ YES: Check Admin List
Lookup in Store              ├─ YES: Check Site Owner List
Dashboard Table              └─ NO: Deny Access
    │
    ├─ Manager Role
    ├─ Associate Role
    └─ Not Found: Deny Access
    
Store Admin List Match → Assign Admin Role
Site Owner List Match → Assign Site Owner Role
Neither → Assign Business Owner Role
```

---

## **Data Sources Needed**

### **1. Store Managers (From Walmart Database)** ✅ CREATED
**Source:** `wmt-assetprotection-prod.Store_Support_Dev.Store Management Contacts`

**Local File:** `server/data/store_managers.json`

**Current Status:** Template created with sample data
- Store #2425: John Smith (Manager), Sarah Johnson (Coach)
- Store #5000: Mike Johnson (Manager), Lisa Anderson & David Brown (Coaches)

**How to Update:**
1. Query Walmart database for latest store contacts
2. Export as JSON
3. Replace `store_managers.json` content
4. System will automatically use updated data

---

### **2. Admin Users List** ✅ CREATED
**File:** `server/data/admin_users.json`

**Current Data:**
- Kendall Rush (kendall.rush@walmart.com) - Super Admin

**To Add/Manage Admins:**
Use API endpoint: `POST /api/management/admin-users`

**Example:**
```json
{
  "email": "neyadmin@walmart.com",
  "firstName": "John",
  "lastName": "Admin",
  "adminLevel": "admin"
}
```

---

### **3. Site Owner List** ✅ CREATED
**File:** `server/data/site_owners.json`

**Current Data:** Sample site owner entry

**To Add/Manage Site Owners:**
Use API endpoint: `POST /api/management/site-owners`

**Example:**
```json
{
  "email": "owner@walmart.com",
  "firstName": "Bob",
  "lastName": "Owner",
  "region": "Region A",
  "stores": ["2425", "5000"]
}
```

---

### **4. Test Users (For Testing)** ✅ CREATED
**File:** `server/data/test_users.json`

**Current Test Users:**
- test.manager@wal-mart.com (Store Manager - Store #9999)
- test.coach@wal-mart.com (Store Coach - Store #9999)
- test.admin@walmart.com (Admin)
- test.businessowner@walmart.com (Business Owner)

**To Add Test Users:**
Use API endpoint: `POST /api/management/test-users`

---

## **Implementation Checklist**

- [x] Create Store Managers data file (store_managers.json)
- [x] Create Admin Users list (admin_users.json)
- [x] Create Site Owners list (site_owners.json)
- [x] Create Test Users file (test_users.json)
- [x] Create User Management API Routes (userManagement.js)
- [x] Register routes in server (index.js)
- [ ] Update `LoginPage.tsx` to use new data sources
- [ ] Implement role determination logic in Auth
- [ ] Test all user types with new system
- [ ] Create Admin UI for managing users (Phase 2)
- [ ] Integrate with Walmart database (Phase 2)

---

## **Current Test Data**

### Store #2425
**Manager:** `john.s2425.us@wal-mart.com` (John Smith)
**Coaches:**
- `sarah.s2425.us@wal-mart.com` (Sarah Johnson)

### Store #5000
**Manager:** `manager.s5000.us@wal-mart.com` (Mike Johnson)
**Coaches:**
- `coach1.s5000.us@wal-mart.com` (Lisa Anderson)
- `coach2.s5000.us@wal-mart.com` (David Brown)

### Admin Users
**Super Admin:**
- `kendall.rush@walmart.com` (Kendall Rush)

### Site Owners
**Sample Site Owner:**
- `admin1@walmart.com` (Admin User) - Region A

### Test Users
For testing without database:
- `test.manager@wal-mart.com` - Store Manager (Store #9999)
- `test.coach@wal-mart.com` - Store Coach (Store #9999)
- `test.admin@walmart.com` - Admin
- `test.businessowner@walmart.com` - Business Owner

---

## **How to Add New Users**

### Add New Admin User
```bash
POST /api/management/admin-users
{
  "email": "newadmin@walmart.com",
  "firstName": "Jane",
  "lastName": "Admin",
  "adminLevel": "admin"
}
```

### Add New Site Owner
```bash
POST /api/management/site-owners
{
  "email": "owner@walmart.com",
  "firstName": "Bob",
  "lastName": "Owner",
  "region": "Region A",
  "stores": ["2425", "5000"]
}
```

### Add Test User
```bash
POST /api/management/test-users
{
  "email": "test.newuser@wal-mart.com",
  "firstName": "Test",
  "lastName": "User",
  "storeNumber": "9999",
  "role": "manager"
}
```

---

## **Next Steps**

**Immediate:**
1. ✅ Data files created
2. ✅ API endpoints created
3. ⏳ Update LoginPage.tsx to use new API
4. ⏳ Test login with different user types

**Phase 2:**
1. Create Admin Dashboard for user management
2. Add UI for managing admins, site owners, and test users
3. Integrate with Walmart `Store Management Contacts` database
4. Add audit logging for all user changes
