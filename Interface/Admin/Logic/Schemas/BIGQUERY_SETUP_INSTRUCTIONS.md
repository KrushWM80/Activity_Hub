# Steps to Create BigQuery Tables for Logic Rules Engine

## Overview
You need to create **6 tables** in BigQuery using the schema defined in `Schemas/bigquery_tables.sql`.

**Target Project**: `wmt-assetprotection-prod`  
**Target Dataset**: `Store_Support_Dev`

---

## Step 1: Access BigQuery Console

1. Open browser and go to: **https://console.cloud.google.com/bigquery**
2. Verify you're in project: `wmt-assetprotection-prod`
   - Top-left corner should show "wmt-assetprotection-prod"
   - If not, click dropdown and select it
3. In left sidebar, expand **Datasets** and find `Store_Support_Dev`

---

## Step 2: Get the Schema SQL

Copy the complete SQL from the schema file:

**File Location**: 
```
Interface\Admin\Logic\Schemas\bigquery_tables.sql
```

**How to copy:**
1. Open the file in VS Code or your editor
2. **Select ALL** (Ctrl+A)
3. **Copy** (Ctrl+C)

---

## Step 3: Create Tables in BigQuery Console

### Method A: Using BigQuery Web UI (RECOMMENDED)

1. In BigQuery Console, click **"+ Create Dataset"** (if Store_Support_Dev doesn't exist)
   - Name: `Store_Support_Dev`
   - Leave other defaults
   - Click Create

2. Click on `Store_Support_Dev` dataset in left sidebar

3. Click **"CREATE TABLE"** button
   - From where? → **"Write custom query"**
   - Paste the ENTIRE SQL from `bigquery_tables.sql`

4. Click **"Run"** button (top right)
   - This will execute all CREATE TABLE statements at once

5. Wait for completion (should take 10-30 seconds)

6. Verify tables were created:
   - Left sidebar → expand `Store_Support_Dev`
   - Should see 6 new tables:
     - ✅ `logic_requests`
     - ✅ `notification_logic_rules`
     - ✅ `scheduler_execution_log`
     - ✅ `notification_deliveries`
     - ✅ `notification_user_preferences`
     - ✅ `logic_request_approvals`

### Method B: Using gcloud CLI (ALTERNATIVE)

```powershell
# Set project
gcloud config set project wmt-assetprotection-prod

# Create dataset (if needed)
gcloud bq datasets create Store_Support_Dev --location=US

# Run schema creation
gcloud bq query --use_legacy_sql=false < Interface\Admin\Logic\Schemas\bigquery_tables.sql
```

---

## Step 4: Verify Table Creation

### Option 1: BigQuery Web UI (Visual)

1. Go to `Store_Support_Dev` dataset
2. Expand the dataset in left sidebar
3. You should see all 6 tables listed:
   ```
   ✓ logic_requests
   ✓ notification_logic_rules
   ✓ scheduler_execution_log
   ✓ notification_deliveries
   ✓ notification_user_preferences
   ✓ logic_request_approvals
   ```

4. Click on each table to see schema

### Option 2: Run Verification Query

In BigQuery Console, run this query:

```sql
SELECT 
    table_name,
    row_count,
    size_bytes
FROM `wmt-assetprotection-prod.Store_Support_Dev.__TABLES__`
ORDER BY table_name;
```

**Expected Output (6 rows)**:
```
table_name                          | row_count | size_bytes
------------------------------------------------------------
logic_request_approvals             | 0         | 0
logic_requests                      | 0         | 0
notification_deliveries             | 0         | 0
notification_logic_rules            | 0         | 0
scheduler_execution_log             | 0         | 0
notification_user_preferences       | 0         | 0
```

---

## Step 5: Detailed Table Information

Click on each table name to see its schema:

### 1. **logic_requests** (Parent table)
- Stores composite Logic Requests
- **Key fields**: request_id, name, trigger_type, status, is_active, approval_status
- **Partitioned by**: DATE(created_at)

### 2. **notification_logic_rules** (Notification child rules)
- Stores notification configuration for approved requests
- **Key fields**: rule_id, logic_request_id, title_template, message_template, channels
- **Partitioned by**: DATE(created_at)

### 3. **scheduler_execution_log** (Execution audit trail)
- Logs every time scheduler detects trigger and executes rules
- **Key fields**: execution_id, trigger_timestamp, status, delivery_status
- **Partitioned by**: DATE(trigger_timestamp)

### 4. **notification_deliveries** (Sent notifications)
- Records every notification sent to each recipient
- **Key fields**: delivery_id, recipient_email, channel, is_read, sent_at
- **Partitioned by**: DATE(sent_at)

### 5. **notification_user_preferences** (User settings)
- Stores user delivery preferences (channels, DND hours, batching)
- **Key fields**: preference_id, user_email, preferred_channels, do_not_disturb_enabled
- **Partitioned by**: DATE(created_at)

### 6. **logic_request_approvals** (Approval history)
- Audit trail of approvals and rejections
- **Key fields**: approval_id, logic_request_id, action, admin_email, action_timestamp
- **Partitioned by**: DATE(action_timestamp)

---

## Step 6 (Optional): Check BigQuery Permissions

If you get permission errors, verify you have:
- ✅ `bigquery.datasets.update`
- ✅ `bigquery.tables.create`
- ✅ `bigquery.tables.delete`

**Who to contact**: Your GCP project admin or cloud team

---

## Troubleshooting

### Problem: "Dataset not found: Store_Support_Dev"

**Solution**: Create the dataset first
```sql
CREATE SCHEMA IF NOT EXISTS `wmt-assetprotection-prod.Store_Support_Dev`
```

### Problem: "Permission denied: User does not have bigquery.tables.create"

**Solution**: 
- Ask your GCP admin to grant you the `BigQuery Editor` role
- Or contact your cloud team

### Problem: "Syntax error in SQL"

**Solution**:
- Make sure you copied the ENTIRE file from `bigquery_tables.sql`
- Don't paste individual CREATE TABLE statements
- Paste as one batch in "Write custom query" mode

### Problem: "Some tables created, others failed"

**Solution**:
- Check error message in BigQuery console
- Usually due to missing dataset or permissions
- Drop all tables and re-run: 
  ```sql
  DROP TABLE IF EXISTS `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`;
  DROP TABLE IF EXISTS `wmt-assetprotection-prod.Store_Support_Dev.notification_logic_rules`;
  -- ... (repeat for all 6 tables)
  ```

---

## After Tables Are Created

1. **Test data insertion** (optional):
   ```sql
   INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`
   (name, created_by_admin, trigger_type, trigger_table, has_notification_component, is_active)
   VALUES
   ('Test Logic Request', 'admin@walmart.com', 'new_project', 'projects', TRUE, FALSE);
   
   -- Check insert
   SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.logic_requests` LIMIT 5;
   ```

2. **Start Scheduler Service**:
   ```powershell
   cd "Interface\Admin\Logic\Scheduler"
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
   python main.py
   ```

3. **Open Admin Dashboard**:
   - Go to Logic → Notification Alerts tab
   - Create test Logic Request
   - Watch data appear in BigQuery

---

## Quick Reference Card

| Step | Action | Time |
|------|--------|------|
| 1 | Open BigQuery Console | 1 min |
| 2 | Copy schema SQL | 1 min |
| 3 | Paste & Run in BigQuery | 2 min |
| 4 | Verify 6 tables created | 1 min |
| 5 | Review table schemas | 5 min |
| **Total** | | **~10 minutes** |

---

## Column Naming Convention Reference

The schema uses these column naming patterns:
- **IDs**: `xxx_id` (request_id, rule_id, execution_id)
- **Timestamps**: `xxx_at` or `xxx_timestamp` (created_at, executed_at, trigger_timestamp)
- **Status**: `status`, `approval_status` (draft, pending_approval, approved, active)
- **Flags**: `is_xxx`, `has_xxx` (is_active, is_read, has_notification_component)
- **Templates**: `xxx_template` (title_template, message_template)
- **JSON**: Fields like `trigger_condition`, `delivery_status` stored as STRING but contain JSON

---

## Table Relationships (Visual)

```
logic_requests (Parent)
├─ has many: notification_logic_rules
├─ has many: scheduler_execution_log
├─ has many: logic_request_approvals
└─ references: has_notification_component

notification_logic_rules (Child)
├─ belongs to: logic_requests (via logic_request_id)
└─ triggers: scheduler_execution_log

scheduler_execution_log (Execution)
├─ references: logic_requests
├─ references: notification_logic_rules
└─ creates: notification_deliveries

notification_deliveries (Result)
├─ one per: recipient + channel
└─ references: scheduler_execution_log

notification_user_preferences (User Settings)
└─ user_id/email lookup for delivery preferences

logic_request_approvals (Audit)
└─ logs all approval actions on logic_requests
```

---

That's it! Once these 6 tables are created in BigQuery, the system is ready to:
- Accept Logic Requests from Admin Dashboard
- Store them in `logic_requests`
- Execute them via Scheduler Service
- Log everything in audit tables
