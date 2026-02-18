# Debug the Form - Step by Step

## What I Added

I've added a **DEBUG INFO** section that will appear below the form fields. This will show:

- **User**: Email and name of logged-in user
- **Profile**: Current profile selected (Store Manager, etc.)
- **Store**: Store number
- **isStoreManager**: TRUE/FALSE - whether system thinks you're a manager
- **canEditOwner**: TRUE/FALSE - whether Owner field should be editable
- **clickedItem**: Whether the item was found from checklist data
- **Form Data**: Current values of owner, status, deadline, notes fields

This will help us understand WHY the form isn't responding.

---

## Steps to Test

### 1. Restart Frontend Server

```powershell
# In terminal where frontend is running:
Ctrl+C

# Then restart:
cd client
npm start

# Wait for: "webpack compiled successfully"
```

### 2. Clear Browser Cache

Press: **Ctrl+Shift+Delete**
- Select: "All time"
- Check: ☑ Cached images and files
- Click: "Clear data"

### 3. Restart Browser

- Close browser completely
- Reopen it
- Go to http://localhost:3000

### 4. Login & Navigate to Form

1. Email: `store_manager@example.com`
2. Password: `password123`
3. Click "View All Items"
4. Click "Continue Survey" on any item

### 5. Look for DEBUG INFO Section

You should see a box below the form fields that looks like:

```
🐛 DEBUG INFO (Remove this section later)
User: store_manager@example.com
Profile: Store Manager
Store: 1234
isStoreManager: TRUE ✓
isStoreAssociate: FALSE ✗
canEditOwner: TRUE ✓
clickedItem: Found (item-0)
Form Data:
owner: "Coach 1" | status: "Pending" | deadline: "" | notes: ""
```

### 6. Check the Debug Values

**If you see:**

| Value | Means |
|-------|-------|
| Profile: Store Manager ✓ | Good - you're logged in as manager |
| isStoreManager: TRUE ✓ | Good - form recognizes you as manager |
| canEditOwner: TRUE ✓ | Good - Owner field SHOULD be editable |
| clickedItem: Found ✓ | Good - form found the item from checklist |

**If you see:**

| Value | Problem |
|-------|---------|
| Profile: Not Set | User context not set properly |
| isStoreManager: FALSE ✗ | Form thinks you're NOT a manager |
| canEditOwner: FALSE ✗ | Owner field will be read-only |
| clickedItem: NOT FOUND | Item wasn't found in checklist data |

### 7. Try to Change a Form Field

**Try to change Owner field:**
1. Click on "Owner (Coach)" dropdown
2. Try to select "Coach 2"
3. Watch the DEBUG INFO section
4. The "owner:" value should change to `"Coach 2"`

**If it changes:**
- Form state IS working ✓
- Problem might be UI rendering issue

**If it doesn't change:**
- Form state is NOT updating ✗
- Problem is in event handler or form initialization

### 8. Open Browser Console

Press: **F12**
- Go to "Console" tab
- Try clicking form fields
- You should see logs like:
  ```
  Field changed: owner = Coach 2
  Updated formData: {area: "", type: "", item: "", owner: "Coach 2", ...}
  ```

**If you see these logs:**
- Event handler IS working ✓
- State IS updating ✓

**If you DON'T see these logs:**
- Event handler isn't being triggered ✗
- Form fields aren't connected properly ✗

---

## Possible Issues & What They Mean

### Scenario 1: DEBUG INFO shows everything is correct BUT fields don't change

**Diagnosis**: Form state updates but UI doesn't refresh

**Next Step**: 
1. Try refreshing page with F5
2. Try closing browser and reopening
3. Check if form fields have `disabled` attribute (they shouldn't)

### Scenario 2: isStoreManager is FALSE but you logged in as manager

**Diagnosis**: `currentProfile` not being set by auth system

**Next Step**:
1. Check that you're selecting "Store Manager" profile after login
2. Check that profile selection is saving to user context

### Scenario 3: canEditOwner is FALSE

**Diagnosis**: Either not Store Manager OR marked as Associate

**Possible causes**:
- You logged in as Store Associate instead of Store Manager
- Auth system has wrong profile
- `currentProfile` has unexpected value

**Next Step**:
1. Logout completely
2. Login again as `store_manager@example.com`
3. Make sure to select "Store Manager" profile

### Scenario 4: clickedItem is NOT FOUND

**Diagnosis**: Item wasn't found in checklist-data.json

**Possible causes**:
- Item IDs don't match
- Checklist data didn't load properly
- Query params have wrong item/area/topic IDs

**Next Step**:
1. Open browser console (F12)
2. Look for error messages about loading checklist-data.json
3. Check that checklist-data.json file exists in `client/public/`

### Scenario 5: All debug info looks correct but STILL can't interact

**Diagnosis**: Might be CSS issue, Material-UI issue, or React rendering problem

**Next Step**:
1. Right-click on Owner field → "Inspect"
2. In DevTools, look for element that's blocking clicks
3. Check if there's `disabled` attribute
4. Check CSS for `pointer-events: none` or similar

---

## What to Tell Me

When you test, please share:

1. **Screenshot of DEBUG INFO section**
   - What does each value show?

2. **Are form fields clickable/editable?**
   - Can you click the dropdown?
   - Can you type in notes field?

3. **Does DEBUG INFO update when you try to change a field?**
   - Does the owner value change?
   - Does status value change?

4. **What does browser console show? (F12)**
   - Do you see the "Field changed:" logs?
   - Are there any red error messages?

5. **Any other unusual behavior?**
   - Does dropdown open but items not clickable?
   - Does calendar appear but dates not clickable?
   - Does form show but everything appears "greyed out"?

---

## File Modified

**`client/src/pages/StoreAssociate/Survey.tsx`**
- Added DEBUG INFO section below form fields
- Shows user info, permissions, and current form state
- Will help identify WHERE the problem is

**Status**: Code compiles with no errors ✅

