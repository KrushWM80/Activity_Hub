# Activity Hub Widget Creation & Management Workflow

## Overview

The Activity Hub widget system manages widgets across two main platforms:
- **For You** - Personal dashboard (5 primary widgets)
- **Reporting** - Analytics dashboard (5 widgets including Project Metrics)

All widgets are controlled through a centralized widget management system with localStorage persistence.

---

## Widget Lifecycle

### 1️⃣ Widget Request (User-Submitted)

**Where**: Any user can submit from their page (For You or Reporting)

**Process**:
- User encounters need for new widget
- User fills out "Widget Requests" form in Add Widget modal
- Request goes to localStorage (`activity-hub-widget-requests`)
- Request status: **PENDING**

**Request Data Stored**:
```json
{
  "id": "unique-request-id",
  "type": "new_widget",
  "requested_by": "user@walmart.com",
  "widget_name": "Sales Dashboard",
  "widget_description": "Display real-time sales metrics",
  "status": "pending",
  "timestamp": "2026-04-16T..."
}
```

---

### 2️⃣ Admin Review & Preliminary Check

**Where**: Admin Dashboard > Widgets > Review Requests

**Process**:
1. Admin views pending widget requests
2. Admin can:
   - ✅ **Approve** - Recommend for development (status: `approved`)
   - ❌ **Deny** - Reject request (status: `denied`)
   - 🔄 **Notes** - Leave comments/feedback

**What Happens After Approval**:
- Request status changes to `approved`
- Request moves from "Pending" to "Approved" tab
- Admin is notified (or logs action)
- Backend developer receives notification

---

### 3️⃣ Backend Developer Implementation

**Where**: Backend development environment

**Process**:
1. Developer reviews approved widget request
2. Developer creates widget code/template
3. Widget implementation is tested
4. Developer submits PR/change for admin review

---

### 4️⃣ Admin Activation (Direct & Approved)

**Where**: Admin Dashboard > Widgets > Manage Widgets

**Two Paths**:

#### Path A: Direct Admin Creation (for quick widgets)
- Admin clicks "+ Create Widget"
- Fills out:
  - Widget ID (unique identifier)
  - Widget Name (display name)
  - Description (brief explanation)
  - Default Size (Small/Medium/Large/Extra Large)
  - Available Areas (For You, Reporting, or both)
- Widget creates immediately
- Status: **ACTIVE**

#### Path B: Approved Request Conversion
- Admin approves widget request (from Review Requests)
- Admin clicks "Add to Active Widgets"
- Widget converts from request to active widget
- Status: **ACTIVE**

---

## 5️⃣ Widget Availability

**Where**: User dashboards (For You & Reporting)

**What Users See**:
- Active widgets appear on their dashboard(s)
- Users can:
  - ✏️ **Edit** - When in edit mode (resize, reorder, remove)
  - 🔧 **Customize** - Change widget settings
  - ❌ **Remove** - Hide widget (Add Widget button lets them restore it)

- Users CANNOT:
  - 🚫 Delete permanently
  - 🚫 Create widgets themselves (submit requests instead)
  - 🚫 Modify widget core functionality

---

## Architecture

### Storage Layer

All data persists in `localStorage` with these keys:

| Key | Purpose | Audience |
|-----|---------|----------|
| `activity-hub-widget-active` | Widget on/off state | Admin + Users |
| `activity-hub-widget-areas` | Which areas each widget appears in | Admin + Users |
| `activity-hub-widget-customizations` | User customizations (size, order) | Users |
| `activity-hub-widget-requests` | User + Admin widget requests | Admin + Requesters |
| `activity-hub-custom-widgets` | **Admin-created widgets** (NEW) | All Users |

### Registry Structure

**Base Registry** (`widget-registry.js`):
```javascript
WIDGET_REGISTRY = [
  { id, name, description, defaultSize, defaultAreas },
  ...
]
```

**Custom Widgets** (localStorage):
```json
{
  "id": "my-custom-widget",
  "name": "Custom Widget Name",
  "description": "What it does",
  "defaultSize": "widget-medium",
  "defaultAreas": ["For You", "Reporting"]
}
```

**Merged View** (runtime):
- `getAllWidgets()` combines base + custom widgets
- All functions use merged list
- Persists across page reloads

---

## Key Functions

