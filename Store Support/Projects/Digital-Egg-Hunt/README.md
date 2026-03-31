# 🥚 Digital Egg Hunt 2026 - Setup & Launch Guide

## Overview
The Digital Egg Hunt is an interactive Easter egg hunt where participants scan QR codes printed on colorful eggs. The first person to find all 50 eggs (or the person with the most eggs by 9:30 AM on April 3rd, 2026) wins a prize!

**System Components:**
- **Backend**: FastAPI service (port 8003)
- **Frontend**: Web-based scanning and leaderboard interface
- **Data**: JSON-based tracking system
- **QR Codes**: Printable colorful Easter eggs with embedded QR codes

---

## Phase 1: Installation & Setup

### 1.1 Install Dependencies

```powershell
# Navigate to Activity Hub directory
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install fastapi uvicorn qrcode[pil] reportlab python-multipart
```

### 1.2 Verify Installation

```powershell
# Test that packages are installed
python -c "import fastapi, qrcode, reportlab; print('✅ All packages installed')"
```

---

## Phase 2: Generate Egg PDFs

### 2.1 Generate Test Eggs (for 4/2 testing)

```powershell
# From the Digital-Egg-Hunt directory
python generate_eggs.py
```

This creates:
- **Test PDF**: 10 colored eggs labeled T1-T10 with "TEST EGG" watermark
- **Production PDF**: 50 colored eggs labeled EGG-001 to EGG-050

**Output Files:**
```
Digital_Egg_Hunt_Test.pdf          # Print on 4/2 for testing
Digital_Egg_Hunt_Production.pdf    # Print on 4/3 for real event
```

### 2.2 Print the PDFs

- Print on cardstock (recommended) or regular paper
- Cut out the egg circles
- Optionally laminate for durability
- Use for testing on 4/2 and event on 4/3

---

## Phase 3: Start the Backend Service

### 3.1 Launch FastAPI Server

Open a PowerShell terminal:

```powershell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Digital-Egg-Hunt"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start the backend service
python backend/main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
```

✅ **Backend is now running on http://localhost:8003**

> **Keep this terminal open!** The backend must continue running throughout the event.

---

## Phase 4: Access the Frontend

### 4.1 Open in Web Browser

The frontend is a standalone HTML file. Open it in your default browser:

**Option A: Direct File Access**
```powershell
# Open the HTML file directly
start "Store Support\Projects\Digital-Egg-Hunt\frontend\index.html"
```

**Option B: Browser URL**
- Copy the full path: `c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Digital-Egg-Hunt\frontend\index.html`
- Open your browser and enter: `file:///c:/Users/krush/OneDrive%20-%20Walmart%20Inc/Documents/VSCode/Activity_Hub/Store%20Support/Projects/Digital-Egg-Hunt/frontend/index.html`

**Option C: Start Local Web Server (Recommended)**
```powershell
# Run from the frontend directory
cd "Store Support\Projects\Digital-Egg-Hunt\frontend"
python -m http.server 8080
# Then visit: http://localhost:8080/index.html
```

---

## Phase 5: Testing on 4/2

### 5.1 Test Workflow

1. **Print Test Eggs**
   - Print the `Digital_Egg_Hunt_Test.pdf`
   - Cut out T1-T10 eggs

2. **Hide Test Eggs**
   - Place T1-T10 in accessible locations for testing

3. **Test Scanning**
   ```
   User enters name → Scans T1 → Sees "T1 found"
   Continue with T2-T10
   ```

4. **Verify Leaderboard**
   - Check that users appear in real-time
   - Verify progress bar updates correctly
   - Confirm countdown timer works

5. **Test Winner Detection**
   - Have someone scan all 10 test eggs
   - Verify "Winner" announcement appears
   - Check Kendall's email inbox

### 5.2 Email Configuration (for testing winner notification)

```powershell
# Set these environment variables before starting backend
$env:OUTLOOK_EMAIL = "your_email@walmart.com"
$env:OUTLOOK_PASSWORD = "your_password"

# Then start backend
python backend/main.py
```

---

## Phase 6: Launch Live Event on 4/3

### 6.1 Event Timeline

