#!/usr/bin/env python3
"""
Verify WM WK 12 counts after cleanup
"""

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

# WM Week 12: April 18-24, 2026
# Calculate which projects fall in this range
query = """
SELECT 
    COUNT(DISTINCT project_id) as total_wk12,
    COUNT(CASE WHEN project_update_date IS NULL THEN 1 END) as null_count,
    COUNT(CASE WHEN project_update_date IS NOT NULL THEN 1 END) as with_dates,
    MIN(project_update_date) as earliest_date,
    MAX(project_update_date) as latest_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NULL
   OR (project_update_date >= TIMESTAMP('2026-04-18') AND project_update_date < TIMESTAMP('2026-04-25'))
"""

results = client.query(query).result()

for row in results:
    print("\n" + "="*80)
    print("WM WEEK 12 (April 18-24, 2026) - AH_Projects After Cleanup")
    print("="*80)
    print(f"Total projects in WK12 range: {row.total_wk12}")
    print(f"  - With dates in range: {row.with_dates}")
    print(f"  - With NULL dates: {row.null_count}")
    print(f"Earliest update: {row.earliest_date}")
    print(f"Latest update: {row.latest_date}")
    print("="*80)
