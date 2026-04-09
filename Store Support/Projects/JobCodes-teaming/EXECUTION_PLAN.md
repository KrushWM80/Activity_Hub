"""
NEXT STEPS: Execute BigQuery Pipeline

Created Files:
1. query_polaris_jobcodes.py    - Extract Polaris job codes (SMART format)
2. query_corehr_jobcodes.py     - Extract CoreHR employment data (Workday format)
3. join_engine.py               - Orchestrate joins: Polaris → Excel → TMS

EXECUTION SEQUENCE:
"""

# ============================================================================
# STEP 1: Extract Polaris Data
# ============================================================================

# Prerequisites:
#   - BigQuery authentication set up (gcloud auth or service account)
#   - google-cloud-bigquery library installed

# Command:
python query_polaris_jobcodes.py

# Output:
#   - polaris_job_codes_extracted.csv (271 SMART format codes)
#   - Console summary with record counts


# ============================================================================
# STEP 2: Extract CoreHR Data (Optional - for user/role context)
# ============================================================================

# Note: CoreHR stores Workday format codes (US-01-XXXX-XXXXXX), not SMART
#       If you only need job code enrichment, can skip this

# Command:
python query_corehr_jobcodes.py

# Output:
#   - corehr_job_codes_extracted.csv (employment history with Workday codes)
#   - Can be used for user/role lookup separate from job code join


# ============================================================================
# STEP 3: Execute Full Join Pipeline
# ============================================================================

# Prerequisites:
#   - polaris_job_codes_extracted.csv in workspace (from Step 1)
#   - Job_Code_Master_Table.xlsx in workspace (Excel enrichment)
#   - TMS Data (3).xlsx in workspace (organizational teaming)
#   - openpyxl installed (already confirmed working)

# Command:
python join_engine.py

# Process:
#   1. Loads Polaris (271 codes) - AUTHORITY
#   2. LEFT JOIN Excel enrichment (864 records) on job_code
#   3. LEFT JOIN TMS data (492 records) on job_code
#   4. Saves to: 
#      - enriched_job_codes.csv (flat file)
#      - jobcodes_cache.db (SQLite) → loaded by backend on startup

# Output Summary:
✓ Total codes enriched: 271 (all Polaris codes preserved)
✓ Excel matched: ~70-80% (will show in console)
✓ TMS matched: ~60-70% (will show in console)
✓ Unmatched codes: Will have NULL for enrichment columns


# ============================================================================
# STEP 4: Update Backend to Use Enriched Data
# ============================================================================

# In main.py (FastAPI startup):
#   - Instead of syncing from openpyxl directly
#   - Load enriched data from SQLite table 'enriched_job_codes'
#   - Populate API responses with all enrichment fields

# Key API Endpoint Update: /api/job-codes-master
#   Current fields: job_code, job_nm (from Polaris)
#   ADD fields (from Excel enrichment):
#     - category
#     - job_family
#     - pg_level
#     - [50 other Excel columns]
#   ADD fields (from TMS):
#     - teamName
#     - teamId
#     - baseDivisionCode
#     - bannerCode
#     - [other TMS fields]


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Q: "BigQuery authentication failed"
# A: Follow: https://cloud.google.com/docs/authentication/getting-started
#    Set environment variable: GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

# Q: "Excel file not found"
# A: Ensure Job_Code_Master_Table.xlsx is in workspace directory
#    Check file name case sensitivity

# Q: "Low match rate (< 50%)"
# A: Check job_code format consistency:
#    - Polaris: "1-995-710"
#    - Excel: Check if codes have spaces, different format
#    - Add logging to join_engine.py to debug mismatches

# Q: "Module not found: google.cloud"
# A: Install: pip install google-cloud-bigquery

# ============================================================================
# SUCCESS INDICATORS
# ============================================================================

✓ Step 1 Complete: polaris_job_codes_extracted.csv created with 271 records
✓ Step 3 Complete: enriched_job_codes.csv with 271 rows, 50+ columns
✓ Database populated: SELECT COUNT(*) FROM enriched_job_codes; returns 271
✓ Dashboard updates: API /job-codes-master includes all enrichment fields
✓ No NULL job codes: All 271 Polaris codes present (some fields may be NULL)

# ============================================================================
