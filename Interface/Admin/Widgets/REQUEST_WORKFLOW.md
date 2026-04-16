# Widget Request → Approval → Activation Workflow

## Complete User Journey

### 1️⃣ User Creates Widget Request

**Where**: Any user page (For You or Reporting)

**What User Does**:
1. User navigates to For You or Reporting page
2. User clicks "Add Widget" or "Customize" button
3. User clicks "+ Request New Widget" 
4. User fills form:
   - Widget Name (e.g., "Sales Performance Dashboard")
   - Description (e.g., "Shows real-time store sales by department")
   - Which area(s) they want it
   - Why they need it (optional notes)
5. User clicks "Submit Request"

**What Happens Behind-the-Scenes**:
- Request saved to localStorage: `activity-hub-widget-requests`
- Request status: `pending`
- Timestamp recorded: `submittedAt`
- Request ID generated: UUID or auto-increment
- Requestor email/name recorded (if available)

**User Sees**: "✅ Request submitted to admin team! You'll be notified when it's ready."

---

### 2️⃣ Admin Reviews Widget Requests

**Where**: Admin Dashboard > Widgets > Review Requests

**What Admin Sees**:
- Table of all widget requests
- Columns:
  - Requested By (user name/email)
  - Widget Name
  - Description
  - Areas Requested
  - Date Submitted
  - Status (Pending/Approved/Denied)
  - Action Buttons

**What Admin Does** (for each request):
```
Option A: APPROVE REQUEST
├─ Read description and notes
├─ Determine if feasible/useful
├─ Click "✅ Approve" button
└─ Status changes to "approved"
   └─ Next: Admin or developer implements widget

Option B: DENY REQUEST
├─ Read description
├─ Determine why not feasible
├─ Click "❌ Deny" button
├─ Enter notes (optional reason)
└─ Status changes to "denied"
   └─ System: Notifies requestor (email/notification)

Option C: NEEDS INFO
├─ Click "❓ Request More Info"
├─ Add comments/questions
└─ Status: "awaiting-info"
   └─ Requestor notified to clarify
```

**Admin Table View Example**:
```
Requested By | Widget Name | Status | Actions
─────────────┼─────────────┼────────┼────────
john@store   | Sales Dash  | pending| ✅ Approve | ❌ Deny
jane@hq      | Task Board  | pending| ✅ Approve | ❌ Deny
bob@store    | Reports     | denied | View Notes
```

---

### 3️⃣ Admin Adds Approved Widget to Active

**For Approved Requests**:

When request is approved, admin has two paths:

#### Path A: Create from Approved Request
```
1. Admin clicks "Convert to Widget" on approved request
2. Widget auto-generates with:
   - ID: auto-generated (widget-sales-dashboard-001)
   - Name: from request (Sales Dashboard)
   - Description: from request
   - Areas: from request (For You, Reporting, etc.)
3. Widget moves from "Approved" to "Active Widgets"
```

#### Path B: Quick Admin Create (for simple widgets)
```
1. Admin goes to Manage Widgets > Active Widgets
2. Clicks "+ Create Widget"
3. Fills custom widget form (same as in current system)
4. Widget added directly to Active Widgets
```

**Result**: Widget now appears in "Manage Widgets > Active Widgets" tab

---

### 4️⃣ Admin Configures Widget Settings

**What Admin Sees in Manage Widgets**:
```
Active Widgets Table:
├─ Widget ID
├─ Widget Name
├─ Description
├─ Active Toggle (ON/OFF)
├─ Areas (For You ✓, Reporting ✓)
└─ Actions (Edit | Delete | Preview)
```

**Admin Can**:
- ✏️ Edit widget settings
- 🔄 Toggle On/Off (control visibility)
- 📍 Change area assignments
- 🗑️ Delete widget (optional)
- 👁️ Preview widget

**Typical Configuration**:
```
Widget: Sales Dashboard
├─ Areas: Mark as available in "For You" + "Reporting"
├─ Status: ACTIVE (toggle ON)
└─ Users can now see this widget
```

---

### 5️⃣ Widget Appears on User Pages

**Automatic**:
- User visits For You or Reporting page
- Page loads active widgets for that area
- Widget appears in "Add Widget" list
- User can add it to their dashboard

**What User Can Do**:
- ✅ Add widget to their page
- ✅ Customize appearance (size, position)
- ✅ Remove widget (can re-add later)
- ❌ Cannot delete or modify widget behavior

---

## Current System State (April 16, 2026)

### ✅ Implemented Features:
1. **Widget Creation** - Direct creation in Admin > Manage Widgets
2. **Widget Registry** - Base widgets defined in code
3. **Custom Widgets** - NEW - Stored in localStorage
4. **Widget Storage** - Persistent storage system
5. **Widget Persistence** - NEW - Saves across page reloads

### ⏳ Partially Implemented:
- Widget Requests - Data structure exists, UI needs work
- Request Review - Table not yet displayed to admin
- Request Approval - Functions exist but not wired to UI

