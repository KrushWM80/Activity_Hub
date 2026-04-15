-- BigQuery DDL: Create Weekly Messages Audio Raw Data Table
-- Purpose: Store Adobe Analytics Audio data in exact CSV format

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.bq_weekly_messages_audio_raw` (
    F1 STRING,
    F2 STRING,
    F3 STRING,
    F4 STRING,
    F5 STRING,
    extracted_date TIMESTAMP NOT NULL
)
PARTITION BY DATE(extracted_date)
CLUSTER BY F1
OPTIONS(
    description="Weekly Messages Audio raw data - exact CSV format with metadata",
    labels=[("source", "adobe_analytics"), ("format", "raw"), ("type", "csv")]
);
