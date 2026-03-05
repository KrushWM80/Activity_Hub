#!/usr/bin/env python3
"""
Investigate what definition WK7 was actually using
Query 2/23 data for status breakdown
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 120)
print('INVESTIGATING WK7 DEFINITION - WHAT WAS IT ACTUALLY USING?')
print('=' * 120 + '\n')

# ============================================================================
# WK7 DATE (2/23/26) STATUS BREAKDOWN
# ============================================================================
print('📊 WK7 (2/23/26) DATA FROM BIGQUERY')
print('-' * 120)

status_query_2_23 = '''
SELECT
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
  COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending,
  COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned,
  COUNT(*) as total_records,
  COUNT(DISTINCT businessUnitNumber) as store_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
'''

result_2_23 = list(client.query(status_query_2_23).result())[0]

completed_2_23 = result_2_23.completed
pending_2_23 = result_2_23.pending
unassigned_2_23 = result_2_23.unassigned
total_records_2_23 = result_2_23.total_records
stores_2_23 = result_2_23.store_count

print(f"  Status Breakdown on 2/23:")
print(f"    COMPLETED:    {completed_2_23:>12,} items")
print(f"    PENDING:      {pending_2_23:>12,} items")
print(f"    UnAssigned:   {unassigned_2_23:>12,} items")
print(f"    ─────────────────────────")
print(f"    TOTAL (all):  {total_records_2_23:>12,} items")
print()

# Calculate what different definitions would give
assigned_correct_2_23 = completed_2_23 + pending_2_23
total_minus_unassigned_2_23 = total_records_2_23 - unassigned_2_23

print(f"  Possible Definitions:")
print(f"    A) COMPLETED + PENDING:        {assigned_correct_2_23:>12,}")
print(f"    B) Total - UnAssigned:         {total_minus_unassigned_2_23:>12,}")
print(f"    C) Raw total records:          {total_records_2_23:>12,}")
print()

# WK7 dashboard value
wk7_dashboard_value = 1387578

print(f"  WK7 Dashboard Value:             {wk7_dashboard_value:>12,}")
print()

# Which definition does it match?
print('  Analysis:')
if wk7_dashboard_value == assigned_correct_2_23:
    print(f"    ✓ Matches COMPLETED + PENDING (correct)")
elif wk7_dashboard_value == total_minus_unassigned_2_23:
    print(f"    ✗ Matches Total - UnAssigned (INCORRECT)")
    print(f"      └─ This is likely what WK7 was using incorrectly!")
    print(f"      └─ Difference from correct: {wk7_dashboard_value - assigned_correct_2_23:,}")
elif wk7_dashboard_value == total_records_2_23:
    print(f"    ✗ Matches raw total records (VERY INCORRECT)")
else:
    print(f"    ? Does not match any standard definition")
    print(f"      └─ Closest match: Total - UnAssigned ({total_minus_unassigned_2_23:,})")
    print(f"      └─ Difference: {abs(wk7_dashboard_value - total_minus_unassigned_2_23):,}")

print()

# ============================================================================
# WK8 COMPARISON
# ============================================================================
print('=' * 120)
print('COMPARISON: WK7 Definition vs WK8 (Correct) Definition')
print('=' * 120)
print()

status_query_2_28 = '''
SELECT
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
  COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending,
  COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned,
  COUNT(*) as total_records
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
'''

result_2_28 = list(client.query(status_query_2_28).result())[0]

completed_2_28 = result_2_28.completed
pending_2_28 = result_2_28.pending
unassigned_2_28 = result_2_28.unassigned
total_records_2_28 = result_2_28.total_records

print(f"If WK7 used 'Total - UnAssigned' definition:")
print(f"  WK7 (2/23): Total - UnAssigned = {total_records_2_23:,} - {unassigned_2_23:,} = {total_minus_unassigned_2_23:,}")
print(f"  WK8 (2/28): Total - UnAssigned = {total_records_2_28:,} - {unassigned_2_28:,} = {total_records_2_28 - unassigned_2_28:,}")
print()

print(f"But CORRECT definition is 'COMPLETED + PENDING':")
print(f"  WK7 (2/23): COMPLETED + PENDING = {completed_2_23:,} + {pending_2_23:,} = {assigned_correct_2_23:,}")
print(f"  WK8 (2/28): COMPLETED + PENDING = {completed_2_28:,} + {pending_2_28:,} = {completed_2_28 + pending_2_28:,}")
print()

print('=' * 120)
print('🔍 ROOT CAUSE OF WK7 INCORRECT DEFINITION')
print('=' * 120)
print()

print("The issue:")
print(f"  • WK7 used: 'Total Records - UnAssigned' = {total_minus_unassigned_2_23:,}")
print(f"  • Correct:  'COMPLETED + PENDING' = {assigned_correct_2_23:,}")
print()

diff_wk7 = total_minus_unassigned_2_23 - assigned_correct_2_23
print(f"  • Difference: {diff_wk7:,} items")
print()

print("Why this is wrong:")
print(f"  'Total - UnAssigned' includes items that aren't truly 'assigned'")
print(f"  It's mathematically: {total_records_2_23:,} - {unassigned_2_23:,} = {total_minus_unassigned_2_23:,}")
print()
print(f"  But those {total_records_2_23:,} records include some records that are")
print(f"  neither COMPLETED, PENDING, nor properly assigned.")
print()
print(f"  Correct method counts only items that have an assignment status:")
print(f"  COMPLETED ({completed_2_23:,}) + PENDING ({pending_2_23:,}) = {assigned_correct_2_23:,}")
print()

print('=' * 120)
print('📋 SUMMARY')
print('=' * 120)
print()

print("WK7 Definition (INCORRECT):")
print(f"  totalAssignedItems = Total Records - UnAssigned")
print(f"  = {total_records_2_23:,} - {unassigned_2_23:,}")
print(f"  = {total_minus_unassigned_2_23:,}")
print()

print("WK8 Definition (CORRECT):")
print(f"  totalAssignedItems = COMPLETED + PENDING")
print(f"  = {completed_2_28:,} + {pending_2_28:,}")
print(f"  = {completed_2_28 + pending_2_28:,}")
print()

print("Why we're fixing it now:")
print("  The 'Total - UnAssigned' approach was treating the data differently")
print("  than the actual business definition of 'assigned'.")
print("  ASSIGNED items are those actively being worked (COMPLETED or PENDING),")
print("  not simply 'not unassigned'. The gap represents records that may be")
print("  in other states or represent placeholder/dummy data.")
print()
