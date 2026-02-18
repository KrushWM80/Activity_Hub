# Quick Start: Email Reporting

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd backend
pip install apscheduler reportlab email-validator
```

### Step 2: Configure Email (Optional)

Add to `.env` file (defaults work for Walmart network):
```bash
SMTP_SERVER=mailhub.wal-mart.com
SMTP_PORT=25
FROM_EMAIL=IntakeHub-Reports@walmart.com
```

### Step 3: Start Backend

```bash
python main.py
```

Look for: `✅ Email report scheduler initialized`

### Step 4: Open Reports Interface

Navigate to: **http://localhost:8001/reports.html**

### Step 5: Create Your First Report

1. Click **"➕ Create New Report"**

2. **Basic Info**:
   - Name: "My Weekly Status"
   - User ID: your_user_id
   - Email: your.email@walmart.com

3. **Content** (check these):
   - ✅ Overview
   - ✅ Counts
   - ✅ New

4. **Schedule**:
   - Frequency: **Weekly**
   - Day: **Friday**
   - Time: **09:00**
   - Format: **Email Body**

5. **Timeframe** (check this):
   - ✅ Current Week

6. Click **"Save Report Configuration"**

7. Click **"🧪 Test"** to send immediately!

## 📧 What You'll Get

A professional email containing:
- 📊 Overview statistics (total projects, facilities)
- 📈 Count breakdowns by Business Org and Store Area
- 🆕 New cards created this week
- 📋 Full project table with selected columns

## 🎛️ Common Configurations

### Daily Morning Digest
```
Frequency: Daily
Time: 08:00
Content: Overview, My Actions, Upcoming
Timeframe: Current Day
```

### Weekly Partner Report (Fridays)
```
Frequency: Weekly
Day: Friday
Time: 09:00
Content: Overview, Counts, New, Upcoming
Timeframe: Current Week
Filters: Partner = "Operations"
```

### Monthly Summary
```
Frequency: Monthly
Time: 09:00
Content: Overview, Counts, Activity Feed
Timeframe: Current Month
Format: Both (Email + PDF)
```

## ⚡ Quick Actions

### Test a Report Now
1. Find your report card
2. Click **"🧪 Test"**
3. Enter test email (optional)
4. Check inbox!

### Pause a Report
- Click **"⏸️ Pause"** on any active report
- No emails will be sent
- Resume anytime with **"▶️ Resume"**

### Edit Configuration
- Click **"✏️ Edit"**
- Update any settings
- Save changes
- Schedule automatically updates

## 📝 Tips & Tricks

### 1. Start Simple
- Begin with just "Overview" and "Counts"
- Add more content types after you're comfortable

### 2. Test First
- Always test before activating schedule
- Verify filters work correctly
- Check email formatting

### 3. Use Filters Wisely
- Filter by Partner to reduce noise
- Filter by Store Area for regional focus
- Leave empty to see everything

### 4. Column Selection
- Standard columns always included (Card #, Title, Facilities)
- Add only columns you actually need
- Fewer columns = easier to read

### 5. Multiple Reports
- Create separate reports for different purposes
- One for daily updates, one for weekly summary
- Different filters for different teams

## 🔧 Troubleshooting

### "Report not sending"
1. Check report is **Active** (green badge)
2. Verify you're on Walmart network
3. Check execution logs: View console output

### "Test fails"
1. Verify email address is correct
2. Check SMTP settings in `.env`
3. Try "Email Body" instead of PDF first

### "No data in report"
1. Check your filters - might be too restrictive
2. Verify timeframe selection
3. Ensure projects exist in database

## 🎯 Next Steps

1. **Explore Content Types**: Try "Upcoming" and "Activity Feed"
2. **Add Recipients**: Use CC emails for team distribution
3. **Try PDF Format**: Great for archiving and printing
4. **Multiple Timeframes**: Combine "Current Week" + "Last 7 Days"
5. **Advanced Filters**: Filter by Phase, Owner, Health status

## 📖 Full Documentation

See [EMAIL_REPORTING_GUIDE.md](EMAIL_REPORTING_GUIDE.md) for:
- Complete API documentation
- Architecture details
- Advanced configurations
- Troubleshooting guide

## ✅ Checklist

Before your first report:
- [ ] Dependencies installed
- [ ] Backend running
- [ ] Opened `/reports.html`
- [ ] Created first configuration
- [ ] Tested successfully
- [ ] Activated schedule

You're all set! 🎉

Your reports will automatically send on schedule. Check execution logs to verify delivery.
