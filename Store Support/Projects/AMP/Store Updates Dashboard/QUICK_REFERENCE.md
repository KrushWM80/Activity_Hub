# AMP Dashboard - Quick Reference Card

**Version:** 1.0 | **Date:** February 11, 2026

---

## 🎨 Design System Quick Guide

### Colors (Copy-Paste)
```css
/* Primary Actions */
background: #3B82F6;      /* Walmart Blue - Buttons, links */
background: #FFCC00;      /* Yellow - Feedback CTA */

/* Professional */
background: #1E3A8A;      /* Navy - Headers */

/* Status */
color: #38A169;           /* Green - Success */
color: #E53E3E;           /* Red - Error */
color: #D69E2E;           /* Orange - Warning */
```

### Font Stack
```css
font-family: 'Everyday Sans', 'Segoe UI', Arial, sans-serif;
```

### Spacing Units
- 4px (space-1)
- 8px (space-2)
- 12px (space-3)
- 16px (space-4)
- 24px (space-6)

### Border Radius
- Buttons/Inputs: 4px-6px (--radius-md)
- Cards/Containers: 12px (--radius-lg)

---

## 💬 Feedback Loop Quick Start

### For Users
1. Click **"💬 Send Feedback"** (header, yellow button)
2. Select **category** (UI, Data, Performance, Filters, Other)
3. Choose **rating** (1-5 stars with emoji)
4. Write **comments** (what's working/broken/could improve)
5. Click **"Submit Feedback"** → See success ✅

### For Developers
**Connect to backend:**
```javascript
// In amp_analysis_dashboard.html, find this line:
const response = await fetch('/api/feedback', {

// Replace with your endpoint:
const response = await fetch('https://your-api.com/api/feedback', {
```

**Test with cURL:**
```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"category":"UI","rating":5,"comments":"Test","timestamp":"'$(date -Iseconds)'","url":"http://localhost","userAgent":"curl","dashboard":"AMP","dashboardVersion":"1.0"}'
```

### For Admins
**View feedback:**
1. Check database: `SELECT * FROM dashboard_feedback;`
2. Monitor: Which categories have low ratings?
3. Respond: Fix issues mentioned in multiple feedback
4. Report: Share improvements with team

---

## 📱 File Locations

| File | Purpose |
|------|---------|
| `amp_analysis_dashboard.html` | Main dashboard (design system + feedback) |
| `DASHBOARD_DESIGN_AND_FEEDBACK.md` | Design & feedback overview |
| `FEEDBACK_BACKEND_SETUP.md` | Backend integration (Python, Node, SQL examples) |
| `UPDATE_SUMMARY.md` | Complete update documentation |
| `AMP_ANALYSIS_DASHBOARD_README.md` | Original dashboard guide |

---

## ✅ Design System Checklist

- [x] Color palette implemented (Walmart official)
- [x] Typography standardized (Everyday Sans)
- [x] Spacing aligned to 4px grid
- [x] Components styled consistently
- [x] Accessibility (WCAG AA)
- [x] Responsive design (mobile/tablet/desktop)

---

## 🔧 Feedback Loop Checklist

- [x] Frontend widget built (multi-step form)
- [x] Category system (5 categories)
- [x] Rating system (1-5 emoji scale)
- [x] Comments capture
- [x] Offline storage (localStorage)
- [x] Success confirmation
- [x] Backend API ready
- [ ] Connect to `/api/feedback` (YOUR TASK)
- [ ] Set up database table (YOUR TASK)
- [ ] Create admin view (YOUR TASK)

---

## 🚀 Deploy in 3 Steps

1. **Copy files to your server**
   ```bash
   cp amp_analysis_dashboard.html /var/www/html/
   ```

2. **Create `/api/feedback` endpoint**
   ```
   See FEEDBACK_BACKEND_SETUP.md for examples
   (Python/FastAPI, Node/Express, PostgreSQL, MongoDB)
   ```

3. **Update API URL in HTML**
   ```javascript
   Change: fetch('/api/feedback', {
   To: fetch('https://your-api.com/api/feedback', {
   ```

---

## 🆘 Troubleshooting

**Feedback button not showing?**
- Check CSS loaded correctly (browser DevTools)
- Verify JavaScript not throwing errors (F12 console)

**Feedback form opens but doesn't submit?**
- Check API endpoint exists
- Verify CORS enabled on backend
- Check browser Network tab for request/response

**Users see success but data not in database?**
- Check endpoint receiving requests (check logs)
- Verify database connection
- Check request body format matches schema

**Need to change something?**

| Change | Where | How |
|--------|-------|-----|
| Colors | `amp_analysis_dashboard.html` | Search `:root {` |
| Categories | HTML | Edit Step 1 radio buttons |
| Feedback endpoint | Line ~1350 | Update `fetch('...')` URL |
| Auto-close delay | Line ~1400 | Change `setTimeout(..., 3000)` ms |
| Thank you message | HTML | Edit success div text |

---

## 📊 Sample Feedback Report

```
Week of Feb 11, 2026 - AMP Dashboard Feedback

Total: 12 submissions
Avg Rating: 4.2/5 ⭐

By Category:
  📋 Data Quality: 4 (avg 3.5★) - "Missing columns", "Wrong counts"
  🎨 Dashboard UI: 3 (avg 4.2★) - "Love the colors", "Layout confusing"
  ⚡ Performance: 3 (avg 4.0★) - "Takes 5 seconds to load"
  🔍 Filters: 2 (avg 4.5★) - "Works great", "Wish for more"

Action Items:
  1. Investigate data quality issues (3 mentions)
  2. Optimize dashboard loading (2 mentions)
  3. Add more filter options (1 request)
```

---

## 🎓 Learn More

- **Design System:** `Spark-Playground/General Setup/Design/`
- **Feedback Loop:** `Spark-Playground/General Setup/Feedback_Loop/`
- **Data Model:** `AMP data/AMP_DASHBOARD_DATA_MODEL.md`
- **Original Guide:** `AMP data/AMP_ANALYSIS_DASHBOARD_README.md`

---

## 📞 Quick Links

- **View Dashboard:** `Store Updates Dashboard/amp_analysis_dashboard.html`
- **Setup Backend:** `Store Updates Dashboard/FEEDBACK_BACKEND_SETUP.md`
- **Full Details:** `Store Updates Dashboard/UPDATE_SUMMARY.md`
- **Design Guide:** `Store Updates Dashboard/DASHBOARD_DESIGN_AND_FEEDBACK.md`

---

| Component | Status | Notes |
|-----------|--------|-------|
| Dashboard UI | ✅ Ready | Design system applied, responsive |
| Feedback Widget | ✅ Ready | Multi-step form, offline support |
| Database | ⏳ Pending | Create table (see FEEDBACK_BACKEND_SETUP.md) |
| Backend API | ⏳ Pending | Implement `/api/feedback` endpoint |
| Admin View | ⏳ Pending | Optional, see FEEDBACK_BACKEND_SETUP.md |
| Email Alerts | ⏳ Optional | Notify team of feedback, see examples |

---

**Everything is ready to go! Just need to connect the backend.** 🚀

Questions? Check the documentation files or ask in the feedback!

