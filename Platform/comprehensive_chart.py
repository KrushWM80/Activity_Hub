#!/usr/bin/env python3
"""
Create comprehensive weekly/daily comparison chart from available data (2/23 onwards)
"""

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 160)
print('COMPREHENSIVE STORE REFRESH PROGRESS - WK7 (2/23) THROUGH WK8+ (3/5)')
print('=' * 160 + '\n')

# Format-specific baseline (constant)
baseline_sc = 3555 * 328      # 1,166,040
baseline_div1 = 366 * 327     # 119,682
baseline_nhm = 674 * 209      # 140,866
baseline_total = baseline_sc + baseline_div1 + baseline_nhm  # 1,426,588

print(f"📊 FORMAT-SPECIFIC BASELINE: {baseline_total:,} max items")
print(f"   SC (3,555 stores × 328 Q): {baseline_sc:,}")
print(f"   DIV1 (366 stores × 327 Q): {baseline_div1:,}")
print(f"   NHM (674 stores × 209 Q): {baseline_nhm:,}")
print()

# Query all dates
query = '''
SELECT
  DATE(exportDate) as export_date,
  COUNT(DISTINCT businessUnitNumber) as store_count,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
  COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending,
  COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned,
  COUNT(*) as total_records
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) >= '2026-02-23'
GROUP BY
  DATE(exportDate)
ORDER BY
  export_date ASC
'''

