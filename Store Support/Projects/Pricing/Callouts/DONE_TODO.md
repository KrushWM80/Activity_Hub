# Pricing Callouts Dashboard - Done & TODO

## ✅ COMPLETED (This Week - May 1, 2026)

### Backend Fixes
- ✅ Fixed fiscal year showing 2031 → Now correctly returns 2027 by querying TODAY's date
- ✅ Fixed POST /api/callouts datetime serialization error → Converted to ISO 8601 strings
- ✅ Fixed DELETE streaming buffer error → Returns 409 with friendly "Please wait a few seconds" message
- ✅ Fixed PUT /api/callouts validation → Made content optional, title required only
- ✅ Added dynamic SQL query builder for UPDATE statements

### Frontend Enhancements
- ✅ Changed callouts table title from "Callouts for Selected Week" → "Call Outs Log"
- ✅ Added FY column (shows full year: "FY 2027")
- ✅ Added WM WK column (shows: "WK 13")
- ✅ Added Edit button with modal dialog (no more browser prompt())
- ✅ Added Delete button with proper error handling
- ✅ Edit modal with Cancel/Save buttons and keyboard shortcuts (Enter/Escape)

### Email System
- ✅ Implemented HTML email building with dashboard screenshots
- ✅ SMTP email sending via Walmart mail server (smtp-gw1.homeoffice.wal-mart.com:25)
- ✅ Email recipient database management
- ✅ Test email endpoint working with /api/send-test-email

### Dashboard UI Polish
- ✅ Walmart yellow (#FFCC00) alert banner with correct branding
- ✅ Countdown timer to Friday 4:00 PM CT
- ✅ Logo displaying correctly (walmart-spark-logo.png)
- ✅ Email recipient list showing active recipients
- ✅ Form validation for required fields
- ✅ Error messages for user feedback

---

## 📋 TODO (Next Week - May 6-10, 2026)

### PRIORITY 1: Email Content & Display Format
- [ ] **Remove Title from Call Outs Log table** - Delete the "Title" column completely
- [ ] **Remove Title from email display** - Only show Details (content field) under "Call outs" in email
- [ ] **Update email HTML builder** - Modify build_callout_email_html() to exclude title
- [ ] **Test email output** - Send test email and verify only content shows

### PRIORITY 2: Edit Functionality Expansion
- [ ] **Expand Edit modal to edit all fields** - Allow users to edit title AND content (currently title-only)
- [ ] **Update editCallout() function** - Show modal with both title and content fields
- [ ] **Add form layout in modal** - Title field + Content textarea
- [ ] **Test multi-field edit** - Verify both fields save to database

### PRIORITY 3: Screenshot Upload/Management
- [ ] **Add file upload zone** - Drag-and-drop area for screenshot files (.png, .jpg, .jpeg)
- [ ] **Add file input UI** - "Choose file" button as fallback
- [ ] **Server-side file handling** - Endpoint to receive and store uploaded files
- [ ] **Auto-select latest** - System automatically uses latest uploaded screenshot for email
- [ ] **Show current screenshot** - Display thumbnail of active screenshot on dashboard
- [ ] **File size validation** - Limit to reasonable size (e.g., 5MB max)

### PRIORITY 4: Column Display Optimization
- [ ] **FY Column format** - Show only last 2 digits (27 instead of "FY 2027")
- [ ] **WM WK Column format** - Show only number (13 instead of "WK 13")
- [ ] **Update loadCallouts()** - Modify table rendering logic
- [ ] **Test display** - Verify compact format in table

### PRIORITY 5: Testing & Validation
- [ ] **Full CRUD workflow test** - Create, Read (display), Update, Delete
- [ ] **Email preview test** - Send test email and verify new format
- [ ] **Edge case testing** - Special characters, long content, etc.
- [ ] **Cross-browser testing** - Ensure UI works on Chrome, Edge, Firefox

### PRIORITY 6: Production Readiness
- [ ] **Switch to production email** - Update from kendall.rush@walmart.com to storeops_pricinginfo@email.wal-mart.com
- [ ] **Windows Task Scheduler setup** - Configure Friday 4 PM automated send
- [ ] **Documentation update** - Update README with new features
- [ ] **Final deployment** - Deploy to production

---

## Implementation Notes

### Files to Modify

1. **pricing_callouts_server.py**
   - Remove title from build_callout_email_html() email template
   - Add screenshot upload endpoint /api/upload-screenshot
   - Update query logic for screenshot retrieval

2. **dashboard.html**
   - Remove Title column from callouts table (line ~604-610)
   - Update FY column display logic (line ~843)
   - Update WM WK column display logic (line ~844)
   - Expand editCallout() modal to show title + content fields
   - Add file upload zone UI before email recipients section
   - Add JavaScript for drag-and-drop file handling

3. **New file: upload-area.html** (optional)
   - Screenshot upload component
   - Could be embedded directly in dashboard.html

### Database Considerations
- No schema changes needed for existing tables
- Screenshot files can be stored in:
  - Local filesystem (simpler, current approach)
  - Google Cloud Storage (scalable, requires auth)
  - BigQuery blob field (not ideal for images)

### Email Template Changes
**Current format:**
```
[Callout Title]
[Callout Content]
```

**New format:**
```
[Callout Content ONLY]
```

### UI/UX Improvements
- Column compression makes table cleaner
- All-field edit reduces context switching
- File upload gives users control over screenshots
- Content-only email is more concise

---

## Success Criteria

1. ✅ Email shows only callout content (no title)
2. ✅ Users can edit title, content, and other fields
3. ✅ Screenshot upload works (drag-drop or file picker)
4. ✅ FY shows as "27", WM WK shows as "13"
5. ✅ All CRUD operations working smoothly
6. ✅ Test email format verified
7. ✅ Task Scheduler running automated sends on Friday

---

## Estimated Timeline
- **Priority 1-2**: 1-2 hours
- **Priority 3**: 1-2 hours  
- **Priority 4**: 30 minutes
- **Priority 5-6**: 1 hour
- **Total**: ~4-6 hours

---

Last Updated: May 1, 2026
