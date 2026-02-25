# 🔄 Activity Hub - Data Synchronization Guide

## Overview
This guide documents all data synchronization processes, schedules, monitoring, and troubleshooting procedures for Activity Hub datasources.

---

## 📅 Synchronization Schedule

### Daily Syncs (Overnight - 1:00 AM to 3:30 AM CT)

| Time | Data Source | From | To | Duration | Owner |
|---|---|---|---|---|---|
| 1:00 AM | Store Refresh Data | Athena | BigQuery | 15 min | Store Leadership |
| 1:30 AM | HR Data | Workday | BigQuery → PostgreSQL | 30 min | HR Systems |
| 2:00 AM | Polaris Schedules | Polaris | BigQuery | 45 min | Workforce |
| 2:30 AM | Distribution Lists | Directory | BigQuery → Cache | 20 min | Security |
| 3:00 AM | Asset Protection Data | Asset Prot Sys | BigQuery → PostgreSQL | 30 min | Asset Protection |
| 3:15 AM | Cache Warm | PostgreSQL | Redis | 15 min | App Ops |

### Real-Time Syncs

| Data Source | Frequency | Type | Target Systems |
|---|---|---|---|
| Active Directory | Real-time | Event-based | Cache, Session store |
| Microsoft Graph | Real-time | Event-based | Teams, Calendar, Email |
| Sparky AI | On-demand | Query-based | Backend services |
| User Updates | Real-time | Event-based | PostgreSQL, Cache |

### Triggered Syncs

| Trigger | Action | Target | Frequency |
|---|---|---|---|
| File Upload | Process & Load | PostgreSQL | On-demand |
| Project Update | Invalidate Cache | Redis | Immediate |
| BigQuery Update | Refresh Cache | Redis | If changed |

---

## 🔧 Sync Procedures by Datasource

### 1. BigQuery Data Sync

#### Polaris Scheduling Data

**Source**: `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
**Destination**: Activity Hub projects (Intake Hub, AMP)
**Frequency**: Daily
**Time**: 2:00 AM CT

**Sync Process**:
```bash
#!/bin/bash
# sync_polaris_data.sh

echo "Starting Polaris data sync..."
START_TIME=$(date +%s)

# Query Polaris for current schedules
gcloud bigquery query \
  --project_id=polaris-analytics-prod \
  --use_legacy_sql=false \
  --format=json \
  'SELECT * FROM us_walmart.vw_polaris_current_schedule 
   WHERE DATE(shift_date) = CURRENT_DATE()' > /tmp/polaris_data.json

# Validate results
RECORD_COUNT=$(jq 'length' /tmp/polaris_data.json)
echo "Retrieved $RECORD_COUNT records"

if [ "$RECORD_COUNT" -lt 100 ]; then
    echo "ERROR: Insufficient records ($RECORD_COUNT < 100)"
    EXIT_CODE=1
else
    # Load into application
    python3 /opt/scripts/load_polaris_data.py /tmp/polaris_data.json
    EXIT_CODE=$?
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Log results
echo "Sync completed with exit code $EXIT_CODE in ${DURATION}s" >> /var/log/polaris_sync.log
exit $EXIT_CODE
```

**Validation**:
```python
class PolarisSyncValidator:
    def validate_sync(self, data: list) -> bool:
        """Validate Polaris data sync"""
        checks = {
            'record_count': len(data) > 100,
            'required_fields': all(
                'associate_id' in r and 'store_number' in r 
                for r in data
            ),
            'data_freshness': all(
                (datetime.now() - datetime.fromisoformat(r['last_modified'])).days < 1
                for r in data if 'last_modified' in r
            )
        }
        return all(checks.values())
```

#### Asset Protection Data Sync

**Source**: `wmt-assetprotection-prod.Store_Support_Dev` tables
**Destination**: PostgreSQL + Redis Cache
**Frequency**: Daily
**Time**: 3:00 AM CT

**Sync Process**:
```bash
#!/bin/bash
# sync_asset_protection.sh

# 1. Query BigQuery
bq query --project_id=wmt-assetprotection-prod \
  --format=csv \
  'SELECT * FROM Store_Support_Dev.projects_intake_data' > /tmp/projects.csv

