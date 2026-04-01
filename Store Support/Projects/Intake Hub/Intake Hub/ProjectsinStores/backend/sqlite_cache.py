"""
SQLite Cache for Projects in Stores

This module provides a local SQLite cache that syncs from BigQuery.
Queries hit SQLite (milliseconds) instead of BigQuery (seconds).
Background sync keeps data fresh every 15 minutes.

VALIDATION STRATEGY:
- Only updates cache if BigQuery sync produces valid data
- Minimum expected records: 1,400,000 (based on ~1,420,167 historical average)
- Sends email alerts if validation fails
- Prevents bad data from overwriting good cache
"""

import sqlite3
import threading
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration for alerts
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
NOTIFY_EMAIL = "kendall.rush@walmart.com"
FROM_EMAIL = "ProjectsInStoresDashboard@walmart.com"

# Cache validation thresholds
# BQ table has ~3.27M records per successful Tableau Prep refresh
MIN_EXPECTED_RECORDS = 100000  # Minimum to consider sync valid
MIN_SYNC_DURATION = 5  # Seconds - very fast sync still OK if we got records
MAX_ALLOWED_VARIANCE = 5000000  # Allow wide variance - table size changes with refreshes
ZERO_RECORD_RETRY_COUNT = 2  # Retry this many times before sending email
ZERO_RECORD_RETRY_TIMEOUT = 2700  # 45 minutes - sync window is 15-35 min, give buffer
MID_REFRESH_RETRY_INTERVAL = 120  # 2 minutes - retry quickly when BQ mid-refresh

# Snapshot file for fallback when cache is empty
SNAPSHOT_DIR = Path(__file__).parent / "snapshots"
SNAPSHOT_FILE = SNAPSHOT_DIR / "last_good_sync.json"
SNAPSHOT_META_FILE = SNAPSHOT_DIR / "last_good_sync_meta.json"

