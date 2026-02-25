#!/usr/bin/env python3
"""
EXTRACTION SCRIPT: Week 7 Division, Format, and Area Breakdown
This script generates the correct division/format/area completed counts for Week 7
that must sum to 1,111,851 (the verified total)
"""

from google.cloud import bigquery
from datetime import datetime

def extract_week7_breakdown():
    """Extract Week 7 breakdowns by division, format, and area."""
    
    week7_export_date = "2026-02-23"
    
    print("=" * 80)
    print("WEEK 7 DETAILED BREAKDOWN EXTRACTION")
    print("=" * 80)
    print(f"\nTarget Date: {week7_export_date}")
    print("Expected Total: 1,111,851 completed items\n")
    
    try:
        client = bigquery.Client(project='wmt-assetprotection-prod')
    except Exception as e:
        print(f"❌ BigQuery connection failed: {e}")
        return None
    
    # ============================================================================
    # EXTRACTION 1: BY DIVISION
    # ============================================================================
    print("\n" + "=" * 80)
    print("EXTRACTING: DIVISION BREAKDOWN")
    print("=" * 80)
    
    division_query = """
    SELECT
        businessUnitNumber as divisionId,
        COUNT(DISTINCT businessUnitNumber) as storeCount,
        COUNT(*) as totalRecords,
        COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completedCount,
        COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pendingCount
    FROM `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE DATE(exportDate) = @export_date
    GROUP BY businessUnitNumber
    ORDER BY completedCount DESC
    LIMIT 10
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("export_date", "DATE", week7_export_date),
        ]
    )
    
    try:
        print("\n📊 Querying by Division...")
        results = client.query(division_query, job_config=job_config).result()
        division_totals = []
        rows = list(results)
        
        for i, row in enumerate(rows, 1):
            print(f"\n{i}. Division {row['divisionId']}:")
            print(f"   Store Count: {row['storeCount']:,}")
            print(f"   Completed Items: {row['completedCount']:,}")
            print(f"   Pending Items: {row['pendingCount']:,}")
            division_totals.append(int(row['completedCount']))
        
        division_sum = sum(division_totals)
        print(f"\n✅ Total From Divisions: {division_sum:,}")
        print(f"   Expected: 1,111,851")
        print(f"   Match: {'✅ YES' if division_sum == 1111851 else '❌ NO - Difference: ' + str(1111851 - division_sum)}")
        
    except Exception as e:
        print(f"❌ Division query failed: {e}")
        return None
    
    # ============================================================================
    # EXTRACTION 2: BY FORMAT (SC, DIV1, NHM)
    # ============================================================================
    print("\n\n" + "=" * 80)
    print("EXTRACTING: FORMAT BREAKDOWN (SC, DIV1, NHM)")
    print("=" * 80)
    
    format_query = """
    SELECT
        'SC' as format,
        COUNT(CASE WHEN status = 'COMPLETED' AND storeFormat = 'SC' THEN 1 END) as completedCount
    UNION ALL
    SELECT
        'DIV1' as format,
        COUNT(CASE WHEN status = 'COMPLETED' AND storeFormat = 'DIV1' THEN 1 END)
    UNION ALL
    SELECT
        'NHM' as format,
        COUNT(CASE WHEN status = 'COMPLETED' AND storeFormat = 'NHM' THEN 1 END)
    FROM `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE DATE(exportDate) = @export_date
    """
    
    try:
        print("\n📊 Querying by Format (SC/DIV1/NHM)...")
        results = client.query(format_query, job_config=job_config).result()
        format_totals = {}
        
        for row in results:
            format_name = row['format']
            completed = int(row['completedCount'])
            format_totals[format_name] = completed
            print(f"\n{format_name}:")
            print(f"   Completed Items: {completed:,}")
        
        format_sum = sum(format_totals.values())
        print(f"\n✅ Total From Formats: {format_sum:,}")
        print(f"   Expected: 1,111,851")
        print(f"   Match: {'✅ YES' if format_sum == 1111851 else '❌ NO - Difference: ' + str(1111851 - format_sum)}")
        
    except Exception as e:
        print(f"❌ Format query failed: {e}")
        return None
    
    # ============================================================================
    # EXTRACTION 3: BY AREA (8 store areas)
    # ============================================================================
    print("\n\n" + "=" * 80)
    print("EXTRACTING: AREA BREAKDOWN (8 store areas)")
    print("=" * 80)
    
    area_query = """
    SELECT
        storeArea as area,
        COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completedCount,
        COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pendingCount
    FROM `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE DATE(exportDate) = @export_date
    GROUP BY storeArea
    ORDER BY area
    """
    
    try:
        print("\n📊 Querying by Area...")
        results = client.query(area_query, job_config=job_config).result()
        area_totals = {}
        rows = list(results)
        
        for i, row in enumerate(rows, 1):
            area_name = row['area'] or 'UNKNOWN'
            completed = int(row['completedCount'])
            area_totals[area_name] = completed
            print(f"\n{i}. {area_name}:")
            print(f"   Completed Items: {completed:,}")
            print(f"   Pending Items: {int(row['pendingCount']):,}")
        
        area_sum = sum(area_totals.values())
        print(f"\n✅ Total From Areas: {area_sum:,}")
        print(f"   Expected: 1,111,851")
        print(f"   Match: {'✅ YES' if area_sum == 1111851 else '❌ NO - Difference: ' + str(1111851 - area_sum)}")
        
    except Exception as e:
        print(f"❌ Area query failed: {e}")
        return None
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    
    print(f"\n✅ Total Completions (Verified): 1,111,851")
    print(f"   Division Breakdown Sum: {division_sum:,} ({division_sum/1111851*100:.1f}%)")
    print(f"   Format Breakdown Sum: {format_sum:,} ({format_sum/1111851*100:.1f}%)")
    print(f"   Area Breakdown Sum: {area_sum:,} ({area_sum/1111851*100:.1f}%)")
    
    if division_sum == 1111851 and format_sum == 1111851 and area_sum == 1111851:
        print("\n✅ ALL BREAKDOWNS VERIFIED AND MATCH TOTAL!")
    else:
        print("\n⚠️  WARNING: Breakdowns do not match total - investigate data inconsistency")
    
    print("\n" + "=" * 80)
    print("OUTPUT: Copy the extracted values above into Week 7 dashboard")
    print("=" * 80)
    
    return {
        'divisions': division_totals,
        'formats': format_totals,
        'areas': area_totals
    }


if __name__ == "__main__":
    print("\n🔍 Starting Week 7 breakdown extraction...\n")
    data = extract_week7_breakdown()
    
    if data:
        print("\n✅ Extraction complete")
    else:
        print("\n❌ Extraction failed")
