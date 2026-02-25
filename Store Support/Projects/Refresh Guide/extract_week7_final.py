#!/usr/bin/env python3
"""
CORRECTED: Extract Week 7 (2/23/26) completed checklist items from BigQuery
Using the correct schema discovered: checklistQuestionId, status, exportDate, etc.
"""

from google.cloud import bigquery
from datetime import datetime

if __name__ == "__main__":
    print("=" * 70)
    print("CORRECTED WEEK 7 DATA EXTRACTION")
    print("=" * 70)
    
    try:
        client = bigquery.Client(project='wmt-assetprotection-prod')
    except Exception as e:
        print(f"❌ BigQuery connection failed: {e}")
        exit(1)
    
    # Week 7: 2/23/26 export date (latest snapshot of the week)
    week7_export_date = "2026-02-23"
    
    print(f"\n🔍 Extracting Week 7 data for export date: {week7_export_date}")
    
    # Corrected query using the actual schema fields
    query = """
    SELECT
        DATE(exportDate) as export_date,
        COUNT(*) as total_records,
        COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as total_completed_items,
        COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as total_pending_items,
        COUNT(DISTINCT businessUnitNumber) as store_count
    FROM `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE DATE(exportDate) = @export_date
    GROUP BY DATE(exportDate)
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("export_date", "DATE", week7_export_date),
        ]
    )
    
    try:
        print(f"\n📊 Executing BigQuery...".ljust(40))
        results = client.query(query, job_config=job_config).result()
        rows = list(results)
        
        if rows:
            row = rows[0]
            export_date = row['export_date']
            total_records = int(row['total_records']) or 0
            total_completed_items = int(row['total_completed_items']) or 0
            total_pending_items = int(row['total_pending_items']) or 0
            store_count = int(row['store_count']) or 0
            
            # Calculate completion percentage against max possible (1,677,600)
            max_possible_items = 1677600
            completion_pct = round((total_completed_items / max_possible_items) * 100, 1)
            
            print(f"✅ SUCCESS - Data retrieved!\n")
            print(f"   Export Date: {export_date}")
            print(f"   Total Records: {total_records:,}")
            print(f"   Total Store Units: {store_count:,}")
            print(f"   Total Pending Items: {total_pending_items:,}")
            print(f"\n   ✨ TOTAL COMPLETED ITEMS: {total_completed_items:,} ✨")
            print(f"   Completion %: {completion_pct}% (of {max_possible_items:,} max)")
            
            # Comparison with Week 6
            week6_completed = 1100127
            difference = total_completed_items - week6_completed
            if total_completed_items >= week6_completed:
                print(f"\n   ✅ VALID: {difference:,} more items completed than Week 6 ✅")
            else:
                print(f"\n   ❌ INVALID: {abs(difference):,} fewer items than Week 6 ❌")
            
            print("\n" + "=" * 70)
            print(f"🎯 CORRECT WEEK 7 totalCompletedItems VALUE: {total_completed_items:,}")
            print("=" * 70)
        else:
            print("❌ No data found for the week")
            print("   This could mean:")
            print("   - The exportDate 2026-02-23 has no records")
            print("   - Try a different date within the week (2026-02-16 through 2026-02-23)")
            exit(1)
            
    except Exception as e:
        print(f"❌ Query execution failed:")
        print(f"   {type(e).__name__}: {e}")
        exit(1)
