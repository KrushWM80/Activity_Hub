#!/usr/bin/env python3
"""
Week 7 (2/23-2/28/26) Data Extraction - CORRECTED METHOD
Using Store Format × Question Count Matrix
================================

Correct Methodology:
- SC: 3,555 stores × 328 questions = 1,166,040 maxPossible
- DIV1: 366 stores × 327 questions = 119,682 maxPossible
- NHM: 674 stores × 209 questions = 140,866 maxPossible
- TOTAL POSSIBLE: 1,677,600 items

This script extracts actual assigned/completed counts for Week 7
and reports them against the correct possible baseline.
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='athena-gateway-prod')

# Week 7 export date (single snapshot date)
WEEK_7_DATE = '2026-02-23'

# Store Format Constants (from knowledge base)
FORMAT_STRUCTURE = {
    'SC': {'stores': 3555, 'questions': 328, 'maxPossible': 1166040},
    'DIV1': {'stores': 366, 'questions': 327, 'maxPossible': 119682},
    'NHM': {'stores': 674, 'questions': 209, 'maxPossible': 140866},
}

TOTAL_POSSIBLE_ITEMS = sum(f['maxPossible'] for f in FORMAT_STRUCTURE.values())

print("=" * 80)
print("WEEK 7 DATA EXTRACTION (2/23/26) - CORRECTED METHOD")
print("=" * 80)
print()

# ============================================================================
# 1. OVERALL SUMMARY
# ============================================================================
print("[1/5] Extracting OVERALL SUMMARY...")

summary_query = """
SELECT
  COUNT(DISTINCT businessUnitNumber) as storesWithAssignments,
  COUNT(CASE WHEN assignedTo IS NOT NULL THEN 1 END) as totalAssignedItems,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as totalCompletedItems
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = @export_date
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("export_date", "DATE", WEEK_7_DATE),
    ]
)

summary_results = client.query(summary_query, job_config=job_config).result()
for row in summary_results:
    stores_with_assignments = row.storesWithAssignments or 0
    total_assigned = row.totalAssignedItems or 0
    total_completed = row.totalCompletedItems or 0
    
    assigned_pct = (total_assigned / TOTAL_POSSIBLE_ITEMS * 100) if TOTAL_POSSIBLE_ITEMS > 0 else 0
    completed_pct = (total_completed / TOTAL_POSSIBLE_ITEMS * 100) if TOTAL_POSSIBLE_ITEMS > 0 else 0
    
    print(f"✓ Overview Stats:")
    print(f"  - Stores with Assignments: {stores_with_assignments:,}")
    print(f"  - Total Possible Items (Correct): {TOTAL_POSSIBLE_ITEMS:,}")
    print(f"  - Total Assigned Items: {total_assigned:,} ({assigned_pct:.1f}% of possible)")
    print(f"  - Total Completed Items: {total_completed:,} ({completed_pct:.1f}% of possible)")
    print()

# ============================================================================
# 2. FORMAT STATS
# ============================================================================
print("[2/5] Extracting FORMAT STATS...")

format_query = """
SELECT
  storeFormat,
  COUNT(CASE WHEN assignedTo IS NOT NULL THEN 1 END) as assignedCount,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completedCount
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = @export_date
GROUP BY
  storeFormat
ORDER BY
  storeFormat
"""

format_results = client.query(format_query, job_config=job_config).result()
format_stats = {}

print("  Format Breakdown:")
for row in format_results:
    fmt = row.storeFormat or 'UNKNOWN'
    assigned = row.assignedCount or 0
    completed = row.completedCount or 0
    
    if fmt in FORMAT_STRUCTURE:
        max_possible = FORMAT_STRUCTURE[fmt]['maxPossible']
        assigned_pct = (assigned / max_possible * 100) if max_possible > 0 else 0
        completed_pct = (completed / max_possible * 100) if max_possible > 0 else 0
        
        format_stats[fmt] = {
            'storeCount': FORMAT_STRUCTURE[fmt]['stores'],
            'assignedCount': assigned,
            'completedCount': completed,
            'maxPossibleCount': max_possible,
            'completionPercentage': round(completed_pct, 1),
            'assignedPercentage': round(assigned_pct, 1)
        }
        
        print(f"    {fmt}: {assigned:,} assigned ({assigned_pct:.1f}%), {completed:,} completed ({completed_pct:.1f}%)")
    else:
        print(f"    {fmt}: {assigned:,} assigned, {completed:,} completed [NOT IN MATRIX - May indicate data issue]")

print()

# ============================================================================
# 3. DIVISION STATS
# ============================================================================
print("[3/5] Extracting DIVISION STATS...")

division_query = """
SELECT
  businessUnitNumber as divisionId,
  COUNT(CASE WHEN assignedTo IS NOT NULL THEN 1 END) as assignedCount,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completedCount
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = @export_date
  AND businessUnitNumber IS NOT NULL
GROUP BY
  businessUnitNumber
ORDER BY
  businessUnitNumber
"""

division_results = client.query(division_query, job_config=job_config).result()
division_stats = []

print("  Division Breakdown:")
for row in division_results:
    div = row.divisionId or 'UNKNOWN'
    assigned = row.assignedCount or 0
    completed = row.completedCount or 0
    
    division_stats.append({
        'divisionId': div,
        'assignedCount': assigned,
        'completedCount': completed
    })
    
    print(f"    {div}: {assigned:,} assigned, {completed:,} completed")

print()

# ============================================================================
# 4. DATA VALIDATION
# ============================================================================
print("[4/5] DATA VALIDATION...")
print()
print("  Sanity Checks:")
print(f"  ✓ Total Possible Items (Formula): {TOTAL_POSSIBLE_ITEMS:,}")
print(f"    = SC(3555×328) + DIV1(366×327) + NHM(674×209)")
print(f"    = {FORMAT_STRUCTURE['SC']['maxPossible']:,} + {FORMAT_STRUCTURE['DIV1']['maxPossible']:,} + {FORMAT_STRUCTURE['NHM']['maxPossible']:,}")

format_totals = {
    'assigned': sum(s['assignedCount'] for s in format_stats.values()),
    'completed': sum(s['completedCount'] for s in format_stats.values())
}

print()
print(f"  Format Totals:")
print(f"    - Assigned: {format_totals['assigned']:,}")
print(f"    - Completed: {format_totals['completed']:,}")

div_totals = {
    'assigned': sum(d['assignedCount'] for d in division_stats),
    'completed': sum(d['completedCount'] for d in division_stats)
}

print()
print(f"  Division Totals:")
print(f"    - Assigned: {div_totals['assigned']:,}")
print(f"    - Completed: {div_totals['completed']:,}")

print()

# ============================================================================
# 5. FINAL JSON OUTPUT
# ============================================================================
print("[5/5] Building JSON Structure...")

week7_data = {
    "week": 7,
    "date": WEEK_7_DATE,
    "summary": {
        "storesWithAssignments": stores_with_assignments,
        "totalPossibleItems": TOTAL_POSSIBLE_ITEMS,
        "totalAssignedItems": total_assigned,
        "totalCompletedItems": total_completed,
        "overallCompletionOfMax": round((total_completed / TOTAL_POSSIBLE_ITEMS * 100), 1) if TOTAL_POSSIBLE_ITEMS > 0 else 0
    },
    "formatStats": [
        {
            "format": fmt,
            **stats
        }
        for fmt, stats in sorted(format_stats.items())
    ],
    "divisionStats": division_stats
}

print()
print("=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print()
print(json.dumps(week7_data, indent=2))
print()
print("=" * 80)
print(f"Ready to embed into dashboard!")
print("=" * 80)
