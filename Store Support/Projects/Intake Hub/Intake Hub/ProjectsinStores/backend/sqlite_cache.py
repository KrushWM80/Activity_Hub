"""
SQLite Cache for Projects in Stores

This module provides a local SQLite cache that syncs from BigQuery.
Queries hit SQLite (milliseconds) instead of BigQuery (seconds).
Background sync keeps data fresh every 15 minutes.
"""

import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import os

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
        
        conn.commit()
        conn.close()
        print(f"[SQLite] Database initialized at {self.db_path}")
    
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
                    COALESCE(CAST(Intake_Card AS STRING), CONCAT('R-', CAST(Facility AS STRING))) as project_id,
                    CAST(Intake_Card AS STRING) as intake_card,
                    CASE
                        WHEN Project_Title IS NOT NULL AND Project_Title != '' THEN Project_Title
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
                    COALESCE(Store_Area, '') as store_area,
                    COALESCE(Business_Area, '') as business_area,
                    COALESCE(Health, PROJECT_HEALTH, '') as health,
                    COALESCE(Business_Type, '') as business_type,
                    COALESCE(ASSOCIATE_IMPACT, '') as associate_impact,
                    COALESCE(CUSTOMER_IMPACT, '') as customer_impact,
                    Last_Updated as last_updated
                FROM `{project_id}.{dataset}.{table}`
                WHERE Status = 'Active'
                ORDER BY title, WM_Week
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
                    None,  # partner - will be populated from IH_Branch_Data separately
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
            
            # Update sync metadata
            now = datetime.now().isoformat()
            cursor.execute("""
                INSERT OR REPLACE INTO sync_metadata (key, value, updated_at)
                VALUES ('last_sync', ?, ?)
            """, (now, now))
            
            conn.commit()
            conn.close()
            
            elapsed = time.time() - start_time
            self._last_sync = datetime.now()
            print(f"[SQLite] Sync complete! {len(rows)} rows in {elapsed:.2f}s")
            
            # Invalidate in-memory filter cache so next call queries fresh data
            SQLiteCache._filter_cache = None
            SQLiteCache._filter_cache_timestamp = None
            
            return True
            
        except Exception as e:
            print(f"[SQLite] Sync error: {e}")
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
        
        where_clause = " AND ".join(conditions)
        
        # Build query with DISTINCT to deduplicate rows
        query = f"""
            SELECT DISTINCT project_id, intake_card, title, project_source, division, region,
                   market, store, facility, phase, wm_week, fy, status, 
                   store_count, owner, partner, store_area, business_area, health, 
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
                'store_count': row['store_count'] or 1,
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
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT project_id) as total_projects,
                COUNT(DISTINCT store) as total_stores,
                COUNT(DISTINCT CASE WHEN project_source IN ('Operations', 'Intake Hub') THEN project_id END) as intake_projects,
                COUNT(DISTINCT CASE WHEN project_source IN ('Operations', 'Intake Hub') THEN store END) as intake_stores,
                COUNT(DISTINCT CASE WHEN project_source = 'Realty' THEN project_id END) as realty_projects,
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
                    self.sync_from_bigquery(bigquery_client, project_id, dataset, table)
                except Exception as e:
                    print(f"[SQLite] Background sync error: {e}")
                
                # Wait for next sync interval (check every second for stop signal)
                for _ in range(self.sync_interval):
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
