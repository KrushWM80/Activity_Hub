# AMP Dashboard - Backend Implementation Guide for Feedback Loop

**Created:** February 11, 2026  
**Purpose:** Step-by-step guide to connect feedback widget to your backend  
**Estimated Time:** 30-45 minutes

---

## 📋 Quick Summary

The dashboard now has a production-ready feedback widget that collects:
- **Category** (UI, Data, Performance, Filters, Other)
- **Rating** (1-5 stars with emoji)
- **Comments** (freeform text explaining the issue/suggestion)
- **Metadata** (timestamp, URL, browser, dashboard version)

Currently feedback is stored in browser localStorage as a fallback. You need to connect it to your backend API.

---

## 🔗 Backend Endpoint Setup

### Endpoint Details
```
Method: POST
URL: /api/feedback
Content-Type: application/json
Authentication: Optional (add as needed)
```

### Expected Request Body
```json
{
  "category": "Performance",
  "rating": 3,
  "comments": "Dashboard takes 5 seconds to load with 196 projects",
  "timestamp": "2026-02-11T15:30:00.000Z",
  "url": "http://localhost:8081/amp_analysis_dashboard.html?filters=...",
  "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
  "dashboard": "AMP Analysis Dashboard",
  "dashboardVersion": "1.0"
}
```

### Expected Response
```json
{
  "status": "success",
  "feedback_id": "FB-1707585000",
  "message": "Thank you for your feedback!"
}
```

---

## 🐍 Python/FastAPI Example

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

app = FastAPI()

# Enable CORS for feedback submissions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Database would go here (MongoDB, PostgreSQL, etc.)
# For now, we'll use a simple list
feedback_storage = []

# Pydantic model for type validation
class FeedbackSubmission(BaseModel):
    category: str
    rating: int
    comments: str
    timestamp: str
    url: str
    userAgent: str
    dashboard: str
    dashboardVersion: str
    email: Optional[str] = None  # Optional for authenticated users

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackSubmission):
    """
    Receive and store user feedback from the AMP Analysis Dashboard
    """
    try:
        # Generate unique feedback ID
        feedback_id = f"FB-{int(datetime.now().timestamp())}"
        
        # Create feedback record with additional metadata
        feedback_record = {
            "feedback_id": feedback_id,
            "category": feedback.category,
            "rating": feedback.rating,
            "comments": feedback.comments,
            "timestamp": feedback.timestamp,
            "url": feedback.url,
            "userAgent": feedback.userAgent,
            "dashboard": feedback.dashboard,
            "dashboardVersion": feedback.dashboardVersion,
            "status": "received",
            "server_received_at": datetime.now().isoformat(),
            "review_status": "pending"  # pending → reviewed → actioned → closed
        }
        
        # Store in database
        feedback_storage.append(feedback_record)  # Replace with: db.feedback.insert_one(feedback_record)
        
        # Optional: Send email notification
        # send_admin_notification(feedback_record)
        
        # Optional: Log for monitoring
        print(f"✅ Feedback received: {feedback_id} - {feedback.category} ({feedback.rating}★)")
        
        return {
            "status": "success",
            "feedback_id": feedback_id,
            "message": "Thank you for your feedback! We'll review it shortly."
        }
        
    except Exception as e:
        # Log error but still return success to user (graceful degradation)
        print(f"❌ Error storing feedback: {str(e)}")
        return {
            "status": "success",
            "feedback_id": f"FB-{uuid.uuid4().hex[:8]}",
            "message": "Thank you for your feedback!"
        }

# Optional: Endpoint to view feedback (admin only)
@app.get("/api/feedback/admin")
async def get_feedback(limit: int = 50, category: Optional[str] = None):
    """
    Admin endpoint to view recent feedback
    In production, add authentication/authorization
    """
    feedback = feedback_storage
    
    if category:
        feedback = [f for f in feedback if f['category'] == category]
    
    return {
        "total": len(feedback),
        "recent": sorted(feedback, key=lambda x: x['timestamp'], reverse=True)[:limit]
    }