| Time | Task |
|------|------|
| **9:00 AM** | Print production PDFs (EGG-001-050) |
| **9:10 AM** | Hide all 50 eggs in building |
| **9:15 AM** | Verify backend is running |
| **9:20 AM** | Open frontend interface |
| **9:30 AM** | HUNT BEGINS ← Countdown reaches 0:00:00 |
| **9:30 AM+** | Participants start scanning, leaderboard updates live |
| **Whenever** | If someone finds all 50 → Winner email sent to Kendall, banner displays |
| **END TIME** | When you decide event is over (or someone finds all 50) |

### 6.2 Pre-Launch Checklist

- [ ] Backend running (`python backend/main.py`)
- [ ] Frontend accessible in browser
- [ ] Production eggs (50) printed and cut
- [ ] Eggs hidden throughout building
- [ ] WiFi coverage verified in all locations where eggs are hidden
- [ ] Outlook credentials set (for winner email)
- [ ] Kendall's email address confirmed: kendall.rush@walmart.com
- [ ] Test with a participant before official launch

### 6.3 During the Event

**Monitor These:**
1. **Leaderboard** - Updates every 5 seconds automatically
2. **Countdown Timer** - Running down to 9:30 AM deadline
3. **Backend Console** - Watch for errors (keep terminal visible)
4. **Winner Announcement** - When someone finds all 50 eggs (or at 9:30 AM if no one found all)

---

## Admin Tasks

### Reset Game Data (for testing)
```powershell
curl -X POST "http://localhost:8003/reset-data?admin_key=admin123"
```

### Check API Status
```powershell
curl "http://localhost:8003/status"
```

### View Game Data File
```powershell
# Edit the JSON file directly if needed
notepad "data\egg_hunt_data.json"
```

### Adjust Cutoff Time
Edit `backend/main.py` and change:
```python
CUTOFF_TIME = datetime(2026, 4, 3, 9, 30, 0, tzinfo=timezone.utc)  # Change this line
```

Then restart the backend.

---

## API Endpoints Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register` | Register new participant |
| POST | `/scan` | Record egg scan |
| GET | `/leaderboard` | Get current leaderboard |
| GET | `/status` | Get game status and countdown |
| POST | `/reset-data` | Reset all data (admin) |

### Example API Call (PowerShell)
```powershell
# Register a user
$body = @{
    first_name = "John"
    last_name = "Doe"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8003/register" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

---

## Troubleshooting

### Backend won't start
- [ ] Verify FastAPI is installed: `pip install fastapi uvicorn`
- [ ] Check port 8003 is not in use: `netstat -ano | findstr :8003`
- [ ] Verify correct directory

### Frontend won't connect to backend
- [ ] Ensure backend is running on port 8003
- [ ] Check browser console for CORS errors
- [ ] Verify you're accessing frontend over HTTP (not HTTPS)

### QR codes don't scan
- [ ] Check print quality (dark enough)
- [ ] Try scanning with multiple devices (some phones read better)
- [ ] Ensure good lighting when scanning

### No winner email
- [ ] Check Outlook credentials are set correctly
- [ ] Verify Kendall's email address
- [ ] Check email spam folder
- [ ] Verify backend console for email errors

### Leaderboard doesn't update
- [ ] Check browser console (F12) for errors
- [ ] Refresh the page
- [ ] Ensure backend is responding: `curl http://localhost:8003/status`

---

## File Structure

```
Digital-Egg-Hunt/
├── backend/
│   └── main.py              # FastAPI service
├── frontend/
│   └── index.html           # Web interface
├── data/
│   └── egg_hunt_data.json   # Game data file
├── generate_eggs.py         # QR code generator
├── send_winner_email.py     # Email notifier
└── README.md                # This file
```

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the backend console for error messages
3. Check browser console (F12) for frontend errors
4. Contact Activity Team for support

---

## Event Summary

📅 **Date:** April 3, 2026
🕖 **Start Time:** 9:30 AM (Cutoff time)
🥚 **Total Eggs:** 50
🏆 **Prize:** Awarded to first to find all 50 or most by 9:30 AM
📧 **Winner Notification:** Kendall.rush@walmart.com

Good luck with the Digital Egg Hunt! 🥚🎉
