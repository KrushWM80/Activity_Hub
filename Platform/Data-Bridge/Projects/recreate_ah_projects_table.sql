-- ============================================================================
-- AH_Projects Table Recreation SQL
-- Purpose: Drop existing table and recreate with updated 48-column schema
-- Source: projects-schema.json (updated April 17, 2026)
-- Target: wmt-assetprotection-prod.Store_Support_Dev.AH_Projects
-- ============================================================================

-- Step 1: BACKUP existing data (optional - creates snapshot)
-- Note: Run this first if you want to preserve historical data
/*
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects_BACKUP_20260417` AS
SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`;
*/

-- Step 2: DROP existing table
DROP TABLE IF EXISTS `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`;

-- Step 3: CREATE new table with updated 48-column schema
CREATE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` (
  -- IDENTIFIERS (3 fields)
  project_id STRING NOT NULL,
  intake_card STRING,
  title STRING NOT NULL,
  
  -- STATUS (4 fields)
  status STRING,
  phase STRING,
  health STRING,
  project_source STRING NOT NULL,
  
  -- LOCATION (12 fields)
  division STRING,
  region STRING,
  market STRING,
  facility STRING,
  store_count INT64,
  city STRING,
  state STRING,
  postal_code STRING,
  latitude FLOAT64,
  longitude FLOAT64,
  store_area STRING,
  business_area STRING,
  
  -- TIME (7 fields)
  created_date TIMESTAMP,
  last_updated TIMESTAMP,
  projected_completion DATE,
  wm_week INT64,
  fiscal_year INT64,
  implementation_week STRING,
  projected_start_date DATE,
  
  -- OWNERSHIP (6 fields)
  owner STRING,
  owner_id STRING,
  director STRING,
  director_id STRING,
  sr_director STRING,
  sr_director_id STRING,
  
  -- CATEGORIZATION (6 fields)
  project_type STRING,
  initiative_type STRING,
  business_type STRING,
  facility_type STRING,
  partner STRING,
  business_organization STRING,
  
  -- IMPACT (4 fields)
  associate_impact STRING,
  customer_impact STRING,
  ho_impact STRING,
  impact STRING,
  
  -- AMP_MEETING (5 fields)
  amp_event_id STRING,
  amp_activity_title STRING,
  meeting_type STRING,
  sif_date DATE,
  aim_date DATE,
  
  -- DESCRIPTION (3 fields)
  summary STRING,
  overview STRING,
  project_update STRING
)
OPTIONS(
  description="Activity Hub Projects table - canonical 48-column schema aligned with Intake Hub data",
  labels=[("managed_by", "activity_hub"), ("data_source", "intake_hub"), ("last_updated", "2026-04-17")]
);

-- Step 4: Verify table creation
SELECT
  table_name,
  column_name,
  data_type,
  is_nullable,
  ordinal_position
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'AH_Projects'
ORDER BY ordinal_position;

-- ============================================================================
-- Result: New AH_Projects table ready for data loading
-- Next Step: Run intake_hub_to_ah_projects_loader.py to populate data
-- ============================================================================
