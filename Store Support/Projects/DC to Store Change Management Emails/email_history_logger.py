#!/usr/bin/env python3
"""
Email History Logger Module
Tracks all sent emails to SQLite database for dashboard analytics.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum


class EmailStatus(Enum):
    """Email delivery status"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    BOUNCED = "bounced"


class EmailHistoryLogger:
    """
    Logs email sending history to SQLite database.
    Provides analytics queries for dashboard.
    """
    
    DB_PATH = "email_history.db"
    
    def __init__(self):
        """Initialize database connection"""
        self.db_path = Path(self.DB_PATH)
        self._init_database()
    
    def _init_database(self):
        """Create database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Email sends table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_sends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                send_date TEXT NOT NULL,
                send_timestamp TEXT NOT NULL,
                dc_number INTEGER,
                dc_type TEXT,
                recipients_count INTEGER,
                recipient_emails TEXT,
                subject TEXT,
                status TEXT DEFAULT 'sent',
                store_manager_changes INTEGER DEFAULT 0,
                market_manager_changes INTEGER DEFAULT 0,
                region_manager_changes INTEGER DEFAULT 0,
                total_changes INTEGER,
                stores_affected INTEGER,
                test_mode BOOLEAN DEFAULT 1,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Email delivery confirmations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_confirmations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_send_id INTEGER NOT NULL,
                recipient_email TEXT NOT NULL,
                delivery_status TEXT,
                delivery_timestamp TEXT,
                bounce_reason TEXT,
                FOREIGN KEY (email_send_id) REFERENCES email_sends(id)
            )
        """)
        
        # Daily metrics table (cached for performance)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_date TEXT UNIQUE NOT NULL,
                total_changes INTEGER DEFAULT 0,
                total_emails_sent INTEGER DEFAULT 0,
                unique_dcs_affected INTEGER DEFAULT 0,
                store_manager_changes INTEGER DEFAULT 0,
                market_manager_changes INTEGER DEFAULT 0,
                region_manager_changes INTEGER DEFAULT 0,
                stores_affected INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Change tracking by DC/role table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS changes_by_dc (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                change_date TEXT NOT NULL,
                dc_number INTEGER NOT NULL,
                dc_type TEXT,
                role_type TEXT,
                change_count INTEGER DEFAULT 1,
                stores_affected TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_email_send(self, 
                      dc_number: int,
                      dc_type: str,
                      recipients: List[str],
                      subject: str,
                      changes: Dict[str, Any],
                      test_mode: bool = True,
                      status: str = "sent") -> int:
        """
        Log an email send event.
        
        Args:
            dc_number: DC number
            dc_type: 'Ambient' or 'Perishable'
            recipients: List of recipient email addresses
            subject: Email subject line
            changes: Dict with change counts by role
                {
                    'store_manager': 4,
                    'market_manager': 2,
                    'region_manager': 0,
                    'stores_affected': 10
                }
            test_mode: Whether in test mode
            status: Email status (sent, pending, failed, bounced)
        
        Returns:
            Email send record ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        send_date = datetime.now().strftime("%Y-%m-%d")
        send_timestamp = datetime.now().isoformat()
        
        store_manager_changes = changes.get('store_manager', 0)
        market_manager_changes = changes.get('market_manager', 0)
        region_manager_changes = changes.get('region_manager', 0)
        total_changes = store_manager_changes + market_manager_changes + region_manager_changes
        stores_affected = changes.get('stores_affected', 0)
        
        cursor.execute("""
            INSERT INTO email_sends (
                send_date, send_timestamp, dc_number, dc_type, 
                recipients_count, recipient_emails, subject,
                store_manager_changes, market_manager_changes, region_manager_changes,
                total_changes, stores_affected, test_mode, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            send_date, send_timestamp, dc_number, dc_type,
            len(recipients), json.dumps(recipients), subject,
            store_manager_changes, market_manager_changes, region_manager_changes,
            total_changes, stores_affected, test_mode, status
        ))
        
        email_send_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Update daily metrics
        self._update_daily_metrics(send_date, total_changes, store_manager_changes, 
                                   market_manager_changes, region_manager_changes, stores_affected)
        
        # Log by DC
        self._log_change_by_dc(send_date, dc_number, dc_type, changes)
        
        return email_send_id
    
    def _update_daily_metrics(self, date: str, total_changes: int, 
                             store_manager_changes: int, market_manager_changes: int,
                             region_manager_changes: int, stores_affected: int):
        """Update daily metrics cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM daily_metrics WHERE metric_date = ?", (date,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE daily_metrics SET
                    total_changes = total_changes + ?,
                    total_emails_sent = total_emails_sent + 1,
                    store_manager_changes = store_manager_changes + ?,
                    market_manager_changes = market_manager_changes + ?,
                    region_manager_changes = region_manager_changes + ?,
                    stores_affected = stores_affected + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE metric_date = ?
            """, (total_changes, store_manager_changes, market_manager_changes,
                  region_manager_changes, stores_affected, date))
        else:
            cursor.execute("""
                INSERT INTO daily_metrics (
                    metric_date, total_changes, total_emails_sent,
                    store_manager_changes, market_manager_changes, region_manager_changes,
                    stores_affected
                ) VALUES (?, ?, 1, ?, ?, ?, ?)
            """, (date, total_changes, store_manager_changes, market_manager_changes,
                  region_manager_changes, stores_affected))
        
        conn.commit()
        conn.close()
    
    def _log_change_by_dc(self, date: str, dc_number: int, dc_type: str, changes: Dict):
        """Log changes broken down by DC"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        store_manager = changes.get('store_manager', 0)
        market_manager = changes.get('market_manager', 0)
        region_manager = changes.get('region_manager', 0)
        stores = changes.get('stores_affected', 0)
        
        if store_manager > 0:
            cursor.execute("""
                INSERT INTO changes_by_dc (change_date, dc_number, dc_type, role_type, change_count, stores_affected)
                VALUES (?, ?, ?, 'Store Manager', ?, ?)
            """, (date, dc_number, dc_type, store_manager, stores))
        
        if market_manager > 0:
            cursor.execute("""
                INSERT INTO changes_by_dc (change_date, dc_number, dc_type, role_type, change_count, stores_affected)
                VALUES (?, ?, ?, 'Market Manager', ?, ?)
            """, (date, dc_number, dc_type, market_manager, stores))
        
        if region_manager > 0:
            cursor.execute("""
                INSERT INTO changes_by_dc (change_date, dc_number, dc_type, role_type, change_count, stores_affected)
                VALUES (?, ?, ?, 'Region Manager', ?, ?)
            """, (date, dc_number, dc_type, region_manager, stores))
        
        conn.commit()
        conn.close()
    
    def log_delivery_confirmation(self, email_send_id: int, recipient_email: str,
                                 delivery_status: str, bounce_reason: Optional[str] = None):
        """Log email delivery confirmation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        delivery_timestamp = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO email_confirmations (
                email_send_id, recipient_email, delivery_status, delivery_timestamp, bounce_reason
            ) VALUES (?, ?, ?, ?, ?)
        """, (email_send_id, recipient_email, delivery_status, delivery_timestamp, bounce_reason))
        
        conn.commit()
        conn.close()
    
    # QUERY METHODS FOR DASHBOARD
    
    def get_total_changes_detected(self, days: int = 30) -> int:
        """Get total changes detected in last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(total_changes), 0) FROM daily_metrics
            WHERE metric_date >= date('now', '-' || ? || ' days')
        """, (days,))
        
        result = cursor.fetchone()[0]
        conn.close()
        return result
    
    def get_total_emails_sent(self, days: int = 30) -> int:
        """Get total emails sent in last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM email_sends
            WHERE send_date >= date('now', '-' || ? || ' days')
            AND status = 'sent'
        """, (days,))
        
        result = cursor.fetchone()[0]
        conn.close()
        return result
    
    def get_changes_by_dc(self, days: int = 30) -> List[Dict]:
        """Get changes grouped by DC territory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                dc_number,
                dc_type,
                SUM(change_count) as total_changes,
                COUNT(DISTINCT change_date) as days_with_changes
            FROM changes_by_dc
            WHERE change_date >= date('now', '-' || ? || ' days')
            GROUP BY dc_number, dc_type
            ORDER BY total_changes DESC
        """, (days,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'dc_number': r[0],
                'dc_type': r[1],
                'total_changes': r[2],
                'days_with_changes': r[3]
            }
            for r in results
        ]
    
    def get_changes_by_role_type(self, days: int = 30) -> Dict[str, int]:
        """Get changes broken down by role type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                role_type,
                SUM(change_count) as total
            FROM changes_by_dc
            WHERE change_date >= date('now', '-' || ? || ' days')
            GROUP BY role_type
            ORDER BY total DESC
        """, (days,))
        
        results = cursor.fetchall()
        conn.close()
        
        return {r[0]: r[1] for r in results}
    
    def get_email_delivery_confirmations(self, days: int = 30) -> Dict[str, int]:
        """Get email delivery status summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                delivery_status,
                COUNT(*) as count
            FROM email_confirmations ec
            JOIN email_sends es ON ec.email_send_id = es.id
            WHERE es.send_date >= date('now', '-' || ? || ' days')
            GROUP BY delivery_status
        """, (days,))
        
        results = cursor.fetchall()
        conn.close()
        
        return {r[0]: r[1] for r in results if r[0]}
    
    def get_daily_trend(self, days: int = 30) -> List[Dict]:
        """Get daily trend data for charts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                metric_date,
                total_changes,
                total_emails_sent,
                store_manager_changes,
                market_manager_changes,
                region_manager_changes,
                stores_affected
            FROM daily_metrics
            WHERE metric_date >= date('now', '-' || ? || ' days')
            ORDER BY metric_date ASC
        """, (days,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'date': r[0],
                'total_changes': r[1],
                'emails_sent': r[2],
                'store_manager': r[3],
                'market_manager': r[4],
                'region_manager': r[5],
                'stores_affected': r[6]
            }
            for r in results
        ]
    
    def get_dc_territory_details(self, dc_number: int, days: int = 30) -> Dict:
        """Get detailed metrics for specific DC"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                dc_type,
                role_type,
                SUM(change_count) as total,
                COUNT(DISTINCT change_date) as days
            FROM changes_by_dc
            WHERE dc_number = ?
            AND change_date >= date('now', '-' || ? || ' days')
            GROUP BY dc_type, role_type
            ORDER BY role_type
        """, (dc_number, days))
        
        results = cursor.fetchall()
        conn.close()
        
        detail = {
            'dc_number': dc_number,
            'by_role': {}
        }
        
        for r in results:
            dc_type, role_type, total, days_count = r
            if role_type not in detail['by_role']:
                detail['by_role'][role_type] = {}
            detail['by_role'][role_type][dc_type] = {
                'total_changes': total,
                'days_with_changes': days_count
            }
        
        return detail


# Convenience functions
def log_email(dc_number: int, dc_type: str, recipients: List[str], subject: str, 
              changes: Dict, test_mode: bool = True, status: str = "sent") -> int:
    """Convenience function to log email"""
    logger = EmailHistoryLogger()
    return logger.log_email_send(dc_number, dc_type, recipients, subject, changes, test_mode, status)


def get_dashboard_metrics(days: int = 30) -> Dict[str, Any]:
    """Get all metrics needed for dashboard"""
    logger = EmailHistoryLogger()
    
    return {
        'total_changes_detected': logger.get_total_changes_detected(days),
        'total_emails_sent': logger.get_total_emails_sent(days),
        'changes_by_dc': logger.get_changes_by_dc(days),
        'changes_by_role': logger.get_changes_by_role_type(days),
        'delivery_confirmations': logger.get_email_delivery_confirmations(days),
        'daily_trend': logger.get_daily_trend(days)
    }


if __name__ == "__main__":
    # Test the logger
    logger = EmailHistoryLogger()
    
    # Log a sample email
    sample_id = logger.log_email_send(
        dc_number=6020,
        dc_type='Ambient',
        recipients=['6020GM@email.wal-mart.com', '6020AGM@email.wal-mart.com'],
        subject='Test Email - Manager Changes',
        changes={
            'store_manager': 3,
            'market_manager': 1,
            'region_manager': 0,
            'stores_affected': 4
        },
        test_mode=True
    )
    
    print(f"✓ Created sample email record: {sample_id}")
    print(f"\n✓ Dashboard Metrics:")
    metrics = get_dashboard_metrics(30)
    print(f"  - Total Changes: {metrics['total_changes_detected']}")
    print(f"  - Total Emails: {metrics['total_emails_sent']}")
    print(f"  - By Role: {metrics['changes_by_role']}")
    print(f"  - By DC: {metrics['changes_by_dc'][:3]}...")
