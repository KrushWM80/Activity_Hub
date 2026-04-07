"""
SQLite Cache for Job Codes Dashboard

This module provides a local SQLite cache that syncs Polaris job code data from BigQuery.
Instead of relying on static CSV files, the cache auto-syncs to keep data fresh.

Features:
- Local SQLite database for fast queries (milliseconds vs BigQuery seconds)
- Automatic background sync from BigQuery every 30 minutes
- Fallback snapshots for resilience if sync fails
- Validation to prevent bad data from overwriting good cache
- Job code master table for platform-managed enrichment data
"""

import sqlite3
import threading
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
import os
import logging
from functools import lru_cache

# Setup logging
logger = logging.getLogger(__name__)

# Cache configuration
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DB = CACHE_DIR / "jobcodes_cache.db"
SNAPSHOTS_DIR = CACHE_DIR / "snapshots"
MIN_EXPECTED_RECORDS = 100  # Minimum job codes to consider sync valid
SYNC_INTERVAL = 1800  # 30 minutes in seconds
FILTER_CACHE_TTL = 300  # 5 minutes for filter cache

# Ensure directories exist
CACHE_DIR.mkdir(exist_ok=True)
SNAPSHOTS_DIR.mkdir(exist_ok=True)


class JobCodeCache:
    """SQLite cache for job codes with BigQuery sync"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = str(CACHE_DB)
        self.db_path = db_path
        self.sync_interval = SYNC_INTERVAL
        self._sync_thread = None
        self._stop_sync = threading.Event()
        self._last_sync = None
        self._sync_in_progress = False
        self._filter_cache = {}
        self._filter_cache_timestamp = {}
        
        # Initialize database
        self._init_db()
        logger.info(f"JobCodeCache initialized at {self.db_path}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper settings"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")
        return conn
    
    def _init_db(self):
        """Initialize database tables"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Polaris job codes table (source of truth)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS polaris_job_codes (
                    job_code TEXT PRIMARY KEY,
                    job_nm TEXT NOT NULL,
                    user_count INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    synced_at TIMESTAMP
                )
            """)
            
            # Job code master table (platform-managed enrichment)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_code_master (
                    job_code TEXT PRIMARY KEY,
                    workday_code TEXT,
                    category TEXT,
                    job_family TEXT,
                    pg_level TEXT,
                    supervisor BOOLEAN,
                    reports_to TEXT,
                    position_mgmt TEXT,
                    notes TEXT,
                    created_by TEXT,
                    updated_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(job_code) REFERENCES polaris_job_codes(job_code)
                )
            """)
            
            # Sync history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sync_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    record_count INTEGER,
                    success BOOLEAN,
                    error_message TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Database tables initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def get_job_codes(self, filters: Dict[str, Any] = None) -> List[Dict]:
        """
        Get all job codes with their master data merged
        
        Returns: List of dicts with combined Polaris + Master data
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    p.job_code,
                    p.job_nm,
                    p.user_count,
                    m.workday_code,
                    m.category,
                    m.job_family,
                    m.pg_level,
                    m.supervisor,
                    m.reports_to,
                    m.position_mgmt,
                    m.notes,
                    m.created_by,
                    m.updated_at,
                    p.last_updated as polaris_updated
                FROM polaris_job_codes p
                LEFT JOIN job_code_master m ON p.job_code = m.job_code
                WHERE 1=1
            """
            
            params = []
            
            # Apply filters if provided
            if filters:
                if filters.get('job_code'):
                    query += " AND p.job_code LIKE ?"
                    params.append(f"%{filters['job_code']}%")
                if filters.get('category'):
                    query += " AND m.category = ?"
                    params.append(filters['category'])
                if filters.get('job_family'):
                    query += " AND m.job_family = ?"
                    params.append(filters['job_family'])
            
            query += " ORDER BY p.job_code"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Error getting job codes: {e}")
            return []
    
    def get_job_code(self, job_code: str) -> Optional[Dict]:
        """Get a specific job code with master data"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    p.job_code,
                    p.job_nm,
                    p.user_count,
                    m.workday_code,
                    m.category,
                    m.job_family,
                    m.pg_level,
                    m.supervisor,
                    m.reports_to,
                    m.position_mgmt,
                    m.notes,
                    m.created_by,
                    m.updated_at,
                    p.last_updated as polaris_updated
                FROM polaris_job_codes p
                LEFT JOIN job_code_master m ON p.job_code = m.job_code
                WHERE p.job_code = ?
            """, (job_code,))
            
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting job code {job_code}: {e}")
            return None
    
    def update_master_data(self, job_code: str, data: Dict) -> bool:
        """Update job code master data (user-entered enrichment)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if job code exists in Polaris
            cursor.execute("SELECT 1 FROM polaris_job_codes WHERE job_code = ?", (job_code,))
            if not cursor.fetchone():
                logger.error(f"Job code {job_code} not found in Polaris data")
                conn.close()
                return False
            
            # Upsert into master table
            cursor.execute("""
                INSERT INTO job_code_master (
                    job_code, workday_code, category, job_family, pg_level,
                    supervisor, reports_to, position_mgmt, notes, created_by, updated_by, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(job_code) DO UPDATE SET
                    workday_code = COALESCE(?, workday_code),
                    category = COALESCE(?, category),
                    job_family = COALESCE(?, job_family),
                    pg_level = COALESCE(?, pg_level),
                    supervisor = COALESCE(?, supervisor),
                    reports_to = COALESCE(?, reports_to),
                    position_mgmt = COALESCE(?, position_mgmt),
                    notes = COALESCE(?, notes),
                    updated_by = ?,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                job_code,
                data.get('workday_code'),
                data.get('category'),
                data.get('job_family'),
                data.get('pg_level'),
                data.get('supervisor'),
                data.get('reports_to'),
                data.get('position_mgmt'),
                data.get('notes'),
                data.get('created_by', 'system'),
                data.get('updated_by', 'system'),
                # For UPDATE clause
                data.get('workday_code'),
                data.get('category'),
                data.get('job_family'),
                data.get('pg_level'),
                data.get('supervisor'),
                data.get('reports_to'),
                data.get('position_mgmt'),
                data.get('notes'),
                data.get('updated_by', 'system')
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Updated master data for {job_code}")
            return True
        except Exception as e:
            logger.error(f"Error updating master data for {job_code}: {e}")
            return False
    
    def sync_polaris_data(self, polaris_df) -> bool:
        """
        Sync Polaris data from BigQuery to cache
        
        Args:
            polaris_df: Pandas DataFrame with columns: job_code, job_nm, user_count
        
        Returns:
            True if sync successful, False otherwise
        """
        try:
            if polaris_df is None or len(polaris_df) < 1:  # Reduced threshold for initial load
                logger.warning(f"Polaris data validation failed: {len(polaris_df) if polaris_df is not None else 0} records")
                return False
            
            self._sync_in_progress = True
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Begin transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Clear existing data
            try:
                cursor.execute("DELETE FROM polaris_job_codes")
            except Exception as e:
                logger.warning(f"Could not delete old data: {e}")
            
            # Insert new data using REPLACE to handle any conflicts
            for _, row in polaris_df.iterrows():
                try:
                    job_code = str(row['job_code']).strip() if 'job_code' in row else None
                    job_nm = str(row.get('job_nm', '')).strip()
                    user_count = int(row.get('user_count', 0)) if 'user_count' in row else 0
                    
                    if job_code:
                        cursor.execute("""
                            REPLACE INTO polaris_job_codes (job_code, job_nm, user_count, synced_at)
                            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                        """, (job_code, job_nm, user_count))
                except Exception as e:
                    logger.warning(f"Could not insert row: {e}")
                    continue
            
            # Record successful sync
            cursor.execute("""
                INSERT INTO sync_history (record_count, success)
                VALUES (?, 1)
            """, (len(polaris_df),))
            
            conn.commit()
            self._last_sync = datetime.now()
            self._sync_in_progress = False
            
            # Save snapshot for fallback
            self._save_snapshot(polaris_df)
            
            logger.info(f"Successfully synced {len(polaris_df)} job codes from Polaris")
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error syncing Polaris data: {e}")
            try:
                cursor.execute("ROLLBACK")
                conn.close()
            except:
                pass
            self._sync_in_progress = False
            return False
    
    def _save_snapshot(self, df):
        """Save snapshot for fallback recovery"""
        try:
            snapshot_file = SNAPSHOTS_DIR / f"polaris_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            data = df.to_dict(orient='records')
            with open(snapshot_file, 'w') as f:
                json.dump(data, f)
            logger.info(f"Snapshot saved: {snapshot_file}")
        except Exception as e:
            logger.error(f"Error saving snapshot: {e}")
    
    def start_sync_thread(self, bigquery_sync_func):
        """Start background sync thread"""
        if self._sync_thread and self._sync_thread.is_alive():
            return
        
        def sync_loop():
            while not self._stop_sync.is_set():
                try:
                    if not self._sync_in_progress:
                        logger.info("Starting BigQuery sync...")
                        result = bigquery_sync_func()
                        if result is not None:
                            self.sync_polaris_data(result)
                except Exception as e:
                    logger.error(f"Sync thread error: {e}")
                
                # Sleep for sync_interval or until stop signal
                self._stop_sync.wait(self.sync_interval)
        
        self._sync_thread = threading.Thread(target=sync_loop, daemon=True)
        self._sync_thread.start()
        logger.info("Sync thread started")
    
    def stop_sync_thread(self):
        """Stop background sync thread"""
        self._stop_sync.set()
        if self._sync_thread:
            self._sync_thread.join(timeout=5)
        logger.info("Sync thread stopped")
    
    def get_sync_status(self) -> Dict:
        """Get cache sync status"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM polaris_job_codes")
            job_code_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM job_code_master")
            master_count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT sync_timestamp, record_count, success 
                FROM sync_history 
                ORDER BY sync_timestamp DESC 
                LIMIT 1
            """)
            last_sync = cursor.fetchone()
            
            conn.close()
            
            return {
                'job_codes_cached': job_code_count,
                'master_records': master_count,
                'last_sync': dict(last_sync) if last_sync else None,
                'sync_in_progress': self._sync_in_progress,
                'last_sync_time': self._last_sync.isoformat() if self._last_sync else None
            }
        except Exception as e:
            logger.error(f"Error getting sync status: {e}")
            return {}


# Global cache instance
_cache_instance = None

def get_cache() -> JobCodeCache:
    """Get or create global cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = JobCodeCache()
    return _cache_instance


def init_cache() -> JobCodeCache:
    """Initialize cache"""
    return get_cache()
