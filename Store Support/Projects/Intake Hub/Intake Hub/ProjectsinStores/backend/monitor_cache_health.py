"""
Cache Health Monitor - Track sync history and errors
Shows when cache last synced, how many records, and any error history
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

class CacheHealthMonitor:
    """Monitor SQLite cache sync status and history"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent / "projects_cache.db"
        self.db_path = str(db_path)
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn
    
    def check_cache_exists(self) -> bool:
        """Check if cache database exists"""
        return Path(self.db_path).exists()
    
    def get_last_sync_info(self) -> dict:
        """Get last sync timestamp and record count"""
        if not self.check_cache_exists():
            return {"exists": False, "records": 0, "last_sync": None, "status": "Cache database not found"}
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get last sync time
            cursor.execute("SELECT value FROM sync_metadata WHERE key = 'last_sync' ORDER BY updated_at DESC LIMIT 1")
            sync_row = cursor.fetchone()
            
            # Get record count
            cursor.execute("SELECT COUNT(*) as count FROM projects")
            count_row = cursor.fetchone()
            
            conn.close()
            
            last_sync = sync_row['value'] if sync_row else None
            record_count = count_row['count'] if count_row else 0
            
            return {
                "exists": True,
                "records": record_count,
                "last_sync": last_sync,
                "status": "OK" if record_count > 0 else "WARNING - No records"
            }
        except Exception as e:
            return {
                "exists": True,
                "error": str(e),
                "status": f"ERROR - {e}"
            }
    
    def get_sync_history(self, limit: int = 30) -> list:
        """Get sync attempts and errors from sync_error_log"""
        if not self.check_cache_exists():
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if error_log table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='sync_error_log'
            """)
            
            if cursor.fetchone():
                cursor.execute("""
                    SELECT timestamp, error_message, record_count, sync_duration_seconds
                    FROM sync_error_log 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                
                results = []
                for row in cursor.fetchall():
                    is_success = row['error_message'].startswith('SUCCESS')
                    results.append({
                        "timestamp": row['timestamp'],
                        "message": row['error_message'],
                        "records": row['record_count'],
                        "duration_sec": row['sync_duration_seconds'],
                        "is_success": is_success
                    })
                
                conn.close()
                return results
            else:
                conn.close()
                return []
        except Exception as e:
            print(f"Error reading sync history: {e}")
            return []
    

    
    def get_record_breakdown(self) -> dict:
        """Get breakdown of records by status/type"""
        if not self.check_cache_exists():
            return {}
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get counts by division, region, phase, etc.
            queries = {
                "By Division": "SELECT division, COUNT(*) as count FROM projects WHERE division IS NOT NULL GROUP BY division ORDER BY count DESC LIMIT 10",
                "By Phase": "SELECT phase, COUNT(*) as count FROM projects WHERE phase IS NOT NULL GROUP BY phase ORDER BY count DESC",
                "By FY": "SELECT fy, COUNT(*) as count FROM projects WHERE fy IS NOT NULL GROUP BY fy ORDER BY fy DESC",
                "Top Project Sources": "SELECT project_source, COUNT(*) as count FROM projects WHERE project_source IS NOT NULL GROUP BY project_source ORDER BY count DESC LIMIT 5",
            }
            
            results = {}
            for category, query in queries.items():
                cursor.execute(query)
                rows = cursor.fetchall()
                results[category] = [(row[0], row[1]) for row in rows]
            
            conn.close()
            return results
        except Exception as e:
            print(f"Error getting record breakdown: {e}")
            return {}
    
    def print_status_report(self):
        """Print a comprehensive status report"""
        print("\n" + "=" * 100)
        print(f"{'CACHE HEALTH MONITOR - Projects in Stores Dashboard':^100}")
        print("=" * 100)
        
        # Cache existence and counts
        print("\n[1] CACHE STATUS")
        print("-" * 100)
        info = self.get_last_sync_info()
        
        if not info.get('exists'):
            print("❌ Cache database NOT FOUND")
            print(f"   Expected location: {self.db_path}")
            return
        
        print(f"✓ Cache database exists")
        print(f"✓ Total records in cache: {info.get('records', 0):,}")
        print(f"✓ Cache status: {info.get('status')}")
        
        # Last sync info
        print("\n[2] LAST SYNC")
        print("-" * 100)
        last_sync = info.get('last_sync')
        if last_sync:
            sync_dt = datetime.fromisoformat(last_sync)
            now = datetime.now()
            age = now - sync_dt
            age_str = f"{age.days}d {age.seconds//3600}h {(age.seconds//60)%60}m ago"
            print(f"✓ Last sync: {last_sync}")
            print(f"✓ Age: {age_str}")
            
            if age < timedelta(hours=1):
                print("✓ Status: RECENT - Cache is current")
            elif age < timedelta(hours=24):
                print("⚠ Status: OK but aging - should sync again soon")
            else:
                print("❌ Status: STALE - Sync may be failing")
        else:
            print("❌ No sync record found - cache may be empty or first sync")
        
        # Sync history
        print("\n[3] SYNC HISTORY & ERRORS (Last 30 Attempts)")
        print("-" * 100)
        history = self.get_sync_history(30)
        if history:
            print(f"{'Timestamp':<26} {'Status':<15} {'Records':<12} {'Duration':<12} {'Message':<40}")
            print("-" * 100)
            for entry in history:
                status = "✓ SUCCESS" if entry['is_success'] else "✗ ERROR"
                duration = f"{entry['duration_sec']:.1f}s" if entry['duration_sec'] else "N/A"
                message = entry['message'][:40]
                if len(entry['message']) > 40:
                    message = message + "..."
                timestamp = entry['timestamp'][:19] if entry['timestamp'] else "Unknown"
                print(f"{timestamp:<26} {status:<15} {entry['records']:<12} {duration:<12} {message:<40}")
        else:
            print("No sync history found")
            print("(Run the backend server to populate sync tracking)")
        
        # Record breakdown
        print("\n[4] RECORD BREAKDOWN BY CATEGORY")
        print("-" * 100)
        breakdown = self.get_record_breakdown()
        
        if breakdown:
            for category, items in breakdown.items():
                print(f"\n{category}:")
                if items:
                    max_key_len = max(len(str(key)) for key, _ in items) if items else 20
                    for key, count in items:
                        print(f"  {str(key):<{max_key_len}}  {count:>10,} records")
                else:
                    print("  (No data)")
        else:
            print("(Unable to get record breakdown)")
        
        # Recommendations
        print("\n[5] RECOMMENDATIONS")
        print("-" * 100)
        
        record_count = info.get('records', 0)
        if record_count == 0:
            print("❌ CRITICAL: Cache is empty!")
            print("   → Run backend server to perform initial sync from BigQuery")
            print("   → Check console logs for BigQuery connection errors")
        elif record_count < 500:
            print("⚠ WARNING: Cache has very few records (< 500)")
            print("   → Check sync errors in [3] above")
            print("   → Verify column names in sync query match BigQuery schema")
            print("   → Check 'Project_Title' was removed and 'Title' is being used")
        elif record_count < 1000:
            print("⚠ NOTICE: Cache has fewer records than expected")
            print("   → Expected ~1700 records for full project list")
            print("   → May indicate WHERE Status='Active' filter is too restrictive")
        else:
            print("✓ Cache has good record count (1000+)")
            print("   → Dashboard should display all projects correctly")
        
        last_sync = info.get('last_sync')
        if last_sync:
            sync_dt = datetime.fromisoformat(last_sync)
            age = datetime.now() - sync_dt
            if age > timedelta(hours=24):
                print("\n⚠ WARNING: Cache is STALE (hasn't synced in 24+ hours)")
                print("   → Check if background sync is running")
                print("   → Verify BigQuery credentials and connectivity")
            elif age > timedelta(hours=6):
                print("\n⚠ NOTICE: Cache is aging (last sync 6+ hours ago)")
                print("   → Background sync should refresh every 15 minutes")
                print("   → May indicate intermittent sync failures")
        
        print("\n" + "=" * 100)


if __name__ == "__main__":
    monitor = CacheHealthMonitor()
    monitor.print_status_report()
