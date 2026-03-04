"""
Feedback Handler - Collects, stores, and manages user feedback
Part of the Manager Change Tracking System feedback loop
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class FeedbackHandler:
    """Manages feedback collection, storage, and notification"""
    
    def __init__(self, db_path="feedback.db", email_config=None):
        """Initialize feedback handler with database and email config"""
        self.db_path = db_path
        self.email_config = email_config
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for feedback storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_email TEXT NOT NULL,
                user_dc TEXT,
                feedback_category TEXT,
                rating INTEGER,
                message TEXT,
                status TEXT DEFAULT 'new',
                admin_notes TEXT,
                submitted_via TEXT DEFAULT 'email'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback_activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                feedback_id INTEGER,
                admin_user TEXT,
                action TEXT,
                details TEXT,
                FOREIGN KEY (feedback_id) REFERENCES feedback_submissions(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def parse_user_email(self, email_address):
        """Extract DC number from email address"""
        # Pattern: 6020GM@email.wal-mart.com -> DC 6020
        try:
            prefix = email_address.split('@')[0]
            # Extract numbers from prefix
            dc_number = ''.join(c for c in prefix if c.isdigit())
            return dc_number if dc_number else None
        except:
            return None
    
    def submit_feedback(self, user_email, feedback_category, rating, message, submitted_via="email"):
        """
        Submit feedback to the system
        
        Args:
            user_email: User's email address
            feedback_category: Category of feedback (e.g., 'UI', 'Data Quality', 'Performance')
            rating: Rating from 1-5
            message: Feedback message
            submitted_via: Channel used to submit (default: 'email')
        
        Returns:
            dict: Feedback record with ID
        """
        user_dc = self.parse_user_email(user_email)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO feedback_submissions 
            (user_email, user_dc, feedback_category, rating, message, submitted_via)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_email, user_dc, feedback_category, rating, message, submitted_via))
        
        feedback_id = cursor.lastrowid
        
        # Log activity
        cursor.execute("""
            INSERT INTO feedback_activity_log 
            (event_type, feedback_id, action, details)
            VALUES (?, ?, ?, ?)
        """, ("FEEDBACK_SUBMITTED", feedback_id, "New feedback received", 
              f"Category: {feedback_category}, Rating: {rating}"))
        
        conn.commit()
        conn.close()
        
        # Send notification to admin
        self._notify_admin_new_feedback(feedback_id, user_email, feedback_category, rating)
        
        return {
            "id": feedback_id,
            "status": "success",
            "message": "Thank you for your feedback!"
        }
    
    def get_feedback(self, feedback_id):
        """Retrieve specific feedback submission"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, user_email, user_dc, feedback_category, 
                   rating, message, status, admin_notes
            FROM feedback_submissions
            WHERE id = ?
        """, (feedback_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "timestamp": result[1],
                "user_email": result[2],
                "user_dc": result[3],
                "category": result[4],
                "rating": result[5],
                "message": result[6],
                "status": result[7],
                "admin_notes": result[8]
            }
        return None
    
    def get_all_feedback(self, status_filter=None, dc_filter=None, limit=100):
        """
        Retrieve all feedback submissions with optional filtering
        
        Args:
            status_filter: Filter by status (new, reviewed, resolved, archived)
            dc_filter: Filter by DC number
            limit: Maximum records to return
        
        Returns:
            list: Feedback submissions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT id, timestamp, user_email, user_dc, feedback_category, 
                   rating, message, status, admin_notes
            FROM feedback_submissions
            WHERE 1=1
        """
        params = []
        
        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)
        
        if dc_filter:
            query += " AND user_dc = ?"
            params.append(dc_filter)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        feedback_list = []
        for row in results:
            feedback_list.append({
                "id": row[0],
                "timestamp": row[1],
                "user_email": row[2],
                "user_dc": row[3],
                "category": row[4],
                "rating": row[5],
                "message": row[6],
                "status": row[7],
                "admin_notes": row[8]
            })
        
        return feedback_list
    
    def update_feedback_status(self, feedback_id, new_status, admin_user, admin_notes=""):
        """Update feedback submission status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE feedback_submissions
            SET status = ?, admin_notes = ?
            WHERE id = ?
        """, (new_status, admin_notes, feedback_id))
        
        # Log activity
        cursor.execute("""
            INSERT INTO feedback_activity_log 
            (event_type, feedback_id, admin_user, action, details)
            VALUES (?, ?, ?, ?, ?)
        """, ("FEEDBACK_STATUS_CHANGED", feedback_id, admin_user, 
              f"Status changed to {new_status}", admin_notes))
        
        conn.commit()
        conn.close()
    
    def get_activity_log(self, feedback_id=None, limit=500):
        """Retrieve activity log with submitter information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if feedback_id:
            cursor.execute("""
                SELECT fal.id, fal.timestamp, fal.event_type, fal.feedback_id, 
                       fal.admin_user, fal.action, fal.details,
                       fs.user_email, fs.feedback_category, fs.status
                FROM feedback_activity_log fal
                LEFT JOIN feedback_submissions fs ON fal.feedback_id = fs.id
                WHERE fal.feedback_id = ?
                ORDER BY fal.timestamp DESC
                LIMIT ?
            """, (feedback_id, limit))
        else:
            cursor.execute("""
                SELECT fal.id, fal.timestamp, fal.event_type, fal.feedback_id, 
                       fal.admin_user, fal.action, fal.details,
                       fs.user_email, fs.feedback_category, fs.status
                FROM feedback_activity_log fal
                LEFT JOIN feedback_submissions fs ON fal.feedback_id = fs.id
                ORDER BY fal.timestamp DESC
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        activity = []
        for row in results:
            activity.append({
                "id": row[0],
                "timestamp": row[1],
                "event_type": row[2],
                "feedback_id": row[3],
                "admin_user": row[4],
                "action": row[5],
                "details": row[6],
                "submitted_by": row[7],  # User who submitted the feedback
                "feedback_category": row[8],  # Category of the feedback
                "feedback_status": row[9]  # Current status of the feedback
            })
        
        return activity
    
    def get_feedback_stats(self):
        """Get feedback statistics for admin dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total feedback count
        cursor.execute("SELECT COUNT(*) FROM feedback_submissions")
        total = cursor.fetchone()[0]
        
        # Status breakdown
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM feedback_submissions 
            GROUP BY status
        """)
        status_counts = dict(cursor.fetchall())
        
        # Rating average
        cursor.execute("""
            SELECT AVG(rating) 
            FROM feedback_submissions 
            WHERE rating IS NOT NULL
        """)
        avg_rating = cursor.fetchone()[0]
        
        # Category breakdown
        cursor.execute("""
            SELECT feedback_category, COUNT(*) 
            FROM feedback_submissions 
            WHERE feedback_category IS NOT NULL
            GROUP BY feedback_category
        """)
        category_counts = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            "total_feedback": total,
            "status_breakdown": status_counts,
            "average_rating": round(avg_rating, 2) if avg_rating else 0,
            "category_breakdown": category_counts
        }
    
    def _notify_admin_new_feedback(self, feedback_id, user_email, category, rating):
        """Send email notification to admin about new feedback"""
        if not self.email_config:
            return
        
        try:
            subject = f"New Feedback Submitted - {category} (Rating: {rating}/5)"
            body = f"""
            New feedback submission received:
            
            Feedback ID: {feedback_id}
            User Email: {user_email}
            Category: {category}
            Rating: {rating}/5
            
            Review this feedback in the Admin Dashboard:
            https://localhost:5000/admin/feedback/{feedback_id}
            """
            
            # Send notification (implement based on your email configuration)
            # self._send_email(self.email_config.get('admin_email'), subject, body)
            
        except Exception as e:
            print(f"Error notifying admin: {e}")
    
    def export_feedback_json(self, output_path="feedback_export.json", status_filter=None):
        """Export feedback to JSON file"""
        feedback = self.get_all_feedback(status_filter=status_filter, limit=1000)
        
        output_dir = Path(__file__).parent / "reports"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / output_path
        
        with open(output_file, 'w') as f:
            json.dump(feedback, f, indent=2, default=str)
        
        return str(output_file)


# Example usage
if __name__ == "__main__":
    handler = FeedbackHandler()
    
    # Example: Submit feedback
    result = handler.submit_feedback(
        user_email="6020GM@email.wal-mart.com",
        feedback_category="Dashboard UI",
        rating=4,
        message="The manager change cards are very helpful, but would be nice to have a filter by market."
    )
    print(f"Feedback submitted: {result}")
    
    # Example: Get all feedback
    all_feedback = handler.get_all_feedback()
    print(f"\nTotal feedback: {len(all_feedback)}")
    
    # Example: Get stats
    stats = handler.get_feedback_stats()
    print(f"\nFeedback stats: {stats}")
