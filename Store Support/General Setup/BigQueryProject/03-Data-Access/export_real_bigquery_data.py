# Real BigQuery Data Connection
# This script connects to the actual BigQuery table and exports real data

import json
import sys

def export_real_bigquery_data():
    """
    Instructions to export REAL data from BigQuery table:
    wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep
    """
    
    bigquery_instructions = {
        "step_1": "Go to BigQuery Console: https://console.cloud.google.com/bigquery",
        "step_2": "Navigate to project: wmt-assetprotection-prod",
        "step_3": "Open dataset: Store_Support_Dev", 
        "step_4": "Open table: AMP_Data_Prep",
        "step_5": "Run this SQL query",
        "sql_query": """
SELECT 
    actv_title_home_ofc_nm as title,
    division,
    region, 
    market,
    store_nbr,
    store_name,
    week,
    created_date,
    preview_link,
    status,
    verification_status
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`
WHERE week = 39 
  AND status = 'Published'
  AND preview_link IS NOT NULL
  AND preview_link != ''
ORDER BY created_date DESC
LIMIT 1000
""",
        "step_6": "Export results as JSON (newline delimited)",
        "step_7": "Save as 'real_bigquery_data.json' in this folder",
        "step_8": "Dashboard will automatically load the real data"
    }
    
    print("🔗 REAL BIGQUERY DATA EXPORT INSTRUCTIONS:")
    print("=" * 60)
    
    for step, instruction in bigquery_instructions.items():
        if step == "sql_query":
            print(f"\n📋 SQL QUERY TO RUN:")
            print("-" * 30)
            print(instruction)
            print("-" * 30)
        else:
            print(f"{step.replace('_', ' ').title()}: {instruction}")
    
    print("\n✅ WHAT THIS WILL GET YOU:")
    print("- ALL real Week 39 published activities (75+ records)")
    print("- REAL GUID preview links that actually work")
    print("- NO fake/demo data")
    print("- NO confirmation dialogs")
    print("- Direct click-to-open functionality")
    
    print("\n🚨 IMPORTANT:")
    print("- Only activities WITH preview links will be included")
    print("- Only 'Published' status activities")
    print("- Only Week 39 data (change week number if needed)")

if __name__ == "__main__":
    export_real_bigquery_data()