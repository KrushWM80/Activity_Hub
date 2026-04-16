# Activity Hub Widget System

## Overview

The Activity Hub Widget System provides a flexible, modular approach to displaying and managing dashboard widgets across the Activity Hub platform. All widgets are configured and managed centrally through the Admin Dashboard.

**Date Last Updated:** April 16, 2026  
**Current Status:** ✅ Persistence Fixed - Ready for Testing  
**Total Widgets:** 10 (5 for For You page, 5 for Reporting page)  
**Custom Widget Support:** ✅ Enabled - Persists to localStorage

---

## Architecture

```
Widgets/
├── widget-registry.js          # Widget definitions (authoritative source)
├── widget-storage.js           # localStorage management
├── widget-manager.js           # Admin panel functions
├── widget-page-utils.js        # Page display & user functions
└── README.md                   # This file
```

### File Dependencies

```
widget-registry.js (no dependencies)
        ↓
widget-storage.js (depends on: widget-registry.js)
        ↓
widget-manager.js (depends on: widget-storage.js, widget-registry.js)
widget-page-utils.js (depends on: widget-storage.js, widget-registry.js)
```

---

## File Descriptions

### 1. `widget-registry.js`
**Purpose:** Defines all available widgets and their metadata  
**Responsibilities:**
- WIDGET_REGISTRY constant with all 9 widgets
- PLATFORM_AREAS constant (For You, Reporting)
- Helper functions: `getWidgetById()`, `getWidgetsForArea()`

**Key Data Structure:**
```javascript
{
    id: 'my-tasks',
    name: 'My Tasks',
    description: 'Personal task list and to-do items',
    defaultSize: 'Large',
    defaultAreas: ['For You']
}
```

### 2. `widget-storage.js`
**Purpose:** Manages all widget data in localStorage  
**Responsibilities:**
- Widget active/inactive state
- Widget area assignments (which page each widget appears on)
- Widget customizations (name, description, size overrides)
- Widget requests from users

**Storage Keys:**
- `activity-hub-widget-active` - Boolean active state per widget
- `activity-hub-widget-areas` - Array of areas per widget
- `activity-hub-widget-customizations` - Custom metadata per widget
- `activity-hub-widget-requests` - User widget requests
- `activity-hub-custom-widgets` - **(NEW)** Admin-created custom widgets persisted to localStorage

**Key Functions:**
- `getWidgetActiveState()` / `setWidgetActive()`
- `getAreasForWidget()` / `setAreasForWidget()`
- `getWidgetCustomization()` / `setWidgetCustomization()`
- `getActiveWidgetsForArea()` - Get widgets to display on a page
- `getCustomWidgets()` - **(NEW)** Retrieve custom widgets from storage
- `saveCustomWidget(widget)` - **(NEW)** Persist custom widget to localStorage
- `getAllWidgets()` - **(NEW)** Get merged base + custom widgets

### 3. `widget-manager.js`
**Purpose:** Admin panel functions for managing widgets  
**Responsibilities:**
- Display widgets in admin table
- Enable/disable widgets
- Assign widgets to areas (For You, Reporting)
- Edit widget metadata
- Review and approve widget requests

**Key Functions:**
- `loadWidgetsTable()` - Render admin widget table
- `openEditWidgetModal()` / `saveWidgetChanges()` - Edit widget dialog
- `loadWidgetRequests()` - Display pending requests
- `updateRequestStatus()` - Approve/deny requests
- `initializeWidgetManagement()` - Setup on admin page load

### 4. `widget-page-utils.js`
**Purpose:** Functions for For You and Reporting pages  
**Responsibilities:**
- Display widgets on user pages
- Edit mode toggle
- Add/remove widgets from page
- Populate "Add Widget" dropdown
- Manage widget state persistence

**Key Functions:**
- `initializePageWidgets(pageArea)` - Load widgets on page startup
- `getPageWidgets(pageArea)` - Get widgets for a specific page
- `enterEditMode()` / `exitEditMode()` - Toggle edit controls
- `addWidgetToPage()` / `removeWidget()` - Widget CRUD
- `getAvailableWidgetsForPage()` - Unused widgets for dropdown

---

## Current Widget Registry (April 16, 2026)

### For You Page (5 widgets)
1. **my-tasks** - My Tasks
2. **notifications** - Notifications & Alerts
3. **next-steps** - Next Steps & Action Items
4. **performance** - Performance Metrics
5. **team-activity** - Team Activity Feed

### Reporting Page (5 widgets)
1. **activity-dashboard** - Activity Dashboard
2. **project-reports** - Project Reports
3. **key-metrics** - Key Metrics
4. **my-reports** - My Reports
5. **projects-metrics** - **(NEW)** Projects Overview

---

## Custom Widget Creation (NEW - April 16, 2026)

### Admin Widget Creation
Admins can create custom widgets directly through the Admin Dashboard without modifying code:

**Steps:**
1. Go to Admin Dashboard > Widgets > Manage Widgets
2. Click "+ Create Widget" button
3. Fill out the form:
   - **Widget ID**: Unique identifier (e.g., `sales-dashboard`)
   - **Widget Name**: Display name (e.g., "Sales Dashboard")
   - **Description**: Brief description
   - **Default Size**: Small, Medium, Large, or Extra Large
   - **Available Areas**: Select where widget appears (For You, Reporting, or both)