# 2. Validate file
wc -l /tmp/projects.csv

# 3. Load to PostgreSQL
psql -h $DB_HOST -U $DB_USER -d activity_hub_prod \
  -c "COPY projects FROM STDIN WITH CSV HEADER" < /tmp/projects.csv

# 4. Update cache timestamp
redis-cli SET "sync:asset_protection:last_update" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# 5. Invalidate project caches
redis-cli KEYS "projects:*" | xargs redis-cli DEL
```

---

### 2. API Data Sync

#### Workday HR Data

**Source**: Workday HRIS System via API
**Destination**: PostgreSQL `users` table + Distribution Lists
**Frequency**: Daily
**Time**: 1:30 AM CT

**Sync Process**:
```python
import requests
from datetime import datetime
import logging

class WorkdaySync:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.workday.com/v1"
        self.logger = logging.getLogger(__name__)
    
    def sync_employees(self) -> dict:
        """Sync employee data from Workday"""
        try:
            # 1. Get token
            token = self._get_token()
            
            # 2. Query all employees
            employees = self._query_employees(token)
            
            # 3. Validate data
            self._validate_employee_data(employees)
            
            # 4. Load to PostgreSQL
            inserted, updated = self._load_to_postgres(employees)
            
            # 5. Update metadata
            self._log_sync_result(
                datasource='workday',
                status='success',
                records=len(employees),
                inserted=inserted,
                updated=updated
            )
            
            return {
                'success': True,
                'records_synced': len(employees),
                'inserted': inserted,
                'updated': updated,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Workday sync failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _get_token(self) -> str:
        """Get OAuth token"""
        response = requests.post(
            f"{self.base_url}/oauth/token",
            json={'client_id': self.api_key}
        )
        return response.json()['access_token']
    
    def _query_employees(self, token: str) -> list:
        """Query Workday for all employees"""
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f"{self.base_url}/employees",
            headers=headers,
            params={'limit': 10000}
        )
        return response.json()['data']
    
    def _validate_employee_data(self, employees: list):
        """Validate employee data"""
        for emp in employees:
            assert 'id' in emp, "Missing employee ID"
            assert 'email' in emp, "Missing email"
            assert emp['status'] in ['active', 'inactive'], "Invalid status"
    
    def _load_to_postgres(self, employees: list) -> tuple:
        """Load employees into PostgreSQL"""
        # Implementation details...
        pass
```

#### Active Directory Sync

**Type**: Real-time (event-based)
**Trigger**: Group membership changes, user updates
**Destination**: Cache + PostgreSQL

**Process**:
```python
class ActiveDirectorySync:
    def __init__(self):
        self.graph_client = self._init_graph_client()
    
    def sync_group_members(self, group_id: str):
        """Sync group members from AD"""
        # Get group members
        members = self.graph_client.get_group_members(group_id)
        
        # Validate
        assert len(members) > 0, "Group has no members"
        
        # Update cache
        self._update_cache(group_id, members)
        
        # Update database
        self._update_database(group_id, members)
        
        # Log sync
        self._log_sync(group_id, len(members))
```

---

### 3. File-Based Data Sync

#### CSV/Excel Upload Processing

**Source**: User file uploads
**Destination**: PostgreSQL + BigQuery
**Trigger**: File upload
**Duration**: Real-time (< 5 minutes)

**Process**:
```python
from pathlib import Path
import pandas as pd

