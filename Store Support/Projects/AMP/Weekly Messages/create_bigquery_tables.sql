-- Adobe Analytics to BigQuery - Table Creation
-- Created: April 7, 2026
-- Purpose: Store Adobe Analytics data from Weekly Messages and Playbook Hub reports
-- Dataset: wmt-assetprotection-prod.Store_Support_Dev
-- Direction: Copy-paste each CREATE statement into BigQuery Console and run

-- ============================================================
-- TABLE 1: bq_weekly_messages_devices
-- ============================================================
-- Device-level page views for Weekly Messages FY27 (by device type)
-- Categories: Fashion, Home, Fresh, Frontend, Hardlines, Backroom, People, Asset Protection, Entertainment, MM Overview, Consumables & OTC, Food, Store Fulfillment, Seasonal

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.bq_weekly_messages_devices` (
    report_date DATE NOT NULL,
    category STRING NOT NULL,
    page_name STRING NOT NULL,
    tablets_page_views INT64,
    desktop_page_views INT64,
    store_devices_page_views INT64,
    mobile_phones_page_views INT64,
    xcover_devices_page_views INT64,
    total_page_views INT64,
    extracted_date TIMESTAMP NOT NULL,
    
    PRIMARY KEY(report_date, category, page_name) NOT ENFORCED
) 
PARTITION BY report_date
CLUSTER BY category, page_name
OPTIONS(
    description="Weekly Messages device-level page views from Adobe Analytics",
    require_partition_filter=FALSE
);

-- ============================================================
-- TABLE 2: bq_weekly_messages_metrics
-- ============================================================
-- Aggregated metrics for Weekly Messages FY27 (Page Views, Unique Users, Average Time, Visits)

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.bq_weekly_messages_metrics` (
    report_date DATE NOT NULL,
    category STRING NOT NULL,
    page_name STRING NOT NULL,
    page_views INT64,
    unique_users FLOAT64,
    average_time_on_site FLOAT64,
    visits INT64,
    extracted_date TIMESTAMP NOT NULL,
    
    PRIMARY KEY(report_date, category, page_name) NOT ENFORCED
) 
PARTITION BY report_date
CLUSTER BY category, page_name
OPTIONS(
    description="Weekly Messages aggregated metrics (page views, unique users, time, visits) from Adobe Analytics",
    require_partition_filter=FALSE
);

-- ============================================================
-- TABLE 3: bq_playbook_hub_metrics
-- ============================================================
-- Playbook Hub page views by user type (Salary Associates vs Hourly Associates)
-- Playbooks: Playbook Hub, Valentines, Baby Days, Easter

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.bq_playbook_hub_metrics` (
    report_date DATE NOT NULL,
    playbook_category STRING NOT NULL,
    page_name STRING NOT NULL,
    total_page_views INT64,
    store_salary_associates_views INT64,
    store_hourly_associates_views INT64,
    report_period_start DATE,
    report_period_end DATE,
    extracted_date TIMESTAMP NOT NULL,
    
    PRIMARY KEY(report_date, playbook_category, page_name) NOT ENFORCED
) 
PARTITION BY report_date
CLUSTER BY playbook_category
OPTIONS(
    description="Playbook Hub page views by user type (Salary/Hourly Associates) from Adobe Analytics",
    require_partition_filter=FALSE
);

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Verify tables exist
SELECT
    table_schema,
    table_name,
    CASE 
        WHEN table_type = 'TABLE' THEN 'Table'
        WHEN table_type = 'VIEW' THEN 'View'
        ELSE table_type
    END as type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.TABLES`
WHERE table_name IN ('bq_weekly_messages_devices', 'bq_weekly_messages_metrics', 'bq_playbook_hub_metrics')
ORDER BY table_name;

-- Check table schemas (run each separately for each table)
-- SELECT column_name, data_type, is_nullable
-- FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
-- WHERE table_schema = 'Store_Support_Dev' AND table_name = 'bq_weekly_messages_devices'
-- ORDER BY ordinal_position;
