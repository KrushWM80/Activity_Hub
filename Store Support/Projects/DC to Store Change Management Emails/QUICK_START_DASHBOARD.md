# QUICK START: Your Dashboard is Running! 🚀

## Status: ✅ Everything Working

- **Dashboard**: Running on http://localhost:5000
- **Test Data**: Loaded and visible
- **Database**: Created and populated
- **Charts**: Rendering in real-time

## What You're Seeing

The dashboard currently shows **30 days of simulated email history**:
- 29 emails sent to 5 different DC territories
- Manager changes across Ambient and Perishable DCs
- Daily trend charts with realistic data
- Role type breakdown (Store, Market, Region managers)

## What's Next

### Option A: Test Dashboard Now (Recommended)
1. ✅ Dashboard is running at http://localhost:5000
2. Open it in your browser
3. Play with the time filters (30/60/90 days)
4. Explore the charts and metrics
5. No additional setup needed

### Option B: Integrate Real Emails (Later)
When ready, add 3 lines to `daily_check_smart.py`:
```python
from email_history_logger import log_email_send

# After sending email:
log_email_send(dc_number, dc_type, recipients, subject, changes, test_mode=False)
```
See [docs/INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for details.

## Commands Reference

**Stop Dashboard**
- Press `Ctrl+C` in the terminal where it's running
- Or close the terminal

**Restart Dashboard**
```bash
cd "c:\Users\krush\Documents\VSCode\Store Support\Projects\DC to Store Change Management Emails"
python dashboard_builtin.py
```

**Regenerate Test Data**
```bash
python tests/generate_test_data.py
```

**Clear Database & Start Fresh**
```bash
python tests/generate_test_data.py --clear
python tests/generate_test_data.py
```

**Add Today's Data**
```bash
python tests/generate_test_data.py --daily-report
```

## Folder Structure

```
📁 Project Root
├── 📄 dashboard_builtin.py       ← Main dashboard server
├── 📄 email_history_logger.py    ← Logging system
├── 📄 email_history.db           ← Database (auto-created)
│
├── 📁 docs/
│   ├── INTEGRATION_GUIDE.md      ← How to integrate with real emails
│   └── (other documentation)
│
├── 📁 tests/
│   └── generate_test_data.py     ← Test data generator
│
├── 📁 data/
│   └── (data files & snapshots)
│
└── 📁 static/
    └── (CSS, JS if needed)
```

## Dashboard Features

**KPI Cards** (Top)
- Total Changes Detected
- Emails Sent
- Distribution Centers Involved

**Charts**
- Changes by Role Type (pie chart)
- Top 10 DC Territories (bar chart)
- Daily Trend (line chart over time)

**Data Table**
- All DCs with change counts
- Type (Ambient/Perishable)
- Email count per DC

**Auto-Refresh**
- Updates every 5 minutes
- See current time in footer

## Troubleshooting

**Dashboard won't start?**
- Check port 5000 isn't in use: `netstat -an | find ":5000"`
- Try different port: Edit `PORT = 5001` in dashboard_builtin.py

**Database errors?**
- Delete `email_history.db` and regenerate: `python tests/generate_test_data.py --clear`

**No charts showing?**
- Refresh browser (F5)
- Wait 10 seconds for data to load
- Check browser console for errors (F12)

## Architecture

```
User Browser (http://localhost:5000)
        ↓
    dashboard_builtin.py (HTTP Server)
        ↓
    email_history_logger.py (Data Layer)
        ↓
    email_history.db (SQLite)
```

No external dependencies. Works with standard Python 3.14.

## Next Steps

1. **Test the dashboard** - You're good to go!
2. **Review test data** - See what metrics look like
3. **Plan integration** - When ready, add logging to daily_check_smart.py
4. **Enable real emails** - Start tracking actual manager changes

---

**Questions?** See docs/INTEGRATION_GUIDE.md or DASHBOARD_FEATURE_GUIDE.md