### ❌ Not Yet Implemented:
- Request Submission UI for users
- Request Review & Approval UI for admin
- "Convert to Widget" button
- User notifications for request status changes
- Backend persistence (currently localStorage only)

---

## Implementation Priority

### Phase 1 (Current) - Fix Widget Persistence ✅ DONE
- ✅ Custom widget storage
- ✅ Save/load from localStorage
- ✅ Merge base + custom widgets
- ✅ Test persistence across page reloads

### Phase 2 (Next) - User Request Submission
**Work Needed**:
1. Add "+ Request New Widget" button to Add Widget modal
2. Create widget request form
3. Wire form submission to `addWidgetRequest()` function
4. Clear form after submission

**Files to Modify**:
- `activity-hub-demo.html` (For You page)
- `reporting.html` (Reporting page)
- `widget-page-utils.js` (request submission handler)

### Phase 3 - Admin Request Review
**Work Needed**:
1. Add "Review Requests" tab to Admin > Widgets
2. Create request table display
3. Add approve/deny/info-needed buttons
4. Wire buttons to update request status
5. Show action counts on tab

**Files to Modify**:
- `admin-dashboard.html` (add Review Requests section)
- `widget-manager.js` (add request handling functions)

### Phase 4 - Request to Widget Conversion
**Work Needed**:
1. Add "Convert to Widget" button in request table
2. Auto-populate widget form from request
3. Create widget on form submission
4. Move request status to "implemented"
5. Notify requestor (optional)

**Files to Modify**:
- `widget-manager.js` (add conversion function)
- `admin-dashboard.html` (add conversion button)

---

## Console Testing Commands

### Test Widget Request Flow Manually

```javascript
// 1. Create a test request
addWidgetRequest({
  type: 'new_widget',
  widget_name: 'Sales Dashboard',
  widget_description: 'Real-time sales metrics',
  requested_by: 'user@walmart.com',
  status: 'pending'
});

// 2. View all requests
getWidgetRequests();

// 3. Approve a request (change status at index 0)
updateWidgetRequest(0, { status: 'approved' });

// 4. View updated request
getWidgetRequests()[0];

// 5. Convert approved request to widget
const request = getWidgetRequests()[0];
const newWidget = {
  id: 'sales-dashboard-001',
  name: request.widget_name,
  description: request.widget_description,
  defaultSize: 'widget-large',
  defaultAreas: ['For You', 'Reporting']
};
saveCustomWidget(newWidget);

// 6. Mark request as implemented
updateWidgetRequest(0, { status: 'implemented' });

// 7. Verify widget appears in all widgets
getAllWidgets().find(w => w.id === 'sales-dashboard-001');
```

---

## FileStructure After Full Implementation

```
Interface/
└── Admin/
    └── Widgets/
        ├── WIDGET_WORKFLOW.md (Overview)
        ├── PERSISTENCE_TEST_GUIDE.md (Testing)
        ├── REQUEST_WORKFLOW.md (This file)
        ├── widget-registry.js (Base widgets)
        ├── widget-storage.js (Storage layer)
        ├── widget-manager.js (Admin functions)
        └── widget-page-utils.js (Page functions)

Interface/Admin/
└── admin-dashboard.html
    └── Sections:
        ├── Manage Widgets > Active Widgets
        ├── Manage Widgets > Review Requests (NEW)
        └── Manage Widgets > Create Widget (EXISTS)

Interface/For You - Landing Page/
└── activity-hub-demo.html
    └── Add Widget Modal
        ├── Available Widgets (existing)
        └── Request New Widget (NEW)

Interface/Reporting/
└── reporting.html
    └── Add Widget Modal
        ├── Available Widgets (existing)
        └── Request New Widget (NEW)
```

---

## Summary Table

| Phase | Feature | Status | Users | Admins | Location |
|-------|---------|--------|-------|--------|----------|
| 1 | Create Widget Direct | ✅ Done | ❌ | ✅ | Manage Widgets |
| 1 | Widget Persistence | ✅ Done | ✅ | ✅ | localStorage |
| 2 | Request Submission | ⏳ TODO | ✅ | ❌ | Add Widget Modal |
| 3 | Request Review | ⏳ TODO | ❌ | ✅ | Admin Dashboard |
| 4 | Request Approval | ⏳ TODO | ❌ | ✅ | Admin Dashboard |
| 4 | Auto-Convert | ⏳ TODO | ❌ | ✅ | Admin Dashboard |
| 5 | Notifications | ⏳ TODO | ✅ | ✅ | Email/In-App |

---

## Key Design Principles

1. **User Perspective**:
   - Users request widgets they need
   - They don't manage widget registry
   - They can customize but not create core widgets
   - They get feedback on their requests

2. **Admin Perspective**:
   - Admin reviews all requests
   - Admin decides what gets built
   - Admin controls visibility and settings
   - Admin can quickly create simple widgets

3. **System Perspective**:
   - Two widget sources: Base (code) + Custom (admin-created)
   - All widgets stored and retrieved consistently
   - localStorage for now, backend-ready architecture
   - Clean separation of concerns

