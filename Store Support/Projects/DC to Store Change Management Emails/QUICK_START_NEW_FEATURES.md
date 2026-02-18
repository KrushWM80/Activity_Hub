# Quick Start Guide - New Features

**Last Updated:** February 16, 2026

---

## 🚀 What's New?

Your Manager Change Management Email system now includes:

1. ✨ **Spark Branded Email** with refreshed colors and logo
2. 💬 **Feedback Loop** for capturing user feedback
3. 📊 **Admin Dashboard** to review feedback and activity
4. 👥 **Store Manager Directory** for DCs to find contacts

---

## 🎯 Quick Setup (5 Minutes)

### Step 1: Install Flask
```bash
pip install flask
```

### Step 2: Start the Admin Server
```bash
python admin_app.py
```

You should see:
```
Running on http://localhost:5000
```

### Step 3: Access the Dashboards

**Admin Dashboard:**
```
http://localhost:5000/admin
```

**Store Manager Directory:**
```
http://localhost:5000/store-manager-directory
```

---

## 📧 Using the Email Features

### For Email Recipients

#### Sending Feedback
1. Open the Email
2. Click the **"Send Feedback"** button
3. Type your feedback in the email window
4. Send to: `feedback@walmart.com`

#### Finding Store Managers
1. Open the Email
2. Click the **"View Store Managers"** button
3. Email address is auto-detected
4. See all managers for your DC

### For Admins

#### Reviewing Feedback
1. Go to `http://localhost:5000/admin`
2. See feedback metrics in dashboard
3. Click "View Details" on any feedback
4. Update status and add notes
5. Activity automatically logged

#### Checking Activity
1. Click "Activity Log" in navigation
2. See all system activities
3. Filter by event type if needed
4. Timestamps and details for each action

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `MOCK_EMAIL_TEMPLATE.html` | Email template (updated with logo & colors) |
| `feedback_handler.py` | Feedback collection & storage |
| `admin_app.py` | Flask web app for dashboards |
| `dc_to_stores_config.py` | Store manager data management |
| `templates/*.html` | Dashboard HTML pages |

---

## 🔧 Configuration

### Database Location
```
./feedback.db
```

Auto-created on first run. Contains:
- Feedback submissions
- Activity log
- Status changes

### Manager Data Location
```
./config/dc_store_managers.json
```

Auto-created. Contains:
- All DCs
- Managers per DC
- Contact information

### Update Manager Directory
```python
# In your daily process script:
from dc_to_stores_config import DCStoreManagerConfig

config = DCStoreManagerConfig()
config.update_from_snapshot(snapshot_data)
```

---

## 🎨 Email Customization

**Logo Path:**
```
C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Design\Spark Blank.png
```

**Colors Used:**
- Navy: `#1E3A8A`
- Primary Blue: `#3B82F6`
- Dark Blue: `#1D4ED8`
- Light Blue: `#DBEAFE`

**Edit Buttons:**
Look for `action-buttons` div in `MOCK_EMAIL_TEMPLATE.html`

---

## 📊 Dashboard Features

### Admin Dashboard
- **Metrics:** Total feedback, pending items, average rating
- **Charts:** Status and category distribution
- **Feed:** Recent feedback with quick review
- **Log:** Activity timeline with timestamps

### Store Manager Directory
- **Auto-Detection:** Extracts DC from email (6020GM → DC 6020)
- **Cards:** Manager info with email/phone links
- **Search:** Find any manager in system
- **Statistics:** Total managers by category

---

## 🔗 Integration Points

### Email Generation
```python
# Add to your email sending code:
from feedback_handler import FeedbackHandler

# Creates feedback links in email
feedback_button_url = "https://localhost:5000/admin/feedback/submit"
manager_search_url = "https://localhost:5000/store-manager-directory"
```

### Daily Updates
```python
# In your daily snapshot process:
from dc_to_stores_config import DCStoreManagerConfig

config = DCStoreManagerConfig()
config.update_from_snapshot(your_snapshot_data)
```

---

## 📝 API Endpoints

### Feedback Submission (JSON)
```bash
POST /api/submit-feedback

{
    "user_email": "6020GM@email.wal-mart.com",
    "category": "Dashboard UI",
    "rating": 4,
    "message": "Great system, needs market filter",
    "via": "email"
}
```

### Get Store Managers
```bash
GET /api/store-managers/<dc_number>

Response:
{
    "dc": "6020",
    "managers": [...],
    "total": 15
}
```

### Get All DCs
```bash
GET /api/all-dcs

Response:
{
    "dcs": ["6020", "6080", ...],
    "total": 45
}
```

---

## 🐛 Troubleshooting

### Admin Dashboard Not Loading
```
✓ Check: Python Flask installed (pip install flask)
✓ Check: Server is running (python admin_app.py)
✓ Try: http://localhost:5000/admin
```

### Manager Directory Returns Empty
```
✓ Manager data needs to be populated
✓ Run: config.update_from_snapshot(snapshot_data)
✓ Or: config.add_manager("6020", {...})
```

### Feedback Not Showing
```
✓ Check database exists: ./feedback.db
✓ Verify email sent to: feedback@walmart.com
✓ Check admin dashboard refresh
```

### Email Logo Not Displaying
```
✓ Verify image path: C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Design\Spark Blank.png
✓ Use full file path in HTML: <img src="C:\..." alt="Logo">
✓ For web: Convert to base64 or CDN URL
```

---

## 📈 Next Steps

1. **Populate Manager Data**
   ```python
   config = DCStoreManagerConfig()
   config.update_from_snapshot(snapshot_data)
   ```

2. **Deploy Admin App**
   - Set up production Flask hosting (Gunicorn, Docker, etc.)
   - Configure HTTPS
   - Add authentication

3. **Configure Email Forwarding**
   - Set up feedback@walmart.com to route to your server
   - Enable email parsing and FeedbackHandler integration

4. **Monitor & Improve**
   - Check admin dashboard weekly
   - Review feedback stats
   - Adjust based on user suggestions

---

## 💡 Tips

- **Auto-fill DC:** Email format 6020GM@... auto-detects as DC 6020
- **Bulk Update:** Use `update_from_snapshot()` for daily manager updates
- **Export Data:** Call `export_feedback_json()` to backup feedback
- **Search Managers:** Use `search_managers("keyword")` for quick lookups

---

## 📞 Questions?

Contact: **ATCTEAMSUPPORT@walmart.com**

---

**Version:** 1.0  
**Last Updated:** February 16, 2026  
**Status:** ✅ Ready to Use
