#!/usr/bin/env python3
"""
Extract all weekly data WK1-WK8 for comprehensive comparison chart
"""

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 150)
print('COMPREHENSIVE WEEKLY COMPARISON CHART - WK1 THROUGH WK8')
print('=' * 150 + '\n')

# Define weeks
weeks = [
    {'num': 1, 'date': '2026-01-19', 'label': 'WK1 (1/19)'},
    {'num': 2, 'date': '2026-01-26', 'label': 'WK2 (1/26)'},
    {'num': 3, 'date': '2026-02-01', 'label': 'WK3 (2/1)'},
    {'num': 4, 'date': '2026-02-02', 'label': 'WK4 (2/2)'},
    {'num': 5, 'date': '2026-02-09', 'label': 'WK5 (2/9)'},
    {'num': 6, 'date': '2026-02-16', 'label': 'WK6 (2/16)'},
    {'num': 7, 'date': '2026-02-23', 'label': 'WK7 (2/23)'},
    {'num': 8, 'date': '2026-02-28', 'label': 'WK8 (2/28)'},
]

# Format-specific baseline (constant)
baseline_sc = 3555 * 328
baseline_div1 = 366 * 327
baseline_nhm = 674 * 209
baseline_total = baseline_sc + baseline_div1 + baseline_nhm

weekly_data = []

print("📊 Extracting data for all weeks...")
print()

for week in weeks:
    date_str = week['date']
    
    query = f'''
    SELECT
      COUNT(DISTINCT businessUnitNumber) as store_count,
      COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
      COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending,
      COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned,
      COUNT(*) as total_records
    FROM
      `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE
      DATE(exportDate) = '{date_str}'
    '''
    
    try:
        result = list(client.query(query).result())[0]
        
        store_count = result.store_count
        completed = result.completed
        pending = result.pending
        unassigned = result.unassigned
        assigned = completed + pending
        
        weekly_data.append({
            'week': week['num'],
            'label': week['label'],
            'date': date_str,
            'stores': store_count,
            'completed': completed,
            'pending': pending,
            'assigned': assigned,
            'unassigned': unassigned,
            'total_records': result.total_records
        })
        
        print(f"  ✓ {week['label']:12} : {store_count:>5,} stores | Completed: {completed:>10,} | Pending: {pending:>9,} | Assigned: {assigned:>10,}")
        
    except Exception as e:
        print(f"  ✗ {week['label']:12} : ERROR - {str(e)[:50]}")

print()
print()

# ============================================================================
# CREATE COMPREHENSIVE TABLE
# ============================================================================
print('=' * 150)
print('DETAILED WEEKLY METRICS TABLE')
print('=' * 150)
print()

# Header
print(f"{'Week':<8} {'Date':<12} {'Stores':<8} {'Max Poss':<12} {'Unassigned':<12} {'Assigned':<12} {'%Assign':<9} {'Completed':<12} {'%Comp':<9}")
print(f"{'':8} {'':12} {'':8} {'(Baseline)':<12} {'':12} {'C+P':<12} {'':9} {'':12} {'':9}")
print('-' * 150)

for data in weekly_data:
    stores = data['stores']
    assigned = data['assigned']
    completed = data['completed']
    unassigned = data['unassigned']
    
    pct_assigned = (assigned / baseline_total * 100) if baseline_total > 0 else 0
    pct_completed = (completed / assigned * 100) if assigned > 0 else 0
    
    print(f"WK{data['week']:<6} {data['date']:<12} {stores:<8,} {baseline_total:<12,} {unassigned:<12,} {assigned:<12,} {pct_assigned:<9.1f}% {completed:<12,} {pct_completed:<9.1f}%")

print()
print()

# ============================================================================
# FORMAT BREAKDOWN (if we can determine it)
# ============================================================================
print('=' * 150)
print('FORMAT-SPECIFIC BREAKDOWN')
print('=' * 150)
print()

print(f"{'':30} {'SC':>15} {'DIV1':>15} {'NHM':>15} {'Total':>15}")
print(f"{'':30} {'(3555×328)':>15} {'(366×327)':>15} {'(674×209)':>15} {'':>15}")
print('-' * 150)
print(f"{'Max Possible Items':30} {baseline_sc:>15,} {baseline_div1:>15,} {baseline_nhm:>15,} {baseline_total:>15,}")
print()

# Store format distribution (constant)
print(f"{'Store Count':30} {3555:>15,} {366:>15,} {674:>15,} {3555+366+674:>15,}")
print(f"{'Questions per Format':30} {328:>15,} {327:>15,} {209:>15,} {328+327+209:>15,}")
print()

print()
print()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print('=' * 150)
print('TREND ANALYSIS')
print('=' * 150)
print()

if len(weekly_data) > 1:
    first_week = weekly_data[0]
    last_week = weekly_data[-1]
    
    print(f"First Week (WK1):")
    print(f"  Date: {first_week['date']}")
    print(f"  Stores: {first_week['stores']:,}")
    print(f"  Assigned: {first_week['assigned']:,}")
    print(f"  Completed: {first_week['completed']:,}")
    print(f"  Completion %: {(first_week['completed'] / first_week['assigned'] * 100):.1f}%")
    print()
    
    print(f"Last Week (WK{last_week['week']}):")
    print(f"  Date: {last_week['date']}")
    print(f"  Stores: {last_week['stores']:,}")
    print(f"  Assigned: {last_week['assigned']:,}")
    print(f"  Completed: {last_week['completed']:,}")
    print(f"  Completion %: {(last_week['completed'] / last_week['assigned'] * 100):.1f}%")
    print()
    
    store_change = last_week['stores'] - first_week['stores']
    assigned_change = last_week['assigned'] - first_week['assigned']
    completed_change = last_week['completed'] - first_week['completed']
    
    print(f"WK1 → WK{last_week['week']} Change:")
    print(f"  Store Count: {store_change:+,} ({(store_change/first_week['stores']*100):+.1f}%)")
    print(f"  Assigned Items: {assigned_change:+,} ({(assigned_change/first_week['assigned']*100):+.1f}%)")
    print(f"  Completed Items: {completed_change:+,} ({(completed_change/first_week['completed']*100):+.1f}%)")
    print()

print('=' * 150)
print()
