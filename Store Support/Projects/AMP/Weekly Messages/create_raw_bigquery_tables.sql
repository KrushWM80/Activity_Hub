-- BigQuery DDL: Create Raw Data Tables
-- Purpose: Store Adobe Analytics data in exact Excel format

-- Playbook Hub Raw Data Table
-- Columns: F1, F2, F3, F4 (STRING)
-- Stores all rows from Excel file exactly as-is
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.bq_playbook_hub_raw` (
    F1 STRING,
    F2 STRING,
    F3 STRING,
    F4 STRING,
    extracted_date TIMESTAMP NOT NULL
)
PARTITION BY DATE(extracted_date)
CLUSTER BY F1
OPTIONS(
    description="Playbook Hub raw data - exact Excel format with metadata",
    labels=[("source", "adobe_analytics"), ("format", "raw")]
);

-- Weekly Messages Raw Data Table
-- Columns: F1, F2, F3, F4, F5, F6 (STRING)
-- Stores all rows from Excel file exactly as-is
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.bq_weekly_messages_raw` (
    F1 STRING,
    F2 STRING,
    F3 STRING,
    F4 STRING,
    F5 STRING,
    F6 STRING,
    extracted_date TIMESTAMP NOT NULL
)
PARTITION BY DATE(extracted_date)
CLUSTER BY F1
OPTIONS(
    description="Weekly Messages raw data - exact Excel format with metadata",
    labels=[("source", "adobe_analytics"), ("format", "raw")]
);