try:
    results = list(client.query(query).result())
    
    # Map to week labels
    date_to_week = {
        '2026-02-23': 'WK7',
        '2026-02-24': 'WK7+1',
        '2026-02-25': 'WK7+2',
        '2026-02-26': 'WK7+3',
        '2026-02-27': 'WK7+4',
        '2026-02-28': 'WK8',
        '2026-03-01': 'WK8+1',
        '2026-03-02': 'WK8+2',
        '2026-03-03': 'WK8+3',
        '2026-03-04': 'WK8+4',
        '2026-03-05': 'WK8+5',
    }
    
    print()
    print('=' * 160)
    print('DETAILED METRICS TABLE')
    print('=' * 160)
    print()
    
    print(f"{'Week':<12} {'Date':<12} {'Stores':<10} {'Max Poss':<12} | {'Unassigned':<12} {'Assigned':<12} {'%Assign':<9} | {'Completed':<12} {'%Comp':<9}")
    print('-' * 160)
    
    for row in results:
        date_str = str(row.export_date)
        week = date_to_week.get(date_str, date_str)
        
        stores = row.store_count
        completed = row.completed
        pending = row.pending
        unassigned = row.unassigned
        assigned = completed + pending
        
        pct_assigned = (assigned / baseline_total * 100) if baseline_total > 0 else 0
        pct_completed = (completed / assigned * 100) if assigned > 0 else 0
        
        print(f"{week:<12} {date_str:<12} {stores:<10,} {baseline_total:<12,} | {unassigned:<12,} {assigned:<12,} {pct_assigned:<9.1f}% | {completed:<12,} {pct_completed:<9.1f}%")
    
    print()
    print()
    
    # ========================================================================
    # WEEKLY SUMMARY (Key snapshots)
    # ========================================================================
    print('=' * 160)
    print('WEEKLY SUMMARY - KEY DATES')
    print('=' * 160)
    print()
    
    # Get specific week data
    wk7_data = results[0]  # 2/23
    wk8_data = next((r for r in results if str(r.export_date) == '2026-02-28'), None)
    latest_data = results[-1]  # Latest
    
    print(f"{'Metric':<30} {'WK7 (2/23)':<20} {'WK8 (2/28)':<20} {'Latest (3/5)':<20}")
    print('-' * 160)
    
    def get_date_data(target_date_str):
        for r in results:
            if str(r.export_date) == target_date_str:
                return r
        return None
    
    wk7 = get_date_data('2026-02-23')
    wk8 = get_date_data('2026-02-28')
    latest = get_date_data('2026-03-05')
    
    for r, label in [(wk7, 'WK7'), (wk8, 'WK8'), (latest, 'Latest')]:
        if r is None:
            continue
    
    # Store count
    print(f"{'Store Count':<30} {wk7.store_count:<20,} {wk8.store_count:<20,} {latest.store_count:<20,}")
    
    # Max possible (constant)
    print(f"{'Max Possible (Baseline)':<30} {baseline_total:<20,} {baseline_total:<20,} {baseline_total:<20,}")
    
    # Unassigned
    print(f"{'Unassigned':<30} {wk7.unassigned:<20,} {wk8.unassigned:<20,} {latest.unassigned:<20,}")
    
    # Assigned (C+P)
    wk7_assigned = wk7.completed + wk7.pending
    wk8_assigned = wk8.completed + wk8.pending
    latest_assigned = latest.completed + latest.pending
    print(f"{'Assigned (C+P)':<30} {wk7_assigned:<20,} {wk8_assigned:<20,} {latest_assigned:<20,}")
    
    # Completed
    print(f"{'Completed':<30} {wk7.completed:<20,} {wk8.completed:<20,} {latest.completed:<20,}")
    
    # Percentages
    print()
    wk7_pct_assign = (wk7_assigned / baseline_total * 100)
    wk8_pct_assign = (wk8_assigned / baseline_total * 100)
    latest_pct_assign = (latest_assigned / baseline_total * 100)
    print(f"{'% Assigned of Max':<30} {wk7_pct_assign:<20.1f}% {wk8_pct_assign:<20.1f}% {latest_pct_assign:<20.1f}%")
    
    wk7_pct_comp = (wk7.completed / wk7_assigned * 100) if wk7_assigned > 0 else 0
    wk8_pct_comp = (wk8.completed / wk8_assigned * 100) if wk8_assigned > 0 else 0
    latest_pct_comp = (latest.completed / latest_assigned * 100) if latest_assigned > 0 else 0
    print(f"{'% Completed of Assigned':<30} {wk7_pct_comp:<20.1f}% {wk8_pct_comp:<20.1f}% {latest_pct_comp:<20.1f}%")
    
    print()
    print()
    
    # ========================================================================
    # PROGRESS ANALYSIS
    # ========================================================================
    print('=' * 160)
    print('PROGRESS ANALYSIS - WK7 TO WK8 TO LATEST')
    print('=' * 160)
    print()
    
    print(f"WK7 (2/23/26) → WK8 (2/28/26) [5 days]:")
    print(f"  Stores:     {wk7.store_count:,} → {wk8.store_count:,} ({(wk8.store_count - wk7.store_count):+,})")
    print(f"  Assigned:   {wk7_assigned:,} → {wk8_assigned:,} ({(wk8_assigned - wk7_assigned):+,})")
    print(f"  Completed:  {wk7.completed:,} → {wk8.completed:,} ({(wk8.completed - wk7.completed):+,})")
    print(f"  Completion %: {wk7_pct_comp:.1f}% → {wk8_pct_comp:.1f}% ({(wk8_pct_comp - wk7_pct_comp):+.1f}pp)")
    print()
    
    print(f"WK8 (2/28/26) → Latest (3/5/26) [5 days]:")
    print(f"  Stores:     {wk8.store_count:,} → {latest.store_count:,} ({(latest.store_count - wk8.store_count):+,})")
    print(f"  Assigned:   {wk8_assigned:,} → {latest_assigned:,} ({(latest_assigned - wk8_assigned):+,})")
    print(f"  Completed:  {wk8.completed:,} → {latest.completed:,} ({(latest.completed - wk8.completed):+,})")
    print(f"  Completion %: {wk8_pct_comp:.1f}% → {latest_pct_comp:.1f}% ({(latest_pct_comp - wk8_pct_comp):+.1f}pp)")
    print()
    
    print('=' * 160)
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()