# Optional: Email notification function
async def send_admin_notification(feedback_record):
    """Send email to admins when feedback received"""
    # Configure with your email service (SendGrid, SMTP, etc.)
    # subject = f"New Dashboard Feedback: {feedback_record['category']} ({feedback_record['rating']}★)"
    # body = f"""
    # Category: {feedback_record['category']}
    # Rating: {feedback_record['rating']}/5
    # Comments: {feedback_record['comments']}
    # Dashboard: {feedback_record['dashboard']}
    # Timestamp: {feedback_record['timestamp']}
    # """
    # send_email(to="team@example.com", subject=subject, body=body)
    pass
```

---

## 🟩 Node.js/Express Example

```javascript
// routes/feedback.js
const express = require('express');
const router = express.Router();

// In-memory storage for demo (use MongoDB/PostgreSQL in production)
let feedbackStorage = [];

router.post('/api/feedback', async (req, res) => {
    try {
        const {
            category,
            rating,
            comments,
            timestamp,
            url,
            userAgent,
            dashboard,
            dashboardVersion
        } = req.body;

        // Validate required fields
        if (!category || !rating || !comments) {
            return res.status(400).json({
                status: 'error',
                message: 'Missing required fields'
            });
        }

        // Generate feedback ID
        const feedbackId = `FB-${Date.now()}`;

        // Create record
        const feedbackRecord = {
            feedbackId,
            category,
            rating,
            comments,
            timestamp,
            url,
            userAgent,
            dashboard,
            dashboardVersion,
            status: 'received',
            serverReceivedAt: new Date().toISOString(),
            reviewStatus: 'pending'
        };

        // Store in database
        feedbackStorage.push(feedbackRecord);
        // db.collection('feedback').insertOne(feedbackRecord);

        // Optional: Send email
        // await sendEmailNotification(feedbackRecord);

        console.log(`✅ Feedback received: ${feedbackId}`);

        return res.json({
            status: 'success',
            feedbackId,
            message: 'Thank you for your feedback!'
        });

    } catch (error) {
        console.error('❌ Feedback error:', error);
        
        // Still return success to user (graceful degradation)
        return res.json({
            status: 'success',
            feedbackId: `FB-${Date.now()}`,
            message: 'Thank you for your feedback!'
        });
    }
});

// Admin: Get feedback
router.get('/api/feedback/admin', (req, res) => {
    // Add authentication here
    const limit = req.query.limit || 50;
    const category = req.query.category;

    let feedback = feedbackStorage;

    if (category) {
        feedback = feedback.filter(f => f.category === category);
    }

    return res.json({
        total: feedbackStorage.length,
        recent: feedback.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, limit)
    });
});

module.exports = router;

