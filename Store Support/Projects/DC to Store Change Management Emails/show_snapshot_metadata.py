#!/usr/bin/env python3
"""Regenerate May 1 snapshot with enhanced audit trail."""
import json
from elm_data_fetcher import save_elm_snapshot

print('\nRegenerating May 1 snapshot with enhanced audit trail metadata...\n')
snapshot_file = save_elm_snapshot('2026-05-01')

# Load and display metadata
data = json.loads(open(snapshot_file).read())

print('\n' + '='*80)
print('SNAPSHOT METADATA - FOR AUDIT TRAIL & FUTURE REFERENCE')
print('='*80)
print(f'\nSnapshot ID:              {data.get("snapshot_id")}')
print(f'Date:                     {data.get("date")}')
print(f'Generated (UTC):          {data.get("generation_time_utc")}')
print(f'Generated (Local):        {data.get("generation_time_local")}')
print()
print('DATA QUALITY:')
print(f'  Total Locations:        {data["data_quality"]["total_locations"]:,}')
print(f'  Managers with Email:    {data["data_quality"]["managers_with_email"]:,}')
print(f'  Email Coverage:         {data["data_quality"]["email_coverage_pct"]}%')
print()
print('ROLES DISTRIBUTION:')
for role, count in data["data_quality"]["roles_distribution"].items():
    print(f'  {role.replace("_", " ").title()}: {count:,}')
print()
print('FILTERING CRITERIA APPLIED:')
for criterion, value in data["filters_applied"].items():
    print(f'  • {criterion.replace("_", " ").title()}: {value}')
print()
print('AUDIT TRAIL:')
for key, value in data["audit_info"].items():
    print(f'  {key.replace("_", " ").title()}: {value}')
print()
print('='*80)
print(f'✓ Snapshot ready for reference: {data["audit_info"]["snapshot_reference"]}')
print('='*80)