class SQLiteCache:
    """Local SQLite cache for fast data access"""
    
    # Class-level filter cache
    _filter_cache = None
    _filter_cache_timestamp = None
    _filter_cache_ttl = 300  # 5 minutes
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to same directory as this file
            db_path = Path(__file__).parent / "projects_cache.db"
        self.db_path = str(db_path)
        self.sync_interval = 900  # 15 minutes in seconds
        self._sync_thread = None
        self._stop_sync = threading.Event()
        self._last_sync = None
        self._sync_in_progress = False
        
        # Track zero-record failures for smart retry logic
        self._zero_record_failures = []  # List of timestamps when 0 records synced
        
        # Initialize database
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory and proper settings for concurrent access"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for better concurrent read/write
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")  # 30 second timeout
        return conn
    
    def _init_db(self):
        """Initialize the SQLite database schema"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Main projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                intake_card TEXT,
                title TEXT,
                project_source TEXT,
                division TEXT,
                region TEXT,
                market TEXT,
                store TEXT,
                facility TEXT,
                phase TEXT,
                wm_week TEXT,
                fy TEXT,
                status TEXT,
                store_count INTEGER DEFAULT 1,
                owner TEXT,
                partner TEXT,
                store_area TEXT,
                business_area TEXT,
                health TEXT,
                business_type TEXT,
                associate_impact TEXT,
                customer_impact TEXT,
                last_updated TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add new columns if they don't exist (for existing databases)
        for col in ['owner', 'partner', 'store_area', 'business_area', 'health', 'business_type', 'associate_impact', 'customer_impact']:
            try:
                cursor.execute(f"ALTER TABLE projects ADD COLUMN {col} TEXT")
            except:
                pass  # Column already exists
        
        # Create indexes for fast filtering
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_project_id ON projects(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON projects(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_division ON projects(division)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON projects(region)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_market ON projects(market)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_store ON projects(store)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_phase ON projects(phase)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fy ON projects(fy)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_project_source ON projects(project_source)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_owner ON projects(owner)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_partner ON projects(partner)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_store_area ON projects(store_area)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_business_area ON projects(business_area)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_health ON projects(health)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_business_type ON projects(business_type)")
        
        # Metadata table for sync tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Error log table for persistent error tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_error_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT NOT NULL,
                record_count INTEGER DEFAULT 0,
                sync_duration_seconds FLOAT DEFAULT 0
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sync_errors_timestamp ON sync_error_log(timestamp)")
        
        # Project-Partner lookup table for fast partner filtering
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_partners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intake_card TEXT NOT NULL,
                partner_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Index for fast partner lookups
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_project_partners_intake_card ON project_partners(intake_card)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_project_partners_partner ON project_partners(partner_name)")
        
        conn.commit()
        conn.close()
        print(f"[SQLite] Database initialized at {self.db_path}")
        
        # If cache is empty, try to restore from last good snapshot
        if self.get_record_count() == 0:
            self._restore_from_snapshot()
    
    def _save_snapshot(self, row_count: int):
        """Save current SQLite cache to a JSON snapshot file as fallback"""
        try:
            SNAPSHOT_DIR.mkdir(exist_ok=True)
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects")
            columns = [desc[0] for desc in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Save partner data too
            cursor.execute("SELECT intake_card, partner_name FROM project_partners")
            partners = [{"intake_card": r[0], "partner_name": r[1]} for r in cursor.fetchall()]
            conn.close()
            
            snapshot = {"projects": rows, "partners": partners}
            
            # Write to temp file then rename for atomicity
            tmp_file = SNAPSHOT_FILE.with_suffix(".tmp")
            with open(tmp_file, "w") as f:
                json.dump(snapshot, f)
            tmp_file.replace(SNAPSHOT_FILE)
            
            # Save metadata separately (small file, quick to read)
            meta = {
                "record_count": row_count,
                "snapshot_time": datetime.now().isoformat(),
                "partner_count": len(partners)
            }
            with open(SNAPSHOT_META_FILE, "w") as f:
                json.dump(meta, f, indent=2)
            
            print(f"[SQLite] Snapshot saved: {row_count:,} projects, {len(partners):,} partners")
        except Exception as e:
            print(f"[SQLite] Failed to save snapshot: {e}")
    
    def _restore_from_snapshot(self):
        """Restore cache from last good JSON snapshot"""
        if not SNAPSHOT_FILE.exists():
            print("[SQLite] No snapshot file found, cache will be empty until BQ sync completes")
            return
        
        try:
            # Read metadata first
            meta = {}
            if SNAPSHOT_META_FILE.exists():
                with open(SNAPSHOT_META_FILE) as f:
                    meta = json.load(f)
            
            snapshot_time = meta.get("snapshot_time", "unknown")
            print(f"[SQLite] Restoring from snapshot (saved: {snapshot_time})...")
            
            with open(SNAPSHOT_FILE) as f:
                snapshot = json.load(f)
            
            projects = snapshot.get("projects", [])
            partners = snapshot.get("partners", [])
            
            if not projects:
                print("[SQLite] Snapshot is empty, skipping restore")
                return
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get column names from first row
            columns = list(projects[0].keys())
            # Filter to only columns that exist in our table (skip 'id')
            columns = [c for c in columns if c != 'id']
            placeholders = ','.join(['?' for _ in columns])
            col_names = ','.join(columns)
            
            cursor.execute("DELETE FROM projects")
            
            insert_sql = f"INSERT INTO projects ({col_names}) VALUES ({placeholders})"
            batch = []
            for row in projects:
                batch.append(tuple(row.get(c) for c in columns))
                if len(batch) >= 1000:
                    cursor.executemany(insert_sql, batch)
                    batch = []
            if batch:
                cursor.executemany(insert_sql, batch)
            
            # Restore partners
            if partners:
                cursor.execute("DELETE FROM project_partners")
                partner_batch = []
                for p in partners:
                    partner_batch.append((p["intake_card"], p["partner_name"]))
                    if len(partner_batch) >= 5000:
                        cursor.executemany("INSERT INTO project_partners (intake_card, partner_name) VALUES (?, ?)", partner_batch)
                        partner_batch = []
                if partner_batch:
                    cursor.executemany("INSERT INTO project_partners (intake_card, partner_name) VALUES (?, ?)", partner_batch)
            
            # Set sync metadata to indicate this is snapshot data
            now = datetime.now().isoformat()
            cursor.execute("""
                INSERT OR REPLACE INTO sync_metadata (key, value, updated_at)
                VALUES ('last_sync', ?, ?)
            """, (snapshot_time, now))
            cursor.execute("""
                INSERT OR REPLACE INTO sync_metadata (key, value, updated_at)
                VALUES ('data_source', 'snapshot', ?)
            """, (now,))
            
            conn.commit()
            conn.close()
            
            self._last_sync = datetime.fromisoformat(snapshot_time) if snapshot_time != "unknown" else None
            print(f"[SQLite] Restored {len(projects):,} projects and {len(partners):,} partners from snapshot")
        except Exception as e:
            print(f"[SQLite] Failed to restore from snapshot: {e}")
    
    def get_data_freshness(self) -> Dict:
        """Get information about data freshness for the API"""
        record_count = self.get_record_count()
        last_sync = self.get_last_sync_time()
        
        # Check data source (live sync vs snapshot)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM sync_metadata WHERE key = 'data_source'")
        row = cursor.fetchone()
        if row:
            data_source = row['value']
        elif last_sync:
            # data_source key absent but last_sync exists → was a live BQ sync (snapshot restores always write both)
            data_source = 'live'
        else:
            data_source = 'unknown'
        conn.close()
        
        # Read snapshot time from meta file (independent of DB state, useful as ultimate fallback)
        snapshot_time = None
        if SNAPSHOT_META_FILE.exists():
            try:
                with open(SNAPSHOT_META_FILE) as f:
                    snap_meta = json.load(f)
                snapshot_time = snap_meta.get("snapshot_time")
            except Exception:
                pass

        freshness = {
            "record_count": record_count,
            "last_sync": last_sync.isoformat() if last_sync else None,
            "snapshot_time": snapshot_time,  # Raw snapshot file timestamp (ISO string or None)
            "data_source": data_source,  # 'live', 'snapshot', or 'unknown'
            "is_stale": False,
            "message": ""
        }
        
        if record_count == 0:
            freshness["is_stale"] = True
            freshness["message"] = "No data available. BigQuery may be mid-refresh (runs every 4 hours, takes 20-45 min)."
        elif data_source == "snapshot":
            freshness["is_stale"] = True
            freshness["message"] = f"Serving cached data from {last_sync.strftime('%b %d, %I:%M %p') if last_sync else 'unknown time'}. Live refresh pending."
        elif last_sync:
            age_minutes = (datetime.now() - last_sync).total_seconds() / 60
            if age_minutes > 60:
                freshness["is_stale"] = True
                freshness["message"] = f"Data is {int(age_minutes)} minutes old. Next sync may be pending."
            else:
                freshness["message"] = f"Data synced {int(age_minutes)} minutes ago."
        
        return freshness
    
    def get_last_sync_time(self) -> Optional[datetime]:
        """Get the last successful sync time"""
        # Return instance variable first (most recent, no race condition)
        if self._last_sync:
            return self._last_sync
        
        # Fallback to database
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM sync_metadata WHERE key = 'last_sync'")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return datetime.fromisoformat(row['value'])
        return None
    
    def get_record_count(self) -> int:
        """Get the number of records in cache"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM projects")
        row = cursor.fetchone()
        conn.close()
        return row['count'] if row else 0
    
    def is_cache_valid(self, max_age_minutes: int = 30) -> bool:
        """Check if cache is valid (has data and not too old)"""
        last_sync = self.get_last_sync_time()
        has_data = self.get_record_count() > 0
        
        # If we have data but no sync time, still consider it valid
        if has_data and not last_sync:
            return True
        
        if not last_sync:
            return False
        
        age = (datetime.now() - last_sync).total_seconds() / 60
        
        # Handle clock skew - if age is negative (future timestamp), cache is valid
        if age < 0:
            return has_data
        
        return has_data and age < max_age_minutes
    
    def send_validation_failure_email(self, reason: str, record_count: int, sync_duration: float):
        """Send email alert when cache validation fails"""
        try:
            last_sync_time = self.get_last_sync_time()
            current_cache_count = self.get_record_count()
            
            if last_sync_time:
                cache_age = datetime.now() - datetime.fromisoformat(last_sync_time.isoformat() if isinstance(last_sync_time, datetime) else last_sync_time)
                age_str = f"{cache_age.days}d {cache_age.seconds//3600}h {(cache_age.seconds//60)%60}m"
            else:
                age_str = "No valid sync on record"
            
            subject = "⚠️ [ALERT] Projects in Stores Cache Sync Failed"
            
            variance = abs(record_count - MIN_EXPECTED_RECORDS) if record_count > 0 else 0
            
            body = f"""
CACHE VALIDATION FAILED - INVESTIGATION REQUIRED

Sync Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: VALIDATION FAILED

Data Quality Check:
- Records Synced: {record_count:,}
- Expected: ~{MIN_EXPECTED_RECORDS:,}
- Variance: ±{variance:,} (threshold: ±{MAX_ALLOWED_VARIANCE:,})
- Sync Duration: {sync_duration:.1f} seconds

Failure Reason: {reason}

System Protection:
✓ Cache NOT updated - using last valid version
✓ Previous data preserved and serving
✓ Cache Age: {age_str}
✓ Records in Cache: {current_cache_count:,}

Validation Rules:
1. Variance within ±50k is normal (acceptable)
2. 0 records: Retried 2 times (15-35 min sync window)
3. Sync < 60 seconds: Incomplete (data error)
4. Duration & variance: Validates data quality

Action Required:
1. Check if data sync is still running (check timestamps: started 8:36am, runs 15-35 min)
2. If still running: System will retry, no action needed
3. If stuck past 45 minutes:
   a) Log in to Google Cloud Console
   b) Query: wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data
   c) Check: SELECT COUNT(*) FROM ... WHERE Status='Active'
   d) Verify result is ~1,420,000 records
   e) Check for schema changes or BigQuery errors

Resources:
- BigQuery Table: wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data
- Cache Location: {self.db_path}
- Monitor: Run monitor_cache_health.py to check full status
- Last Sync Log: Check sync_error_log table in projects_cache.db

Current Protection:
- Dashboard continues working with valid cached data
- System will attempt recovery on next sync cycle
- You will receive another email only if issue persists

This is an automated alert. Do not reply to this email.
"""
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = FROM_EMAIL
            msg['To'] = NOTIFY_EMAIL
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email via Walmart SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.send_message(msg)
            
            print(f"[Email] Alert sent to {NOTIFY_EMAIL}")
            
        except Exception as e:
            print(f"[Email] Failed to send alert: {e}")
    
    def validate_bigquery_sync(self, record_count: int, sync_duration: float) -> tuple[bool, str]:
        """
        Validate if BigQuery sync data is valid before updating cache
        
        Smart validation with retry logic:
        - Variance within ±50k is acceptable (no email)
        - 0 records: Likely mid-sync (15-35 min), retry before emailing
        - Uses last good cache version until issue resolves
        
        Returns: (is_valid, reason_if_invalid)
        """
        # Check 1: Handle 0 records (mid-sync scenario)
        if record_count == 0:
            current_time = datetime.now()
            self._zero_record_failures.append(current_time)
            
            # Clean up old failures outside the retry window
            self._zero_record_failures = [
                t for t in self._zero_record_failures 
                if (current_time - t).total_seconds() < ZERO_RECORD_RETRY_TIMEOUT
            ]
            
            # Count recent failures in retry window
            recent_failures = len(self._zero_record_failures)
            
            if recent_failures <= ZERO_RECORD_RETRY_COUNT:
                # Still within retry attempts - don't email yet
                reason = f"0 records received (retry {recent_failures}/{ZERO_RECORD_RETRY_COUNT}) - likely mid-sync"
                print(f"[SQLite] ⏳ {reason} - will retry")
                return False, reason
            else:
                # Exceeded retries - this is a real failure
                reason = f"0 records after {recent_failures} retry attempts (45+ minutes) - data sync appears stuck"
                print(f"[SQLite] ❌ {reason}")
                return False, reason
        
        # Check 2: Validate record count is within acceptable variance
        variance = abs(record_count - MIN_EXPECTED_RECORDS)
        
        if variance > MAX_ALLOWED_VARIANCE:
            reason = f"Record count variance too high ({record_count:,} vs {MIN_EXPECTED_RECORDS:,}, variance: ±{variance:,} > ±{MAX_ALLOWED_VARIANCE:,})"
            return False, reason
        
        # Check 3: Sync duration reasonable (only check if we have records)
        # If we got valid record count, speed doesn't matter - fast sync is good!
        # Only worry about slow/incomplete syncs if we got 0 records
        if record_count > 0 and sync_duration < MIN_SYNC_DURATION:
            # Got records quickly - this is actually good, not bad. Accept it.
            print(f"[SQLite] ✓ Fast sync completed in {sync_duration:.1f}s with {record_count:,} records")
            return True, ""
        
        # All checks passed
        if variance > 0:
            print(f"[SQLite] ✓ Valid sync (variance: ±{variance:,} within ±{MAX_ALLOWED_VARIANCE:,})")
        return True, ""
    
    def _should_send_email(self, record_count: int, validation_reason: str) -> bool:
        """
        Determine if an email alert should be sent
        
        Don't email if:
        - 0 records and within retry attempts window
        - Variance within ±50k (acceptable normal variation)
        
        Do email if:
        - 0 records exceeded retry attempts
        - Variance significantly outside threshold
        - Other critical issues
        """
        # If 0 records and we have some failures but haven't exceeded retry limit
        if record_count == 0:
            recent_failures = len(self._zero_record_failures)
            if recent_failures <= ZERO_RECORD_RETRY_COUNT:
                return False  # Still retrying, don't email
        
        return True  # Email for all other failures
    
    def sync_from_bigquery(self, bigquery_client, project_id: str, dataset: str, table: str) -> bool:
        """Sync all data from BigQuery to SQLite"""
        if self._sync_in_progress:
            print("[SQLite] Sync already in progress, skipping...")
            return False
        
        self._sync_in_progress = True
        start_time = time.time()
        
        try:
            print(f"[SQLite] Starting sync from BigQuery...")
            
            # Fetch all data from BigQuery
            query = f"""
                SELECT 
                    COALESCE(CAST(Intake_Card AS STRING), CAST(PROJECT_ID AS STRING), Unique_Key, CONCAT('FAC-', CAST(Facility AS STRING))) as project_id,
                    CAST(Intake_Card AS STRING) as intake_card,
                    CASE
                        WHEN Title IS NOT NULL AND Title != '' THEN Title
                        WHEN Project_Type IS NOT NULL AND Project_Type != 'None' AND Project_Type != '' 
                             AND Initiative_Type IS NOT NULL AND Initiative_Type != '' 
                            THEN CONCAT(Project_Type, ' - ', Initiative_Type)
                        WHEN Initiative_Type IS NOT NULL AND Initiative_Type != '' THEN Initiative_Type
                        ELSE 'Untitled'
                    END as title,
                    Project_Source as project_source,
                    Division as division,
                    Region as region,
                    Market as market,
                    CAST(Facility AS STRING) as store,
                    CAST(Facility AS STRING) as facility,
                    Phase as phase,
                    WM_Week as wm_week,
                    FY as fy,
                    Status as status,
                    COALESCE(Owner, PROJECT_OWNER, '') as owner,
                    '' as partner,
                    COALESCE(Store_Area, '') as store_area,
                    COALESCE(Business_Area, '') as business_area,
                    COALESCE(Health, PROJECT_HEALTH_DESC, PROJECT_HEALTH, '') as health,
                    COALESCE(Business_Type, '') as business_type,
                    COALESCE(ASSOCIATE_IMPACT_DESC, ASSOCIATE_IMPACT, '') as associate_impact,
                    COALESCE(CUSTOMER_IMPACT_DESC, CUSTOMER_IMPACT, '') as customer_impact,
                    COALESCE(Last_Updated, UPDATE_TS) as last_updated
                FROM `{project_id}.{dataset}.{table}`
                WHERE Status = 'Active'
                ORDER BY Title, WM_Week
            """
            
            result = bigquery_client.query(query).result()
            rows = list(result)
            
            print(f"[SQLite] Fetched {len(rows)} rows from BigQuery")
            
            # Clear existing data and insert new
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Use transaction for atomicity
            cursor.execute("DELETE FROM projects")
            
            # Batch insert
            insert_sql = """
                INSERT INTO projects (
                    project_id, intake_card, title, project_source, division, region,
                    market, store, facility, phase, wm_week, fy, status, owner, partner,
                    store_area, business_area, health, business_type, associate_impact,
                    customer_impact, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            batch = []
            for row in rows:
                batch.append((
                    row.project_id,
                    row.intake_card,
                    row.title,
                    row.project_source,
                    row.division,
                    row.region,
                    row.market,
                    row.store,
                    row.facility,
                    row.phase,
                    row.wm_week,
                    row.fy,
                    row.status,
                    row.owner,
                    row.partner,
                    row.store_area,
                    row.business_area,
                    row.health,
                    row.business_type,
                    row.associate_impact,
                    row.customer_impact,
                    row.last_updated.isoformat() if row.last_updated else None
                ))
                
                # Insert in batches of 1000
                if len(batch) >= 1000:
                    cursor.executemany(insert_sql, batch)
                    batch = []
            
            # Insert remaining
            if batch:
                cursor.executemany(insert_sql, batch)
            
            # Sync partner data from IH_Branch_Data
            print("[SQLite] Syncing partner data...")
            try:
                partner_query = """
                    SELECT 
                        CAST(Intake_Card_Nbr AS STRING) as intake_card,
                        BRANCH_NAME as partner_name
                    FROM `{project_id}.Store_Support.IH_Branch_Data`
                    WHERE BRANCH_NAME IS NOT NULL AND BRANCH_NAME != ''
                """.format(project_id=project_id)
                
                partner_result = bigquery_client.query(partner_query).result()
                partner_rows = list(partner_result)
                
                # Clear existing partner data
                cursor.execute("DELETE FROM project_partners")
                
                # Insert partners
                partner_insert_sql = """
                    INSERT INTO project_partners (intake_card, partner_name)
                    VALUES (?, ?)
                """
                
                partner_batch = []
                for row in partner_rows:
                    partner_batch.append((row.intake_card, row.partner_name))
                    
                    if len(partner_batch) >= 5000:
                        cursor.executemany(partner_insert_sql, partner_batch)
                        partner_batch = []
                
                if partner_batch:
                    cursor.executemany(partner_insert_sql, partner_batch)
                
                print(f"[SQLite] Synced {len(partner_rows)} partner records")
                
            except Exception as e:
                print(f"[SQLite] Partner sync warning: {e} (continuing without partners)")
            
            # VALIDATION: Check if sync data is valid before updating cache
            elapsed = time.time() - start_time
            is_valid, validation_reason = self.validate_bigquery_sync(len(rows), elapsed)
            
            if not is_valid:
                # VALIDATION FAILED - Rollback transaction (preserve old cache)
                print(f"[SQLite] ❌ VALIDATION FAILED: {validation_reason}")
                print(f"[SQLite] Rolling back transaction - cache will NOT be updated")
                
                # Rollback the transaction (don't update cache)
                conn.rollback()
                
                # Log the failure
                cursor.execute("""
                    INSERT INTO sync_error_log (error_message, record_count, sync_duration_seconds)
                    VALUES (?, ?, ?)
                """, (f"VALIDATION FAILED: {validation_reason}", len(rows), elapsed))
                conn.commit()
                conn.close()
                
                # Determine if we should send email
                should_email = self._should_send_email(len(rows), validation_reason)
                
                if should_email:
                    # Send email alert only if not a retry scenario
                    print(f"[SQLite] Sending validation failure alert...")
                    self.send_validation_failure_email(validation_reason, len(rows), elapsed)
                else:
                    print(f"[SQLite] Retry scenario detected - not emailing yet. {validation_reason}")
                
                print(f"[SQLite] Cache NOT updated. Keeping previous valid data.")
                return False
            
            # VALIDATION PASSED - Commit the cache update
            print(f"[SQLite] ✓ Validation passed - updating cache with {len(rows):,} records")
            
            # Clear zero-record failures on successful sync
            self._zero_record_failures = []
            
            # Update sync metadata
            now = datetime.now().isoformat()
            cursor.execute("""
                INSERT OR REPLACE INTO sync_metadata (key, value, updated_at)
                VALUES ('last_sync', ?, ?)
            """, (now, now))
            cursor.execute("""
                INSERT OR REPLACE INTO sync_metadata (key, value, updated_at)
                VALUES ('data_source', 'live', ?)
            """, (now,))
            
            # Log successful sync with record count
            cursor.execute("""
                INSERT INTO sync_error_log (error_message, record_count, sync_duration_seconds)
                VALUES (?, ?, ?)
            """, (f"SUCCESS: {len(rows)} records synced from BigQuery", len(rows), elapsed))
            
            conn.commit()
            
            # Save snapshot for fallback (after commit so data is consistent)
            self._save_snapshot(len(rows))
            
            # Invalidate in-memory caches - partner data now comes from BigQuery JOIN
            from database import DatabaseService
            DatabaseService._projects_cache = None
            DatabaseService._cache_timestamp = None
            SQLiteCache._filter_cache = None
            SQLiteCache._filter_cache_timestamp = None
            
            conn.close()
            
            elapsed = time.time() - start_time
            self._last_sync = datetime.now()
            print(f"[SQLite] Sync complete! {len(rows)} rows in {elapsed:.2f}s")
            
            # Invalidate in-memory filter cache so next call queries fresh data
            SQLiteCache._filter_cache = None
            SQLiteCache._filter_cache_timestamp = None
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"[SQLite] Sync error: {error_msg}")
            
            # Log error to database
            try:
                elapsed = time.time() - start_time
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sync_error_log (error_message, record_count, sync_duration_seconds)
                    VALUES (?, ?, ?)
                """, (error_msg, 0, elapsed))
                conn.commit()
                conn.close()
                print(f"[SQLite] Error logged to database")
            except Exception as log_error:
                print(f"[SQLite] Failed to log error: {log_error}")
            
            return False
        finally:
            self._sync_in_progress = False
    
    def get_projects(self, filters: Dict[str, Any] = None, limit: int = None, 
                     title_search: str = None) -> List[Dict]:
        """Get projects from SQLite cache with optional filters"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build WHERE clause
        conditions = ["1=1"]
        params = []
        
        if filters:
            if filters.get('division'):
                conditions.append("division = ?")
                params.append(filters['division'])
            if filters.get('region'):
                conditions.append("region = ?")
                params.append(filters['region'])
            if filters.get('market'):
                conditions.append("market = ?")
                params.append(filters['market'])
            if filters.get('store'):
                conditions.append("store = ?")
                params.append(str(filters['store']))
            if filters.get('phase'):
                conditions.append("phase = ?")
                params.append(filters['phase'])
            if filters.get('fy'):
                conditions.append("fy = ?")
                params.append(filters['fy'])
            if filters.get('wm_week'):
                conditions.append("wm_week = ?")
                params.append(filters['wm_week'])
            if filters.get('project_source'):
                conditions.append("project_source = ?")
                params.append(filters['project_source'])
            if filters.get('owner'):
                conditions.append("owner = ?")
                params.append(filters['owner'])
            if filters.get('partner'):
                conditions.append("partner = ?")
                params.append(filters['partner'])
            if filters.get('business_area'):
                conditions.append("business_area = ?")
                params.append(filters['business_area'])
            if filters.get('store_area'):
                conditions.append("store_area = ?")
                params.append(filters['store_area'])
            if filters.get('business_type'):
                conditions.append("business_type = ?")
                params.append(filters['business_type'])
            if filters.get('health'):
                conditions.append("health = ?")
                params.append(filters['health'])
            if filters.get('associate_impact'):
                conditions.append("associate_impact = ?")
                params.append(filters['associate_impact'])
            if filters.get('customer_impact'):
                conditions.append("customer_impact = ?")
                params.append(filters['customer_impact'])
        
        if title_search:
            conditions.append("(LOWER(title) LIKE ? OR LOWER(project_id) LIKE ?)")
            params.append(f"%{title_search.lower()}%")
            params.append(f"%{title_search.lower()}%")
        
        # Always exclude NULL project_ids — they cause Pydantic validation crashes
        conditions.append("project_id IS NOT NULL")
        conditions.append("project_id != ''")
        
        where_clause = " AND ".join(conditions)
        
        # Build query with DISTINCT to deduplicate rows
        query = f"""
            SELECT DISTINCT project_id, intake_card, title, project_source, division, region,
                   market, store, facility, phase, wm_week, fy, status, 
                   owner, partner, store_area, business_area, health, 
                   business_type, associate_impact, customer_impact, last_updated
            FROM projects
            WHERE {where_clause}
            ORDER BY title, wm_week
        """
        
        if limit:
            query += f" LIMIT {limit}"
        else:
            # Default limit: 50,000 rows to capture all unique projects
            # (vs 1,000 which was causing missing results when filtering to all sources)
            query += " LIMIT 50000"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts
        projects = []
        for row in rows:
            projects.append({
                'project_id': row['project_id'],
                'intake_card': row['intake_card'],
                'title': row['title'],
                'project_source': row['project_source'],
                'division': row['division'],
                'region': row['region'],
                'market': row['market'],
                'store': row['store'],
                'facility': row['facility'],
                'phase': row['phase'],
                'wm_week': row['wm_week'],
                'fy': row['fy'],
                'status': row['status'],
                'store_count': 1,
                'owner': row['owner'],
                'store_area': row['store_area'],
                'business_area': row['business_area'],
                'health': row['health'],
                'business_type': row['business_type'],
                'associate_impact': row['associate_impact'],
                'customer_impact': row['customer_impact'],
                'last_updated': row['last_updated']
            })
        
        return projects
    
    def get_summary(self) -> Dict:
        """Get summary statistics from SQLite cache"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Total counts
        # NOTE: Realty records use title as unique identifier (project_id is NULL for Realty)
        # Operations/Intake Hub records use project_id as unique identifier
        cursor.execute("""
            SELECT 
                (COUNT(DISTINCT CASE WHEN project_source IN ('Operations', 'Intake Hub') AND project_id IS NOT NULL THEN project_id END) +
                 COUNT(DISTINCT CASE WHEN project_source = 'Realty' AND title IS NOT NULL THEN title END)) as total_projects,
                COUNT(DISTINCT store) as total_stores,
                COUNT(DISTINCT CASE WHEN project_source IN ('Operations', 'Intake Hub') AND project_id IS NOT NULL THEN project_id END) as intake_projects,
                COUNT(DISTINCT CASE WHEN project_source IN ('Operations', 'Intake Hub') THEN store END) as intake_stores,
                COUNT(DISTINCT CASE WHEN project_source = 'Realty' AND title IS NOT NULL THEN title END) as realty_projects,
                COUNT(DISTINCT CASE WHEN project_source = 'Realty' THEN store END) as realty_stores,
                MAX(last_updated) as last_updated
            FROM projects
        """)
        row = cursor.fetchone()
        
        summary = {
            'total_active_projects': row['total_projects'] or 0,
            'total_stores': row['total_stores'] or 0,
            'intake_hub_projects': row['intake_projects'] or 0,
            'intake_hub_stores': row['intake_stores'] or 0,
            'realty_projects': row['realty_projects'] or 0,
            'realty_stores': row['realty_stores'] or 0,
            'last_updated': row['last_updated'],
            'cache_last_sync': self.get_last_sync_time().isoformat() if self.get_last_sync_time() else None
        }
        
        conn.close()
        return summary
    
    def get_filter_options(self) -> Dict:
        """Get all unique filter values from SQLite cache"""
        # Check if filter cache is still valid
        if (SQLiteCache._filter_cache is not None and 
            SQLiteCache._filter_cache_timestamp is not None):
            age = (datetime.now() - SQLiteCache._filter_cache_timestamp).total_seconds()
            if age < SQLiteCache._filter_cache_ttl:
                print(f"[CACHE] Returning cached filters with {len(SQLiteCache._filter_cache)} keys (age: {age:.1f}s)", flush=True)
                return SQLiteCache._filter_cache
        
        # Cache is stale or doesn't exist, query database
        conn = self._get_connection()
        cursor = conn.cursor()
        
        filters = {}
        
        # Get unique values for each filter
        columns_to_fetch = [
            ('division', 'divisions'),
            ('region', 'regions'),
            ('market', 'markets'),
            ('store', 'stores'),
            ('phase', 'phases'),
            ('fy', 'fiscal_years'),
            ('wm_week', 'wm_weeks'),
            ('project_source', 'project_sources'),
            ('owner', 'owners'),
            ('store_area', 'store_areas'),
            ('business_area', 'business_areas'),
            ('health', 'health_statuses'),
            ('business_type', 'business_types'),
            ('associate_impact', 'associate_impacts'),
            ('customer_impact', 'customer_impacts')
        ]
        
        print(f"[FILTER] Fetching {len(columns_to_fetch)} filter columns from database", flush=True)
        for column, key in columns_to_fetch:
            try:
                cursor.execute(f"SELECT DISTINCT {column} FROM projects WHERE {column} IS NOT NULL AND {column} != '' ORDER BY {column}")
                values = [row[0] for row in cursor.fetchall()]
                filters[key] = values
                print(f"[FILTER]   {key}: {len(values)} values", flush=True)
            except Exception as e:
                print(f"[FILTER] ERROR fetching {key}: {e}", flush=True)
        
        print(f"[FILTER] Total filters collected: {len(filters)} keys", flush=True)
        conn.close()
        
        # Cache the results
        SQLiteCache._filter_cache = filters
        SQLiteCache._filter_cache_timestamp = datetime.now()
        
        return filters
    
    def get_unique_project_titles(self) -> List[Dict]:
        """Get all unique project titles with their store counts and project IDs"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                title,
                MIN(project_id) as project_id,
                COUNT(DISTINCT store) as store_count,
                MIN(project_source) as project_source
            FROM projects 
            WHERE title IS NOT NULL AND title != '' AND title != 'Untitled'
            GROUP BY title
            ORDER BY title
        """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'title': row['title'],
                'project_id': row['project_id'],
                'store_count': row['store_count'],
                'project_source': row['project_source']
            })
        
        conn.close()
        return results
    
    def start_background_sync(self, bigquery_client, project_id: str, dataset: str, table: str):
        """Start background sync thread"""
        if self._sync_thread and self._sync_thread.is_alive():
            print("[SQLite] Background sync already running")
            return
        
        self._stop_sync.clear()
        
        def sync_loop():
            while not self._stop_sync.is_set():
                try:
                    success = self.sync_from_bigquery(bigquery_client, project_id, dataset, table)
                except Exception as e:
                    print(f"[SQLite] Background sync error: {e}")
                    success = False
                
                # If sync got 0 rows (BQ mid-refresh), retry faster (every 2 min)
                # Otherwise use normal 15-minute interval
                if not success and self.get_record_count() == 0 and len(self._zero_record_failures) > 0:
                    wait_seconds = MID_REFRESH_RETRY_INTERVAL
                    print(f"[SQLite] BQ appears mid-refresh, retrying in {wait_seconds}s...")
                elif not success and self._zero_record_failures:
                    wait_seconds = MID_REFRESH_RETRY_INTERVAL
                    print(f"[SQLite] Zero records from BQ, retrying in {wait_seconds}s...")
                else:
                    wait_seconds = self.sync_interval
                
                for _ in range(wait_seconds):
                    if self._stop_sync.is_set():
                        break
                    time.sleep(1)
        
        self._sync_thread = threading.Thread(target=sync_loop, daemon=True)
        self._sync_thread.start()
        print(f"[SQLite] Background sync started (interval: {self.sync_interval}s)")
    
    def stop_background_sync(self):
        """Stop background sync thread"""
        self._stop_sync.set()
        if self._sync_thread:
            self._sync_thread.join(timeout=5)
        print("[SQLite] Background sync stopped")
    
    def get_project_ids_by_partners(self, partners: List[str]) -> List[str]:
        """Get list of intake_cards (project IDs) for given partners"""
        if not partners:
            return []
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build a parameter list for the IN clause
        placeholders = ','.join('?' * len(partners))
        query = f"""
            SELECT DISTINCT intake_card
            FROM project_partners
            WHERE partner_name IN ({placeholders})
        """
        
        cursor.execute(query, partners)
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_partners_for_project(self, intake_card: str) -> List[str]:
        """Get list of partners for a given project (intake_card)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT partner_name
            FROM project_partners
            WHERE intake_card = ?
            ORDER BY partner_name
        """, (intake_card,))
        
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def force_sync(self, bigquery_client, project_id: str, dataset: str, table: str) -> bool:
        """Force an immediate sync from BigQuery"""
        return self.sync_from_bigquery(bigquery_client, project_id, dataset, table)


# Singleton instance
_cache_instance: Optional[SQLiteCache] = None

def get_cache() -> SQLiteCache:
    """Get or create the singleton cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = SQLiteCache()
    return _cache_instance