// In main server.js:
// const feedbackRoutes = require('./routes/feedback');
// app.use(feedbackRoutes);
```

---

## 🐘 PostgreSQL Database Schema

```sql
-- Create feedback table
CREATE TABLE dashboard_feedback (
    id SERIAL PRIMARY KEY,
    feedback_id VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    timestamp TIMESTAMP,
    url TEXT,
    user_agent TEXT,
    dashboard VARCHAR(100),
    dashboard_version VARCHAR(20),
    status VARCHAR(20) DEFAULT 'received',
    review_status VARCHAR(20) DEFAULT 'pending',
    server_received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster queries
CREATE INDEX idx_category ON dashboard_feedback(category);
CREATE INDEX idx_rating ON dashboard_feedback(rating);
CREATE INDEX idx_timestamp ON dashboard_feedback(timestamp);
CREATE INDEX idx_review_status ON dashboard_feedback(review_status);
```

---

## 🍃 MongoDB Collections

```javascript
// Insert feedback
db.dashboard_feedback.insertOne({
    feedback_id: "FB-1707585000",
    category: "Performance",
    rating: 3,
    comments: "Dashboard takes 5 seconds to load...",
    timestamp: ISODate("2026-02-11T15:30:00Z"),
    url: "http://localhost:8081/amp_analysis_dashboard.html",
    userAgent: "Mozilla/5.0...",
    dashboard: "AMP Analysis Dashboard",
    dashboardVersion: "1.0",
    status: "received",
    reviewStatus: "pending",
    serverReceivedAt: ISODate(),
    adminNotes: "",
    createdAt: ISODate(),
    updatedAt: ISODate()
});

// Create indexes for performance
db.dashboard_feedback.createIndex({ category: 1 });
db.dashboard_feedback.createIndex({ rating: 1 });
db.dashboard_feedback.createIndex({ timestamp: -1 });
db.dashboard_feedback.createIndex({ reviewStatus: 1 });

// Query examples
db.dashboard_feedback.find({ category: "Performance" });
db.dashboard_feedback.find({ rating: { $lt: 3 } });
db.dashboard_feedback.find({ reviewStatus: "pending" });
```

---

## 🔄 Update Dashboard API Endpoint

Edit `amp_analysis_dashboard.html` and change the API URL:

### Find this line (around line 1350):
```javascript
const response = await fetch('/api/feedback', {
```

### Replace with your endpoint:
```javascript
// Local development
const response = await fetch('http://localhost:8000/api/feedback', {

// Or production
const response = await fetch('https://api.example.com/api/feedback', {
```

---

## 🧪 Test the Integration

### Manual Test
1. Open `amp_analysis_dashboard.html` in browser
2. Click "💬 Send Feedback" button
3. Select category: "Performance"
4. Select rating: 3 stars
5. Type comment: "Test feedback"
6. Click "Submit Feedback"
7. Should see success message (✅)
8. Check your backend database for the record

### Backend Test (cURL)
```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Performance",
    "rating": 3,
    "comments": "Test feedback",
    "timestamp": "2026-02-11T15:30:00Z",
    "url": "http://localhost:8080/dashboard.html",
    "userAgent": "curl",
    "dashboard": "AMP Analysis Dashboard",
    "dashboardVersion": "1.0"
  }'
```

Expected response:
```json
{
  "status": "success",
  "feedback_id": "FB-1707585000",
  "message": "Thank you for your feedback!"
}
```

---

## 📊 Admin Dashboard for Feedback Review

```html
<!-- feedback-admin.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Feedback Admin Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #3B82F6; color: white; }
        .rating-1 { color: #E53E3E; font-weight: bold; }
        .rating-5 { color: #38A169; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Dashboard Feedback Review</h1>
    
    <div id="stats">
        <!-- Populated by JavaScript -->
    </div>

    <table id="feedbackTable">
        <thead>
            <tr>
                <th>ID</th>
                <th>Category</th>
                <th>Rating</th>
                <th>Comments</th>
                <th>Date</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody id="feedbackBody">
            <!-- Populated by fetch -->
        </tbody>
    </table>

    <script>
        async function loadFeedback() {
            const response = await fetch('/api/feedback/admin');
            const data = await response.json();
            
            // Populate table
            const tbody = document.getElementById('feedbackBody');
            data.recent.forEach(fb => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${fb.feedback_id}</td>
                    <td>${fb.category}</td>
                    <td class="rating-${fb.rating}">${'⭐'.repeat(fb.rating)}</td>
                    <td>${fb.comments.substring(0, 100)}...</td>
                    <td>${new Date(fb.timestamp).toLocaleDateString()}</td>
                    <td>${fb.review_status}</td>
                `;
            });
            
            // Show stats
            document.getElementById('stats').innerHTML = `
                <p><strong>Total Feedback:</strong> ${data.total}</p>
                <p><strong>Recent Records:</strong> ${data.recent.length}</p>
            `;
        }
        
        loadFeedback();
    </script>
</body>
</html>
```

---

## ✅ Checklist

- [ ] Create `/api/feedback` endpoint in backend
- [ ] Update database schema with `dashboard_feedback` table
- [ ] Update API URL in `amp_analysis_dashboard.html`
- [ ] Test feedback submission
- [ ] Verify data appears in database
- [ ] Set up admin dashboard to view feedback
- [ ] Configure email notifications (optional)
- [ ] Deploy to production

---

## 📞 Support

If feedback widget isn't working:

1. Check browser console for errors (F12 → Console)
2. Verify API endpoint is accessible
3. Check CORS headers (if cross-origin)
4. Verify `/api/feedback` accepts POST requests
5. Test with cURL command above

**Feedback fallback:** If backend unavailable, feedback is stored in browser localStorage and can be retrieved later.

---

**Ready to deploy!** Once backend is set up, the dashboard will automatically send feedback to your API.

