# API POST Endpoint Fix - Cannot POST /api/survey-responses

## Problem
When clicking "Update Item", you get error: `Failed to save survey response: Cannot POST /api/survey-responses`

## Root Cause
The backend server was running **before** the survey response route was added, so Express doesn't know about the endpoint yet.

**Solution:** Restart the backend server.

---

## Steps to Fix

### 1. **Stop Backend Server**

Look for the terminal where backend is running (should show port 5000).

```powershell
# In the terminal showing backend:
Ctrl+C

# You should see it shut down
```

### 2. **Restart Backend Server**

```powershell
# Make sure you're in the server directory
cd server

# Start the server
npm start

# Wait for this message:
# "Walmart Refresh Guide API is running on port 5000"
```

### 3. **Verify API is Accessible**

Open browser and go to:
```
http://localhost:5000/health
```

You should see:
```json
{
  "status": "OK",
  "message": "Walmart Refresh Guide API is running",
  "timestamp": "2025-11-17T..."
}
```

If you see this ✓ then the backend is running correctly.

---

## Test the API Endpoint

### Using Postman (or any API tool):

**Request:**
```
POST http://localhost:5000/api/survey-responses
Content-Type: application/json
Authorization: Bearer <YOUR_JWT_TOKEN>

Body:
{
  "storeId": 1234,
  "itemId": "item-0",
  "status": "Completed",
  "owner": "Coach 2",
  "deadline": "2025-12-20",
  "notes": "Test comment",
  "version": "Refresh Guide 2026"
}
```

**Expected Response (201 Created):**
```json
{
  "message": "Survey response saved successfully",
  "data": {
    "id": "1702829400000",
    "storeId": 1234,
    "itemId": "item-0",
    "status": "Completed",
    "owner": "Coach 2",
    "version": "Refresh Guide 2026",
    ...
  }
}
```

---

## Test Via App UI

### 1. Login & Fill Form
- Login as Store Manager
- Click "Continue Survey"
- Make changes:
  - Owner: Coach 2
  - Status: Completed
  - Deadline: Pick a date
  - Notes: Add a comment

### 2. Click "Update Item"

**Expected Results:**
- ✅ Modal/alert says "Survey response saved successfully!"
- ✅ You're redirected to "View All Items" page
- ✅ No error message

### 3. Verify Data Saved

Check that data was saved to database:

```powershell
# Open file:
server/data/survey_responses.json

# Should contain new entry:
[
  {
    "id": "1702829400000",
    "storeId": 1234,
    "itemId": "item-0",
    "owner": "Coach 2",
    "status": "Completed",
    "deadline": "2025-12-20",
    "notes": "Add a comment",
    "version": "Refresh Guide 2026",
    "createdAt": "2025-11-17T...",
    "updatedAt": "2025-11-17T..."
  }
]
```

---

## API Endpoint Details

**File:** `server/src/routes/surveyResponses.js`

**POST /api/survey-responses**
- **Auth:** Requires JWT token
- **Body Fields:**
  - `storeId` (required)
  - `itemId` (required)
  - `status` (required: Pending, In Progress, Completed, On Hold)
  - `owner` (optional)
  - `deadline` (optional)
  - `notes` (optional)
  - `version` (optional, defaults to "Refresh Guide 2026")
  - `areaId`, `areaName`, `topicId`, `topicName` (optional)

**Response:** 201 Created with saved object

---

## Troubleshooting

### If you get "Cannot POST /api/survey-responses" error:

**Checklist:**
- [ ] Backend server running? (check for "API is running on port 5000")
- [ ] Did you restart server after stopping? (don't just close terminal)
- [ ] Is the route file at `server/src/routes/surveyResponses.js`?
- [ ] Does `server/src/index.js` have line: `app.use('/api/survey-responses', surveyResponseRoutes);`?
- [ ] Check browser console (F12) for exact error message

### If you get 401 Unauthorized:

**Problem:** JWT token missing or invalid

**Fix:**
1. Make sure you're logged in
2. Check that token is in localStorage
3. Refresh page and try again

### If you get 400 Bad Request:

**Problem:** Missing required fields

**Check:**
- Is `storeId` being sent? (user.storeNumber)
- Is `itemId` being sent? (should be from query params)
- Is `status` being sent? (required)

### If backend won't start:

```powershell
# Try clearing npm cache
npm cache clean --force

# Then try again
npm start
```

---

## Next Steps After API Works

1. ✅ Form shows "Survey response saved successfully!"
2. ✅ Data appears in survey_responses.json
3. ✅ Ready to build:
   - Admin dashboard to view all responses
   - Export functionality (CSV/Excel)
   - Role-based dashboards

---

**File Modified:** None (just need to restart backend)  
**Status:** Ready to test after server restart
