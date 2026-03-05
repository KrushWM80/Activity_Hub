#!/usr/bin/env python3
"""
Copy WK7 dashboard v3 to WK8 and update with 2/28 metrics
"""

import shutil
from pathlib import Path

# Paths
wk7_file = Path(r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Refresh Guide\business-overview-dashboard-v3-2-23-26.html")
wk8_file = Path(r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Refresh Guide\business-overview-dashboard-v3-2-28-26.html")

print("=" * 100)
print("CREATING WK8 DASHBOARD FROM WK7 TEMPLATE")
print("=" * 100)
print()

# Copy file
print(f"📋 Copying WK7 template...")
print(f"   From: {wk7_file.name}")
print(f"   To:   {wk8_file.name}")

shutil.copy2(wk7_file, wk8_file)
print(f"✓ File copied")
print()

# Read the new WK8 file
print(f"📖 Reading WK8 file...")
with open(wk8_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✓ File read ({len(content):,} characters)")
print()

# Update metrics in summary section
print("🔄 Updating metrics...")
print()

updates = [
    # Date references
    ('2-23-26', '2-28-26', 'date references'),
    ('2/23/26', '2/28/26', 'formatted dates'),
    ('February 23, 2026', 'February 28, 2026', 'long date format'),
    
    # Summary metrics
    ('"totalAssignedItems": 1387578', '"totalAssignedItems": 1240922', 'totalAssignedItems'),
    ('"totalCompletedItems": 1111851', '"totalCompletedItems": 1117646', 'totalCompletedItems'),
    ('"overallCompletionOfMax": "80.1"', '"overallCompletionOfMax": "90.1"', 'overallCompletionOfMax percentage'),
    ('"storesWithAssignments": 4459', '"storesWithAssignments": 4460', 'storesWithAssignments count'),
]

updated_count = 0
for old_str, new_str, description in updates:
    if old_str in content:
        count = content.count(old_str)
        content = content.replace(old_str, new_str)
        updated_count += count
        print(f"  ✓ {description:40} : {count:3d} replacements")
    else:
        print(f"  ⚠ {description:40} : NOT FOUND")

print()

# Write back the updated content
print(f"💾 Writing updated WK8 file...")
with open(wk8_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ File written ({len(content):,} characters)")
print()

print("=" * 100)
print("✅ WK8 DASHBOARD CREATED SUCCESSFULLY")
print("=" * 100)
print()
print(f"File: {wk8_file.name}")
print(f"Location: Store Support/Projects/Refresh Guide/")
print()
print("Updates Applied:")
print(f"  • Date: 2-23-26 → 2-28-26")
print(f"  • totalAssignedItems: 1,387,578 → 1,240,922")
print(f"  • totalCompletedItems: 1,111,851 → 1,117,646")
print(f"  • overallCompletionOfMax: 80.1% → 90.1%")
print(f"  • storesWithAssignments: 4,459 → 4,460")
print()
print(f"Total replacements made: {updated_count}")
print()
