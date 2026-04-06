-- Activity Hub Logic Rules Engine - BigQuery Schema
-- Created: April 6, 2026
-- Purpose: Store Logic Requests (notification + task + next-step composites) and execution logs
-- Dataset: wmt-assetprotection-prod.Store_Support_Dev

-- ============================================================
-- TABLE 1: logic_requests (Parent table for all logic rules)
-- ============================================================
-- Stores composite Logic Requests that may include notification, task, and next-step components
-- Single approval of the parent request activates all child components

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.logic_requests` (
    request_id STRING NOT NULL,
    name STRING NOT NULL,
    description STRING,
    created_by_admin STRING NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    
    -- Trigger configuration
    trigger_type STRING NOT NULL, -- "new_project", "project_status_changed", "task_assigned", "custom", etc.
    custom_trigger_text STRING, -- For trigger_type="custom": user's description of the custom trigger requirement
    trigger_condition STRING, -- JSON: {"project_status": "Active", "timeframe": "last_24_hours"}
    trigger_table STRING, -- Source table to monitor: "projects", "tasks", etc.
    
    -- Component selections (which child rules are included)
    has_notification_component BOOL DEFAULT FALSE,
    has_task_component BOOL DEFAULT FALSE,
    has_nextstep_component BOOL DEFAULT FALSE,
    
    -- Approval workflow
    status STRING DEFAULT "draft", -- draft, pending_approval, approved, active, inactive, archived
    approval_status STRING DEFAULT "pending", -- pending, approved, rejected
    approved_by STRING, -- Admin email who approved
    approved_at TIMESTAMP,
    rejection_reason STRING,
    
    -- Execution tracking
    next_execution TIMESTAMP,
    last_execution TIMESTAMP,
    execution_count INT64 DEFAULT 0,
    is_active BOOL DEFAULT FALSE,
    
    -- Metadata
    tags ARRAY<STRING>,
    owner_email STRING,
    
    PRIMARY KEY(request_id) NOT ENFORCED
) PARTITION BY DATE(created_at);

-- ============================================================
-- TABLE 2: notification_logic_rules (Child rules for Notification component)
-- ============================================================
-- Each Logic Request can have one notification rule (child)
-- Once parent is approved, this rule executes automatically on trigger

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.notification_logic_rules` (
    rule_id STRING NOT NULL,
    logic_request_id STRING NOT NULL, -- Foreign key to logic_requests
    
    -- Rule metadata
    name STRING,
    description STRING,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    
    -- Notification content
    category STRING NOT NULL, -- PROJECT_LIFECYCLE, TASK_WORK, URGENT, COMPLIANCE, ORG_CHANGE, SYSTEM
    trigger_event STRING NOT NULL, -- new_project, status_changed, task_assigned, etc.
    title_template STRING NOT NULL, -- "SIF Meeting Required: {project_name}"
    message_template STRING NOT NULL, -- HTML/plain text with {variable} placeholders
    
    -- Recipient and delivery
    recipient_rule STRING NOT NULL, -- JSON: {"type": "owner", "fallback": "manager"} or {"type": "users", "emails": ["user@walmart.com"]}
    channels ARRAY<STRING>, -- ["email", "in_app", "teams", "slack"]
    schedule STRING DEFAULT "immediate", -- immediate, delay_1h, daily_8am, etc.
    
    -- Status
    is_active BOOL DEFAULT TRUE,
    status STRING DEFAULT "active", -- active, inactive, archived
    
    -- Execution tracking
    last_executed_at TIMESTAMP,
    execution_count INT64 DEFAULT 0,
    last_error STRING,
    
    PRIMARY KEY(rule_id) NOT ENFORCED,
    FOREIGN KEY(logic_request_id) REFERENCES `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`(request_id) NOT ENFORCED
) PARTITION BY DATE(created_at);