class FileUploadProcessor:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.logger = None
    
    def process_upload(self) -> dict:
        """Process uploaded file"""
        try:
            # 1. Validate file
            self._validate_file()
            
            # 2. Parse file
            df = self._parse_file()
            
            # 3. Validate data
            self._validate_data(df)
            
            # 4. Check duplicates
            duplicates = self._check_duplicates(df)
            
            # 5. Transform data
            df = self._transform_data(df)
            
            # 6. Load to database
            rows_inserted = self._load_to_database(df)
            
            # 7. Generate report
            return self._generate_report(
                rows_inserted,
                duplicates,
                'success'
            )
        except Exception as e:
            return self._generate_report(
                0,
                0,
                'error',
                str(e)
            )
    
    def _validate_file(self):
        """Validate file integrity"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        if self.file_path.suffix.lower() not in ['.csv', '.xlsx', '.json']:
            raise ValueError(f"Unsupported file type: {self.file_path.suffix}")
        
        if self.file_path.stat().st_size > 100 * 1024 * 1024:  # 100 MB
            raise ValueError("File size exceeds 100 MB limit")
    
    def _parse_file(self) -> pd.DataFrame:
        """Parse file based on type"""
        if self.file_path.suffix == '.csv':
            return pd.read_csv(self.file_path)
        elif self.file_path.suffix == '.xlsx':
            return pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file type")
```

---

## 📊 Monitoring & Status

### Health Check Dashboard

```bash
#!/bin/bash
# health_check.sh - Check all datasource sync status

echo "=== Activity Hub Datasource Health Check ==="
echo "Timestamp: $(date)"
echo

# BigQuery Status
echo "1. BigQuery Syncs:"
bq query --project_id=wmt-assetprotection-prod --format=table \
  'SELECT table_name, MAX(updated_at) as last_update
   FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.TABLES`
   GROUP BY table_name'

# PostgreSQL Status
echo
echo "2. PostgreSQL Replication:"
psql -h $DB_HOST -U $DB_USER -d activity_hub_prod \
  -c "SELECT datname, stats_reset FROM pg_stat_database WHERE datname = 'activity_hub_prod'"

# Redis Status
echo
echo "3. Redis Cache:"
redis-cli --stat

# API Sync Status
echo
echo "4. Recent API Syncs:"
psql -h $DB_HOST -U $DB_USER -d activity_hub_prod \
  -c "SELECT sync_source, status, max(sync_timestamp) as last_sync
      FROM sync_logs
      WHERE sync_timestamp > NOW() - INTERVAL '24 hours'
      GROUP BY sync_source, status
      ORDER BY last_sync DESC"
```

### Status Indicators

```javascript
// Frontend status indicator
const DataSourceStatus = {
    'Polaris': {
        'status': 'OK',
        'last_sync': '2026-02-25T02:00:00Z',
        'records': 2500000,
        'lag_hours': 0.5
    },
    'Asset Protection': {
        'status': 'OK',
        'last_sync': '2026-02-25T03:00:00Z',
        'records': 196,
        'lag_hours': 0.25
    },
    'BigQuery': {
        'status': 'OK',
        'availability': '99.95%'
    },
    'PostgreSQL': {
        'status': 'OK',
        'replication_lag_ms': 45,
        'connections': 42
    },
    'Redis': {
        'status': 'OK',
        'memory_used_mb': 1240,
        'hit_rate': 0.87
    }
};
```

---

## ⚠️ Error Handling & Recovery

### Common Sync Errors

#### Error 1: "Connection Timeout"
```
Symptom: Sync fails after 30 seconds
Cause: Network issue or service unavailable
Solution:
1. Check network connectivity
2. Verify API/database is accessible
3. Increase timeout and retry
4. Use fallback to cached data
```

**Recovery Script**:
```python
def retry_with_backoff(func, max_retries=3, initial_delay=1):
    """Retry pattern with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            time.sleep(delay)
```

#### Error 2: "Data Validation Failed"
```
Symptom: Rows rejected due to schema mismatch
Cause: Upstream data changed
Solution:
1. Review data schema
2. Update mappings if needed
3. Manual remediation for failed rows
4. Notify data owner
```

#### Error 3: "Insufficient Disk Space"
```
Symptom: Database write fails
Cause: Storage capacity reached
Solution:
1. Archive old data
2. Increase storage allocation
3. Optimize cleanup policies
4. Monitor disk usage trends
```

---

## 🔄 Retry & Fallback Logic

### Retry Strategy
```python
class RobustSyncManager:
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [30, 60, 300]  # 30s, 1m, 5m
    
    def sync_with_retry(self, datasource_name: str, sync_func):
        """Execute sync with retry logic"""
        for attempt in range(self.max_retries):
            try:
                result = sync_func()
                self._log_success(datasource_name, attempt)
                return result
            except Exception as e:
                self._log_error(datasource_name, attempt, str(e))
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_delays[attempt]
                    time.sleep(delay)
                else:
                    self._trigger_fallback(datasource_name)
                    raise
    
    def _trigger_fallback(self, datasource_name: str):
        """Fall back to cached data"""
        logger.warning(f"Triggering fallback for {datasource_name}")
        # Use last known good data from cache/backup
