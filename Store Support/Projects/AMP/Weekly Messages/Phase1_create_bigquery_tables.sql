# BigQuery Setup Script for Adobe Analytics Pipeline
# Path: Store Support\Projects\AMP\Weekly Messages\Phase1_create_bigquery_tables.sql
#
# Instructions:
# 1. Open BigQuery Console: https://console.cloud.google.com/bigquery
# 2. Set project to: wmt-assetprotection-prod
# 3. Copy and paste each CREATE statement below into the query editor
# 4. Run each query
#
# Alternative: Run via gcloud CLI
#   bq mk --dataset --location=US wmt-assetprotection-prod:Weekly_Message_FY27
#   bq mk --dataset --location=US wmt-assetprotection-prod:Playbook_Hub_Data
#   (Then run the CREATE TABLE statements)

-- ============================================================================
-- STEP 1: CREATE DATASETS
-- ============================================================================

-- Create Dataset 1: Weekly_Message_FY27
CREATE SCHEMA IF NOT EXISTS `wmt-assetprotection-prod.Weekly_Message_FY27`
OPTIONS(
  description="Adobe Analytics Weekly Messages FY27 data",
  location="US"
);

-- Create Dataset 2: Playbook_Hub_Data
CREATE SCHEMA IF NOT EXISTS `wmt-assetprotection-prod.Playbook_Hub_Data`
OPTIONS(
  description="Adobe Analytics Playbook Hub data",
  location="US"
);

-- ============================================================================
-- STEP 2: CREATE TABLES
-- ============================================================================

-- Table 1: Weekly Messages - Device Level Page Views
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`
PARTITION BY report_date
CLUSTER BY category, page_name
OPTIONS(
  description="Weekly Messages device-level page views by category",
  require_partition_filter=FALSE
) AS
SELECT
  CAST(NULL AS DATE) as report_date,
  CAST(NULL AS STRING) as category,
  CAST(NULL AS STRING) as page_name,
  CAST(NULL AS INT64) as tablets_page_views,
  CAST(NULL AS INT64) as desktop_page_views,
  CAST(NULL AS INT64) as store_devices_page_views,
  CAST(NULL AS INT64) as mobile_phones_page_views,
  CAST(NULL AS INT64) as xcover_devices_page_views,
  CAST(NULL AS INT64) as total_page_views,
  CAST(NULL AS TIMESTAMP) as extracted_date
WHERE FALSE;

-- Table 2: Weekly Messages - Aggregated Metrics
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_metrics`
PARTITION BY report_date
CLUSTER BY category, page_name
OPTIONS(
  description="Weekly Messages aggregated metrics: page views, unique users, time, visits",
  require_partition_filter=FALSE
) AS
SELECT
  CAST(NULL AS DATE) as report_date,
  CAST(NULL AS STRING) as category,
  CAST(NULL AS STRING) as page_name,
  CAST(NULL AS INT64) as page_views,
  CAST(NULL AS FLOAT64) as unique_users,
  CAST(NULL AS FLOAT64) as average_time_on_site,
  CAST(NULL AS INT64) as visits,
  CAST(NULL AS TIMESTAMP) as extracted_date
WHERE FALSE;

-- Table 3: Playbook Hub - Playbook Metrics
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Playbook_Hub_Data.bq_playbook_hub_metrics`
PARTITION BY report_date
CLUSTER BY playbook_category
OPTIONS(
  description="Playbook Hub page views by user type (Salary/Hourly Associates)",
  require_partition_filter=FALSE
) AS
SELECT
  CAST(NULL AS DATE) as report_date,
  CAST(NULL AS STRING) as playbook_category,
  CAST(NULL AS STRING) as page_name,
  CAST(NULL AS INT64) as total_page_views,
  CAST(NULL AS INT64) as store_salary_associates_views,
  CAST(NULL AS INT64) as store_hourly_associates_views,
  CAST(NULL AS DATE) as report_period_start,
  CAST(NULL AS DATE) as report_period_end,
  CAST(NULL AS TIMESTAMP) as extracted_date
WHERE FALSE;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check Dataset 1 Existence
SELECT schema_name, description
FROM `wmt-assetprotection-prod.region-us`.INFORMATION_SCHEMA.SCHEMATA
WHERE schema_name IN ('Weekly_Message_FY27', 'Playbook_Hub_Data');

-- Check Table 1
SELECT table_name, row_count, type_name
FROM `wmt-assetprotection-prod.Weekly_Message_FY27`.INFORMATION_SCHEMA.TABLES
WHERE table_name = 'bq_weekly_messages_devices';

-- Check Table 2
SELECT table_name, row_count, type_name
FROM `wmt-assetprotection-prod.Weekly_Message_FY27`.INFORMATION_SCHEMA.TABLES
WHERE table_name = 'bq_weekly_messages_metrics';

-- Check Table 3
SELECT table_name, row_count, type_name
FROM `wmt-assetprotection-prod.Playbook_Hub_Data`.INFORMATION_SCHEMA.TABLES
WHERE table_name = 'bq_playbook_hub_metrics';

-- ============================================================================
-- SAMPLE VALIDATION QUERIES (After first data load)
-- ============================================================================

-- Sample: Check today's device data
-- SELECT report_date, category, COUNT(*) as row_count, SUM(total_page_views) as total_views
-- FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`
-- WHERE DATE(extracted_date) = CURRENT_DATE()
-- GROUP BY report_date, category
-- ORDER BY category;

-- Sample: Check paybook data
-- SELECT playbook_category, COUNT(*) as row_count, SUM(total_page_views) as total_views
-- FROM `wmt-assetprotection-prod.Playbook_Hub_Data.bq_playbook_hub_metrics`
-- WHERE DATE(extracted_date) = CURRENT_DATE()
-- GROUP BY playbook_category;