-- ============================================================
-- TABLE 3: scheduler_execution_log (Audit trail of rule execution)
-- ============================================================
-- Logs every time Scheduler detects a trigger and executes a Logic Rule
-- Tracks success/failure of notification delivery

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.scheduler_execution_log` (
    execution_id STRING NOT NULL,
    
    -- Trigger detection
    trigger_timestamp TIMESTAMP NOT NULL,
    trigger_type STRING NOT NULL, -- "new_project", etc.
    trigger_source_table STRING NOT NULL,
    trigger_source_record_id STRING, -- Project ID, task ID, etc.
    
    -- Rule execution
    logic_request_id STRING NOT NULL,
    notification_rule_id STRING,
    
    -- Execution result
    status STRING NOT NULL, -- "pending", "in_progress", "success", "partial_success", "failed"
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    completed_at TIMESTAMP,
    duration_ms INT64, -- How long execution took
    
    -- Recipient and delivery details
    recipient_emails ARRAY<STRING>,
    channels_attempted ARRAY<STRING>,
    delivery_status JSON, -- {"email": "sent", "in_app": "sent", "teams": "failed"}
    error_message STRING,
    
    -- Execution metadata
    scheduler_instance_id STRING, -- Which scheduler instance ran this
    attempt_number INT64 DEFAULT 1,
    
    PRIMARY KEY(execution_id) NOT ENFORCED,
    FOREIGN KEY(logic_request_id) REFERENCES `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`(request_id) NOT ENFORCED
) PARTITION BY DATE(trigger_timestamp);

-- ============================================================
-- TABLE 4: notification_deliveries (Audit log of sent notifications)
-- ============================================================
-- Final delivery record for each notification sent to each recipient
-- Used for inbox, read status, and delivery audit

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.notification_deliveries` (
    delivery_id STRING NOT NULL,
    
    -- Reference to rule that triggered this
    execution_id STRING,
    logic_request_id STRING,
    notification_rule_id STRING,
    
    -- Recipient
    recipient_email STRING NOT NULL,
    recipient_id STRING,
    
    -- Notification content
    title STRING,
    message STRING,
    action_link STRING, -- Link to SIF form, etc.
    
    -- Channel-specific details
    channel STRING NOT NULL, -- "email", "in_app", "teams", "slack"
    channel_message_id STRING, -- e.g., Teams message ID for threading
    
    -- Status tracking
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,
    is_read BOOL DEFAULT FALSE,
    is_snoozed BOOL DEFAULT FALSE,
    snoozed_until TIMESTAMP,
    is_archived BOOL DEFAULT FALSE,
    
    -- User interactions
    clicked_at TIMESTAMP,
    click_count INT64 DEFAULT 0,
    
    -- Metadata
    tags ARRAY<STRING>,
    
    PRIMARY KEY(delivery_id) NOT ENFORCED
) PARTITION BY DATE(sent_at);

-- ============================================================
-- TABLE 5: notification_user_preferences (User delivery settings)
-- ============================================================
-- User preferences for notification delivery (channels, do-not-disturb, batching)

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.notification_user_preferences` (
    preference_id STRING NOT NULL,
    user_email STRING NOT NULL,
    user_id STRING,
    
    -- Channel preferences
    preferred_channels ARRAY<STRING>, -- ["in_app", "email", "teams"]
    do_not_disturb_enabled BOOL DEFAULT FALSE,
    do_not_disturb_start_time STRING, -- "22:00"
    do_not_disturb_end_time STRING, -- "08:00"
    do_not_disturb_days ARRAY<STRING>, -- ["saturday", "sunday"]
    
    -- Batching preferences
    batch_email BOOL DEFAULT FALSE,
    batch_frequency STRING, -- "hourly", "daily_morning", "daily_evening"
    
    -- Category preferences (optional fine-grained control)
    disabled_categories ARRAY<STRING>, -- Can opt-out of specific categories
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    
    PRIMARY KEY(preference_id) NOT ENFORCED
) PARTITION BY DATE(created_at);

-- ============================================================
-- TABLE 6: logic_request_approvals (Approval audit trail)
-- ============================================================
-- Track who approved/rejected requests and when (for compliance)

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.logic_request_approvals` (
    approval_id STRING NOT NULL,
    logic_request_id STRING NOT NULL,
    
    -- Admin action
    action STRING NOT NULL, -- "approved", "rejected", "edited"
    admin_email STRING NOT NULL,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    
    -- Approval details
    comment STRING,
    approval_level INT64 DEFAULT 1, -- Single-level approval (Phase 1)
    
    PRIMARY KEY(approval_id) NOT ENFORCED,
    FOREIGN KEY(logic_request_id) REFERENCES `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`(request_id) NOT ENFORCED
) PARTITION BY DATE(action_timestamp);