```

### Fallback Data Sources

```
Primary → Secondary → Tertiary

BigQuery → PostgreSQL Cache → Last snapshot
API → Cached response → Default/mock data
File Upload → Previous version → Manual entry
```

---

## 📈 Performance Metrics

### SLOs (Service Level Objectives)

| Datasource | Availability | Freshness | P95 Latency |
|---|---|---|---|
| BigQuery | 99.9% | < 4 hours | 500ms |
| Workday API | 99.5% | < 2 hours | 2s |
| Active Directory | 99.95% | Real-time | 200ms |
| PostgreSQL | 99.95% | Real-time | 50ms |
| Redis Cache | 99.9% | < 1 hour | 5ms |

### Monitoring Queries

```sql
-- Record count by datasource (last 7 days)
SELECT 
    datasource,
    DATE(sync_date) as date,
    COUNT(*) as records,
    AVG(sync_duration_ms) as avg_duration_ms
FROM sync_logs
WHERE sync_date > NOW() - INTERVAL '7 days'
GROUP BY datasource, date
ORDER BY datasource, date DESC

-- Sync success rate
SELECT
    datasource,
    ROUND(
        COUNT(CASE WHEN status = 'success' THEN 1 END) * 100.0 / COUNT(*),
        2
    ) as success_rate_pct
FROM sync_logs
WHERE sync_date > NOW() - INTERVAL '30 days'
GROUP BY datasource
```

---

## 🛠️ Maintenance & Cleanup

### Regular Maintenance Tasks

#### Weekly
```bash
# Check BigQuery optimizer statistics
bq update --description="Refreshed $(date +%Y-%m-%d)" datasets

# Analyze PostgreSQL query plans
ANALYZE activity_hub_prod;

# Redis memory optimization
redis-cli MEMORY DOCTOR
```

#### Monthly
```bash
# Archive old logs
archive_sync_logs.sh 90  # Keep 90 days

# Clean up failed data
DELETE FROM sync_logs WHERE status = 'error' AND sync_date < NOW() - INTERVAL '60 days'

# PostgreSQL maintenance
REINDEX DATABASE activity_hub_prod;
VACUUM ANALYZE;
```

---

## 📞 Support & Escalation

### Sync Issues Escalation Path

```
Tier 1: Automated Recovery
├─ Check network connectivity
├─ Retry with backoff
├─ Use fallback data
└─ Alert monitoring team

Tier 2: Manual Investigation (if Tier 1 fails)
├─ Review sync logs
├─ Check source system status  
├─ Validate data schema
└─ Contact data owner

Tier 3: Escalation (if Tier 2 fails)
├─ Engage infrastructure team
├─ Contact BigQuery support
├─ Coordinate with external systems
└─ Plan manual remediation
```

### Contact Information
```
Tier 1 On-Call: activity-hub-oncall@walmart.com
BigQuery Support: cloud-support@walmart.com
Database Admin: dba-team@walmart.com
Workday Integration: workday-admin@walmart.com
```

---

## 📋 Sync Log Retention

| Log Type | Retention | Location |
|---|---|---|
| Success logs | 90 days | PostgreSQL + Archive |
| Error logs | 180 days | PostgreSQL + Archive |
| Audit trail | 3 years | Cold storage |
| Performance metrics | 1 year | Time-series DB |

---

## 🎯 Key Takeaways

1. **Scheduled syncs run nightly**, 1:00-3:30 AM CT
2. **Real-time syncs** for user/AD changes and API updates
3. **Automated retry logic** handles transient failures
4. **Fallback to cache** when primary source unavailable
5. **Monitor SLOs** and track sync health
6. **Archive logs** for audit and troubleshooting