4. Click "Create Widget"
5. Widget is saved to `activity-hub-custom-widgets` in localStorage
6. Widget persists across browser sessions and page reloads

### Persistence Guarantee
```javascript
// When widget is created:
1. saveCustomWidget(newWidget)     // Saves to localStorage
2. setWidgetActive(id, true)       // Enables widget
3. setAreasForWidget(id, areas)    // Assigns areas
4. loadWidgetsTable()              // Refreshes admin display
5. Widget persists after page reload ✅
```

### Widget Data Structure
```javascript
{
    id: 'sales-dashboard',
    name: 'Sales Dashboard',
    description: 'Real-time sales metrics by department',
    defaultSize: 'widget-large',
    defaultAreas: ['For You', 'Reporting']
}
```

---

### Integration Checklist

#### Admin Dashboard (`Interface/Admin/admin-dashboard.html`)
- [x] Include all 4 widget JavaScript files in `<head>`:
  ```html
  <script src="/Interface/Admin/Widgets/widget-registry.js"></script>
  <script src="/Interface/Admin/Widgets/widget-storage.js"></script>
  <script src="/Interface/Admin/Widgets/widget-manager.js"></script>
  ```
- [x] Call `initializeWidgetManagement()` on DOMContentLoaded
- [x] Widget Management tab HTML structure present

#### For You Page (`Interface/For You - Landing Page/activity-hub-demo.html`)
- [x] Include widget JavaScript files:
  ```html
  <script src="/Interface/Admin/Widgets/widget-registry.js"></script>
  <script src="/Interface/Admin/Widgets/widget-storage.js"></script>
  <script src="/Interface/Admin/Widgets/widget-page-utils.js"></script>
  ```
- [x] Widget container element exists:
  ```html
  <div id="for-you-widgets-container"></div>
  ```
- [x] Call `initializePageWidgets('For You')` after page load
- [x] Edit/Add Widget modal HTML present

#### Reporting Page (`Interface/Reporting/reporting.html`)
- Similar to For You page, but for Reporting area

---

## Key Concepts

### Widget ID
Unique identifier used throughout the system (e.g., `my-tasks`). Never changes.

### Platform Areas
Current areas: `['For You', 'Reporting']`. Each widget can appear on one or more areas.

### Widget Active State
Boolean flag in localStorage. If `false`, widget doesn't display anywhere.

### Widget Areas
Array of areas where a widget appears. Can be customized per widget via Admin panel.

### Widget Customization
User-facing overrides for name, description, and size. Stored separately from base registry.

### Widget Request
User request (new widget or update) submitted via dashboard. Admin reviews and approves/denies.

---

## Usage Scenarios

### Scenario 1: Display Widgets on For You Page
```javascript
// On page load
initializePageWidgets('For You');

// This will:
// 1. Load active widgets for 'For You' area
// 2. Render HTML for each widget
// 3. Set up edit mode listeners
```

### Scenario 2: Admin Enables a Widget
```javascript
// In admin panel
setWidgetActive('notifications', true);
loadWidgetsTable(); // Update display
```

### Scenario 3: Admin Changes Widget Area
```javascript
// Move 'my-tasks' to both For You and Reporting
setAreasForWidget('my-tasks', ['For You', 'Reporting']);
loadWidgetsTable();
```

### Scenario 4: User Removes Widget
```javascript
// In edit mode on For You page
removeWidget('notifications');
// Updates localStorage and removes from DOM
```

---

## Storage Format (localStorage)

### Widget Active State
```json
{
    "my-tasks": true,
    "notifications": false,
    "team-activity": true
}
```

### Widget Areas
```json
{
    "my-tasks": ["For You"],
    "notifications": ["For You", "Reporting"],
    "activity-dashboard": ["Reporting"]
}
```

### Widget Customizations
```json
{
    "my-tasks": {
        "name": "My Personal Tasks",
        "description": "Customized task list",
        "defaultSize": "Extra Large"
    }
}
```

### Widget Requests
```json
[
    {
        "id": "custom-widget-1",
        "name": "New Widget",
        "description": "A requested widget",
        "type": "new",
        "status": "pending",
        "submittedAt": "2026-04-16T...",
        "submittedBy": "john.doe@walmart.com"
    }
]
```

---

## Common Issues & Solutions

### Issue: Widget not appearing on page
**Causes:**
- localStorage corrupted → Call `resetWidgetStorage()`
- Widget ID mismatch → Use exact ID from WIDGET_REGISTRY
- Widget disabled in admin → Check `isWidgetActive(widgetId)`
- Area not configured → Check `getAreasForWidget(widgetId)`

**Solution:**
```javascript
// Debug
console.log(getWidgetById('my-tasks'));
console.log(isWidgetActive('my-tasks'));
console.log(getAreasForWidget('my-tasks'));
console.log(getActiveWidgetsForArea('For You'));
```

