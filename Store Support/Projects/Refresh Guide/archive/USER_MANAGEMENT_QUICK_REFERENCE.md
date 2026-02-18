# User Management Quick Reference

## Files & Locations

| Purpose | File | Location | Endpoint |
|---------|------|----------|----------|
| Store Managers/Coaches | `store_managers.json` | `server/data/` | `GET /api/management/store-managers` |
| Admin Users | `admin_users.json` | `server/data/` | `/api/management/admin-users` |
| Site Owners | `site_owners.json` | `server/data/` | `/api/management/site-owners` |
| Test Users | `test_users.json` | `server/data/` | `/api/management/test-users` |
| API Routes | `userManagement.js` | `server/src/routes/` | — |

---

## Quick Add Operations

### Add Admin User
```bash
curl -X POST http://localhost:5000/api/management/admin-users \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@walmart.com",
    "firstName": "John",
    "lastName": "Admin",
    "title": "Administrator",
    "adminLevel": "admin"
  }'
```

### Add Site Owner
```bash
curl -X POST http://localhost:5000/api/management/site-owners \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@walmart.com",
    "firstName": "Bob",
    "lastName": "Owner",
    "region": "Region A",
    "stores": ["2425", "5000"]
  }'
```

### Add Test User
```bash
curl -X POST http://localhost:5000/api/management/test-users \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.user@wal-mart.com",
    "firstName": "Test",
    "lastName": "User",
    "storeNumber": "9999",
    "jobTitle": "Store Manager",
    "role": "manager"
  }'
```

---

## API Endpoints Summary

### Admin Users
- `GET /api/management/admin-users` - List all
- `GET /api/management/admin-users/:id` - Get one
- `POST /api/management/admin-users` - Create
- `PUT /api/management/admin-users/:id` - Update
- `DELETE /api/management/admin-users/:id` - Delete

### Site Owners
- `GET /api/management/site-owners` - List all
- `GET /api/management/site-owners/:id` - Get one
- `POST /api/management/site-owners` - Create
- `PUT /api/management/site-owners/:id` - Update
- `DELETE /api/management/site-owners/:id` - Delete

### Store Managers
- `GET /api/management/store-managers` - List all
- `GET /api/management/store-managers/store/:storeNumber` - By store

### Test Users
- `GET /api/management/test-users` - List all
- `POST /api/management/test-users` - Create

---

## Test Logins

**Store Manager (Store #2425):**
- Email: `john.s2425.us@wal-mart.com`

**Store Coach (Store #2425):**
- Email: `sarah.s2425.us@wal-mart.com`

**Admin:**
- Email: `kendall.rush@walmart.com`

**Business Owner:**
- Email: `test.businessowner@walmart.com`

**Test Users:**
- Manager: `test.manager@wal-mart.com`
- Coach: `test.coach@wal-mart.com`
- Admin: `test.admin@walmart.com`

---

## Adding Users to Walmart Database Query

When ready to integrate with `wmt-assetprotection-prod.Store_Support_Dev.Store Management Contacts`:

1. Query the table
2. Export as JSON
3. Transform to format in `store_managers.json`
4. Replace file contents
5. System automatically uses updated data

No code changes needed!

---

## Making Changes to User Data

**Option 1: Via API (Recommended)**
- Use REST endpoints
- Automatic validation
- Audit trail ready

**Option 2: Direct File Edit**
- Edit JSON files directly
- Restart backend
- Manual validation

**Option 3: Admin UI (Coming Phase 2)**
- Beautiful UI for management
- Bulk operations
- Export/Import