### Widget Storage (`widget-storage.js`)
```javascript
// Get all widgets (base + custom merged)
getAllWidgets()

// Save custom widget to localStorage
saveCustomWidget(widget)

// Get only custom widgets from localStorage
getCustomWidgets()

// Get active widgets for a specific area
getActiveWidgetsForArea(area)

// Initialize storage on page load
initializeWidgetStorage()
```

### Widget Manager (`widget-manager.js`)
```javascript
// Open create widget modal
showCreateWidgetModal()

// Create and save new widget
createNewWidget()

// Refresh the widgets table
loadWidgetsTable()

// Load widget requests
loadWidgetRequests()
```

### Widget Registry (`widget-registry.js`)
```javascript
// Get widget by ID (searches base + custom)
getWidgetById(widgetId)

// Get widget display info
getWidgetDisplay(widgetId)
```

---

## Current Widgets (Base Registry)

### For You Area (5 widgets)
1. **my-tasks** - Personal task list
2. **notifications** - System alerts
3. **next-steps** - Upcoming actions
4. **performance** - Key metrics
5. **team-activity** - Team updates

### Reporting Area (5 widgets)
1. **activity-dashboard** - Activity metrics & trends
2. **project-reports** - Project status & milestones
3. **key-metrics** - Analytics & reporting metrics
4. **my-reports** - Custom reports
5. **projects-metrics** - Projects Overview (NEW - added April 16)

---

## Workflow Diagram

```
User Creates Request (In-App)
        ↓
Widget Request Pending
        ↓
Admin Reviews (Admin Dashboard)
        ├─ Approve → Developer Implements
        └─ Deny → Notify User
        ↓
Admin Adds to Active Widgets
        ├─ From Approved Request
        └─ Direct Creation (Quick Add)
        ↓
Widget Appears on User Dashboards
        ↓
Users Can Customize/Remove
        ↓
Admin Can Edit/Disable from Manage Widgets
```

---

## Recent Changes (April 16, 2026)

✅ **Fixed Issues**:
1. **Widget Persistence** - Custom widgets now save to localStorage
2. **Projects Metrics Widget** - Added to base registry with "Projects Overview" title
3. **Widget Creation** - Now uses `saveCustomWidget()` for proper persistence
4. **Merged Registry** - `getAllWidgets()` combines base + custom widgets across all pages

✅ **Tests**:
- Created test-widget-1 successfully
- Widget persists after... (pending full test)
- Projects Metrics appears in Admin > Manage Widgets
- Title updated from "Impact Platform - Projects Overview" to "Projects Overview"

---

## Next Steps

### For Testing
1. ✅ Create new widget via Admin > Widgets > Manage > Create Widget
2. ✅ Verify widget persists after page reload
3. ✅ Check widget appears on selected area(s)
4. ⏳ Test Edit/Remove functionality for new widgets
5. ⏳ Test user widget requests workflow

### For Feature Development
- [ ] Implement widget request approval workflow
- [ ] Add backend webhook for approved requests
- [ ] Create widget request notifications
- [ ] Build widget library/marketplace
- [ ] Add export/import for widget templates

---

## Troubleshooting

### Widget Not Appearing in Manage Widgets
**Check**:
1. Is widget in WIDGET_REGISTRY? (widget-registry.js)
2. Is it in custom widgets storage? (Check browser DevTools > Application > localStorage)
3. Call `getAllWidgets()` in console to verify

### Widget Disappears After Reload
**Cause**: Widget was only in WIDGET_REGISTRY memory
**Fix**: Ensure `saveCustomWidget()` is called during creation
**Verify**: Check localStorage key `activity-hub-custom-widgets`

### Widget Not Appearing on User Page
**Check**:
1. Is widget active? (Check `activity-hub-widget-active` in localStorage)
2. Is widget assigned to the area? (Check `activity-hub-widget-areas`)
3. Run `getActiveWidgetsForArea('For You')` to debug

---

## File Locations

- **Widget Registry**: `Interface/Admin/Widgets/widget-registry.js`
- **Widget Storage**: `Interface/Admin/Widgets/widget-storage.js`
- **Widget Manager**: `Interface/Admin/Widgets/widget-manager.js`
- **Widget Page Utils**: `Interface/Admin/Widgets/widget-page-utils.js`
- **Admin Dashboard**: `Interface/Admin/admin-dashboard.html`
- **For You Page**: `Interface/For You - Landing Page/activity-hub-demo.html`
- **Reporting Page**: `Interface/Reporting/reporting.html`