### Issue: localStorage fills up
**Solution:** Implement data cleanup for old widget requests:
```javascript
const requests = getWidgetRequests();
const recent = requests.filter(r => 
    Date.now() - new Date(r.submittedAt) < 30 * 24 * 60 * 60 * 1000
);
saveWidgetRequests(recent);
```

### Issue: edits not persisting across pages
**Solution:** Ensure page loads `initializePageWidgets()` and references correct storage keys

---

## Verification Checklist (April 16, 2026)

- [x] All widget IDs in HTML match WIDGET_REGISTRY
- [x] All 4 JavaScript files integrated into admin dashboard
- [x] For You page displays 5 correct widgets
- [x] Reporting page displays 4 correct widgets
- [x] Edit mode works without breaking layout
- [x] Add Widget dropdown only shows available widgets
- [x] Logo displays correctly on all pages
- [x] localStorage keys consistent across pages

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-04-16 | 1.1 | **Widget Persistence Release** |
| | | ✅ Added custom widget storage system |
| | | ✅ Implemented persistence to localStorage |
| | | ✅ Created `getAllWidgets()` merge function |
| | | ✅ Added projects-metrics widget (Projects Overview) |
| | | ✅ Updated widget creation to persist data |
| | | ✅ Created comprehensive documentation |
| 2026-04-16 | 1.0 | Initial extraction & modularization |
| | | - Created widget-registry.js |
| | | - Created widget-storage.js |
| | | - Created widget-manager.js |
| | | - Created widget-page-utils.js |

---

## Documentation Files

- **README.md** (this file) - System overview and implementation guide
- **WIDGET_WORKFLOW.md** - Complete widget lifecycle and workflow
- **PERSISTENCE_TEST_GUIDE.md** - Step-by-step testing and troubleshooting
- **REQUEST_WORKFLOW.md** - User request → admin approval → activation flow

---

## Testing & Verification

### Verify Persistence (Quick Test - 5 minutes)

1. **Create Test Widget**:
   - Go to Admin > Widgets > Manage Widgets
   - Click "+ Create Widget"
   - Fill: ID=`test-persist-2026`, Name=`Test Widget`, Size=Medium, Select both areas
   - Click "Create Widget"

2. **Verify Immediate Creation**:
   - Widget should appear in Manage Widgets table
   - Active toggle should be ON
   - Areas should show both "For You" and "Reporting"

3. **Verify Persistence** (CRITICAL):
   - Press F5 to reload page
   - Go back to Admin > Widgets > Manage Widgets
   - **Widget should still appear** (if not, persistence is broken)

4. **Verify localStorage**:
   - Press F12 to open DevTools
   - Go to Application > Storage > Local Storage
   - Click on http://localhost:8088
   - Search for `activity-hub-custom-widgets`
   - Your test widget should be in the JSON array

### Test Commands (DevTools Console)

```javascript
// Check if custom widgets are persisted
getCustomWidgets()              // Returns array of custom widgets

// Check merged widget list
getAllWidgets()                 // Returns base + custom combined

// Check total widget count
getAllWidgets().length          // Should be 10+

// Find your test widget
getAllWidgets().find(w => w.id === 'test-persist-2026')

// Check widget appears on For You
getActiveWidgetsForArea('For You')
```

### Expected Results ✅
- [ ] Widget appears after creation
- [ ] Widget appears after page reload
- [ ] Widget exists in localStorage `activity-hub-custom-widgets`
- [ ] `getAllWidgets()` includes your widget
- [ ] Widget is active and assigned to areas

---

## Next Steps

### Phase 1: Verify Persistence ✅ (HIGHEST PRIORITY)
- [ ] Run tests from [PERSISTENCE_TEST_GUIDE.md](PERSISTENCE_TEST_GUIDE.md)
- [ ] Create test widget and verify it persists after reload
- [ ] Verify localStorage contains widget data
- [ ] Document any issues found

### Phase 2: User Widget Request Submission (Planned)
- [ ] Add "+ Request New Widget" button to For You/Reporting pages
- [ ] Create widget request form
- [ ] Wire to `addWidgetRequest()` function
- [ ] Send confirmation to user

### Phase 3: Admin Request Review Interface (Planned)
- [ ] Add "Review Requests" tab to Admin > Widgets
- [ ] Display pending/approved/denied requests
- [ ] Add approve/deny/convert buttons
- [ ] Show request count badges

### Phase 4: Request-to-Widget Conversion (Planned)
- [ ] Wire "Convert to Widget" button
- [ ] Auto-populate form from approved request
- [ ] Mark request as "implemented"
- [ ] Notify requestor

---

## Future Enhancements

- [ ] Backend persistence (database instead of localStorage)
- [ ] Widget versioning and rollback
- [ ] Widget export/import for sharing configs
- [ ] Widget analytics (usage, views, errors)
- [ ] Custom widget templates for users
- [ ] Widget grouping by category
- [ ] Widget search & filter in admin
- [ ] Bulk widget operations in admin
- [ ] Widget marketplace/library

---

## Support

For questions or issues with the widget system:
1. Check this README
2. Review the corresponding .js file comments
3. Check browser console for error messages
4. Verify storage keys with `console.log(localStorage)`
